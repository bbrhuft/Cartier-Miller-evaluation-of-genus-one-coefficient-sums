"""cmbench.bgs07 -- a transparent implementation of the Bostan-Gaudry-Schost (2007) block-product
algorithm for P(N) = A(N) A(N-1) ... A(1), A(X) = A0 + A1 X an n x n matrix over F_p.

Written 20 October 2026 for this package (not a published kernel).  It follows the structure of
BGS (2007), Theorem 5 (shifting evaluation values), Theorem 8 (dyadic doubling of the values of
M_d(X) = A(X+d) ... A(X+1) on an arithmetic progression with step k) and Theorem 14/(5)
(block assembly), with a simple tail treatment documented below.  Polynomial products use
FLINT nmod_poly multiplication through python-flint; pointwise arithmetic uses numpy with an
exact float-quotient mulmod that is valid for p < 2^50.

Algorithm (k = 2^s, s = floor(log_4 N), so k^2 <= N < 4 k^2):
  1. V_1[j] = A(jk + 1), j = 0, 1                                    (M_1(X) = A(X+1))
  2. for d = 1, 2, 4, ..., k/2: from V_d[j] = M_d(jk), j = 0..d, compute
        S1 = M_d(jk),     j = d+1 .. 2d+1   (shift by alpha = (d+1)k)
        S2 = M_d(jk + d), j = 0 .. d        (shift by alpha = d)
        S3 = M_d(jk + d), j = d+1 .. 2d+1   (shift by alpha = d + (d+1)k)
     and V_{2d}[j] = M_d(jk + d) M_d(jk), j = 0..2d.   [M_{2d}(X) = M_d(X+d) M_d(X)]
  3. extend V_k to j = 0 .. m-1, m = floor(N/k) <= 4k - 1, by at most three further shifts of
     the degree-k values (alpha = (k+1)k, (2k+2)k, (3k+3)k);
  4. P(N) = [A(N) ... A(mk+1)] M_k((m-1)k) ... M_k(k) M_k(0), the tail (< k factors) naively.
Each shift of a degree-d polynomial known at 0, k, ..., dk to alpha, alpha + k, ..., alpha + dk is
the Lagrange formula of BGS Theorem 5:
     G(a + j) = [prod_{m=0}^{d} (a + j - m)] * sum_i G(i) w_i / (a + j - i),
     a = alpha / k,  w_i = (-1)^(d-i) / (i! (d-i)!),
a middle product of length (d+1) x (2d+1).  Required units, all checked at run time:
k, 1..d, and alpha + t k for -d <= t <= d.  For prime p > 4k + 3 with N < p these hold for every
shift above (proof in REPORT section 6); the code raises ArithmeticError otherwise.
Cost: O(n^2 M(sqrt N) + n^3 sqrt N) field operations, O(n^2 sqrt N) storage.
"""
import numpy as np
import flint

__all__ = ['interval_product', 'BGSUnitError', 'MAX_P']

MAX_P = 1 << 50


class BGSUnitError(ArithmeticError):
    pass


def _mulmod(a, b, p):
    """Exact (a*b) mod p for uint64 arrays with entries < p < 2^50."""
    q = np.floor(a.astype(np.float64) * b.astype(np.float64) / float(p))
    r = (a * b - q.astype(np.uint64) * np.uint64(p)).view(np.int64)
    r = np.where(r < 0, r + p, r)
    r = np.where(r >= p, r - p, r)
    return r.astype(np.uint64)


def _addmod(a, b, p):
    s = a + b
    return np.where(s >= p, s - np.uint64(p), s)


def _batch_inverse(vals, p):
    """Montgomery simultaneous inversion of a Python list of nonzero residues."""
    n = len(vals)
    pref = [1] * (n + 1)
    acc = 1
    for i, v in enumerate(vals):
        if v % p == 0:
            raise BGSUnitError('non-unit in shift: %d' % v)
        pref[i] = acc
        acc = acc * v % p
    inv = pow(acc, -1, p)
    out = [0] * n
    for i in range(n - 1, -1, -1):
        out[i] = inv * pref[i] % p
        inv = inv * vals[i] % p
    return out


class _Shifter:
    """Precomputed data for shifting degree-d values from {0,k,...,dk} to {alpha + jk}."""

    def __init__(self, d, k, alpha, p, fact, ifact):
        if k % p == 0:
            raise BGSUnitError('step k not invertible')
        for i in range(1, d + 1):
            if i % p == 0:
                raise BGSUnitError('1..d not invertible')
        a = alpha * pow(k, -1, p) % p
        # s_t = 1/(a + t - d), t = 0..2d   (units <=> alpha + t'k != 0 mod p for |t'| <= d)
        s = _batch_inverse([(a + t - d) % p for t in range(2 * d + 1)], p)
        self.S = flint.nmod_poly(s, p)
        pre = 1
        for t in range(-d, 1):
            pre = pre * ((a + t) % p) % p
        pref = [0] * (d + 1)
        pref[0] = pre
        for j in range(d):
            pre = pre * ((a + j + 1) % p) % p * s[j] % p
            pref[j + 1] = pre
        self.pref = np.array(pref, dtype=np.uint64)
        w = [((-1) ** (d - i)) * ifact[i] * ifact[d - i] % p for i in range(d + 1)]
        self.w = np.array(w, dtype=np.uint64)
        self.d, self.p = d, p

    def apply(self, vals):
        """vals: uint64 array (d+1,) of G(0..d); returns G(a..a+d)."""
        d, p = self.d, self.p
        q = _mulmod(vals, self.w, p)
        prod = flint.nmod_poly(q.tolist(), p) * self.S
        c = prod.coeffs()
        mid = c[d:2 * d + 1]
        if len(mid) < d + 1:
            mid = mid + [0] * (d + 1 - len(mid))
        return _mulmod(np.array([int(x) for x in mid], dtype=np.uint64), self.pref, p)


def _shift_matrices(V, d, k, alpha, p, fact, ifact):
    """V: uint64 array (d+1, n, n) of M(jk); returns M(alpha + jk), j = 0..d, entrywise."""
    sh = _Shifter(d, k, alpha, p, fact, ifact)
    n = V.shape[1]
    out = np.empty_like(V)
    for r in range(n):
        for c in range(n):
            out[:, r, c] = sh.apply(V[:, r, c])
    return out


def _matmul_batch(X, Y, p):
    """X, Y: (J, n, n) uint64; returns X[j] @ Y[j] mod p for every j."""
    J, n, _ = X.shape
    Z = np.zeros_like(X)
    for r in range(n):
        for c in range(n):
            acc = np.zeros(J, dtype=np.uint64)
            for m in range(n):
                acc = _addmod(acc, _mulmod(X[:, r, m], Y[:, m, c], p), p)
            Z[:, r, c] = acc
    return Z


def _eval_A(A0, A1, x, p):
    return [[(A0[i][j] + A1[i][j] * x) % p for j in range(len(A0))] for i in range(len(A0))]


def _matmul_py(X, Y, p):
    n = len(X)
    return [[sum(X[i][m] * Y[m][j] for m in range(n)) % p for j in range(n)] for i in range(n)]


def interval_product(A0, A1, N, p, stats=None):
    """Return P(N) = A(N) ... A(1) (n x n, Python ints), A(X) = A0 + A1 X over F_p, N < p."""
    if not (7 <= p < MAX_P):
        raise ValueError('bgs07 requires 7 <= p < 2^50 (exact float-quotient mulmod)')
    n = len(A0)
    if N < 256:          # naive below 256 factors: no square-root benefit; avoids tiny-p unit edge cases
        P = [[int(i == j) for j in range(n)] for i in range(n)]
        for t in range(1, N + 1):
            P = _matmul_py(_eval_A(A0, A1, t, p), P, p)
        return P
    s = 0
    while 4 ** (s + 1) <= N:
        s += 1
    k = 1 << s
    if p <= 4 * k + 3:
        raise BGSUnitError('p too small relative to sqrt(N)')
    fact = [1] * (k + 1)
    for i in range(1, k + 1):
        fact[i] = fact[i - 1] * i % p
    ifact = [1] * (k + 1)
    ifact[k] = pow(fact[k], -1, p)
    for i in range(k, 0, -1):
        ifact[i - 1] = ifact[i] * i % p
    V = np.array([_eval_A(A0, A1, 1, p), _eval_A(A0, A1, k + 1, p)], dtype=np.uint64)
    d = 1
    shifts = 0
    while d < k:
        S1 = _shift_matrices(V, d, k, (d + 1) * k, p, fact, ifact)
        S2 = _shift_matrices(V, d, k, d, p, fact, ifact)
        S3 = _shift_matrices(V, d, k, d + (d + 1) * k, p, fact, ifact)
        shifts += 3
        lower = np.concatenate([V, S1])[:2 * d + 1]      # M_d(jk),     j = 0..2d
        upper = np.concatenate([S2, S3])[:2 * d + 1]     # M_d(jk + d), j = 0..2d
        V = _matmul_batch(upper, lower, p)
        d *= 2
    m = N // k
    blocks = [V]
    have = k + 1
    c = 1
    while have < m:
        blocks.append(_shift_matrices(V, k, k, c * (k + 1) * k, p, fact, ifact))
        shifts += 1
        have += k + 1
        c += 1
    Vall = np.concatenate(blocks)[:m]
    P = [[int(i == j) for j in range(n)] for i in range(n)]
    for j in range(m):
        P = _matmul_py([[int(x) for x in row] for row in Vall[j]], P, p)
    for t in range(m * k + 1, N + 1):
        P = _matmul_py(_eval_A(A0, A1, t, p), P, p)
    if stats is not None:
        stats.update({'k': k, 'blocks': m, 'tail': N - m * k, 'shifts': shifts, 'n': n})
    return P
