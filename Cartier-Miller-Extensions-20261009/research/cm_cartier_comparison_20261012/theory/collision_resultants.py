"""Exact j-collision exclusions for the D=-7 seed (and the D=-8 control)
against the two easy seeds and the six retained families.

N_D = Res_J(J - j_new, H_D(J)) = +- H_D(j_new) (H_D monic). A prime p can
carry a collision j_new = j_D (mod p) only if p | N_D. Each N_D is factored
completely; every factor is certified prime (PARI isprime, which returns a
proven result; factors below 10^12 are also checked by trial division) and
the factorization is multiplied back. For each prime factor we record whether
it is admissible for the new seed and whether it is eligible for family D.
H_D are the exact class polynomials computed in cm_tables.json (equal to PARI
polclass, checked there).
"""
import json, sys, math
import cypari2
pari = cypari2.Pari(); pari.allocatemem(10**9)
here = __file__.rsplit('/theory/', 1)[0]
tabs = json.load(open(here + '/results/cm_tables.json'))
HD = {v['D']: v['H_D_low_to_high'] for v in tabs.values()}
HD[-3] = [0, 1]; HD[-4] = [-1728, 1]

def ev(poly, x):
    s = 0
    for c in reversed(poly): s = s*x + c
    return s

def td_prime(n):
    if n < 2: return False
    d = 2
    while d*d <= n:
        if n % d == 0: return False
        d += 1
    return True

def family_eligible(D, p):
    """Eligibility of the retained families at p (from the retained recognizers)."""
    return {-3: p % 3 == 1, -4: p % 4 == 1, -12: p % 3 == 1, -16: p % 4 == 1,
            -48: p % 12 == 1, -64: p % 8 == 1, -192: p % 24 == 1,
            -256: p % 8 == 1 and pow(2, (p-1)//4, p) == 1,
            -7: p != 7 and p % 7 in (1, 2, 4), -8: p % 8 in (1, 3)}[D]

out = {}
for new_D, j_new in [(-7, -3375), (-8, 8000)]:
    rows = []
    for D in [-3, -4, -12, -16, -48, -64, -192, -256, -7, -8]:
        if D == new_D: continue
        N = ev(HD[D], j_new)
        fac = pari(f'factor({N})')
        primes = [int(fac[0][k]) for k in range(len(fac[0]))]
        exps = [int(fac[1][k]) for k in range(len(fac[0]))]
        prod = 1
        for q, e in zip(primes, exps): prod *= abs(q)**e if q != -1 else 1
        assert prod == abs(N), 'factorization does not multiply back'
        info = []
        for q in primes:
            if q == -1: continue
            proven = bool(pari(f'isprime({q})'))
            if q < 10**12: assert td_prime(q) == proven
            assert proven
            info.append({'prime': q, 'admissible_for_new_seed': family_eligible(new_D, q) and q >= 11,
                         'eligible_for_family_D': family_eligible(D, q) if q >= 5 else False,
                         'kronecker_D_q': int(pari(f'kronecker({D},{q})')),
                         'kronecker_newD_q': int(pari(f'kronecker({new_D},{q})'))})
        danger = [d['prime'] for d in info if d['admissible_for_new_seed']]
        rows.append({'D': D, 'N_D': str(N), 'digits': len(str(abs(N))), 'factors': {str(d['prime']): e for d, e in zip(info, [x for q, x in zip(primes, exps) if q != -1])},
                     'prime_info': info, 'admissible_collision_primes': danger})
    out[str(new_D)] = rows
print(json.dumps({k: [{kk: vv for kk, vv in r.items() if kk != 'prime_info'} for r in v] for k, v in out.items()}, indent=1))
bad = [(k, r['D'], r['admissible_collision_primes']) for k, v in out.items() for r in v if r['admissible_collision_primes']]
print('ADMISSIBLE COLLISION PRIMES:', bad)
json.dump(out, open(here + '/results/collision_resultants.json', 'w'), indent=1)
sys.exit(1 if bad else 0)
