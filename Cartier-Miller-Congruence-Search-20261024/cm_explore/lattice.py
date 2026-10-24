"""
Integer-relation search modulo a product of primes by lattice reduction.

Given columns v_0 (target), v_1..v_d (basis) as residues modulo distinct primes,
we CRT-combine them modulo P = prod p and look for small integer x with
    sum_j x_j v_j = 0 (mod P).
The lattice rows are [e_j | K v_j] and [0 | K P]; reduced rows with last entry 0
are relations.  Uses python-flint's LLL when available, else a slow exact fallback.
"""
from math import isqrt

try:
    import flint
    HAVE_FLINT = True
except ImportError:          # pragma: no cover
    HAVE_FLINT = False


def crt(residues, primes):
    P = 1
    for p in primes:
        P *= p
    x = 0
    for r, p in zip(residues, primes):
        m = P // p
        x = (x + r * m * pow(m, -1, p)) % P
    return x, P


def _lll_fallback(B, delta=0.99):
    """Exact-rational LLL (slow; only used without python-flint)."""
    from fractions import Fraction
    B = [list(map(int, r)) for r in B]
    n = len(B)

    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    def gso(B):
        Bs, mu = [], [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            v = [Fraction(x) for x in B[i]]
            for j in range(i):
                mu[i][j] = dot(B[i], Bs[j]) / dot(Bs[j], Bs[j])
                v = [a - mu[i][j] * b for a, b in zip(v, Bs[j])]
            Bs.append(v)
        return Bs, mu

    Bs, mu = gso(B)
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [a - q * b for a, b in zip(B[k], B[j])]
                Bs, mu = gso(B)
        if dot(Bs[k], Bs[k]) >= (delta - mu[k][k - 1] ** 2) * dot(Bs[k - 1], Bs[k - 1]):
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bs, mu = gso(B)
            k = max(k - 1, 1)
    return B


def lll_rows(rows):
    if HAVE_FLINT:
        M = flint.fmpz_mat(rows).lll()
        return [[int(M[i, j]) for j in range(M.ncols())] for i in range(M.nrows())]
    return _lll_fallback(rows)


def relations(columns, primes):
    """columns: list of lists (one list of residues per variable, aligned with primes).
    Returns relation vectors (lists of ints), sorted by Euclidean length."""
    combined = []
    P = None
    for col in columns:
        x, P = crt(col, primes)
        combined.append(x)
    n = len(columns)
    K = P                        # weight: any relation must vanish modulo P exactly
    rows = []
    for j in range(n):
        r = [0] * (n + 1)
        r[j] = 1
        r[n] = K * combined[j]
        rows.append(r)
    rows.append([0] * n + [K * P])
    red = lll_rows(rows)
    rels = [r[:n] for r in red if r[n] == 0 and any(r[:n])]
    rels.sort(key=lambda v: sum(x * x for x in v))
    return rels


def norm2(v):
    return sum(x * x for x in v)


def supnorm(v):
    return max(abs(x) for x in v)
