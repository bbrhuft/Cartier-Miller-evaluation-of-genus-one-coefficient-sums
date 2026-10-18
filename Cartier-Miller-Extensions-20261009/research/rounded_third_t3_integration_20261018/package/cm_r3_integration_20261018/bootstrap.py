"""Load byte-preserved project kernels from this standalone experiment."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
for path in (ROOT / 'vendor', ROOT / 'vendor/boundary', ROOT / 'vendor/atkin_r3'):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
