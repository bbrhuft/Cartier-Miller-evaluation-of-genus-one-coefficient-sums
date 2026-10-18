"""Calibrate exact local many-prime workloads; verify every timed output."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import median
from time import perf_counter

from boundary_framework import BoundaryError, ResourceLimitError, UnsupportedPrefixError, _integer, __version__
from many_primes import ManyPrimeEvaluator, PrimeQuery, range_queries
from dispatch_profile import configuration, workload_key, write_record, validate_target
from benchmark_many_primes import reference


def _values(rows):
    return {(r['p'], r['L']): (r['B_L'], r['a_L'], r['U_p_L']) for r in rows}


def calibrate(queries, profile, *, evaluator=None, repeats=3, output_mode='full',
              collection='collected', forest_chunks=(1, 8, 32),
              max_reference_steps=10_000_000):
    _integer(repeats, 'repeats'); _integer(max_reference_steps, 'max_reference_steps')
    if not 3 <= repeats <= 20 or max_reference_steps < 0:
        raise BoundaryError('repeats must be 3..20 and max_reference_steps nonnegative')
    if collection not in ('collected', 'streaming'):
        raise BoundaryError('collection must be collected or streaming')
    evaluator = evaluator or ManyPrimeEvaluator()
    wanted, unique, _, _ = evaluator._prepare(queries, 'independent', 32, 'auto', 1, output_mode)
    if not wanted:
        raise BoundaryError('calibration requires at least one query')
    maxima = {}
    for query in unique:
        maxima[query.p] = max(maxima.get(query.p, 0), query.L)
    if sum(maxima.values()) > max_reference_steps:
        raise ResourceLimitError('definition-level calibration reference exceeds max_reference_steps')
    try:
        forest_chunks = tuple(forest_chunks)
    except TypeError as exc:
        raise BoundaryError('forest_chunks must be iterable') from exc
    for count in forest_chunks:
        _integer(count, 'forest chunk count')
        if not 1 <= count <= 100000:
            raise BoundaryError('forest chunk count must be 1..100000')
    validate_target(profile)
    expected = _values(reference(unique))
    if output_mode == 'u_only':
        expected = {key: (None, None, value[2]) for key, value in expected.items()}
    methods = [('independent', backend, 32) for backend in ('auto', 'direct', 'product_tree', 'bgs')]
    seen_sizes = set()
    for chunks in forest_chunks:
        size = evaluator._schedule(unique, chunks)['chunk_size']
        if size not in seen_sizes:
            methods.append(('forest', 'auto', chunks)); seen_sizes.add(size)
    samples = {method: [] for method in methods}
    failures = {}
    # Rotate method order to reduce fixed-order warming and load bias.
    for repeat in range(repeats):
        order = methods[repeat % len(methods):] + methods[:repeat % len(methods)]
        for method in order:
            if method in failures:
                continue
            engine, backend, chunks = method
            begin = perf_counter()
            try:
                if collection == 'collected':
                    result = evaluator.evaluate(wanted, engine=engine, backend=backend,
                                                chunks=chunks, output_mode=output_mode)
                    rows = result['outputs']
                else:
                    rows = list(evaluator.iter_evaluate(wanted, engine=engine, backend=backend,
                                                        chunks=chunks, output_mode=output_mode))
                elapsed = perf_counter() - begin
            except (ResourceLimitError, UnsupportedPrefixError) as exc:
                failures[method] = str(exc)
                continue
            if (_values(rows) != expected or any(
                    (row['B_L'], row['a_L'], row['U_p_L']) != expected[row['p'], row['L']]
                    for row in rows)):
                # A wrong answer aborts the calibration; it is never treated
                # as a slow method that can simply be dropped from the profile.
                raise BoundaryError(f'calibration output mismatch for {engine}/{backend}/{chunks}')
            if collection == 'collected' and [(r['p'], r['L']) for r in rows] != [(q.p, q.L) for q in wanted]:
                raise BoundaryError('calibration output order mismatch')
            if len(rows) != (len(wanted) if collection == 'collected' else len(unique)):
                raise BoundaryError('calibration output count mismatch')
            samples[method].append(elapsed)
    candidates = []
    for (engine, backend, chunks), values in samples.items():
        if len(values) != repeats:
            continue
        candidates.append({'engine': engine, 'backend': backend, 'chunks': chunks,
                           'samples_seconds': values, 'median_seconds': median(values),
                           'verified': True})
    if not candidates:
        raise ResourceLimitError('no candidate completed calibration within its resource limits')
    record = {'workload_sha256': workload_key(wanted, output_mode, collection),
              'configuration': configuration(evaluator), 'output_mode': output_mode,
              'collection': collection, 'requested_queries': len(wanted),
              'unique_queries': len(unique), 'max_cutoff': max(q.L for q in unique),
              'reference_steps': sum(maxima.values()), 'candidates': candidates,
              'excluded_candidates': [{'engine': e, 'backend': b, 'chunks': c, 'reason': why}
                                      for (e, b, c), why in failures.items()],
              'generated_utc': datetime.now(timezone.utc).isoformat(),
              'verification': 'Every timed B/a/U output checked against scaled coefficient and original t recurrences.',
              'timing_scope': 'Same-process rotated candidate order, complete evaluate call or materialized '
                              'unique iterator; validation and result storage included. Constructor, reference '
                              'generation, output verification, profile I/O, CSV writing and imports excluded.'}
    write_record(profile, record)
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--bound', type=int)
    source.add_argument('--queries', nargs='*')
    parser.add_argument('--family', choices=('thirds', 'ordinary_third', 'rounded_third', 'fifths'), default='thirds')
    parser.add_argument('--profile', type=Path, required=True)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--collection', choices=('collected', 'streaming'), default='collected')
    parser.add_argument('--output-mode', choices=('full', 'u_only'), default='full')
    parser.add_argument('--max-reference-steps', type=int, default=10_000_000)
    parser.add_argument('--forest-chunks', type=int, nargs='*', default=[1, 8, 32])
    args = parser.parse_args(argv)
    try:
        if args.bound is not None:
            queries = range_queries(args.bound, args.family)
        else:
            queries = []
            for value in args.queries:
                try:
                    p, L = map(int, value.split(':'))
                except ValueError as exc:
                    raise BoundaryError('queries must be p:L pairs') from exc
                queries.append(PrimeQuery(p, L))
        record = calibrate(queries, args.profile, repeats=args.repeats, collection=args.collection,
                           output_mode=args.output_mode, forest_chunks=args.forest_chunks,
                           max_reference_steps=args.max_reference_steps)
        print(json.dumps({'version': __version__, 'profile': str(args.profile), **record}, indent=2))
        return 0
    except (BoundaryError, OSError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
