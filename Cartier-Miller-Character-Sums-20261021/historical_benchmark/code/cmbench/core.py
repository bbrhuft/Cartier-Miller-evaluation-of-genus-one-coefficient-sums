"""cmbench.core -- shared exact arithmetic and the matched output contract.

Matched output (BENCHMARK_PROTOCOL.md): for a prime p >= 7, a squarefree exact-degree cubic or
quartic f (coefficients low -> high) and a residue a,

    C_f(a) = sum_{x in F_p, x != a} chi(f(x)) / (x - a)        returned as an integer in [0, p).

Reversed-coefficient identity (COMPARATOR_MATHEMATICS.md, re-derived in REPORT section 5):

    C_f(a) = -F'(a) - [z^N] G_a(z)^h,   F = f^h, h = (p-1)/2, G_a(z) = z^d f(a + 1/z), N = d h - p,

with F'(a) = h f(a)^(h-1) f'(a).  N = (p-3)/2 (cubic) or p-2 (quartic), so 0 <= N < p.

Written 20 October 2026 for this package; no inherited code.
"""
from math import comb

__all__ = ['peval', 'deriv', 'taylor_shift', 'reversed_shift', 'N_index', 'Fprime_at',
           'from_high_value', 'legendre', 'squarefree', 'n_infinity', 'is_prime_small',
           'companion_matrices']


def peval(c, x, p):
    v = 0
    for a in reversed(c):
        v = (v * x + a) % p
    return v


def deriv(c, p):
    return [(i * c[i]) % p for i in range(1, len(c))] or [0]


def taylor_shift(f, a, p):
    """Coefficients of f(a + z), low -> high (O(d^2) for fixed degree d)."""
    d = len(f) - 1
    return [sum(f[i] * comb(i, j) * pow(a, i - j, p) for i in range(j, d + 1)) % p
            for j in range(d + 1)]


def reversed_shift(f, a, p):
    """g with G_a(z) = z^d f(a + 1/z) = sum_j g[j] z^j; g[0] = leading coefficient of f."""
    return list(reversed(taylor_shift(f, a, p)))


def N_index(p, d):
    return d * ((p - 1) // 2) - p


def Fprime_at(f, a, p):
    h = (p - 1) // 2
    fa = peval(f, a, p)
    if fa == 0:
        return 0          # h - 1 >= 2: F' vanishes at a root of f
    return h * pow(fa, h - 1, p) % p * peval(deriv(f, p), a, p) % p


def from_high_value(f, a, p, high):
    """C_f(a) from H_high(a) = [z^N] G_a^h."""
    return (-Fprime_at(f, a, p) - high) % p


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def _trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def squarefree(f, p):
    a, b = _trim([c % p for c in f]), _trim(deriv(f, p))
    while b:
        r = a[:]
        inv = pow(b[-1], -1, p)
        while len(r) >= len(b):
            q, off = r[-1] * inv % p, len(r) - len(b)
            for j, v in enumerate(b):
                r[off + j] = (r[off + j] - q * v) % p
            r = _trim(r)
        a, b = b, r
    return len(a) == 1


def n_infinity(f, p):
    d = len(f) - 1
    if d == 3:
        return 1
    return 1 + legendre(f[-1], p)


def is_prime_small(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):   # deterministic for n < 3.3e24
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


def companion_matrices(g, h, p):
    """A(k) = A0 + k*A1 with W_k = A(k) W_{k-1}, W_k = D_k (e_k, ..., e_{k-d+1}), D_k = k! g0^k.

    From k g0 e_k = sum_{j=1}^{d} ((h+1) j - k) g_j e_{k-j}  (G (G^h)' = h G' G^h):
      row 0:  A(k)[0][j-1] = ((h+1) j - k) g_j
      rows i>=1: A(k)[i][i-1] = k g0      (keeps D_k e_{k-i} = k g0 * D_{k-1} e_{k-i})
    Every entry is linear in k.  W_0 = (g0^h, 0, ..., 0); e_N = W_N[0] / (N! g0^N).
    """
    d = len(g) - 1
    A0 = [[0] * d for _ in range(d)]
    A1 = [[0] * d for _ in range(d)]
    for j in range(1, d + 1):
        A0[0][j - 1] = (h + 1) * j * g[j] % p
        A1[0][j - 1] = (-g[j]) % p
    for i in range(1, d):
        A1[i][i - 1] = g[0] % p
    return A0, A1
