"""Exact characteristic-zero eigenline coefficients c = nu/(mu - lam) from
explicit non-scalar endomorphisms (loops of normalized isogenies), for the two
seeds, the six retained families and the new discriminants -7 and -8.

The loop computation does NOT use the retained characteristic-p slope, the
seed property beta=0, or any transport recurrence. Inputs are only the curve
model, kernel coordinates (each checked to be a root, each quotient checked to
equal the next model) and the closing isomorphism scale u (checked).

Output: c (twist parameter r = 1), S = 2 A c/(3 B) (the weight-zero CM value),
j, comparison with the retained multiplier beta/(rH) = m from
knowledge/EXISTING_FAMILIES.md (expected relation: -c = m).
"""
import json, sys
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/theory/', 1)[0] + '/core')
from qtower import Tower
from isogeny_matrices import matmul, velu2, velu_odd, iso, aut, quotient2, slope_from_matrix

results = {}

def run_path(T, A, B, roots):
    """Follow normalized 2-isogenies; return final model and matrix."""
    M = None
    for q in roots:
        A, B = quotient2(T, A, B, q)
        step = velu2(T, q)
        M = step if M is None else matmul(T, M, step)
    return A, B, M

def same_model_scale(T, A, B, A2, B2, u):
    """Check (A2,B2) = (u^4 A, u^6 B)."""
    u2 = T.mul(u, u); u4 = T.mul(u2, u2); u6 = T.mul(u4, u2)
    return T.eq(A2, T.mul(u4, A)) and T.eq(B2, T.mul(u6, B))

def record(name, T, A, B, M, extra, m_expected=None, D=None, embed=None):
    lam, mu, nu, c, slope = slope_from_matrix(T, M)
    assert not T.is_zero(T.sub(mu, lam)), 'scalar endomorphism: no information'
    rec = {'D': D, 'tower': list(zip(T.names, [T.show(d) for d in T.d])),
           'A': T.show(A), 'B': T.show(B), 'lambda': T.show(lam), 'mu': T.show(mu),
           'nu': T.show(nu), 'c_eigenline': T.show(c), 'slope_beta_over_H_r1': T.show(slope),
           'lambda_minus_mu_squared': T.show(T.mul(T.sub(lam, mu), T.sub(lam, mu)))}
    rec.update(extra)
    if not T.is_zero(A) and not T.is_zero(B):
        S = T.div(T.mul(T.const(2), T.mul(A, c)), T.mul(T.const(3), B))
        rec['S_weight_zero'] = T.show(S)
        A3 = T.pow(A, 3); B2 = T.mul(B, B)
        den = T.add(T.mul(T.const(4), A3), T.mul(T.const(27), B2))
        j = T.div(T.mul(T.const(1728*4), A3), den)
        rec['j'] = T.show(j)
        rec['_S'] = S; rec['_j'] = j
    if m_expected is not None:
        rec['retained_multiplier'] = T.show(m_expected)
        rec['minus_c_equals_retained_multiplier'] = T.eq(T.neg(c), m_expected)
    rec['_T'] = T; rec['_c'] = c; rec['_A'] = A; rec['_B'] = B
    results[name] = rec
    return rec

def vec(T, coeffs, basis):
    s = T.const(0)
    for cf, b in zip(coeffs, basis):
        s = T.add(s, T.mul(T.const(cf), b))
    return s

# ---------------- seeds ----------------
T = Tower(['t'], [Fr(-3)]); t = T.gen(0); z = T.mul(T.const(Fr(1,2)), T.add(T.const(-1), t))
record('seed_A0_D-3', T, T.const(0), T.const(-1), aut(T, z, T.mul(z, z)), {'endomorphism': 'automorphism (x,y)->(z x,y), z^2+z+1=0'}, D=-3)
T = Tower(['i'], [Fr(-1)]); i = T.gen(0)
record('seed_B0_D-4', T, T.const(-1), T.const(0), aut(T, i, T.neg(i)), {'endomorphism': 'automorphism (x,y)->(-x,i y)'}, D=-4)

# ---------------- generic rotation loop through the seed ----------------
def rotation_loop(name, T, A, B, rev_roots, seed_kind, R, fwd_roots, u, rot, m_expected, D):
    As, Bs, Mrev = run_path(T, A, B, rev_roots)
    if seed_kind == 'A0':
        assert T.is_zero(As) and T.eq(Bs, T.neg(T.pow(R, 3))), 'reverse path does not end at (0,-R^3)'
        Maut = aut(T, rot, T.mul(rot, rot))
    else:
        assert T.is_zero(Bs) and T.eq(As, T.neg(T.mul(R, R))), 'reverse path does not end at (-R^2,0)'
        Maut = aut(T, rot, T.neg(rot))
    Af, Bf, Mfwd = run_path(T, As, Bs, fwd_roots)
    assert same_model_scale(T, A, B, Af, Bf, u), 'forward path does not close up to the scale u'
    M = matmul(T, matmul(T, matmul(T, Mrev, Maut), Mfwd), iso(T, u))
    return record(name, T, A, B, M, {'endomorphism': f'reverse path ({len(rev_roots)} steps) -> seed automorphism -> forward path -> isomorphism u', 'degree': 4**len(rev_roots), 'closing_u': T.show(u)}, m_expected, D)

# D=-12 depth one from A=0
T = Tower(['t'], [Fr(-3)]); t = T.gen(0); z = T.mul(T.const(Fr(1,2)), T.add(T.const(-1), t))
rotation_loop('depth1_A0_D-12', T, T.const(-15), T.const(-22), [T.const(-2)], 'A0', T.const(4), [T.const(4)], T.const(2), z, T.const(-1), -12)
# seed-free: sqrt(-3) degree-3 endomorphism; kernel x-coordinate -3 (y^2=-4)
A0, B0 = T.const(-15), T.const(-22)
xQ = T.const(-3); yQ2 = T.add(T.add(T.pow(xQ, 3), T.mul(A0, xQ)), B0)
gx = T.add(T.mul(T.const(3), T.mul(xQ, xQ)), A0); vQ = T.mul(T.const(2), gx); uQ = T.mul(T.const(4), yQ2)
A3 = T.sub(A0, T.mul(T.const(5), vQ)); B3 = T.sub(B0, T.mul(T.const(7), T.add(uQ, T.mul(xQ, vQ))))
u3 = t  # sqrt(-3)
assert same_model_scale(T, A0, B0, A3, B3, u3)
M = matmul(T, velu_odd(T, T.mul(T.const(2), xQ), 3), iso(T, u3))
record('depth1_A0_D-12_seedfree_deg3', T, A0, B0, M, {'endomorphism': 'sqrt(-3): odd Velu 3-isogeny, kernel x=-3, then isomorphism u=sqrt(-3)', 'degree': 3}, T.const(-1), -12)

# D=-16 depth one from B=0
T = Tower(['i'], [Fr(-1)]); i = T.gen(0)
rotation_loop('depth1_B0_D-16', T, T.const(-11), T.const(-14), [T.const(-2)], 'B0', T.const(4), [T.const(4)], T.const(2), i, T.const(-1), -16)

# D=-48 depth two from A=0: e^2=3
T = Tower(['e', 'i'], [Fr(3), Fr(-1)]); e = T.gen(0); i = T.gen(1)
z = T.mul(T.const(Fr(1,2)), T.add(T.const(-1), T.mul(e, i)))
one = T.const(1)
A = T.add(T.const(-135), T.mul(T.const(-60), e)); B = T.add(T.const(-694), T.mul(T.const(-420), e))
rev = [T.mul(T.const(-2), T.add(one, T.mul(T.const(2), e))), T.const(-8)]
R = T.const(16); fwd = [R, T.mul(R, T.add(one, T.mul(T.const(2), e)))]
rotation_loop('depth2_A0_D-48', T, A, B, rev, 'A0', R, fwd, T.const(4), z, T.neg(T.add(T.const(3), T.mul(T.const(2), e))), -48)

# D=-64 depth two from B=0: e^2=2
T = Tower(['e', 'i'], [Fr(2), Fr(-1)]); e = T.gen(0); i = T.gen(1); one = T.const(1)
A = T.add(T.const(-91), T.mul(T.const(-60), e)); B = T.add(T.const(-462), T.mul(T.const(-308), e))
rev = [T.mul(T.const(-2), T.add(one, T.mul(T.const(2), e))), T.const(-8)]
R = T.const(16); fwd = [R, T.mul(R, T.add(one, T.mul(T.const(2), e)))]
rotation_loop('depth2_B0_D-64', T, A, B, rev, 'B0', R, fwd, T.const(4), i, T.neg(T.add(T.const(3), T.mul(T.const(2), e))), -64)

# D=-192 depth three from A=0: e^2=3, g^2=2, basis (1,e,g,eg)
T = Tower(['e', 'g', 'i'], [Fr(3), Fr(2), Fr(-1)]); e = T.gen(0); g = T.gen(1); i = T.gen(2)
basis = [T.const(1), e, g, T.mul(e, g)]
z = T.mul(T.const(Fr(1,2)), T.add(T.const(-1), T.mul(e, i)))
A = vec(T, (-1095, -540, -540, -420), basis); B = vec(T, (-22198, -13860, -16380, -8820), basis)
rev = [vec(T, c, basis) for c in ((-2, -4, -12, -4), (-8, -16, 0, 0), (-32, 0, 0, 0))]
R = T.const(64); fwd = [T.mul(R, vec(T, c, basis)) for c in ((1, 0, 0, 0), (1, 2, 0, 0), (1, 2, 6, 2))]
rotation_loop('depth3_A0_D-192', T, A, B, rev, 'A0', R, fwd, T.const(8), z, vec(T, (-7, -6, -6, -2), basis), -192)

# D=-256 depth three from B=0: w^2=2, s^2=w (s^4=2), i^2=-1 ; basis (1,s,s^2,s^3)
T = Tower(['w', 's', 'i'], [Fr(2), lambda TT: (Fr(0), Fr(1)), Fr(-1)])
w = T.gen(0); s = T.gen(1); i = T.gen(2)
assert T.eq(T.mul(s, s), w) and T.eq(T.pow(s, 4), T.const(2))
basis = [T.const(1), s, T.mul(s, s), T.pow(s, 3)]
A = vec(T, (-731, -600, -540, -360), basis); B = vec(T, (-14798, -11816, -10164, -8456), basis)
q0 = T.const(1); q1 = vec(T, (1, 0, 2, 0), basis); q2 = vec(T, (1, 4, 2, 4), basis)
rev = [T.mul(T.const(-2), q2), T.mul(T.const(-8), q1), T.mul(T.const(-32), q0)]
R = T.const(64); fwd = [T.mul(R, q0), T.mul(R, q1), T.mul(R, q2)]
rotation_loop('depth3_B0_D-256', T, A, B, rev, 'B0', R, fwd, T.const(8), i, vec(T, (-7, -4, -6, -4), basis), -256)

# ---------------- new seed D=-7 (principal) ----------------
T = Tower(['e'], [Fr(-7)]); e = T.gen(0)
A = T.const(-35); B = T.const(-98)
q = T.mul(T.const(Fr(1,2)), T.add(T.const(-7), e))
A1, B1 = quotient2(T, A, B, q)
u = T.mul(T.const(Fr(1,2)), T.add(T.const(1), e))
assert same_model_scale(T, A, B, A1, B1, u)
assert T.is_zero(T.add(T.sub(T.mul(u, u), u), T.const(2)))   # u^2 - u + 2 = 0
M = matmul(T, velu2(T, q), iso(T, u))
record('new_seed_D-7', T, A, B, M, {'endomorphism': '(1+sqrt(-7))/2: normalized 2-isogeny, kernel root (-7+e)/2, closing u=(1+e)/2', 'degree': 2,
        'kernel_root': T.show(q), 'quotient': [T.show(A1), T.show(B1)]}, None, -7)
# conjugate endomorphism (other horizontal root) as a consistency check
q_ = T.mul(T.const(Fr(1,2)), T.sub(T.const(-7), e)); u_ = T.mul(T.const(Fr(1,2)), T.sub(T.const(1), e))
A1_, B1_ = quotient2(T, A, B, q_); assert same_model_scale(T, A, B, A1_, B1_, u_)
record('new_seed_D-7_conjugate_endomorphism', T, A, B, matmul(T, velu2(T, q_), iso(T, u_)), {'endomorphism': '(1-sqrt(-7))/2', 'degree': 2}, None, -7)

# ---------------- control D=-8 ----------------
T = Tower(['v'], [Fr(-2)]); v = T.gen(0)
A = T.const(-30); B = T.const(56); q = T.const(4)
A1, B1 = quotient2(T, A, B, q)
assert same_model_scale(T, A, B, A1, B1, v)
record('control_D-8', T, A, B, matmul(T, velu2(T, q), iso(T, v)), {'endomorphism': 'sqrt(-2): normalized 2-isogeny, kernel root 4 (rational), closing u=sqrt(-2)', 'degree': 2,
        'quotient': [T.show(A1), T.show(B1)]}, None, -8)

if __name__ == '__main__':
    clean = {k: {kk: vv for kk, vv in v.items() if not kk.startswith('_')} for k, v in results.items()}
    print(json.dumps(clean, indent=1))
    if len(sys.argv) > 1:
        json.dump(clean, open(sys.argv[1], 'w'), indent=1)
    bad = [k for k, v in clean.items() if v.get('minus_c_equals_retained_multiplier') is False]
    print('MISMATCHES:', bad)
    sys.exit(1 if bad else 0)
