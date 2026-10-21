"""cmbench.cmcs_v2 -- separately identified CORRECTED VARIANT of the inherited candidate.

The frozen candidate (inherited src/cmcs.py, SHA-256 763c8681...c59c) is imported unchanged and
subclassed; nothing in it is edited.  Changes, each tied to CORRECTIONS_AND_GATES.md:

  V2-1  Projective scope.  When N_inf = 0 (quartic with nonsquare leading coefficient) there are no
        F_p-rational points at infinity, so a polynomial weight is defined at every point of E(F_p)
        and the projective rational-point sum equals the affine sum.  The frozen API rejects this
        request; Curve2.weighted_sum accepts it (and still rejects it when N_inf > 0, where the
        weight has poles at rational points that would otherwise be included).
  V2-2  Endpoint check from the original chain.  Curve2.oracle_checked returns the same value as the
        inherited oracle and tests the necessary condition [M]R+ = [M]R- on the endpoint that the
        Miller chain already computes, instead of rerunning the chain (frozen endpoint_check).
        Passing the test does NOT certify the trace.
  V2-3  Complete common domain (statement fix, not a code fix).  weighted_sum already sums over
        x notin U with U = poles + excluded; Curve2 adds weighted_sum_U(U, coeffs, b) that takes U
        explicitly and requires every u in U to carry a (possibly zero) coefficient, matching the
        corrected theorem text.
"""
import os
import sys

from .methods import cmcs_module


def _load():
    cm = cmcs_module()
    from cm_system.backends.genus_one.fields import QuadCtx, FpCtx            # inherited
    from cm_system.backends.genus_one.miller import (miller_alpha_resumable,  # inherited
                                                     miller_continue, Resume)
    return cm, QuadCtx, FpCtx, miller_alpha_resumable, miller_continue, Resume


def make_curve2_class():
    cm, QuadCtx, FpCtx, miller_alpha_resumable, miller_continue, Resume = _load()

    class Curve2(cm.Curve):
        variant = 'cmcs_v2'

        def weighted_sum(self, simple=(), double=(), poly=(), b=0, excluded=(),
                         kind='character', check_endpoints=False):
            poly_nonconst = any(int(c) % self.p for c in list(poly)[1:])
            if kind == 'projective_points' and poly_nonconst and self.n_inf == 0:
                # V2-1: no rational points at infinity; projective sum = affine sum
                val, info = super().weighted_sum(simple, double, poly, b, excluded,
                                                 'affine_points', check_endpoints)
                info['projective_note'] = 'N_inf = 0: no rational points at infinity; equals affine sum'
                return val, info
            return super().weighted_sum(simple, double, poly, b, excluded, kind, check_endpoints)

        def weighted_sum_U(self, U, coeffs, b=0, kind='character'):
            """V2-3: U listed explicitly; coeffs[u] (possibly 0) required for every u in U."""
            U = list(U)
            if len(set(U)) != len(U):
                raise cm.InputError('U must consist of distinct residues')
            if set(coeffs) != set(U):
                raise cm.InputError('every u in U needs a (possibly zero) coefficient, and only those')
            simple = [(u, coeffs[u]) for u in U if coeffs[u] % self.p]
            excluded = [u for u in U if coeffs[u] % self.p == 0]
            return self.weighted_sum(simple=simple, b=b, excluded=excluded, kind=kind)

        def oracle_checked(self, mu, a):
            """V2-2: inherited oracle arithmetic, plus the endpoint test on the chain's own endpoint.
            Returns (C_f(mu), eps_f(mu), meta) exactly like Curve.oracle; raises TraceInconsistent
            when [M]R+ != [M]R-."""
            p = self.p
            s = self.session(a)
            nu = (mu - a) % p
            if nu == 0:
                raise cm.InputError('translation parameter coincides with the pole')
            lam = pow(nu, -1, p)
            model = s.model
            w = nu                                   # = 1/lam
            d = cm._peval(s.g, w, p)
            if d == 0:
                raise cm.UnsupportedCase('branch pole')
            chi = 1 if pow(d, (p - 1) // 2, p) == 1 else -1
            M = p + 1 - chi * s.trace_g
            k = QuadCtx(p, d)
            R = model.to_short(k, k.fromint(w), k.gen)
            split = False
            try:
                alpha, T = miller_alpha_resumable(k, R, M, model.A)
                ok = T is None or (T[0][1] % p == 0 and T[1][1] % p == 0)
                rphi = 2 * alpha[1] * pow(lam, -1, p) % p
            except Resume as z:
                split = True
                root = k.sqrt_from_witness(z.witness)
                F = FpCtx(p)

                def comp(e, i):
                    return (e[0] + (1 if i == 0 else -1) * e[1] * root) % p
                alphas, ends = [], []
                for i in (0, 1):
                    Ti = None if z.T is None else tuple(comp(e, i) for e in z.T)
                    Ri = tuple(comp(e, i) for e in R)
                    al, Te = miller_continue(F, Ri, M, model.A, Ti, comp(z.alpha, i), z.j)
                    alphas.append(al)
                    ends.append(Te)
                ok = ends[0] == ends[1]
                rphi = (alphas[0] - alphas[1]) * pow(lam * root, -1, p) % p
            if not ok:
                raise cm.TraceInconsistent('[M]R+ != [M]R-: supplied trace is wrong')
            rpsi = rphi * pow(model.kappa, -1, p) % p
            H = s.trace_g % p
            T_g = (H - chi * rpsi) % p
            gv = d
            gd = cm._peval(cm._deriv(s.g, p), nu, p)
            Cg = ((T_g - chi) * lam + chi * gd * pow(2 * gv, -1, p)) % p
            return s.alpha * Cg % p, s.alpha * chi, {'a': a, 'M': M, 'split': split,
                                                     'exceptional': M % p == 0, 'T_g': T_g}

        def single_pole_checked(self, mu):
            mu = cm.validate_residue(mu, self.p, 'mu')
            if self.is_branch(mu):
                return self.branch_value(mu)
            return self.oracle_checked(mu, self.choose_translation({mu}))[0]

    return Curve2
