"""General-trace evaluation of C_f(a) from Voloch's characteristic-p zeta function (post-freeze,
separately hashed; NOT part of FREEZE.json; exploratory comparator for the prior-work audit).

Ingredients (Voloch 1997, as extracted; see SOURCE_LEDGER row V97):
  p. 2   y^{p-1} = f^{(p-1)/2} = U + A x^{p-1} + x^p T(x);  z on E^(p) with z^p - A z = -yT(x),
         the function field of E viewed inside that of E^(p) via Verschiebung V;
  Prop 2 z(P + Q) = z(P) + z(Q) + (y(Q) - y(P))/(x(Q) - x(P))   [x, y pulled back along V].
Deduction (REPORT section 4.4): for E/F_p ordinary with p not dividing n = #E(F_p), and a
rational P = (a, b), b != 0, let Q' = [p^{-1} mod n] P (so V(Q') = [p]Q' = P on rational points).
Then b T(a) = (A - 1) z(Q') and, when the chain avoids O, z(Q') = alpha_p(Q'), Miller's slope
accumulator for M = p (since p z(Q'') = 0 in F_p).  With Miller's conventions the same formula was
observed also when the chain passes through O.
Hence on the short model W of v^2 = g(z) (origin P+, R = image of P-), using the decomposition
1/z = h_R/2 - g_1/4 and sum_{P != O, R} h_R = -Y_R T_W(X_R) = -(A - 1) alpha(R'):
      C_g(0) = -(A - 1) alpha_m([p^{-1}]R) / 2 - (g_1/4)(n - 2),
and C_f(a) = chi(f(a)) C_g(0) after twisting by d in {1, f(a)} so that f~(a) is a square.
The exceptional case (twisted trace 1) uses the Semaev/descent formula instead.
Requires the exact trace (for n and A = tau mod p).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from cmbench import core
from cmbench.methods import connell_short, miller_transfer


def _add(P, Q, A, p):
    if P is None:
        return Q, 0, False
    if Q is None:
        return P, 0, False
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None, 0, True
    lam = ((3 * x1 * x1 + A) * pow(2 * y1, -1, p) if x1 == x2 else (y2 - y1) * pow(x2 - x1, -1, p)) % p
    x3 = (lam * lam - x1 - x2) % p
    return (x3, (lam * (x1 - x3) - y1) % p), lam, False


def _mul(P, k, A, p):
    R, Q = None, P
    while k:
        if k & 1:
            R = _add(R, Q, A, p)[0]
        Q = _add(Q, Q, A, p)[0]
        k >>= 1
    return R


def _alpha_clean(X, m, A, p):
    """Slope accumulator for [m]X; returns None if any intermediate multiple is O."""
    T, a = X, 0
    for bit in bin(m)[3:]:
        T, lam, v = _add(T, T, A, p)
        if v or T is None:
            return None
        a = (2 * a + lam) % p
        if bit == '1':
            T, lam, v = _add(T, X, A, p)
            if v or (T is None):
                return None
            a = (a + lam) % p
    return a


def value(p, f, a, tau, stats=None):
    f = [c % p for c in f]
    fa = core.peval(f, a, p)
    e = core.legendre(fa, p)
    if e == 0:
        raise ValueError('branch pole')
    d = 1 if e == 1 else fa
    taut = e * tau                       # trace of the twist by d
    ft = [c * d % p for c in f]
    fta = fa * d % p                     # a nonzero square
    g = [c * pow(fta, -1, p) % p for c in core.taylor_shift(ft, a, p)]
    Aw, Bw, R = connell_short(g, p)
    g1 = g[1]
    i2, i4 = pow(2, -1, p), pow(4, -1, p)
    if taut == 1:                        # exceptional: Voloch descent + Semaev (formula (A7))
        alpha, end = miller_transfer(R, p, Aw, p)
        if stats is not None:
            stats['route'] = 'exceptional'
        return e * (g1 * i2 - alpha * i2) % p
    n = p + 1 - taut
    Qp = _mul(R, pow(p, -1, n), Aw, p)   # Q' = [p^{-1}] R
    # Miller's conventions (vertical and identity steps contribute 0): alpha_p(Q') is the dlog
    # constant at O of f_{p,Q'}, div = p(Q') - (R) - (p-1)(O).  The z-derivation covers chains that
    # avoid O; chains through O are covered by the same formula empirically (53,504/53,504, p < 60).
    alpha, end = miller_transfer(Qp, p, Aw, p)
    if end != R:
        raise ArithmeticError('[p]Q\' != R: inconsistent trace')
    if stats is not None:
        stats['route'] = 'general'
        stats['chain_clean'] = _alpha_clean(Qp, p, Aw, p) is not None
    Cg = (-(taut - 1) * alpha * i2 - g1 * i4 * (n - 2)) % p
    return e * Cg % p


if __name__ == '__main__':
    import json, random
    sys.path.insert(0, os.environ.get('CM_HANDOVER_COMPARATORS', ''))
    import reference_comparators as Rf
    from cmbench import cases, methods as M
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    out = {'small_checks': 0, 'small_fail': 0, 'routes': {}, 'fallbacks': 0, 'note_fallbacks': 'count of general-route queries whose chain passes through O', 'large_checks': 0, 'large_fail': 0}
    for p in [q for q in range(11, 700) if core.is_prime_small(q)]:
        for d in (3, 4):
            for _ in range(2):
                f = cases.random_curve(rng, p, d)
                eps, fib, inv = Rf.character_tables(f, p)
                tau = 1 - core.n_infinity(f, p) - sum(eps)
                for a in rng.sample(range(p), min(p, 25)):
                    if eps[a] == 0:
                        continue
                    st = {}
                    v = value(p, f, a, tau, st)
                    out['small_checks'] += 1
                    out['routes'][st['route']] = out['routes'].get(st['route'], 0) + 1
                    out['fallbacks'] += (st.get('chain_clean') is False)
                    if v != Rf.direct_single(eps, inv, a, p):
                        out['small_fail'] += 1
    # large primes: compare with the frozen inherited candidate (trace by PARI)
    for bits in (30, 40, 50, 62):
        for d in (3, 4):
            for _ in range(5):
                p = cases.random_prime(rng, 1 << (bits - 1), 1 << bits)
                f = cases.random_curve(rng, p, d)
                tau = M.TraceProvider.trace(p, f)
                E = M.CmcsFrozen.prepare(p, f, trace=tau)
                for _ in range(4):
                    a = cases.random_pole(rng, p, f)
                    out['large_checks'] += 1
                    out['large_fail'] += value(p, f, a, tau) != E.single_pole(a)
    out['status'] = 'PASS' if not (out['small_fail'] or out['large_fail']) else 'FAIL'
    print(json.dumps(out))
    if len(sys.argv) > 1:
        json.dump(out, open(sys.argv[1], 'w'), indent=1)
