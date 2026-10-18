"""Verify delivered bytes, the round-1 freeze and the round-2 freeze; standard library only."""
from pathlib import Path
import hashlib
import json
import sys
sys.dont_write_bytecode = True
from confirm import verify_freeze

root = Path(__file__).resolve().parent
verify_freeze()
fr2 = json.loads((root / 'evidence/charp/FREEZE_CHARP.json').read_text())
for name, digest in fr2['sha256'].items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
manifest = json.loads((root / 'MANIFEST.json').read_text())
for name, digest in manifest['sha256'].items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
print('PASS: delivered manifest, round-1 freeze and round-2 freeze hashes')
