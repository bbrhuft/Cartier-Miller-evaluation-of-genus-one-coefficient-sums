"""Standard-library reproduction of the depth-three family's exact integer data.

Arithmetic is in Z[e,g]/(e^2-3, g^2-2) with elements stored as integer
4-tuples in the basis (1, e, g, eg). Everything is recomputed from the seed
and the quotient formula; nothing is imported from the sympy derivation.
Outputs theory/integer_invariants_depth3.json. Complete factorizations are
certified by trial division with an explicit cofactor-equals-one assertion.
"""
from __future__ import annotations
import hashlib
import json
import platform
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ONE = (1, 0, 0, 0)
E = (0, 1, 0, 0)
G = (0, 0, 1, 0)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def neg(x):
    return tuple(-a for a in x)


def scale(k, x):
    return tuple(k * a for a in x)


def mul(x, y):
    """(x0 + x1 e + x2 g + x3 eg)(y0 + ...) with e^2=3, g^2=2."""
    x0, x1, x2, x3 = x
    y0, y1, y2, y3 = y
    return (x0*y0 + 3*x1*y1 + 2*x2*y2 + 6*x3*y3,
            x0*y1 + x1*y0 + 2*x2*y3 + 2*x3*y2,
            x0*y2 + x2*y0 + 3*x1*y3 + 3*x3*y1,
            x0*y3 + x3*y0 + x1*y2 + x2*y1)


def power(x, n):
    out = ONE
    for _ in range(n):
        out = mul(out, x)
    return out


def conj(x, se, sg):
    x0, x1, x2, x3 = x
    return (x0, se*x1, sg*x2, se*sg*x3)


def norm(x):
    out = ONE
    for se in (1, -1):
        for sg in (1, -1):
            out = mul(out, conj(x, se, sg))
    assert out[1:] == (0, 0, 0), out
    return out[0]


def factor(v):
    """Complete trial-division factorization; asserts the cofactor is 1."""
    v = abs(v)
    out = {}
    q = 2
    while q * q <= v and q <= 20000:
        if v % q == 0:
            t = 0
            while v % q == 0:
                v //= q
                t += 1
            out[str(q)] = t
        q += 1 if q == 2 else 2
    if v > 1:
        out[str(v)] = 1
        # Certify the remaining cofactor is prime by trial division.
        assert v <= 20000**2 and all(v % d for d in range(2, int(v**0.5) + 1)), 'incomplete factorization'
    return out


def prime_factors(v):
    return [int(q) for q in factor(v)]


# ---- polynomial helpers over Z (coefficient lists, low to high) ----

def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def peval(a, v):
    out = 0
    for c in reversed(a):
        out = out * v + c
    return out


def bareiss_det(M):
    """Exact integer determinant by fraction-free Gaussian elimination."""
    M = [row[:] for row in M]
    n = len(M)
    sign = 1
    prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if swap is None:
                return 0
            M[k], M[swap] = M[swap], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


def resultant(a, b):
    """Sylvester resultant of integer polynomials (low-to-high lists)."""
    m, n = len(a) - 1, len(b) - 1
    size = m + n
    rows = []
    ah = a[::-1]
    bh = b[::-1]
    for i in range(n):
        rows.append([0] * i + ah + [0] * (size - m - 1 - i))
    for i in range(m):
        rows.append([0] * i + bh + [0] * (size - n - 1 - i))
    return bareiss_det(rows)


def main():
    r = 1  # work with r = 1; homogeneity restores r
    # Seed (0,-1), kernel roots in Z[e,g].
    A0, B0 = (0, 0, 0, 0), neg(ONE)
    q0 = ONE

    def quotient(A, B, q):
        return (add(scale(-4, A), scale(-15, mul(q, q))),
                add(scale(-8, mul(A, q)), scale(-22, power(q, 3))))

    def is_root(A, B, q):
        return add(add(power(q, 3), mul(A, q)), B) == (0, 0, 0, 0)

    assert is_root(A0, B0, q0)
    A1, B1 = quotient(A0, B0, q0)
    assert (A1, B1) == ((-15, 0, 0, 0), (-22, 0, 0, 0))
    q1 = (1, 2, 0, 0)
    assert is_root(A1, B1, q1)
    A2, B2 = quotient(A1, B1, q1)
    assert (A2, B2) == ((-135, -60, 0, 0), (-694, -420, 0, 0))
    # F1'(q1) = A1 + 3 q1^2 and its square root (3g + eg)
    F1p = add(A1, scale(3, mul(q1, q1)))
    s = (0, 0, 3, 1)
    assert mul(s, s) == F1p
    q2 = add(q1, scale(2, s))
    assert q2 == (1, 2, 6, 2)
    assert is_root(A2, B2, q2)
    alpha, gamma = quotient(A2, B2, q2)
    mult = scale(-1, q0)
    mult = add(scale(2, mult), neg(q1))
    mult = add(scale(2, mult), neg(q2))
    assert mult == (-7, -6, -6, -2)
    # Reverse certificate: roots -2 q2, -8 q1, -32 q0 ending at (0, -(64)^3)
    model = (alpha, gamma)
    rev = [scale(-2, q2), scale(-8, q1), scale(-32, q0)]
    for q in rev:
        assert is_root(model[0], model[1], q)
        model = quotient(model[0], model[1], q)
    assert model == ((0, 0, 0, 0), (-64**3, 0, 0, 0))
    rmult = add(add(scale(1, rev[0]), scale(1, rev[1])), scale(1, rev[2]))  # placeholder
    # exact: rev0/2 + rev1/4 + rev2/8 ; multiply by 8 to stay integral
    eight = add(add(scale(4, rev[0]), scale(2, rev[1])), rev[2])
    assert eight == scale(8, mult)
    a3 = power(alpha, 3)
    g2 = power(gamma, 2)
    Delta = add(scale(4, a3), scale(27, g2))
    # Class polynomial: N(Delta) * prod_sigma (J - j_sigma) = prod_sigma (sigma(Delta) J - 6912 sigma(alpha)^3)
    # computed as a polynomial in J with coefficients in Z[e,g].
    poly = [ONE]  # coefficients low-to-high, each a 4-tuple
    for se in (1, -1):
        for sg in (1, -1):
            lin = [scale(-6912, conj(a3, se, sg)), conj(Delta, se, sg)]
            new = [(0, 0, 0, 0)] * (len(poly) + 1)
            for i, c in enumerate(poly):
                for j, d in enumerate(lin):
                    new[i + j] = add(new[i + j], mul(c, d))
            poly = new
    assert all(c[1:] == (0, 0, 0) for c in poly)
    lead = poly[-1][0]
    assert lead == norm(Delta)
    assert all(c[0] % lead == 0 for c in poly)
    HJ = [c[0] // lead for c in poly]  # low to high, monic quartic
    assert HJ[-1] == 1 and len(HJ) == 5
    P2 = [-7367066619912, -82226316240, 1]
    P3 = [6549518250000, -2835810000, 1]
    # Class polynomial of discriminant -256 (the depth-three chain below j=1728),
    # as returned by PARI polclass(-256); its Galois group is D4 (PARI polgalois),
    # so it is absent from Lario's multiquadratic table. Used only to exclude
    # j-collisions between the two depth-three chains at eligible primes.
    H256 = [-1064410681181869521037208505239142408, 26925623396663008311375890966784,
            -1826592673506207200904172752, -6761166974781862161312, 1]
    # Conjugate collision elements.
    coll = {}
    for name, (se, sg) in {'e_to_minus_e': (-1, 1), 'g_to_minus_g': (1, -1), 'both': (-1, -1)}.items():
        C = add(mul(g2, power(conj(alpha, se, sg), 3)), neg(mul(a3, power(conj(gamma, se, sg), 2))))
        coll[name] = {'coords_1_e_g_eg': list(C), 'norm': norm(C), 'factorization': factor(norm(C))}
    dHJ = [i * HJ[i] for i in range(1, len(HJ))]
    disc = resultant(HJ, dHJ)
    quantities = {
        'norm_alpha': norm(alpha), 'norm_gamma': norm(gamma), 'norm_discriminant': norm(Delta),
        'H_at_0': peval(HJ, 0), 'H_at_1728': peval(HJ, 1728), 'H_at_54000': peval(HJ, 54000),
        'H_at_287496': peval(HJ, 287496),
        'resultant_H_P2': resultant(HJ, P2), 'resultant_H_P3': resultant(HJ, P3),
        'resultant_H_H256': resultant(HJ, H256),
        'discriminant_H': disc,
    }
    for k, v in coll.items():
        quantities['norm_collision_' + k] = v['norm']
    # Nondual-step guards: q2 + 2 q1 and the root difference (3+e) g must be nonzero.
    quantities['norm_q2_plus_2q1'] = norm(add(q2, scale(2, q1)))
    quantities['norm_root_difference_(3+e)g'] = norm(s)
    assert quantities['norm_q2_plus_2q1'] == 9 and quantities['norm_root_difference_(3+e)g'] == 144
    factorizations = {k: factor(v) for k, v in quantities.items()}
    offending = {k: [q for q in prime_factors(v) if q >= 7 and q % 24 == 1] for k, v in quantities.items()}
    assert all(not v for v in offending.values()), offending
    # Relative-norm extraction constants: for L = U0 + U1 e + U2 g + U3 eg,
    # L * sigma_g(L) = (U0^2+3U1^2-2U2^2-6U3^2) + 2(U0 U1 - 2 U2 U3) e,
    # L * sigma_e(L) = (U0^2-3U1^2+2U2^2-6U3^2) + 2(U0 U2 - 3 U1 U3) g.
    # Check these on random integer vectors.
    import random
    rng = random.Random(20261007)
    for _ in range(200):
        U = tuple(rng.randrange(-50, 50) for _ in range(4))
        Ng = mul(U, conj(U, 1, -1))
        Ne = mul(U, conj(U, -1, 1))
        U0, U1, U2, U3 = U
        assert Ng == (U0*U0 + 3*U1*U1 - 2*U2*U2 - 6*U3*U3, 2*(U0*U1 - 2*U2*U3), 0, 0)
        assert Ne == (U0*U0 - 3*U1*U1 + 2*U2*U2 - 6*U3*U3, 0, 2*(U0*U2 - 3*U1*U3), 0)
    # Degenerate models at excluded primes (documented, not eligible).
    degenerate = []
    for p in sorted({q for v in quantities.values() for q in prime_factors(v) if q >= 7}):
        if p % 24 == 1:
            continue
        sq3 = [v for v in range(p) if v * v % p == 3]
        sq2 = [v for v in range(p) if v * v % p == 2]
        rows = []
        for e0 in sq3:
            for g0 in sq2:
                ev = lambda t: (t[0] + t[1]*e0 + t[2]*g0 + t[3]*e0*g0) % p
                rows.append({'e': e0, 'g': g0, 'alpha': ev(alpha), 'gamma': ev(gamma), 'Delta': ev(Delta)})
        degenerate.append({'p': p, 'p_mod_24': p % 24, 'sqrt3_exists': bool(sq3), 'sqrt2_exists': bool(sq2),
                           'seed_congruence_p_1_mod_3': p % 3 == 1, 'rational_parameter_models': rows})
    result = {
        'status': 'passed',
        'basis': '(1, e, g, eg) with e^2=3, g^2=2',
        'alpha': list(alpha), 'gamma': list(gamma), 'beta_multiplier_over_r': list(mult),
        'kernel_roots_over_r': [list(q0), list(q1), list(q2)],
        'reverse_roots_over_r': [list(q) for q in rev], 'reverse_endpoint': [[0, 0, 0, 0], [-64**3, 0, 0, 0]],
        'alpha_cubed': list(a3), 'gamma_squared': list(g2), 'discriminant': list(Delta),
        'class_polynomial_low_to_high': HJ,
        'class_polynomial_disc_minus_256_low_to_high_source_pari_polclass': H256,
        'quantities': {k: str(v) for k, v in quantities.items()},
        'factorizations': factorizations,
        'primes_1_mod_24_dividing_any_quantity': offending,
        'conjugate_collision_elements': {k: {'coords_1_e_g_eg': v['coords_1_e_g_eg'], 'norm': str(v['norm']), 'factorization': v['factorization']} for k, v in coll.items()},
        'degenerate_models_at_excluded_primes': degenerate,
        'environment': {'python': sys.version, 'platform': platform.platform()},
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE / 'integer_invariants_depth3.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'alpha', 'gamma', 'beta_multiplier_over_r', 'class_polynomial_low_to_high', 'factorizations', 'primes_1_mod_24_dividing_any_quantity')}, indent=1))


if __name__ == '__main__':
    main()
