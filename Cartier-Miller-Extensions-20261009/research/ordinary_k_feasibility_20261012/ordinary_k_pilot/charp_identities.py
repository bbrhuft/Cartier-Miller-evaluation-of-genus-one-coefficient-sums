"""Characteristic-p checks of the normalization theorem  M_bar = [[0, -beta], [0, H]].

Three independent numerical routes, none of which reads the handover targets:

  (P) Vélu data of the separable endomorphism pi - 1 (kernel E(F_p)):
        sigma_{E(F_p)} = sum_{Q != O} x(Q)  ==  -beta,
        t_G == w_G == 0  (normalized Vélu codomain is (A, B), scale u = -1),
      hence F_bar = (pi-1)^* + I = [[0, sigma], [0, 1 - #E]] = [[0, -beta], [0, t - p]].
  (V) Vélu data of the Verschiebung pi_hat = t - pi (kernel = étale p-torsion):
        psi_p = c * psi_V^p in F_p[x];  sigma_V = 2 * (sum of roots of psi_V);
        kappa == -sigma_V / t^2.
  (S) supersingular controls: psi_p is a nonzero constant mod p (no étale p-torsion).

Exit status is nonzero on any failure (CheckFailure propagates).
"""
from pathlib import Path
import csv
import json
import random
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from okp_common import (CheckFailure, require, primes_between, nonsingular, trace_by_count,  # noqa: E402
                        points, j_invariant, H_beta_recurrence, division_polynomial_odd,
                        sha256_file, environment, is_prime)

OUT = Path(__file__).resolve().parent / 'results'


def route_P(A, B, p):
    pts = points(A, B, p)
    N = len(pts) + 1
    sigma = sum(x for x, _ in pts) % p
    tG = sum(3 * x * x + A for x, _ in pts) % p
    wG = sum(5 * x ** 3 + 3 * A * x + 2 * B for x, _ in pts) % p
    return N, sigma, tG, wG


def route_V(A, B, p):
    """Return (deg of f_p mod p, sigma_V or None, leading constant)."""
    fp = division_polynomial_odd(p, A, B, p)
    deg = len(fp) - 1
    if deg <= 0:
        return deg, None, (fp[0] if fp else 0)
    require(all(c == 0 for i, c in enumerate(fp) if i % p), 'f_p mod p is not a polynomial in x^p')
    g = [fp[k * p] for k in range(deg // p + 1)]
    h = (p - 1) // 2
    require(len(g) - 1 == h, f'Verschiebung kernel degree {len(g)-1} != {h}')
    sigma_V = (-2 * g[h - 1] * pow(g[h], -1, p)) % p
    return deg, sigma_V, g[h]


def check_model(A, B, p, with_V=True, with_twist=True):
    H, beta = H_beta_recurrence(A, B, p)
    t = trace_by_count(A, B, p)
    require(H == t % p, f'H != t mod p at {(p, A, B)}')
    row = {'p': p, 'A': A, 'B': B, 'j': j_invariant(A, B, p), 'trace': t, 'H': H, 'beta': beta}
    if H == 0:
        row['class'] = 'supersingular'
        if with_V:
            deg, sV, lead = route_V(A, B, p)
            require(deg == 0 and lead != 0, f'supersingular f_p mod p not a nonzero constant at {(p, A, B)}')
            row.update({'deg_fp_mod_p': deg})
        return row
    kappa = beta * pow(H, -1, p) % p
    N, sigma, tG, wG = route_P(A, B, p)
    require(N == p + 1 - t, 'point count mismatch')
    require(sigma == (-beta) % p, f'point-sum identity fails at {(p, A, B)}')
    # Vélu codomain A' = A - 5 t_G, B' = B - 7 w_G must equal (A, B) (scale u = -1).
    # (At p = 7 the factor 7 makes the B' condition automatic; w_G itself need not vanish.)
    require((A - 5 * tG) % p == A % p and (B - 7 * wG) % p == B % p,
            f'pi-1 Vélu codomain is not (A,B) at {(p, A, B)}')
    b0, d0 = sigma, (1 - N) % p
    require(d0 == H, 'assembled d0 != H')
    require((-b0 * pow(d0, -1, p)) % p == kappa, 'assembled -b0/d0 != kappa')
    row.update({'class': 'ordinary', 'kappa': kappa, 'sigma_EFp': sigma, 'tG': tG, 'wG': wG,
                'Mbar_b0': b0, 'Mbar_d0': d0})
    if with_V:
        deg, sV, lead = route_V(A, B, p)
        require(sV is not None, 'ordinary curve without étale p-torsion kernel')
        kV = (-sV * pow(t * t, -1, p)) % p
        require(kV == kappa, f'Verschiebung route kappa {kV} != {kappa} at {(p, A, B)}')
        row.update({'deg_fp_mod_p': deg, 'sigma_V': sV, 'kappa_V': kV, 'psiV_lead_const': lead})
        if with_twist:
            d = 2
            A2, B2 = A * d * d % p, B * d ** 3 % p
            _, sV2, _ = route_V(A2, B2, p)
            t2 = trace_by_count(A2, B2, p)
            k2 = (-sV2 * pow(t2 * t2, -1, p)) % p
            require(k2 == d * kappa % p, f'twist law fails on V route at {(p, A, B)}')
            row['twist_d2_kappa_V'] = k2
    return row


def main():
    t0 = time.time()
    OUT.mkdir(exist_ok=True)
    rows = []
    exhaustive = primes_between(7, 23)
    sampled = primes_between(29, 31)
    rng = random.Random(20261012)
    for p in exhaustive:
        for A in range(p):
            for B in range(p):
                if nonsingular(A, B, p):
                    rows.append(check_model(A, B, p))
    for p in sampled:
        models = [(A, B) for A in range(p) for B in range(p) if nonsingular(A, B, p)]
        for A, B in rng.sample(models, 80):
            rows.append(check_model(A, B, p, with_twist=False))
    # Larger primes: route P only (point enumeration), random models.
    big = []
    while len(big) < 60:
        q = rng.randrange(1000, 20000)
        if is_prime(q):
            big.append(q)
    for p in big:
        for _ in range(3):
            while True:
                A, B = rng.randrange(p), rng.randrange(p)
                if nonsingular(A, B, p):
                    break
            rows.append(check_model(A, B, p, with_V=False))
    cols = ['p', 'A', 'B', 'j', 'trace', 'H', 'beta', 'class', 'kappa', 'sigma_EFp', 'tG', 'wG',
            'Mbar_b0', 'Mbar_d0', 'deg_fp_mod_p', 'sigma_V', 'kappa_V', 'psiV_lead_const', 'twist_d2_kappa_V']
    with (OUT / 'charp_identities.csv').open('w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in cols})
    ordinary = [r for r in rows if r['class'] == 'ordinary']
    summary = {
        'status': 'PASS', 'failures': 0,
        'models_checked': len(rows),
        'ordinary': len(ordinary), 'supersingular': len(rows) - len(ordinary),
        'route_P_point_sum_and_codomain_checks': len(ordinary),
        'route_V_verschiebung_kernel_checks': sum(1 for r in ordinary if 'kappa_V' in r),
        'route_V_twist_checks': sum(1 for r in ordinary if 'twist_d2_kappa_V' in r),
        'supersingular_constant_fp_checks': sum(1 for r in rows if r['class'] == 'supersingular' and 'deg_fp_mod_p' in r),
        'trace_plus_one_rows': sum(1 for r in ordinary if r['trace'] == 1),
        'trace_minus_one_rows': sum(1 for r in ordinary if r['trace'] == -1),
        'A0_rows': sum(1 for r in ordinary if r['A'] == 0), 'B0_rows': sum(1 for r in ordinary if r['B'] == 0),
        'exhaustive_primes': exhaustive, 'sampled_primes': sampled, 'large_primes_route_P': sorted(set(big)),
        'source_sha256': {'charp_identities.py': sha256_file(__file__),
                          'okp_common.py': sha256_file(Path(__file__).resolve().parent / 'okp_common.py')},
        'environment': environment(), 'seconds': round(time.time() - t0, 2),
        'scope': 'Finite checks of derived identities; not a fast algorithm and not a proof.'}
    (OUT / 'charp_identities_summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k not in ('environment',)}, indent=1))
    print('CHARP_IDENTITIES_PASS')


if __name__ == '__main__':
    try:
        main()
    except CheckFailure as exc:
        print('FAIL:', exc)
        sys.exit(1)
