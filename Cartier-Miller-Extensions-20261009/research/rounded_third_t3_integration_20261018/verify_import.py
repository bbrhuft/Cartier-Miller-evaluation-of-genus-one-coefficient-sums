"""Integrity check for the imported rounded-third T3 integration package.

Runs the same three hash lists as the package's own audit.py
(evidence/FREEZE.json, provenance/VENDOR_HASHES.json, MANIFEST.json) over
package/cm_r3_integration_20261018/, without modifying the package.

Exactly one listed file is allowed to be absent: a verbatim excerpt of the
PARI/GP documentation, which is GPL-licensed and is therefore not
redistributed in this repository (see RELEASE_NOTE.md). It is identified by
its SHA-256. Any other missing file, any mismatch, or any file in the
package not covered by a hash list makes this script exit with status 1.

This is an integrity check only. It does not rerun any mathematics.
Standard library only.
"""
import hashlib
import json
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent / 'package' / 'cm_r3_integration_20261018'
NOT_REDISTRIBUTED = {
    'vendor/atkin_r3/r3/sources/PARI_2.17.2_installed_doc.json':
        '9e1ffb9d88273dc61d0001ecfa48094f24a982e4a92e82fbd39dd60c67c2ad84',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entries():
    freeze = json.loads((PKG / 'evidence/FREEZE.json').read_text())['sha256']
    yield from (('FREEZE', k, v) for k, v in freeze.items())
    vendors = json.loads((PKG / 'provenance/VENDOR_HASHES.json').read_text())
    for name, e in vendors.items():
        if isinstance(e, str):
            yield 'VENDOR', f'vendor/{name}', e
        else:
            yield from (('VENDOR', f'vendor/{name}/{sub}', v) for sub, v in e.items())
    manifest = json.loads((PKG / 'MANIFEST.json').read_text())['sha256']
    yield from (('MANIFEST', k, v) for k, v in manifest.items())


def main():
    failures, counts, covered, skipped = [], {}, {'MANIFEST.json'}, set()
    for lst, rel, want in entries():
        counts[lst] = counts.get(lst, 0) + 1
        covered.add(rel)
        path = PKG / rel
        if not path.exists():
            if NOT_REDISTRIBUTED.get(rel) == want:
                skipped.add(rel)
                continue
            failures.append(f'{lst}: missing {rel}')
        elif sha(path) != want:
            failures.append(f'{lst}: hash mismatch {rel}')
    present = {p.relative_to(PKG).as_posix() for p in PKG.rglob('*')
               if p.is_file() and '__pycache__' not in p.parts}
    failures += [f'not covered by any hash list: {r}' for r in sorted(present - covered)]
    failures += [f'excluded file unexpectedly present: {r}' for r in sorted(set(NOT_REDISTRIBUTED) & present)]
    out = {'status': 'failed' if failures else 'passed', 'entries_checked': counts,
           'files_present': len(present), 'not_redistributed_skipped': sorted(skipped),
           'failures': failures, 'scope': 'integrity only; mathematics is checked by the package scripts'}
    print(json.dumps(out, indent=2))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
