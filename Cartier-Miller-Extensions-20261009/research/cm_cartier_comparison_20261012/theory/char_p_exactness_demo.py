"""Concrete illustration of the characteristic-p warning: on an ordinary
E/F_p, the second-kind differential eta - (beta/H) omega is EXACT.
With c = beta/H and (x - c) F^h = sum a_m x^m, put
    G(x) = sum_{m != -1 mod p} a_m x^(m+1) / ((m mod p) + 1),  g = G(x)/y^p.
Then dg = G'(x) dx / y^p = (x - c) F^h dx / y^p = (x - c) dx / y.
We check G' = (x - c) F^h, ord_O(g) >= -1, and G(e_i) != 0 at the 2-torsion
roots e_i (so g has p-th-power poles of order p there)."""
import json, sys
from flint import nmod_poly
out = []
for p, A, B in [(11, -35 % 11, -98 % 11), (29, -35 % 29, -98 % 29), (43, 3, 7), (101, 5, 17), (113, -35 % 113, -98 % 113)]:
    F = nmod_poly([B, A, 0, 1], p); h = (p - 1)//2
    P = F**h; H = int(P[p-1]); beta = int(P[p-2])
    if H == 0:
        out.append({'p': p, 'A': A, 'B': B, 'skipped': 'supersingular'}); continue
    c = beta * pow(H, -1, p) % p
    Q = nmod_poly([(-c) % p, 1], p) * P
    coeffs = [int(Q[m]) for m in range(Q.degree() + 1)]
    G = [0]*(len(coeffs) + 1)
    for m, a in enumerate(coeffs):
        if (m + 1) % p == 0:
            assert a == 0, 'a_{p-1} must vanish'
            continue
        G[m+1] = a * pow((m % p) + 1, -1, p) % p
    Gp = nmod_poly(G, p)
    ok = Gp.derivative() == Q
    roots = [x for x in range(p) if (x**3 + A*x + B) % p == 0]
    out.append({'p': p, 'A': A, 'B': B, 'H': H, 'beta': beta, 'c': c, 'Gprime_equals_(x-c)F^h': ok,
                'deg_G': Gp.degree(), 'pole_order_of_g_at_O': max(0, 2*Gp.degree() - 3*p),
                'G_at_rational_2torsion_roots_nonzero': [int(Gp(x)) != 0 for x in roots]})
print(json.dumps(out, indent=1))
json.dump(out, open(__file__.rsplit('/theory/', 1)[0] + '/results/char_p_exactness_demo.json', 'w'), indent=1)
