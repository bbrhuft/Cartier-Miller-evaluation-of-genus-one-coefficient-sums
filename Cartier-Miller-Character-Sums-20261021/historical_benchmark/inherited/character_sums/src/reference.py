"""Independent reference computations (ground truth) for the character-sum investigation.

Nothing here imports the candidate implementation (cmcs.py) or the inherited
Cartier-Miller evaluator.  Three independent mechanisms are provided:

  * direct enumeration of quadratic-character values and of actual points
    (y counted by a table of squares, not by Euler's criterion);
  * polynomial powers f^h computed by FLINT (python-flint), from which the
    truncation T_f and any coefficient c_m are read off;
  * Frobenius traces from PARI/GP (hyperellcharpoly), cross-checked against
    direct point counts where p is small enough.

numpy is used for vectorised enumeration; every residue stays below 2^31, so
products fit in int64.
"""
import numpy as np

# ----------------------------------------------------------------- integers

def is_prime(n):
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for q in small:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:          # deterministic for n < 3.3e24
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


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def peval(f, x, p):
    v = 0
    for c in reversed(f):
        v = (v * x + c) % p
    return v

# ----------------------------------------------------------------- tables

def square_counts(p):
    """counts[a] = #{y in F_p : y^2 = a}, by enumerating y (no Euler criterion)."""
    y = np.arange(p, dtype=np.int64)
    return np.bincount((y * y) % p, minlength=p).astype(np.int64)


def poly_values(f, p):
    """f(x) mod p for every x in F_p (vectorised Horner)."""
    x = np.arange(p, dtype=np.int64)
    v = np.zeros(p, dtype=np.int64)
    for c in reversed(f):
        v = (v * x + (c % p)) % p
    return v


def fibre_counts(f, p, counts=None):
    """nu(x) = number of affine points over x, by direct count of y."""
    if counts is None:
        counts = square_counts(p)
    return counts[poly_values(f, p)]


def inverse_table(p):
    """inv[t] = t^{-1} mod p for t = 1..p-1 (inv[0] = 0), by vectorised t^(p-2)."""
    t = np.arange(p, dtype=np.int64)
    result = np.ones(p, dtype=np.int64)
    base = t.copy()
    e = p - 2
    while e:
        if e & 1:
            result = (result * base) % p
        base = (base * base) % p
        e >>= 1
    result[0] = 0
    return result

# ----------------------------------------------------------------- traces

def trace_by_count(f, p, counts=None):
    """tau = p + 1 - #E(F_p) for the smooth projective model of y^2 = f(x)."""
    nu = fibre_counts(f, p, counts)
    deg = len(f) - 1
    while f[deg] % p == 0:
        deg -= 1
    if deg == 3:
        n_inf = 1
    elif deg == 4:
        n_inf = 1 + legendre(f[4], p)
    else:
        raise ValueError('degree must be 3 or 4')
    return p + 1 - int(nu.sum()) - n_inf


_PARI = None


def pari():
    global _PARI
    if _PARI is None:
        import cypari2
        _PARI = cypari2.Pari()
        _PARI.allocatemem(4 * 10**8, silent=True)
    return _PARI


def trace_invariants(f, p):
    """Trace via the classical-invariant Jacobian y^2 = x^3 - 27 I x - 27 J of the quartic
    (a cubic is treated as a quartic with a = 0) and PARI's ellap.  Over a finite field a
    genus-one curve and its Jacobian have equally many points.  Valid for p >= 5."""
    P = pari()
    g = [c % p for c in f] + [0] * (5 - len(f))
    e, d, c, b, a = g
    I = (12 * a * e - 3 * b * d + c * c) % p
    J = (72 * a * c * e + 9 * b * c * d - 27 * a * d * d - 27 * e * b * b - 2 * c ** 3) % p
    E = P.ellinit([0, 0, 0, (-27 * I) % p, (-27 * J) % p], p)
    return int(P.ellap(E))


def trace_pari(f, p):
    """Trace from PARI: hyperellcharpoly for p < 5000 (cross-checked against the
    invariant route), the invariant route otherwise."""
    if p >= 5000:
        return trace_invariants(f, p)
    t = trace_hyperell(f, p)
    if t != trace_invariants(f, p):
        raise ArithmeticError('PARI trace routes disagree')
    return t


def trace_hyperell(f, p):
    """Trace of Frobenius via PARI hyperellcharpoly (charpoly x^2 - t x + p)."""
    P = pari()
    poly = P('Mod(1,%d)*(%s)' % (p, ' + '.join('(%d)*x^%d' % (c % p, i) for i, c in enumerate(f))))
    cp = P.hyperellcharpoly(poly)
    t = -int(P.polcoef(cp, 1))
    if int(P.polcoef(cp, 0)) != p or int(P.polcoef(cp, 2)) != 1:
        raise ArithmeticError('unexpected charpoly shape')
    return t

# ----------------------------------------------------------------- polynomial powers

def power_coefficients(f, p):
    """All coefficients c_0..c_{deg(f) h} of f^h over F_p, computed by FLINT."""
    import flint
    h = (p - 1) // 2
    P = flint.nmod_poly([c % p for c in f], p) ** h
    co = [int(c) for c in P.coeffs()]
    full = h * (len(f) - 1) + 1
    return co + [0] * (full - len(co))


def truncation_value(c, mu, p):
    """T_f(mu) = sum_{m<p} c_m mu^m."""
    v = 0
    for m in range(min(p, len(c)) - 1, -1, -1):
        v = (v * mu + c[m]) % p
    return v

# ----------------------------------------------------------------- direct sums

class DirectSums:
    """Ground truth for one (p, f): every sum is formed by enumeration over F_p."""

    def __init__(self, p, f, counts=None, inv=None):
        self.p = p
        self.f = [c % p for c in f]
        self.counts = square_counts(p) if counts is None else counts
        self.inv = inverse_table(p) if inv is None else inv
        self.nu = fibre_counts(self.f, p, self.counts)          # actual points
        vals = poly_values(self.f, p)
        sq = self.counts > 0
        self.eps = np.where(vals == 0, 0, np.where(sq[vals], 1, -1)).astype(np.int64)
        assert np.array_equal(self.nu, 1 + self.eps)              # sanity of the two routes

    def weight_vector(self, simple=(), double=(), poly=(), b=0, excluded=()):
        """Return (mask, R) with R(x) mod p on the common domain x notin U."""
        p = self.p
        x = np.arange(p, dtype=np.int64)
        U = set(m for m, _ in simple) | set(m for m, _ in double) | set(excluded)
        mask = np.ones(p, dtype=bool)
        for u in U:
            mask[u] = False
        R = np.full(p, b % p, dtype=np.int64)
        for mu, a in simple:
            R = (R + (a % p) * self.inv[(x - mu) % p]) % p
        for mu, a in double:
            iv = self.inv[(x - mu) % p]
            R = (R + (a % p) * ((iv * iv) % p)) % p
        xp = np.ones(p, dtype=np.int64)
        for k, a in enumerate(poly):
            if a % p:
                R = (R + (a % p) * xp) % p
            xp = (xp * x) % p
        return mask, R

    def character_sum(self, **kw):
        mask, R = self.weight_vector(**kw)
        return int(((self.eps[mask] % self.p) * R[mask] % self.p).sum() % self.p)

    def affine_point_sum(self, **kw):
        mask, R = self.weight_vector(**kw)
        return int((self.nu[mask] * R[mask] % self.p).sum() % self.p)

    def integer_character_sum(self, excluded=()):
        mask = np.ones(self.p, dtype=bool)
        for u in excluded:
            mask[u] = False
        return int(self.eps[mask].sum())

    def multiplicative_sum(self, mu):
        """Integer sum_{x != mu} chi(f(x)/(x - mu)) -- the *different* problem."""
        p = self.p
        x = np.arange(p, dtype=np.int64)
        mask = x != mu
        vals = poly_values(self.f, p) * ((x - mu) % p) % p      # chi(f/(x-mu)) = chi(f (x-mu))
        sq = self.counts > 0
        e = np.where(vals == 0, 0, np.where(sq[vals], 1, -1))
        return int(e[mask].sum())

# ----------------------------------------------------------------- F_{p^2} for extension poles

class Fp2:
    """F_p[t]/(t^2 - n) with n a nonresidue; elements (a, b) = a + b t."""

    def __init__(self, p):
        self.p = p
        self.n = next(c for c in range(2, p) if legendre(c, p) == -1)

    def mul(self, u, v):
        p = self.p
        return ((u[0] * v[0] + self.n * u[1] * v[1]) % p, (u[0] * v[1] + u[1] * v[0]) % p)

    def add(self, u, v):
        return ((u[0] + v[0]) % self.p, (u[1] + v[1]) % self.p)

    def sub(self, u, v):
        return ((u[0] - v[0]) % self.p, (u[1] - v[1]) % self.p)

    def pow(self, u, e):
        r, b = (1, 0), u
        while e:
            if e & 1:
                r = self.mul(r, b)
            b = self.mul(b, b)
            e >>= 1
        return r

    def inv(self, u):
        p = self.p
        nrm = (u[0] * u[0] - self.n * u[1] * u[1]) % p
        ni = pow(nrm, -1, p)
        return (u[0] * ni % p, (-u[1]) * ni % p)

    def scal(self, c):
        return (c % self.p, 0)
