import torch
from xitorch import LinearOperator
from typing import Union
from xitorch._utils.bcast import get_bcasted_dims
from xitorch._utils.misc import dummy_context_manager
from xitorch._utils.tensor import tallqr, to_fortran_order

def exacteig(A:LinearOperator, neig:Union[int,None],
        mode:str, M:Union[LinearOperator,None]):
    """
    Eigendecomposition using explicit matrix construction.
    No additional option for this method.

    Warnings
    --------
    * As this method construct the linear operators explicitly, it might requires
      a large memory.
    """
    Amatrix = A.fullmatrix() # (*BA, q, q)
    if neig is None:
        neig = A.shape[-1]
    if M is None:
        evals, evecs = torch.symeig(Amatrix, eigenvectors=True) # (*BA, q), (*BA, q, q)
        return _take_eigpairs(evals, evecs, neig, mode)
    else:
        Mmatrix = M.fullmatrix() # (*BM, q, q)

        # M decomposition to make A symmetric
        # it is done this way to make it numerically stable in avoiding
        # complex eigenvalues for (near-)degenerate case
        L = torch.cholesky(Mmatrix, upper=False) # (*BM, q, q)
        Linv = torch.inverse(L) # (*BM, q, q)
        LinvT = Linv.transpose(-2,-1) # (*BM, q, q)
        A2 = torch.matmul(Linv, torch.matmul(Amatrix, LinvT)) # (*BAM, q, q)

        # calculate the eigenvalues and eigenvectors
        # (the eigvecs are normalized in M-space)
        evals, evecs = torch.symeig(A2, eigenvectors=True) # (*BAM, q, q)
        evals, evecs = _take_eigpairs(evals, evecs, neig, mode) # (*BAM, neig) and (*BAM, q, neig)
        evecs = torch.matmul(LinvT, evecs)
        return evals, evecs

def davidson(A, params, neig, mode, M=None, mparams=[],
        max_niter=1000,
        nguess=None,
        v_init="randn",
        max_addition=None,
        min_eps=1e-6,
        verbose=False,
        **unused):
    """
    Using Davidson method for large sparse matrix eigendecomposition [1]_.

    Arguments
    ---------
    max_niter: int
        Maximum number of iterations
    nguess: int or None
        The number of initial guess of the eigenvectors
        If None, set to ``neig``.
    v_init: str
        Mode of the initial guess (``"randn"``, ``"rand"``, ``"eye"``)
    max_addition: int or None
        Maximum number of new guesses to be added to the collected vectors.
        If None, set to ``neig``.
    min_eps: float
        Minimum residual error to be stopped
    verbose: bool
        Option to be verbose

    References
    ----------
    .. [1] P. Arbenz, "Lecture Notes on Solving Large Scale Eigenvalue Problems"
           http://people.inf.ethz.ch/arbenz/ewp/Lnotes/chapter12.pdf
    """
    # TODO: optimize for large linear operator and strict min_eps
    # Ideas:
    # (1) use better strategy to get the estimate on eigenvalues
    # (2) use restart strategy

    if nguess is None:
        nguess = neig
    if max_addition is None:
        max_addition = neig

    # get the shape of the transformation
    na = A.shape[-1]
    if M is None:
        bcast_dims = A.shape[:-2]
    else:
        bcast_dims = get_bcasted_dims(A.shape[:-2], M.shape[:-2])
    dtype = A.dtype
    device = A.device

    # TODO: A to use params
    prev_eigvals = None
    prev_eigvalT = None
    stop_reason = "max_niter"
    shift_is_eigvalT = False
    idx = torch.arange(neig).unsqueeze(-1) # (neig, 1)

    with A.uselinopparams(*params), M.uselinopparams(*mparams) if M is not None else dummy_context_manager():
        # set up the initial guess
        V = _set_initial_v(v_init.lower(), dtype, device,
            bcast_dims, na, nguess,
            M=M, mparams=mparams) # (*BAM, na, nguess)
        # V = V.reshape(*bcast_dims, na, nguess) # (*BAM, na, nguess)

        # estimating the lowest eigenvalues
        eig_est, rms_eig = _estimate_eigvals(A, neig, mode,
            bcast_dims=bcast_dims, na=na, ntest=20,
            dtype=V.dtype, device=V.device)

        best_resid = float("inf")
        AV = A.mm(V)
        for i in range(max_niter):
            VT = V.transpose(-2,-1) # (*BAM,nguess,na)
            # Can be optimized by saving AV from the previous iteration and only
            # operate AV for the new V. This works because the old V has already
            # been orthogonalized, so it will stay the same
            # AV = A.mm(V) # (*BAM,na,nguess)
            T = torch.matmul(VT, AV) # (*BAM,nguess,nguess)

            # eigvals are sorted from the lowest
            # eval: (*BAM, nguess), evec: (*BAM, nguess, nguess)
            eigvalT, eigvecT = torch.symeig(T, eigenvectors=True)
            eigvalT, eigvecT = _take_eigpairs(eigvalT, eigvecT, neig, mode) # (*BAM, neig) and (*BAM, nguess, neig)

            # calculate the eigenvectors of A
            eigvecA = torch.matmul(V, eigvecT) # (*BAM, na, neig)

            # calculate the residual
            AVs = torch.matmul(AV, eigvecT) # (*BAM, na, neig)
            LVs = eigvalT.unsqueeze(-2) * eigvecA # (*BAM, na, neig)
            if M is not None:
                LVs = M.mm(LVs)
            resid = AVs - LVs # (*BAM, na, neig)

            # print information and check convergence
            max_resid = resid.abs().max()
            if prev_eigvalT is not None:
                deigval = eigvalT - prev_eigvalT
                max_deigval = deigval.abs().max()
                if verbose:
                    print("Iter %3d (guess size: %d): resid: %.3e, devals: %.3e" % \
                          (i+1, nguess, max_resid, max_deigval))

            if max_resid < best_resid:
                best_resid = max_resid
                best_eigvals = eigvalT
                best_eigvecs = eigvecA
            if max_resid < min_eps:
                break
            if AV.shape[-1] == AV.shape[-2]:
                break
            prev_eigvalT = eigvalT

            # apply the preconditioner
            # initial guess of the eigenvalues are actually help really much
            if not shift_is_eigvalT:
                z = eig_est # (*BAM,neig)
            else:
                z = eigvalT # (*BAM,neig)
            # if A.is_precond_set():
            #     t = A.precond(-resid, *params, biases=z, M=M, mparams=mparams) # (nbatch, na, neig)
            # else:
            t = -resid # (*BAM, na, neig)

            # set the estimate of the eigenvalues
            if not shift_is_eigvalT:
                eigvalT_pred = eigvalT + torch.einsum('...ae,...ae->...e', eigvecA, A.mm(t)) # (*BAM, neig)
                diff_eigvalT = (eigvalT - eigvalT_pred) # (*BAM, neig)
                if diff_eigvalT.abs().max() < rms_eig*1e-2:
                    shift_is_eigvalT = True
                else:
                    change_idx = eig_est > eigvalT
                    next_value = eigvalT - 2*diff_eigvalT
                    eig_est[change_idx] = next_value[change_idx]

            # orthogonalize t with the rest of the V
            t = to_fortran_order(t)
            Vnew = torch.cat((V, t), dim=-1)
            if Vnew.shape[-1] > Vnew.shape[-2]:
                Vnew = Vnew[...,:Vnew.shape[-2]]
            nadd = Vnew.shape[-1] - V.shape[-1]
            nguess = nguess + nadd
            if M is not None:
                MV_ = M.mm(Vnew)
                V, R = tallqr(Vnew, MV=MV_)
            else:
                V, R = tallqr(Vnew)
            AVnew = A.mm(V[...,-nadd:]) # (*BAM,na,nadd)
            AVnew = to_fortran_order(AVnew)
            AV = torch.cat((AV, AVnew), dim=-1)

    eigvals = best_eigvals # (*BAM, neig)
    eigvecs = best_eigvecs # (*BAM, na, neig)
    return eigvals, eigvecs

def _set_initial_v(vinit_type, dtype, device, batch_dims, na, nguess,
                   M=None, mparams=None):
    torch.manual_seed(12421)
    if vinit_type == "eye":
        nbatch = functools.reduce(lambda x,y: x*y, bcast_dims, 1)
        V = torch.eye((na, nguess), dtype=dtype, device=device).unsqueeze(0).repeat(nbatch,1,1).reshape(*batch_dims, na, nguess)
    elif vinit_type == "randn":
        V = torch.randn((*batch_dims, na, nguess), dtype=dtype, device=device)
    elif vinit_type == "random" or vinit_type == "rand":
        V = torch.rand((*batch_dims, na, nguess), dtype=dtype, device=device)
    else:
        raise ValueError("Unknown v_init type: %s" % vinit_type)

    # orthogonalize V
    if M is not None:
        V, R = tallqr(V, MV=M.mm(V))
    else:
        V, R = tallqr(V)
    return V

def _estimate_eigvals(A, neig, mode, bcast_dims, na, ntest, dtype, device):
    # estimate the lowest eigen value
    x = torch.randn((*bcast_dims, na, ntest), dtype=dtype, device=device) # (*BAM, na, ntest)
    x = x / x.norm(dim=-2, keepdim=True)
    Ax = A.mm(x) # (*BAM, na, ntest)
    xTAx = (x * Ax).sum(dim=-2) # (*BAM, ntest)
    mean_eig = xTAx.mean(dim=-1) # (*BAM,)
    std_f = (xTAx).std(dim=-1) # (*BAM,)
    std_x2 = (x*x).std()
    rms_eig = (std_f / std_x2) / (na**0.5) # (*BAM,)
    if mode == "lowest":
        eig_est = mean_eig - 2*rms_eig # (*BAM,)
    else: # uppest
        eig_est = mean_eig + 2*rms_eig # (*BAM,)
    eig_est = eig_est.unsqueeze(-1).repeat_interleave(repeats=neig, dim=-1) # (*BAM,neig)
    return eig_est, rms_eig.max()

def _take_eigpairs(eival, eivec, neig, mode):
    # eival: (*BV, na)
    # eivec: (*BV, na, na)
    if mode == "lowest":
        eival = eival[...,:neig]
        eivec = eivec[...,:neig]
    else: # uppest
        eival = eival[...,-neig:]
        eivec = eivec[...,-neig:]
    return eival, eivec
