"""Matched cold BGS/direct/product-tree benchmarks and independent oracles."""
import argparse
import csv
import json
from pathlib import Path
import platform
from statistics import median
import sys
from time import perf_counter

from boundary_framework import (
    BGSFactorialBackend, DirectFactorialBackend, ProductTreeFactorialBackend,
    BoundaryEvaluator, __version__,
)
from integrated_fifths import FifthPointSession, IntervalProductEvaluator
from integrated_thirds import ThirdPointSession
from benchmark_fifths import original_pair_shared
from benchmark_integrated import original_sum_scaled


def direct_product(p, start, length):
    value = 1
    for j in range(start, start + length):
        value = value * j % p
    return value


def run(repeats=3, output=Path('results')):
    output.mkdir(exist_ok=True, parents=True)
    rows = []

    def measure(kind, p, length, backend, call, expected):
        for repeat in range(repeats):
            begin = perf_counter()
            actual = call()
            elapsed = perf_counter() - begin
            if actual != expected:
                raise RuntimeError(f'incorrect result: {kind}, {p}, {length}, {backend}')
            rows.append(dict(kind=kind, p=p, length=length, backend=backend,
                             repeat=repeat, seconds=elapsed, correct=True))

    cases = [(100000007, n) for n in
             (100, 1000, 10000, 32768, 65536, 262144, 333334, 3333339, 33333335)]
    cases += [(p, n) for p in (4294967291, 18446744073709551557)
              for n in (10000, 262144, 333334)]
    for p, n in cases:
        for kind in ('factorial', 'shifted_interval'):
            start = 1 if kind == 'factorial' else p - n
            expected = direct_product(p, start, n)
            for backend in ('direct', 'product_tree', 'bgs'):
                if kind == 'factorial':
                    cls = {'direct': DirectFactorialBackend,
                           'product_tree': ProductTreeFactorialBackend,
                           'bgs': BGSFactorialBackend}[backend]
                    def call(cls=cls, p=p, n=n):
                        engine = cls(50_000_000) if cls is DirectFactorialBackend else cls()
                        return engine.factorial(n, p).value
                else:
                    def call(p=p, start=start, n=n, backend=backend):
                        return IntervalProductEvaluator(max_direct_terms=50_000_000).product(
                            p, start, n, backend).value
                measure(kind, p, n, backend, call, expected)

    for p in (100003, 1000037, 10000019):
        L = (p - 1) // 3 if p % 3 == 1 else (p + 1) // 3
        expected = original_sum_scaled(p, L)
        for backend in ('direct', 'product_tree', 'bgs', 'auto'):
            def call(p=p, backend=backend):
                return ThirdPointSession(p, max_direct_terms=50_000_000).evaluate(
                    backend=backend, boundary_policy='factorial')['U_p_L']
            measure('complete_third_forced_factorial', p, L, backend, call, expected)
    for p in (100019, 1000039, 10000019):
        L = (p + 1) // 5
        expected = original_pair_shared(p, (L, 2 * L))
        for backend in ('direct', 'product_tree', 'bgs', 'auto'):
            def call(p=p, backend=backend):
                result = FifthPointSession(p, max_direct_terms=50_000_000).evaluate(backend=backend)
                return [row['U_p_L'] for row in result['outputs']]
            measure('complete_fifth_pair', p, L, backend, call, expected)

    medians = []
    for key in dict.fromkeys((r['kind'], r['p'], r['length'], r['backend']) for r in rows):
        group = [r['seconds'] for r in rows
                 if (r['kind'], r['p'], r['length'], r['backend']) == key]
        medians.append(dict(zip(('kind', 'p', 'length', 'backend'), key),
                            median_seconds=median(group)))
    with (output / 'bgs_benchmark.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    record = dict(version=__version__, python=sys.version, platform=platform.platform(),
                  repeats=repeats, evaluations=len(rows), all_correct=True, medians=medians,
                  scope='Cold API calls including construction, arithmetic and validation where offered; '
                        'imports, reference generation, serialization excluded. No persistent cache. '
                        'Factorial and interval low-level APIs expect an already validated prime. '
                        'Complete third cases force factorial acquisition for all backends.',
                  oracles='Independent sequential product for kernels; original scaled t recurrence '
                          'for complete U, shared single pass for the fifth pair.',
                  auto_policy='Direct up to 262144 effective terms, BGS above; explicit product_tree retained. '
                              'Conservative configurable threshold, not a universal optimum.')
    (output / 'bgs_benchmark_summary.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'medians'}, indent=2))
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--output', type=Path, default=Path('results'))
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error('--repeats must be positive')
    run(args.repeats, args.output)
