"""Route 3: precision-two baby-step giant-step evaluation of the W1 coefficient.

Identity used (archived Theorem C / W1, re-checked mod p^2 in audit_checks.py):
    G_p := c_1^p + p c_p = -M beta ( z^{-p} S_n(z) - (z^{-1} - eps) a_n ),
    c_1 = -M beta eps,   S_n(z) = sum_{k=0}^{n} a_k z^{4k},
so  K_p = c_p/(M beta) = (G_p - c_1^p)/(p M beta)  (mod p).
S_n(z) mod p^2 comes from the degree-one recurrence
    A_{k+1} = (2k+1) y A_k,  T_{k+1} = 4(k+1)(T_k + A_k),  y = z^4,
with A_0=1, T_0=0, so that S = T_{n+1} / (4^{n+1} (n+1)!).
Baby-step giant-step: Q(X) = M(X+s-1)...M(X) by a product tree of polynomial
matrices, evaluated at X = 0, s, ..., (m-1)s by a subproduct/remainder tree,
followed by m numeric products and a direct tail.  All arithmetic is over
Z/p^2; the only divisions are by monic polynomials, by the unit
4^{n+1}(n+1)!, and by M beta.  This is an incomplete-sum computation
(a B_n-class method), disclosed as such; it is NOT a Witt extractor that
avoids summation.  Cost O(M(sqrt n) log n) ring operations, O(sqrt n log n)
stored ring elements for the trees.

The same kernel evaluates B_n directly (y=1) and the original U_p(n) through the
archived four-dimensional recurrence; those are the matched baselines.
"""
import math, sys, time
from . import polyzq as PZ
from .padic_lift import Ring, lifted_quarter

# ---------------- lower-triangular matrices of polynomials / numbers -------------

def lt_keys(d):
    return [(i, j) for i in range(d) for j in range(i + 1)]


def lt_mul_poly(A, B, d, q):
    C = {}
    for (i, j) in lt_keys(d):
        acc = []
        for k in range(j, i + 1):
            a, b = A.get((i, k)), B.get((k, j))
            if a and b:
                acc = PZ.add(acc, PZ.mul(a, b, q), q)
        if acc:
            C[(i, j)] = acc
    return C


def lt_mul_num(A, B, d, q):
    C = {}
    for (i, j) in lt_keys(d):
        acc = 0
        for k in range(j, i + 1):
            acc += A.get((i, k), 0) * B.get((k, j), 0)
        C[(i, j)] = acc % q
    return C


def leaf(coef, j, q):
    """M(X+j) as polynomials in X; coef[(i,j)] = (c0, c1) meaning c0 + c1*k."""
    return {key: [(c0 + c1 * j) % q, c1 % q] if c1 % q else [(c0 + c1 * j) % q]
            for key, (c0, c1) in coef.items()}


def poly_matrix_block(coef, lo, hi, d, q):
    """M(X+hi-1) ... M(X+lo) as polynomial matrix in X."""
    if hi - lo == 1:
        return leaf(coef, lo, q)
    mid = (lo + hi) // 2
    return lt_mul_poly(poly_matrix_block(coef, mid, hi, d, q),
                       poly_matrix_block(coef, lo, mid, d, q), d, q)


def eval_step(coef, k, q):
    return {key: (c0 + c1 * k) % q for key, (c0, c1) in coef.items()}


def product_bsgs(coef, N, d, q, s=None):
    """Numeric product M(N-1)...M(0) over Z/q by baby-step giant-step."""
    if s is None:
        if N <= 64:
            return product_direct(coef, N, d, q)
        s = max(1, math.isqrt(N))
    m = N // s
    Q = poly_matrix_block(coef, 0, s, d, q)
    keys = list(Q.keys())
    xs = [(j * s) % q for j in range(m)]
    vals = PZ.multipoint([Q[kk] for kk in keys], xs, q)
    total = {key: (1 if key[0] == key[1] else 0) for key in lt_keys(d)}
    for j in range(m):
        Mj = {kk: vals[t][j] for t, kk in enumerate(keys)}
        total = lt_mul_num(Mj, total, d, q)
    for k in range(m * s, N):
        total = lt_mul_num(eval_step(coef, k, q), total, d, q)
    return total


def product_direct(coef, N, d, q):
    total = {key: (1 if key[0] == key[1] else 0) for key in lt_keys(d)}
    for k in range(N):
        total = lt_mul_num(eval_step(coef, k, q), total, d, q)
    return total

# ---------------- the specific recurrences --------------------------------------

def coef_S(y, q):
    return {(0, 0): (y % q, 2 * y % q), (1, 0): (4, 4), (1, 1): (4, 4)}


def partial_sum_bsgs(y, N, q, s=None):
    """sum_{k<N} a_k y^k mod q, a_k = C(2k,k)/8^k; requires N < p."""
    P = product_bsgs(coef_S(y, q), N, 2, q, s)
    return P[(1, 0)] * pow(P[(1, 1)], -1, q) % q


def partial_sum_direct(y, N, q):
    """Same quantity by the cleared-denominator loop (one inversion at the end)."""
    A, T, D = 1, 0, 1
    for k in range(N):
        T = 4 * (k + 1) * (T + A) % q
        A = (2 * k + 1) * y * A % q
        D = 4 * (k + 1) * D % q
    return T * pow(D, -1, q) % q


def coef_U(p, q):
    h = (p - 1) // 2
    return {(0, 0): (h + 2, 1), (1, 0): (h + 2, 0), (1, 1): (h + 3, 1),
            (2, 0): (2 * (h + 1), 2 * (h + 1)), (2, 1): (2, 2), (2, 2): (2, 2),
            (3, 3): (2, 2)}


def U_bsgs(p, L, s=None):
    q = p * p
    P = product_bsgs(coef_U(p, q), L, 4, q, s)
    V = [(P.get((i, 0), 0) + P.get((i, 3), 0)) % q for i in range(4)]  # V_0 = (1,0,0,1)
    return V[2] * pow(V[3], -1, q) % q


def U_direct(p, L):
    q = p * p; h = (p - 1) // 2
    a, b, c, d = 1, 0, 0, 1
    for i in range(L):
        a, b, c, d = ((i + h + 2) * a % q,
                      ((h + 2) * a + (i + h + 3) * b) % q,
                      (2 * (h + 1) * (i + 1) * a + 2 * (i + 1) * b + 2 * (i + 1) * c) % q,
                      2 * (i + 1) * d % q)
    return c * pow(d, -1, q) % q

# ---------------- Witt coefficient from the W1 coefficient -----------------------

def kpow(k, x, e):
    r = k.e(1)
    for bit in bin(e)[2:]:
        r = k.mul(r, r)
        if bit == '1':
            r = k.mul(r, x)
    return r


def K_from_S(p, z, S):
    """K_p and predicted B_n mod p^2 from setup z and S = S_n(z) mod p^2."""
    q = p * p; k = Ring(p)
    assert z['w'][1] == 0
    zz = z['w'][0]; eps = z['e']; an = z['boundary']
    Mb = k.scale(z['M'], z['v'])
    zinv = pow(zz, -1, q)
    inner = (pow(zinv, p, q) * S - (zinv - eps) * an) % q
    G = k.neg(k.scale(inner, Mb))
    c1 = k.neg(k.scale(eps, Mb))
    num = k.sub(G, kpow(k, c1, p))
    assert num[0] % p == 0 and num[1] % p == 0, 'W1 numerator not divisible by p'
    cp = ((num[0] // p) % p, (num[1] // p) % p)
    kp = Ring(p); kp.q = p
    if kp.root is not None:
        kp.root %= p
    K = kp.div(cp, (Mb[0] % p, Mb[1] % p))
    assert K[1] == 0, 'K_p failed base-field descent'
    K = K[0]
    # W2 reconstruction: B_n = Gamma - p(K + 2 d (b + a))
    d = ((zz - 1) // p) % p
    b = eps * (z['chi'] - an) % p          # archived modulo-p theorem (E0)
    pw = kpow(k, Mb, p - 1); assert pw[1] == 0
    Gam = (pw[0] * pow(eps, p, q) - eps * an) % q
    Bpred = (Gam - p * (K + 2 * d * (b + an))) % q
    return K, Bpred


def K_route3(p, z=None, method='bsgs', s=None):
    if z is None:
        z = lifted_quarter(p)
    q = p * p; n = z['L']; y = pow(z['w'][0], 4, q)
    S = partial_sum_bsgs(y, n + 1, q, s) if method == 'bsgs' else partial_sum_direct(y, n + 1, q)
    return K_from_S(p, z, S)


def K_reverse(p, z, B):
    """Reverse identity (R): the correctness control, given B_n mod p^2."""
    q = p * p; k = Ring(p)
    eps = z['e']; an = z['boundary']; zz = z['w'][0]
    Mb = k.scale(z['M'], z['v'])
    pw = kpow(k, Mb, p - 1)
    Gam = (pw[0] * pow(eps, p, q) - eps * an) % q
    d = ((zz - 1) // p) % p; b = B % p
    assert (Gam - B) % p == 0
    return ((Gam - B) % q // p - 2 * d * (b + an)) % p


if __name__ == '__main__':
    p = int(sys.argv[1])
    z = lifted_quarter(p)
    K, Bp = K_route3(p, z)
    print(dict(p=p, K_p=K, predicted_B=Bp, backend=PZ.BACKEND))
