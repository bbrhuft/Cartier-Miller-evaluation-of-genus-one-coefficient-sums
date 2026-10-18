"""Capture reproducible release evidence and a shareable ZIP on this machine."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from time import perf_counter
import zipfile

from boundary_framework import __version__
from release_integrity import verify_manifest, verify_provenance

BENCHMARKS = [
    ('boundary', 'benchmark.py', 'benchmark_summary.json'),
    ('thirds', 'benchmark_integrated.py', 'integrated_benchmark_summary.json'),
    ('fifths', 'benchmark_fifths.py', 'fifth_benchmark_summary.json'),
    ('output_modes', 'benchmark_output_modes.py', 'output_mode_benchmark_summary.json'),
    ('bgs', 'benchmark_bgs.py', 'bgs_benchmark_summary.json'),
    ('shared', 'benchmark_shared.py', 'shared_benchmark_summary.json'),
    ('many_primes', 'benchmark_many_primes.py', 'many_prime_benchmark_summary.json'),
    ('dispatch', 'benchmark_dispatch.py', 'dispatch_benchmark_summary.json'),
]


def run_command(command, root, log):
    begin = perf_counter()
    with Path(log).open('w', encoding='utf-8') as stream:
        result = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT, text=True)
    return {'command': command, 'exit_code': result.returncode,
            'elapsed_seconds': perf_counter() - begin, 'log': Path(log).name}


def capture(root, output, *, benchmarks='smoke', repeats=3, integrity_only=False):
    root, output = Path(root).resolve(), Path(output).resolve()
    bundle = output.parent / (output.name + '.zip')
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('evidence output must be a new or empty directory')
    if bundle.exists():
        raise ValueError('evidence ZIP already exists; choose a new output path')
    output.mkdir(parents=True, exist_ok=True)
    record = {
        'version': __version__, 'generated_utc': datetime.now(timezone.utc).isoformat(),
        'environment': {'python': sys.version, 'implementation': platform.python_implementation(),
                        'platform': platform.platform(), 'system': platform.system(),
                        'machine': platform.machine(), 'processor': platform.processor(),
                        'logical_cpus': os.cpu_count(), 'optimized': sys.flags.optimize},
        'execution_attribution': 'Executed by this runner on the recorded machine; not inferred from user reports.',
        'scope': 'integrity_only' if integrity_only else 'validation_and_' + benchmarks,
        'passed': False, 'complete': False, 'steps': [], 'benchmark_summaries': {},
        'windows_execution': platform.system() == 'Windows',
    }
    begin = perf_counter()
    summary_path = output / 'release_results.json'

    def persist():
        record['elapsed_seconds'] = perf_counter() - begin
        summary_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')

    def stage(name, script, args, summary, expected_pass_key=None):
        print(f'Starting {name}', flush=True)
        folder = output / name; folder.mkdir()
        command = [sys.executable, str(root / script), *args, '--output', str(folder)]
        record['active_stage'] = name; persist()
        result = run_command(command, root, output / (name + '.log'))
        result['stage'] = name
        record['steps'].append(result); persist()
        if result['exit_code'] != 0:
            raise RuntimeError(f'{name} returned exit code {result["exit_code"]}')
        data = json.loads((folder / summary).read_text(encoding='utf-8'))
        if expected_pass_key is not None and data.get(expected_pass_key) is not True:
            raise RuntimeError(f'{name} did not report {expected_pass_key}=true')
        print(f'Completed {name}', flush=True)
        return data

    try:
        record['runtime_before'] = verify_manifest(root)
        record['retained_sources'] = verify_provenance(root)
        persist()
        if not record['runtime_before']['passed'] or not record['retained_sources']['passed']:
            raise RuntimeError('runtime integrity or retained-source provenance failed')
        if not integrity_only:
            validation = stage('validation', 'run_validation.py', [], 'validation_results.json', 'passed')
            record['validation'] = {key: validation[key] for key in
                                    ('test_methods', 'failures', 'errors', 'passed', 'elapsed_seconds')}
            if benchmarks in ('smoke', 'all'):
                smoke = stage('smoke', 'release_smoke.py', [], 'smoke_results.json', 'passed')
                record['smoke'] = {'passed': True, 'subprocess_checks': smoke['subprocess_checks']}
            if benchmarks == 'all':
                for name, script, filename in BENCHMARKS:
                    data = stage('benchmark_' + name, script, ['--repeats', str(repeats)], filename,
                                 None if name == 'boundary' else 'all_correct')
                    record['benchmark_summaries'][name] = {
                        key: data[key] for key in ('version', 'repeats', 'timed_evaluations', 'evaluations',
                                                   'held_out_evaluations', 'calibration_evaluations',
                                                   'timed_evaluations', 'memory_evaluations', 'all_correct')
                        if key in data}
                    # Boundary benchmark checks every row in code; also verify
                    # the saved rows rather than relying only on exit status.
                    if name == 'boundary':
                        import csv
                        with (output / ('benchmark_' + name) / 'benchmark.csv').open(newline='') as stream:
                            rows = list(csv.DictReader(stream))
                        if len(rows) != data['timed_evaluations'] or any(r['correct'] != 'True' for r in rows):
                            raise RuntimeError('boundary benchmark CSV evidence mismatch')
                    persist()
        record['runtime_after'] = verify_manifest(root)
        if (not record['runtime_after']['passed'] or
                record['runtime_after']['manifest_sha256'] != record['runtime_before']['manifest_sha256']):
            raise RuntimeError('runtime changed during evidence capture')
        record['passed'] = True
    except Exception as exc:
        record['failure'] = {'type': type(exc).__name__, 'message': str(exc)}
    finally:
        record['active_stage'] = None
        record['complete'] = True
        persist()
        files = sorted(p for p in output.rglob('*') if p.is_file())
        checksums = ''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' +
                            p.relative_to(output).as_posix() + '\n' for p in files)
        (output / 'EVIDENCE_SHA256SUMS.txt').write_text(checksums, encoding='utf-8')
        with zipfile.ZipFile(bundle, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(output.rglob('*')):
                if path.is_file():
                    archive.write(path, Path(output.name) / path.relative_to(output))
        with zipfile.ZipFile(bundle) as archive:
            if archive.testzip() is not None:
                raise RuntimeError('evidence ZIP integrity failed')
    print(json.dumps({'passed': record['passed'], 'scope': record['scope'],
                      'evidence_directory': str(output), 'evidence_zip': str(bundle),
                      'failure': record.get('failure')}, indent=2))
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmarks', choices=('none', 'smoke', 'all'), default='smoke')
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args(argv)
    if not 3 <= args.repeats <= 20:
        parser.error('repeats must be 3..20')
    root = Path(__file__).resolve().parent
    output = args.output or root / 'results' / ('release_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'))
    try:
        record = capture(root, output, benchmarks=args.benchmarks, repeats=args.repeats,
                         integrity_only=args.integrity_only)
        return 0 if record['passed'] else 1
    except (OSError, ValueError) as exc:
        print(json.dumps({'error': str(exc)})); return 2


if __name__ == '__main__':
    raise SystemExit(main())
