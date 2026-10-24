"""
Core arithmetic for the Cartier-Miller congruence experiment.

Target:  S_k(z) = sum_{i=0}^{floor((p-1)/k)} binom(2i,i) z^i  (mod p),  k in {3,4},
computed as T_f(1) for f = 1 - 4 z x^k by one differentiated Miller chain on the
normalized twist (Corollary 4.2 of the paper), with N = #E_1(F_p) selected from the
CM candidate traces by a random-point annihilation test.

Pure Python 3.10+, no dependencies.
"""
from math import comb, isqrt
from fractions import Fraction
import random

# ---------------------------------------------------------------- basics

def inv(a, p):
    return pow(a % p, -1, p)

def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1

_SMALL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)

def is_prime(n):
    """Deterministic Miller-Rabin for n < 3.3e24; for larger n it is a strong
    probable-prime test with 15 bases plus 8 random bases (error < 4^-23)."""
    if n < 2:
        return False
    for q in _SMALL:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    bases = list(_SMALL)
    if n >= 3317044064679887385961981:
        rng = random.Random(n)
        bases += [rng.randrange(2, n - 2) for _ in range(8)]
    for a in bases:
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

def frac_mod(q, p):
    """Fraction -> residue mod p."""
    q = Fraction(q)
    return q.numerator % p * inv(q.denominator, p) % p

def sqrt_mod(a, p, rng=None):
    """Tonelli-Shanks; returns a square root of a mod p (a must be a square)."""
    a %= p
    if a == 0:
        return 0
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
        assert r * r % p == a
        return r
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while legendre(z, p) != -1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    assert r * r % p == a
    return r

def cornacchia(d, p):
    """Solve x^2 + d y^2 = p (d = 1 or 3), x, y >= 0. Returns (x, y) or None."""
    if legendre(-d, p) != 1:
        return None
    r = sqrt_mod(-d % p, p)
    if r < p // 2:
        r = p - r
    a, b = p, r
    lim = isqrt(p)
    while b > lim:
        a, b = b, a % b
    rem = p - b * b
    if rem % d:
        return None
    y2 = rem // d
    y = isqrt(y2)
    if y * y != y2:
        return None
    return b, y

# ---------------------------------------------------------------- polynomials

def ev(f, x, p):
    r = 0
    for c in reversed(f):
        r = (r * x + c) % p
    return r

def taylor(f, a, p):
    """Coefficients of f(a + z)."""
    g = [0] * len(f)
    for i, c in enumerate(f):
        if c:
            for k in range(i + 1):
                g[k] = (g[k] + c * comb(i, k) * pow(a, i - k, p)) % p
    return g

# ---------------------------------------------------------------- elliptic curves

def ec_add(P, Q, A, p):
    """Affine addition on Y^2 = X^3 + A X + B; None is O. Returns (point, slope)."""
    if P is None:
        return Q, 0
    if Q is None:
        return P, 0
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2:
        if (y1 + y2) % p == 0:
            return None, 0
        rho = (3 * x1 * x1 + A) * inv(2 * y1, p) % p     # operands coincide: tangent
    else:
        rho = (y2 - y1) * inv(x2 - x1, p) % p            # distinct abscissae: chord
    x3 = (rho * rho - x1 - x2) % p
    return (x3, (rho * (x1 - x3) - y1) % p), rho

def ec_mul(n, P, A, p):
    R = None
    Q = P
    while n:
        if n & 1:
            R, _ = ec_add(R, Q, A, p)
        Q, _ = ec_add(Q, Q, A, p)
        n >>= 1
    return R

def miller_alpha(m, R, A, p):
    """Algorithm 2.2: returns (alpha_m(R), [m]R)."""
    T, al = R, 0
    for bit in bin(m)[3:]:
        T, rho = ec_add(T, T, A, p)
        al = (2 * al + rho) % p
        if bit == "1":
            T, rho = ec_add(T, R, A, p)
            al = (al + rho) % p
    return al, T

def twist_data(f, p, a):
    """Normalized model g(z)=f(a+z)/f(a), short coefficients (A_g, B_g), point R
    (equation 4.2 of the paper)."""
    fa = ev(f, a, p)
    assert fa != 0, "branch point"
    g = taylor(f, a, p) + [0] * 5
    fi = inv(fa, p)
    g1, g2, g3, g4 = (g[i] * fi % p for i in (1, 2, 3, 4))
    i3, i27 = inv(3, p), inv(27, p)
    Ag = (-4 * g4 + g1 * g3 - g2 * g2 * i3) % p
    Bg = (g3 * g3 - 8 * g2 * g4 * i3 + g1 * g1 * g4 - g1 * g2 * g3 * i3
          + 2 * pow(g2, 3, p) * i27) % p
    xR = (g1 * g1 * inv(4, p) - 2 * g2 * i3) % p
    yR = (-g3 + g1 * g2 * inv(2, p) - pow(g1, 3, p) * inv(8, p)) % p
    assert (yR * yR - (xR ** 3 + Ag * xR + Bg)) % p == 0
    return g1, Ag, Bg, (xR, yR)

def random_point(A, B, p, rng):
    while True:
        x = rng.randrange(p)
        r = (x * x * x + A * x + B) % p
        if r == 0:
            continue
        if legendre(r, p) == 1:
            return (x, sqrt_mod(r, p))

# ---------------------------------------------------------------- traces

def candidate_traces(k, p):
    """All possible traces of curves with j = 0 (k = 3) or j = 1728 (k = 4) over F_p."""
    if k == 3:
        if p % 3 == 2:
            return [0]
        a, b = cornacchia(3, p)               # p = a^2 + 3 b^2
        base = [2 * a, a + 3 * b, a - 3 * b]
    elif k == 4:
        if p % 4 == 3:
            return [0]
        u, s = cornacchia(1, p)               # p = u^2 + s^2
        base = [2 * u, 2 * s]
    else:
        raise ValueError(k)
    return sorted({t for b0 in base for t in (b0, -b0)})

class AmbiguousTrace(Exception):
    pass

def select_order(Ag, Bg, k, p, rng, n_points=3):
    """Group order of E: Y^2 = X^3 + Ag X + Bg, chosen among p + 1 - t for the CM
    candidate traces t by requiring [N]P = O at n_points random points."""
    cands = [p + 1 - t for t in candidate_traces(k, p)]
    if len(cands) == 1:
        return cands[0]
    pts = [random_point(Ag, Bg, p, rng) for _ in range(n_points)]
    alive = [N for N in cands if all(ec_mul(N, P, Ag, p) is None for P in pts)]
    if len(alive) != 1:
        raise AmbiguousTrace(f"p={p}, survivors={alive}")
    return alive[0]

# ---------------------------------------------------------------- the target

def S_fast(k, z, p, rng):
    """S_k(z) mod p by one Miller chain (Corollary 4.2 with a = 1)."""
    zz = frac_mod(z, p)
    f = [1] + [0] * (k - 1) + [(-4 * zz) % p]
    if ev(f, 1, p) == 0 or zz == 0:
        raise ValueError("branch or degenerate z for this p")
    eps = legendre(ev(f, 1, p), p)
    g1, Ag, Bg, R = twist_data(f, p, 1)
    N = select_order(Ag, Bg, k, p, rng)
    al, T = miller_alpha(N, R, Ag, p)
    if T is not None:
        raise AmbiguousTrace(f"[N]R != O at p={p}")
    return eps * (1 - N * g1 * inv(4, p) - al * inv(2, p)) % p

def S_direct(k, z, p):
    """Definition-level S_k(z) mod p (O(p) with a linear-time inverse table)."""
    zz = frac_mod(z, p)
    L = (p - 1) // k
    invt = [0, 1] + [0] * L
    for i in range(2, L + 2):
        invt[i] = (p - (p // i) * invt[p % i] % p) % p
    s, c, zp = 0, 1, 1
    for i in range(L + 1):
        s = (s + c * zp) % p
        c = c * 2 * (2 * i + 1) % p * invt[i + 1] % p
        zp = zp * zz % p
    return s

def brute_trace(f, p):
    """Projective trace of v^2 = f(x) by counting (small p)."""
    deg = len(f) - 1
    aff = sum(1 + legendre(ev(f, x, p), p) for x in range(p))
    ninf = 1 if deg == 3 else 1 + legendre(f[4], p)
    return p + 1 - aff - ninf
