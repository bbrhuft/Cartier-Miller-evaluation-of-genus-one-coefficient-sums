"""Public facade, audit fixes, runtime integrity and evidence-runner contracts."""
from contextlib import redirect_stdout, redirect_stderr
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import cartier_miller as cm
from calibrate_dispatch import calibrate
from release_integrity import build_manifest, verify_manifest, verify_provenance
from release_check import capture


class ReleaseTests(unittest.TestCase):
    def test_public_exports_and_native_examples(self):
        for name in cm.__all__:
            self.assertTrue(hasattr(cm, name), name)
        self.assertEqual(cm.ThirdPointSession(23).evaluate()['U_p_L'], 17)
        self.assertEqual([r['U_p_L'] for r in cm.FifthPointSession(29).evaluate()['outputs']], [8, 10])
        self.assertEqual(cm.BoundaryBatchSession(59).evaluate([6, 12, 24, 20, 6])['values'],
                         [14, 5, 30, 6, 14])

    def test_facade_delegation_and_status_codes(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.assertEqual(cm.main(['third', '--p', '17']), 0)
        self.assertEqual(json.loads(buffer.getvalue())['U_p_L'], 7)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(cm.main(['third', '--p', '9']), 2)
            self.assertEqual(cm.main([]), 0)
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                cm.main(['unknown'])
        self.assertEqual(raised.exception.code, 2)

    def test_deep_profile_json_uses_documented_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'deep.json'
            path.write_text('[' * 2000 + ']' * 2000)
            result = cm.ManyPrimeEvaluator().evaluate([cm.PrimeQuery(17, 6)], engine='auto', profile=path)
        self.assertEqual(result['statistics']['dispatch']['reason'], 'profile_invalid_or_unreadable')
        self.assertEqual(result['outputs'][0]['U_p_L'], 7)

    def test_missing_profile_source_uses_documented_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'profile.json'
            queries = [cm.PrimeQuery(17, 6)]
            calibrate(queries, path)
            with patch('dispatch_profile.implementation_hash', side_effect=FileNotFoundError('missing source')):
                result = cm.ManyPrimeEvaluator().evaluate(queries, engine='auto', profile=path)
        self.assertEqual(result['statistics']['dispatch']['reason'], 'profile_source_unavailable')
        self.assertEqual(result['outputs'][0]['U_p_L'], 7)

    def fixture(self, parent):
        root = Path(parent) / 'fixture'; root.mkdir()
        (root / 'retained_cm').mkdir()
        module = root / 'retained_cm' / 'kernel.py'; module.write_text('value = 1\n')
        (root / 'example.py').write_text('value = 2\n')
        provenance = {'copied_files': [], 'many_prime_forest':
                      {'copied_path': 'retained_cm/kernel.py',
                       'sha256': hashlib.sha256(module.read_bytes()).hexdigest()}}
        (root / 'SOURCE_PROVENANCE.json').write_text(json.dumps(provenance))
        (root / 'RUNTIME_MANIFEST.json').write_text(json.dumps(build_manifest(root)))
        return root

    def test_manifest_detects_modified_missing_and_extra_runtime_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            self.assertTrue(verify_manifest(root)['passed'])
            self.assertTrue(verify_provenance(root)['passed'])
            (root / 'extra.py').write_text('unexpected = 1')
            self.assertFalse(verify_manifest(root)['passed'])
            (root / 'extra.py').unlink()
            (root / 'example.py').write_text('changed = 1')
            self.assertFalse(verify_manifest(root)['passed'])
            (root / 'example.py').unlink()
            self.assertFalse(verify_manifest(root)['passed'])
            (root / 'retained_cm/kernel.py').write_text('changed = 1')
            self.assertFalse(verify_provenance(root)['passed'])

    def test_integrity_capture_and_evidence_zip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            output = Path(directory) / 'evidence'
            with redirect_stdout(io.StringIO()):
                record = capture(root, output, integrity_only=True)
            self.assertTrue(record['passed'])
            self.assertEqual(record['scope'], 'integrity_only')
            self.assertEqual(record['steps'], [])
            bundle = output.parent / (output.name + '.zip')
            with zipfile.ZipFile(bundle) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn('evidence/release_results.json', archive.namelist())
            for line in (output / 'EVIDENCE_SHA256SUMS.txt').read_text().splitlines():
                digest, name = line.split('  ', 1)
                self.assertEqual(hashlib.sha256((output / name).read_bytes()).hexdigest(), digest)
            with self.assertRaises(ValueError):
                capture(root, output, integrity_only=True)

    def test_failed_validation_still_publishes_failed_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory); output = Path(directory) / 'failed'
            with patch('release_check.run_command', return_value=
                       {'command': ['test fixture'], 'exit_code': 1, 'elapsed_seconds': 0.0, 'log': 'fixture.log'}):
                with redirect_stdout(io.StringIO()):
                    record = capture(root, output, benchmarks='none')
            self.assertFalse(record['passed'])
            self.assertEqual(record['failure']['type'], 'RuntimeError')
            self.assertTrue((output.parent / 'failed.zip').exists())

    def test_runtime_mutation_during_capture_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory); output = Path(directory) / 'mutated'

            def fake_validation(command, cwd, log):
                folder = Path(command[-1])
                (folder / 'validation_results.json').write_text(json.dumps(
                    {'passed': True, 'test_methods': 1, 'failures': 0, 'errors': 0, 'elapsed_seconds': 0.0}))
                (root / 'example.py').write_text('modified during capture\n')
                return {'exit_code': 0, 'command': command, 'elapsed_seconds': 0.0, 'log': str(log)}

            with patch('release_check.run_command', side_effect=fake_validation):
                with redirect_stdout(io.StringIO()):
                    record = capture(root, output, benchmarks='none')
            self.assertFalse(record['passed'])
            self.assertFalse(record['runtime_after']['passed'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
