"""Check that every frozen file still matches FREEZE.json (fast; no recomputation).

Usage (package root): python3 src/verify_freeze.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import environment as envmod   # noqa: E402
import freeze as fz            # noqa: E402


def main():
    with open(os.path.join(envmod.ROOT, 'FREEZE.json')) as fh:
        frz = json.load(fh)
    current = envmod.file_hashes(list(frz['files']))
    bad = sorted(k for k in frz['files'] if current.get(k) != frz['files'][k])
    ok = not bad and fz.digest(current) == frz['digest']
    print(json.dumps({'frozen_files': len(frz['files']), 'mismatches': bad,
                      'digest': frz['digest'], 'status': 'MATCH' if ok else 'MISMATCH'}, indent=1))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
