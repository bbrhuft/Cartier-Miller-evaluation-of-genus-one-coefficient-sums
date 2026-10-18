"""Fresh-process complete-output timing and separate peak-memory samples."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
from statistics import median
import subprocess
import sys
from time import perf_counter

from boundary_framework import __version__
from many_primes import ManyPrimeEvaluator, PrimeQuery, range_queries


def queries_for(case, bound):
    if case == 'sparse':
        return [PrimeQuery(10007, 3336), PrimeQuery(100003, 33334), PrimeQuery(1000037, 333346)]
    return range_queries(bound, case)


def fingerprint(rows):
    digest = hashlib.sha256()
    for row in rows:
        digest.update((','.join(str(row[k]) for k in ('p', 'L', 'B_L', 'a_L', 'U_p_L')) + '\n').encode())
    return digest.hexdigest()


def reference(queries):
    """Definition-level scaled coefficient and original t recurrences."""
    groups, results = {}, {}
    for query in queries:
        groups.setdefault(query.p, set()).add(query.L)
    for p, indices in groups.items():
        A, B, C = 1, 0, 1
        T, S, D = 1, 0, 1
        h = (p - 1) // 2
        if 0 in indices:
            results[p, 0] = (0, 1, 0)
        for i in range(max(indices)):
            four, two = 4 * (i + 1) % p, 2 * (i + 1) % p
            A, B, C = A * (2 * i + 1) % p, (B + A) * four % p, C * four % p
            T, S, D = T * (h + 2 + i) % p, (S + (h + 1 + i) * T) * two % p, D * two % p
            if i + 1 in indices:
                inverse = pow(C, -1, p)
                results[p, i + 1] = (B * inverse % p, A * inverse % p, S * pow(D, -1, p) % p)
    return [{'p': q.p, 'L': q.L, 'B_L': results[q.p, q.L][0],
             'a_L': results[q.p, q.L][1], 'U_p_L': results[q.p, q.L][2]} for q in queries]


def worker(case, bound, engine, chunks, memory=False):
    if memory:
        import tracemalloc
        tracemalloc.start()
    begin = perf_counter()
    queries = queries_for(case, bound)
    generation = perf_counter() - begin
    result = ManyPrimeEvaluator().evaluate(queries, engine=engine, chunks=chunks)
    elapsed = perf_counter() - begin
    python_peak = None
    if memory:
        _, python_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    rss = None
    try:
        import resource
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss = int(peak if sys.platform == 'darwin' else 1024 * peak)
    except ImportError:
        pass
    stats = result['statistics']
    return dict(case=case, bound=bound, engine=engine, chunks=chunks, phase='memory' if memory else 'timing',
                seconds=elapsed, query_generation_seconds=generation, rows=len(result['outputs']),
                fingerprint=fingerprint(result['outputs']), python_peak_bytes=python_peak,
                process_peak_rss_bytes=rss, chunks_used=stats['chunks_used'],
                carry_updates=stats['carry_updates'], recurrence_steps=stats['recurrence_steps'],
                largest_remaining_modulus_bits=stats['largest_remaining_modulus_bits'],
                largest_exact_chunk_entry_bits=stats['largest_exact_chunk_entry_bits'],
                native_third_primes=stats['native_third_primes'], native_fifth_primes=stats['native_fifth_primes'])


def run(repeats=3, bound=20000, output=Path('results')):
    output.mkdir(exist_ok=True, parents=True)
    rows, groups = [], []
    for case in ('rounded_third', 'thirds', 'fifths', 'sparse'):
        queries = queries_for(case, bound)
        expected = fingerprint(reference(queries))
        for engine, chunks in (('independent', 32), ('forest', 1), ('forest', 8), ('forest', 32)):
            members = []
            for repeat in range(repeats + 1):
                memory = repeat == repeats
                command = [sys.executable, str(Path(__file__).resolve()), '--worker', '--case', case,
                           '--bound', str(bound), '--engine', engine, '--chunks', str(chunks)]
                if memory:
                    command.append('--memory')
                completed = subprocess.run(command, capture_output=True, text=True, check=True)
                record = json.loads(completed.stdout)
                if record['fingerprint'] != expected:
                    raise RuntimeError(f'full-output reference mismatch: {case}, {engine}, {chunks}')
                record.update(repeat=repeat, correct=True)
                rows.append(record)
                members.append(record)
            timings = [r for r in members if r['phase'] == 'timing']
            measured = members[-1]
            groups.append(dict(case=case, bound=bound, engine=engine, chunks=chunks,
                               rows=len(queries), median_seconds=median(r['seconds'] for r in timings),
                               python_peak_bytes=measured['python_peak_bytes'],
                               process_peak_rss_bytes=measured['process_peak_rss_bytes'],
                               chunks_used=measured['chunks_used'], carry_updates=measured['carry_updates'],
                               recurrence_steps=measured['recurrence_steps'],
                               largest_remaining_modulus_bits=measured['largest_remaining_modulus_bits'],
                               largest_exact_chunk_entry_bits=measured['largest_exact_chunk_entry_bits']))
    with (output / 'many_prime_benchmark.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    record = dict(version=__version__, python=sys.version, platform=platform.platform(),
                  repeats=repeats, evaluations=len(rows), timed_evaluations=16 * repeats,
                  memory_evaluations=16, all_correct=True, medians=groups,
                  scope='Complete B,a,U outputs, collected in request order. Each sample runs in a fresh process. '
                        'Timing includes query generation, validation, forest or native prefix/boundary work, and '
                        'result collection; imports, canonical fingerprinting and serialization excluded.',
                  memory='Separate untimed tracemalloc runs; traced Python allocation peak excludes imports, '
                         'RSS when available is whole-process high water including imports. '
                         'Both include collected result storage; neither is a claim about streaming peak memory.',
                  oracle='Full ordered output fingerprints against independent scaled coefficient and original t '
                         'recurrences. Tests separately check exact binomial values and retained forest agreement.',
                  comparison='Independent uses native thirds and paired fifth work. Forest reuses the retained '
                             'integer recurrence kernels with a mixed-prime scheduler. Sparse cases deliberately '
                             'show that the forest is not always the faster route.')
    (output / 'many_prime_benchmark_summary.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'medians'}, indent=2))
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--memory', action='store_true')
    parser.add_argument('--case', choices=('rounded_third', 'thirds', 'fifths', 'sparse'))
    parser.add_argument('--engine', choices=('forest', 'independent'), default='forest')
    parser.add_argument('--chunks', type=int, default=32)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--bound', type=int, default=20000)
    parser.add_argument('--output', type=Path, default=Path('results'))
    args = parser.parse_args()
    if args.repeats < 1 or args.bound < 0:
        parser.error('repeats must be positive and bound nonnegative')
    if args.worker:
        print(json.dumps(worker(args.case, args.bound, args.engine, args.chunks, args.memory)))
    else:
        run(args.repeats, args.bound, args.output)
