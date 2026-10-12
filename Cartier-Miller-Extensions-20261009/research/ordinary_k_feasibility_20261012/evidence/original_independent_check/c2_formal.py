"""C2: canonical subgroup via the formal group of an integral lift E~ : y^2 = x^3 + A~ x + B~ over Z_p.

Formal group law (Silverman IV.1, a1=a2=a3=0, a4=A, a6=B), z = -x/y, w = -1/y, w = z^3 + A z w^2 + B w^3:
  lambda = sum_{n>=3} w_n h_{n-1}(z1,z2)       (h_m = complete homogeneous symmetric poly = (z2^n-z1^n)/(z2-z1))
  nu     = w(z1) - lambda z1
  F(z1,z2) = z1 + z2 + (2 A lambda nu + 3 B lambda^2 nu)/(1 + A lambda^2 + B lambda^3)     (inverse is z -> -z)
[p](z) by double-and-add, all arithmetic in (Z/p^R)[[z]] truncated at z^D (integral: no denominators anywhere).
f = [p](z)/z; Weierstrass preparation gives the monic distinguished polynomial g of degree p-1 whose roots are
the p-1 nonzero points of the canonical subgroup C (all of valuation 1/(p-1), straight Newton polygon).
sigma_C = sum x(z_i) = s_{-2} + sum_n c_n s_{2n} where x(z) = z^-2 + sum_{n>=1} c_n z^{2n},
  s_{-2} = (g1^2 - 2 g0 g2)/g0^2,  s_{2n} by Newton's identities.
"""
import sys, random
from fractions import Fraction
from common import *


def smul(a, b, D, m):
    """truncated product of power series (lists) mod z^D mod m"""
    r = [0] * D
    for i, x in enumerate(a[:D]):
        if x:
            lim = D - i
            for j, y in enumerate(b[:lim]):
                r[i + j] += x * y
    return [c % m for c in r]


def sinv(a, D, m):
    a0inv = pow(a[0], -1, m)
    r = [0] * D
    r[0] = a0inv
    for k in range(1, D):
        t = 0
        for j in range(1, min(k, len(a) - 1) + 1):
            t += a[j] * r[k - j]
        r[k] = (-t * a0inv) % m
    return r


def w_series(A, B, D, m):
    w = [0] * D
    w[3] = 1
    while True:
        w2 = smul(w, w, D, m)
        w3 = smul(w2, w, D, m)
        new = [0] * D
        new[3] = 1
        for k in range(D):
            if k >= 1:
                new[k] += A * w2[k - 1]
            new[k] += B * w3[k]
        new = [c % m for c in new]
        if new == w:
            return w
        w = new


def compose(w, f, D, m):
    """w(f) for w a power series, f with f(0)=0"""
    r = [0] * D
    for n in range(len(w) - 1, -1, -1):
        r = smul(r, f, D, m)
        r[0] = (r[0] + w[n]) % m
    return r


def fg_add(z1, z2, w, A, B, D, m):
    # lambda = sum_n w_n h_{n-1}(z1, z2),  h_0 = 1, h_k = z1 h_{k-1} + z2^k
    lam = [0] * D
    h = [1] + [0] * (D - 1)
    z2pow = [1] + [0] * (D - 1)
    for k in range(1, D):
        z2pow = smul(z2pow, z2, D, m)
        h = smul(z1, h, D, m)
        h = [(a + b) % m for a, b in zip(h, z2pow)]
        n = k + 1
        if n < D and w[n]:
            lam = [(a + w[n] * b) % m for a, b in zip(lam, h)]
    w1 = compose(w, z1, D, m)
    nu = [(a - b) % m for a, b in zip(w1, smul(lam, z1, D, m))]
    lam2 = smul(lam, lam, D, m)
    lam3 = smul(lam2, lam, D, m)
    num = [(2 * A * a + 3 * B * b) % m for a, b in zip(smul(lam, nu, D, m), smul(lam2, nu, D, m))]
    den = [(A * a + B * b) % m for a, b in zip(lam2, lam3)]
    den[0] = (den[0] + 1) % m
    q = smul(num, sinv(den, D, m), D, m)
    return [(a + b + c) % m for a, b, c in zip(z1, z2, q)]


def mult_series(n, A, B, D, m):
    w = w_series(A, B, D, m)
    z = [0, 1] + [0] * (D - 2)
    result = None
    base = z
    bits = bin(n)[2:]
    acc = z
    for b in bits[1:]:
        acc = fg_add(acc, acc, w, A, B, D, m)
        if b == '1':
            acc = fg_add(acc, z, w, A, B, D, m)
    return acc, w


def weierstrass_prep(f, d, D, m, iters):
    """f power series mod p^R with f_k in pZ for k<d, f_d unit. Return monic g (list, degree d)."""
    flow = f[:d] + [0] * (D - d)
    fhigh = f[d:] + [0] * d
    fhinv = sinv(fhigh, D, m)
    V = fhinv[:]
    for _ in range(iters):
        t = smul(flow, V, D, m)
        tau = t[d:] + [0] * d
        V = smul(fhinv, [((1 if i == 0 else 0) - tau[i]) % m for i in range(D)], D, m)
    fV = smul(f, V, D, m)
    g = fV[:d] + [1]
    # check: coefficients d+1.. of fV should vanish (up to truncation-affected tail)
    return g, fV


def vp(x, p):
    if x == 0:
        return 99
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def sigma_C(p, A, B, R=6, extra=2):
    d = p - 1
    D = (R + extra) * d + 2
    m = p ** R
    pz, w = mult_series(p, A, B, D + 3, m)
    pz, w = pz[:D], w[:D]
    assert pz[0] == 0 and pz[1] % m == p % m
    # mod p, [p](z) should be a series in z^p with unit z^p coefficient (ordinary)
    assert all(pz[k] % p == 0 for k in range(1, p))
    f = pz[1:] + [0]
    assert f[d] % p != 0, "not ordinary?"
    g, fV = weierstrass_prep(f, d, D, m, iters=R + 3)
    assert all(g[k] % p == 0 for k in range(d)) and vp(g[0], p) == 1
    # x(z) = z / w(z):  W1 = w/z^3, x = z^-2 * W1^{-1}
    W1 = w[3:] + [0, 0, 0]
    Xs = sinv(W1, D, m)  # x = z^-2 * Xs(z): coefficient of z^{2n} in x is Xs[2n+2]
    assert all(Xs[k] == 0 for k in range(1, D, 2))
    # power sums of roots of g (monic, degree d): Newton identities, s_k for k up to D
    e = [1] + [((-1) ** k * g[d - k]) % m for k in range(1, d + 1)]  # elementary symmetric
    S = [d % m]
    for k in range(1, D):
        t = 0
        for i in range(1, min(k, d) + 1):
            t += (-1) ** (i - 1) * e[i] * (S[k - i] if k - i > 0 else 0)
        if k <= d:
            t += (-1) ** (k - 1) * k * e[k]
        S.append(t % m)
    # s_{-2} as a Fraction (denominator g0^2, valuation 2)
    g0, g1, g2 = g[0], g[1], g[2]
    sm2 = Fraction(g1 * g1 - 2 * g0 * g2, g0 * g0)
    tot = sm2
    for n in range(1, (D - 3) // 2):
        cn = Xs[2 * n + 2]
        if 2 * n < D:
            tot += cn * S[2 * n]
    # tot is known modulo p^(R-2) (from the s_{-2} division) -- reduce to integer mod p^(R-2)
    mod = p ** (R - 2)
    if tot.denominator % p == 0:
        return None, ("sigma_C not p-integral", tot)
    sc = (tot.numerator * pow(tot.denominator, -1, mod)) % mod
    return sc, mod


if __name__ == "__main__":
    random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 11)
    p = int(sys.argv[1])
    nmodels = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    nlifts = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    R = 6
    rows = [r for r in load_targets() if r['p'] == p]
    random.shuffle(rows)
    rows = rows[:nmodels]
    out = open("c2_results.txt", "a")
    ok = total = 0
    fails = []
    for r in rows:
        A, B, kap = r['A'], r['B'], r['kappa']
        lifts = [(A, B)] + [(A + p * random.randrange(1, p ** 3), B + p * random.randrange(1, p ** 3)) for _ in range(nlifts)]
        vals = []
        for (At, Bt) in lifts:
            sc, mod = sigma_C(p, At, Bt, R=R)
            total += 1
            if sc is None:
                fails.append((A, B, At, Bt, mod))
                continue
            div = (sc % p == 0)
            val = (sc // p) % p if div else None
            vals.append((At, Bt, sc, vp(sc, p), (sc // p) % (mod // p) if div else None))
            if div and val == kap:
                ok += 1
            else:
                fails.append((A, B, At, Bt, sc, kap))
        line = f"p={p} (A,B)=({A},{B}) kappa={kap}: " + "; ".join(
            f"lift({a},{b}): sigma_C mod p^{R-2}={s} v_p={v} sigma_C/p mod p^{R-3}={q}" for a, b, s, v, q in vals)
        print(line)
        out.write(line + "\n")
    summ = f"SUMMARY C2 p={p}: {ok}/{total} (model,lift) pairs with p | sigma_C and sigma_C/p == kappa mod p; fails={fails[:5]}"
    print(summ)
    out.write(summ + "\n")
    out.close()
