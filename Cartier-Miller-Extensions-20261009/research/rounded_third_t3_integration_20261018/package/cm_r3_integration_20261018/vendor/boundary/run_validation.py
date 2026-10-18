"""Run independent tests and write a machine-readable validation record."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
from time import perf_counter
import unittest

from test_boundary_framework import sieve
from boundary_framework import __version__


def main(argv=None):
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "results")
    args = parser.parse_args(argv)
    results = args.output
    results.mkdir(exist_ok=True, parents=True)
    suite = unittest.defaultTestLoader.discover(str(root), pattern="test_*.py")
    start = perf_counter()
    with (results / "validation_console.txt").open("w", encoding="utf-8") as log:
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    primes257 = [p for p in sieve(257) if p > 2]
    primes127 = [p for p in sieve(127) if p > 2]
    thirds = [p for p in sieve(10000) if p >= 7]
    record = {
        "version": __version__,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "platform": platform.platform(),
        "elapsed_seconds": perf_counter()-start, "passed": result.wasSuccessful(),
        "test_methods": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "coverage": {
            "primality_inputs_checked_against_independent_sieve": 50001,
            "exhaustive_small_prime_boundary_inputs": sum(primes257),
            "routes_per_small_prime_boundary_input": 3,
            "exhaustive_small_prime_factorial_inputs": sum(primes127),
            "backends_per_factorial_input": 2,
            "third_family_prime_inputs": len(thirds),
            "ordinary_third_primes": sum(p % 3 == 1 for p in thirds),
            "rounded_third_primes": sum(p % 3 == 2 for p in thirds),
            "backends_per_third_input": 3,
            "original_t_recurrence_complete_sum_inputs": sum(primes127),
            "held_out_primes": [10007, 20021, 50021, 100003, 1000003],
            "integrated_third_prime_inputs": len(thirds),
            "integrated_comparisons_per_prime": "B_L vs scaled recurrence, a_L vs integer binomial, U vs original t recurrence",
            "integrated_forced_factorial_comparisons": len([p for p in sieve(2000) if p>=7]),
            "integrated_held_out_primes": [10007,20021,50021,100003,100019,1000003,1000037],
            "fifth_prime_inputs": len([p for p in sieve(10000) if p%5==4]),
            "fifth_boundary_checks": "both indices, direct, product_tree and bgs; exact integer binomial oracle",
            "fifth_complete_checks": "both indices at every supported prime <=10000; B, a, U against independent recurrence/binomial oracles",
            "fifth_held_out_primes": [10009,20029,50069,100019,1000039],
            "bgs_factorial_inputs": sum(primes257),
            "bgs_generic_boundary_inputs": sum(primes257),
            "bgs_exhaustive_unit_intervals":sum(p*(p+1)//2 for p in sieve(43) if p>2),
            "bgs_shifts":"Every degree < p and every shift at odd primes <=19, plus packed and 64-bit field cases; zero polynomials and known-node overlap included",
            "bgs_complete_forced_factorial_third_primes":len([p for p in sieve(1000) if p>=7]),
            "bgs_complete_fifth_primes":len([p for p in sieve(1000) if p%5==4]),
            "shared_batch_boundary_output_checks":6*sum(primes257),
            "shared_batch_modes":"exact and adjacent sharing; direct, product_tree and bgs",
            "shared_batch_generic_indices":sum(primes127),
            "shared_batch_third_family_primes":len(thirds),
            "shared_batch_fifth_family_primes":len([p for p in sieve(10000) if p%5==4]),
            "shared_batch_complete_indices":sum(p+2 for p in primes127),
            "shared_batch_complete_modes":"full and u_only against the original t recurrence; duplicate prefix calls intercepted",
            "shared_batch_counts":"p=59 indices 6,12,24,20: separate 7, exact 5, adjacent 4 primitive acquisitions; ratio denominators use <=1 shared inversion",
            "many_prime_all_index_outputs":4*sum(primes127),
            "many_prime_chunk_counts":[1,2,7,32],
            "many_prime_oracles":"B vs scaled strict-prefix recurrence; a vs exact integer binomial; U vs original t recurrence; every index at odd primes <=127",
            "many_prime_native_third_queries":len([p for p in sieve(2000) if p>=7]),
            "many_prime_native_fifth_queries":2*len([p for p in sieve(2000) if p%5==4]),
            "many_prime_retained_forest_bounds":[0,11,12,100,5000],
            "many_prime_contracts":"unordered queries, repeated prime moduli, duplicates, streaming/cancellation, U-only joint computation, preflight limits, native fifth grouping and atomic CSV failure handling",
            "dispatch_test_methods":12,
            "dispatch_policy_fixtures":"Explicitly synthetic unit-test timings, not benchmark evidence",
            "dispatch_validation":"Exact matching; order/duplicates/output/collection; source/environment/configuration invalidation; finite samples; recomputed medians; tie policy; real small-workload calibration; overrides; resource preflight; atomic profile publication; no implicit calibration",
            "release_consolidation_tests":8,
            "release_contracts":"Public facade/exports, malformed profile fallback, unavailable source fallback, runtime and retained-source integrity, failed evidence capture, runtime mutation detection, evidence ZIP checksums",
            "u_only_generic_input_count":sum(primes127),
            "u_only_third_prime_inputs":len([p for p in sieve(2000) if p>=7]),
            "u_only_fifth_prime_inputs":len([p for p in sieve(2000) if p%5==4]),
            "u_only_zero_multiplier_cases":"ordinary p=13; rounded p=17; fifth p=29 second index; generic bounded domain",
        },
        "source_sha256": {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(list(root.glob("*.py"))+list((root / "retained_cm").rglob("*.py")))},
        "limits": "Finite independent checks, not a formal proof or an audit of the published Cartier--Miller implementation.",
    }
    (results / "validation_results.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
