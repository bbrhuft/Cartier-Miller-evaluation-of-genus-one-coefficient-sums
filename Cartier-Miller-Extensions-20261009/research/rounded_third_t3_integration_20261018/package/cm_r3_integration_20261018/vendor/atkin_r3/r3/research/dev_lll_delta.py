"""Round-3 POST-FREEZE DEVELOPMENT (after the run-1 confirmation failure): LLL success rate and
cost for delta in {0.99, 0.999} on the Stickelberger ideal of J(chi, chi), every prime 5<=q<=89.
Inputs: for each q, 12 primes p = 5 mod 6, p = 1 mod q drawn with random.Random(q*1000+3)
uniformly from [1e9, 1e12) (development; recorded in this file and added to the ledger).
Usage: python3 r3/research/dev_lll_delta.py OUT.json"""
import json, random, sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import flint
from r3.common import is_prime
from r3.jacobi import ideal_basis, stickelberger_set, element_of_order, mul, conj

def emb(b, q):
    s = sum(b); return [q * v - s for v in b] + [-s]

rows = []
for q in [x for x in range(5, 90) if is_prime(x)]:
    rng = random.Random(q * 1000 + 3)
    ps = []
    while len(ps) < 12:
        p = rng.randrange(10 ** 9, 10 ** 12)
        p -= (p - 1) % (6 * q)          # p = 1 mod 6q
        p += q * ((4 * q) % 6)           # CRT: p = 1 mod q and p = 5 mod 6
        if p % 6 == 5 and p % q == 1 and is_prime(p):
            ps.append(p)
    res = {0.99: [0, 0.0], 0.999: [0, 0.0]}
    for p in ps:
        eta, _ = element_of_order(p, q)
        M = flint.fmpz_mat([emb(b, q) for b in ideal_basis(p, q, eta, stickelberger_set(q, 1, 1))])
        tgt = q * (q - 1) * p
        for dl in (0.99, 0.999):
            t = perf_counter(); R = M.lll(delta=dl); res[dl][1] += perf_counter() - t
            if any(sum(int(R[i, j]) ** 2 for j in range(q)) == tgt for i in range(R.nrows())):
                res[dl][0] += 1
    rows.append(dict(q=q, primes=ps, success={str(k): v[0] for k, v in res.items()},
                     mean_lll_s={str(k): v[1] / len(ps) for k, v in res.items()}))
    print(q, {k: v[0] for k, v in res.items()}, {k: round(v[1] / len(ps) * 1e3, 1) for k, v in res.items()}, flush=True)
Path(sys.argv[1]).write_text(json.dumps(dict(role='post-freeze development (LLL delta)', trials_per_q=12, rows=rows), indent=1) + '\n')
