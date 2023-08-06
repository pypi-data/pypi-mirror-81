import warnings
import functools
from typing import Union, Optional, List, Callable, Tuple
import torch
import numpy as np
from xitorch import LinearOperator
from scipy.sparse.linalg import gmres
from xitorch._impls.optimize.root.rootsolver import broyden1
from xitorch._utils.misc import dummy_context_manager
from xitorch._utils.bcast import normalize_bcast_dims, get_bcasted_dims

def wrap_gmres(A, params, B, E=None, M=None, mparams=[],
        min_eps=1e-9,
        max_niter=None,
        **unused):
    """
    Using SciPy's gmres method to solve the linear equation.

    Keyword arguments
    -----------------
    min_eps: float
        Relative tolerance for stopping conditions
    max_niter: int or None
        Maximum number of iterations. If ``None``, default to twice of the
        number of columns of ``A``.
    """
    # A: (*BA, nr, nr)
    # B: (*BB, nr, ncols)
    # E: (*BE, ncols) or None
    # M: (*BM, nr, nr) or None

    # NOTE: currently only works for batched B (1 batch dim), but unbatched A
    assert len(A.shape) == 2 and len(B.shape) == 3, "Currently only works for batched B (1 batch dim), but unbatched A"

    # check the parameters
    msg = "GMRES can only do AX=B"
    assert A.shape[-2] == A.shape[-1], "GMRES can only work for square operator for now"
    assert E is None, msg
    assert M is None, msg

    nbatch, na, ncols = B.shape
    if max_niter is None:
        max_niter = 2*na

    B = B.transpose(-1,-2) # (nbatch, ncols, na)

    # convert the numpy/scipy
    with A.uselinopparams(*params):
        op = A.scipy_linalg_op()
        B_np = B.detach().cpu().numpy()
        res_np = np.empty(B.shape, dtype=np.float64)
        for i in range(nbatch):
            for j in range(ncols):
                x, info = gmres(op, B_np[i,j,:], tol=min_eps, atol=1e-12, maxiter=max_niter)
                if info > 0:
                    msg = "The GMRES iteration does not converge to the desired value "\
                          "(%.3e) after %d iterations" % \
                          (config["min_eps"], info)
                    warnings.warn(msg)
                res_np[i,j,:] = x

        res = torch.tensor(res_np, dtype=B.dtype, device=B.device)
        res = res.transpose(-1,-2) # (nbatch, na, ncols)
        return res

def cg(A:LinearOperator, params:List, B:torch.Tensor,
        E:Optional[torch.Tensor]=None,
        M:Optional[LinearOperator]=None,
        mparams:List=[],
        posdef:bool=False,
        precond:Optional[LinearOperator]=None,
        max_niter:Optional[int]=None,
        rtol:float=1e-6,
        atol:float=1e-8,
        eps:float=1e-12,
        **unused):
    r"""
    Solve the linear equations using Conjugate-Gradient (CG) method.

    Keyword arguments
    -----------------
    posdef: bool
        Indicating if the operation :math:`\mathbf{AX-MXE}` a positive
        definite for all columns and batches.
    precond: LinearOperator or None
        LinearOperator for the preconditioning. If None, no preconditioner is
        applied.
    max_niter: int or None
        Maximum number of iteration. If None, it is set to ``int(1.5 * A.shape[-1])``
    rtol: float
        Relative tolerance for stopping condition w.r.t. norm of B
    atol: float
        Absolute tolerance for stopping condition w.r.t. norm of B
    eps: float
        Substitute the absolute zero in the algorithm's denominator with this
        value to avoid nan.
    """
    def _safedenom(r, eps):
        r[r == 0] = eps
        return r

    def _dot(r, z):
        # r: (*BR, nr, nc)
        # z: (*BR, nr, nc)
        # return: (*BR, 1, nc)
        return torch.einsum("...rc,...rc->...c", r, z).unsqueeze(-2)

    with A.uselinopparams(*params), M.uselinopparams(*mparams) if M is not None else dummy_context_manager():
        nr = A.shape[-1]
        ncols = B.shape[-1]
        if max_niter is None:
            max_niter = int(1.5 * nr)

        # if B is all zeros, then return zeros
        batchdims = _get_batchdims(A, B, E, M)
        if torch.allclose(B, B*0, rtol=rtol, atol=atol):
            x0 = torch.zeros((*batchdims, nr, ncols), dtype=A.dtype, device=A.device)
            return x0

        # setup the preconditioning and the matrix problem
        precond_fcn = _setup_precond(precond)
        A_fcn, B2, col_swapped = _setup_linear_problem(A, B, E, M, posdef)

        # get the stopping matrix
        B_norm = B2.norm(dim=-2, keepdim=True) # (*BB, 1, nc)
        stop_matrix = torch.max(rtol * B_norm, atol * torch.ones_like(B_norm)) # (*BB, 1, nc)

        # prepare the initial guess (it's just all zeros)
        x0shape = (ncols, *batchdims, nr, 1) if col_swapped else (*batchdims, nr, ncols)
        xk = torch.zeros(x0shape, dtype=A.dtype, device=A.device)

        rk = B2 - A_fcn(xk) # (*, nr, nc)
        zk = precond_fcn(rk) # (*, nr, nc)
        pk = zk # (*, nr, nc)
        rkzk = _dot(rk, zk)
        converge = False
        for k in range(max_niter):
            Apk = A_fcn(pk)
            alphak = rkzk / _safedenom(_dot(pk, Apk), eps)
            xk_1 = xk + alphak * pk
            rk_1 = rk - alphak * Apk # (*, nr, nc)

            # check for the stopping condition
            resid = B2 - A_fcn(xk_1)
            resid_norm = resid.norm(dim=-2, keepdim=True)
            if torch.all(resid_norm < stop_matrix):
                converge = True
                break

            zk_1 = precond_fcn(rk_1)
            rkzk_1 = _dot(rk_1, zk_1)
            betak = rkzk_1 / _safedenom(rkzk, eps)
            pk_1 = zk_1 + betak * pk

            # move to the next index
            pk = pk_1
            zk = zk_1
            xk = xk_1
            rk = rk_1
            rkzk = rkzk_1

        if not converge:
            warnings.warn("Convergence is not achieved after %d iterations. "\
                "Max norm of resid: %.3e" % (max_niter, torch.max(resid_norm)))
        if col_swapped:
            # x: (ncols, *, nr, 1)
            xk_1 = xk_1.transpose(0, -1).squeeze(0) # (*, nr, ncols)
        return xk_1

@functools.wraps(broyden1)
def broyden1_solve(A, params, B, E=None, M=None, mparams=[], **options):
    return rootfinder_solve("broyden1", A, params, B, E, M, mparams, **options)

def rootfinder_solve(alg, A, params, B, E=None, M=None, mparams=[], **options):
    # using rootfinder algorithm
    with A.uselinopparams(*params), M.uselinopparams(*mparams) if M is not None else dummy_context_manager():
        nr = A.shape[-1]
        ncols = B.shape[-1]

        # set up the function for the rootfinding
        def fcn_rootfinder(xi):
            # xi: (*BX, nr*ncols)
            x = xi.reshape(*xi.shape[:-1], nr, ncols) # (*BX, nr, ncols)
            y = A.mm(x) - B # (*BX, nr, ncols)
            if E is not None:
                MX = M.mm(x) if M is not None else x
                MXE = MX * E.unsqueeze(-2)
                y = y - MXE # (*BX, nr, ncols)
            y = y.reshape(*xi.shape[:-1], -1) # (*BX, nr*ncols)
            return y

        # setup the initial guess (the batch dimension must be the largest)
        batchdims = _get_batchdims(A, B, E, M)
        x0 = torch.zeros((*batchdims, nr*ncols), dtype=A.dtype, device=A.device)

        if alg == "broyden1":
            x = broyden1(fcn_rootfinder, x0, **options)
        else:
            raise RuntimeError("Unknown method %s" % alg)
        x = x.reshape(*x.shape[:-1], nr, ncols)
        return x

def exactsolve(A:LinearOperator, B:torch.Tensor,
               E:Union[torch.Tensor,None],
               M:Union[LinearOperator,None]):
    """
    Solve the linear equation by contructing the full matrix of LinearOperators.

    Warnings
    --------
    * As this method construct the linear operators explicitly, it might requires
      a large memory.
    """
    # A: (*BA, na, na)
    # B: (*BB, na, ncols)
    # E: (*BE, ncols)
    # M: (*BM, na, na)
    if E is None:
        Amatrix = A.fullmatrix() # (*BA, na, na)
        x, _ = torch.solve(B, Amatrix) # (*BAB, na, ncols)
    elif M is None:
        Amatrix = A.fullmatrix()
        x = _solve_ABE(Amatrix, B, E)
    else:
        Mmatrix = M.fullmatrix() # (*BM, na, na)
        L = torch.cholesky(Mmatrix, upper=False) # (*BM, na, na)
        Linv = torch.inverse(L) # (*BM, na, na)
        LinvT = Linv.transpose(-2,-1) # (*BM, na, na)
        A2 = torch.matmul(Linv, A.mm(LinvT)) # (*BAM, na, na)
        B2 = torch.matmul(Linv, B) # (*BBM, na, ncols)

        X2 = _solve_ABE(A2, B2, E) # (*BABEM, na, ncols)
        x = torch.matmul(LinvT, X2) # (*BABEM, na, ncols)
    return x

def _solve_ABE(A:torch.Tensor, B:torch.Tensor, E:torch.Tensor):
    # A: (*BA, na, na) matrix
    # B: (*BB, na, ncols) matrix
    # E: (*BE, ncols) matrix
    na = A.shape[-1]
    BA, BB, BE = normalize_bcast_dims(A.shape[:-2], B.shape[:-2], E.shape[:-1])
    E = E.reshape(1, *BE, E.shape[-1]).transpose(0,-1) # (ncols, *BE, 1)
    B = B.reshape(1, *BB, *B.shape[-2:]).transpose(0,-1) # (ncols, *BB, na, 1)

    # NOTE: The line below is very inefficient for large na and ncols
    AE = A - torch.diag_embed(E.repeat_interleave(repeats=na, dim=-1), dim1=-2, dim2=-1) # (ncols, *BAE, na, na)
    r, _ = torch.solve(B, AE) # (ncols, *BAEM, na, 1)
    r = r.transpose(0,-1).squeeze(0) # (*BAEM, na, ncols)
    return r

def _get_batchdims(A:LinearOperator, B:torch.Tensor,
        E:Union[torch.Tensor,None],
        M:Union[LinearOperator,None]):

    batchdims = [A.shape[:-2], B.shape[:-2]]
    if E is not None:
        batchdims.append(E.shape[:-1])
        if M is not None:
            batchdims.append(M.shape[:-2])
    return get_bcasted_dims(*batchdims)

def _setup_precond(precond:Optional[LinearOperator]) -> Callable[[torch.Tensor], torch.Tensor]:
    if precond is None:
        precond_fcn = lambda x: x
    elif isinstance(precond, LinearOperator):
        precond_fcn = lambda x: precond.mm(x)
    return precond_fcn

def _setup_linear_problem(A:LinearOperator, B:torch.Tensor,
        E:Optional[torch.Tensor], M:Optional[LinearOperator],
        posdef:bool) -> Tuple[Callable[[torch.Tensor],torch.Tensor], torch.Tensor, bool]:

    # get the linear operator (including the MXE part)
    if E is None:
        A_fcn = lambda x: A.mm(x)
        AT_fcn = lambda x: A.rmm(x)
        B_new = B
        col_swapped = False
    else:
        # A: (*BA, nr, nr) linop
        # B: (*BB, nr, ncols)
        # E: (*BE, ncols)
        # M: (*BM, nr, nr) linop
        if M is None:
            BAs, BBs, BEs = normalize_bcast_dims(A.shape[:-2], B.shape[:-2], E.shape[:-1])
        else:
            BAs, BBs, BEs, BMs = normalize_bcast_dims(A.shape[:-2], B.shape[:-2],
                                                      E.shape[:-1], M.shape[:-2])
        E = E.reshape(*BEs, *E.shape[-1:])
        E_new = E.unsqueeze(0).transpose(-1, 0).unsqueeze(-1) # (ncols, *BEs, 1, 1)
        B = B.reshape(*BBs, *B.shape[-2:]) # (*BBs, nr, ncols)
        B_new = B.unsqueeze(0).transpose(-1, 0) # (ncols, *BBs, nr, 1)

        def A_fcn(x):
            # x: (ncols, *BX, nr, 1)
            Ax = A.mm(x) # (ncols, *BAX, nr, 1)
            Mx = M.mm(x) if M is not None else x # (ncols, *BMX, nr, 1)
            MxE = Mx * E_new # (ncols, *BMXE, nr, 1)
            return Ax - MxE

        def AT_fcn(x):
            # x: (ncols, *BX, nr, 1)
            ATx = A.rmm(x)
            MTx = M.rmm(x) if M is not None else x
            MTxE = MTx * E_new
            return ATx - MTxE

        col_swapped = True

    # get the linear operation if it is not a posdef (A -> AT.A)
    if posdef:
        return A_fcn, B_new, col_swapped
    else:
        def A_new_fcn(x):
            return AT_fcn(A_fcn(x))
        B2 = AT_fcn(B_new)
        return A_new_fcn, B2, col_swapped
