"""Common helpers for the independent check (pure Python 3 stdlib).

Polynomials are lists of ints, index = degree (little-endian).
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # explicit: python -I omits the script directory

import csv
from harness import require, CheckFailure  # noqa: F401


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def ptrim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def pmul(a, b, m):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] += ai * bj
    return ptrim([c % m for c in r])


def padd(a, b, m):
    n = max(len(a), len(b))
    r = [((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % m for i in range(n)]
    return ptrim(r)


def psub(a, b, m):
    n = max(len(a), len(b))
    r = [((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % m for i in range(n)]
    return ptrim(r)


def pscale(a, c, m):
    return ptrim([(x * c) % m for x in a])


def ppow(a, e, m):
    r = [1]
    base = a[:]
    while e:
        if e & 1:
            r = pmul(r, base, m)
        e >>= 1
        if e:
            base = pmul(base, base, m)
    return r


def pdivmod_monic(a, b, m):
    """Divide a by monic b modulo m. Returns (q, r)."""
    a = [x % m for x in a]
    db = len(b) - 1
    require(b[-1] % m == 1, 'common.py:69: invariant failed')
    if len(a) - 1 < db:
        return [], ptrim(a[:])
    q = [0] * (len(a) - db)
    for k in range(len(a) - 1, db - 1, -1):
        c = a[k] % m
        if c:
            q[k - db] = c
            for j in range(db + 1):
                a[k - db + j] = (a[k - db + j] - c * b[j]) % m
    return ptrim(q), ptrim(a[:db])


def pderiv(a, m):
    return ptrim([(i * a[i]) % m for i in range(1, len(a))])


def coeff(a, k):
    return a[k] if 0 <= k < len(a) else 0


def F_poly(A, B, m):
    return ptrim([B % m, A % m, 0, 1])


def hasse_beta(p, A, B):
    """H = [x^(p-1)] F^h, beta = [x^(p-2)] F^h mod p, computed by direct polynomial power."""
    h = (p - 1) // 2
    G = ppow(F_poly(A, B, p), h, p)
    return coeff(G, p - 1) % p, coeff(G, p - 2) % p


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def count_points(p, A, B):
    """#E(F_p) including O."""
    n = 1
    for x in range(p):
        n += 1 + legendre(x * x * x + A * x + B, p)
    return n


def trace(p, A, B):
    return p + 1 - count_points(p, A, B)


def nonsingular(p, A, B):
    return (4 * A ** 3 + 27 * B ** 2) % p != 0


def load_targets(path):
    """Read the handover target CSV from an explicit path (no default location)."""
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            rows.append({k: (int(v) if k not in ("outside_retained_tables",) else v) for k, v in r.items()})
    return rows


def all_models(p):
    return [(A, B) for A in range(p) for B in range(p) if nonsingular(p, A, B)]
