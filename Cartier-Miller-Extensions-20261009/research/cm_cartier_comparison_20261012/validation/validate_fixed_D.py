"""Validate the uniform fixed-D CM evaluator against (i) the retained
recognizers (depth <= 3) and (ii) dense coefficients, over all members of
every family at eligible primes up to a bound, plus exhaustive scans at small
primes (every model with j a root of some H_D).  Also pairwise exact
resultants of all class polynomials (collisions between table discriminants).
"""
import os, sys, json, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'core'))
RETAINED = os.environ.get('RETAINED_RESEARCH', os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))  # release research/
for sub in ['branch_point_20261006', 'depth_three_recognition_20261007/core', 'depth_two_recognition_20261006/core', 'isogeny_closure_20261006/core']:
    sys.path.insert(0, os.path.join(RETAINED, sub))
from fixed_D_evaluator import load_table, slope_from_cm_table, SPLIT_TEST
from depth_three_recognize import recognize_short_through_depth_three as retained_recognize
from flint import nmod_poly
import cypari2
pari = cypari2.Pari(); pari.allocatemem(10**9)

table = load_table()
fails = []; stats = {}
t0 = time.time()

def dense_Hbeta(A, B, p):
    P = nmod_poly([B % p, A % p, 0, 1], p) ** ((p - 1) // 2)
    return int(P[p - 1]), int(P[p - 2])

def roots_mod(poly, p):
    P = pari(f'Pol({list(reversed(poly))})')
    return [int(x) for x in pari(f'polrootsmod({P},{p})')]

# --- members of every table discriminant at split primes up to bounds
cnt = 0; agree_retained = 0; dense_checked = 0; per_D = {}
for p in [int(x) for x in pari('primes([7,1500])')]:
    for D, t in table.items():
        if not SPLIT_TEST[D](p) or p % abs(D) == 0:
            continue
        js = roots_mod(t['H'], p)
        if not js:
            continue
        if len(js) != len(t['H']) - 1:
            fails.append(('partial_split', D, p, len(js)))
        for j0 in js:
            if j0 in (0, 1728 % p):
                fails.append(('j_seed_collision', D, p)); continue
            A0 = 3 * j0 * (1728 - j0) % p; B0 = 2 * j0 * (1728 - j0)**2 % p
            ts = range(1, p) if p < 200 else random.Random(p*abs(D)).sample(range(1, p), 6)
            for tt in ts:
                A, B = A0 * tt * tt % p, B0 * tt**3 % p
                hits = slope_from_cm_table(A, B, p, table)
                if len(hits) != 1 or hits[0][0] != D:
                    fails.append(('hits', D, p, A, B, hits)); continue
                slope = hits[0][1]
                if D in (-12, -16, -48, -64, -192, -256):
                    rec = retained_recognize(A, B, p)
                    if rec['status'] == 'recognized':
                        if rec['matches'][0]['beta_multiplier'] != slope:
                            fails.append(('retained_mismatch', D, p, A, B))
                        else:
                            agree_retained += 1
                    else:
                        # retained families exist only at their eligible primes
                        fails.append(('retained_not_recognized', D, p, A, B, rec['status']))
                if p < 400 or tt == ts[0]:
                    H, beta = dense_Hbeta(A, B, p)
                    if H == 0 or beta != slope * H % p:
                        fails.append(('dense', D, p, A, B))
                    dense_checked += 1
                cnt += 1; per_D[D] = per_D.get(D, 0) + 1
stats['members_checked'] = cnt
stats['members_per_D'] = {str(k): v for k, v in sorted(per_D.items())}
stats['agree_with_retained_recognizer'] = agree_retained
stats['dense_coefficient_checks'] = dense_checked

# --- exhaustive scan: at small primes, the CM-table evaluator accepts a model
#     iff the retained combined recognizer or the D=-7 / D=-8 seeds do
scan = 0; disagreements = 0
for p in [int(x) for x in pari('primes([7,100])')]:
    for A in range(1, p):
        for B in range(1, p):
            if (4*A**3 + 27*B*B) % p == 0: continue
            hits = slope_from_cm_table(A, B, p, table)
            hitsD = {D for D, _ in hits}
            rec = retained_recognize(A, B, p)
            retained_D = None
            if rec['status'] == 'recognized':
                fam = rec['matches'][0]['family']
                retained_D = {'depth1_0': -12, 'depth1_1728': -16, 'depth2_0': -48, 'depth2_1728': -64,
                              'depth3_0_disc_-192': -192, 'depth3_1728_disc_-256': -256}.get(fam, fam)
            retained_hits = {D for D in hitsD if D in (-12, -16, -48, -64, -192, -256)}
            if (retained_D is None and retained_hits) or (retained_D is not None and retained_hits != {retained_D}):
                disagreements += 1; fails.append(('scan', p, A, B, hits, retained_D))
            if len(hits) > 1:
                fails.append(('multiple_hits', p, A, B, hits))
            scan += 1
stats['exhaustive_models_scanned_p_le_100'] = scan
stats['exhaustive_disagreements_with_retained'] = disagreements

# --- pairwise resultants of class polynomials (incl. seeds j=0,1728)
polys = {D: t['H'] for D, t in table.items()}
polys[-3] = [0, 1]; polys[-4] = [-1728, 1]
pair = []
Ds = sorted(polys)
for i, D1 in enumerate(Ds):
    for D2 in Ds[i+1:]:
        R = pari(f'polresultant(Pol({list(reversed(polys[D1]))}), Pol({list(reversed(polys[D2]))}))')
        fac = pari(f'factor({R})')
        primes = [int(fac[0][k]) for k in range(len(fac[0])) if int(fac[0][k]) > 1]
        assert all(bool(pari(f'isprime({q})')) for q in primes)
        split_both = [q for q in primes if q >= 7 and q % abs(D1) and q % abs(D2)
                      and int(pari(f'kronecker({D1},{q})')) == 1 and int(pari(f'kronecker({D2},{q})')) == 1]
        pair.append({'D1': D1, 'D2': D2, 'resultant_digits': len(str(abs(int(R)))), 'prime_factors': primes,
                     'primes_split_in_both_fields': split_both})
        if split_both:
            fails.append(('pairwise_collision_at_split_prime', D1, D2, split_both))
stats['pairwise_resultants'] = len(pair)
stats['elapsed_seconds'] = round(time.time() - t0, 1)
stats['failures'] = len(fails)
os.makedirs(os.path.join(ROOT, 'results', 'validation'), exist_ok=True)
json.dump({'stats': stats, 'pairwise': pair, 'failures': [str(f) for f in fails[:100]]},
          open(os.path.join(ROOT, 'results', 'validation', 'fixed_D_validation.json'), 'w'), indent=1)
print(json.dumps(stats, indent=1))
print('FAILURES', len(fails)); [print(f) for f in fails[:15]]
sys.exit(1 if fails else 0)
