"""Round-3 integrity audit (standard library only).

Checks, in order: the inherited round-1/round-2 audit (audit.py logic), the R3 freeze, the R3.1
freeze, and the round-3 delivery manifest r3/MANIFEST_R3.json.  The R3 freeze still verifies:
amendment R3.1 is strictly additive.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check(name):
    fr = json.loads((ROOT / name).read_text())
    bad = [f for f, d in fr['sha256'].items() if hashlib.sha256((ROOT / f).read_bytes()).hexdigest() != d]
    if bad:
        raise SystemExit('FAIL %s: %s' % (name, bad))
    return fr.get('timestamp_utc') or fr.get('created_utc')


if __name__ == '__main__':
    r = subprocess.run([sys.executable, str(ROOT / 'audit.py')], capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        raise SystemExit('FAIL inherited audit: ' + r.stdout + r.stderr)
    print(r.stdout.strip())
    print('PASS r3/FREEZE_R3.json', check('r3/FREEZE_R3.json'))
    print('PASS r3/FREEZE_R3_1.json', check('r3/FREEZE_R3_1.json'))
    if (ROOT / 'r3/MANIFEST_R3.json').exists():
        print('PASS r3/MANIFEST_R3.json', check('r3/MANIFEST_R3.json'))
