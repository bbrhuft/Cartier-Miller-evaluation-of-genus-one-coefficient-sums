"""Dense polynomial arithmetic over Z/qZ (any modulus) by Kronecker substitution.

Uses gmpy2 (GMP) for the big-integer product when importable, otherwise
Python's built-in integers (Karatsuba; asymptotically slower but exact).
No division by any integer is performed except through monic polynomials.
"""
try:
    import gmpy2
    _mpz = gmpy2.mpz
    BACKEND = 'gmpy2-' + gmpy2.version()
except Exception:                      # pragma: no cover - portability path
    gmpy2 = None
    _mpz = int
    BACKEND = 'python-int'

NAIVE = 24          # below this length use schoolbook products
COUNT = {'mul': 0, 'coeff_mul': 0}


def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def mul(a, b, q):
    if not a or not b:
        return []
    la, lb = len(a), len(b)
    COUNT['mul'] += 1
    if min(la, lb) <= NAIVE:
        COUNT['coeff_mul'] += la * lb
        c = [0] * (la + lb - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    c[i + j] += x * y
        return [x % q for x in c]
    bits = 2 * q.bit_length() + min(la, lb).bit_length() + 1
    nb = (bits + 7) // 8
    A = int.from_bytes(b''.join(x.to_bytes(nb, 'little') for x in a), 'little')
    B = int.from_bytes(b''.join(x.to_bytes(nb, 'little') for x in b), 'little')
    C = int(_mpz(A) * _mpz(B))
    n = la + lb - 1
    raw = C.to_bytes(n * nb, 'little')
    fb = int.from_bytes
    return [fb(raw[i * nb:(i + 1) * nb], 'little') % q for i in range(n)]


def add(a, b, q):
    if len(a) < len(b):
        a, b = b, a
    c = a[:]
    for i, y in enumerate(b):
        c[i] = (c[i] + y) % q
    return c


def sub(a, b, q):
    n = max(len(a), len(b))
    c = [0] * n
    for i, x in enumerate(a): c[i] = x
    for i, y in enumerate(b): c[i] = (c[i] - y) % q
    return c


def inv_series(f, n, q):
    """g with f*g = 1 mod x^n; f[0] must be a unit mod q (here f[0] = 1)."""
    g = [pow(f[0], -1, q)]
    k = 1
    while k < n:
        k2 = min(2 * k, n)
        fg = mul(f[:k2], g, q)[:k2]
        e = [(-x) % q for x in fg]
        e[0] = (e[0] + 2) % q
        g = mul(g, e, q)[:k2]
        k = k2
    return g


def divmod_monic(a, b, q, binv_rev=None):
    """Remainder of a modulo monic b; binv_rev = inverse of reversed b if cached."""
    da, db = len(a) - 1, len(b) - 1
    assert b[-1] == 1
    if da < db:
        return a[:]
    m = da - db + 1
    ra = a[::-1][:m]
    if binv_rev is None or len(binv_rev) < m:
        binv_rev = inv_series(b[::-1], m, q)
    qr = mul(ra, binv_rev[:m], q)[:m]
    qu = qr[::-1]
    r = sub(a, mul(qu, b, q), q)[:db]
    return r


def horner(a, x, q):
    r = 0
    for c in reversed(a):
        r = (r * x + c) % q
    return r


def multipoint(polys, xs, q):
    """Evaluate each polynomial in `polys` at all points xs (subproduct/remainder tree)."""
    n = len(xs)
    if n <= 16:
        return [[horner(P, x, q) for x in xs] for P in polys]
    # subproduct tree
    levels = [[[(-x) % q, 1] for x in xs]]
    while len(levels[-1]) > 1:
        prev = levels[-1]; nxt = []
        for i in range(0, len(prev), 2):
            nxt.append(mul(prev[i], prev[i + 1], q) if i + 1 < len(prev) else prev[i])
        levels.append(nxt)
    invs = {}
    out = []
    for P in polys:
        rems = [divmod_monic(P, levels[-1][0], q)]
        for lev in range(len(levels) - 2, -1, -1):
            nodes = levels[lev]; new = []
            for i, node in enumerate(nodes):
                parent = rems[i // 2]
                if lev == 0:
                    new.append([horner(parent, (-node[0]) % q, q)])
                    continue
                if len(node) - 1 <= 8:
                    new.append(parent)          # defer: reduce later
                else:
                    key = (lev, i)
                    if key not in invs and len(parent) >= len(node):
                        invs[key] = inv_series(node[::-1], max(1, len(parent) - len(node) + 1), q)
                    new.append(divmod_monic(parent, node, q, invs.get(key)) if len(parent) >= len(node) else parent)
            rems = new
        out.append([(r[0] if r else 0) % q for r in rems])
    return out
