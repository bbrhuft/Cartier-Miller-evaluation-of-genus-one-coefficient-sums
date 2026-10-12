"""C1, route 1: direct Cech-de Rham computation of absolute Frobenius F^* on H^1_dR(E/F_p).

Cover: U1 = E - {O} (affine), U2 = E - {y=0} (contains O).  A 1-cocycle is (w1, w2; f12) with
w1 - w2 = d f12 on U12; coboundary of (a1,a2) is (da1, da2, a1 - a2).
  [omega] = (dx/y, dx/y; 0)
  [eta]   = (x dx/y, x dx/y - d f, f)   with f = c x^2/y, c chosen (by Laurent expansion at O)
            so that x dx/y - d f is regular at O ("low-pole" representative, pole order 1 at O).
Absolute Frobenius acts componentwise: F^*(w1,w2;f) = (F^*w1, F^*w2; f^p) = (0, 0; f^p).
So F^*[omega] = 0 identically and F^*[eta] = (0,0; f^p).  We decompose
  f^p = M22 * f + (a1 - a2),  a1 in O(U1), a2 in O(U2),
where M22 is found with the Serre-duality functional  [g] -> Res_O(g dx/y)  on H^1(O)
(computed with Laurent series in z = -x/y), then the remaining class is (-M22 eta - d a1, ..., 0),
a global regular form which must equal lambda*dx/y; then F^*[eta] = lambda[omega] + M22[eta].
Everything is checked (regularity, constancy of lambda), nothing is assumed.
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # explicit: python -I omits the script directory

import sys
from common import *


# ---------- Laurent series at O over F_p, parameter z = -x/y ----------
class Laurent:
    """Truncated Laurent series: val (lowest exponent) + list of coefficients, absolute precision `prec`
    (exponent up to which coefficients are known, exclusive)."""

    def __init__(self, val, coeffs, prec, p):
        self.v, self.c, self.prec, self.p = val, [x % p for x in coeffs], prec, p

    def coef(self, k):
        i = k - self.v
        return self.c[i] if 0 <= i < len(self.c) and k < self.prec else 0

    def __add__(s, o):
        p = s.p
        v = min(s.v, o.v)
        prec = min(s.prec, o.prec)
        return Laurent(v, [(s.coef(k) + o.coef(k)) % p for k in range(v, prec)], prec, p)

    def __neg__(s):
        return Laurent(s.v, [-x for x in s.c], s.prec, s.p)

    def __sub__(s, o):
        return s + (-o)

    def scale(s, a):
        return Laurent(s.v, [a * x for x in s.c], s.prec, s.p)

    def __mul__(s, o):
        p = s.p
        v = s.v + o.v
        # relative precisions
        prec = min(s.prec + o.v, o.prec + s.v)
        n = prec - v
        r = [0] * max(n, 0)
        for i, a in enumerate(s.c):
            if a and i < n:
                for j, b in enumerate(o.c):
                    if i + j >= n:
                        break
                    r[i + j] += a * b
        return Laurent(v, r, prec, p)

    def normalize(s):
        while s.c and s.c[0] % s.p == 0:
            s.c.pop(0)
            s.v += 1
        return s

    def inv(s):
        s = Laurent(s.v, s.c[:], s.prec, s.p).normalize()
        p = s.p
        n = s.prec - s.v  # relative precision
        a0inv = pow(s.c[0], -1, p)
        r = [0] * n
        r[0] = a0inv
        for k in range(1, n):
            t = 0
            for j in range(1, k + 1):
                if j < len(s.c):
                    t += s.c[j] * r[k - j]
            r[k] = (-t * a0inv) % p
        return Laurent(-s.v, r, -s.v + n, p)

    def deriv(s):
        p = s.p
        return Laurent(s.v - 1, [((s.v + i) * a) % p for i, a in enumerate(s.c)], s.prec - 1, p)

    def __pow__(s, e):
        r = Laurent(0, [1], 10 ** 9, s.p)
        for _ in range(e):
            r = r * s
        return r


def local_xy(p, A, B, prec):
    """x(z), y(z) as Laurent series over F_p with precision ~prec in z."""
    # w = z^3 + A z w^2 + B w^3, w power series in z, compute to degree prec+6
    N = prec + 12
    w = [0] * N
    w[3] = 1
    for _ in range(N):
        w2 = pmul(w, w, p)[:N]
        w3 = pmul(w2, w, p)[:N]
        new = [0] * N
        new[3] = 1
        for k in range(N):
            if k - 1 >= 0 and k - 1 < len(w2):
                new[k] += A * w2[k - 1]
            if k < len(w3):
                new[k] += B * w3[k]
        new = [c % p for c in new]
        if new == w:
            break
        w = new
    W = Laurent(0, w, N, p).normalize()
    z = Laurent(1, [1], 10 ** 9, p)
    Winv = W.inv()
    X = z * Winv
    Y = Winv.scale(-1)
    return X, Y


def form_res(L):
    return L.coef(-1)


def frobenius_cech(p, A, B, verbose=False):
    PREC = 6 * p + 20
    X, Y = local_xy(p, A, B, PREC)
    # sanity: Y^2 = X^3 + A X + B
    chk = Y * Y - (X * X * X + X.scale(A) + Laurent(0, [B], 10 ** 9, p))
    require(all(chk.coef(k) == 0 for k in range(chk.v, min(chk.prec, 30))), "local expansion wrong")
    dX = X.deriv()
    Yi = Y.inv()
    omega = dX * Yi                    # dx/y as series (coefficient of dz)
    eta = X * omega                    # x dx/y
    g0 = X * X * Yi                    # x^2/y
    dg0 = g0.deriv()
    # choose c with eta - c d(x^2/y) regular at O: kill z^-2 coefficient (z^-1 coefficient must already vanish)
    require(eta.v >= -2 and eta.coef(-1) == 0 and dg0.coef(-1) == 0, 'c1_cech.py:139: invariant failed')
    c = (eta.coef(-2) * pow(dg0.coef(-2), -1, p)) % p
    eta2 = eta - dg0.scale(c)
    require(all(eta2.coef(k) == 0 for k in range(eta2.v, 0)), "eta2 not regular at O")
    # --- algebraic side ---
    Q = F_poly(A, B, p)
    dQ = pderiv(Q, p)
    # eta2 regularity on the rest of U2 (y != 0): eta - c d(x^2/y) = [x Q - c(2xQ - x^2 Q'/2)]/ y^3 dx -> poly/y^3, fine.
    # f = c x^2 / y = c x^2 y / Q ;  g := f^p = c^p x^{2p} / y^p = c x^{2p} y / Q^{(p+1)/2}
    n = (p + 1) // 2
    cp = pow(c, p, p)
    # M22 via residue functional, computed with Laurent series
    gL = (g0 ** p).scale(cp)
    fL = g0.scale(c)
    r_g = form_res(gL * omega)
    r_f = form_res(fL * omega)
    require(r_f != 0, 'c1_cech.py:155: invariant failed')
    M22 = (r_g * pow(r_f, -1, p)) % p
    # h = g - M22 f = y * Nn / Q^n,  Nn = c x^{2p} - M22 c x^2 Q^{n-1}
    Nn = psub(pscale([0] * (2 * p) + [1], cp, p), pscale(pmul([0, 0, 1], ppow(Q, n - 1, p), p), M22 * c, p), p)
    Qn = ppow(Q, n, p)
    P, Rm = pdivmod_monic(Nn, Qn, p)
    # [h] = 0 in H^1(O) iff deg Rm <= 3n-2  (then Rm*y/Q^n is regular at O)
    require(coeff(Rm, 3 * n - 1) == 0, "residue functional inconsistent")
    # a1 = P*y (regular on U1), a2 = -Rm*y/Q^n (regular on U2).  mu = -M22*eta - d a1
    # d(P y) = (P' Q + P Q'/2) dx/y
    inv2 = pow(2, -1, p)
    dPy = padd(pmul(pderiv(P, p), Q, p), pscale(pmul(P, dQ, p), inv2, p), p)
    mu = psub(pscale([0, 1], -M22, p), dPy, p)  # coefficient poly of dx/y
    require(len(mu) <= 1, ("mu not constant multiple of dx/y", mu))
    lam = coeff(mu, 0) % p
    # independent cross-check of mu on U2: mu = -M22*eta2 - d a2 must be regular at O and equal lam*omega there
    a2L = None
    # build a2 as Laurent series: -Rm(X) * Y / Q(X)^n
    def polyL(poly):
        r = Laurent(0, [0], PREC, p)
        Xk = Laurent(0, [1], 10 ** 9, p)
        for k, a in enumerate(poly):
            if a:
                r = r + Xk.scale(a)
            Xk = Xk * X
        return r
    QL = polyL(Q)
    a2L = (polyL(Rm) * Y * (QL ** n).inv()).scale(-1)
    mu2 = eta2.scale(-M22) - a2L.deriv()
    diff = mu2 - omega.scale(lam)
    require(all(diff.coef(k) == 0 for k in range(diff.v, 8)), "U2-side check failed")
    # Matrix, column convention F^*(omega,eta) = (omega,eta) M
    M = [[0, lam], [0, M22]]
    return c, M


def _main():
    import random
    from harness import base_parser, Run, run_main
    ap = base_parser('C1 by Cech-de Rham cocycles: F* matrix vs [[0,-beta],[0,H]]')
    ap.add_argument('--primes', type=int, nargs='*', default=[7, 11, 13, 17, 19, 23],
                    help='primes checked exhaustively over all nonsingular models')
    ap.add_argument('--sample-primes', type=int, nargs='*', default=[], help='primes checked on a random sample')
    ap.add_argument('--sample-size', type=int, default=30)
    ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    scope = {'exhaustive_primes': a.primes, 'sample_primes': a.sample_primes, 'sample_size': a.sample_size,
             'seed': a.seed, 'models': 'all nonsingular short models, supersingular included'}

    def body(run):
        per_p = {}
        rng = random.Random(a.seed)
        jobs = [(p, all_models(p)) for p in a.primes]
        for p in a.sample_primes:
            models = all_models(p)
            rng.shuffle(models)
            jobs.append((p, models[:a.sample_size]))
        for p, models in jobs:
            cs, ok = set(), 0
            for A, B in models:
                c, M = frobenius_cech(p, A, B)
                cs.add(c)
                H, beta = hasse_beta(p, A, B)
                good = M == [[0, (-beta) % p], [0, H]]
                ok += good
                run.check(good, {'p': p, 'A': A, 'B': B, 'M': M, 'H': H, 'beta': beta}, group=f'p={p}')
            per_p[p] = {'models': len(models), 'matches': ok, 'primitive_multipliers_c': sorted(cs)}
            print(f'p={p}: {ok}/{len(models)} match; c values {sorted(cs)}', flush=True)
        run.note('per_prime', per_p)
        run.note('total_exhaustive_models', sum(per_p[p]['models'] for p in a.primes))

    run_main(lambda: Run('c1_cech', scope, a.out), body)


if __name__ == "__main__":
    _main()
