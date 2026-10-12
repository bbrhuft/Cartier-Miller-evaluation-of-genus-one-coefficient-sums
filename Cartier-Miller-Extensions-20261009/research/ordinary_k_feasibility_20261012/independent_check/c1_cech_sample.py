"""Compatibility wrapper: sampling is now part of c1_cech.py (--sample-primes, --sample-size, --seed)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c1_cech  # noqa: E402

if __name__ == "__main__":
    c1_cech._main()
