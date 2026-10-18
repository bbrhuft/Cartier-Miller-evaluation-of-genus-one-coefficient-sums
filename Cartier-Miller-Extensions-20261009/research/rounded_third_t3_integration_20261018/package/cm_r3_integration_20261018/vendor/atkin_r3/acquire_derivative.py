"""Thin production API over the frozen acquisition core; no reference cross-check.

Example: python3 acquire_derivative.py 100000007 --method shared
Prime certification is the caller's input contract. Timings include conversion.
"""
import argparse
import json
from time import perf_counter
from atkin import nodal_c, factorial_c, derivative_from_c


def acquire(p, method='shared'):
    started = perf_counter()
    if method in ('factorial-block', 'factorial-linear'):
        c, metadata = factorial_c(p, method.split('-')[1])
    else:
        mode = 'linear' if method == 'nodal-linear' else method
        c, metadata = nodal_c(p, mode)
    derivative = derivative_from_c(p, c)
    return dict(p=p, derivative=derivative, c=c, method=method,
                seconds=perf_counter()-started, metadata=metadata)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('p', type=int)
    parser.add_argument('--method', choices=['shared', 'separate', 'nodal-linear',
                                            'factorial-block', 'factorial-linear'], default='shared')
    args = parser.parse_args()
    print(json.dumps(acquire(args.p, args.method), indent=2))
