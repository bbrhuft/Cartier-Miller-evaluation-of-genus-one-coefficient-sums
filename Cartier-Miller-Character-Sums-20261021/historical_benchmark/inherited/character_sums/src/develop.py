"""Development run: all check families on the development prime ledger.

Usage (from the package root):   python3 src/develop.py
Writes results/development_results.json and results/development_ledger.json.
Development primes are recorded so that confirmation can exclude them.
"""
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import environment as envmod          # noqa: E402
import harness as H                   # noqa: E402

SEED = 20261020

DEV_SMALL = H.primes_in(7, 200)                                   # 42 primes
DEV_MEDIUM = [211, 307, 401, 503, 601, 701, 809, 907, 1009, 1999, 4999]
DEV_LARGE_GT = [10007, 100003, 1000003]                           # numpy + FLINT ground truth
DEV_HUGE = [1000000007, 1000000000039, 2305843009213693951, 1000000000000000009]
DEV_ROUNDED_THIRD = H.primes_in(11, 3000)                         # reference-only identity family


def main():
    t0 = time.time()
    rng = random.Random(SEED)
    fams = []
    fams.append(H.fam_reference_identities(DEV_SMALL, rng, per_prime=4))
    fams.append(H.fam_reference_identities(DEV_LARGE_GT[:2], rng, per_prime=2))
    fams.append(H.fam_constants_infinity(DEV_SMALL + DEV_MEDIUM, rng, per_prime=3))
    fams.append(H.fam_translation_twist(DEV_SMALL, rng, per_prime=3))
    fams.append(H.fam_extension_and_multiplicative(DEV_SMALL[:20], rng, per_prime=2))
    fams.append(H.fam_multipoint_identity(DEV_SMALL + DEV_MEDIUM, rng, per_prime=6))
    fams.append(H.fam_rounded_third(DEV_ROUNDED_THIRD))
    fams.append(H.fam_inherited_miller(DEV_SMALL, rng, per_prime=6))
    fams.append(H.fam_inherited_miller(DEV_MEDIUM, rng, per_prime=4))
    fams.append(H.fam_candidate_single(DEV_SMALL, rng, per_prime=4))
    fams.append(H.fam_candidate_weighted(DEV_SMALL + DEV_MEDIUM, rng, per_prime=3, configs=10))
    fams.append(H.fam_quartic_infinity(DEV_SMALL + DEV_MEDIUM, rng, per_prime=2))
    fams.append(H.fam_degenerate_domains(DEV_SMALL[:12], rng))
    fams.append(H.fam_endpoint(DEV_SMALL + DEV_MEDIUM, rng, per_prime=3))
    fams.append(H.fam_partial_fractions(DEV_SMALL, rng))
    fams.append(H.fam_invalid_inputs(rng))
    fams.append(H.fam_medium_ground_truth(DEV_LARGE_GT, rng, per_prime=2, configs=3))
    fams.append(H.fam_large_consistency(DEV_HUGE, rng, per_prime=3, queries=6))
    total_checks = sum(f['checks'] for f in fams)
    total_fail = sum(f['failures'] for f in fams)
    out = {
        'run': 'development',
        'seed': SEED,
        'command': 'python3 src/develop.py',
        'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0)),
        'seconds': round(time.time() - t0, 2),
        'total_checks': total_checks,
        'total_failures': total_fail,
        'families': fams,
        'environment': envmod.environment(),
        'file_hashes': envmod.file_hashes(envmod.CANDIDATE_FILES + envmod.vendor_files()),
    }
    ledger = {
        'implementation_primes': sorted(set(DEV_SMALL + DEV_MEDIUM + DEV_LARGE_GT + DEV_HUGE)),
        'rounded_third_primes_range': [11, 3000],
        'note': ('every family except rounded_third used only implementation_primes; the reference-only '
                 'rounded_third family used every prime 11 <= p < 3000. Confirmation excludes both.'),
    }
    os.makedirs(os.path.join(envmod.ROOT, 'results'), exist_ok=True)
    with open(os.path.join(envmod.ROOT, 'results', 'development_results.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    with open(os.path.join(envmod.ROOT, 'results', 'development_ledger.json'), 'w') as fh:
        json.dump(ledger, fh)
    for f in fams:
        print('%-46s checks=%7d failures=%d  (%.1fs)' % (f['family'], f['checks'], f['failures'], f['seconds']))
    print('TOTAL checks=%d failures=%d seconds=%.1f' % (total_checks, total_fail, out['seconds']))
    return 0 if total_fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
