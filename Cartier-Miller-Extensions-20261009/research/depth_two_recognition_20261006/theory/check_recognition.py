"""Independent exact parameter certificate checks; Python standard library only."""
from __future__ import annotations
import csv
import hashlib
import json
import math
import platform
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = {
    2: {'alpha': (-91, -60), 'gamma': (-462, -308),
        'a3': (-2719171, -1922580), 'g2': (403172, 284592),
        'modulus': 8},
    3: {'alpha': (-135, -60), 'gamma': (-694, -420),
        'a3': (-6834375, -3928500), 'g2': (1010836, 582960),
        'modulus': 12},
}

def prime(p):
    return p >= 2 and all(p % k for k in range(2, math.isqrt(p) + 1))

def coeff_pair(A, B, p):
    """Integer multinomial expansion, separate from recognition identities."""
    h = (p - 1) // 2
    out = []
    for degree in (p - 1, p - 2):
        value = 0
        for i in range(h + 1):
            j = degree - 3 * i
            k = h - i - j
            if j >= 0 and k >= 0:
                value += math.comb(h, i) * math.comb(h - i, j) * A**j * B**k
        out.append(value % p)
    return tuple(out)

def recognize(A, B, p, n):
    """Extract parameters by rational invariants, then verify every equality."""
    f = FAMILIES[n]
    A %= p
    B %= p
    if p < 7 or p % f['modulus'] != 1 or not A or not B:
        return None
    if (4 * A**3 + 27 * B**2) % p == 0:
        return None
    a0, a1 = f['a3']
    g0, g1 = f['g2']
    U = (a0 * B**2 - g0 * A**3) % p
    V = (a1 * B**2 - g1 * A**3) % p
    if not V:
        return None
    e = -U * pow(V, -1, p) % p
    if e * e % p != n:
        return None
    alpha = sum(x * e**i for i, x in enumerate(f['alpha'])) % p
    gamma = sum(x * e**i for i, x in enumerate(f['gamma'])) % p
    if not alpha or not gamma:
        return None
    r = alpha * B * pow(gamma * A % p, -1, p) % p
    if not r or A != alpha * r*r % p or B != gamma * r*r*r % p:
        return None
    return {'n': n, 'e': e, 'r': r, 'slope': -(3 + 2 * e) * r % p}

def jinv(A, B, p):
    return 6912 * A**3 * pow((4*A**3 + 27*B**2) % p, -1, p) % p

def run():
    parameter_rows = []
    exact_checked = 0
    known_sets = {}
    example = None
    for p in range(7, 251):
        if not prime(p):
            continue
        for n, f in FAMILIES.items():
            if p % f['modulus'] != 1:
                continue
            known = set()
            for e in range(p):
                if e*e % p != n:
                    continue
                alpha = (f['alpha'][0] + f['alpha'][1] * e) % p
                gamma = (f['gamma'][0] + f['gamma'][1] * e) % p
                assert alpha and gamma
                for r in range(1, p):
                    A, B = alpha * r*r % p, gamma * r*r*r % p
                    cert = recognize(A, B, p, n)
                    assert cert and cert['e'] == e and cert['r'] == r
                    known.add((A, B))
                    if p <= 97:
                        H, beta = coeff_pair(A, B, p)
                        assert H and beta == cert['slope'] * H % p
                        exact_checked += 1
                    else:
                        H = beta = ''
                    # Twists are included by r <- d r, without extracting sqrt(d).
                    d = 2
                    twist = recognize(d*d*A % p, d*d*d*B % p, p, n)
                    assert twist and twist['e'] == e and twist['r'] == d*r % p
                    assert twist['slope'] == d * cert['slope'] % p
                    parameter_rows.append((p,n,e,r,A,B,cert['slope'],H,beta,jinv(A,B,p)))
                    if example is None and n == 3:
                        example = parameter_rows[-1]
            known_sets[p,n] = known
    model_checks = 0
    for p in range(7, 74):
        if not prime(p):
            continue
        for n in FAMILIES:
            known = known_sets.get((p,n), set())
            for A in range(p):
                for B in range(p):
                    if (4*A**3+27*B**2) % p:
                        assert bool(recognize(A,B,p,n)) == ((A,B) in known)
                        model_checks += 1
    with (HERE/'parameter_checks.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(('p','family','e','r','A','B','slope','H','beta','j'))
        w.writerows(parameter_rows)
    exception_rows = []
    exceptional_primes = sorted({7,11,17,19,23,29,31,41,47,59,71,167,191,239,479,599,647,719,743})
    for p in exceptional_primes:
        for n, f in FAMILIES.items():
            for e in range(p):
                if e*e % p != n:
                    continue
                alpha = (f['alpha'][0]+f['alpha'][1]*e) % p
                gamma = (f['gamma'][0]+f['gamma'][1]*e) % p
                D = (4*alpha**3+27*gamma**2) % p
                assert D
                j=jinv(alpha,gamma,p)
                ec=(-e) % p
                ac=(f['alpha'][0]+f['alpha'][1]*ec) % p
                gc=(f['gamma'][0]+f['gamma'][1]*ec) % p
                jc=jinv(ac,gc,p)
                lower=';'.join(str(x) for x in (0,1728,287496,54000) if j==x % p)
                exception_rows.append((p,n,e,int(p % f['modulus']==1),alpha,gamma,j,int(j==jc),lower))
    with (HERE/'exceptional_reductions.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(('p','family','e','ordinary_congruence','alpha','gamma','j','conjugate_j_collision','lower_j_collision'))
        w.writerows(exception_rows)
    result={'parameter_cases':len(parameter_rows),'exact_multinomial_pairs':exact_checked,
            'exhaustive_short_model_recognition_cases':model_checks,
            'exceptional_reduction_rows':len(exception_rows),'example_n3':example,
            'scope':'all allowed family parameters for 7<=p<=250; all nonsingular models for 7<=p<=73; exact coefficient pairs through 97',
            'environment':{'python':platform.python_version(),'platform':platform.platform()},
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'all_passed':True,'timing_claim':'none'}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    run()
