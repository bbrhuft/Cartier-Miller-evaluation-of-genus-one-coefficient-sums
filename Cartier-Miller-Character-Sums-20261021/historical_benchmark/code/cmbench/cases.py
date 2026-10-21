"""cmbench.cases -- deterministic case generation (primes, curves, poles) and the common-domain
multi-pole adapter shared by every scalar method.

Selection rules are pure functions of (seed, label); see REPORT section 8 for the recorded seeds.
"""
import hashlib
import random

from . import core

# primes used by the inherited archive's development/confirmation runs and the handover verifier;
# excluded from this package's confirmation and benchmark selections (REPORT section 8).
INHERITED_PRIMES = set(
    [q for q in range(7, 200) if core.is_prime_small(q)]
    + [211, 4999, 10007, 100003, 1000003, 2 ** 61 - 1, 10 ** 18 + 9]
    + [227, 239, 251, 263, 271, 281, 311, 347, 367, 419, 433, 491, 521, 541, 547, 569, 607, 2647,
       2689, 2857, 3389, 4139, 4519, 4967, 911087, 728681, 5314391, 717754976387, 952110247849697,
       661479507218101589, 8984630942399791949, 101])


def rng_for(seed, label):
    h = hashlib.sha256(('%s|%s' % (seed, label)).encode()).digest()
    return random.Random(int.from_bytes(h[:16], 'big'))


def random_prime(rng, lo, hi, exclude=()):
    while True:
        q = rng.randrange(lo, hi) | 1
        if q >= 7 and q not in exclude and core.is_prime_small(q):
            return q


def random_curve(rng, p, d, kind='generic'):
    """Squarefree exact-degree d polynomial.  kind: generic | zero_const | unit_const |
    lead_square | lead_nonsquare (quartics)."""
    while True:
        f = [rng.randrange(p) for _ in range(d)] + [rng.randrange(1, p)]
        if kind == 'zero_const':
            f[0] = 0
        elif kind == 'unit_const':
            f[0] = 1
        elif kind in ('lead_square', 'lead_nonsquare') and d == 4:
            want = 1 if kind == 'lead_square' else -1
            if core.legendre(f[-1], p) != want:
                continue
        if core.squarefree(f, p):
            return f


def random_pole(rng, p, f, allow_branch=False, prefer_zero=False):
    if prefer_zero and (allow_branch or core.peval(f, 0, p)):
        return 0
    while True:
        a = rng.randrange(p)
        if allow_branch or core.peval(f, a, p):
            return a


# ---------------------------------------------------------------- CM construction of trace +-1 curves
CM_DATA = [  # (D, j), class number one, D = 5 mod 8 (D = 1 mod 8, e.g. -7, forces an even trace)
    (-3, 0), (-11, -32768), (-19, -884736), (-43, -884736000),
    (-67, -147197952000), (-163, -262537412640768000)]


def cm_trace_pm1_curve(rng, bits, D, j, want_trace, pari):
    """Prime p = (1 + |D| v^2)/4 of about `bits` bits and a short cubic of trace want_trace (+-1)
    with CM by the order of discriminant D.  Uses PARI ellap only to select the twist."""
    if D % 8 != 5:
        raise ValueError('need D = 5 mod 8 for an odd trace')
    from math import isqrt
    lo = max(3, isqrt((4 << (bits - 1)) // (-D)))
    hi = max(lo + 4, isqrt((4 << bits) // (-D)))
    while True:
        v = rng.randrange(lo, hi) | 1
        p = (1 + (-D) * v * v) // 4
        if p < 1000 or p >= 1 << 64 or not core.is_prime_small(p):
            continue
        if j == 0:
            twists = [[b, 0, 0, 1] for b in range(1, 50)]
        else:
            k = j * pow((1728 - j) % p, -1, p) % p
            twists = []
            for c in range(1, 50):
                twists.append([2 * k * c ** 3 % p, 3 * k * c * c % p, 0, 1])
        for f in twists:
            if not core.squarefree(f, p):
                continue
            E = pari.ellinit([0, 0, 0, f[1], f[0]], p)
            if int(pari.ellap(E)) == want_trace:
                return p, f


def scramble_cubic(rng, p, f):
    """x -> alpha x + beta and multiplication by a nonzero square: same trace, generic coefficients."""
    alpha = rng.randrange(1, p)
    beta = rng.randrange(p)
    u = pow(rng.randrange(1, p), 2, p)
    g = core.taylor_shift(f, beta, p)                       # f(beta + z)
    g = [c * pow(alpha, i, p) % p for i, c in enumerate(g)]  # f(beta + alpha z)
    return [c * u % p for c in g]


def cubic_to_quartic(rng, p, c):
    """y^2 = c(x) -> y^2 = q(u) = (gamma u + delta)^4 c((alpha u + beta)/(gamma u + delta)),
    an isomorphic genus-one model (same trace) with a genuine quartic."""
    while True:
        al, be, ga, de = (rng.randrange(p) for _ in range(4))
        if (al * de - be * ga) % p == 0 or ga == 0:
            continue
        if core.peval(c, al * pow(ga, -1, p) % p, p) == 0:
            continue
        # q(u) = sum_i c_i (al u + be)^i (ga u + de)^(4-i)
        q = [0] * 5
        for i, ci in enumerate(c):
            A = [1]
            for _ in range(i):
                A = _pmul(A, [be, al], p)
            B = [1]
            for _ in range(4 - i):
                B = _pmul(B, [de, ga], p)
            for k, t in enumerate(_pmul(A, B, p)):
                q[k] = (q[k] + ci * t) % p
        if q[4] and core.squarefree(q, p):
            return q


def _pmul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = (r[i + j] + x * y) % p
    return r


# ---------------------------------------------------------------- common-domain multi-pole adapter
def sum_eps_from_H(p, f, H):
    """sum_{x in F_p} chi(f(x)) mod p from H = c_{p-1} (Lemma 1: -c_{p-1} - c_{2p-2})."""
    s = -H
    if len(f) == 5:
        s -= core.legendre(f[-1], p)
    return s % p


def weighted_from_scalars(single, eps_at, poles, weights, b, sum_eps, p):
    """sum_{x notin U} chi(f(x)) (b + sum_j v_j/(x - a_j)),  U = {a_j} (zero v_j allowed).

    single[a] = C_f(a) (full-field single-pole value), eps_at[a] = chi(f(a)), sum_eps = residue of
    sum_x chi(f(x)).  Exact O(s^2) correction (corrected Theorem A2):
        sum_j v_j C_f(a_j) - sum_k eps(a_k) r_k + b (sum_eps - sum_k eps(a_k)),
        r_k = sum_{j != k} v_j / (a_k - a_j).
    Also returns the affine-point version (adds sum_{x notin U} R(x) = -sum r_k - b s)."""
    s = len(poles)
    if len(set(poles)) != s:
        raise ValueError('poles must be distinct')
    r = []
    for k, ak in enumerate(poles):
        diffs = [(ak - aj) % p for j, aj in enumerate(poles) if j != k]
        acc = 0
        if diffs:
            inv = _batch_inv(diffs, p)
            idx = 0
            for j in range(s):
                if j != k:
                    acc += weights[j] * inv[idx]
                    idx += 1
        r.append(acc % p)
    char = sum(v * single[a] for a, v in zip(poles, weights))
    char -= sum(eps_at[a] * rk for a, rk in zip(poles, r))
    char += b * (sum_eps - sum(eps_at[a] for a in poles))
    char %= p
    affine = (char - sum(r) - b * s + b * p) % p
    return char, affine


def _batch_inv(vals, p):
    n = len(vals)
    pref, acc = [0] * n, 1
    for i, v in enumerate(vals):
        pref[i] = acc
        acc = acc * v % p
    inv = pow(acc, -1, p)
    out = [0] * n
    for i in range(n - 1, -1, -1):
        out[i] = inv * pref[i] % p
        inv = inv * vals[i] % p
    return out
