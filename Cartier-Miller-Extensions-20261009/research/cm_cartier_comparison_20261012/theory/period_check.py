"""Direct check of the period normalization in Theorem 2 (not only the
weight-zero value): for each model over a real embedding, PARI's periods
[w1,w2] and quasi-periods [e1,e2] (zeta(z+w_i) = zeta(z) + e_i) for the
parametrization x = wp(z), y = wp'(z)/2 give the antiholomorphic line
eta + G omega with G = (e1 conj(w2) - e2 conj(w1)) / (w1 conj(w2) - w2 conj(w1)).
Compare with the exact algebraic c from the endomorphism loop, and with
pi^2 E2*(tau)/(3 w1^2)."""
import json, sys
sys.path.insert(0, __file__.rsplit('/theory/', 1)[0] + '/theory')
sys.path.insert(0, __file__.rsplit('/theory/', 1)[0] + '/core')
import family_loops as FL
from cm_tables import embeddings, evalc, eisenstein_with_bound
from mpmath import mpc, mpf, pi as mpi, mp, fabs
import cypari2
pari = cypari2.Pari(); pari.set_real_precision(80)
out = []
for name, rec in FL.results.items():
    if 'conjugate' in name or 'seedfree' in name: continue
    T = rec['_T']
    for signs, vals in embeddings(T):
        A = evalc(T, rec['_A'], vals); B = evalc(T, rec['_B'], vals); c = evalc(T, rec['_c'], vals)
        if abs(A.imag) > 1e-40 or abs(B.imag) > 1e-40:
            continue   # PARI ellinit over R only for real embeddings here
        A = pari(str(A.real)); B = pari(str(B.real))
        E = pari.ellinit([A, B], precision=320)
        per = pari.ellperiods(E, 1, precision=320)
        w1, w2 = per[0][0], per[0][1]; e1, e2 = per[1][0], per[1][1]
        G = (e1*pari.conj(w2) - e2*pari.conj(w1)) / (w1*pari.conj(w2) - w2*pari.conj(w1))
        tau = w2/w1
        if pari.imag(tau) < 0:
            w1, w2, e1, e2 = w2, w1, e2, e1; tau = w2/w1
        # E2*(tau) via PARI eta-free q-series
        tz = complex(tau); tm = mpc(str(pari.real(tau)), str(pari.imag(tau)))
        E2, E4, E6, N, tb = eisenstein_with_bound(tm)
        E2s = E2 - 3/(mpi*tm.imag)
        w1m = mpc(str(pari.real(w1)), str(pari.imag(w1)))
        G2 = mpi**2*E2s/(3*w1m**2)
        legendre = e1*w2 - e2*w1
        cP = pari(mp.nstr(c.real, 75)) + pari('I') * pari(mp.nstr(c.imag, 75))
        out.append({'model': name, 'signs': signs, 'G_from_quasiperiods': str(pari.real(G))[:30],
                    'c_exact_numeric': str(c.real)[:30], 'abs(G-c)': str(pari.abs(G - cP)),
                    'abs(pi^2E2*/(3w1^2) - c)': mp.nstr(fabs(G2 - c), 5),
                    'legendre_e1w2-e2w1': str(legendre)[:40]})
for o in out: print(o['model'], o['signs'], '|G-c|=', o['abs(G-c)'], '|G2*-c|=', o['abs(pi^2E2*/(3w1^2) - c)'], 'Legendre=', o['legendre_e1w2-e2w1'])
json.dump(out, open(__file__.rsplit('/theory/', 1)[0] + '/results/period_check.json', 'w'), indent=1)
worst = max(max(float(pari(o['abs(G-c)'].replace(' ', ''))), float(o['abs(pi^2E2*/(3w1^2) - c)'])) for o in out)
print('PERIOD_CHECK_MAX_ABS_DIFF', worst)
sys.exit(0 if worst < 1e-60 else 1)
