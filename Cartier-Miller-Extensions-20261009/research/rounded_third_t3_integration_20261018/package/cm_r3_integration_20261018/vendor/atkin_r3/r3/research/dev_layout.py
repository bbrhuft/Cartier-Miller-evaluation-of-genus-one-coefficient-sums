"""Round-3 DEVELOPMENT: interval layout choice (separate channels vs one shared tree).
Inputs are DEV_TIMING primes (development).  Usage: python3 r3/research/dev_layout.py OUT.json"""
import json, statistics, sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from r3.common import flint_rising
from r3.tal3 import residuals

def separate(p, R):
    out = []
    for (a, b) in (R['I_m'], R['I_a']):
        (v,), _ = flint_rising(p, b - a + 1, [a]); out.append(v)
    return out

def shared(p, R):
    (a1, b1), (a2, b2) = R['I_m'], R['I_a']
    Lm, La = b1 - a1 + 1, b2 - a2 + 1
    c = max(1, round(Lm / La))
    l = min(Lm // c, La)
    starts = [a1 + i * l for i in range(c)] + [a2]
    vals, _ = flint_rising(p, l, starts)
    Im = 1
    for v in vals[:c]: Im = Im * v % p
    for j in range(a1 + c * l, b1 + 1): Im = Im * j % p          # O(1)-ish fix-up
    Ia = vals[c]
    for j in range(a2 + l, b2 + 1): Ia = Ia * j % p
    return [Im, Ia], (Lm - c * l) + (La - l)

rows = []
for (p, q) in [(50000004161, 31), (50000002097, 37), (500000000537, 37), (500000002727, 31), (500000001689, 53)]:
    for an in (('dup6', 'dup12') if p % 12 == 5 else ('dup6',)):
        R = residuals(p, q, an)
        ref = separate(p, R)
        vs, fix = shared(p, R)
        assert vs == ref
        ts = {'separate': [], 'shared': []}
        for rep in range(5):
            for name, f in ((('separate', separate), ('shared', shared)) if rep % 2 == 0 else (('shared', shared), ('separate', separate))):
                t = perf_counter(); f(p, R); ts[name].append(perf_counter() - t)
        med = {k: statistics.median(v) for k, v in ts.items()}
        rows.append(dict(p=p, q=q, anchor=an, lengths=[R['len_m'], R['len_a']], fixup_factors=fix, samples_s=ts, medians_s=med))
        print(p, q, an, R['len_m'], R['len_a'], 'fix', fix, {k: round(v * 1e3, 1) for k, v in med.items()}, flush=True)
Path(sys.argv[1]).write_text(json.dumps(dict(role='Round-3 development layout choice', rows=rows), indent=1) + '\n')
