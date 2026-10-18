"""Subprocess checks of the public facade; values checked independently."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from test_boundary_framework import original_sum_oracle, binomial_oracle


def run(output):
    output = Path(output).resolve(); output.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parent
    facade = root / 'cartier_miller.py'
    records = []

    def invoke(args, expected=0):
        result = subprocess.run([sys.executable, str(facade), *args], cwd=root,
                                capture_output=True, text=True)
        if result.returncode != expected:
            raise RuntimeError(f'facade failed: {args}: {result.stdout} {result.stderr}')
        payload = json.loads(result.stdout)
        records.append({'command': ['python', 'cartier_miller.py', *args],
                        'exit_code': result.returncode, 'result': payload})
        return payload

    for p in (13, 17, 23, 61):
        result = invoke(['third', '--p', str(p), '--backend', 'bgs'])
        if result['U_p_L'] != original_sum_oracle(p, result['L']):
            raise RuntimeError('third facade oracle mismatch')
    fifth = invoke(['fifth', '--p', '29', '--backend', 'bgs'])
    for row in fifth['outputs']:
        if row['U_p_L'] != original_sum_oracle(29, row['L']):
            raise RuntimeError('fifth facade oracle mismatch')
    batch = invoke(['boundaries', '--p', '59', '--indices', '6', '12', '24', '20', '6', '--backend', 'bgs'])
    if batch['values'] != [binomial_oracle(59, n) for n in batch['indices']]:
        raise RuntimeError('batch facade oracle mismatch')
    boundary = invoke(['boundary', '--p', '101', '--index', '17', '--family', 'generic', '--backend', 'bgs'])
    if boundary['value'] != binomial_oracle(101, 17):
        raise RuntimeError('boundary facade oracle mismatch')
    profile = output / 'smoke_profile.json'
    invoke(['calibrate', '--bound', '100', '--family', 'rounded_third', '--profile', str(profile)])
    many = invoke(['many', '--bound', '100', '--family', 'rounded_third',
                   '--engine', 'auto', '--profile', str(profile)])
    if not many['statistics']['dispatch']['status'].startswith('measured_'):
        raise RuntimeError('facade calibration profile did not match')
    for row in many['outputs']:
        if row['U_p_L'] != original_sum_oracle(row['p'], row['L']):
            raise RuntimeError('many facade oracle mismatch')
    invoke(['third', '--p', '9'], 2)
    invoke(['third', '--p', '17', '--modulus-power', '2'], 2)
    record = {'passed': True, 'subprocess_checks': len(records), 'records': records,
              'scope': 'Public facade and independent small-input mathematical oracles; not a timing benchmark.'}
    (output / 'smoke_results.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'passed': True, 'subprocess_checks': len(records)}))
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    run(parser.parse_args().output)
