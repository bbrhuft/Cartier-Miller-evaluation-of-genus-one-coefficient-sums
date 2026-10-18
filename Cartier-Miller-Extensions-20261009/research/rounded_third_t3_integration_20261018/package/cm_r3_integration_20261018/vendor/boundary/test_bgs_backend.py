"""Independent oracles for scalar BGS shifts, blocks, factorials and outputs."""
from math import factorial, prod
import random
import unittest

from boundary_framework import (
    _APShiftPlan, _block_values, _bgs_interval_product, BGSFactorialBackend,
    BoundaryError, ResourceLimitError, BoundaryEvaluator, BoundaryRequest,
)
from integrated_fifths import IntervalProductEvaluator, FifthPointSession
from integrated_thirds import ThirdPointSession
from test_boundary_framework import sieve, binomial_oracle, original_sum_oracle


def horner(coefficients, x, p):
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * x + coefficient) % p
    return value


class BGSBackendTests(unittest.TestCase):
    def test_shifts_every_degree_and_shift_small_fields(self):
        rng = random.Random(1052026)
        for p in sieve(19):
            if p == 2:
                continue
            for degree in range(p):
                coefficients = [rng.randrange(p) for _ in range(degree + 1)]
                values = [horner(coefficients, i, p) for i in range(degree + 1)]
                for alpha in range(p):
                    plan = _APShiftPlan(degree, alpha, p)
                    self.assertEqual(plan.apply(values),
                                     [horner(coefficients, alpha + i, p)
                                      for i in range(degree + 1)], (p, degree, alpha))
                    self.assertEqual(plan.apply([0] * (degree + 1)), [0] * (degree + 1))

    def test_shifts_packed_products_and_large_field_wrap(self):
        rng = random.Random(842139)
        for p in (101, 10007, 4294967291, 18446744073709551557):
            for d in (15, 16, 31, 64):
                coefficients = [rng.randrange(p) for _ in range(d + 1)]
                values = [horner(coefficients, i, p) for i in range(d + 1)]
                for alpha in (0, 1, d, d + 1, p - 1, p - d, rng.randrange(p)):
                    self.assertEqual(_APShiftPlan(d, alpha, p).apply(values),
                                     [horner(coefficients, alpha + i, p) for i in range(d + 1)])

    def test_blocks_even_odd_and_square_boundaries(self):
        p = 10007
        for size in range(1, 70):
            for start in (1, 19, p - 1):
                self.assertEqual(_block_values(start, size, p),
                                 [prod((start + i * size + j) % p for j in range(size)) % p
                                  for i in range(size + 1)], (start, size))

    def test_all_unit_intervals_small_fields(self):
        engine = IntervalProductEvaluator()
        for p in sieve(43):
            if p == 2:
                continue
            for start in range(1, p + 1):
                value = 1
                for length in range(p - start + 1):
                    if length:
                        value = value * (start + length - 1) % p
                    self.assertEqual(engine.product(p, start, length, 'bgs').value,
                                     value, (p, start, length))

    def test_factorials_every_index_small_primes(self):
        backend = BGSFactorialBackend()
        for p in sieve(257):
            if p == 2:
                continue
            for n in range(p):
                result = backend.factorial(n, p)
                self.assertEqual(result.value, factorial(n) % p, (p, n))
                self.assertEqual(result.reflected, n > (p - 1) // 2)

    def test_large_unit_intervals_against_direct_product(self):
        for p in (1000003, 4294967291, 18446744073709551557):
            for length in (255, 256, 257, 1023, 1024, 1025, 100003):
                for start in (1, p - length):
                    expected = 1
                    for j in range(start, start + length):
                        expected = expected * j % p
                    self.assertEqual(_bgs_interval_product(p, start, length)[0], expected)

    def test_generic_boundaries_small_fields(self):
        engine = BoundaryEvaluator()
        for p in sieve(257):
            if p == 2:
                continue
            for n in range(p):
                self.assertEqual(engine.evaluate(BoundaryRequest(p, n, 'generic', 'bgs')).value,
                                 binomial_oracle(p, n), (p, n))

    def test_complete_thirds_and_fifths_against_original_sum(self):
        for p in sieve(1000):
            if p < 7:
                continue
            session = ThirdPointSession(p)
            result = session.evaluate(backend='bgs', boundary_policy='factorial')
            self.assertEqual(result['U_p_L'], original_sum_oracle(p, session.L))
            self.assertEqual(result['a_L'], binomial_oracle(p, session.L))
            if p % 5 == 4:
                result = FifthPointSession(p).evaluate(backend='bgs')
                for row in result['outputs']:
                    self.assertEqual(row['U_p_L'], original_sum_oracle(p, row['L']))
                    self.assertEqual(row['a_L'], binomial_oracle(p, row['L']))
        result = FifthPointSession(29).evaluate(backend='bgs', output_mode='u_only')
        self.assertEqual([r['U_p_L'] for r in result['outputs']], [8, 10])
        self.assertEqual(len(result['boundary_details']['interval_calls']), 2)

    def test_domain_and_resource_guards(self):
        for degree in (-1, True, 101):
            with self.assertRaises(BoundaryError):
                _APShiftPlan(degree, 1, 101)
        with self.assertRaises(BoundaryError):
            _APShiftPlan(3, 1, 101).apply([1])
        for args in ((0, 1), (1, -1), (100, 2), (True, 1)):
            with self.assertRaises(BoundaryError):
                _bgs_interval_product(101, *args)
        for cap in (0, True, -1):
            with self.assertRaises(BoundaryError):
                BGSFactorialBackend(cap)
        with self.assertRaises(ResourceLimitError):
            BGSFactorialBackend(2).factorial(33, 101)
        with self.assertRaises(ResourceLimitError):
            IntervalProductEvaluator(max_degree=2).product(101, 1, 33, 'bgs')

    def test_automatic_dispatch_and_explicit_overrides(self):
        engine = BoundaryEvaluator(direct_cutoff=10)
        for backend in ('auto', 'direct', 'product_tree', 'bgs'):
            result = engine.evaluate(BoundaryRequest(101, 33, backend=backend))
            self.assertEqual(result.value, binomial_oracle(101, 33))
            self.assertEqual(result.factorial_calls[0].backend,
                             'bgs' if backend == 'auto' else backend)
        engine = IntervalProductEvaluator(direct_cutoff=10)
        self.assertEqual(engine.product(101, 1, 10).backend, 'direct')
        self.assertEqual(engine.product(101, 1, 11).backend, 'bgs')
        self.assertEqual(engine.product(101, 1, 11, 'product_tree').backend, 'product_tree')


if __name__ == '__main__':
    unittest.main(verbosity=2)
