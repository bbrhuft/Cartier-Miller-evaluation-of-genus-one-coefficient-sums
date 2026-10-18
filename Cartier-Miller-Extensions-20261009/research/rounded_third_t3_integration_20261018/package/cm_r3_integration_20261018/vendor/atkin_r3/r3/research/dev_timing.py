"""Round-3 DEVELOPMENT timings (inputs recorded; excluded from confirmation).

For S in {5e9, 5e10, 5e11} and each q in QS: the first prime p >= S with p = 5 mod 6, p = 1 mod q.
Cold calls (fresh JacobiContext / FLINT trees / form-count sieve).  The PARI interpreter object
is a process-level singleton created before timing (disclosed).  Samples rotated, all retained.
Usage: python3 r3/research/dev_timing.py OUT.json [samples]
"""
import json
import statistics
import sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from r3.common import is_prime, flint_factorial, c_from_mfact, pari, ClassNumberPolicy, params, flint_rising
from r3.tal3 import acquire, plan
from r3.halfint import halfinterval_c3

QS = [5, 7, 11, 13, 17, 23, 31, 37, 41, 47, 53, 61, 71]


def first(S, q):
    p = S
    while not (p % 6 == 5 and p % q == 1 and is_prime(p)):
        p += 1
    return p


def native(p):
    return c_from_mfact(p, flint_factorial((p - 2) // 3, p)), {}


def flint_nodal(p):
    P = params(p)
    N = P['N']
    inv3 = pow(3, p - 2, p)
    chi = 1 if pow(6, (p - 1) // 2, p) == 1 else p - 1
    (num, den), _ = flint_rising(p, N, [4 * inv3 % p, 1])
    return -4 * inv3 * chi * pow(-1, N, p) * num * pow(den, p - 2, p) % p, {}


def main(out, samples=3):
    pari()
    for q in QS:
        plan(q, 'dup6'), plan(q, 'dup12')
    unc, grh = ClassNumberPolicy('unconditional'), ClassNumberPolicy('grh')
    rows = []
    for S in (5 * 10 ** 9, 5 * 10 ** 10, 5 * 10 ** 11):
        for q in QS:
            p = first(S, q)
            ref = native(p)[0]
            meths = [('native', native), ('flint_nodal', flint_nodal),
                     ('hi_grh', lambda p: halfinterval_c3(p, grh)),
                     ('tal_dup6', lambda p, q=q: acquire(p, q, 'dup6'))]
            if p % 12 == 5:
                meths.append(('tal_dup12', lambda p, q=q: acquire(p, q, 'dup12')))
            in_range = (p if p % 4 == 3 else 3 * p) < 2 * 10 ** 10
            if in_range:
                meths.append(('hi_uncond', lambda p: halfinterval_c3(p, unc)))
            samp = {n: [] for n, _ in meths}
            metas = {}
            for rep in range(samples):
                k = rep % len(meths)
                for n, f in meths[k:] + meths[:k]:
                    t = perf_counter()
                    c, md = f(p)
                    samp[n].append(perf_counter() - t)
                    if c != ref:
                        raise AssertionError((n, p, q))
                    metas[n] = md
            if not in_range:          # one disclosed sample of the unconditional forms backend
                t = perf_counter()
                c, md = halfinterval_c3(p, unc)
                samp['hi_uncond_forms_1sample'] = [perf_counter() - t]
                assert c == ref
            med = {n: statistics.median(v) for n, v in samp.items()}
            row = dict(S=S, q=q, p=p, p_mod_12=p % 12, samples_s=samp, medians_s=med,
                       tal=dict((n, dict(timings=metas[n]['timings'], residual_lengths=metas[n]['residual_lengths'],
                                         svp=metas[n]['svp'], fallbacks=metas[n]['enumeration_fallbacks']))
                                for n in metas if n.startswith('tal')))
            rows.append(row)
            print(json.dumps(dict(p=p, q=q, ms={k: round(v * 1e3, 1) for k, v in med.items()})), flush=True)
    Path(out).write_text(json.dumps(dict(role='Round-3 development timing; inputs excluded from confirmation',
                                         samples=samples, rows=rows), indent=1) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 3)
