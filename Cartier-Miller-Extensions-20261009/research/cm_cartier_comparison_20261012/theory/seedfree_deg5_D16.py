"""Seed-free check for D=-16: the endomorphism 1+2i (degree 5) of
y^2 = x^3 - 11x - 14, via odd Velu with kernel polynomial found by PARI
nffactor over Q(i) (PARI used only to find a candidate factor; every
subsequent identity is checked exactly in the tower Q(i))."""
import json, sys
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/theory/', 1)[0] + '/core')
from qtower import Tower
from isogeny_matrices import matmul, velu_odd, iso, slope_from_matrix
import cypari2
pari = cypari2.Pari()
A0, B0 = -11, -14
fac = pari(f'nffactor(nfinit(t^2+1), elldivpol(ellinit([{A0},{B0}]),5))')
quads = [fac[0][k] for k in range(len(fac[0])) if pari(f'poldegree({fac[0][k]})') == 2]
T = Tower(['i'], [Fr(-1)]); i = T.gen(0)
def tow(polmod):  # PARI element a + b*t (t^2=-1) -> tower element
    a = pari(f'polcoef(lift({polmod}),0)'); b = pari(f'polcoef(lift({polmod}),1)')
    return T.add(T.const(Fr(str(a))), T.mul(T.const(Fr(str(b))), i))
out = []
for Q in quads:
    c1 = tow(pari(f'polcoef({Q},1)')); c0 = tow(pari(f'polcoef({Q},0)'))   # x^2 + c1 x + c0
    s1 = T.neg(c1); s2 = c0                    # x1+x2, x1*x2
    A = T.const(A0); B = T.const(B0)
    p2 = T.sub(T.mul(s1, s1), T.mul(T.const(2), s2))            # x1^2+x2^2
    p3 = T.sub(T.mul(s1, p2), T.mul(s2, s1))                    # x1^3+x2^3
    p4 = T.sub(T.mul(s1, p3), T.mul(s2, p2))
    t_ = T.add(T.mul(T.const(6), p2), T.mul(T.const(4), A))     # sum v_R, v_R = 2(3x^2+A)
    sumF = T.add(T.add(p3, T.mul(A, s1)), T.mul(T.const(2), B)) # sum F(x_R)
    w_ = T.add(T.mul(T.const(4), sumF), T.add(T.mul(T.const(6), p3), T.mul(T.const(2), T.mul(A, s1))))
    A5 = T.sub(A, T.mul(T.const(5), t_)); B5 = T.sub(B, T.mul(T.const(7), w_))
    if T.is_zero(A5) or T.is_zero(B5):
        continue
    u2 = T.div(T.div(B5, B), T.div(A5, A))
    # candidate u: solve u^2 = u2 among 1+-2i, -1+-2i, 2+-i etc. (units times (1+-2i))
    cands = [T.add(T.const(a), T.mul(T.const(b), i)) for a in range(-3, 4) for b in range(-3, 4)]
    us = [u for u in cands if T.eq(T.mul(u, u), u2) and T.eq(T.pow(u, 4), T.div(A5, A))]
    if not us:
        out.append({'factor': str(Q), 'quotient': [T.show(A5), T.show(B5)], 'isomorphic_to_E': False})
        continue
    u = us[0]
    sigma = T.mul(T.const(2), s1)
    M = matmul(T, velu_odd(T, sigma, 5), iso(T, u))
    lam, mu, nu, c, slope = slope_from_matrix(T, M)
    out.append({'factor': str(Q), 'quotient': [T.show(A5), T.show(B5)], 'isomorphic_to_E': True, 'u': T.show(u),
                'lambda': T.show(lam), 'mu': T.show(mu), 'c': T.show(c), 'slope_r1': T.show(slope)})
print(json.dumps(out, indent=1))
ok = any(o.get('isomorphic_to_E') and o['slope_r1'] == '-1' for o in out)
print('SEEDFREE_DEG5_OK' if ok else 'NOT_FOUND')
if len(sys.argv) > 1: json.dump(out, open(sys.argv[1], 'w'), indent=1)
sys.exit(0 if ok else 1)
