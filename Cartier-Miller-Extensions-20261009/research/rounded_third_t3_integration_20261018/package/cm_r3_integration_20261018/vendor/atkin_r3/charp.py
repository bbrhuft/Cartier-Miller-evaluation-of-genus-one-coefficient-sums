"""Characteristic-p half-interval acquisition of c_p = 2((p-2)/3)!^{-3} mod p.

Certified prime p >= 11, p = 5 (mod 6) is an input contract. Standard library only.

Identity (exact, elementary):  with m = (p-2)/3, h = (p-1)/2,
    P = prod_{j=m+1}^{h} j   (length (p+1)/6),   H = h! mod p,
    m! = H / P   and   H^4 = 1,   hence   c_p = 2 H P^3.
H is a square root of -1 (p = 1 mod 4) or of +1 (p = 3 mod 4). It is acquired, sign
included, from class numbers of imaginary quadratic orders:
  route 'mordell'  p = 3 mod 4: H = (-1)^((h(-p)+1)/2)                 (Mordell 1961)
  route 'gauss4p'  p = 5 mod 8: H is the root of -1 with
                   H^((p-1)/4) = (((p-1)/4)!/p) (2a)^((p-1)/4),
                   (((p-1)/4)!/p) = (-1)^{((p-1)/4 - h(-4p)/2)/2},
                   p = a^2+b^2, a = 1 mod 4                        (Gauss 1828 + Dirichlet)
  route 'h3p'      p = 1 mod 4, p = 2 mod 3 (CONJECTURAL identity (*), finite evidence):
                   H = (2/p) ((m!)/p) 3^((p-1)/4),
                   (m!/p) = (-1)^{(m - h(-3p)/2)/2}.
The class number is computed by counting reduced forms, O(|D|^{1/2} polylog) operations;
this has the same exponent as the product and is charged in all timings.
Asymptotic cost of the whole method: still O(M(sqrt p) log p). Constant-factor only.
"""
from math import gcd, isqrt
from atkin import parameters, pochhammer_many


# ---------------------------------------------------------------- class numbers
def _spf(n):
    s = list(range(n + 1))
    for i in range(2, isqrt(n) + 1):
        if s[i] == i:
            for k in range(i * i, n + 1, i):
                if s[k] == k:
                    s[k] = i
    return s


def _tonelli(n, q):
    """square root of n mod odd prime q, (n/q)=1."""
    n %= q
    if n == 0:
        return 0
    if q % 4 == 3:
        return pow(n, (q + 1) // 4, q)
    s, t = 0, q - 1
    while t % 2 == 0:
        s += 1
        t //= 2
    z = 2
    while pow(z, (q - 1) // 2, q) != q - 1:
        z += 1
    m, c, x, b = s, pow(z, t, q), pow(n, (t + 1) // 2, q), pow(n, t, q)
    while b != 1:
        i, bb = 0, b
        while bb != 1:
            bb = bb * bb % q
            i += 1
        g = pow(c, 1 << (m - i - 1), q)
        m, c, x, b = i, g * g % q, x * g % q, b * g * g % q
    return x


def _roots_pp(D, q, e):
    """all x mod q^e with x^2 = D (mod q^e), for the discriminants used here."""
    mod = q ** e
    if q == 2:
        sols = [x for x in range(2) if (x * x - D) % 2 == 0]
        k = 1
        while k < e:
            nxt = 1 << (k + 1)
            sols = sorted({y for x in sols for y in (x, x + (1 << k)) if (y * y - D) % nxt == 0})
            k += 1
        return sols
    if D % q == 0:
        if D % (q * q) != 0:          # v_q(D)=1: x=0 mod q, and no lift beyond q
            return [0] if e == 1 else []
        if mod <= 4096:
            return [x for x in range(mod) if (x * x - D) % mod == 0]
        raise ValueError('unsupported ramified prime power')
    if pow(D % q, (q - 1) // 2, q) != 1:
        return []
    r = _tonelli(D, q)
    cur, x = q, r
    while cur < mod:
        nxt = cur * q
        x = (x - (x * x - D) * pow(2 * x, -1, nxt)) % nxt
        cur = nxt
    return sorted({x % mod, (-x) % mod})


def classno(D, _cache={}):
    """h(D) for a negative fundamental discriminant D by counting reduced forms."""
    if D >= 0 or D % 4 not in (0, 1):
        raise ValueError('negative discriminant required')
    A = isqrt(-D // 3)
    spf = _cache.get(A)
    if spf is None:
        spf = _spf(max(4 * A + 4, 16))
        _cache.clear()
        _cache[A] = spf
    h = 0
    for a in range(1, A + 1):
        n, fac = 4 * a, {}
        while n > 1:
            q = spf[n]
            fac[q] = fac.get(q, 0) + 1
            n //= q
        residues = [0]
        modulus = 1
        for q, e in fac.items():
            rq = _roots_pp(D, q, e)
            if not rq:
                residues = []
                break
            qe = q ** e
            inv = pow(modulus, -1, qe)
            residues = [(r + modulus * ((s - r) * inv % qe)) for r in residues for s in rq]
            modulus *= qe
        bs = {r % (2 * a) for r in residues}
        for r in bs:
            b = r if r <= a else r - 2 * a
            c = (b * b - D) // (4 * a)
            if c < a:
                continue
            if b < 0 and (-b == a or a == c):
                continue
            if gcd(gcd(a, abs(b)), c) != 1:
                continue
            h += 1
    return h


# ---------------------------------------------------------------- half factorial
def cornacchia_a(p):
    """p = 5 mod 8: return a with p=a^2+b^2, a = 1 mod 4 (deterministic sqrt(-1)=2^((p-1)/4))."""
    if p % 8 != 5:
        raise ValueError('deterministic square root of -1 used here needs p = 5 mod 8')
    r = pow(2, (p - 1) // 4, p)
    a0, b0 = p, r if r < p - r else p - r
    lim = isqrt(p)
    while b0 > lim:
        a0, b0 = b0, a0 % b0
    x = b0
    y2 = p - x * x
    y = isqrt(y2)
    assert y * y == y2
    a = x if x % 2 else y
    return a if a % 4 == 1 else -a


def half_factorial(p, route=None, classno_fn=classno):
    """((p-1)/2)! mod p acquired from class numbers; returns (H, metadata)."""
    parameters(p)
    h = (p - 1) // 2
    if route is None:
        route = 'mordell' if p % 4 == 3 else ('gauss4p' if p % 8 == 5 else 'h3p')
    if route == 'mordell':
        if p % 4 != 3:
            raise ValueError
        hD = classno_fn(-p)
        H = 1 if ((hD + 1) // 2) % 2 == 0 else p - 1
        return H, dict(route=route, D=-p, classno=hD, status='theorem (Mordell 1961)')
    if route == 'gauss4p':
        if p % 8 != 5:
            raise ValueError
        hD = classno_fn(-4 * p)
        q = (p - 1) // 4                       # odd
        lam = 1 if ((q - hD // 2) // 2) % 2 == 0 else -1
        a = cornacchia_a(p)
        iota = pow(2, q, p)                    # a square root of -1
        target = lam * pow(2 * a % p, q, p) % p
        H = iota if pow(iota, q, p) == target else p - iota
        assert pow(H, q, p) == target
        return H, dict(route=route, D=-4 * p, classno=hD, a=a,
                       status='theorem (Gauss binomial congruence + Dirichlet class number formula)')
    if route == 'h3p':
        if p % 4 != 1:
            raise ValueError
        m = (p - 2) // 3
        hD = classno_fn(-3 * p)
        leg = 1 if ((m - hD // 2) // 2) % 2 == 0 else -1
        two = 1 if p % 8 == 1 else -1
        H = two * leg * pow(3, (p - 1) // 4, p) % p
        return H, dict(route=route, D=-3 * p, classno=hD,
                       status='CONJECTURE (*) with finite evidence; Dirichlet-type sum identity')
    raise ValueError(route)


def halfinterval_c(p, route=None, layout=1, classno_fn=classno, product_fn=None):
    """c_p = 2 H P^3 with P = prod_{(p+1)/3}^{(p-1)/2} j, H from class numbers.

    layout=1: one rising-product channel of length (p+1)/6.
    layout=2: two channels of length about (p+1)/12 sharing one evaluation tree.
    product_fn(p, length, starts) may replace the stdlib engine (e.g. FLINT backend).
    """
    parameters(p)
    start, L = (p + 1) // 3, (p + 1) // 6
    H, hmeta = half_factorial(p, route, classno_fn)
    eng = product_fn or (lambda p_, L_, s_: pochhammer_many(p_, L_, s_))
    if layout == 1:
        (P,), meta = eng(p, L, [start])
    else:
        L1 = L // 2
        (P1, P2), meta = eng(p, L1, [start, start + L1])
        P = P1 * P2 % p
        for j in range(start + 2 * L1, start + L):      # at most one tail factor
            P = P * (j % p) % p
    c = 2 * H * pow(P, 3, p) % p
    return c, dict(half_factorial=hmeta, product_length=L, layout=layout, product=meta)
