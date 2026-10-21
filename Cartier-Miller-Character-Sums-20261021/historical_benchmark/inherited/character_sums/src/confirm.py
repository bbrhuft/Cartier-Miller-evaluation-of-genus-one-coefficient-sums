"""Confirmation run on a sample selected AFTER the freeze, seeded by the freeze digest.

Usage (package root):  python3 src/confirm.py
1. Re-hash every frozen file; abort on any mismatch with FREEZE.json.
2. Seed = first 16 hex digits of the freeze digest; select primes by the fixed rule
   below, excluding every development prime and the development rounded-third range.
3. Run the same check families; write results/confirmation_results.json.
"""
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import environment as envmod   # noqa: E402
import freeze as fz            # noqa: E402
import harness as H            # noqa: E402
import reference as ref        # noqa: E402

SELECTION_RULE = {
    'small': '16 primes uniformly without replacement from primes in [200, 600) not in the development ledger',
    'medium': '8 primes uniformly from primes in [600, 5000) not in the ledger',
    'large_ground_truth': ('2 primes: next prime after a uniform integer in [20000, 2000000]; '
                           '1 prime: next prime after a uniform integer in [5000000, 10000000]'),
    'huge_consistency': '4 primes: next prime after a uniform integer of 40, 50, 60 and 63 bits',
    'rounded_third': '150 primes p = 5 mod 6 uniformly from [3000, 40000)',
    'invalid_inputs': 'smallest selected small prime; budget cases use the first large prime',
}


def next_prime(n):
    n |= 1
    while not ref.is_prime(n):
        n += 2
    return n


def main():
    with open(os.path.join(envmod.ROOT, 'FREEZE.json')) as fh:
        frz = json.load(fh)
    current = envmod.file_hashes(list(frz['files']))
    bad = [k for k in frz['files'] if current.get(k) != frz['files'][k]]
    if bad or fz.digest(current) != frz['digest']:
        print('FROZEN FILES CHANGED:', bad)
        return 2
    with open(os.path.join(envmod.ROOT, 'results', 'development_ledger.json')) as fh:
        ledger = json.load(fh)
    dev = set(ledger['implementation_primes'])
    seed = int(frz['digest'][:16], 16)
    sel = random.Random(seed)
    small = sel.sample([q for q in H.primes_in(200, 600) if q not in dev], 16)
    medium = sel.sample([q for q in H.primes_in(600, 5000) if q not in dev], 8)
    large = [next_prime(sel.randrange(20000, 2000001)) for _ in range(2)]
    large.append(next_prime(sel.randrange(5000000, 10000001)))
    huge = [next_prime(sel.randrange(2**(b - 1), 2**b)) for b in (40, 50, 60, 63)]
    r3 = sel.sample([q for q in H.primes_in(3000, 40000) if q % 6 == 5], 150)
    for q in large + huge:
        assert q not in dev
    sample = {'small': sorted(small), 'medium': sorted(medium), 'large_ground_truth': large,
              'huge_consistency': huge, 'rounded_third': sorted(r3)}
    print('confirmation sample:', json.dumps({k: v for k, v in sample.items() if k != 'rounded_third'}))
    t0 = time.time()
    rng = random.Random(seed ^ 0x5A5A5A5A)
    fams = []
    fams.append(H.fam_reference_identities(sorted(small), rng, per_prime=4))
    fams.append(H.fam_constants_infinity(sorted(small) + sorted(medium), rng, per_prime=3))
    fams.append(H.fam_translation_twist(sorted(small), rng, per_prime=3))
    fams.append(H.fam_extension_and_multiplicative(sorted(small)[:8], rng, per_prime=2))
    fams.append(H.fam_multipoint_identity(sorted(small) + sorted(medium), rng, per_prime=6))
    fams.append(H.fam_rounded_third(sorted(r3)))
    fams.append(H.fam_inherited_miller(sorted(small), rng, per_prime=4))
    fams.append(H.fam_inherited_miller(sorted(medium), rng, per_prime=3))
    fams.append(H.fam_candidate_single(sorted(small), rng, per_prime=4))
    fams.append(H.fam_candidate_weighted(sorted(small) + sorted(medium), rng, per_prime=3, configs=10))
    fams.append(H.fam_quartic_infinity(sorted(small) + sorted(medium), rng, per_prime=2))
    fams.append(H.fam_degenerate_domains(sorted(small)[:6], rng))
    fams.append(H.fam_endpoint(sorted(small) + sorted(medium), rng, per_prime=3))
    fams.append(H.fam_partial_fractions(sorted(small), rng))
    fams.append(H.fam_invalid_inputs(rng, p=min(small), big=large[0]))
    fams.append(H.fam_medium_ground_truth(large, rng, per_prime=2, configs=3))
    fams.append(H.fam_large_consistency(huge, rng, per_prime=3, queries=6))
    total_checks = sum(f['checks'] for f in fams)
    total_fail = sum(f['failures'] for f in fams)
    out = {
        'run': 'confirmation',
        'command': 'python3 src/confirm.py',
        'freeze_digest': frz['digest'],
        'frozen_utc': frz['frozen_utc'],
        'seed': seed,
        'selection_rule': SELECTION_RULE,
        'sample': sample,
        'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0)),
        'seconds': round(time.time() - t0, 2),
        'total_checks': total_checks,
        'total_failures': total_fail,
        'families': fams,
        'environment': envmod.environment(),
    }
    with open(os.path.join(envmod.ROOT, 'results', 'confirmation_results.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    for f in fams:
        print('%-46s checks=%7d failures=%d  (%.1fs)' % (f['family'], f['checks'], f['failures'], f['seconds']))
    print('TOTAL checks=%d failures=%d seconds=%.1f' % (total_checks, total_fail, out['seconds']))
    return 0 if total_fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
