"""Many-prime scheduler checks against definitions and preserved source."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from boundary_framework import BoundaryError, ResourceLimitError
from many_primes import ManyPrimeEvaluator, PrimeQuery, main, range_queries
from retained_cm import rounded_third_batch as retained
from test_boundary_framework import sieve, binomial_oracle, original_sum_oracle
from test_integrated_thirds import scaled_prefix_oracle


class ManyPrimeTests(unittest.TestCase):
    def test_every_index_small_primes_all_chunk_counts(self):
        queries = [PrimeQuery(p, L) for p in sieve(127) if p > 2 for L in range(p)]
        expected = [(scaled_prefix_oracle(q.p, q.L), binomial_oracle(q.p, q.L),
                     original_sum_oracle(q.p, q.L)) for q in queries]
        for chunks in (1, 2, 7, 32):
            result = ManyPrimeEvaluator().evaluate(queries, chunks=chunks)
            actual = [(row['B_L'], row['a_L'], row['U_p_L']) for row in result['outputs']]
            self.assertEqual(actual, expected, chunks)
            stats = result['statistics']
            self.assertEqual(stats['recurrence_steps'], max(q.L for q in queries))
            self.assertEqual(stats['carry_updates'], stats['chunks_used'] - 1)
            self.assertEqual(stats['rows_emitted'], len(queries))
            self.assertTrue(stats['complete'])
            self.assertLessEqual(stats['largest_remaining_modulus_bits'], stats['remaining_modulus_bits_bound'])
            self.assertLessEqual(stats['largest_exact_chunk_entry_bits'], stats['largest_chunk_entry_bits_bound'])

    def test_retained_rounded_forest_agreement(self):
        for bound in (0, 11, 12, 100, 5000):
            queries = range_queries(bound, 'rounded_third')
            old = retained.evaluate(bound, chunks=7)
            new = ManyPrimeEvaluator().evaluate(queries, chunks=7)
            self.assertEqual([(r['p'], r['B_L'], r['a_L'], r['U_p_L']) for r in new['outputs']],
                             [(r.p, r.B_L, r.a_L, r.U_p_L) for r in old])

    def test_all_native_families_against_original_sum(self):
        for family in ('thirds', 'fifths'):
            queries = range_queries(2000, family)
            forest = ManyPrimeEvaluator().evaluate(queries)
            independent = ManyPrimeEvaluator().evaluate(queries, engine='independent', backend='bgs')
            expected = [(scaled_prefix_oracle(q.p, q.L), binomial_oracle(q.p, q.L),
                         original_sum_oracle(q.p, q.L)) for q in queries]
            for result in (forest, independent):
                self.assertEqual([(r['B_L'], r['a_L'], r['U_p_L']) for r in result['outputs']], expected)
            stats = independent['statistics']
            self.assertEqual(stats['reference_queries'], 0)
            if family == 'fifths':
                self.assertEqual(stats['native_fifth_primes'], len(queries) // 2)

    def test_unordered_repeated_primes_and_duplicate_requests(self):
        queries = [PrimeQuery(59, 24), PrimeQuery(11, 4), PrimeQuery(59, 6),
                   PrimeQuery(19, 8), PrimeQuery(59, 24), PrimeQuery(7, 6),
                   PrimeQuery(59, 12), PrimeQuery(59, 20), PrimeQuery(3, 0)]
        for engine in ('forest', 'independent'):
            result = ManyPrimeEvaluator().evaluate(queries, engine=engine, chunks=3)
            self.assertEqual([(r['p'], r['L']) for r in result['outputs']], [(q.p, q.L) for q in queries])
            self.assertEqual([r['U_p_L'] for r in result['outputs']],
                             [original_sum_oracle(q.p, q.L) for q in queries])
            self.assertEqual(result['statistics']['unique_queries'], len(set(queries)))
            result['outputs'][0]['a_L'] = -1
            self.assertNotEqual(result['outputs'][4]['a_L'], -1)  # No mutable alias.

    def test_streaming_order_empty_and_cancellation(self):
        queries = list(reversed(range_queries(500, 'thirds')))
        queries += queries[:3]
        stats = {}
        iterator = ManyPrimeEvaluator().iter_evaluate(queries, chunks=7, stats=stats)
        first = next(iterator)
        self.assertFalse(stats['complete'])
        self.assertEqual(stats['rows_emitted'], 1)
        self.assertEqual(stats['chunks_used'], 1)
        iterator.close()
        self.assertFalse(stats['complete'])
        self.assertGreater(stats['total_seconds'], 0)
        rows = list(ManyPrimeEvaluator().iter_evaluate(queries, chunks=7))
        self.assertEqual([(r['L'], r['p']) for r in rows], sorted(set((q.L, q.p) for q in queries)))
        for engine in ('forest', 'independent'):
            empty = ManyPrimeEvaluator().evaluate([], engine=engine)
            self.assertEqual(empty['outputs'], [])
            self.assertTrue(empty['statistics']['complete'])
            self.assertEqual(empty['statistics']['chunks_used'], 0)

    def test_u_only_joint_and_independent_semantics(self):
        queries = [PrimeQuery(13, 4), PrimeQuery(17, 6), PrimeQuery(29, 6), PrimeQuery(29, 12)]
        for engine in ('forest', 'independent'):
            result = ManyPrimeEvaluator().evaluate(queries, engine=engine, output_mode='u_only')
            self.assertEqual([r['U_p_L'] for r in result['outputs']],
                             [original_sum_oracle(q.p, q.L) for q in queries])
            for row in result['outputs']:
                self.assertIsNone(row['B_L']); self.assertIsNone(row['a_L'])
                if engine == 'forest':
                    self.assertEqual(row['boundary_status'], 'computed_jointly')
            if engine == 'independent':
                self.assertEqual(result['outputs'][0]['boundary_status'], 'skipped_zero_multiplier')
                self.assertEqual(result['outputs'][1]['boundary_status'], 'skipped_zero_multiplier')
                self.assertEqual(result['outputs'][3]['boundary_status'], 'skipped_zero_multiplier')

    def test_range_generation_exact_prime_coverage(self):
        for bound in (0, 1, 2, 7, 8, 11, 12, 1000):
            primes = [p for p in sieve(max(0, bound)) if p < bound]
            for family in ('thirds', 'ordinary_third', 'rounded_third', 'fifths'):
                expected = []
                for p in primes:
                    if family == 'fifths':
                        if p >= 19 and p % 5 == 4:
                            expected.extend([PrimeQuery(p, (p + 1) // 5), PrimeQuery(p, 2 * (p + 1) // 5)])
                    elif p >= 7 and p % 3 == 1 and family in ('thirds', 'ordinary_third'):
                        expected.append(PrimeQuery(p, (p - 1) // 3))
                    elif p >= 11 and p % 3 == 2 and family in ('thirds', 'rounded_third'):
                        expected.append(PrimeQuery(p, (p + 1) // 3))
                self.assertEqual(range_queries(bound, family), expected, (bound, family))

    def test_invalid_inputs_rejected_before_forest_work(self):
        evaluator = ManyPrimeEvaluator()
        bad = [([PrimeQuery(9, 1)], {}), ([PrimeQuery(11.0, 1)], {}),
               ([PrimeQuery(11, True)], {}), ([PrimeQuery(11, -1)], {}),
               ([PrimeQuery(11, 11)], {}), ([PrimeQuery(2**64 + 13, 1)], {}),
               ([(11, 4)], {}), (None, {}), ([], {'chunks': True}),
               ([], {'chunks': 0}), ([], {'engine': []}), ([], {'backend': 'unknown'}),
               ([], {'modulus_power': True}), ([], {'modulus_power': 2}),
               ([], {'output_mode': []})]
        with patch.object(retained, 'interval_product', side_effect=AssertionError('invalid arithmetic')):
            for queries, options in bad:
                with self.assertRaises(BoundaryError):
                    evaluator.evaluate(queries, **options)
        with self.assertRaises(BoundaryError):
            evaluator.iter_evaluate([], stats=[])
        for options in ({'max_queries': True}, {'max_forest_index': -1}, {'max_modulus_bits': 1.0}):
            with self.assertRaises(BoundaryError):
                ManyPrimeEvaluator(**options)

    def test_preflight_resource_caps_and_sparse_alternative(self):
        query = [PrimeQuery(101, 33)]
        for options in ({'max_queries': 0}, {'max_forest_index': 32},
                        {'max_modulus_bits': 6}, {'max_chunk_product_bits': 3}):
            with patch.object(retained, 'interval_product', side_effect=AssertionError('work before cap')):
                with self.assertRaises(ResourceLimitError):
                    ManyPrimeEvaluator(**options).evaluate(query)
        alternative = ManyPrimeEvaluator(max_forest_index=0, max_modulus_bits=0,
                                          max_chunk_product_bits=0).evaluate(query, engine='independent')
        self.assertEqual(alternative['outputs'][0]['U_p_L'], original_sum_oracle(101, 33))
        with self.assertRaises(ResourceLimitError):
            range_queries(101, max_bound=100)
        for bound in (-1, True, 1.0):
            with self.assertRaises(BoundaryError):
                range_queries(bound)

    def test_fifth_grouping_and_forest_reruns_are_real(self):
        queries = range_queries(100, 'fifths')
        with patch('many_primes.FifthPointSession', wraps=__import__('many_primes').FifthPointSession) as fifth:
            result = ManyPrimeEvaluator().evaluate(queries, engine='independent')
            self.assertEqual(fifth.call_count, len(queries) // 2)
        with patch.object(retained, 'interval_product', wraps=retained.interval_product) as interval:
            evaluator = ManyPrimeEvaluator()
            evaluator.evaluate(queries)
            count = interval.call_count
            evaluator.evaluate(queries)
            self.assertEqual(interval.call_count, 2 * count)
        self.assertFalse(result['statistics']['answer_cache_used'])

    def test_larger_sparse_stopping_queries(self):
        queries = [PrimeQuery(10007, (10007 + 1) // 3), PrimeQuery(50021, (50021 + 1) // 3),
                   PrimeQuery(100019, (100019 + 1) // 5), PrimeQuery(100019, 2 * (100019 + 1) // 5)]
        forest = ManyPrimeEvaluator().evaluate(queries, chunks=3)
        independent = ManyPrimeEvaluator().evaluate(queries, engine='independent', backend='bgs')
        for row, other, query in zip(forest['outputs'], independent['outputs'], queries):
            self.assertEqual((row['B_L'], row['a_L'], row['U_p_L']),
                             (other['B_L'], other['a_L'], other['U_p_L']))
            self.assertEqual(row['U_p_L'], original_sum_oracle(query.p, query.L))

    def test_csv_atomic_publication_and_cli_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'results.csv'
            base = ['--bound', '100', '--family', 'rounded_third', '--out', str(path)]
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                self.assertEqual(main(base), 0)
            record = json.loads(buffer.getvalue())
            self.assertTrue(record['statistics']['complete'])
            self.assertTrue(path.read_text().startswith('p,L,B_L,a_L,U_p_L\n'))
            previous = path.read_bytes()
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--queries', '9:1', '--out', str(path)]), 2)
            self.assertEqual(path.read_bytes(), previous)
            with patch.object(retained, 'interval_product', side_effect=ResourceLimitError('injected failure')):
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(main(base), 2)
            self.assertEqual(path.read_bytes(), previous)
            self.assertEqual(list(Path(directory).iterdir()), [path])
        for args in (['--queries', 'bad'], ['--queries', '11:4', '--modulus-power', '2']):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(args), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
