"""Cold, sequential matched benchmarks after confirmation; all methods return c_p."""
from pathlib import Path
import json
import platform
import statistics
import sys
from time import perf_counter
from atkin import nodal_c, factorial_c
from confirm import verify_freeze

ROOT = Path(__file__).resolve().parent


def main():
    verify_freeze()
    confirmed = json.loads((ROOT/'evidence/CONFIRMATION.json').read_text())
    assert confirmed['status'] == 'PASS'
    primes = confirmed['selection']['benchmark_primes']
    methods = [
        ('factorial_linear', lambda p: factorial_c(p, 'linear')),
        ('factorial_block', lambda p: factorial_c(p, 'block')),
        ('nodal_linear', lambda p: nodal_c(p, 'linear')),
        ('nodal_separate', lambda p: nodal_c(p, 'separate')),
        ('nodal_shared', lambda p: nodal_c(p, 'shared'))]
    out = dict(python=sys.version, platform=platform.platform(), status='PASS',
               samples_per_method=5, scope='Matched standard-library generic backends, not optimized BGS/FLINT/PARI', rows=[])
    for p in primes:
        samples = {name: [] for name, _ in methods}
        metadata = {}
        answers = set()
        for repetition in range(5):
            order = methods[repetition:]+methods[:repetition]
            for name, function in order:
                start = perf_counter()
                c, meta = function(p)
                elapsed = perf_counter()-start
                answers.add(c)
                samples[name].append(elapsed)
                metadata[name] = meta
        assert len(answers) == 1
        medians = {name: statistics.median(values) for name, values in samples.items()}
        best_fact = min(medians['factorial_linear'], medians['factorial_block'])
        row = dict(p=p, c=answers.pop(), samples_s=samples, medians_s=medians,
                   speedup_vs_factorial_block=medians['factorial_block']/medians['nodal_shared'],
                   speedup_vs_best_included_factorial=best_fact/medians['nodal_shared'],
                   speedup_vs_separate_channels=medians['nodal_separate']/medians['nodal_shared'],
                   metadata=metadata)
        out['rows'].append(row)
        print(json.dumps(dict(p=p, medians_ms={k:round(v*1000,3) for k,v in medians.items()},
                              shared_vs_best_factorial=round(best_fact/medians['nodal_shared'],3))), flush=True)
    (ROOT/'evidence/BENCHMARK.json').write_text(json.dumps(out, indent=2)+'\n')


if __name__ == '__main__':
    main()
