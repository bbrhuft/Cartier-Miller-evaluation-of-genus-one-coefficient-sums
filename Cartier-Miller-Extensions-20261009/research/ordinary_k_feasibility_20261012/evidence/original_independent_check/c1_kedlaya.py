"""C1, route 2: Kedlaya / Monsky-Washnitzer computation of the p-adic Frobenius matrix on
H^1_MW(E')^- with basis {dx/y, x dx/y} for y^2 = Q(x) = x^3 + A x + B over Z_p (sigma = id),
then reduction mod p.  Column convention: Frob(omega, eta) = (omega, eta) M.

Frobenius lift: x -> x^p, 1/y -> y^{-p} (1 + E y^{-2p})^{-1/2}, E = Q(x^p) - Q(x)^p.
  Frob(x^i dx/y) = sum_k p binom(-1/2,k) x^{p(i+1)-1} E^k y^{-p(2k+1)} dx.
Reductions (exact identities in MW cohomology):
  A dx/y^{2s+1} = U dx/y^{2s-1} + V Q' dx/y^{2s+1},   V Q' dx/y^{2s+1} == (2/(2s-1)) V' dx/y^{2s-1}
  x^m dx/y == -[A (2m-3) x^{m-2} + 2 (m-2) B x^{m-3}]/(2m-1) dx/y      (m >= 2)
p-adic bookkeeping: a form is p^e * poly with poly mod p^MW; a division by p^v u lowers e by v.
Self-checks: trace(M) = t (mod p^N), det(M) = p (mod p^N), stability in (K, MW).
"""
import sys
from fractions import Fraction
from math import comb
from common import *


def inv_mod_poly(a, Q, m, p):
    """inverse of a modulo monic Q over Z/m, m = p^k; extended Euclid mod p then Newton lifting."""
    # mod p inverse via extended Euclid
    def egcd(a, b):
        # returns (g, s) with s*a == g mod b, polys over F_p
        r0, r1 = ptrim([x % p for x in b]), ptrim([x % p for x in a])
        s0, s1 = [], [1]
        while r1:
            lc = pow(r1[-1], -1, p)
            q = []
            r = r0[:]
            dq = len(r) - len(r1)
            q = [0] * (max(dq, 0) + 1)
            while r and len(r) >= len(r1):
                c = (r[-1] * lc) % p
                sh = len(r) - len(r1)
                q[sh] = c
                for j in range(len(r1)):
                    r[sh + j] = (r[sh + j] - c * r1[j]) % p
                ptrim(r)
            r0, r1 = r1, r
            s0, s1 = s1, psub(s0, pmul(ptrim(q), s1, p), p)
        return r0, s0
    g, s = egcd(a, Q)
    assert len(g) == 1
    s = pscale(s, pow(g[0], -1, p), p)
    T = s
    prec = p
    while prec < m:
        prec = min(prec * prec, m)
        # T <- T (2 - a T) mod Q
        aT = pdivmod_monic(pmul(a, T, prec), Q, prec)[1]
        two_minus = psub([2], aT, prec)
        T = pdivmod_monic(pmul(T, two_minus, prec), Q, prec)[1]
    return [x % m for x in T]


def vsplit(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v, n


def reduce_form(e, poly, s, p, A, B, MW, Q, dQ, T):
    """Reduce p^e * poly dx / y^{2s+1} to p^e' (a0 + a1 x) dx/y.  Returns (e', a0, a1)."""
    m = p ** MW
    poly = [x % m for x in poly]
    inv2 = pow(2, -1, m)
    while s >= 1:
        # V = poly * T mod Q ; U = (poly - V Q')/Q
        r = pdivmod_monic(poly, Q, m)[1]
        V = pdivmod_monic(pmul(r, T, m), Q, m)[1]
        U, rem = pdivmod_monic(psub(poly, pmul(V, dQ, m), m), Q, m)
        assert not rem
        v, u = vsplit(2 * s - 1, p)
        newp = padd(pscale(U, p ** v, m), pscale(pderiv(V, m), 2 * pow(u, -1, m), m), m)
        e -= v
        poly = newp
        s -= 1
    # s = 0: reduce degree
    poly = poly[:]
    while len(poly) > 2:
        mdeg = len(poly) - 1
        c = poly[mdeg] % m
        poly.pop()
        if c:
            v, u = vsplit(2 * mdeg - 1, p)
            # x^m == -[A(2m-3) x^{m-2} + 2(m-2) B x^{m-3}] / (2m-1)
            if v:
                poly = [(x * p ** v) % m for x in poly]
                e -= v
            cu = (c * pow(u, -1, m)) % m
            poly[mdeg - 2] = (poly[mdeg - 2] - cu * A * (2 * mdeg - 3)) % m
            poly[mdeg - 3] = (poly[mdeg - 3] - cu * 2 * (mdeg - 2) * B) % m
        ptrim(poly)
    return e, coeff(poly, 0), coeff(poly, 1)


def binom_mhalf(k):
    # binom(-1/2, k) = (-1)^k C(2k,k)/4^k
    return Fraction((-1) ** k * comb(2 * k, k), 4 ** k)


def frob_matrix(p, A, B, K, MW):
    """Return (M as Fractions, precision exponent) for lift (A,B) in Z."""
    m = p ** MW
    Q = [B, A, 0, 1]
    dQ = [A, 0, 3]
    T = inv_mod_poly(dQ, Q, m, p)
    # E = Q(x^p) - Q(x)^p over Z, divided by p
    Qp = [0] * (3 * p + 1)
    Qp[0] += B; Qp[p] += A; Qp[3 * p] += 1
    Qpow = [1]
    for _ in range(p):
        Qpow = [x for x in pmul_Z(Qpow, Q)]
    E = [(Qp[i] if i < len(Qp) else 0) - (Qpow[i] if i < len(Qpow) else 0) for i in range(max(len(Qp), len(Qpow)))]
    assert all(x % p == 0 for x in E)
    E1 = [x // p for x in E]
    cols = []
    precs = []
    for i in (0, 1):
        tot0 = Fraction(0)
        tot1 = Fraction(0)
        Ek = [1]
        for k in range(K + 1):
            b = binom_mhalf(k)
            bm = (b.numerator * pow(b.denominator, -1, m)) % m
            poly = [0] * (p * (i + 1) - 1) + [x % m for x in Ek]
            poly = pscale(poly, bm, m)
            s = (p * (2 * k + 1) - 1) // 2
            e, a0, a1 = reduce_form(1 + k, poly, s, p, A, B, MW, Q, dQ, T)
            precs.append(e + MW)
            tot0 += Fraction(a0) * Fraction(p) ** e
            tot1 += Fraction(a1) * Fraction(p) ** e
            Ek = pmul(Ek, E1, m)
        cols.append((tot0, tot1))
    M = [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]
    return M, min(precs)


def pmul_Z(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def fr_mod(x, mod, p):
    """Fraction with p-integral value -> int mod `mod`; raise if not p-integral."""
    d = x.denominator
    if d % p == 0:
        raise ValueError("non-integral entry %s" % x)
    return (x.numerator * pow(d, -1, mod)) % mod


if __name__ == "__main__":
    import random
    p = int(sys.argv[1])
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    K = N + 2
    MW = N + 4
    models = all_models(p)
    sample = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    if sample:
        random.seed(7)
        random.shuffle(models)
        models = models[:sample]
    out = open("c1_kedlaya_results.txt", "a")
    ok = 0
    nint = 0
    fails = []
    stab = 0
    for A, B in models:
        M, prec = frob_matrix(p, A, B, K, MW)
        mod = p ** N
        try:
            Mi = [[fr_mod(M[r][c], mod, p) for c in range(2)] for r in range(2)]
        except ValueError as ex:
            fails.append((A, B, "nonintegral", str(ex)))
            continue
        nint += 1
        t = trace(p, A, B)
        tr = (Mi[0][0] + Mi[1][1]) % mod
        det = (Mi[0][0] * Mi[1][1] - Mi[0][1] * Mi[1][0]) % mod
        H, beta = hasse_beta(p, A, B)
        Mp = [[x % p for x in row] for row in Mi]
        good = (tr == t % mod) and (det == p % mod) and Mp == [[0, (-beta) % p], [0, H]]
        # stability: recompute with larger K, MW
        if len(models) <= 60 or random.random() < 0.1:
            M2, _ = frob_matrix(p, A, B, K + 2, MW + 2)
            Mi2 = [[fr_mod(M2[r][c], mod, p) for c in range(2)] for r in range(2)]
            if Mi2 != Mi:
                good = False
                fails.append((A, B, "unstable", Mi, Mi2))
            else:
                stab += 1
        if good:
            ok += 1
        else:
            fails.append((A, B, Mi, tr, t, det, H, beta))
    line = (f"p={p} N={N} K={K} MW={MW}: models={len(models)}, integral={nint}, "
            f"[trace==t, det==p mod p^{N}, M mod p == [[0,-beta],[0,H]]] ok={ok}; stability rechecks passed={stab}; fails={fails[:4]}")
    print(line)
    out.write(line + "\n")
    out.close()
