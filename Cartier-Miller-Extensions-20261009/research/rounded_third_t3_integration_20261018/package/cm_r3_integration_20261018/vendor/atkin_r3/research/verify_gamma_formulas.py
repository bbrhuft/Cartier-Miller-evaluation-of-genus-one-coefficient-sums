"""Post-freeze support for the written proofs (not part of the frozen confirmation).

Checks, modulo p, the exact forms of the classical formulas used in the proofs of C5:
  (R) Gamma_p(x) Gamma_p(1-x) = (-1)^{R(x)}
  (M) prod_{i<M} Gamma_p((x+i)/M) = eps_M M^{1-R(x)} Gamma_p(x),  eps_M = prod_{0<i<M} Gamma_p(i/M)
  (G) binom((p-1)/2,(p-1)/4) = 2a, p=a^2+b^2, a = 1 mod 4            (Gauss)
and the derived identity T^2 = (2/p) 3^{(p-1)/4} / 2 for p = 5 mod 12, T = m!((p-1)/4)!/N!,
at development primes and (labelled separately) at the round-2 confirmation primes.
Here Gamma_p(x) mod p = (-1)^R (R-1)!, R in [1,p], R = x mod p.
"""
import json
import random
import sys
from fractions import Fraction as Fr
from math import gcd
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from develop import prime


def R(x, p):
    r = x.numerator * pow(x.denominator, -1, p) % p
    return r if r else p


def G(x, p, fact):
    r = R(x, p)
    return (-1) ** r * fact[r - 1] % p


def small_checks(limit=2500, trials=60, seed=7):
    rng = random.Random(seed)
    n = dict(R=0, M=0, G=0)
    for p in [q for q in range(7, limit) if prime(q)]:
        fact = [1] * (p + 1)
        for i in range(1, p + 1):
            fact[i] = fact[i - 1] * i % p
        for _ in range(trials):
            d = rng.randint(2, 40)
            if d % p == 0:
                continue
            x = Fr(rng.randint(1, 5 * d), d)
            assert G(x, p, fact) * G(1 - x, p, fact) % p == (-1) ** R(x, p) % p
            n['R'] += 1
            M = rng.choice([2, 3, 4, 5, 6, 12])
            if M % p == 0:
                continue
            eps = 1
            for i in range(1, M):
                eps = eps * G(Fr(i, M), p, fact) % p
            lhs = 1
            for i in range(M):
                lhs = lhs * G((x + i) / M, p, fact) % p
            assert lhs == eps * pow(M, (1 - R(x, p)) % (p - 1), p) * G(x, p, fact) % p, (p, x, M)
            n['M'] += 1
        if p % 4 == 1:
            a = next(t for t in range(1, p, 2) if int((p - t * t) ** .5) ** 2 == p - t * t)
            a = a if a % 4 == 1 else -a
            h, q = (p - 1) // 2, (p - 1) // 4
            assert fact[h] * pow(fact[q] * fact[q], p - 2, p) % p == 2 * a % p
            n['G'] += 1
    return n


def T2(p, fac):
    m, N, q = (p - 2) // 3, (p - 5) // 12, (p - 1) // 4
    T = fac(m) * fac(q) * pow(fac(N), p - 2, p) % p
    rhs = (1 if p % 8 == 1 else -1) * pow(3, q, p) * pow(2, p - 2, p) % p
    return T * T % p == rhs


def main():
    out = dict(role='post-freeze proof support; finite checks of classical formula forms and of the derived T^2 identity')
    out['classical_forms'] = small_checks()
    dev = [p for p in range(17, 60000) if p % 12 == 5 and prime(p)]
    ok = 0
    for p in dev:
        f = [1] * p
        for i in range(1, p):
            f[i] = f[i - 1] * i % p
        assert T2(p, lambda k: f[k])
        ok += 1
    out['T2_development_primes_below_60000'] = ok
    try:
        from flint_backend import flint_factorial
        conf = json.loads((ROOT / 'evidence/charp/CONFIRMATION_CHARP.json').read_text())
        cps = [c['p'] for c in conf['cases'] if c['p'] % 12 == 5]
        out['T2_round2_confirmation_primes'] = {str(p): T2(p, lambda k, p=p: flint_factorial(k, p)) for p in cps}
        assert all(out['T2_round2_confirmation_primes'].values())
    except ImportError as exc:
        out['T2_round2_confirmation_primes'] = 'skipped: %s' % exc
    out['pass_'] = True
    (ROOT / 'evidence/charp/GAMMA_FORMULAS_POSTFREEZE.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
