"""Dispatch policy fixtures are synthetic; actual calibration is tested separately."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from boundary_framework import BoundaryError, ResourceLimitError
from calibrate_dispatch import calibrate, main as calibrate_main
from dispatch_profile import configuration, load_profile, workload_key, write_record
from many_primes import ManyPrimeEvaluator, PrimeQuery, range_queries, main
from test_boundary_framework import original_sum_oracle


def fixture_record(evaluator, queries, collection='collected', mode='full'):
    # Deterministic policy fixtures; these values are never reported as real timings.
    methods = [('independent', 'auto', 32, 10.0), ('independent', 'direct', 32, 9.0),
               ('independent', 'bgs', 32, 8.0), ('forest', 'auto', 1, 3.0),
               ('forest', 'auto', 8, 2.0)]
    return {'workload_sha256': workload_key(queries, mode, collection),
            'configuration': configuration(evaluator), 'candidates': [
                {'engine': e, 'backend': b, 'chunks': c, 'samples_seconds': [t] * 3,
                 'verified': True} for e, b, c, t in methods]}


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'dispatch.json'
        self.queries = range_queries(100, 'rounded_third')
        self.evaluator = ManyPrimeEvaluator()

    def decision(self, queries=None, **options):
        result = self.evaluator.evaluate(self.queries if queries is None else queries,
                                         engine='auto', profile=self.path, **options)
        self.assertEqual([r['U_p_L'] for r in result['outputs']],
                         [original_sum_oracle(r['p'], r['L']) for r in result['outputs']])
        return result['statistics']['dispatch']

    def test_exact_selection_and_correct_outputs(self):
        write_record(self.path, fixture_record(self.evaluator, self.queries))
        decision = self.decision()
        self.assertEqual(decision['status'], 'measured_exact')
        self.assertEqual(decision['selected_engine'], 'forest')
        self.assertEqual(decision['selected_chunks'], 8)
        self.assertEqual(decision['measured_median_seconds'], 2.0)

    def test_missing_unknown_and_corrupt_profiles_fall_back(self):
        self.assertEqual(self.decision()['reason'], 'profile_missing')
        self.path.write_text('not JSON')
        self.assertEqual(self.decision()['reason'], 'profile_invalid_or_unreadable')
        write = self.path.write_text
        write(json.dumps({'schema': 999, 'records': []}))
        self.assertEqual(self.decision()['selected_engine'], 'independent')
        self.path.unlink()
        write_record(self.path, fixture_record(self.evaluator, self.queries))
        self.assertEqual(self.decision(self.queries[:-1])['reason'], 'workload_unmeasured')

    def test_order_duplicates_modes_and_collection_do_not_cross_match(self):
        write_record(self.path, fixture_record(self.evaluator, self.queries))
        for queries in (list(reversed(self.queries)), self.queries + self.queries[:1]):
            self.assertEqual(self.decision(queries)['reason'], 'workload_unmeasured')
        self.assertEqual(self.decision(output_mode='u_only')['reason'], 'workload_unmeasured')
        stats = {}
        rows = list(self.evaluator.iter_evaluate(self.queries, engine='auto', profile=self.path, stats=stats))
        self.assertEqual(stats['dispatch']['reason'], 'workload_unmeasured')
        self.assertEqual(len(rows), len(self.queries))
        write_record(self.path, fixture_record(self.evaluator, self.queries, collection='streaming'))
        stats = {}
        list(self.evaluator.iter_evaluate(self.queries, engine='auto', profile=self.path, stats=stats))
        self.assertEqual(stats['dispatch']['status'], 'measured_exact')

    def test_environment_source_and_configuration_invalidation(self):
        record = fixture_record(self.evaluator, self.queries)
        write_record(self.path, record)
        original = self.path.read_text()
        for field, value, reason in (
                ('environment', {}, 'profile_environment_mismatch'),
                ('implementation_sha256', 'changed', 'profile_implementation_mismatch'),
                ('version', 'old', 'profile_implementation_mismatch')):
            data = json.loads(original); data[field] = value
            self.path.write_text(json.dumps(data))
            self.assertEqual(self.decision()['reason'], reason)
        self.path.write_text(original)
        different = ManyPrimeEvaluator(max_degree=4096).evaluate(
            self.queries, engine='auto', profile=self.path)
        self.assertEqual(different['statistics']['dispatch']['reason'], 'profile_configuration_mismatch')

    def test_explicit_override_never_reads_profile(self):
        with patch('dispatch_profile.load_profile', side_effect=AssertionError('unexpected profile read')):
            result = self.evaluator.evaluate(self.queries, engine='forest', chunks=1, profile=self.path)
        self.assertEqual(result['statistics']['dispatch']['status'], 'explicit_override')
        self.assertEqual(result['statistics']['engine'], 'forest')

    def test_backend_constraint_and_tie_margin(self):
        record = fixture_record(self.evaluator, self.queries)
        record['candidates'] = [c for c in record['candidates'] if c['engine'] == 'independent']
        write_record(self.path, record)
        self.assertEqual(self.decision()['selected_backend'], 'bgs')
        self.assertEqual(self.decision(backend='direct')['selected_backend'], 'direct')
        for c in record['candidates']:
            c['samples_seconds'] = [9.8 if c['backend'] == 'bgs' else 10.0] * 3
        write_record(self.path, record)
        self.assertEqual(self.decision()['status'], 'measured_near_tie')
        self.assertEqual(self.decision()['selected_backend'], 'auto')

    def test_candidate_validation_and_medians_are_recomputed(self):
        record = fixture_record(self.evaluator, self.queries)
        write_record(self.path, record)
        original = self.path.read_text()
        for values in ([float('nan')] * 3, [float('inf')] * 3, [-1] * 3,
                       [True] * 3, [10**400] * 3, [1.0]):
            data = json.loads(original)
            data['records'][0]['candidates'][0]['samples_seconds'] = values
            self.path.write_text(json.dumps(data))
            self.assertEqual(self.decision()['reason'], 'profile_candidate_invalid')
        data = json.loads(original)
        data['records'][0]['candidates'][0]['median_seconds'] = 0.00001
        self.path.write_text(json.dumps(data))
        self.assertEqual(self.decision()['selected_engine'], 'forest')

    def test_resource_caps_are_rechecked_before_selected_forest(self):
        record = fixture_record(self.evaluator, self.queries)
        write_record(self.path, record)
        with patch.object(self.evaluator, '_check_forest', side_effect=ResourceLimitError('cap')):
            decision = self.decision()
        self.assertEqual(decision['selected_engine'], 'independent')
        self.assertEqual(len(decision['resource_rejections']), 2)

    def test_no_training_on_hot_path_and_input_validation_first(self):
        with patch('calibrate_dispatch.calibrate', side_effect=AssertionError('implicit training')):
            result = self.evaluator.evaluate(self.queries, engine='auto')
        self.assertEqual(result['statistics']['dispatch']['status'], 'fallback_untrained')
        with patch('dispatch_profile.select', side_effect=AssertionError('selection before validation')):
            with self.assertRaises(BoundaryError):
                self.evaluator.evaluate([PrimeQuery(9, 1)], engine='auto', profile=self.path)
        empty = self.evaluator.evaluate([], engine='auto', profile=self.path)
        self.assertEqual(empty['statistics']['dispatch']['reason'], 'empty_workload')

    def test_real_calibration_and_profile_upsert(self):
        record = calibrate(self.queries, self.path, repeats=3)
        self.assertGreaterEqual(len(record['candidates']), 5)
        self.assertTrue(self.decision()['status'].startswith('measured_'))
        calibrate(self.queries, self.path, repeats=3)
        self.assertEqual(len(load_profile(self.path)['records']), 1)
        calibrate(self.queries, self.path, repeats=3, output_mode='u_only')
        self.assertEqual(len(load_profile(self.path)['records']), 2)

    def test_mismatch_or_calibration_failure_preserves_profile(self):
        calibrate(self.queries, self.path)
        previous = self.path.read_bytes()
        with patch('calibrate_dispatch.reference', return_value=[]):
            with self.assertRaises(BoundaryError):
                calibrate(self.queries, self.path)
        self.assertEqual(self.path.read_bytes(), previous)
        data = json.loads(previous); data['environment'] = {}
        self.path.write_text(json.dumps(data)); previous = self.path.read_bytes()
        with self.assertRaises(BoundaryError):
            calibrate(self.queries, self.path)
        self.assertEqual(self.path.read_bytes(), previous)

    def test_reference_budget_bad_repeats_and_cli(self):
        for options in ({'max_reference_steps': 0}, {'repeats': 1}, {'repeats': True}):
            with self.assertRaises(BoundaryError):
                calibrate(self.queries, self.path, **options)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(calibrate_main(['--bound', '100', '--family', 'rounded_third',
                                              '--profile', str(self.path)]), 0)
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.assertEqual(main(['--bound', '100', '--family', 'rounded_third', '--engine', 'auto',
                                   '--profile', str(self.path)]), 0)
        self.assertTrue(json.loads(buffer.getvalue())['statistics']['dispatch']['status'].startswith('measured_'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
