"""Symbolic derivation of the depth-three family from the ordinary j=0 seed.

Exact arithmetic in Z[e,g]/(e^2-3, g^2-2) with sympy. Produces:
  * alpha(e,g), gamma(e,g) with (A,B)=(alpha r^2, gamma r^3),
  * the beta/H multiplier,
  * the reverse (target-to-seed) kernel roots,
  * the minimal polynomial of j over Q (compared with the class polynomial
    of discriminant -192 computed independently by PARI when available),
  * exact integer norms needed for the exceptional-prime analysis,
  * the p=73 fixture check.
This is a derivation aid; the standard-library prototype does not import it.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

e, g, r = sp.symbols('e g r')
RED = {e**2: 3, g**2: 2}


def red(expr):
    """Reduce a polynomial in e,g,r modulo e^2=3, g^2=2 (fully expanded)."""
    expr = sp.expand(expr)
    poly = sp.Poly(expr, e, g)
    out = 0
    for (i, j), c in poly.terms():
        out += c * 3**(i // 2) * e**(i % 2) * 2**(j // 2) * g**(j % 2)
    return sp.expand(out)


def coords(expr):
    """Coordinates of a reduced element in the basis (1, e, g, eg)."""
    expr = red(expr)
    poly = sp.Poly(expr, e, g)
    d = {(0, 0): 0, (1, 0): 0, (0, 1): 0, (1, 1): 0}
    for m, c in poly.terms():
        d[m] = c
    return [d[(0, 0)], d[(1, 0)], d[(0, 1)], d[(1, 1)]]


def quotient(A, B, q):
    return red(-4*A - 15*q**2), red(-8*A*q - 22*q**3)


def conj(expr, se, sg):
    return red(expr.subs({e: se*e, g: sg*g}, simultaneous=True))


def norm(expr):
    """Norm from Q(e,g) to Q of a reduced element (product of four conjugates)."""
    prod = 1
    for se in (1, -1):
        for sg in (1, -1):
            prod = red(prod * conj(expr, se, sg))
    assert coords(prod)[1:] == [0, 0, 0], prod
    return sp.Integer(coords(prod)[0])


def main():
    # Seed: (0,-r^3), p = 1 mod 3. Rational root r.
    A0, B0 = sp.Integer(0), -r**3
    assert red(r**3 + A0*r + B0) == 0
    q0 = r
    A1, B1 = quotient(A0, B0, q0)
    assert (A1, B1) == (-15*r**2, -22*r**3)
    # Second kernel: nondual root of x^3+A1 x+B1; q1 = (1+2e) r with e^2=3.
    q1 = red((1 + 2*e)*r)
    assert red(q1**3 + A1*q1 + B1) == 0
    A2, B2 = quotient(A1, B1, q1)
    assert (coords(A2) == [-135*r**2, -60*r**2, 0, 0]) and coords(B2) == [-694*r**3, -420*r**3, 0, 0]
    # Third kernel: nondual root of x^3+A2 x+B2. General fact: cubic has root
    # -2 q1 and the quadratic cofactor x^2-2 q1 x + (A2+4 q1^2) has roots
    # q1 +- 2 sqrt(F1'(q1)), F1'(q1)=A1+3 q1^2.
    F1p = red(A1 + 3*q1**2)
    assert F1p == red(12*(2 + e)*r**2)
    s = red((3*g + e*g)*r)  # candidate square root of F1p
    assert red(s**2 - F1p) == 0
    q2 = red(q1 + 2*s)
    assert coords(q2) == [r, 2*r, 6*r, 2*r]
    assert red(q2**3 + A2*q2 + B2) == 0
    # Also check the cofactor structure explicitly.
    cof = sp.expand((sp.Symbol('x') + 2*q1) * (sp.Symbol('x')**2 - 2*q1*sp.Symbol('x') + (A2 + 4*q1**2)))
    assert red(cof - (sp.Symbol('x')**3 + A2*sp.Symbol('x') + B2)) == 0
    A3, B3 = quotient(A2, B2, q2)
    alpha = sp.Poly(red(A3 / r**2), e, g)
    gamma = sp.Poly(red(B3 / r**3), e, g)
    assert red(A3 - alpha.as_expr()*r**2) == 0 and red(B3 - gamma.as_expr()*r**3) == 0
    alpha_c = coords(alpha.as_expr())
    gamma_c = coords(gamma.as_expr())
    # beta transport: beta' = 2 beta - q H; seed beta = 0.
    m1 = red(-q0)
    m2 = red(2*m1 - q1)
    m3 = red(2*m2 - q2)
    mult = coords(m3 / r)
    # Reverse roots: -2 4^i q_{m-1-i}
    rev = [red(-2*q2), red(-8*q1), red(-32*q0)]
    model = (A3, B3)
    for q in rev:
        assert red(q**3 + model[0]*q + model[1]) == 0
        model = quotient(model[0], model[1], q)
    assert model[0] == 0 and red(model[1] + (64*r)**3) == 0
    rev_mult = red(rev[0]/2 + rev[1]/4 + rev[2]/8)
    assert red(rev_mult - m3) == 0
    # Exact integer data for extraction: alpha^3, gamma^2 coordinates.
    a3 = coords(alpha.as_expr()**3)
    g2 = coords(gamma.as_expr()**2)
    Delta = red(4*alpha.as_expr()**3 + 27*gamma.as_expr()**2)
    # Minimal polynomial of j = 6912 alpha^3 / Delta over Q.
    J = sp.Symbol('J')
    conjs = []
    for se in (1, -1):
        for sg in (1, -1):
            a = conj(alpha.as_expr(), se, sg)
            d = conj(Delta, se, sg)
            conjs.append((a, d))
    # Product over conjugates of (d*J - 6912*a^3) = N(Delta) * prod (J - j_sigma)
    prod = sp.Integer(1)
    for a, d in conjs:
        prod = red(prod * (d*J - 6912*a**3))
    pc = coords(prod)
    assert all(sp.expand(x) == 0 for x in pc[1:])
    PJ = sp.Poly(sp.expand(pc[0]), J)
    lead = PJ.LC()
    assert lead == norm(Delta)
    HJ = sp.Poly(sp.expand(PJ.as_expr() / lead), J)
    assert all(c.is_integer for c in HJ.all_coeffs())
    # Norms for exceptional-prime analysis.
    data = {
        'alpha_coords_1_e_g_eg': [int(x) for x in alpha_c],
        'gamma_coords_1_e_g_eg': [int(x) for x in gamma_c],
        'beta_multiplier_coords_times_r': [int(x) for x in mult],
        'alpha_cubed_coords': [int(x) for x in a3],
        'gamma_squared_coords': [int(x) for x in g2],
        'discriminant_coords': [int(x) for x in coords(Delta)],
        'reverse_roots_over_r': [[int(x) for x in coords(q/r)] for q in rev],
        'reverse_endpoint': '(0, -(64 r)^3)',
        'norm_alpha': int(norm(alpha.as_expr())),
        'norm_gamma': int(norm(gamma.as_expr())),
        'norm_discriminant': int(norm(Delta)),
        'j_min_poly_coeffs_high_to_low': [int(c) for c in HJ.all_coeffs()],
    }
    # Conjugate-collision elements: for each nontrivial automorphism sigma,
    # C_sigma = gamma^2 sigma(alpha)^3 - alpha^3 sigma(gamma)^2.
    coll = {}
    for name, (se, sg) in {'e->-e': (-1, 1), 'g->-g': (1, -1), 'both': (-1, -1)}.items():
        C = red(gamma.as_expr()**2 * conj(alpha.as_expr(), se, sg)**3 - alpha.as_expr()**3 * conj(gamma.as_expr(), se, sg)**2)
        coll[name] = {'coords': [int(x) for x in coords(C)], 'norm': int(norm(C))}
    data['conjugate_collision_elements'] = coll
    # Relative norms used by the recognizer: for a generic element L with
    # coordinates U=(U0,U1,U2,U3), N_{g}(L)=L*sigma_g(L)=P0+P1 e, N_{e}(L)=Q0+Q1 g.
    U0, U1, U2, U3 = sp.symbols('U0 U1 U2 U3')
    L = U0 + U1*e + U2*g + U3*e*g
    Ng = coords(L * conj(L, 1, -1))
    Ne = coords(L * conj(L, -1, 1))
    data['relative_norm_to_Q(e)'] = [str(sp.factor(x)) for x in Ng]
    data['relative_norm_to_Q(g)'] = [str(sp.factor(x)) for x in Ne]
    # p = 73 fixture check.
    p = 73
    e0, g0, r0 = 21, 41, 42
    assert e0*e0 % p == 3 and g0*g0 % p == 2
    sub = {e: e0, g: g0, r: r0}
    A3v = int(A3.subs(sub)) % p
    B3v = int(B3.subs(sub)) % p
    assert (A3v, B3v) == (4, 16), (A3v, B3v)
    assert int(m3.subs(sub)) % p == 15
    assert [int(q.subs(sub)) % p for q in rev] == [71, 6, 43]
    assert [int(q.subs(sub)) % p for q in (q0, q1, q2)] == [42, 54, 1]
    data['p73_fixture'] = {'e': e0, 'g': g0, 'r': r0, 'target': [A3v, B3v], 'beta_multiplier': 15,
                           'forward_roots': [42, 54, 1], 'reverse_roots': [71, 6, 43]}
    # Optional PARI cross-check of the class polynomial.
    try:
        import cypari2
        pari = cypari2.Pari()
        pari.allocatemem(128 * 10**6)
        hc = pari('polclass(-192)')
        hc_coeffs = [int(x) for x in pari('Vecrev(polclass(-192))')][::-1]
        data['pari_polclass_-192_high_to_low'] = hc_coeffs
        data['j_min_poly_equals_polclass_-192'] = hc_coeffs == data['j_min_poly_coeffs_high_to_low']
    except Exception as exc:  # pragma: no cover
        data['pari_polclass_-192_high_to_low'] = None
        data['pari_error'] = repr(exc)
    out = Path(__file__).resolve().parent / 'family_constants.json'
    out.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
