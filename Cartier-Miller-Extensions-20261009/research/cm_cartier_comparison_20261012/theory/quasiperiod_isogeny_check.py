"""Numerical corroboration of the analytic identity used in Theorem 4:
for a normalized isogeny C/L -> C/L' (z -> z, L subset L' of index ell),
    G2*(L') = ell * G2*(L) + sigma_G,   sigma_G = sum_{w in L'/L, w != 0} wp(w; L),
and for an endomorphism z -> a z (L' = a^{-1} L):  G2*(L) = sigma_G / (a (a - conj a)).
Checked with PARI periods for the D=-7 model and its endomorphism (1+sqrt-7)/2,
the D=-8 model (sqrt-2) and the D=-12 model (sqrt-3, degree 3)."""
import json
import cypari2
pari = cypari2.Pari(); pari.set_real_precision(60)
out = []
for lab, A, B, a in [('D-7', -35, -98, '(1+sqrt(-7))/2'), ('D-7 conj', -35, -98, '(1-sqrt(-7))/2'),
                     ('D-8', -30, 56, 'sqrt(-2)'), ('D-12', -15, -22, 'sqrt(-3)')]:
    E = pari.ellinit([A, B], precision=320); per = pari.ellperiods(E, 1, precision=320)
    w1, w2 = per[0][0], per[0][1]; e1, e2 = per[1][0], per[1][1]
    G = (e1*pari.conj(w2) - e2*pari.conj(w1)) / (w1*pari.conj(w2) - w2*pari.conj(w1))
    av = pari(a); ell = pari.norm(av) if False else av*pari.conj(av)
    # kernel of z -> a z: points w in a^{-1}L / L, i.e. w = (m w1 + n w2)/a, reduced mod L
    pts = set(); ker = []
    for m in range(int(round(float(pari.real(ell)))) + 1):
        for n in range(int(round(float(pari.real(ell)))) + 1):
            w = (m*w1 + n*w2)/av
            z = pari.ellztopoint(E, w, precision=320)
            if len(z) == 1:   # point at infinity
                continue
            key = (round(float(pari.real(z[0])), 9), round(float(pari.imag(z[0])), 9), round(float(pari.real(z[1])), 9), round(float(pari.imag(z[1])), 9))
            if key not in pts:
                pts.add(key); ker.append(z)
    sigma = sum(z[0] for z in ker)
    rhs = sigma/(av*(av - pari.conj(av)))
    out.append({'case': lab, 'kernel_size_minus_1': len(ker), 'ell': str(ell), 'sigma_G': str(sigma)[:40],
                'G2*_from_quasiperiods': str(G)[:40], 'sigma/(a(a-abar))': str(rhs)[:40],
                'abs_diff': str(pari.abs(G - rhs))})
for o in out: print(o)
json.dump(out, open(__file__.rsplit('/theory/', 1)[0] + '/results/quasiperiod_isogeny_check.json', 'w'), indent=1)
import sys
worst = max(float(pari(o['abs_diff'].replace(' ', ''))) for o in out)
print('QUASIPERIOD_MAX_ABS_DIFF', worst)
sys.exit(0 if worst < 1e-60 else 1)
