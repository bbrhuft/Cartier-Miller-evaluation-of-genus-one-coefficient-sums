"""Cartier--Miller rounded thirds with certified Jacobi-sum boundary acquisition.

Input: certified prime 11 <= p < 2**63, p == 5 (mod 6). The public adapter also
checks primality using the retained exact 64-bit test. All outputs are modulo p.
No PARI/GRH backend is used. Kernels and plans are preserved under vendor/.
"""
import argparse
from collections import Counter
import json
from time import perf_counter

import bootstrap
from boundary_framework import (BoundaryError, BoundaryEvaluator, BoundaryRequest,
                                FactorialResult, ReductionPlan, complete_sum, is_prime64)
from integrated_thirds import ThirdPointPrefixProvider
from retained_cm import rounded_third_batch as forest
from r3.acquire_r31 import (admissible_q, nodal_flint_c, policy, tal_c, tal_cost)
from r3.common import flint_factorial, a_from_c

VERSION = '0.1.0'
SMALL_NATIVE_CUTOFF = 10_000_000


def check_domain(p):
    if type(p) is not int or not 11 <= p < 2**63 or p % 6 != 5 or not is_prime64(p):
        raise BoundaryError('require a prime 11 <= p < 2**63 with p == 5 (mod 6)')


class NativeFlintFactorial:
    name = 'flint_native'

    def factorial(self, n, p):
        t = perf_counter()
        value = int(flint_factorial(n, p))
        return FactorialResult(n, value, self.name, n, False, 0, 0.0, perf_counter() - t)


def acquire_boundary(p, method='auto', q=None):
    """Return signed a_L and costed route metadata; never use class numbers.

    Auto: native factorial below 10**7; otherwise use the source's frozen
    T3 cost model against its nodal prediction, with the exact nodal fallback.
    This replaces the source's optional class-number fallback, not its algebra.
    A new Jacobi context is constructed on every call (no answer caching).
    """
    t = perf_counter()
    if method not in ('auto', 'native', 'nodal', 't3'):
        raise BoundaryError('method must be auto, native, nodal or t3')
    if q is not None and (type(q) is not int or q < 5 or not is_prime64(q)
                          or (p - 1) % q or (p - 1) // q < 4 or q > 89):
        raise BoundaryError('forced q must be prime, 5 <= q <= 89, q | p-1, K >= 4')
    if q is not None and method not in ('auto', 't3'):
        raise BoundaryError('a forced q applies only to auto or t3')
    qs, degraded, predictions = [], [], {}
    target = method
    if q is not None:
        qs, target = [q], 't3'
    elif method == 'auto':
        if p < SMALL_NATIVE_CUTOFF:
            target = 'native'
        else:
            model = policy()['nodal_model']
            fallback_cost = model['C'] * p ** model['delta']
            predictions = {x: tal_cost(p, x) for x in admissible_q(p)}
            qs = sorted((x for x in predictions if predictions[x] < fallback_cost),
                        key=lambda x: (predictions[x], -x))
            target = 't3' if qs else 'nodal'
    elif method == 't3':
        qs = sorted(admissible_q(p), key=lambda x: (tal_cost(p, x), -x))
        if not qs:
            raise BoundaryError('no admissible small conductor for forced T3')
    if target == 't3':
        for conductor in qs:
            try:
                c, metadata = tal_c(p, conductor)
            except ArithmeticError as exc:
                degraded.append({'q': conductor, 'reason': str(exc)})
                continue
            return a_from_c(p, c), dict(route='t3', q=conductor, status='unconditional',
                                       seconds=perf_counter() - t, degraded=degraded,
                                       predictions=predictions, kernel=metadata)
        if method == 't3' or q is not None:
            raise ArithmeticError('forced T3 reconstruction failed: %r' % degraded)
        target = 'nodal'
    if target == 'native':
        g = flint_factorial((p - 2) // 3, p)
        a = 3 * pow(2, -1, p) * pow(g, -3, p) % p
    else:
        a = a_from_c(p, nodal_flint_c(p))
    return a, dict(route=target, q=None, status='unconditional',
                   seconds=perf_counter() - t, degraded=degraded, predictions=predictions)


class RoundedThirdSession:
    """Adapter using the retained boundary registry and complete_sum unchanged."""

    def __init__(self, p, method='auto', q=None):
        t = perf_counter()
        check_domain(p)
        self.p, self.L, self.method, self.q = p, (p + 1) // 3, method, q
        self.provider = ThirdPointPrefixProvider(p)
        self.engine = BoundaryEvaluator()
        self.engine.register_backend('flint_native', NativeFlintFactorial())
        self.last_boundary = None

        def reducer(prime, index):
            if (prime, index) != (self.p, self.L):
                return None

            def finish(_):
                value, self.last_boundary = acquire_boundary(prime, self.method, self.q)
                return value

            return ReductionPlan('rounded_third_r3', 'a_L acquired by certified T3 or exact fallback',
                                 'REPORT.md; vendor/atkin_r3/REPORT_R3.md, Section 6', (), finish)

        self.engine.register_reduction('rounded_third_r3', reducer)
        self.setup_seconds = perf_counter() - t

    def evaluate(self):
        request = (BoundaryRequest(self.p, self.L, 'rounded_third', 'flint_native')
                   if self.method == 'native' and self.q is None else
                   BoundaryRequest(self.p, self.L, 'rounded_third_r3'))
        r = complete_sum(request,
                         self.provider, self.engine)
        if self.last_boundary is None:
            self.last_boundary = dict(route='native', q=None, status='unconditional',
                                      seconds=r['boundary']['total_seconds'], degraded=[], predictions={})
        # These transformations are separately checked against the definitions.
        p, a, B = self.p, r['a_L'], r['B_L']
        r.update(m=(p - 2) // 3, B_m=(B + 4 * a) % p, a_m=(-4 * a) % p,
                 U_p_m=(4 * B - 32 * pow(9, -1, p) * a) % p,
                 G=pow(3 * pow(2 * a, -1, p) % p, (2 * p - 1) // 3, p),
                 boundary_acquisition=self.last_boundary,
                 retained_prefix_diagnostics=self.provider.last_metadata,
                 setup_seconds=self.setup_seconds, answer_cache_used=False,
                 status='unconditional arithmetic; retained project prefix theorem unrefereed')
        r['cold_total_seconds'] = self.setup_seconds + r['total_seconds']
        return r


def evaluate(p, method='auto', q=None):
    t = perf_counter()
    r = RoundedThirdSession(p, method, q).evaluate()
    r['elapsed_seconds'] = perf_counter() - t
    return r


def dense(bound, method='auto'):
    """Charge sieve, every cold evaluation and collection for the same prime table."""
    t = perf_counter()
    rows = [evaluate(p, method) for p in forest.branch_primes(bound)]
    return rows, dict(seconds=perf_counter() - t, rows=len(rows),
                      routes=dict(Counter(r['boundary_acquisition']['route'] for r in rows)))


def forest_rows(primes, chunks=32, integer_backend='python'):
    """Byte-preserved forest, with a supplied sorted prime schedule (not a Miller route)."""
    if primes != sorted(set(primes)):
        raise ValueError('forest schedule must be sorted and distinct')
    for p in primes:
        check_domain(p)
    if primes and (primes[-1] + 1) // 3 > 2_000_000:
        raise BoundaryError('forest experiment cap: maximum cutoff 2,000,000')
    stats = {}
    rows = list(forest._iter_rows(primes, chunks, integer_backend, stats))
    return rows, stats


def compact(row):
    return tuple(row[k] for k in ('p', 'B_L', 'a_L', 'U_p_L'))


def full_tuple(row):
    return compact(row) + (row['G'],)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('p', type=int)
    parser.add_argument('--method', choices=('auto', 'native', 'nodal', 't3'), default='auto')
    parser.add_argument('--q', type=int)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.p, args.method, args.q), indent=2))
