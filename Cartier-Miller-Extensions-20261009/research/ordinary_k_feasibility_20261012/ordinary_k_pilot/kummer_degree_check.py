"""Field of definition of the étale p-torsion: full point versus Kummer coordinate.

Claim (derived in note §6): for ordinary E/F_p with trace t, Frobenius acts on the
étale p-torsion E[p](F_p-bar) = <P> as multiplication by t mod p.  Hence the full point
P is defined over F_{p^k}, k = ord(t mod p), whereas its Kummer coordinate x(P) is
defined over F_{p^k'}, k' = order of t in F_p^x/{+-1}  (k' = k/2 if k is even, k' = k
if k is odd).  Equivalently the Verschiebung kernel polynomial psi_V in F_p[x] (degree h)
factors into irreducibles all of degree k'.

Check: distinct-degree factorization of psi_V (obtained from psi_p = c * psi_V^p in
F_p[x]) for every ordinary short model with 7 <= p <= 23, plus seeded samples at
p = 29, 31.  (That y(P) is not in F_{p^k'} when k is even follows from pi^{k'} P = -P;
it is argued in the note, not tested here.)  Exit 1 on any disagreement.
"""
from pathlib import Path
import json
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from okp_common import (CheckFailure, require, primes_between, nonsingular, trace_by_count,  # noqa: E402
                        H_beta_recurrence, division_polynomial_odd, pmul, psub, ptrim, sha256_file,
                        environment)


def pdivmod(a, b, p):
    a = [x % p for x in a]
    b = ptrim([x % p for x in b])
    inv = pow(b[-1], -1, p)
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(ptrim(a)) >= len(b):
        a = ptrim(a)
        i = len(a) - len(b)
        c = a[-1] * inv % p
        q[i] = c
        for j, v in enumerate(b):
            a[i + j] = (a[i + j] - c * v) % p
    return ptrim(q), ptrim(a)


def pgcd(a, b, p):
    a, b = ptrim(a[:]), ptrim(b[:])
    while b:
        a, b = b, pdivmod(a, b, p)[1]
    inv = pow(a[-1], -1, p)
    return [x * inv % p for x in a]


def powmod_x(e, m, p):
    """x^e mod m over F_p."""
    result, base = [1], [0, 1]
    while e:
        if e & 1:
            result = pdivmod(pmul(result, base, p), m, p)[1]
        base = pdivmod(pmul(base, base, p), m, p)[1]
        e >>= 1
    return result


def ddf_degrees(f, p):
    """Distinct-degree factorization: {degree d: number of irreducible factors of degree d}."""
    f = ptrim([x % p for x in f])
    out, d, g = {}, 1, f
    xp = [0, 1]
    while len(g) - 1 >= 2 * d:
        xp = powmod_x_poly(xp, p, g, p)
        h = pgcd(g, psub(xp, [0, 1], p), p)
        if len(h) > 1:
            require((len(h) - 1) % d == 0, 'ddf degree mismatch')
            out[d] = (len(h) - 1) // d
            g = pdivmod(g, h, p)[0]
            xp = pdivmod(xp, g, p)[1] if len(g) > 1 else xp
        d += 1
    if len(g) > 1:
        out[len(g) - 1] = out.get(len(g) - 1, 0) + 1
    return out


def powmod_x_poly(a, e, m, p):
    """a^e mod m over F_p."""
    result, base = [1], pdivmod(a, m, p)[1]
    while e:
        if e & 1:
            result = pdivmod(pmul(result, base, p), m, p)[1]
        base = pdivmod(pmul(base, base, p), m, p)[1]
        e >>= 1
    return result


def order_mod(t, p):
    t %= p
    k, v = 1, t
    while v != 1:
        v = v * t % p
        k += 1
    return k


def main():
    rng = random.Random(1013)
    rows, counts = [], {'models': 0, 'k_even': 0, 'k_odd': 0, 'kummer_smaller_than_point': 0}
    jobs = [(p, [(A, B) for A in range(p) for B in range(p) if nonsingular(A, B, p)]) for p in primes_between(7, 23)]
    for p in (29, 31):
        models = [(A, B) for A in range(p) for B in range(p) if nonsingular(A, B, p)]
        jobs.append((p, rng.sample(models, 60)))
    for p, models in jobs:
        h = (p - 1) // 2
        for A, B in models:
            H, _ = H_beta_recurrence(A, B, p)
            if H == 0:
                continue
            t = trace_by_count(A, B, p)
            fp = division_polynomial_odd(p, A, B, p)
            psiV = [fp[i * p] for i in range(h + 1)]
            require(len(ptrim(psiV[:])) == h + 1, 'psi_V degree')
            k = order_mod(t, p)
            kprime = k // 2 if k % 2 == 0 else k
            degs = ddf_degrees(psiV, p)
            require(set(degs) == {kprime} and kprime * degs[kprime] == h,
                    f'psi_V factor degrees {degs} != {{k\'={kprime}}} at {(p, A, B, t)}')
            counts['models'] += 1
            counts['k_even' if k % 2 == 0 else 'k_odd'] += 1
            counts['kummer_smaller_than_point'] += kprime < k
            rows.append({'p': p, 'A': A, 'B': B, 't': t, 'k_point': k, 'k_kummer': kprime, 'psiV_factor_degrees': degs})
    (HERE / 'results').mkdir(exist_ok=True)
    summary = {'status': 'PASS', 'failures': 0, **counts,
               'claim': 'x(P) for P in the etale p-torsion lies in F_{p^k\'}, k\' = ord of t in F_p^x/{+-1}; '
                        'P itself needs F_{p^k}, k = ord(t mod p)',
               'examples_t_minus_one': [r for r in rows if r['t'] == -1][:3],
               'source_sha256': {n: sha256_file(HERE / n) for n in ('kummer_degree_check.py', 'okp_common.py')},
               'environment': environment()}
    (HERE / 'results' / 'kummer_degree_check.json').write_text(json.dumps({'summary': summary, 'rows': rows}, indent=1))
    print(json.dumps({k: summary[k] for k in ('status', 'models', 'k_even', 'k_odd', 'kummer_smaller_than_point')}))
    print('KUMMER_DEGREE_PASS')


if __name__ == '__main__':
    try:
        main()
    except CheckFailure as exc:
        print('FAIL:', exc)
        sys.exit(1)
