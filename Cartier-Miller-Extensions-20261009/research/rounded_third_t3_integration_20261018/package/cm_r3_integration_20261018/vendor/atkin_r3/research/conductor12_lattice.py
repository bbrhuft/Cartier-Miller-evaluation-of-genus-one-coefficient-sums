"""C7 evidence: empirical exact relation lattice of the conductor-12 grid factorials.

Generators per prime p (p = 5 mod 6), split by p mod 24:
  F_k = (R(k/12) - 1)!  (k=1..11), R(x) in [1,p] the residue of x, so Gamma_p(k/12) = +-F_k;
  constants: -1, 2, 3, 2^(1/3), 3^(1/3) (unique cube roots, p=2 mod 3), parity signs (-1)^N,
  (-1)^[N/2], (-1)^[N/4]; for p=1 mod 4 also a (a=1 mod 4), b>0, iota3 = 3^((p-1)/4),
  (-1)^[b/4]; optionally the Legendre symbols (F_k/p) (class-number computable).
A relation is an integer vector e with prod g^e = 1 for EVERY prime of the class in range;
computed as the intersection of the per-prime kernels (discrete logs), short vectors by LLL.
Then: Smith form of the F-projection, and an exhaustive search over at most two intervals
between grid residues for exact representations of m!^w (w = +-1, +-3).
Requires python-flint and sympy. Evidence only (finite range of primes), not a proof.
"""
import itertools, json, math, sys
from flint import fmpz_mat
from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

def isprime(n): return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))
def primroot(p):
    fs = [q for q in range(2, p) if (p - 1) % q == 0 and isprime(q)]
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in fs))
def ab(p):
    for a in range(1, math.isqrt(p) + 1, 2):
        b2 = p - a * a; b = math.isqrt(b2)
        if b * b == b2: return (a if a % 4 == 1 else -a), b
def gens(p, legendre):
    cls = p % 12; N = (p - 5) // 12
    f = [1] * p
    for i in range(1, p): f[i] = f[i - 1] * i % p
    v = {'F%d' % k: f[k * pow(12, p - 2, p) % p - 1] for k in range(1, 12)}
    v.update({'-1': p - 1, '2': 2, '3': 3, 'cbrt2': pow(2, (2 * p - 1) // 3, p), 'cbrt3': pow(3, (2 * p - 1) // 3, p),
              '(-1)^N': pow(-1, N, p), '(-1)^[N/2]': pow(-1, N // 2, p), '(-1)^[N/4]': pow(-1, N // 4, p)})
    if cls == 5:
        a, b = ab(p)
        v.update({'a': a % p, 'b': b, 'iota3': pow(3, (p - 1) // 4, p), '(-1)^[b/4]': pow(-1, b // 4, p)})
    if legendre:
        for k in range(1, 12): v['leg%d' % k] = pow(v['F%d' % k], (p - 1) // 2, p)
    return v
def kernel(B, v, M):
    k = len(B); w = [sum(x * y for x, y in zip(row, v)) % M for row in B]
    rows = [[w[i]] + [int(i == j) for j in range(k)] for i in range(k)] + [[M] + [0] * k]
    while True:
        nz = [r for r in rows if r[0]]
        if len(nz) <= 1: break
        piv = min(nz, key=lambda r: abs(r[0]))
        rows = [piv] + [r if (r is piv or not r[0]) else [a - (r[0] // piv[0]) * b for a, b in zip(r, piv)]
                        for r in rows if r is not piv]
    ker = [r[1:] for r in rows if r[0] == 0]
    basis = [[sum(x[i] * B[i][c] for i in range(k)) for c in range(len(B[0]))] for x in ker]
    H = fmpz_mat(basis).hnf()
    rws = [[int(H[i, j]) for j in range(H.ncols())] for i in range(H.nrows())]
    L = fmpz_mat([r for r in rws if any(r)]).lll()
    return [[int(L[i, j]) for j in range(L.ncols())] for i in range(L.nrows())]
def lattice(cls24, limit, legendre):
    names = B = None; n = 0
    for p in range(17, limit):
        if p % 24 != cls24 or not isprime(p): continue
        v = gens(p, legendre); g = primroot(p); dl = {}; x = 1
        for e in range(p - 1): dl[x] = e; x = x * g % p
        if names is None:
            names = list(v); B = [[int(i == j) for j in range(len(names))] for i in range(len(names))]
        B = kernel(B, [dl[v[k]] for k in names], p - 1); n += 1
    small = [r for r in B if max(map(abs, r)) < 1000]
    return names, small, n
def analyse(cls24, limit, legendre):
    names, small, n = lattice(cls24, limit, legendre)
    proj = [r[:11] for r in small]
    snf = [int(smith_normal_form(Matrix(proj), domain=ZZ)[i, i]) for i in range(11)]
    H = fmpz_mat(proj).hnf()
    rows = [[int(H[i, j]) for j in range(11)] for i in range(H.nrows()) if any(int(H[i, j]) for j in range(11))]
    def member(v):
        v = list(v)
        for r in rows:
            piv = next(j for j in range(11) if r[j]); 
            if v[piv] % r[piv]: return False
            q = v[piv] // r[piv]; v = [a - q * b for a, b in zip(v, r)]
        return not any(v)
    p0 = next(p for p in range(1000, 5000) if p % 24 == cls24 and isprime(p))
    res = {k: k * pow(12, p0 - 2, p0) % p0 for k in range(1, 12)}
    pos2k = {i + 1: k for i, k in enumerate(sorted(res, key=res.get))}
    def vec(i, l):
        v = [0] * 11
        if 1 <= l <= 11: v[pos2k[l] - 1] += 1
        if 1 <= i <= 11: v[pos2k[i] - 1] -= 1
        return v
    ivs = [(i, l) for i in range(13) for l in range(i + 1, 13)]
    e4 = [0] * 11; e4[3] = 1      # F4 = m! (fraction 4/12 = 1/3)
    found = []
    for kint in (1, 2):
        for combo in itertools.combinations_with_replacement(ivs, kint):
            for signs in itertools.product((1, -1), repeat=kint):
                E = [0] * 11
                for iv, s in zip(combo, signs): E = [a + s * b for a, b in zip(E, vec(*iv))]
                for w in (1, -1, 3, -3):
                    if member([a - w * b for a, b in zip(E, e4)]):
                        found.append(dict(total_length_N=sum(l - i for i, l in combo),
                                          sum_sqrt=round(sum(math.sqrt(l - i) for i, l in combo), 4),
                                          intervals=combo, signs=signs, m_power=w))
    min_len = min(f['total_length_N'] for f in found); min_sqrt = min(f['sum_sqrt'] for f in found)
    single_N = any(f['total_length_N'] == 1 for f in found)
    X = [0] * 11; X[3] += 1; X[6] -= 1     # m!/N!  (N! = F7 for p=5 mod 12, F1 for p=11 mod 12)
    if cls24 % 12 == 11: X = [0] * 11; X[3] += 1; X[0] -= 1
    return dict(p_mod_24=cls24, primes=n, legendre_constants=legendre, generators=names,
                relations=small, snf_F_quotient=snf, grid_position_to_fraction=pos2k,
                min_exact_total_length_in_N=min_len, min_exact_sum_sqrt_in_sqrtN=min_sqrt,
                any_exact_length_N_interval=single_N,
                quarter_X_exact={'X': member(X), 'X^2': member([2 * x for x in X]), 'X^4': member([4 * x for x in X])},
                examples=sorted(found, key=lambda f: (f['total_length_N'], f['sum_sqrt']))[:6])
if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
    out = [analyse(c, limit, leg) for c in (5, 17, 11, 23) for leg in (False, True)]
    json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else 'LATTICE_C12.json', 'w'), indent=1, default=str)
    for r in out:
        print(r['p_mod_24'], 'legendre' if r['legendre_constants'] else 'plain', 'primes', r['primes'], 'SNF', r['snf_F_quotient'],
              'min len', r['min_exact_total_length_in_N'], 'min sqrt', r['min_exact_sum_sqrt_in_sqrtN'], 'lenN?', r['any_exact_length_N_interval'], r['quarter_X_exact'])
