"""Frozen confirmation; no candidate edits during confirmation."""
from pathlib import Path
import hashlib
import json
import platform
import sys
from time import perf_counter
from develop import prime
from atkin import (atkin_endpoint, wronskian_endpoint, c_from_derivative,
                   derivative_from_c, nodal_c, factorial_c)

ROOT = Path(__file__).resolve().parent


def verify_freeze():
    freeze = json.loads((ROOT/'evidence/FREEZE.json').read_text())
    for name, digest in freeze['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    return freeze


def select(lower, count, exclude):
    result = []
    p = lower
    while len(result) < count:
        if p % 6 == 5 and p not in exclude and prime(p):
            result.append(p)
        p += 1
    return result


def main():
    freeze = verify_freeze()
    excluded = set(freeze['development_primes'])
    small = select(2001, 6, excluded)
    large = [select(lower, 1, excluded)[0] for lower in (10**4, 10**5, 10**6, 10**7, 10**8)]
    out = dict(status='PASS', python=sys.version, platform=platform.platform(),
               role='Post-freeze exact confirmation; not a polylogarithmic algorithm',
               selection=dict(small=small, benchmark_primes=large), cases=[])
    for p in sorted(set(small+large)):
        started = perf_counter()
        c, fact_meta = factorial_c(p, 'linear')
        deriv = wronskian_endpoint(p)
        assert c_from_derivative(p, deriv) == c
        assert derivative_from_c(p, c) == deriv
        direct = atkin_endpoint(p) if p <= 2*10**6 else None
        if direct is not None:
            assert direct == deriv
        methods = {}
        for mode in ('linear', 'separate', 'shared'):
            value, meta = nodal_c(p, mode)
            assert value == c, (p, mode)
            methods[mode] = meta
        block, block_meta = factorial_c(p)
        assert block == c
        # Test a non-square block width, independently of benchmark selection.
        if p <= 2*10**6:
            altered, _ = nodal_c(p, 'shared', block_size=7)
            assert altered == c
        out['cases'].append(dict(p=p, c=c, derivative=deriv,
            direct_atkin_derivative=direct, nodal_metadata=methods,
            factorial_block_metadata=block_meta, pass_=True,
            seconds=perf_counter()-started))
        print(json.dumps(dict(p=p, status='PASS', c=c,
                              seconds=round(perf_counter()-started, 3))), flush=True)
    verify_freeze()
    (ROOT/'evidence/CONFIRMATION.json').write_text(json.dumps(out, indent=2)+'\n')


if __name__ == '__main__':
    main()
