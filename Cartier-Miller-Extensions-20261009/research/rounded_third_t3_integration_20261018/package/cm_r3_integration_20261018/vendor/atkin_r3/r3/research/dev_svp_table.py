"""Round-3 DEVELOPMENT: per-q cost of one certified Jacobi sum J(1,1) (FLINT LLL path).

For every prime 5 <= q <= 89: the first prime p >= 5e10 + 7q with p = 5 mod 6 and p = 1 mod q.
Three cold samples (fresh JacobiContext).  Inputs are development inputs.
Usage: python3 r3/research/dev_svp_table.py OUT.json
"""
import json, statistics, sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from r3.common import is_prime
from r3.jacobi import JacobiContext


def first(S, q):
    p = S
    while not (p % 6 == 5 and p % q == 1 and is_prime(p)):
        p += 1
    return p


rows = []
for q in [x for x in range(5, 90) if is_prime(x)]:
    p = first(5 * 10 ** 10 + 7 * q, q)
    ts, fb = [], 0
    for _ in range(3):
        ctx = JacobiContext(p, q)
        t = perf_counter()
        ctx.J(1, 1)
        ts.append(perf_counter() - t)
        fb += ctx.stats['enumeration_fallbacks']
    rows.append(dict(q=q, p=p, samples_s=ts, median_s=statistics.median(ts), enumeration_fallbacks=fb))
    print(q, p, round(statistics.median(ts) * 1e3, 2), 'ms', 'fallbacks', fb, flush=True)
Path(sys.argv[1]).write_text(json.dumps(dict(role='Round-3 development SVP cost table', rows=rows), indent=1) + '\n')
