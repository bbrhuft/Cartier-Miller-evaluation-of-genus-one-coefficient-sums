"""Round-2 matched cold benchmarks, run only after CONFIRMATION_CHARP.json is PASS.

Every method returns c_p from p alone, with all setup, class numbers and normalization
inside the timed region. Five samples per method, order rotated. Writes
evidence/charp/BENCHMARK_CHARP.json.
"""
import json
import platform
import statistics
import sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
from confirm import verify_freeze
from confirm_charp import verify_freeze_charp, pari_classno
from atkin import nodal_c, factorial_c, parameters
from charp import classno, halfinterval_c
from flint_backend import flint_factorial, flint_rising, flint_version

ROOT = Path(__file__).resolve().parent


def flint_native_c(p):
    m = (p - 2) // 3
    g = flint_factorial(m, p)
    return 2 * pow(g, 3 * (p - 2), p) % p, dict(backend='flint n_factorial_fast_mod2_preinv')


def flint_block_factorial_c(p):
    m = (p - 2) // 3
    (g,), meta = flint_rising(p, m, [1])
    return 2 * pow(g, 3 * (p - 2), p) % p, meta


def flint_nodal_c(p):
    N, _, _ = parameters(p)
    inv3 = pow(3, p - 2, p)
    chi = 1 if pow(6, (p - 1) // 2, p) == 1 else p - 1
    (num, den), meta = flint_rising(p, N, [4 * inv3 % p, 1])
    return -4 * inv3 * chi * pow(-1, N, p) * num * pow(den, p - 2, p) % p, meta


def main():
    verify_freeze()
    verify_freeze_charp()
    conf = json.loads((ROOT / 'evidence/charp/CONFIRMATION_CHARP.json').read_text())
    assert conf['status'] == 'PASS'
    pari, pari_name = pari_classno()
    primes = sorted(q for v in conf['selection']['large'].values() for q in v)
    out = dict(python=sys.version, platform=platform.platform(), flint=flint_version(),
               pari=pari_name, samples_per_method=5, status='PASS',
               scope='Matched generic block engines (stdlib and FLINT multipoint); FLINT native factorial; '
                     'no BGS shifting, no batch methods', rows=[])
    for p in primes:
        methods = []
        if p <= 2 * 10 ** 9:
            methods += [('std_factorial_block', lambda p: factorial_c(p, 'block')),
                        ('std_nodal_shared', lambda p: nodal_c(p, 'shared')),
                        ('std_hi1_forms', lambda p: halfinterval_c(p, layout=1)),
                        ('std_hi2_forms', lambda p: halfinterval_c(p, layout=2))]
        methods += [('flint_native_factorial', flint_native_c),
                    ('flint_block_factorial', flint_block_factorial_c),
                    ('flint_nodal_shared', flint_nodal_c),
                    ('flint_hi1_forms', lambda p: halfinterval_c(p, layout=1, product_fn=flint_rising))]
        if pari:
            methods += [('flint_hi1_pari', lambda p: halfinterval_c(p, layout=1, product_fn=flint_rising, classno_fn=pari)),
                        ('flint_hi2_pari', lambda p: halfinterval_c(p, layout=2, product_fn=flint_rising, classno_fn=pari))]
        samples = {n: [] for n, _ in methods}
        answers, meta = set(), {}
        for rep in range(5):
            order = methods[rep % len(methods):] + methods[:rep % len(methods)]
            for name, fn in order:
                t = perf_counter()
                c, md = fn(p)
                samples[name].append(perf_counter() - t)
                answers.add(c)
                meta[name] = md
        assert len(answers) == 1
        # class-number cost alone (same D as the HI route), for transparency
        D = -p if p % 4 == 3 else (-4 * p if p % 8 == 5 else -3 * p)
        cls = {}
        for lab, fn in [('forms', classno)] + ([('pari', pari)] if pari else []):
            ts = []
            for _ in range(5):
                t = perf_counter(); fn(D); ts.append(perf_counter() - t)
            cls[lab] = dict(samples_s=ts, median_s=statistics.median(ts))
        med = {n: statistics.median(v) for n, v in samples.items()}
        row = dict(p=p, p_class=('A' if p % 12 == 11 else ('B' if p % 24 == 5 else 'C')), c=answers.pop(),
                   samples_s=samples, medians_s=med, class_number_only=dict(D=D, **cls), metadata=meta)
        out['rows'].append(row)
        print(json.dumps(dict(p=p, medians_ms={k: round(v * 1e3, 3) for k, v in med.items()},
                              classno_ms={k: round(v['median_s'] * 1e3, 3) for k, v in cls.items()})), flush=True)
    (ROOT / 'evidence/charp/BENCHMARK_CHARP.json').write_text(json.dumps(out, indent=2) + '\n')


if __name__ == '__main__':
    main()
