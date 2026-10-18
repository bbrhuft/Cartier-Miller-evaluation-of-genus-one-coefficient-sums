"""Matched shared-boundary benchmark: separate, exact reuse, adjacent reuse."""
import argparse
import csv
import json
from pathlib import Path
import platform
from statistics import median
import sys
from time import perf_counter

from boundary_framework import __version__
from shared_boundaries import BoundaryBatchSession


def recurrence_boundaries(p, indices):
    """One independent denominator-cleared a recurrence, not ratio plans."""
    wanted = set(indices)
    values = {0: 1}
    numerator, denominator = 1, 1
    for i in range(max(wanted, default=0)):
        numerator = numerator * (2 * i + 1) % p
        denominator = denominator * (4 * (i + 1)) % p
        if i + 1 in wanted:
            values[i + 1] = numerator * pow(denominator, -1, p) % p
    return [values[n] for n in indices]


def run(repeats=3, output=Path('results')):
    output.mkdir(exist_ok=True, parents=True)
    rows = []
    cases = []
    for p in (100019, 1000039, 10000019):
        cases.append(('nearby16', p, [p // 10 + j for j in range(16)]))
        third = (p - 1) // 3 if p % 3 == 1 else (p + 1) // 3
        ell = (p + 1) // 10
        cases.append(('mixed_third_fifths_generic', p, [ell, 2 * ell, 4 * ell, third]))
    cases.append(('small_mixed', 59, [6, 12, 24, 20]))
    for label, p, indices in cases:
        expected = recurrence_boundaries(p, indices)
        for backend in ('auto', 'bgs'):
            for mode in ('separate', 'exact', 'adjacent'):
                for repeat in range(repeats):
                    begin = perf_counter()
                    session = BoundaryBatchSession(p)
                    if mode == 'separate':
                        results = [session.evaluate([n], backend=backend, sharing='exact') for n in indices]
                        values = [result['values'][0] for result in results]
                        acquisitions = sum(result['product_acquisitions'] for result in results)
                        inversions = sum(result['denominator_inversions'] for result in results)
                    else:
                        result = session.evaluate(indices, backend=backend, sharing=mode)
                        values = result['values']
                        acquisitions = result['product_acquisitions']
                        inversions = result['denominator_inversions']
                    elapsed = perf_counter() - begin
                    if values != expected:
                        raise RuntimeError(f'wrong result: {label}, {backend}, {mode}')
                    rows.append(dict(case=label, p=p, requests=len(indices), backend=backend,
                                     mode=mode, repeat=repeat, seconds=elapsed,
                                     product_acquisitions=acquisitions,
                                     denominator_inversions=inversions, correct=True))
    groups = []
    for key in dict.fromkeys((r['case'], r['p'], r['backend'], r['mode']) for r in rows):
        members = [r for r in rows if (r['case'], r['p'], r['backend'], r['mode']) == key]
        groups.append(dict(zip(('case', 'p', 'backend', 'mode'), key),
                           median_seconds=median(r['seconds'] for r in members),
                           product_acquisitions=members[0]['product_acquisitions'],
                           denominator_inversions=members[0]['denominator_inversions']))
    with (output / 'shared_benchmark.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    record = dict(version=__version__, python=sys.version, platform=platform.platform(),
                  repeats=repeats, evaluations=len(rows), all_correct=True, medians=groups,
                  oracle='One independent denominator-cleared a recurrence through the largest requested index.',
                  scope='Boundary values only. All modes construct one validated session per timed sample. '
                        'Separate reuses that validated session but recomputes arithmetic independently for each index. '
                        'All modes receive the same unique indices and matching reductions. No prefix work, '
                        'persistent answer cache, imports, prime selection, reference generation or JSON serialization.',
                  interpretation='Adjacent sharing reduces prefix-product lengths and can reuse exact gap intervals. '
                                 'It is a deterministic heuristic; no universal speedup or optimal partition is claimed.')
    (output / 'shared_benchmark_summary.json').write_text(json.dumps(record, indent=2) + '\n')
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
