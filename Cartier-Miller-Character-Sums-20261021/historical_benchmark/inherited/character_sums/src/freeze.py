"""Freeze the candidate: hash every candidate, harness and vendored file.

Usage: python3 src/freeze.py      (writes FREEZE.json; refuses to overwrite)
The freeze digest seeds the confirmation sample, so the sample cannot be chosen
after seeing confirmation inputs.  No external timestamp is obtained.
"""
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import environment as envmod   # noqa: E402

FROZEN = envmod.CANDIDATE_FILES + ['src/freeze.py', 'PROVENANCE_INPUTS.json',
                                   'results/development_ledger.json'] + envmod.vendor_files()


def digest(hashes):
    lines = ''.join('%s  %s\n' % (hashes[k], k) for k in sorted(hashes))
    return hashlib.sha256(lines.encode()).hexdigest()


def main():
    out = os.path.join(envmod.ROOT, 'FREEZE.json')
    if os.path.exists(out):
        print('FREEZE.json exists; refusing to overwrite')
        return 1
    hashes = envmod.file_hashes(FROZEN)
    missing = [p for p in FROZEN if p not in hashes]
    if missing:
        print('missing files:', missing)
        return 1
    rec = {'frozen_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'files': hashes, 'digest': digest(hashes),
           'digest_rule': 'sha256 over sorted lines "<sha256>  <path>\\n"',
           'timestamp_note': 'local clock only; no external timestamp'}
    with open(out, 'w') as fh:
        json.dump(rec, fh, indent=1)
    print('frozen', len(hashes), 'files; digest', rec['digest'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
