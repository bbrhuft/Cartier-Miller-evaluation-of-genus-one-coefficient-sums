"""
Minimal exact finite-field / finite-algebra contexts used by the Cartier–Miller evaluator.
Every context exposes: zero, one, fromint, add, sub, neg, mul, inv, iszero, eq, powi.
  FpCtx(p)          : F_p, elements are Python ints in [0, p)
  QuadCtx(p, d)     : F_p[s]/(s^2 - d), elements (a, b) = a + b s. A field iff d is a nonsquare.
                      If d is a nonzero square the algebra splits; inv() then raises ZeroDivisorFound
                      carrying the witness, from which sqrt(d) is read off.
  GFCtx(p, modulus) : F_p[x]/(m(x)) for an irreducible monic m; elements are tuples (low -> high).
"""
import random

class ZeroDivisorFound(ArithmeticError):
    def __init__(self, element):
        super().__init__("zero divisor encountered")
        self.element = element

def legendre(a, p):
    a %= p
    if a == 0: return 0
    return 1 if pow(a, (p - 1)//2, p) == 1 else -1

def sqrt_mod_p(a, p, nonresidue=None):
    """Tonelli–Shanks; deterministic given a fixed nonresidue."""
    a %= p
    if a == 0: return 0
    assert pow(a, (p-1)//2, p) == 1, "not a square"
    if p % 4 == 3: return pow(a, (p+1)//4, p)
    q, s = p - 1, 0
    while q % 2 == 0: q //= 2; s += 1
    z = nonresidue or next(c for c in range(2, p) if pow(c, (p-1)//2, p) == p-1)
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q+1)//2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1: t2 = t2*t2 % p; i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b*b % p, t*b*b % p, r*b % p
    return r

class FpCtx:
    def __init__(s, p): s.p = p; s.zero = 0; s.one = 1
    def fromint(s, n): return n % s.p
    def add(s, a, b): return (a + b) % s.p
    def sub(s, a, b): return (a - b) % s.p
    def neg(s, a): return (-a) % s.p
    def mul(s, a, b): return a * b % s.p
    def inv(s, a):
        if a % s.p == 0: raise ZeroDivisionError("inverse of 0")
        return pow(a, -1, s.p)
    def iszero(s, a): return a % s.p == 0
    def eq(s, a, b): return (a - b) % s.p == 0
    def powi(s, a, e): return pow(a, e, s.p)

class QuadCtx:
    def __init__(s, p, d):
        s.p, s.d = p, d % p
        s.zero, s.one = (0, 0), (1, 0)
        s.gen = (0, 1)
    def fromint(s, n): return (n % s.p, 0)
    def add(s, a, b): p = s.p; return ((a[0]+b[0]) % p, (a[1]+b[1]) % p)
    def sub(s, a, b): p = s.p; return ((a[0]-b[0]) % p, (a[1]-b[1]) % p)
    def neg(s, a): p = s.p; return ((-a[0]) % p, (-a[1]) % p)
    def mul(s, a, b):
        p = s.p
        return ((a[0]*b[0] + s.d*a[1]*b[1]) % p, (a[0]*b[1] + a[1]*b[0]) % p)
    def inv(s, a):
        p = s.p
        n = (a[0]*a[0] - s.d*a[1]*a[1]) % p
        if n == 0:
            if a[0] % p == 0 and a[1] % p == 0: raise ZeroDivisionError("inverse of 0")
            raise ZeroDivisorFound(a)
        ni = pow(n, -1, p)
        return (a[0]*ni % p, (-a[1]*ni) % p)
    def iszero(s, a): return a[0] % s.p == 0 and a[1] % s.p == 0
    def eq(s, a, b): return s.iszero(s.sub(a, b))
    def powi(s, a, e):
        r, b = s.one, a
        while e:
            if e & 1: r = s.mul(r, b)
            b = s.mul(b, b); e >>= 1
        return r
    def conj(s, a): return (a[0], (-a[1]) % s.p)
    def sqrt_from_witness(s, z):
        """z = a + b s nonzero with norm a^2 - d b^2 = 0  =>  b != 0 and (a/b)^2 = d.  O(1) field operations."""
        a, b = z[0] % s.p, z[1] % s.p
        assert b != 0 and (a*a - s.d*b*b) % s.p == 0
        return a * pow(b, -1, s.p) % s.p

class GFCtx:
    """F_{p^k} = F_p[x]/(m), m monic irreducible of degree k (low -> high coefficient list, length k+1)."""
    def __init__(s, p, m):
        s.p, s.m, s.k = p, [c % p for c in m], len(m) - 1
        assert s.m[-1] == 1
        s.zero = tuple([0]*s.k); s.one = tuple([1] + [0]*(s.k-1))
        s.gen = tuple([0, 1] + [0]*(s.k-2)) if s.k > 1 else (0,)
    def fromint(s, n): return tuple([n % s.p] + [0]*(s.k-1))
    def add(s, a, b): return tuple((x+y) % s.p for x, y in zip(a, b))
    def sub(s, a, b): return tuple((x-y) % s.p for x, y in zip(a, b))
    def neg(s, a): return tuple((-x) % s.p for x in a)
    def mul(s, a, b):
        p, k, m = s.p, s.k, s.m
        prod = [0]*(2*k - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    prod[i+j] += x*y
        for i in range(2*k - 2, k - 1, -1):
            c = prod[i] % p
            if c:
                for j in range(k):
                    prod[i - k + j] -= c * m[j]
            prod[i] = 0
        return tuple(x % p for x in prod[:k])
    def powi(s, a, e):
        r, b = s.one, a
        while e:
            if e & 1: r = s.mul(r, b)
            b = s.mul(b, b); e >>= 1
        return r
    def inv(s, a):
        """Extended Euclid in F_p[x] modulo the irreducible modulus: O(k^2) operations in F_p."""
        if s.iszero(a): raise ZeroDivisionError("inverse of 0")
        p = s.p
        def trim(u):
            u = [c % p for c in u]
            while u and u[-1] == 0: u.pop()
            return u
        def sub_mul(u, c, sh, v):          # u - c * x^sh * v
            u = u + [0]*max(0, len(v) + sh - len(u))
            for i, x in enumerate(v): u[i + sh] = (u[i + sh] - c*x) % p
            return trim(u)
        r0, r1 = trim(list(s.m)), trim(list(a))
        t0, t1 = [], [1]
        while len(r1) > 1:
            while len(r0) >= len(r1) and r0:
                c = r0[-1] * pow(r1[-1], -1, p) % p; sh = len(r0) - len(r1)
                r0 = sub_mul(r0, c, sh, r1); t0 = sub_mul(t0, c, sh, t1)
            r0, r1, t0, t1 = r1, r0, t1, t0
        c = pow(r1[0], -1, p)
        out = [(x * c) % p for x in t1] + [0]*s.k
        return tuple(out[:s.k])
    def iszero(s, a): return all(x % s.p == 0 for x in a)
    def eq(s, a, b): return s.iszero(s.sub(a, b))
    def frob(s, a): return s.powi(a, s.p)
    def is_square(s, a):
        q = s.p**s.k
        return s.iszero(a) or s.eq(s.powi(a, (q-1)//2), s.one)
    def sqrt(s, a, rng=random.Random(1)):
        """Tonelli–Shanks in F_q."""
        q = s.p**s.k
        if s.iszero(a): return s.zero
        assert s.is_square(a)
        Q, S = q - 1, 0
        while Q % 2 == 0: Q //= 2; S += 1
        while True:
            z = tuple(rng.randrange(s.p) for _ in range(s.k))
            if not s.iszero(z) and not s.is_square(z): break
        M, c, t, R = S, s.powi(z, Q), s.powi(a, Q), s.powi(a, (Q+1)//2)
        while not s.eq(t, s.one):
            i, t2 = 0, t
            while not s.eq(t2, s.one): t2 = s.mul(t2, t2); i += 1
            b = s.powi(c, 1 << (M - i - 1))
            M, c, t, R = i, s.mul(b, b), s.mul(t, s.mul(b, b)), s.mul(R, b)
        return R

def irreducible_modulus(p, k, seed=0):
    """Find a monic irreducible polynomial of degree k over F_p (k <= 4) by rejection with a root/quad test."""
    rng = random.Random(seed)
    from sympy import Poly, GF
    from sympy.abc import x
    while True:
        m = [rng.randrange(p) for _ in range(k)] + [1]
        P = Poly(list(reversed(m)), x, modulus=p)
        if P.is_irreducible: return m


class QuadOver:
    """B[s]/(s^2 - d) over a base context B (e.g. GFCtx).  A field iff d is a nonsquare in B.
    In the split case a failed inversion raises ZeroDivisorFound, whose witness yields sqrt(d) in B."""
    def __init__(s, B, d):
        s.B, s.d = B, d
        s.zero, s.one, s.gen = (B.zero, B.zero), (B.one, B.zero), (B.zero, B.one)
    def fromint(s, n): return (s.B.fromint(n), s.B.zero)
    def embed(s, x): return (x, s.B.zero)
    def add(s, a, b): return (s.B.add(a[0], b[0]), s.B.add(a[1], b[1]))
    def sub(s, a, b): return (s.B.sub(a[0], b[0]), s.B.sub(a[1], b[1]))
    def neg(s, a): return (s.B.neg(a[0]), s.B.neg(a[1]))
    def mul(s, a, b):
        B = s.B
        return (B.add(B.mul(a[0], b[0]), B.mul(s.d, B.mul(a[1], b[1]))),
                B.add(B.mul(a[0], b[1]), B.mul(a[1], b[0])))
    def inv(s, a):
        B = s.B
        n = B.sub(B.mul(a[0], a[0]), B.mul(s.d, B.mul(a[1], a[1])))
        if B.iszero(n):
            if B.iszero(a[0]) and B.iszero(a[1]): raise ZeroDivisionError("inverse of 0")
            raise ZeroDivisorFound(a)
        ni = B.inv(n)
        return (B.mul(a[0], ni), B.neg(B.mul(a[1], ni)))
    def iszero(s, a): return s.B.iszero(a[0]) and s.B.iszero(a[1])
    def eq(s, a, b): return s.iszero(s.sub(a, b))
    def powi(s, a, e):
        r, b = s.one, a
        while e:
            if e & 1: r = s.mul(r, b)
            b = s.mul(b, b); e >>= 1
        return r
    def sqrt_from_witness(s, z):
        return s.B.mul(z[0], s.B.inv(z[1]))
