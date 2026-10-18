"""Exact Jacobi sums J(chi^u, chi^v) in Z[zeta_q] for a prime q | p-1 (split case).

Conventions (Tal 2026, Sec. 2.2/2.4; van Wamelen 2002, Sec. 1):
  K = (p-1)/q, eta in F_p of exact order q, rho: Z[zeta_q] -> F_p, zeta_q -> eta.
  chi is the order-q character with rho(chi(x)) = x^{-K};  chi(0) = 0.
  J(chi^u, chi^v) = sum_{x in F_p} chi^u(x) chi^v(1-x).
For 1 <= u, v and u + v < q (all exponents nonzero mod q):
  (J) = prod_{t in S(u,v)} p_t,   p_t = (p, zeta - eta^t),
  S(u,v) = {1 <= t < q : (ut mod q) + (vt mod q) >= q}          (Stickelberger, split case)
  J Jbar = p,  rho(J) = -binom((u+v)K, uK)  (mod p).
Reconstruction (Lenstra's idea in van Wamelen Sec. 7): with the trace form Tr(x xbar), the
minimal vectors of the ideal lattice are exactly the 2q roots-of-unity multiples of J
(AM-GM: Tr(x xbar) >= (q-1) N(x)^{2/(q-1)} >= (q-1) p, equality iff x generates and |sigma x|^2=p).
We LLL-reduce, take a vector of squared length (q-1)p, CERTIFY x xbar = p in Z[zeta] (so x
generates the ideal and x = eps J with eps a root of unity, by Kronecker), and select eps by
van Wamelen's Theorem 6/8/9: the unique twist whose degree-<q lift I with I(1) = p-2 is
integral and satisfies sum_i i a_i = 0 (mod q).  Fallback if LLL's first vectors miss the
minimum: exact Fincke-Pohst enumeration (PARI qfminim) at the known minimum (q-1)p.
"""
from math import gcd

_PARI = []


def _pari():
    if not _PARI:
        import cypari2
        _PARI.append(cypari2.Pari())
    return _PARI[0]


# ------------------------------------------------------------ Z[zeta_q] arithmetic
def _reduce(c, q):
    """coefficient list of length q (mod x^q - 1) -> length q-1 (mod Phi_q)."""
    top = c[q - 1]
    return [c[i] - top for i in range(q - 1)]


def mul(a, b, q):
    """product in Z[zeta_q]; a, b length q-1 vectors (power basis)."""
    c = [0] * q
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    c[(i + j) % q] += ai * bj
    return _reduce(c, q)


def conj(a, q):
    c = [0] * q
    for i, ai in enumerate(a):
        c[(-i) % q] += ai
    return _reduce(c, q)


def galois(a, t, q):
    """sigma_t: zeta -> zeta^t."""
    c = [0] * q
    for i, ai in enumerate(a):
        c[(i * t) % q] += ai
    return _reduce(c, q)


def times_root(a, k, sign, q):
    """sign * zeta^k * a."""
    c = [0] * q
    for i, ai in enumerate(a):
        c[(i + k) % q] += sign * ai
    return _reduce(c, q)


def evaluate(a, eta, p):
    r, e = 0, 1
    for ai in a:
        r = (r + ai * e) % p
        e = e * eta % p
    return r


# ------------------------------------------------------------ setup
def element_of_order(p, q):
    """eta = x^((p-1)/q) for the least x >= 2 giving eta != 1 (q prime, q | p-1).

    Deterministic; the number of trials is bounded by the least q-th power non-residue.
    """
    K = (p - 1) // q
    x = 2
    while True:
        eta = pow(x, K, p)
        if eta != 1:
            return eta, x
        x += 1


def stickelberger_set(q, u, v):
    return [t for t in range(1, q) if (u * t) % q + (v * t) % q >= q]


def ideal_basis(p, q, eta, S):
    """Z-basis (columns as lists) of {f in Z[zeta]: f(eta^t) = 0 mod p for t in S}."""
    d, s = q - 1, len(S)
    rows = [[pow(eta, t * i, p) for i in range(d)] for t in S]
    # row-reduce the s x d system mod p on the first s columns (Vandermonde => invertible)
    A = [r[:] for r in rows]
    for col in range(s):
        piv = next(r for r in range(col, s) if A[r][col] % p)
        A[col], A[piv] = A[piv], A[col]
        inv = pow(A[col][col], p - 2, p)
        A[col] = [x * inv % p for x in A[col]]
        for r in range(s):
            if r != col and A[r][col]:
                f = A[r][col]
                A[r] = [(x - f * y) % p for x, y in zip(A[r], A[col])]
    basis = []
    for i in range(s):
        e = [0] * d
        e[i] = p
        basis.append(e)
    for j in range(s, d):
        e = [0] * d
        e[j] = 1
        for i in range(s):
            e[i] = (-A[i][j]) % p
        basis.append(e)
    return basis


def trace_gram(q):
    """Tr(zeta^{i-j}) on the power basis 1..zeta^{q-2}: q*I - 1."""
    d = q - 1
    return [[(q - 1 if i == j else -1) for j in range(d)] for i in range(d)]


def tracenorm(x, q):
    s = sum(x)
    return q * sum(v * v for v in x) - s * s


# ------------------------------------------------------------ van Wamelen selection
def vw_lift(x, q, p):
    """degree-<q lift I of x with I(1) = p-2, or None if not integral."""
    s = sum(x)
    num = (p - 2) - s
    if num % q:
        return None
    c = num // q
    # I = x + c * (1 + X + ... + X^{q-1})  (Phi_q), as length-q vector
    return [xi + c for xi in x] + [c]


def vw_select(x, p, q):
    """Return the unique root-of-unity twist of x that is the Jacobi sum (van Wamelen)."""
    found = []
    for sign in (1, -1):
        for k in range(q):
            y = times_root(x, k, sign, q)
            I = vw_lift(y, q, p)
            if I is None:
                continue
            if sum(i * a for i, a in enumerate(I)) % q == 0:
                found.append(y)
    if len(found) != 1:
        raise ArithmeticError('van Wamelen selection not unique: %d' % len(found))
    return found[0]


# ------------------------------------------------------------ reconstruction
class JacobiContext:
    """Per-(p, q) context: eta, Gram matrix, counters. Reconstructs and caches J(u, v)."""

    def __init__(self, p, q, eta=None, method='flint'):
        if q < 5 or (p - 1) % q:
            raise ValueError('need a prime q >= 5 dividing p-1')
        self.method = method
        self.p, self.q, self.K = p, q, (p - 1) // q
        self.eta, self.eta_seed = (eta, None) if eta else element_of_order(p, q)
        self.cache = {}
        self.stats = dict(svp=0, enumeration_fallbacks=0, galois_hits=0, lll_seconds=0.0)

    def _svp(self, S, method='flint'):
        """A vector of trace norm (q-1)p in the ideal lattice prod_{t in S} p_t.

        'flint': LLL (FLINT fmpz_lll, delta 0.99) on the integral embedding
                 E(x) = q*(x,0) - (sum x)*1 in Z^q, for which |E(x)|^2 = q Tr(x xbar).
        Fallback (either method): exact Fincke-Pohst enumeration at the known minimum
        (PARI qfminim on the integral Gram matrix of the LLL-reduced basis).
        """
        from time import perf_counter
        p, q = self.p, self.q
        d = q - 1
        B = ideal_basis(p, q, self.eta, S)
        target = d * p
        t0 = perf_counter()
        if method == 'flint':
            import flint
            rows = []                          # E(b) = q*(b,0) - sum(b)*1
            for b in B:
                s = sum(b)
                rows.append([q * v - s for v in b] + [-s])
            M = flint.fmpz_mat(rows)
            R = M.lll(delta=0.99)
            self.stats['lll_seconds'] += perf_counter() - t0
            red = []
            for i in range(R.nrows()):
                row = [int(R[i, j]) for j in range(q)]
                s = -row[q - 1]
                x = [(row[j] + s) // q for j in range(d)]
                if sum(v * v for v in row) == q * target:
                    return x
                red.append(x)
        else:
            P = _pari()
            Bm = P.matrix(d, d, [B[j][i] for i in range(d) for j in range(d)])
            T = P.matrix(d, d, [x for row in trace_gram(q) for x in row])
            U = P.qflllgram(Bm.mattranspose() * T * Bm)
            self.stats['lll_seconds'] += perf_counter() - t0
            Rm = Bm * U
            red = [[int(Rm[i, j]) for i in range(d)] for j in range(d)]
            for x in red:
                if tracenorm(x, q) == target:
                    return x
        self.stats['enumeration_fallbacks'] += 1
        P = _pari()
        Bm = P.matrix(d, d, [red[j][i] for i in range(d) for j in range(d)])
        T = P.matrix(d, d, [x for row in trace_gram(q) for x in row])
        res = P.qfminim(Bm.mattranspose() * T * Bm, target, 4 * q)   # exact enumeration
        V = res[2]
        for j in range(int(P.matsize(V)[1])):
            col = [int(V[i, j]) for i in range(d)]
            x = [sum(red[k][i] * col[k] for k in range(d)) for i in range(d)]
            if tracenorm(x, q) == target:
                return x
        raise ArithmeticError('no minimal vector found')

    def J(self, u, v):
        """Certified J(chi^u, chi^v) as a power-basis vector; 1<=u,v, u+v<q."""
        p, q = self.p, self.q
        if not (1 <= u and 1 <= v and u + v < q):
            raise ValueError('need 1 <= u, v and u + v < q')
        key = (min(u, v), max(u, v))
        if key in self.cache:
            return self.cache[key]
        # Galois: J(chi^{tu}, chi^{tv}) = sigma_t J(chi^u, chi^v); try a cached base pair
        for (a, b), Jab in list(self.cache.items()):
            for (x, y) in ((a, b), (b, a)):
                # find t with t x = u and t y = v (mod q), and t x, t y residues summing < q
                t = u * pow(x, -1, q) % q
                if (t * y) % q == v:
                    Jt = galois(Jab, t, q)
                    self.stats['galois_hits'] += 1
                    self.cache[key] = Jt
                    return Jt
        S = stickelberger_set(q, u, v)
        x = self._svp(S, self.method)
        self.stats['svp'] += 1
        if mul(x, conj(x, q), q) != [p] + [0] * (q - 2):
            raise ArithmeticError('certificate x*xbar = p failed')
        Jx = vw_select(x, p, q)
        self.cache[key] = Jx
        return Jx

    def rho(self, u, v):
        return evaluate(self.J(u, v), self.eta, self.p)
