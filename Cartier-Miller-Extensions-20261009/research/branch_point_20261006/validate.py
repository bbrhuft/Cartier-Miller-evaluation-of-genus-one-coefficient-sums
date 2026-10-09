"""Independent dense-power, point-count and cleared-differential checks."""
from pathlib import Path
import csv
import hashlib
import json
import platform
import random
import sys
import time
from branch_evaluator import prepare, prepare_from_trace, check_cubic, eval_poly, is_prime64


def mul(a, b, p):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    if p:
        c = [x % p for x in c]
    return c


def dense_power(f, h, p):
    # Successive multiplication by the cubic, independent of the recurrence.
    r = [1]
    for _ in range(h):
        r = mul(r, f, p)
    return r


def at(c, n):
    return c[n] if 0 <= n < len(c) else 0


def differential_check(f, mu, p):
    # f=(w-mu)g; check -f'(mu)+g-(w-mu)g'=a(mu-w)(w-mu).
    a, b, c = f[3], f[2], f[1]
    g = [(c+b*mu+a*mu*mu) % p, (b+a*mu) % p, a]
    assert mul([-mu, 1], g, p) == list(f)
    d = eval_poly(g, mu, p)
    prod = mul([-mu, 1], [g[1], 2*g[2]], p)
    left = [(g[i]-prod[i]-(d if i == 0 else 0)) % p for i in range(3)]
    right = [a*x % p for x in mul([mu, -1], [-mu, 1], p)]
    assert left == right


def high_part_check(f, row, H, K, p):
    # General-leading-coefficient version of Voloch's Section 2 lemma.
    R = row[p:]
    derivative = [f[1], 2*f[2], 3*f[3]]
    Rp = [i*R[i] % p for i in range(1, len(R))] or [0]
    left, right = mul(derivative, R, p), mul(f, Rp, p)
    size = max(len(left), len(right), 2)
    total = [(at(left, i)+2*at(right, i)) % p for i in range(size)]
    expected = [f[3]*K % p, -f[3]*H % p]+[0]*(size-2)
    assert total == expected


def trace(f, p):
    total = 0
    for w in range(p):
        d = eval_poly(f, w, p)
        if d:
            total += 1 if pow(d, (p-1)//2, p) == 1 else -1
    return -total


def model_check(f, row, p):
    # X=a*w+b/3, Y=a*v; dw/v=dX/Y.
    _, c, b, a = f
    shift = b*pow(3, -1, p) % p
    A = (a*c-b*b*pow(3, -1, p)) % p
    B = (a*a-a*b*c*pow(3, -1, p)+2*b*b*b*pow(27, -1, p)) % p
    short = dense_power([B, A, 0, 1], (p-1)//2, p)
    assert at(short, p-1) == row[p-1]
    assert at(short, p-2) == (a*row[p-2]+shift*row[p-1]) % p
    return A, B, at(short, p-2)


def main():
    out = Path(__file__).parent/'results'
    out.mkdir(exist_ok=True)
    rows, totals, collisions = [], {}, {}
    examples = {'ordinary': None, 'supersingular': None, 'trace_collision': None}
    start = time.perf_counter()
    def inspect(p, f, phase):
        try:
            f = check_cubic(f, p)
        except ValueError:
            totals[phase+'_singular'] = totals.get(phase+'_singular', 0)+1
            return
        roots = [mu for mu in range(1, p) if eval_poly(f, mu, p) == 0]
        totals[phase+'_squarefree'] = totals.get(phase+'_squarefree', 0)+1
        if not roots:
            totals[phase+'_without_rational_root'] = totals.get(phase+'_without_rational_root', 0)+1
            return
        prepared = prepare(p, f)
        row = dense_power(f, (p-1)//2, p)
        H, K = prepared.H, prepared.K
        assert (H, K) == (row[p-1], row[p-2])
        tau = trace(f, p)
        assert H == tau % p and tau % 2 == 0
        high_part_check(f, row, H, K, p)
        A, B, beta = model_check(f, row, p)
        structural = None
        if (A == 0 and p % 3 == 1) or (B == 0 and p % 4 == 1):
            structural = prepare_from_trace(p, f, tau)
            assert (structural.H, structural.K) == (H, K) and beta == 0
            totals['structural_trace_preparations'] = totals.get('structural_trace_preparations', 0)+1
        if phase == 'exhaustive' and p <= 13:
            integer_row = dense_power(f, (p-1)//2, None)
            assert row == [x % p for x in integer_row]
            totals['integer_power_checks'] = totals.get('integer_power_checks', 0)+1
        kind = 'ordinary' if H else 'supersingular'
        totals[phase+'_'+kind+'_curves'] = totals.get(phase+'_'+kind+'_curves', 0)+1
        for mu in roots:
            result = prepared.query(mu)
            T = eval_poly(row[:p], mu, p)
            lam = pow(mu, -1, p)
            S = sum(cm*pow(lam, p-1-i, p) for i, cm in enumerate(row[:p])) % p
            assert result['T'] == T == S
            if structural is not None:
                assert structural.query(mu)['T'] == T
                totals['structural_branch_queries'] = totals.get('structural_branch_queries', 0)+1
            assert T == -mu*eval_poly(row[p:], mu, p) % p
            differential_check(f, mu, p)
            sample = {'phase': phase, 'p': p, 'c': f[1], 'b': f[2], 'a': f[3],
                      'mu': mu, 'derivative': (f[1]+2*f[2]*mu+3*f[3]*mu*mu) % p,
                      'trace': tau, 'H': H, 'K': K, 'T': T, 'ordinary': bool(H)}
            rows.append(sample)
            if examples[kind] is None:
                examples[kind] = sample
            key = (p, mu, f[3], tau)
            if key in collisions and collisions[key]['K'] != K and examples['trace_collision'] is None:
                examples['trace_collision'] = [collisions[key], sample]
            elif key not in collisions:
                collisions[key] = sample
            totals[phase+'_branch_queries'] = totals.get(phase+'_branch_queries', 0)+1
    primes = [p for p in range(7, 24) if is_prime64(p)]
    for p in primes:
        for a in range(1, p):
            for b in range(p):
                for c in range(p):
                    inspect(p, (1, c, b, a), 'exhaustive')
    rng = random.Random(202610062106)
    held = [p for p in range(29, 252) if is_prime64(p)]
    for p in held:
        for _ in range(16):
            mu, q, r = rng.randrange(1, p), rng.randrange(p), rng.randrange(1, p)
            inv = pow(mu, -1, p)
            # f=(1-w/mu)*(1+q*w+r*w^2), so mu is supplied by construction.
            inspect(p, (1, (q-inv) % p, (r-q*inv) % p, -r*inv % p), 'held_out')
    for p, f, root in [(9, [1, 0, 0, -1], 1), (5, [1, 0, 0, -1], 1),
                       (7, [1, 0, 1, 0], 1), (7, [1, -3, 3, -1], 1),
                       (7, [1, 0, 0, -1], 0), (7, [1, 0, 0, -1], 3)]:
        try:
            prepare(p, f).query(root)
        except ValueError:
            totals['expected_input_rejections'] = totals.get('expected_input_rejections', 0)+1
        else:
            raise AssertionError('invalid input accepted')
    with (out/'validation.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = {'status': 'passed', 'seed': 202610062106,
              'exhaustive_primes': primes, 'held_out_primes': held,
              'held_out_generated_per_prime': 16,
              'counts': totals, 'examples': examples,
              'elapsed_validation_seconds': time.perf_counter()-start,
              'is_benchmark': False,
              'environment': {'python': sys.version, 'platform': platform.platform()},
              'source_sha256': {name: hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                                for name in ['branch_evaluator.py', 'validate.py']}}
    (out/'validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
