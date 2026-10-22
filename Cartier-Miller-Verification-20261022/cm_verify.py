#!/usr/bin/env python3
"""
Verification script for "Cartier--Miller evaluation of genus-one coefficient sums"
(Cartier_Miller_Paper_Rewrite_Corrected.tex, 22 October 2026). Checks the displayed
identities of the paper against direct computation and reproduces every number
quoted in the text; the full run is the paper's Table 2.

Usage:  python3 cm_verify.py            (full run; the paper's Table 2)
        python3 cm_verify.py --quick    (smaller samples, for a smoke test)

Pure Python 3 (3.8+), no dependencies. All arithmetic is exact modulo p.
Seeds: 20261022 for the checks inherited from the first rewrite (their counts are
unchanged), 2026102202 for the checks added in the corrected rewrite.
"""
import platform
import random
import sys
import time
from math import comb, isqrt

QUICK = "--quick" in sys.argv

# ----------------------------------------------------------------------------
# Basic field and polynomial helpers (coefficient lists, low degree first)
# ----------------------------------------------------------------------------

def inv(a, p):
    return pow(a % p, p - 2, p)

def leg(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1

def ev(f, x, p):
    r = 0
    for c in reversed(f):
        r = (r * x + c) % p
    return r

def deriv(f, p):
    return [(i * f[i]) % p for i in range(1, len(f))] or [0]

def pmul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] = (r[i + j] + x * y) % p
    return r

def ppow(f, e, p):
    r, b = [1], f[:]
    while e:
        if e & 1:
            r = pmul(r, b, p)
        b = pmul(b, b, p)
        e >>= 1
    return r

def squarefree(f, p):
    def trim(a):
        while a and a[-1] == 0:
            a.pop()
        return a
    def pmod(a, b):
        a = trim(a[:])
        while len(a) >= len(b) and a:
            c = a[-1] * inv(b[-1], p) % p
            s = len(a) - len(b)
            for i in range(len(b)):
                a[s + i] = (a[s + i] - c * b[i]) % p
            trim(a)
        return a
    a, b = trim(f[:]), trim(deriv(f, p))
    while b:
        a, b = b, pmod(a, b)
    return len(a) == 1

def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def proj_trace(f, p):
    """Exact trace p+1-#E(F_p) of the smooth projective model of v^2=f(w)
    (brute force; small p only)."""
    deg = len(f) - 1
    affine = sum(1 + leg(ev(f, x, p), p) for x in range(p))
    n_inf = 1 if deg == 3 else 1 + leg(f[4], p)
    return p + 1 - affine - n_inf

def high_block(f, p):
    """F = f^((p-1)/2) = T + x^p J ; returns (T, J)."""
    F = ppow(f, (p - 1) // 2, p)
    return F[:p] + [0] * max(0, p - len(F)), F[p:] or [0]

# ----------------------------------------------------------------------------
# Quadratic algebra F_p[s]/(s^2-d), used only for the structural theorem check
# ----------------------------------------------------------------------------

class Q:
    p = d = None
    def __init__(s, a, b=0):
        s.a, s.b = a % Q.p, b % Q.p
    def _c(o):
        return o if isinstance(o, Q) else Q(o)
    def __add__(s, o):
        o = Q._c(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s):
        return Q(-s.a, -s.b)
    def __sub__(s, o):
        o = Q._c(o); return Q(s.a - o.a, s.b - o.b)
    def __rsub__(s, o):
        return Q._c(o) - s
    def __mul__(s, o):
        o = Q._c(o)
        return Q(s.a * o.a + Q.d * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inverse(s):
        n = (s.a * s.a - Q.d * s.b * s.b) % Q.p
        if n == 0:
            raise ZeroDivisionError("zero divisor in quadratic algebra")
        ni = inv(n, Q.p)
        return Q(s.a * ni, -s.b * ni)
    def __truediv__(s, o):
        return s * Q._c(o).inverse()
    def __rtruediv__(s, o):
        return Q._c(o) / s
    def __eq__(s, o):
        o = Q._c(o); return s.a == o.a and s.b == o.b
    def iszero(s):
        return s.a == 0 and s.b == 0

# ----------------------------------------------------------------------------
# Algorithm 1: differentiated Miller chain
# ----------------------------------------------------------------------------

def miller_alpha_F(m, R, A, p):
    """Base-field chain. R=(X,Y) affine on Y^2=X^3+AX+B, or None for O.
    Returns (alpha_m(R), [m]R)."""
    def add(T, S):
        if T is None:
            return S, 0
        if S is None:
            return T, 0
        (x1, y1), (x2, y2) = T, S
        if x1 == x2:
            if (y1 + y2) % p == 0:
                return None, 0
            rho = (3 * x1 * x1 + A) * inv(2 * y1, p) % p
        else:
            rho = (y2 - y1) * inv(x2 - x1, p) % p
        x3 = (rho * rho - x1 - x2) % p
        y3 = (rho * (x1 - x3) - y1) % p
        return (x3, y3), rho
    T, al = R, 0
    for bit in bin(m)[3:]:
        T, rho = add(T, T)
        al = (2 * al + rho) % p
        if bit == "1":
            T, rho = add(T, R)
            al = (al + rho) % p
    return al, T

def miller_alpha_Q(m, R, A):
    """Same chain over the quadratic algebra (no splitting needed in tests:
    a zero divisor raises and the case is reported)."""
    def add(T, S):
        if T is None:
            return S, Q(0)
        if S is None:
            return T, Q(0)
        (x1, y1), (x2, y2) = T, S
        if x1 == x2:
            if (y1 + y2).iszero():
                return None, Q(0)
            rho = (3 * x1 * x1 + A) / (2 * y1)
        else:
            rho = (y2 - y1) / (x2 - x1)
        x3 = rho * rho - x1 - x2
        y3 = rho * (x1 - x3) - y1
        return (x3, y3), rho
    T, al = R, Q(0)
    for bit in bin(m)[3:]:
        T, rho = add(T, T)
        al = 2 * al + rho
        if bit == "1":
            T, rho = add(T, R)
            al = al + rho
    return al, T

# ----------------------------------------------------------------------------
# The evaluator of Theorem B / Corollary 4 (the recommended routine)
# ----------------------------------------------------------------------------

def twist_data(f, p, a):
    """Normalised model g(z)=f(a+z)/f(a), its short model (A_g,B_g) and the
    point R (image of (0,-1)), as in (4.2)."""
    fa = ev(f, a, p)
    assert fa != 0, "branch pole"
    g = [0] * 5
    for i, c in enumerate(f):
        for k in range(i + 1):
            g[k] = (g[k] + c * comb(i, k) * pow(a, i - k, p)) % p
    fi = inv(fa, p)
    g = [x * fi % p for x in g]
    g1, g2, g3, g4 = g[1:5]
    i3, i27 = inv(3, p), inv(27, p)
    Ag = (-4 * g4 + g1 * g3 - g2 * g2 * i3) % p
    Bg = (g3 * g3 - 8 * g2 * g4 * i3 + g1 * g1 * g4 - g1 * g2 * g3 * i3
          + 2 * pow(g2, 3, p) * i27) % p
    xR = (g1 * g1 * inv(4, p) - 2 * g2 * i3) % p
    yR = (-g3 + g1 * g2 * inv(2, p) - pow(g1, 3, p) * inv(8, p)) % p
    assert (yR * yR - (xR ** 3 + Ag * xR + Bg)) % p == 0
    return g, Ag, Bg, (xR, yR)

def C_fast(f, p, a, tau):
    """C_f(a) = sum_{x != a} chi(f(x))/(x-a) by (4.3); tau = exact trace of f."""
    eps = leg(ev(f, a, p), p)
    g, Ag, Bg, R = twist_data(f, p, a)
    N = p + 1 - eps * tau
    al, T = miller_alpha_F(N, R, Ag, p)
    assert T is None, "supplied trace is inconsistent"
    return eps * (-g[1] * inv(4, p) * (N - 2) - al * inv(2, p)) % p

def T_fast(f, p, mu, tau):
    """T_f(mu), T_f = f^((p-1)/2) mod x^p, by (4.5), for mu != 0 nonbranch."""
    fm = ev(f, mu, p)
    eps = leg(fm, p)
    g, Ag, Bg, R = twist_data(f, p, mu)
    N = p + 1 - eps * tau
    al, T = miller_alpha_F(N, R, Ag, p)
    assert T is None
    g1 = g[1]
    return eps * (1 - mu * N * g1 * inv(4, p) - mu * al * inv(2, p)) % p

# ----------------------------------------------------------------------------
# Direct (definition-level) quantities
# ----------------------------------------------------------------------------

def C_direct(f, p, a):
    return sum(leg(ev(f, x, p), p) * inv(x - a, p) for x in range(p) if x != a) % p

# ----------------------------------------------------------------------------
# Structural theorem (Theorem D) on the original model, via quadratic algebra
# ----------------------------------------------------------------------------

def structural_check(f, p, lam):
    """f(0)=1. Returns (ok, exceptional, (H,S,rPsi,eps,tau))."""
    Fh = ppow(f, (p - 1) // 2, p) + [0] * (2 * p)
    H = Fh[p - 1]
    S = sum(Fh[m] * pow(lam, p - 1 - m, p) for m in range(p)) % p
    tau = proj_trace(f, p)
    assert (tau - H) % p == 0
    mu = inv(lam, p)
    d = ev(f, mu, p)
    eps = leg(d, p)
    Q.p = p
    if eps == 1:
        r0 = next(t for t in range(p) if t * t % p == d)
        Q.d = 1
        v0 = Q(r0)
    else:
        Q.d = d
        v0 = Q(0, 1)
    f1, f2, f3, f4 = (f + [0] * 5)[1:5]
    a1 = Q(f1); a2 = Q(f2) - Q(f1) * f1 / 4; a3 = Q(2 * f3); a4 = Q(-4 * f4)
    a6 = a2 * a4
    b2 = a1 * a1 + 4 * a2; b4 = 2 * a4 + a1 * a3; b6 = a3 * a3 + 4 * a6
    A = b4 / 2 - b2 * b2 / 48
    B = b6 / 4 - b2 * b4 / 24 + b2 * b2 * b2 / 864
    def pt(w0, vv):
        x = (2 * (vv + 1) + f1 * w0) / (w0 * w0)
        y = (4 * (vv + 1) + 2 * (f1 * w0 + f2 * w0 * w0)
             - Q(f1 * f1) * w0 * w0 / 2) / (w0 * w0 * w0)
        X = x + b2 / 12
        Y = y + (a1 * x + a3) / 2
        assert Y * Y == X * X * X + A * X + B
        return (X, Y)
    Rp, Rm = pt(Q(mu), v0), pt(Q(mu), -v0)
    M = p + 1 - eps * tau
    ap, _ = miller_alpha_Q(M, Rp, A)
    am, _ = miller_alpha_Q(M, Rm, A)
    Psi = (ap - am) / (-2)          # kappa_omega = -2
    r = Q(1) / (Q(lam) * v0)
    rPsi = r * Psi
    pred = Q(H) - eps * rPsi
    assert pred.b == 0 and rPsi.b == 0
    return pred.a == S, tau == eps, (H, S, rPsi.a, eps, tau)

# ----------------------------------------------------------------------------
# Binomial applications
# ----------------------------------------------------------------------------

def a_seq(p, upto):
    """a_i = binom(2i,i) 8^{-i} mod p for i <= upto, by the ratio recurrence."""
    out = [1]
    for i in range(upto):
        out.append(out[-1] * (2 * i + 1) * inv(4 * (i + 1), p) % p)
    return out

def rounded_third_prefix(p):
    """B_L, L=(p+1)/3, p = 2 mod 3: one Miller chain, no point counting
    (trace of v^2 = 1 - w^3/2 is zero)."""
    assert p % 3 == 2 and p >= 5
    f = [1, 0, 0, (-inv(2, p)) % p]
    return T_fast(f, p, 1, 0)

def sqrt_minus_one(p):
    for c in range(2, p):
        if leg(c, p) == -1:
            return pow(c, (p - 1) // 4, p)

def cornacchia_u(p):
    """p = u^2 + s^2 with u odd, u = 1 mod 4."""
    r = sqrt_minus_one(p)
    a, b = p, r
    while b * b > p:
        a, b = b, a % b
    x, y = b, isqrt(p - b * b)
    u = x if x % 2 else y
    return u if u % 4 == 1 else -u

def quarter_point(p):
    """B_n, a_n, n=(p-1)/4, p = 1 mod 4, p >= 17: Gauss/CM trace + one chain."""
    assert p % 4 == 1 and p >= 17
    n = (p - 1) // 4
    u = cornacchia_u(p)
    a_n = 2 * u * inv(pow(8, n, p), p) % p
    tau = a_n if a_n <= p // 2 else a_n - p      # Hasse: |tau| < p/2
    f = [1, 0, 0, 0, (-inv(2, p)) % p]
    S = T_fast(f, p, 1, tau)                       # S_f(1) = B_n + a_n
    return (S - a_n) % p, a_n, tau


# ----------------------------------------------------------------------------
# Independent construction of Miller functions (added in the corrected rewrite)
# ----------------------------------------------------------------------------

def kernel_vector(M, p):
    """Nonzero vector of the right kernel of M over F_p; also returns its dimension."""
    rows, cols = len(M), len(M[0])
    M = [r[:] for r in M]
    piv_cols, r = [], 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if M[i][c] % p), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = inv(M[r][c], p)
        M[r] = [x * iv % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                fac = M[i][c]
                M[i] = [(x - fac * y) % p for x, y in zip(M[i], M[r])]
        piv_cols.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv_cols]
    if not free:
        return None, 0
    fc = free[0]
    v = [0] * cols
    v[fc] = 1
    for i, c in enumerate(piv_cols):
        v[c] = (-M[i][fc]) % p
    return v, len(free)

def series_mul(a, b, p, K):
    r = [0] * K
    for i, x in enumerate(a[:K]):
        if x:
            for j, y in enumerate(b[:K - i]):
                r[i + j] = (r[i + j] + x * y) % p
    return r

def series_inv(a, p, K):
    r = [0] * K
    r[0] = inv(a[0], p)
    for k in range(1, K):
        acc = sum(a[i] * r[k - i] for i in range(1, min(k, len(a) - 1) + 1)) % p
        r[k] = (-acc * r[0]) % p
    return r

def alpha_by_riemann_roch(A, B, P, N, p):
    """alpha_N(P) computed WITHOUT the Miller recurrence: find the function f in
    L(N(O)) vanishing to order N at P=(a,b), b != 0 (requires [N]P = O), then expand
    it at O in t = -x/y and return [t^0] dlog f / dt."""
    a, b = P
    # basis of L(N O): x^i (2i <= N), y x^j (2j+3 <= N)
    basis = [(i, 0) for i in range(N // 2 + 1)] + [(j, 1) for j in range((N - 3) // 2 + 1)]
    assert len(basis) == N
    # local expansion at P in u = x - a; y(u)^2 = W(a+u), y(0) = b
    W = [B, A, 0, 1]
    Wa = [0] * 4
    for i, c in enumerate(W):
        for k in range(i + 1):
            Wa[k] = (Wa[k] + c * comb(i, k) * pow(a, i - k, p)) % p
    yu = [b % p] + [0] * (N - 1)
    i2b = inv(2 * b, p)
    for k in range(1, N):
        acc = sum(yu[i] * yu[k - i] for i in range(1, k)) % p
        yu[k] = ((Wa[k] if k < 4 else 0) - acc) * i2b % p
    xu = [a % p, 1] + [0] * (N - 2)
    def local(i, e):
        r = [1] + [0] * (N - 1)
        for _ in range(i):
            r = series_mul(r, xu, p, N)
        return series_mul(r, yu, p, N) if e else r
    M = [[0] * N for _ in range(N)]
    for col, (i, e) in enumerate(basis):
        loc = local(i, e)
        for row in range(N):
            M[row][col] = loc[row]
    coef, dim = kernel_vector(M, p)
    assert dim == 1, "expected a one-dimensional space of Miller functions"
    # expansion at O: w = t^3 + A t w^2 + B w^3, x = t/w, y = -1/w
    K = 6
    w = [0] * (K + 3)
    for _ in range(K + 3):
        w2 = series_mul(w, w, p, K + 3)
        w3 = series_mul(w2, w, p, K + 3)
        nw = [0] * (K + 3)
        nw[3] = 1
        for k in range(K + 3):
            if k + 1 < K + 3:
                nw[k + 1] = (nw[k + 1] + A * w2[k]) % p
            nw[k] = (nw[k] + B * w3[k]) % p
        w = nw
    U = w[3:3 + K]                       # w = t^3 U(t)
    iU = series_inv(U, p, K)             # x = t^-2 iU, y = -t^-3 iU
    lead = [0] * K                       # coefficients of t^(-N+k)
    for c, (i, e) in zip(coef, basis):
        if not c:
            continue
        ser = [1] + [0] * (K - 1)
        for _ in range(i + e):
            ser = series_mul(ser, iU, p, K)
        if e:
            ser = [(-x) % p for x in ser]
        shift = N - (2 * i + 3 * e)      # pole order 2i+3e
        for k in range(K - shift):
            lead[shift + k] = (lead[shift + k] + c * ser[k]) % p
    assert lead[0] != 0
    return lead[1] * inv(lead[0], p) % p

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    print(f"cm_verify.py  Python {platform.python_version()} ({platform.python_implementation()}), "
          f"{platform.system()} {platform.release()} {platform.machine()}"
          f"{'  [--quick]' if QUICK else ''}")
    random.seed(20261022)
    t0 = time.time()
    primes = [q for q in range(5, 140 if not QUICK else 60) if is_prime(q)]
    report = {}

    # Theorem A (Theorem 3.2): alpha_N(P) = b J_W(a) at every affine rational point.
    pts = agree = 0
    for p in [q for q in primes if q < 80]:
        for _ in range(6 if not QUICK else 2):
            u, v = random.randrange(p), random.randrange(p)
            if (4 * u ** 3 + 27 * v * v) % p == 0:
                continue
            W = [v, u, 0, 1]
            _, J = high_block(W, p)
            N = p + 1 - proj_trace(W, p)
            for a in range(p):
                y2 = ev(W, a, p)
                for b in range(p):
                    if b * b % p != y2:
                        continue
                    al, T = miller_alpha_F(N, (a, b), u, p)
                    assert T is None
                    pts += 1
                    agree += (al == b * ev(J, a, p) % p)
    report["Theorem A points"] = (pts, agree)

    # Lemma 2.1 (polynomial identity), Theorem B (Theorem 4.1) and Corollary 4.2.
    nC = badC = nT = badT = nP = badP = zero_const = nC0 = 0
    for p in primes:
        for _ in range(10 if not QUICK else 3):
            deg = random.choice([3, 4])
            f = [random.randrange(p) for _ in range(deg)] + [random.randrange(1, p)]
            if not squarefree(f, p):
                continue
            zero_const += (f[0] == 0)
            tau = proj_trace(f, p)
            Tf, J = high_block(f, p)
            F = ppow(f, (p - 1) // 2, p)
            dF = deriv(F, p)
            for a in range(p):
                Cd = C_direct(f, p, a)
                nP += 1
                badP += (Cd != (-ev(dF, a, p) - ev(J, a, p)) % p)
                if ev(f, a, p) == 0:
                    continue
                nC += 1
                nC0 += (a == 0)
                badC += (C_fast(f, p, a, tau) != Cd)
                if a != 0:
                    nT += 1
                    badT += (T_fast(f, p, a, tau) != ev(Tf, a, p))
    report["Lemma 2.1 (all poles incl. branch)"] = (nP, nP - badP)
    report["Theorem 4.1 (B) queries"] = (nC, nC - badC)
    report["  of which at the pole a = 0"] = nC0
    report["Corollary 4.2 truncation queries"] = (nT, nT - badT)
    report["  models with zero constant term"] = zero_const

    # Theorem D (structural residue-divisor identity), p >= 7, f(0)=1.
    n = bad = exc = zd = 0
    for p in [q for q in primes if q >= 7]:
        for _ in range(12 if not QUICK else 4):
            deg = random.choice([3, 4])
            f = [1] + [random.randrange(p) for _ in range(deg)]
            if f[-1] == 0 or not squarefree(f, p):
                continue
            for lam in random.sample(range(1, p), min(8, p - 1)):
                if ev(f, inv(lam, p), p) == 0:
                    continue
                try:
                    ok, ex, _ = structural_check(f, p, lam)
                except ZeroDivisionError:
                    zd += 1      # would need the D5 split; not exercised here
                    continue
                n += 1
                bad += (not ok)
                exc += ex
    report["Theorem D queries (exceptional)"] = (n, n - bad, exc)
    report["  skipped: zero divisor in algebra"] = zd

    # Theorem 4.4 (supplied simple-pole weights), character and point sums.
    nw = badw = nbr = 0
    for p in [q for q in primes if q < 80]:
        for _ in range(8 if not QUICK else 3):
            deg = random.choice([3, 4])
            f = [random.randrange(p) for _ in range(deg)] + [random.randrange(1, p)]
            if not squarefree(f, p):
                continue
            tau = proj_trace(f, p)
            n_inf = 1 if deg == 3 else 1 + leg(f[4], p)
            K = (1 - n_inf - tau) % p
            eps = [leg(ev(f, x, p), p) for x in range(p)]
            for _ in range(5):
                s = random.randint(0, 4)
                A = random.sample(range(p), s)
                c = random.randrange(p)
                r = [0 if eps[a] == 0 else random.randrange(p) for a in A]
                nbr += sum(1 for a in A if eps[a] == 0)
                Om = [x for x in range(p) if x not in A]
                Rw = lambda x: (c + sum(ri * inv(x - ai, p) for ri, ai in zip(r, A))) % p
                lhs1 = sum(Rw(x) * eps[x] for x in Om) % p
                lhs2 = sum(Rw(x) * (1 + eps[x]) for x in Om) % p
                w = [eps[a] for a in A]
                def D(i, vv):
                    return sum(vv[j] * inv(A[i] - A[j], p) for j in range(s) if j != i) % p
                Cv = [C_fast(f, p, a, tau) if r[i] else 0 for i, a in enumerate(A)]
                rhs1 = (c * (K - sum(w)) + sum(r[i] * (Cv[i] + D(i, w)) for i in range(s))) % p
                one_w = [1 + x for x in w]
                rhs2 = (c * (K - s - sum(w)) + sum(r[i] * (Cv[i] + D(i, one_w)) for i in range(s))) % p
                nw += 1
                badw += (lhs1 != rhs1) + (lhs2 != rhs2)
    report["Theorem 4.4 weighted queries (2 outputs each)"] = (nw, 2 * nw - badw)
    report["  excluded branch points (zero residue)"] = nbr

    # Trace-free identity (4.9): J_f(a) = [z^k] Q_a(z)^h, k = d h - p.
    nt = badt = 0
    for p in [q for q in primes if q < 60]:
        for _ in range(5):
            deg = random.choice([3, 4])
            f = [random.randrange(p) for _ in range(deg)] + [random.randrange(1, p)]
            if not squarefree(f, p):
                continue
            _, J = high_block(f, p)
            h = (p - 1) // 2
            k = deg * h - p
            for a in range(p):
                # Q_a(z) = z^d f(a + 1/z) = sum_i f_i (a z + 1)^i z^(d-i)
                Qa = [0] * (deg + 1)
                for i, ci in enumerate(f):
                    for j in range(i + 1):
                        Qa[deg - i + j] = (Qa[deg - i + j] + ci * comb(i, j) * pow(a, j, p)) % p
                Qh = ppow(Qa, h, p)
                nt += 1
                badt += ((Qh[k] if k < len(Qh) else 0) != ev(J, a, p))
    report["Trace-free identity (4.9) queries"] = (nt, nt - badt)

    # Rounded third: Corollary E, B_L by one chain vs direct sum; relations (6.3)-(6.4).
    rt_n = rt_ok = 0
    for p in [q for q in range(5, 3000 if not QUICK else 400) if is_prime(q) and q % 3 == 2]:
        L = (p + 1) // 3
        a = a_seq(p, L)
        BL = sum(a[:L]) % p
        rt_n += 1
        ok = rounded_third_prefix(p) == BL
        if p >= 5:
            m = L - 1
            G = 1
            for kk in range(1, m + 1):
                G = G * kk % p
            G3i = inv(pow(G, 3, p), p)
            U = lambda j, Bj: (4 * Bj - 2 * j * (2 * j + 5) * a[j]) % p
            ok &= a[L] == 3 * inv(2, p) * G3i % p
            ok &= G == pow(3 * inv(2 * a[L], p), (2 * p - 1) // 3, p)
            ok &= a[m] == (-4 * a[L]) % p
            ok &= U(L, BL) == (4 * BL - 17 * inv(3, p) * G3i) % p
            ok &= U(m, (BL - a[m]) % p) == (4 * BL - 16 * inv(3, p) * G3i) % p
            # U_p(L) against its definition (6.2)
            h = (p - 1) // 2
            t, Udef = 1, 0
            for i in range(L):
                Udef = (Udef + (h + 1 + i) * t) % p
                t = t * (h + 2 + i) * inv(2 * i + 2, p) % p
            ok &= Udef == U(L, BL)
        rt_ok += ok
    report["Rounded third primes (B_L and relations)"] = (rt_n, rt_ok)

    # Quarter point (6.5): B_n via CM trace + chain vs direct.
    qp_n = qp_ok = 0
    for p in [q for q in range(17, 3000 if not QUICK else 400) if is_prime(q) and q % 4 == 1]:
        n4 = (p - 1) // 4
        a = a_seq(p, n4)
        Bn, a_n, tau = quarter_point(p)
        f = [1, 0, 0, 0, (-inv(2, p)) % p]
        ok = (Bn == sum(a[:n4]) % p) and (a_n == a[n4])
        if p < 400:
            ok &= tau == proj_trace(f, p)
        qp_n += 1
        qp_ok += ok
    report["Quarter-point primes (B_n, a_n)"] = (qp_n, qp_ok)

    # Medium-size direct confirmation (O(p) loops).
    for p in (1000211, 1000033):
        if p % 3 == 2:
            L = (p + 1) // 3
            a = a_seq(p, L)
            report[f"Rounded third p={p}"] = rounded_third_prefix(p) == sum(a[:L]) % p
        else:
            n4 = (p - 1) // 4
            a = a_seq(p, n4)
            report[f"Quarter point p={p}"] = quarter_point(p)[0] == sum(a[:n4]) % p


    # ======== Checks added in the corrected rewrite (independent seed) ========
    rng = random.Random(2026102202)

    # (N1) Normalization of the Miller coefficient: alpha_N(P) by an independent
    # Riemann-Roch construction of f_{N,P} and its Laurent expansion in t = -x/y,
    # compared with Algorithm 2.2 and with b J_W(a) (Theorem A). Includes trace-one
    # curves (N = p) and supersingular ones.
    n1 = ok1 = n1_tr1 = 0
    for p in (5, 7, 11, 13, 17, 19, 23):
        curves, seen_tr1 = [], False
        for (A, B) in [(A, B) for A in range(p) for B in range(p)]:
            if (4 * A ** 3 + 27 * B * B) % p == 0:
                continue
            tr = proj_trace([B, A, 0, 1], p)
            if tr == 1 and not seen_tr1:
                curves.append((A, B))
                seen_tr1 = True
        allc = [(A, B) for A in range(p) for B in range(p) if (4 * A ** 3 + 27 * B * B) % p]
        curves += rng.sample(allc, 3 if not QUICK else 1)
        for (A, B) in curves:
            W = [B, A, 0, 1]
            _, J = high_block(W, p)
            N = p + 1 - proj_trace(W, p)
            for a in range(p):
                y2 = ev(W, a, p)
                for b in range(1, p):
                    if b * b % p != y2:
                        continue
                    rr = alpha_by_riemann_roch(A, B, (a, b), N, p)
                    ch, _ = miller_alpha_F(N, (a, b), A, p)
                    n1 += 1
                    n1_tr1 += (N == p)
                    ok1 += (rr == ch == b * ev(J, a, p) % p)
    report["[new] alpha_N via Riemann-Roch = chain = bJ_W(a)"] = (n1, ok1)
    report["  of which on trace-one curves (N = p)"] = n1_tr1

    # (N2) Coefficient ranges in Section 6: (6.1) [x^{ki}](1 - x^k/2)^h = a_i for
    # 0 <= i <= h (computed by polynomial powering), ratio recurrence for
    # 0 <= i < h, t_i = (2i+1) a_i for 0 <= i <= h, and (6.3) against the
    # definition (6.2) for every 0 <= L <= h.
    n2 = ok2 = nL = okL = 0
    bound2 = 1000 if not QUICK else 200
    for p in [q for q in range(5, bound2) if is_prime(q)]:
        h = (p - 1) // 2
        coeffs = ppow([1, (-inv(2, p)) % p], h, p)      # (1 - X/2)^h, X = x^k
        a = [comb(2 * i, i) % p * inv(pow(8, i, p), p) % p for i in range(h + 1)]
        ok = coeffs == a
        ok &= all(a[i + 1] == a[i] * (2 * i + 1) * inv(4 * (i + 1), p) % p for i in range(h))
        t, Bsum, Udef = 1, 0, 0
        for L in range(h + 1):
            # here t = t_L, Bsum = B_L, Udef = U_p(L)
            ok &= t == (2 * L + 1) * a[L] % p
            nL += 1
            okL += Udef == (4 * Bsum - 2 * L * (2 * L + 5) * a[L]) % p
            if L < h:
                Udef = (Udef + (h + 1 + L) * t) % p
                Bsum = (Bsum + a[L]) % p
                t = t * (h + 2 + L) * inv(2 * L + 2, p) % p
        n2 += 1
        ok2 += ok
    report[f"[new] (6.1), ratios, t_i, 0<=i<=h, primes 5<=p<{bound2}"] = (n2, ok2)
    report["[new] (6.3) vs (6.2), every 0 <= L <= h, same primes"] = (nL, okL)

    # (N3) Theorem 4.4 as an unrestricted algebraic identity: active poles may be
    # branch points when the exact C_f(a_i) is supplied (direct enumeration).
    n3 = ok3 = n3br = 0
    for p in [q for q in primes if q < 80]:
        for _ in range(6 if not QUICK else 2):
            deg = rng.choice([3, 4])
            f = [rng.randrange(p) for _ in range(deg)] + [rng.randrange(1, p)]
            if not squarefree(f, p):
                continue
            tau = proj_trace(f, p)
            n_inf = 1 if deg == 3 else 1 + leg(f[4], p)
            K = (1 - n_inf - tau) % p
            eps = [leg(ev(f, x, p), p) for x in range(p)]
            roots = [x for x in range(p) if eps[x] == 0]
            for _ in range(4):
                s = rng.randint(1, 4)
                pool = list(range(p))
                Aset = rng.sample(pool, s)
                if roots and rng.random() < 0.7 and roots[0] not in Aset:
                    Aset[0] = rng.choice([x for x in roots if x not in Aset[1:]])
                r0 = rng.randrange(p)
                r = [rng.randrange(1, p) for _ in Aset]
                n3br += sum(1 for x in Aset if eps[x] == 0)
                Om = [x for x in range(p) if x not in Aset]
                Rw = lambda x: (r0 + sum(ri * inv(x - ai, p) for ri, ai in zip(r, Aset))) % p
                lhs1 = sum(Rw(x) * eps[x] for x in Om) % p
                lhs2 = sum(Rw(x) * (1 + eps[x]) for x in Om) % p
                w = [eps[x] for x in Aset]
                D = lambda i, vv: sum(vv[j] * inv(Aset[i] - Aset[j], p) for j in range(s) if j != i) % p
                Cv = [C_direct(f, p, x) for x in Aset]
                rhs1 = (r0 * (K - sum(w)) + sum(r[i] * (Cv[i] + D(i, w)) for i in range(s))) % p
                rhs2 = (r0 * (K - s - sum(w)) + sum(r[i] * (Cv[i] + D(i, [1 + x for x in w])) for i in range(s))) % p
                n3 += 1
                ok3 += (lhs1 == rhs1) and (lhs2 == rhs2)
    report["[new] Theorem 4.4 with exact C_f, active branch poles allowed"] = (n3, ok3)
    report["  active branch poles in that sample"] = n3br

    # -------- Numbers quoted in the paper --------
    print("=" * 72)
    for k, v in report.items():
        print(f"{k:48s} {v}")
    print("=" * 72)

    # Table 1: exceptional examples over F_11 (Theorem D).
    print("Table 1 rows (H, S, rPsi, eps, tau):")
    print("  1+w+3w^3      :", structural_check([1, 1, 0, 3], 11, 1)[2])
    print("  1+w+2w^2+3w^3 :", structural_check([1, 1, 2, 3], 11, 1)[2])

    # Example 6.1: rounded third at p = 23.
    p = 23
    f = [1, 0, 0, (-inv(2, p)) % p]
    g, Ag, Bg, R = twist_data(f, p, 1)
    eps = leg(ev(f, 1, p), p)
    N = p + 1
    al, _ = miller_alpha_F(N, R, Ag, p)
    L = (p + 1) // 3
    a = a_seq(p, L)
    print(f"Worked example p=23: g={g[:4]}, A_g={Ag}, B_g={Bg}, R={R}, eps={eps}, "
          f"N={N}, alpha_N(R)={al}, T_f(1)={T_fast(f, p, 1, 0)}, "
          f"B_L(direct)={sum(a[:L]) % p}, a_L={a[L]}, a_i={a[:L+1]}")
    G = 1
    for kk in range(1, L):
        G = G * kk % p
    print(f"  m!={G}, 3/(2 m!^3)={3 * inv(2 * pow(G, 3, p), p) % p}")

    # Quarter-point example at p = 97.
    Bn, a_n, tau = quarter_point(97)
    print(f"Quarter point p=97: B_n={Bn}, a_n={a_n}, tau={tau}, "
          f"U=4B+9a/4={(4 * Bn + 9 * inv(4, 97) * a_n) % 97}")
    print("p=5 example C_{x^3+3x}(1):", C_fast([0, 3, 0, 1], 5, 1, proj_trace([0, 3, 0, 1], 5)),
          "direct", C_direct([0, 3, 0, 1], 5, 1), "tau", proj_trace([0, 3, 0, 1], 5))

    # Large-prime demonstration (no direct check possible).
    p = (1 << 61) - 1
    while not (p % 3 == 2 and is_prime(p)):
        p -= 2
    t1 = time.perf_counter()
    BL = rounded_third_prefix(p)
    t2 = time.perf_counter()
    print(f"Illustration only (no direct check): rounded third at p={p} ({p.bit_length()} bits): B_L={BL}  "
          f"[{(t2 - t1) * 1e3:.2f} ms, pure Python]")
    print(f"Total run time {time.time() - t0:.1f} s")

if __name__ == "__main__":
    main()
