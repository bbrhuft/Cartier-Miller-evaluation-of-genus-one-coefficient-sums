"""Integrity, bounded validation, and optional focused benchmarks."""
from pathlib import Path
import argparse,subprocess,sys
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--benchmarks',action='store_true')
args=parser.parse_args()
subprocess.run([sys.executable,'verify_package.py'],cwd=ROOT,check=True)
subprocess.run([sys.executable,'validate.py'],cwd=ROOT,check=True)
if args.benchmarks:subprocess.run([sys.executable,'benchmark.py'],cwd=ROOT,check=True)
