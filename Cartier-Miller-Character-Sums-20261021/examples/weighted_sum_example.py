"""Run from any directory: python3 examples/weighted_sum_example.py."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from weighted_sums import single_pole, prepare_weights

# Exact signed projective trace is supplied, not computed here.
p, f, trace = 7, [1, 1, 0, 1], 3
print('Single pole, excludes only x=1:', single_pole(p, f, 1, trace))
prepared = prepare_weights(p, f, trace, excluded=[1, 2])
print('The same reciprocal weight, also excluding x=2:', prepared.evaluate([1, 0]))
print('Change coefficients using cached preparation:', prepared.evaluate([2, 3], constant=4))

print('p=5, twisted curve order 2p:', single_pole(5, [0, 3, 0, 1], 1, -4))
