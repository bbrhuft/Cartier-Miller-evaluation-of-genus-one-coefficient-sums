"""Independent finite checks of boundary batches and actual shared work."""
from contextlib import redirect_stdout
import io
import json
import random
import unittest
from unittest.mock import patch

import shared_boundaries as shared
from shared_boundaries import BoundaryBatchSession, main
from benchmark_shared import recurrence_boundaries
from boundary_framework import (
    BoundaryError, BoundaryEvaluator, BoundaryRequest, DirectReferencePrefix,
    ResourceLimitError, SuppliedPrefix, UnsupportedPrefixError,
)
from integrated_thirds import ThirdPointPrefixProvider
from test_boundary_framework import sieve, binomial_oracle, original_sum_oracle


class SharedBoundaryTests(unittest.TestCase):
    def test_exhaustive_all_indices_backends_and_sharing(self):
        for p in sieve(257):
            if p == 2:
                continue
            expected = [binomial_oracle(p, L) for L in range(p)]
            session = BoundaryBatchSession(p)
            for sharing in ('exact', 'adjacent'):
                for backend in ('direct', 'product_tree', 'bgs'):
                    result = session.evaluate(range(p), backend=backend, sharing=sharing)
                    self.assertEqual(result['values'], expected, (p, sharing, backend))
                    self.assertEqual(result['indices'], list(range(p)))
                    self.assertLessEqual(result['denominator_inversions'], 1)

    def test_generic_plan_and_wilson_reflection(self):
        engine = BoundaryEvaluator()
        for p in sieve(127):
            if p == 2:
                continue
            indices = list(range(p))
            result = BoundaryBatchSession(p).evaluate(indices, family='generic', backend='bgs')
            self.assertEqual(result['values'], [binomial_oracle(p, n) for n in indices])
            self.assertEqual(result['values'],
                             [engine.evaluate(BoundaryRequest(p, n, 'generic', 'direct')).value
                              for n in indices])
            # All factorial acquisitions have already been reflected. No
            # inversion is hidden in backend Wilson restoration.
            for call in result['product_calls']:
                if call['kind'] == 'factorial':
                    self.assertFalse(call['result']['reflected'])
                    self.assertLessEqual(call['length'], (p - 1) // 2)

    def test_third_and_fifth_formulas_through_10000(self):
        for p in sieve(10000):
            if p < 7:
                continue
            third = (p - 1) // 3 if p % 3 == 1 else (p + 1) // 3
            indices = [third]
            if p % 5 == 4:
                indices += [(p + 1) // 5, 2 * (p + 1) // 5]
            result = BoundaryBatchSession(p).evaluate(indices, backend='bgs')
            self.assertEqual(result['values'], [binomial_oracle(p, n) for n in indices], p)

    def test_larger_shuffled_batches_against_integer_binomial(self):
        rng = random.Random(162026)
        for p in (10007, 100019, 1000039):
            indices = [0, 1, p // 4, p // 2, p // 2 + 1, p - 1]
            indices += [rng.randrange(p) for _ in range(8)]
            indices += [indices[3], indices[2]]
            rng.shuffle(indices)
            expected = (recurrence_boundaries(p, indices) if p > 100019 else
                        [binomial_oracle(p, n) for n in indices])
            for sharing in ('exact', 'adjacent'):
                result = BoundaryBatchSession(p).evaluate(indices, backend='bgs', sharing=sharing)
                self.assertEqual(result['values'], expected, (p, sharing))

    def test_duplicate_and_empty_queries(self):
        session = BoundaryBatchSession(59)
        result = session.evaluate([24, 6, 12, 24, 20, 6])
        self.assertEqual(result['indices'], [24, 6, 12, 24, 20, 6])
        self.assertEqual(result['values'], [binomial_oracle(59, n) for n in result['indices']])
        self.assertEqual(result['unique_boundaries'], 4)
        self.assertEqual(result['product_acquisitions'], session.evaluate([6, 12, 24, 20])['product_acquisitions'])
        with patch.object(session.intervals, 'product', side_effect=AssertionError('empty interval work')):
            with patch.object(session.factorials.backends['direct'], 'factorial',
                              side_effect=AssertionError('empty factorial work')):
                empty = session.evaluate([])
        self.assertEqual(empty['values'], [])
        self.assertEqual(empty['product_acquisitions'], 0)
        self.assertEqual(empty['denominator_inversions'], 0)

    def test_real_gap_and_cross_family_interval_reuse(self):
        session = BoundaryBatchSession(59)
        with patch.object(session.intervals, 'product', wraps=session.intervals.product) as interval:
            with patch.object(session.factorials.backends['direct'], 'factorial',
                              wraps=session.factorials.backends['direct'].factorial) as factorial:
                result = session.evaluate([6, 12, 24, 20, 6])
        self.assertEqual(factorial.call_count, 1)  # 6!, also fifth denominator.
        self.assertEqual(interval.call_count, 3)
        # (7..12) is acquired once: extends 6! to 12! and is the second
        # fifth's numerator. Other intervals are 13..19 and 18..23.
        actual = [(c.args[1], c.args[2]) for c in interval.call_args_list]
        self.assertEqual(actual.count((7, 6)), 1)
        self.assertEqual(result['product_acquisitions'], 4)
        exact = session.evaluate([6, 12, 24, 20], sharing='exact')
        self.assertEqual(exact['values'], result['values'][:4])
        self.assertEqual(exact['product_acquisitions'], 5)
        self.assertEqual(sum(session.evaluate([n])['product_acquisitions'] for n in (6, 12, 24, 20)), 7)

    def test_denominators_use_one_real_inversion(self):
        session = BoundaryBatchSession(101)
        with patch.object(shared, '_batch_inverse_nonzero', wraps=shared._batch_inverse_nonzero) as invert:
            result = session.evaluate([5, 6, 7, 8, 9], family='generic')
        self.assertEqual(invert.call_count, 1)
        self.assertGreater(result['distinct_nontrivial_denominators'], 1)
        self.assertTrue(all(invert.call_args.args[0]))
        self.assertEqual(result['denominator_inversions'], 1)

    def test_repeated_evaluations_rerun_acquisitions(self):
        session = BoundaryBatchSession(59)
        with patch.object(session.intervals, 'product', wraps=session.intervals.product) as intervals:
            first = session.evaluate([6, 12, 24, 20])
            count = intervals.call_count
            second = session.evaluate([6, 12, 24, 20])
            self.assertEqual(intervals.call_count, 2 * count)
        self.assertEqual(first['values'], second['values'])
        self.assertFalse(second['answer_cache_used'])

    def test_complete_many_against_original_recurrence_and_prefix_sharing(self):
        for p in sieve(127):
            if p == 2:
                continue
            session = BoundaryBatchSession(p)
            provider = DirectReferencePrefix()
            indices = [*range(p), 0, p // 2]
            with patch.object(provider, 'prefix', wraps=provider.prefix) as prefix:
                full = session.complete_many(indices, provider, backend='bgs')
                self.assertEqual(prefix.call_count, p)
            u_only = session.complete_many(indices, provider, backend='bgs', output_mode='u_only')
            expected = [original_sum_oracle(p, n) for n in indices]
            self.assertEqual([row['U_p_L'] for row in full['outputs']], expected)
            self.assertEqual([row['U_p_L'] for row in u_only['outputs']], expected)
            for row in u_only['outputs']:
                self.assertIsNone(row['a_L'])
                self.assertIsNone(row['B_L'])
                self.assertEqual(row['boundary_status'] == 'skipped_zero_multiplier',
                                 2 * row['L'] * (2 * row['L'] + 5) % p == 0)
            self.assertTrue(all(v is None for v in u_only['boundary_details']['values']))

    def test_retained_third_provider_contract(self):
        for p in (13, 17, 61, 331, 10007):
            provider = ThirdPointPrefixProvider(p)
            result = BoundaryBatchSession(p).complete_many([provider.L, provider.L], provider, backend='bgs')
            self.assertEqual(result['prefix_calls'], 1)
            self.assertEqual([row['U_p_L'] for row in result['outputs']],
                             [original_sum_oracle(p, provider.L)] * 2)

    def test_u_only_skip_and_resource_semantics(self):
        session = BoundaryBatchSession(17, max_direct_terms=0)
        provider = SuppliedPrefix(17, 6, 6)
        with patch.object(session, '_evaluate_plans', wraps=session._evaluate_plans) as evaluator:
            result = session.complete_many([6, 6], provider, output_mode='u_only')
            self.assertEqual(evaluator.call_args.args[0], ())
        self.assertEqual([row['U_p_L'] for row in result['outputs']], [7, 7])
        self.assertEqual(result['boundary_details']['product_acquisitions'], 0)
        with self.assertRaises(ResourceLimitError):
            session.complete_many([6], provider)
        with self.assertRaises(ResourceLimitError):
            BoundaryBatchSession(101, max_degree=1).evaluate([12], backend='bgs')

    def test_invalid_requests_fail_before_acquisition(self):
        for p in (0, 2, 9, 11.0, True, 2**64 + 13):
            with self.assertRaises(BoundaryError):
                BoundaryBatchSession(p)
        session = BoundaryBatchSession(59)
        bad = [(None, {}), ([1, True], {}), ([59], {}), ([-1], {}),
               ([6], {'family': 'ordinary_third'}), ([20], {'family': 'fifth'}),
               ([6], {'family': []}), ([], {'backend': 'unknown'}),
               ([6], {'backend': []}), ([], {'sharing': []}),
               ([], {'modulus_power': True}), ([], {'modulus_power': 2})]
        with patch.object(session, '_evaluate_plans', side_effect=AssertionError('invalid acquisition')):
            for indices, options in bad:
                with self.assertRaises(BoundaryError, msg=str((indices, options))):
                    session.evaluate(indices, **options)
        for value in (-1, 59, True, 1.0):
            with self.assertRaises(BoundaryError):
                session.complete_many([12], SuppliedPrefix(59, 12, value))
        with self.assertRaises(UnsupportedPrefixError):
            session.complete_many([12, 24], SuppliedPrefix(59, 12, 1))
        with self.assertRaises(BoundaryError):
            session.complete_many([12], DirectReferencePrefix(), output_mode=[])

    def test_cli_boundary_complete_empty_and_errors(self):
        cases = [(['--p', '59', '--indices', '6', '12', '24', '20', '--backend', 'bgs'], 0),
                 (['--p', '29', '--indices', '6', '12', '--reference-prefix'], 0),
                 (['--p', '17', '--indices', '6', '--reference-prefix', '--output-mode', 'u_only'], 0),
                 (['--p', '59', '--indices'], 0),
                 (['--p', '9', '--indices', '1'], 2),
                 (['--p', '59', '--indices', '6', '--output-mode', 'u_only'], 2)]
        for args, status in cases:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                self.assertEqual(main(args), status)
            self.assertIsInstance(json.loads(buffer.getvalue()), dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
