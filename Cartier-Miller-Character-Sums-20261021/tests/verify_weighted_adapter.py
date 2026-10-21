"""Independent enumeration checks for the newly packaged weighted adapter."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import weighted_sums as W


def evaluate_polynomial(f, x, p):
    # Deliberately use a different polynomial evaluation from the engine.
    return sum(c*pow(x, k, p) for k, c in enumerate(f)) % p


def reference_data(p, f):
    multiplicity = Counter(y*y % p for y in range(p))
    eps = [multiplicity[evaluate_polynomial(f, x, p)]-1 for x in range(p)]
    n_inf = 1 if len(f) == 4 else multiplicity[f[-1] % p]
    trace = 1-n_inf-sum(eps)
    return eps, trace, n_inf


def reference_sum(p, f, excluded, residues, constant):
    points = [(x, y) for x in range(p) for y in range(p)
              if y*y % p == evaluate_polynomial(f, x, p)]
    eps, _, n_inf = reference_data(p, f)
    def weight(x):
        return (constant+sum(r*pow((x-a) % p, p-2, p)
                            for a, r in zip(excluded, residues))) % p
    ch = sum(eps[x]*weight(x) for x in range(p) if x not in excluded) % p
    aff = sum(weight(x) for x, _ in points if x not in excluded) % p
    return (ch, aff, (aff+constant*n_inf) % p)


def reject(call, count):
    try:
        call()
    except (ValueError, TypeError):
        count['invalid_inputs_rejected'] += 1
    else:
        raise AssertionError('invalid input was accepted')


def run(mode):
    count = Counter()
    freeze = json.loads((ROOT/'verification/ADAPTER_FREEZE.json').read_text())
    for name, digest in freeze['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    seed = 20261021 if mode == 'development' else int(freeze['digest'], 16)
    rng = random.Random(seed)
    primes = [5, 7, 11, 13, 17, 19] if mode == 'development' else [23, 29, 31, 37, 41, 43]
    for p in primes:
        for degree in (3, 4):
            for _ in range(10):
                while True:
                    f = [rng.randrange(p) for _ in range(degree)]+[rng.randrange(1, p)]
                    eps, trace, n_inf = reference_data(p, f)
                    try:
                        W.prepare_weights(p, f, trace)
                    except ValueError:
                        continue
                    break
                count['models'] += 1
                count['zero_constant_models'] += f[0] == 0
                count['quartics_without_rational_infinity'] += degree == 4 and n_inf == 0
                for scenario in range(8):
                    size = [0, 1, min(3, p), p, rng.randrange(p+1),
                            min(6, p), min(2, p), min(5, p)][scenario]
                    excluded = rng.sample(list(range(p)), size)
                    if scenario == 1:
                        excluded = [0]
                    residues = [rng.randrange(p) if eps[a] else 0 for a in excluded]
                    if residues and scenario in (2, 4, 7):
                        residues[-1] = 0
                    constant = rng.randrange(p)
                    state = W.prepare_weights(p, f, trace, excluded)
                    got = state.evaluate(residues, constant)
                    want = reference_sum(p, f, excluded, residues, constant)
                    assert (got.character, got.affine_points, got.projective_points) == want, (
                        p, f, trace, excluded, residues, constant, got, want)
                    count['weighted_queries'] += 1
                    count['output_residue_comparisons'] += 3
                    count['empty_affine_domains'] += size == p
                    count['zero_poles'] += 0 in excluded
                    count['extra_exclusions'] += any(r == 0 for r in residues)
                    count['branch_exclusions'] += any(eps[a] == 0 for a in excluded)
                    count['constant_only_queries'] += not any(residues)
                    # Reuse the exact same prepared vectors with new coefficients.
                    second = [rng.randrange(p) if eps[a] else 0 for a in excluded]
                    got2 = state.evaluate(second, -constant)
                    want2 = reference_sum(p, f, excluded, second, -constant)
                    assert (got2.character, got2.affine_points, got2.projective_points) == want2
                    count['cached_queries'] += 1
                    count['output_residue_comparisons'] += 3
    # Explicit prior counterexample: the zero residue still excludes x=2.
    p, f = 7, [1, 1, 0, 1]
    _, trace, _ = reference_data(p, f)
    assert W.single_pole(p, f, 1, trace) == 0
    assert W.prepare_weights(p, f, trace, [1, 2]).evaluate([1, 0]).character == 6
    count['explicit_domain_counterexamples_checked'] += 1
    # Small-field curve-order 2p example, without enumeration in the evaluator.
    assert W.single_pole(5, [0, 3, 0, 1], 1, -4) == 1
    count['small_field_order_2p_checks'] += 1
    branch = W.prepare_weights(7, [0, 1, 0, 1], 0, [0])
    for call in [
        lambda: W.prepare_weights(3, f, 0),
        lambda: W.prepare_weights(8, f, 0),
        lambda: W.prepare_weights(7, [1, 0, 0, 0, 0, 1], 0),
        lambda: W.prepare_weights(7, [0, 0, 0, 1], 0),
        lambda: W.prepare_weights(7, f, 99),
        lambda: W.prepare_weights(7, f, 0, [1, 8]),
        lambda: W.prepare_weights(7.0, f, 0),
        lambda: W.prepare_weights(7, [1.1, 1, 0, 1], 0),
        lambda: branch.evaluate([1]),
        lambda: branch.evaluate([]),
        lambda: branch.evaluate([0], 1.5),
        lambda: W.single_pole(7, [0, 1, 0, 1], 0, 0),
    ]:
        reject(call, count)
    return {'status': 'PASS', 'mode': mode, 'primes': primes,
            'source_freeze_digest': freeze['digest'], **dict(count)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('development', 'confirmation'), default='development')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(args.mode)
    encoded = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(encoded, end='')
