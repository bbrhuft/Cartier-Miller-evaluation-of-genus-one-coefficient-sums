"""Recompute the manuscript table from recorded timings; never runs benchmarks."""
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]


def check():
    path = ROOT/'historical_benchmark/results/bench/timing_samples_validated.csv'
    record = json.loads((ROOT/'verification/BENCHMARK_TABLE_SOURCE.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record['csv_sha256']
    values = defaultdict(list)
    for row in csv.DictReader(path.open(newline='')):
        if row['workload'] == 'W1' and row['stage'] == 'total' and row['status'] == 'ok':
            values[row['group'], row['method']].append(int(row['ns'])/int(row['reps'])/1e6)
    comparisons = 0
    for row in record['rows_ms']:
        group = 'b%d_d%d' % (row['bits'], row['degree'])
        for method, expected in row.items():
            if method in ('bits', 'degree'):
                continue
            actual = median(values[group, method])
            assert abs(actual-expected) < 1e-9, (group, method, actual, expected)
            comparisons += 1
    return {'status': 'PASS', 'classes': len(record['rows_ms']),
            'median_comparisons': comparisons, 'csv_sha256': record['csv_sha256'],
            'interpretation': 'recomputed historical medians; no new timing run'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
