"""Standard-library derivation of the depth-three family below the B=0 seed.

Exact arithmetic in Z[s]/(s^4-2), basis (1, s, s^2, s^3), e = s^2 = sqrt(2).
Recomputes from the seed (-r^2, 0) and the retained normalized quotient
(A',B') = (-4A-15q^2, -8Aq-22q^3):
  * kernel roots, alpha(s), gamma(s), the beta/(rH) multiplier, reverse roots;
  * the minimal polynomial of j over Q, compared with PARI polclass(-256)
    (coefficients pasted from PARI; recomputed independently here);
  * exact integer norms, discriminant, lower-depth and cross-family
    collision evaluations and resultants, fully factored, with every prime
    factor classified as eligible (p = x^2 + 64 y^2) or not;
  * the retained p=73/89/113/233 audit rows whose seed is B=0.
Writes b0_family_constants.json next to this script.
"""
from __future__ import annotations
import csv
import hashlib
import json
import platform
import random
import sys
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ONE = (1, 0, 0, 0)
ZERO = (0, 0, 0, 0)


# ---------------- Z[s]/(s^4-2) ----------------
def mul(x, y):
    c = [0]*7
    for i in range(4):
        for j in range(4):
            c[i+j] += x[i]*y[j]
    return (c[0]+2*c[4], c[1]+2*c[5], c[2]+2*c[6], c[3])


def add(*xs):
    return tuple(sum(v) for v in zip(*xs))


def sc(k, x):
    return tuple(k*v for v in x)


def pw(x, n):
    out = ONE
    for _ in range(n):
        out = mul(out, x)
    return out


def quotient(A, B, q):
    return add(sc(-4, A), sc(-15, mul(q, q))), add(sc(-8, mul(A, q)), sc(-22, pw(q, 3)))


def is_root(A, B, q):
    return add(pw(q, 3), mul(A, q), B) == ZERO


def mult_matrix(x):
    """Columns are x*s^k in the basis (1,s,s^2,s^3)."""
    cols = []
    v = x
    for _ in range(4):
        cols.append(v)
        v = mul(v, (0, 1, 0, 0))
    return [[cols[k][i] for k in range(4)] for i in range(4)]


def det(M):
    """Exact determinant by fraction-free Bareiss elimination."""
    M = [list(r) for r in M]
    n = len(M); sign = 1; prev = 1
    for k in range(n-1):
        if M[k][k] == 0:
            sw = next((i for i in range(k+1, n) if M[i][k]), None)
            if sw is None:
                return 0
            M[k], M[sw] = M[sw], M[k]; sign = -sign
        for i in range(k+1, n):
            for j in range(k+1, n):
                M[i][j] = (M[i][j]*M[k][k]-M[i][k]*M[k][j])//prev
        prev = M[k][k]
    return sign*M[-1][-1]


def norm(x):
    return det(mult_matrix(x))


# ---------------- integer polynomials ----------------
def peval(a, v):
    out = 0
    for c in reversed(a):
        out = out*v+c
    return out


def resultant(a, b):
    m, n = len(a)-1, len(b)-1
    size = m+n; rows = []
    ah, bh = a[::-1], b[::-1]
    for i in range(n):
        rows.append([0]*i+ah+[0]*(size-m-1-i))
    for i in range(m):
        rows.append([0]*i+bh+[0]*(size-n-1-i))
    return det(rows)


def interpolate(xs, ys):
    """Exact Lagrange interpolation; returns low-to-high Fraction coefficients."""
    n = len(xs); coeffs = [Fraction(0)]*n
    for i in range(n):
        basis = [Fraction(1)]; denom = Fraction(1)
        for j in range(n):
            if j != i:
                basis = [Fraction(0)]+basis
                for k in range(len(basis)-1):
                    basis[k] -= xs[j]*basis[k+1]
                denom *= xs[i]-xs[j]
        for k in range(n):
            coeffs[k] += ys[i]*basis[k]/denom
    return coeffs


# ---------------- factorization ----------------
def is_probable_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        if n % q == 0:
            return n == q
    d, s = n-1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71):
        x = pow(a, d, n)
        if x in (1, n-1):
            continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1:
                break
        else:
            return False
    return True


def pollard_brent(n, rng):
    if n % 2 == 0:
        return 2
    while True:
        y, c, m = rng.randrange(1, n), rng.randrange(1, n), 128
        g, r, q = 1, 1, 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (y*y+c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r-k)):
                    y = (y*y+c) % n
                    q = q*abs(x-y) % n
                g = gcd(q, n); k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys*ys+c) % n
                g = gcd(abs(x-ys), n)
        if g != n:
            return g


def factor(v):
    """Complete factorization: trial division to 10^5, then Pollard-Brent;
    prime factors are certified by 20-base Miller-Rabin (deterministic
    below 3.3e24, strong probable prime above; recorded)."""
    v = abs(v); out = {}
    q = 2
    while q < 100000 and q*q <= v:
        while v % q == 0:
            out[q] = out.get(q, 0)+1; v //= q
        q += 1 if q == 2 else 2
    rng = random.Random(20261012)
    stack = [v] if v > 1 else []
    while stack:
        n = stack.pop()
        if is_probable_prime(n):
            out[n] = out.get(n, 0)+1
            continue
        d = pollard_brent(n, rng)
        stack += [d, n//d]
    return dict(sorted(out.items()))


def eligible(q):
    return q >= 7 and q % 8 == 1 and pow(2, (q-1)//4, q) == 1


def main():
    # ---- the chain ----
    A0, B0 = (-1, 0, 0, 0), ZERO          # seed (-r^2, 0) with r = 1
    q0 = ONE
    assert is_root(A0, B0, q0)
    A1, B1 = quotient(A0, B0, q0)
    assert (A1, B1) == ((-11, 0, 0, 0), (-14, 0, 0, 0))
    q1 = (1, 0, 2, 0)                      # (1+2e) r, e = s^2
    assert is_root(A1, B1, q1)
    A2, B2 = quotient(A1, B1, q1)
    assert (A2, B2) == ((-91, 0, -60, 0), (-462, 0, -308, 0))   # retained depth-two family
    F1p = add(A1, sc(3, mul(q1, q1)))
    assert F1p == (16, 0, 12, 0)           # 4(4+3e) r^2 = 4 e (1+e)^2 r^2
    root_of_F1p = (0, 2, 0, 2)             # 2(1+e) s
    assert mul(root_of_F1p, root_of_F1p) == F1p
    q2 = add(q1, sc(2, root_of_F1p))
    assert q2 == (1, 4, 2, 4) and is_root(A2, B2, q2)
    # nondual: q1 != -2 q0, q2 != -2 q1, the two third roots distinct
    nondual_norms = {'q1_plus_2q0': norm(add(q1, sc(2, q0))), 'q2_plus_2q1': norm(add(q2, sc(2, q1))),
                     'third_root_difference_4(1+e)s': norm(sc(2, root_of_F1p))}
    alpha, gamma = quotient(A2, B2, q2)
    mult = add(sc(2, add(sc(2, sc(-1, q0)), sc(-1, q1))), sc(-1, q2))
    rev = [sc(-2, q2), sc(-8, q1), sc(-32, q0)]
    model = (alpha, gamma)
    for q in rev:
        assert is_root(*model, q)
        model = quotient(*model, q)
    assert model == ((-4096, 0, 0, 0), ZERO)   # (-(64 r)^2, 0)
    assert add(sc(4, rev[0]), sc(2, rev[1]), rev[2]) == sc(8, mult)
    a3, g2 = pw(alpha, 3), pw(gamma, 2)
    Delta = add(sc(4, a3), sc(27, g2))
    # ---- class polynomial: det(J M_Delta - M_{6912 a^3}) / N(Delta) ----
    MD, MA = mult_matrix(Delta), mult_matrix(sc(6912, a3))
    xs = list(range(5))
    ys = [det([[J*MD[i][k]-MA[i][k] for k in range(4)] for i in range(4)]) for J in xs]
    poly = interpolate(xs, ys)
    ND = norm(Delta)
    assert poly[-1] == ND
    H = [c/ND for c in poly]
    assert all(c.denominator == 1 for c in H)
    H = [int(c) for c in H]
    pari_polclass_256 = [-1064410681181869521037208505239142408, 26925623396663008311375890966784,
                         -1826592673506207200904172752, -6761166974781862161312, 1]
    assert H == pari_polclass_256, 'minimal polynomial of j differs from polclass(-256)'
    P2 = [-7367066619912, -82226316240, 1]
    P3 = [6549518250000, -2835810000, 1]
    H192 = [-1080060886113159937649308593750000, 826335556188178615474500000000,
            15705521635909735050750000, -8041801037378436000, 1]
    dH = [i*H[i] for i in range(1, 5)]
    quantities = {
        'norm_alpha': norm(alpha), 'norm_gamma': norm(gamma), 'norm_discriminant': ND,
        'disc_H256_via_resultant_with_derivative': resultant(H, dH),
        'H256_at_0': peval(H, 0), 'H256_at_1728': peval(H, 1728), 'H256_at_287496': peval(H, 287496),
        'H256_at_54000': peval(H, 54000),
        'resultant_H256_P2': resultant(H, P2), 'resultant_H256_P3': resultant(H, P3),
        'resultant_H256_H192': resultant(H, H192),
    }
    quantities.update({'norm_'+k: v for k, v in nondual_norms.items()})
    factorizations = {k: factor(v) for k, v in quantities.items()}
    for k, v in quantities.items():
        prod = 1
        for q, e in factorizations[k].items():
            prod *= q**e
        assert prod == abs(v), k
    eligible_factors = {k: [q for q in f if eligible(q)] for k, f in factorizations.items()}
    large_prime_factors = {k: [q for q in f if q > 3*10**24] for k, f in factorizations.items()}
    assert all(not v for v in eligible_factors.values()), eligible_factors
    # ---- audit rows with B=0 seed ----
    rows_checked = []
    with (ROOT/'fixtures/depth_three_four_certificates_20261006.csv').open() as handle:
        for row in csv.DictReader(handle):
            seed = json.loads(row['seed'])
            if int(row['depth']) != 3 or seed[1] != 0:
                continue
            p = int(row['p']); A, B = json.loads(row['target']); fr = json.loads(row['forward_roots'])
            r = fr[0]
            assert (-r*r - seed[0]) % p == 0
            sols = []
            for s in range(p):
                if (pow(s, 4, p)-2) % p:
                    continue
                ev = lambda t: (t[0]+t[1]*s+t[2]*s*s+t[3]*s**3) % p
                if [ev(q0)*r % p, ev(q1)*r % p, ev(q2)*r % p] == fr:
                    assert (ev(alpha)*r*r % p, ev(gamma)*r**3 % p) == (A, B)
                    assert ev(mult)*r % p == int(row['inverse_beta_multiplier'])
                    assert [ev(q)*r % p for q in rev] == json.loads(row['inverse_roots'])
                    sols.append(s)
            assert len(sols) == 1, (row, sols)
            rows_checked.append({'p': p, 'target': [A, B], 'r': r, 's': sols[0], 'multiplier': int(row['inverse_beta_multiplier'])})
    assert len(rows_checked) == 32
    result = {
        'status': 'passed', 'basis': '(1, s, s^2, s^3) with s^4 = 2, e = s^2',
        'seed': '(-r^2, 0)', 'kernel_roots_over_r': [list(q0), list(q1), list(q2)],
        'alpha': list(alpha), 'gamma': list(gamma), 'beta_multiplier_over_r': list(mult),
        'reverse_roots_over_r': [list(q) for q in rev], 'reverse_endpoint': '(-(64 r)^2, 0)',
        'alpha_cubed': list(a3), 'gamma_squared': list(g2), 'discriminant': list(Delta),
        'class_polynomial_low_to_high': H, 'equals_pari_polclass_-256': True,
        'quantities': {k: str(v) for k, v in quantities.items()},
        'factorizations': {k: {str(q): e for q, e in f.items()} for k, f in factorizations.items()},
        'eligible_prime_factors': eligible_factors,
        'eligibility_definition': 'q >= 7, q = 1 mod 8 and 2^((q-1)/4) = 1 mod q (equivalently q = x^2 + 64 y^2)',
        'probable_prime_factors_above_3.3e24': {k: [str(q) for q in v] for k, v in large_prime_factors.items() if v},
        'audit_rows_with_B0_seed_matched': rows_checked,
        'environment': {'python': sys.version, 'platform': platform.platform()},
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE/'b0_family_constants.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'alpha', 'gamma', 'beta_multiplier_over_r', 'reverse_roots_over_r',
                                             'eligible_prime_factors', 'probable_prime_factors_above_3.3e24')}, indent=1))
    for k, f in factorizations.items():
        print(k, ' * '.join(f'{q}^{e}' if e > 1 else str(q) for q, e in f.items()))


if __name__ == '__main__':
    main()
