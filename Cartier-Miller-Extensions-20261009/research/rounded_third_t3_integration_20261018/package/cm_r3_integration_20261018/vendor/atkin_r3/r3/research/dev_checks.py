"""Archived regeneration of the round-3 development checks quoted in REPORT_R3.md.

These checks were first run inline/scratch before the R3 freeze (and, for item 5, after it); this
script reruns them with the same rules so the archive carries their evidence.  All inputs lie in
the ledger's range rules (p < 2e5, or p = 5 mod 12 with p < 1e5).
  1. brute-force Jacobi sums: every prime 11 <= p < 3000, q in {5..31} with q | p-1, all u, v
     with u + v < q: reconstructed J equals direct summation coefficientwise, and
     rho(J) = -binom((u+v)K, uK).
  2. T3 against FLINT: primes p = 5 mod 6, p < 2e5, q in {5..47} with q | p-1 and K >= 40,
     anchor dup6 always and dup12 when p = 5 mod 12.
  3. anchor identities (m!/N!)^4 = a^2 and (m! (5N+2)!)^4 = (16 a^2)^{-1}, all p = 5 mod 12 < 1e5.
  4. relation lattices: span of Wilson + all Jacobi triples equals D0 for primes q <= 61; anchor
     degrees mod q; single-class (w = 1) plans for primes q <= 97 (dup6) and q <= 89 (dup12).
  5. R3.1 lattice chain returns the same J(1,1) as the frozen R3 module, p < 60000, q in
     {5, 7, 11, 13, 23, 31, 47}, K >= 40.
Usage: python3 r3/research/dev_checks.py OUT.json
"""
import json
import sys
from math import comb
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from r3.common import is_prime, flint_factorial, c_from_mfact
from r3.jacobi import JacobiContext, evaluate
from r3.jacobi_r31 import JacobiContextR31
from r3 import tal3
from r3.research.wc_lemma14c_check import two_squares_a

out = {}
t0 = perf_counter()
# 1
n = 0
for p in range(11, 3000):
    if not is_prime(p):
        continue
    for q in (5, 7, 11, 13, 17, 19, 23, 29, 31):
        if (p - 1) % q:
            continue
        ctx = JacobiContext(p, q)
        K = (p - 1) // q
        tab = {pow(ctx.eta, k, p): k for k in range(q)}
        ind = [None] + [tab[pow(x, (q - 1) * K, p)] for x in range(1, p)]
        for u in range(1, q - 1):
            for v in range(1, q - u):
                c = [0] * q
                for x in range(2, p):
                    c[(u * ind[x] + v * ind[(1 - x) % p]) % q] += 1
                brute = [c[i] - c[q - 1] for i in range(q - 1)]
                J = ctx.J(u, v)
                assert brute == J and evaluate(J, ctx.eta, p) == (-comb((u + v) * K, u * K)) % p
                n += 1
out['1_bruteforce_jacobi'] = n
# 2
cnt = {'dup6': 0, 'dup12': 0}
for p in range(11, 200000):
    if p % 6 != 5 or not is_prime(p):
        continue
    ref = None
    for q in (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        if (p - 1) % q or (p - 1) // q < 40:
            continue
        if ref is None:
            ref = c_from_mfact(p, flint_factorial((p - 2) // 3, p))
        for an in (('dup6', 'dup12') if p % 12 == 5 else ('dup6',)):
            c, _ = tal3.acquire(p, q, an, engine='std' if p < 20000 else 'flint')
            assert c == ref, (p, q, an)
            cnt[an] += 1
out['2_t3_dev_cases'] = cnt
# 3
n = 0
for p in range(17, 100000, 12):
    if not is_prime(p):
        continue
    N, m = (p - 5) // 12, (p - 2) // 3
    a = two_squares_a(p)
    mf, Nf, f5 = flint_factorial(m, p), flint_factorial(N, p), flint_factorial(5 * N + 2, p)
    assert pow(mf * pow(Nf, p - 2, p) % p, 4, p) == a * a % p
    assert pow(mf * f5 % p, 4, p) == pow(16 * a * a % p, p - 2, p)
    n += 1
out['3_anchor_identities_primes'] = n
# 4
import cypari2
P = cypari2.Pari()
lat = {}
for q in [x for x in range(5, 62) if is_prime(x)]:
    rows = [r for _, r in tal3._rows(q, tuple(range(1, q - 1)), 'dup6')][:-1]
    d = q - 1
    H = P.mathnf(P.matrix(d, len(rows), [rows[j][i] for i in range(d) for j in range(len(rows))]))
    D0 = [[0] * d for _ in range(d)]
    D0[0][0] = q
    for a_ in range(2, q):
        D0[a_ - 1][a_ - 1] = 1
        D0[a_ - 1][0] = -a_
    H0 = P.mathnf(P.matrix(d, d, [D0[j][i] for i in range(d) for j in range(d)]))
    degs = [sum(c * v for c, v in tal3.grid(q, an)[3]) % q for an in ('dup6', 'dup12')]
    lat[q] = dict(span_equals_D0=bool(H == H0), anchor_degrees=degs)
out['4a_lattice_D0'] = lat
single = {}
for q in [x for x in range(5, 98) if is_prime(x)]:
    for an in (('dup6', 'dup12') if q <= 89 else ('dup6',)):
        cl, k, _ = tal3.compute_plan(q, an)
        single['%d/%s' % (q, an)] = dict(classes=list(cl), k=k)
out['4b_single_class_plans'] = single
# 5
n = 0
for p in range(11, 60000):
    if p % 6 != 5 or not is_prime(p):
        continue
    for q in (5, 7, 11, 13, 23, 31, 47):
        if (p - 1) % q or (p - 1) // q < 40:
            continue
        assert JacobiContextR31(p, q).J(1, 1) == JacobiContext(p, q).J(1, 1)
        n += 1
out['5_r31_equals_r3'] = n
out['seconds'] = perf_counter() - t0
out['role'] = 'archived regeneration of development checks (inputs within the ledger range rules)'
Path(sys.argv[1]).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if not k.startswith('4')}, indent=1))
print('4a all span==D0:', all(v['span_equals_D0'] for v in lat.values()), 'degrees in {1,q-1}:',
      all(set(v['anchor_degrees']) <= {1, q - 1} for q, v in lat.items()))
print('4b classes:', sorted({tuple(v['classes']) for v in single.values()}), 'k values:', sorted({v['k'] for v in single.values()}))
