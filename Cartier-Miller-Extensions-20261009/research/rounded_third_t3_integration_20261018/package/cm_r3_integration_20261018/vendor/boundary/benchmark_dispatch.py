"""Real calibration plus held-out executions of measured and fallback dispatch."""
import argparse
import csv
import json
from pathlib import Path
import platform
from statistics import median
import sys
from time import perf_counter

from boundary_framework import __version__
from many_primes import ManyPrimeEvaluator, PrimeQuery, range_queries
from calibrate_dispatch import calibrate
from benchmark_many_primes import reference


def run(repeats=3, bound=20000, output=Path('results')):
    output.mkdir(exist_ok=True, parents=True)
    profile = output / 'local_dispatch_profile.json'
    evaluator = ManyPrimeEvaluator()
    cases = [('rounded_dense', range_queries(bound, 'rounded_third'), 'collected'),
             ('rounded_dense_stream', range_queries(bound, 'rounded_third'), 'streaming'),
             ('sparse', [PrimeQuery(10007, 3336), PrimeQuery(50021, 16674),
                         PrimeQuery(100003, 33334)], 'collected'),
             ('fifth_pairs', range_queries(3000, 'fifths'), 'collected')]
    samples, calibrations, groups = [], [], []
    for label, queries, collection in cases:
        record = calibrate(queries, profile, evaluator=evaluator, repeats=repeats, collection=collection)
        calibrations.append({'case': label, 'candidate_evaluations':
                             sum(len(c['samples_seconds']) for c in record['candidates']),
                             'record': record})
        expected = {(r['p'], r['L']): (r['B_L'], r['a_L'], r['U_p_L']) for r in reference(queries)}
        decision = None
        for repeat in range(repeats):
            for mode in ('auto_measured', 'explicit_selected', 'auto_untrained'):
                if mode == 'explicit_selected':
                    options = dict(engine=decision['selected_engine'], backend=decision['selected_backend'],
                                   chunks=decision['selected_chunks'])
                else:
                    options = dict(engine='auto', profile=profile if mode == 'auto_measured' else None)
                begin = perf_counter()
                if collection == 'collected':
                    result = evaluator.evaluate(queries, **options)
                    rows, stats = result['outputs'], result['statistics']
                else:
                    stats = {}
                    rows = list(evaluator.iter_evaluate(queries, stats=stats, **options))
                elapsed = perf_counter() - begin
                actual = {(r['p'], r['L']): (r['B_L'], r['a_L'], r['U_p_L']) for r in rows}
                if actual != expected or len(rows) != len(queries):
                    raise RuntimeError(f'dispatch output mismatch: {label}, {mode}')
                if mode == 'auto_measured':
                    decision = stats['dispatch']
                    if not decision['status'].startswith('measured_'):
                        raise RuntimeError(f'profile did not match: {decision}')
                samples.append(dict(case=label, collection=collection, mode=mode, repeat=repeat,
                                    seconds=elapsed, rows=len(rows), engine=stats['engine'],
                                    backend=stats['independent_boundary_backend'],
                                    chunks=stats['chunks_requested'],
                                    dispatch_status=stats['dispatch']['status'], correct=True))
        for mode in ('auto_measured', 'explicit_selected', 'auto_untrained'):
            members = [r for r in samples if r['case'] == label and r['mode'] == mode]
            groups.append(dict(case=label, collection=collection, mode=mode, rows=len(queries),
                               median_seconds=median(r['seconds'] for r in members),
                               engine=members[0]['engine'], backend=members[0]['backend'],
                               chunks=members[0]['chunks'], dispatch_status=members[0]['dispatch_status']))
    with (output / 'dispatch_benchmark.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(samples[0]))
        writer.writeheader(); writer.writerows(samples)
    result = dict(version=__version__, python=sys.version, platform=platform.platform(),
                  repeats=repeats, held_out_evaluations=len(samples),
                  calibration_evaluations=sum(c['candidate_evaluations'] for c in calibrations),
                  all_correct=True, medians=groups, calibrations=calibrations,
                  scope='Same-process complete-output calls, rotated calibration order and separate held-out '
                        'repetitions on the same calibrated workloads. No generalization to unseen inputs. '
                        'Measured auto timings include profile load, signature checks, selection and arithmetic. '
                        'Reference generation, calibration, imports and JSON/CSV writing excluded. '
                        'Streaming candidates materialize unique outputs, rather than timing disk I/O.',
                  portability='The saved profile is evidence for the generating environment only. '
                              'Calibrate a new profile on another computer; mismatches fall back explicitly.')
    (output / 'dispatch_benchmark_summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('medians', 'calibrations')}, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--bound', type=int, default=20000)
    parser.add_argument('--output', type=Path, default=Path('results'))
    args = parser.parse_args()
    if not 3 <= args.repeats <= 20:
        parser.error('repeats must be 3..20')
    run(args.repeats, args.bound, args.output)
