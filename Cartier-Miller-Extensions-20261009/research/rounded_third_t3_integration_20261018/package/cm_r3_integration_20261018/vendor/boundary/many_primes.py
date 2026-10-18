"""Many-prime complete Cartier--Miller outputs via retained remainder forests.

Forests amortize one integer recurrence across queries sorted by cutoff.
The independent engine uses native stopping-point sessions where supported.
See MANY_PRIMES.md for limits, streaming order and cost accounting.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import json
from math import isqrt
from pathlib import Path
from time import perf_counter

from boundary_framework import (
    BoundaryError, DirectReferencePrefix, ResourceLimitError, _integer,
    is_prime64, __version__,
)
from integrated_thirds import ThirdPointSession
from integrated_fifths import FifthPointSession
from shared_boundaries import BoundaryBatchSession
from retained_cm import rounded_third_batch as retained


@dataclass(frozen=True)
class PrimeQuery:
    p: int
    L: int


def range_queries(bound, family='thirds', *, max_bound=2_000_000):
    """Generate supported stopping queries at primes strictly below bound."""
    _integer(bound, 'bound')
    _integer(max_bound, 'max_bound')
    if bound < 0 or max_bound < 0:
        raise BoundaryError('bound and max_bound must be nonnegative')
    if bound > max_bound:
        raise ResourceLimitError('prime sieve bound exceeds max_bound')
    if not isinstance(family, str) or family not in ('thirds', 'ordinary_third', 'rounded_third', 'fifths'):
        raise BoundaryError('unknown range family')
    if family == 'rounded_third':
        return [PrimeQuery(p, (p + 1) // 3) for p in retained.branch_primes(bound)]
    flags = bytearray(b'\x01') * bound
    if bound:
        flags[0] = 0
    if bound > 1:
        flags[1] = 0
    for q in range(2, isqrt(max(0, bound - 1)) + 1):
        if flags[q]:
            flags[q*q:bound:q] = b'\x00' * len(range(q*q, bound, q))
    result = []
    for p in range(7, bound, 2):
        if not flags[p]:
            continue
        if family == 'fifths':
            if p >= 19 and p % 5 == 4:
                result.extend((PrimeQuery(p, (p + 1) // 5), PrimeQuery(p, 2 * (p + 1) // 5)))
        elif p % 3 == 1 and family in ('thirds', 'ordinary_third'):
            result.append(PrimeQuery(p, (p - 1) // 3))
        elif p >= 11 and p % 3 == 2 and family == 'thirds':
            result.append(PrimeQuery(p, (p + 1) // 3))
    return result


class ManyPrimeEvaluator:
    def __init__(self, *, max_queries=100_000, max_forest_index=2_000_000,
                 max_modulus_bits=2_000_000, max_chunk_product_bits=32_000_000,
                 direct_cutoff=262144, max_degree=8192, max_direct_terms=2_000_000):
        for name, value in (('max_queries', max_queries), ('max_forest_index', max_forest_index),
                            ('max_modulus_bits', max_modulus_bits),
                            ('max_chunk_product_bits', max_chunk_product_bits)):
            _integer(value, name)
            if value < 0:
                raise BoundaryError(f'{name} must be nonnegative')
            setattr(self, name, value)
        # Reuse existing resource validation, without acquiring a boundary.
        BoundaryBatchSession(3, direct_cutoff=direct_cutoff, max_degree=max_degree,
                             max_direct_terms=max_direct_terms)
        self.kernel_options = dict(direct_cutoff=direct_cutoff, max_degree=max_degree,
                                   max_direct_terms=max_direct_terms)

    def _prepare(self, queries, engine, chunks, backend, modulus_power, output_mode):
        begin = perf_counter()
        if not isinstance(engine, str) or engine not in ('forest', 'independent'):
            raise BoundaryError('engine must be forest or independent')
        _integer(chunks, 'chunks')
        if chunks < 1:
            raise BoundaryError('chunks must be positive')
        if not isinstance(backend, str) or backend not in ('auto', 'direct', 'product_tree', 'bgs'):
            raise BoundaryError('unknown independent boundary backend')
        if type(modulus_power) is not int or modulus_power != 1:
            raise BoundaryError('many-prime interface supports modulo p only')
        if not isinstance(output_mode, str) or output_mode not in ('full', 'u_only'):
            raise BoundaryError('output_mode must be full or u_only')
        try:
            iterator = iter(queries)
        except TypeError as exc:
            raise BoundaryError('queries must be an iterable of PrimeQuery objects') from exc
        wanted, primes = [], set()
        for query in iterator:
            if len(wanted) >= self.max_queries:
                raise ResourceLimitError('request count exceeds max_queries')
            if not isinstance(query, PrimeQuery):
                raise BoundaryError('each request must be a PrimeQuery')
            p, L = query.p, query.L
            _integer(p, 'p'); _integer(L, 'L')
            if p not in primes:
                if p < 3 or p % 2 == 0 or not is_prime64(p):
                    raise BoundaryError('each p must be an odd prime less than 2**64')
                primes.add(p)
            if not 0 <= L < p:
                raise BoundaryError('each index requires 0 <= L < p')
            wanted.append(query)
        unique = sorted(set(wanted), key=lambda q: (q.L, q.p))
        schedule = self._schedule(unique, chunks)
        n, size = len(unique), schedule['chunk_size']
        modulus_bound = schedule['remaining_modulus_bits_bound']
        last = schedule['max_cutoff']
        largest_span = schedule['largest_chunk_steps_bound']
        largest_entry_bound = schedule['largest_chunk_entry_bits_bound']
        if engine == 'forest':
            self._check_forest(schedule)
        return wanted, unique, size, {
            'version': __version__, 'engine': engine, 'output_mode': output_mode,
            'independent_boundary_backend': backend,
            'requested_queries': len(wanted), 'unique_queries': n, 'unique_primes': len(primes),
            'canonical_order': ('increasing (L,p)' if engine == 'forest' else
                                'prime groups in first (L,p) encounter order, then L'),
            'chunks_requested': chunks,
            'chunks_used': 0, 'carry_updates': 0, 'recurrence_steps': 0,
            'max_cutoff': last, 'largest_chunk_steps_bound': largest_span,
            'remaining_modulus_bits_bound': modulus_bound,
            'largest_chunk_entry_bits_bound': largest_entry_bound,
            'largest_remaining_modulus_bits': 0, 'largest_chunk_modulus_bits': 0,
            'largest_exact_chunk_entry_bits': 0,
            'native_third_primes': 0, 'native_fifth_primes': 0, 'reference_queries': 0,
            'preparation_seconds': perf_counter() - begin, 'execution_seconds': 0.0,
            'complete': False, 'rows_emitted': 0, 'answer_cache_used': False,
            'memory_note': 'Integer bit counts/bounds, not RSS or total Python memory. '
                           'The scheduler retains request metadata; streaming keeps one forest chunk of residues.',
        }

    @staticmethod
    def _schedule(unique, chunks):
        n = len(unique)
        size = (n + min(chunks, n) - 1) // min(chunks, n) if n else 1
        last, largest_span, largest_entry_bound = 0, 0, 0
        for lo in range(0, n, size):
            end = unique[min(lo + size, n) - 1].L
            span = end - last
            bound = span * (4 * max(1, end)).bit_length() + 2
            largest_span = max(largest_span, span)
            largest_entry_bound = max(largest_entry_bound, bound)
            last = end
        return {'chunk_size': size, 'max_cutoff': last,
                'largest_chunk_steps_bound': largest_span,
                'remaining_modulus_bits_bound': sum(q.p.bit_length() for q in unique),
                'largest_chunk_entry_bits_bound': largest_entry_bound}

    def _check_forest(self, schedule):
        if schedule['max_cutoff'] > self.max_forest_index:
            raise ResourceLimitError('forest cutoff exceeds max_forest_index')
        if schedule['remaining_modulus_bits_bound'] > self.max_modulus_bits:
            raise ResourceLimitError('remaining-modulus bit bound exceeds max_modulus_bits')
        if schedule['largest_chunk_entry_bits_bound'] > self.max_chunk_product_bits:
            raise ResourceLimitError('exact chunk-entry bit bound exceeds max_chunk_product_bits')

    def _prepare_dispatch(self, queries, engine, chunks, backend, modulus_power,
                          output_mode, profile, collection):
        begin = perf_counter()
        if engine != 'auto':
            wanted, unique, size, stats = self._prepare(
                queries, engine, chunks, backend, modulus_power, output_mode)
            stats['dispatch'] = {'status': 'explicit_override', 'reason': 'explicit_engine',
                                 'selected_engine': engine, 'selected_backend': backend,
                                 'selected_chunks': chunks}
            return wanted, unique, size, stats
        # Validate once, without applying forest-only caps to the request.
        wanted, unique, size, stats = self._prepare(
            queries, 'independent', chunks, backend, modulus_power, output_mode)
        from dispatch_profile import select
        decision = select(self, wanted, unique, profile=profile, backend=backend,
                          output_mode=output_mode, collection=collection, chunks=chunks)
        selected = decision['selected_engine']
        schedule = self._schedule(unique, decision['selected_chunks'])
        if selected == 'forest':
            self._check_forest(schedule)
        stats.update({k: v for k, v in schedule.items() if k != 'chunk_size'})
        stats.update(engine=selected, independent_boundary_backend=decision['selected_backend'],
                     chunks_requested=decision['selected_chunks'], dispatch=decision,
                     preparation_seconds=perf_counter() - begin,
                     canonical_order=('increasing (L,p)' if selected == 'forest' else
                                      'prime groups in first (L,p) encounter order, then L'))
        return wanted, unique, schedule['chunk_size'], stats

    @staticmethod
    def _row(query, B, a, mode, method, status='computed'):
        p, L = query.p, query.L
        coefficient = 2 * L * (2 * L + 5) % p
        return {'p': p, 'L': L, 'B_L': B if mode == 'full' else None,
                'a_L': a if mode == 'full' else None,
                'U_p_L': (4 * B - coefficient * a) % p,
                'boundary_multiplier': coefficient, 'boundary_status': status,
                'method': method}

    def _forest_rows(self, unique, size, mode, stats):
        if not unique:
            return
        remaining = retained.balanced_product([q.p for q in unique])
        stats['largest_remaining_modulus_bits'] = remaining.bit_length()
        carry, last_L = (1, 0, 1), 0
        for lo in range(0, len(unique), size):
            selected = unique[lo:lo + size]
            leaves = []
            for query in selected:
                leaves.append(retained.interval_product(last_L, query.L))
                last_L = query.L
            moduli = [query.p for query in selected]
            current = retained.balanced_product(moduli)
            residues, top = retained.remainder_tree(leaves, moduli, retained.reduce_matrix(carry, current))
            remaining, rem = divmod(remaining, current)
            if rem:
                raise ArithmeticError('remaining modulus not divisible by current chunk')
            if remaining != 1:
                carry = retained.reduce_matrix(retained.mul(top, carry), remaining)
                stats['carry_updates'] += 1
            stats['chunks_used'] += 1
            stats['recurrence_steps'] = last_L
            stats['largest_chunk_modulus_bits'] = max(stats['largest_chunk_modulus_bits'], current.bit_length())
            stats['largest_exact_chunk_entry_bits'] = max(stats['largest_exact_chunk_entry_bits'],
                                                         *(entry.bit_length() for entry in top))
            del leaves, moduli, top
            for query, matrix in zip(selected, residues):
                denominator, cleared_B, cleared_a = matrix
                inverse = pow(denominator, -1, query.p)
                B, a = cleared_B * inverse % query.p, cleared_a * inverse % query.p
                yield self._row(query, B, a, mode, 'forest', 'computed_jointly')

    def _independent_rows(self, unique, backend, mode, stats):
        groups = {}
        for query in unique:
            groups.setdefault(query.p, []).append(query.L)
        for p, indices in groups.items():
            third = ((p - 1) // 3 if p % 3 == 1 else (p + 1) // 3) if p >= 7 else None
            fifth = ((p + 1) // 5, 2 * (p + 1) // 5) if p >= 19 and p % 5 == 4 else ()
            results = {}
            if third in indices:
                result = ThirdPointSession(p, **self.kernel_options).evaluate(backend=backend, output_mode=mode)
                results[third] = {key: result[key] for key in
                                  ('p', 'L', 'B_L', 'a_L', 'U_p_L', 'boundary_multiplier', 'boundary_status')}
                results[third]['method'] = 'native_third'
                stats['native_third_primes'] += 1
            selected = [L for L in indices if L in fifth]
            if selected:
                result = FifthPointSession(p, **self.kernel_options).evaluate(selected, backend=backend, output_mode=mode)
                for row in result['outputs']:
                    results[row['L']] = {'p': p, **row, 'method': 'native_fifth'}
                    results[row['L']].setdefault('boundary_status', 'computed')
                stats['native_fifth_primes'] += 1
            other = [L for L in indices if L not in results]
            if other:
                provider = DirectReferencePrefix(self.kernel_options['max_direct_terms'])
                result = BoundaryBatchSession(p, **self.kernel_options).complete_many(
                    other, provider, backend=backend, output_mode=mode)
                for row in result['outputs']:
                    results[row['L']] = {'p': p, **row, 'method': 'direct_reference_prefix'}
                stats['reference_queries'] += len(other)
            for L in indices:
                yield results[L]

    def _run(self, unique, size, engine, backend, mode, stats):
        source = (self._forest_rows(unique, size, mode, stats) if engine == 'forest'
                  else self._independent_rows(unique, backend, mode, stats))
        # Charge arithmetic time but exclude time spent paused in the consumer.
        iterator = iter(source)
        try:
            while True:
                begin = perf_counter()
                try:
                    row = next(iterator)
                except StopIteration:
                    stats['execution_seconds'] += perf_counter() - begin
                    break
                stats['execution_seconds'] += perf_counter() - begin
                stats['rows_emitted'] += 1
                yield row
            stats['complete'] = True
        finally:
            iterator.close()
            stats['total_seconds'] = stats['preparation_seconds'] + stats['execution_seconds']

    def iter_evaluate(self, queries, *, engine='forest', chunks=32, backend='auto',
                      modulus_power=1, output_mode='full', stats=None, profile=None):
        """Stream each unique result; forest order is (L,p), independent is grouped by prime.

        Validation is eager. Only the forest promises chunk-bounded arithmetic
        output storage. stats['complete'] remains false after early cancellation.
        """
        if stats is not None and not isinstance(stats, dict):
            raise BoundaryError('stats must be a dict')
        wanted, unique, size, record = self._prepare_dispatch(
            queries, engine, chunks, backend, modulus_power, output_mode, profile, 'streaming')
        record['result_collection'] = 'streamed unique outputs'
        if stats is not None:
            stats.clear(); stats.update(record); record = stats
        del wanted
        return self._run(unique, size, record['engine'], record['independent_boundary_backend'], output_mode, record)

    def evaluate(self, queries, *, engine='forest', chunks=32, backend='auto',
                 modulus_power=1, output_mode='full', profile=None):
        """Collect results in original request order, preserving duplicates."""
        begin = perf_counter()
        wanted, unique, size, stats = self._prepare_dispatch(
            queries, engine, chunks, backend, modulus_power, output_mode, profile, 'collected')
        results = {(row['p'], row['L']): row
                   for row in self._run(unique, size, stats['engine'], stats['independent_boundary_backend'], output_mode, stats)}
        outputs = [dict(results[(query.p, query.L)]) for query in wanted]
        stats['result_collection'] = 'collected in original request order; duplicates preserved'
        stats['total_seconds'] = perf_counter() - begin
        return {'version': __version__, 'outputs': outputs, 'statistics': stats}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--bound', type=int)
    source.add_argument('--queries', nargs='*', help='explicit p:L pairs')
    parser.add_argument('--family', choices=('thirds', 'ordinary_third', 'rounded_third', 'fifths'), default='thirds')
    parser.add_argument('--engine', choices=('forest', 'independent', 'auto'), default='forest')
    parser.add_argument('--profile', type=Path, help='local calibration profile for --engine auto')
    parser.add_argument('--chunks', type=int, default=32)
    parser.add_argument('--backend', choices=('auto', 'direct', 'product_tree', 'bgs'), default='auto')
    parser.add_argument('--output-mode', choices=('full', 'u_only'), default='full')
    parser.add_argument('--modulus-power', type=int, default=1)
    parser.add_argument('--max-bound', type=int, default=2_000_000)
    parser.add_argument('--max-queries', type=int, default=100_000)
    parser.add_argument('--max-forest-index', type=int, default=2_000_000)
    parser.add_argument('--max-modulus-bits', type=int, default=2_000_000)
    parser.add_argument('--max-chunk-product-bits', type=int, default=32_000_000)
    parser.add_argument('--out', type=Path, help='stream unique results to CSV, instead of collecting JSON outputs')
    args = parser.parse_args(argv)
    try:
        generation_start = perf_counter()
        if args.bound is not None:
            queries = range_queries(args.bound, args.family, max_bound=args.max_bound)
        else:
            queries = []
            for value in args.queries:
                try:
                    p, L = map(int, value.split(':'))
                except ValueError as exc:
                    raise BoundaryError('queries must be p:L pairs') from exc
                queries.append(PrimeQuery(p, L))
        generation = perf_counter() - generation_start
        evaluator = ManyPrimeEvaluator(max_queries=args.max_queries, max_forest_index=args.max_forest_index,
                                       max_modulus_bits=args.max_modulus_bits,
                                       max_chunk_product_bits=args.max_chunk_product_bits)
        options = dict(engine=args.engine, chunks=args.chunks, backend=args.backend,
                       output_mode=args.output_mode, modulus_power=args.modulus_power, profile=args.profile)
        if args.out is None:
            result = evaluator.evaluate(queries, **options)
            result['statistics']['query_generation_seconds'] = generation
            print(json.dumps(result, indent=2))
        else:
            stats = {}
            rows = evaluator.iter_evaluate(queries, stats=stats, **options)
            # Validation happens before any output file is opened. Stage the
            # CSV next to its destination and replace only on full success.
            import tempfile
            temporary = None
            try:
                with tempfile.NamedTemporaryFile('w', encoding='utf-8', newline='',
                                                 dir=args.out.resolve().parent, delete=False) as stream:
                    temporary = Path(stream.name)
                    writer = csv.DictWriter(stream, fieldnames=('p', 'L', 'B_L', 'a_L', 'U_p_L'))
                    writer.writeheader()
                    for row in rows:
                        writer.writerow({key: row[key] for key in writer.fieldnames})
                temporary.replace(args.out)
            finally:
                rows.close()
                if temporary is not None and temporary.exists():
                    temporary.unlink()
            stats['query_generation_seconds'] = generation
            print(json.dumps({'version': __version__, 'output_csv': str(args.out), 'statistics': stats}, indent=2))
        return 0
    except (BoundaryError, OSError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
