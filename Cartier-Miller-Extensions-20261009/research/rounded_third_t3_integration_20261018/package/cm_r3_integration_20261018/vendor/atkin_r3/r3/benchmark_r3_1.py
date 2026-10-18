"""Round-3 amendment R3.1 matched benchmarks.  Run only after CONFIRMATION_R3_1.json has status PASS.

Identical rule to r3/benchmark_r3.py (frozen), using the R3.1 modules (r3/jacobi_r31.py,
r3/acquire_r31.py) and the R3.1 confirmation selection.  WARM reuses a JacobiContextR31.

Policy (CANDIDATE_R3.md, Section "Benchmark rule").  Every method returns c_p from p (and, for
'supplied-q' methods, q), with all input-dependent work inside the timed region: eta search,
lattice reduction, certificate, van Wamelen selection, intervals, assembly, class numbers,
Cornacchia, normalisation.  COLD = fresh JacobiContext, fresh FLINT trees, the reduced-form
sieve cache cleared before every call.  Process-level, p-independent state is created before
timing and disclosed: the PARI interpreter object, the loaded FLINT library, the frozen plan
table PLANS_R3.json (each plan is still re-checked in integers inside the call).  WARM = a second
call at the same p reusing the cached Jacobi sum (amortised use at fixed p; reported separately).
Samples: 5 per method (3 for set B2), method order rotated, all samples retained.
Sets:
  B1  matched supplied-q: confirmation set L (12 primes ~4e11) and confirmation set M restricted to
      q in {5, 11, 23, 31, 47, 61, 89} (21 primes ~4e9).
  B2  p-only distribution: confirmation set E4 (30 generic primes ~2e10) and E1 (6 primes with no
      admissible q).
  B3  unconditional half-interval repair at the round-2 source primes near 2e9:
      2000000063 (A), 2000000141 (B), 2000000033 (C).
  B4  small-p crossover: per class, the first prime at or above 10^6, 10^7, 10^8 with an admissible
      q (not in the ledger), p-only API vs native.
Writes r3/evidence/BENCHMARK_R3.json.
"""
import json
import platform
import statistics
import sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from r3.common import (is_prime, params, flint_factorial, c_from_mfact, ClassNumberPolicy, flint_rising, pari)
from r3.research.ledger import excluded
from r3 import tal3
from r3.jacobi_r31 import JacobiContextR31
from r3.halfint import halfinterval_c3
from r3.acquire_r31 import acquire_aL, admissible_q, nodal_flint_c, tal_c
from r3.confirm_r3_1 import verify, first


def native(p):
    return c_from_mfact(p, flint_factorial((p - 2) // 3, p))


def block_factorial(p):
    (g,), _ = flint_rising(p, (p - 2) // 3, [1])
    return c_from_mfact(p, g)


def hi(mode):
    pol = ClassNumberPolicy(mode)
    return lambda p: halfinterval_c3(p, pol)[0]


def tal_supplied(q, anchor):
    return lambda p: tal_c(p, q, anchor)[0]


def api(mode):
    return lambda p: acquire_aL(p, mode)['c_p']


def run(p, methods, samples):
    ref = native(p)
    samp = {n: [] for n, _ in methods}
    for rep in range(samples):
        k = rep % len(methods)
        for n, f in methods[k:] + methods[:k]:
            t = perf_counter()
            c = f(p)
            samp[n].append(perf_counter() - t)
            if c != ref:
                raise AssertionError((n, p))
    return samp


def warm(p, q, anchor, samples=5):
    ctx = JacobiContextR31(p, q)
    tal3.acquire(p, q, anchor, ctx=ctx)
    ts = []
    for _ in range(samples):
        t = perf_counter()
        tal3.acquire(p, q, anchor, ctx=ctx)
        ts.append(perf_counter() - t)
    return ts


def main():
    verify('r3/FREEZE_R3.json')
    verify('r3/FREEZE_R3_1.json')
    conf = json.loads((ROOT / 'r3/evidence/CONFIRMATION_R3_1.json').read_text())
    assert conf['status'] == 'PASS'
    pari()
    sel = conf['selection']
    rows = []

    def record(setname, p, q, samp, extra=None):
        med = {n: statistics.median(v) for n, v in samp.items()}
        row = dict(set=setname, p=p, cls='A' if p % 12 == 11 else ('B' if p % 24 == 5 else 'C'), q=q,
                   samples_s=samp, medians_s=med, **(extra or {}))
        rows.append(row)
        print(json.dumps(dict(set=setname, p=p, q=q, ms={k: round(v * 1e3, 1) for k, v in med.items()})), flush=True)

    # B1
    b1 = [(p, int(q)) for X in sel['L'] for q, p in sel['L'][X].items()]
    b1 += [(p, int(q)) for X in sel['M'] for q, p in sel['M'][X].items() if int(q) in (5, 11, 23, 31, 47, 61, 89)]
    for p, q in b1:
        D = p if p % 4 == 3 else 3 * p
        meths = [('native', native), ('block_factorial', block_factorial), ('nodal_flint', nodal_flint_c),
                 ('hi_grh', hi('grh')), ('tal_dup6', tal_supplied(q, 'dup6'))]
        if p % 12 == 5:
            meths.append(('tal_dup12', tal_supplied(q, 'dup12')))
        meths.append(('api_unconditional', api('unconditional')))
        if D < 2 * 10 ** 10:
            meths.append(('hi_uncond_qfb', hi('unconditional')))
        samp = run(p, meths, 5)
        if D >= 2 * 10 ** 10:
            t = perf_counter()
            assert hi('forms')(p) == native(p)
            samp['hi_uncond_forms_1sample'] = [perf_counter() - t]
        an = tal3.default_anchor(p)
        record('B1', p, q, samp, dict(tal_warm_default_anchor_s=warm(p, q, an), default_anchor=an,
                                      api_route=acquire_aL(p)['route'], api_q=acquire_aL(p)['q']))
    # B2
    for X in sel['E4']:
        for p in sel['E4'][X] + sel['E1'][X]:
            meths = [('native', native), ('nodal_flint', nodal_flint_c), ('hi_grh', hi('grh')),
                     ('api_unconditional', api('unconditional'))]
            samp = run(p, meths, 3)
            r = acquire_aL(p)
            record('B2', p, r['q'], samp, dict(api_route=r['route'], admissible=admissible_q(p),
                                               generic=p in sel['E4'][X]))
    # B3
    for p in (2000000063, 2000000141, 2000000033):
        meths = [('native', native), ('nodal_flint', nodal_flint_c), ('hi_uncond_qfb', hi('unconditional')),
                 ('hi_grh', hi('grh')), ('hi_forms_cold', hi('forms')), ('api_unconditional', api('unconditional'))]
        samp = run(p, meths, 5)
        r = acquire_aL(p)
        record('B3', p, r['q'], samp, dict(api_route=r['route'], admissible=admissible_q(p)))
    # B4
    for X, (mo, rr) in {'A': (12, 11), 'B': (24, 5), 'C': (24, 17)}.items():
        for e in (6, 7, 8):
            p = first(10 ** e, mo, rr, lambda p: bool(admissible_q(p)))[0]
            meths = [('native', native), ('api_unconditional', api('unconditional')),
                     ('nodal_flint', nodal_flint_c)]
            samp = run(p, meths, 5)
            r = acquire_aL(p)
            record('B4', p, r['q'], samp, dict(api_route=r['route']))
    out = dict(status='PASS', python=sys.version, platform=platform.platform(),
               note='single machine; timings are not universal speed ratios', rows=rows)
    (ROOT / 'r3/evidence/BENCHMARK_R3_1.json').write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
