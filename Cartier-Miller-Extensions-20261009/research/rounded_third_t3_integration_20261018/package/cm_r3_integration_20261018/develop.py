"""Pre-freeze integration development and meaningful interface/failure checks."""
import json
from pathlib import Path
from time import perf_counter
from unittest.mock import patch

from integrated import evaluate, compact, full_tuple, forest_rows, check_domain
from oracles import direct, integer_binomial
from retained_cm.rounded_third_batch import branch_primes
from r3.common import flint_factorial
import independent_elliptic_prefix as independent


def run():
    t = perf_counter()
    ps = branch_primes(20000)
    counts = dict(primes=len(ps), full_definition_checks=0, independent_prefix_checks=0,
                  integer_binomial_checks=0, forced_t3_checks=0)
    expected = []
    for p in ps:
        d = direct(p)
        truth = tuple(d[k] for k in ('p', 'B_L', 'a_L', 'U_p_L'))
        for method in ('auto', 'native', 'nodal'):
            r = evaluate(p, method)
            if compact(r) != truth or r['U_p_m'] != d['U_p_m']:
                raise AssertionError((p, method))
            counts['full_definition_checks'] += 1
        if r['B_L'] != independent.third(p)['B']:
            raise AssertionError(('independent prefix', p))
        counts['independent_prefix_checks'] += 1
        if r['a_L'] != integer_binomial(p):
            raise AssertionError(('integer binomial', p))
        counts['integer_binomial_checks'] += 1
        expected.append(full_tuple(r))
        if counts['forced_t3_checks'] < 200:
            qs = [q for q in (5, 7, 11, 13, 17, 19, 23, 29, 31) if (p - 1) % q == 0 and (p - 1) // q >= 40]
            if qs:
                out = evaluate(p, 't3', qs[-1])
                if full_tuple(out) != full_tuple(r):
                    raise AssertionError(('forced T3', p))
                counts['forced_t3_checks'] += 1
    for chunks in (1, 7, 32):
        rows, _ = forest_rows(ps, chunks)
        if list(map(tuple, rows)) != expected:
            raise AssertionError(('forest', chunks))
    for p in (True, 5, 9, 13, 2**63 + 5):
        try:
            check_domain(p)
        except ValueError:
            pass
        else:
            raise AssertionError(('bad domain accepted', p))
    for q in (1, 3, 25, 97):
        try:
            evaluate(101, 't3', q)
        except ValueError:
            pass
        else:
            raise AssertionError(('bad q accepted', q))
    probe = 20000000549
    with patch('integrated.tal_c', side_effect=ArithmeticError('injected lattice miss')):
        degraded = evaluate(probe)
    if degraded['boundary_acquisition']['route'] != 'nodal' or not degraded['boundary_acquisition']['degraded']:
        raise AssertionError('certified miss did not degrade')
    if full_tuple(degraded) != full_tuple(evaluate(probe, 'native')):
        raise AssertionError('degraded value')
    for p in (1000151, 10000103, 100000223):
        if full_tuple(evaluate(p)) != full_tuple(evaluate(p, 'native')):
            raise AssertionError(('pilot', p))
    # At p=17 the boundary multiplier is zero; still verify a_L itself.
    r17 = evaluate(17)
    if (r17['B_L'], r17['a_L'], r17['U_p_L'], r17['G']) != (6, 10, 7, 1):
        raise AssertionError('exceptional zero-multiplier case')
    counts.update(status='PASS', seconds=perf_counter()-t, forest_chunk_counts=[1,7,32],
                  development_below=20000, pilot_primes=[probe,1000151,10000103,100000223],
                  role='New integration development, not confirmation; earlier sources excluded separately')
    Path('evidence/DEVELOPMENT.json').write_text(json.dumps(counts, indent=2)+'\n')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    run()
