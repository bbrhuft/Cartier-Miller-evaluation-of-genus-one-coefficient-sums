"""Verify the integration freeze, preserved vendors and optional final manifest."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check():
    freeze=json.loads((ROOT/'evidence/FREEZE.json').read_text())
    for name,expected in freeze['sha256'].items():
        actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        if actual!=expected:
            raise SystemExit('Freeze mismatch: '+name)
    vendors=json.loads((ROOT/'provenance/VENDOR_HASHES.json').read_text())
    for name,entries in vendors.items():
        if isinstance(entries,str):
            paths=[(ROOT/'vendor'/name,entries)]
        else:
            paths=[(ROOT/'vendor'/name/sub,expected) for sub,expected in entries.items()]
        for path,expected in paths:
            if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise SystemExit('Vendor mismatch: '+str(path))
    manifest=ROOT/'MANIFEST.json'
    if manifest.exists():
        for name,expected in json.loads(manifest.read_text())['sha256'].items():
            if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
                raise SystemExit('Manifest mismatch: '+name)
    print('PASS: integration freeze, preserved vendors and final manifest when present')


if __name__=='__main__':
    check()
