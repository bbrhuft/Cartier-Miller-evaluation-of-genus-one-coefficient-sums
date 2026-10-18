"""Round-3 audit of Theorem C6 (exact rational arithmetic, independent re-implementation).
Phi([x]) = (1/phi(M)) sum_{u in (Z/M)^*} chi_{-3}(u) B1bar(u x),  M = lcm(den x, 3).
Checks: independence of M; reflection; multiplication (Raabe) for M' <= 12; Gross-Koblitz orbit sums
for p = 2 mod 3 and random x; values at the points used by the round-3 anchors.
Usage: python3 r3/research/c6_audit.py OUT.json"""
import json, random, sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path

def chi3(u):
    return 0 if u % 3 == 0 else (1 if u % 3 == 1 else -1)

def B1(t):
    t = t - (t.numerator // t.denominator)
    return F(0) if t == 0 else t - F(1, 2)

def lcm(a, b): return a * b // gcd(a, b)

def Phi(x, M=None):
    x = x - (x.numerator // x.denominator)
    d = x.denominator
    M0 = lcm(d, 3)
    M = M or M0
    assert M % M0 == 0
    us = [u for u in range(1, M + 1) if gcd(u, M) == 1]
    return sum(chi3(u) * B1(u * x) for u in us) / len(us)

random.seed(20261018)
out = {}
# independence of M
ok = all(Phi(F(a, d)) == Phi(F(a, d), lcm(d, 3) * k) for d in range(1, 25) for a in range(d) if gcd(a, d) == 1 for k in (2, 5))
out['independent_of_M'] = ok
# reflection
out['reflection'] = all(Phi(F(a, d)) + Phi(F(-a, d)) == 0 for d in range(1, 40) for a in range(1, d))
# multiplication: sum_{i<n} Phi((x+i)/n) = Phi(x)  (relation [ (x+i)/n ] - [x], i.e. Raabe for B1 at nx)
def mult_ok(x, n):
    return sum(Phi((x + i) / n) for i in range(n)) == Phi(x)
out['multiplication'] = all(mult_ok(F(a, d), n) for d in range(1, 15) for a in range(d) for n in range(2, 13))
# Gross-Koblitz orbit sums for p = 2 mod 3 (prime) and denominators prime to p
gk = 0; gk_ok = True
for p in [5, 11, 17, 23, 29, 41, 47, 53, 59, 71, 83, 89, 101, 107, 113]:
    for _ in range(40):
        d = random.choice([x for x in range(2, 60) if x % p])
        a = random.randrange(1, d)
        x = F(a, d)
        f = 1
        while pow(p, f, d) != 1: f += 1
        s = sum(Phi(x * p ** i) for i in range(f))
        gk_ok &= (s == 0); gk += 1
out['gross_koblitz'] = dict(instances=gk, all_zero=gk_ok)
pts = {'1/3': F(1, 3), '2/3': F(2, 3), '1/6': F(1, 6), '5/6': F(5, 6), '1/12': F(1, 12), '5/12': F(5, 12),
       '7/12': F(7, 12), '11/12': F(11, 12), '1/4': F(1, 4), '1/2': F(1, 2), '1/q (q=7)': F(1, 7), '1/9': F(1, 9)}
out['values'] = {k: str(Phi(v)) for k, v in pts.items()}
Path(sys.argv[1]).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
