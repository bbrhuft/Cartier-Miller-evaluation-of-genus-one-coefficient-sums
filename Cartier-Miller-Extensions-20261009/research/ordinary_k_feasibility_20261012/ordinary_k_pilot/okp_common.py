"""Shared exact arithmetic for the ordinary Cartier-slope feasibility pilot.

Standard library only.  Everything here is either elementary finite-field
arithmetic or a small capped-absolute-precision p-adic number class.  Nothing
here is a fast algorithm; the purpose is independent verification of the
identities derived in the feasibility note.

Conventions (identical to the handover):
    E : y^2 = F(x) = x^3 + A x + B over F_p, p >= 7 prime, h = (p-1)/2,
    H = [x^(p-1)] F^h,  beta = [x^(p-2)] F^h,  kappa = beta / H,
    omega = dx/y, eta = x dx/y,  column convention phi^*(omega,eta) = (omega,eta) M.
"""
from math import isqrt
import hashlib
import platform
import sys


class CheckFailure(AssertionError):
    """Raised on any mathematical disagreement; run scripts exit nonzero."""


def require(cond, msg):
    if not cond:
        raise CheckFailure(msg)


# ---------------------------------------------------------------- primes
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
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):  # deterministic for n < 3.3e24
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


def primes_between(lo, hi):
    return [q for q in range(max(lo, 2), hi + 1) if is_prime(q)]


# ---------------------------------------------------------------- curve basics
def nonsingular(A, B, p):
    return (4 * A ** 3 + 27 * B * B) % p != 0


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def trace_by_count(A, B, p):
    """Direct point count: t = p + 1 - #E(F_p) = -sum_x chi(F(x))."""
    return -sum(legendre(x * x * x + A * x + B, p) for x in range(p))


def points(A, B, p):
    """All affine F_p-points (list of (x, y))."""
    sq = {}
    for y in range(p):
        sq.setdefault(y * y % p, []).append(y)
    out = []
    for x in range(p):
        for y in sq.get((x * x * x + A * x + B) % p, []):
            out.append((x, y))
    return out


def j_invariant(A, B, p):
    return 6912 * pow(A, 3, p) * pow((4 * pow(A, 3, p) + 27 * B * B) % p, -1, p) % p


def H_beta_recurrence(A, B, p):
    """[x^(p-1)]F^h and [x^(p-2)]F^h via the order-3 recurrence of F^h.

    From F (F^h)' = h F' F^h, with c_n = [x^n] F^h:
        B (n+1) c_{n+1} = (h - n) A c_n + (3h - n + 2) c_{n-2}.
    This is an implementation independent of the handover's multinomial
    extraction and of dense powering.  Requires B != 0 (else uses dense).
    """
    h = (p - 1) // 2
    A %= p
    B %= p
    if B == 0:
        P = dense_power([0, A, 0, 1], h, p)
        return P[p - 1], P[p - 2]
    c = [0] * (p + 1)
    c[0] = pow(B, h, p)
    invB = pow(B, -1, p)
    for n in range(0, p - 1):
        rhs = (h - n) * A % p * c[n] % p
        if n >= 2:
            rhs = (rhs + (3 * h - n + 2) * c[n - 2]) % p
        c[n + 1] = rhs * invB % p * pow(n + 1, -1, p) % p
    return c[p - 1], c[p - 2]


def dense_power(f, e, p):
    out = [1]
    for _ in range(e):
        new = [0] * (len(out) + len(f) - 1)
        for i, a in enumerate(out):
            if a:
                for j, b in enumerate(f):
                    new[i + j] = (new[i + j] + a * b) % p
        out = new
    return out


def kappa_target(A, B, p):
    H, beta = H_beta_recurrence(A, B, p)
    return H, beta, (beta * pow(H, -1, p) % p if H else None)


# ---------------------------------------------------------------- polynomials mod m
def ptrim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def padd(a, b, m):
    n = max(len(a), len(b))
    return ptrim([((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % m for i in range(n)])


def psub(a, b, m):
    n = max(len(a), len(b))
    return ptrim([((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % m for i in range(n)])


def pmul(a, b, m):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return ptrim([v % m for v in out])


def pscale(a, c, m):
    return ptrim([x * c % m for x in a])


def peval(a, x, m):
    v = 0
    for c in reversed(a):
        v = (v * x + c) % m
    return v


def division_polynomial_odd(n, A, B, m):
    """f_n in (Z/m)[x] with psi_n = f_n for odd n (Washington's normalization;
    psi_n = 2y f_n for even n).  Only the indices needed by the doubling
    recursion are computed (memoized)."""
    F = [B % m, A % m, 0, 1]
    F2 = pmul(F, F, m)
    memo = {0: [], 1: [1], 2: [1],
            3: ptrim([(-A * A) % m, (12 * B) % m, (6 * A) % m, 0, 3 % m]),
            4: ptrim([(-2 * A ** 3 - 16 * B * B) % m, (-8 * A * B) % m, (-10 * A * A) % m,
                      (40 * B) % m, (10 * A) % m, 0, 2 % m])}

    def f(k):
        if k in memo:
            return memo[k]
        if k % 2 == 1:
            mm = (k - 1) // 2
            if mm % 2 == 0:
                left = pmul(pscale(F2, 16, m), pmul(f(mm + 2), pmul(f(mm), pmul(f(mm), f(mm), m), m), m), m)
                right = pmul(f(mm - 1), pmul(f(mm + 1), pmul(f(mm + 1), f(mm + 1), m), m), m)
            else:
                left = pmul(f(mm + 2), pmul(f(mm), pmul(f(mm), f(mm), m), m), m)
                right = pmul(pscale(F2, 16, m), pmul(f(mm - 1), pmul(f(mm + 1), pmul(f(mm + 1), f(mm + 1), m), m), m), m)
            res = psub(left, right, m)
        else:
            mm = k // 2
            inner = psub(pmul(f(mm + 2), pmul(f(mm - 1), f(mm - 1), m), m),
                         pmul(f(mm - 2), pmul(f(mm + 1), f(mm + 1), m), m), m)
            res = pmul(f(mm), inner, m)
        memo[k] = res
        return res

    return f(n)


# ---------------------------------------------------------------- capped p-adic numbers
class PAdic:
    """x = p^val * unit, unit a p-adic unit known modulo p^rel (rel >= 0).

    Absolute precision aprec = val + rel: x is known modulo p^aprec.  A value
    that is zero to its absolute precision has unit = 0, rel = 0, val = aprec.
    Capped-absolute semantics: every operation returns the honest precision."""
    __slots__ = ('p', 'val', 'unit', 'rel')

    def __init__(self, p, val, unit, rel):
        self.p, self.val, self.unit, self.rel = p, val, unit, rel

    @staticmethod
    def from_int(p, n, aprec):
        mod = p ** aprec
        n %= mod
        if n == 0:
            return PAdic(p, aprec, 0, 0)
        v = 0
        while n % p == 0:
            n //= p
            v += 1
        return PAdic(p, v, n % p ** (aprec - v), aprec - v)

    @property
    def aprec(self):
        return self.val + self.rel

    def is_zero(self):
        return self.rel == 0

    def _coerce(self, o):
        if isinstance(o, PAdic):
            return o
        return PAdic.from_int(self.p, o, max(self.aprec, 0) + 64)

    def __add__(self, o):
        o = self._coerce(o)
        p = self.p
        ap = min(self.aprec, o.aprec)
        lo = min(self.val, o.val)
        if ap <= lo:
            return PAdic(p, ap, 0, 0)
        mod = p ** (ap - lo)
        s = (self.unit * p ** (self.val - lo) + o.unit * p ** (o.val - lo)) % mod
        if s == 0:
            return PAdic(p, ap, 0, 0)
        v = 0
        while s % p == 0:
            s //= p
            v += 1
        return PAdic(p, lo + v, s % p ** (ap - lo - v), ap - lo - v)

    __radd__ = __add__

    def __neg__(self):
        return PAdic(self.p, self.val, (-self.unit) % (self.p ** self.rel) if self.rel else 0, self.rel)

    def __sub__(self, o):
        return self + (-self._coerce(o))

    def __rsub__(self, o):
        return self._coerce(o) + (-self)

    def __mul__(self, o):
        o = self._coerce(o)
        p = self.p
        if self.is_zero() or o.is_zero():
            # zero times x is zero to absolute precision val_zero + val_other
            ap = min(self.aprec + (o.val if not o.is_zero() else o.aprec),
                     o.aprec + (self.val if not self.is_zero() else self.aprec))
            return PAdic(p, ap, 0, 0)
        rel = min(self.rel, o.rel)
        return PAdic(p, self.val + o.val, self.unit * o.unit % p ** rel, rel)

    __rmul__ = __mul__

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, 'PAdic power must be a nonnegative int')
        out = PAdic.from_int(self.p, 1, max(self.aprec, 1) + 64)
        for _ in range(n):
            out = out * self
        return out

    def inverse(self):
        require(not self.is_zero(), 'PAdic inverse of zero-to-precision')
        return PAdic(self.p, -self.val, pow(self.unit, -1, self.p ** self.rel), self.rel)

    def __truediv__(self, o):
        return self * self._coerce(o).inverse()

    def __rtruediv__(self, o):
        return self._coerce(o) * self.inverse()

    def residue(self, k=1):
        """Integer representative modulo p^k; requires integrality to that precision."""
        p = self.p
        require(self.aprec >= k, f'insufficient precision: need {k}, have {self.aprec}')
        if self.is_zero() or self.val >= k:
            return 0
        require(self.val >= 0, f'value not integral (val={self.val})')
        return self.unit * p ** self.val % p ** k

    def __repr__(self):
        return f'PAdic(p={self.p}, val={self.val}, unit={self.unit}, rel={self.rel})'


# ---------------------------------------------------------------- bookkeeping
def sha256_file(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def environment():
    return {'python': sys.version, 'platform': platform.platform(),
            'dependencies': 'Python standard library only'}


# ---------------------------------------------------------------- original cubic
def cubic_from_point(A, B, p, x0, y0):
    """f = 1 + c w + b w^2 + a w^3 with x = a w + b/3, y = a v (handover convention)."""
    a = y0 % p
    b = 3 * x0 % p
    c = (A + 3 * x0 * x0) * pow(y0, -1, p) % p
    return [1, c, b, a]


def short_model_of_cubic(f, p):
    _, c, b, a = f
    i3 = pow(3, -1, p)
    return ((a * c - b * b * i3) % p,
            (a * a - a * b * c * i3 + 2 * pow(b, 3, p) * pow(27, -1, p)) % p)


def branch_outputs_from_kappa(f, H, kappa, p):
    """Reconstruct (H, K, {mu: T_f(mu)}) from H and kappa only (no coefficient access)."""
    _, c, b, a = f
    beta = kappa * H % p
    K = (beta - b * pow(3, -1, p) * H) * pow(a, -1, p) % p
    out = {}
    for mu in range(1, p):
        if peval(f, mu, p):
            continue
        der = (c + 2 * b * mu + 3 * a * mu * mu) % p
        require(der != 0, 'repeated root in a nonsingular cubic')
        out[mu] = a * mu * (mu * H - K) * pow(der, -1, p) % p
    return K, out


def branch_outputs_direct(f, p):
    """Independent dense reference: coefficients of f^h, strict prefix sums."""
    h = (p - 1) // 2
    P = dense_power(f, h, p)
    P += [0] * (p + 1 - len(P))
    H, K = P[p - 1], P[p - 2]
    out = {}
    for mu in range(1, p):
        if peval(f, mu, p):
            continue
        out[mu] = peval(P[:p], mu, p)
    return H, K, out
