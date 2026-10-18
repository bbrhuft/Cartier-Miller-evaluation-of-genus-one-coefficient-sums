"""Round-2 development checks (characteristic-p half-interval candidate).

Stdlib part: all admissible p < 30000 for C1-C5 and the Dirichlet-type sums, exact
Fraction checks of the Phi functional (C6). Optional FLINT part (python-flint): C4 for all
admissible p < 200000 and C2/C3 on the same range. Writes evidence/charp/DEVELOPMENT_CHARP.json.
"""
import json
import random
import sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path
sys.dont_write_bytecode = True
from charp import classno, half_factorial, halfinterval_c, cornacchia_a
from develop import prime

ROOT = Path(__file__).resolve().parent


def legendre(x, p):
    return 1 if pow(x % p, (p - 1) // 2, p) == 1 else -1


# ------------------------------------------------------------ Phi functional (C6)
def chi3(u):
    return 0 if u % 3 == 0 else (1 if u % 3 == 1 else -1)


def B1bar(t):
    t = t - (t.numerator // t.denominator)
    return F(0) if t == 0 else t - F(1, 2)


def Phi(x):
    """average over u in (Z/M)^* of chi_{-3}(u) B1bar(u x), M = lcm(den x, 3)."""
    d = x.denominator
    M = d * 3 // gcd(d, 3)
    us = [u for u in range(1, M) if gcd(u, M) == 1]
    return sum((chi3(u) * B1bar(u * x) for u in us), F(0)) / len(us)


def order_mod(p, d):
    if d == 1:
        return 1
    k, v = 1, p % d
    while v != 1:
        v = v * p % d
        k += 1
    return k


def phi_checks(trials=400, seed=20261018):
    rng = random.Random(seed)
    res = dict(reflection=0, distribution=0, gross_koblitz=0)
    for _ in range(trials):
        d = rng.randint(2, 60)
        a = rng.randint(1, d - 1)
        x = F(a, d)
        assert Phi(x) + Phi(-x) == 0
        res['reflection'] += 1
        M = rng.randint(2, 7)
        assert sum((Phi(x + F(i, M)) for i in range(M)), F(0)) == Phi(M * x)
        res['distribution'] += 1
        for p in (5, 11, 17, 23, 29, 1013):
            if d % p == 0:
                continue
            f = order_mod(p, d)
            assert sum((Phi(x * p ** i) for i in range(f)), F(0)) == 0, (x, p)
            res['gross_koblitz'] += 1
    special = dict(Phi_1_3=str(Phi(F(1, 3))),
                   Phi_RN_after_coincidence_p5mod12=str(Phi(F(11, 12)) - Phi(F(1, 3)) - Phi(F(7, 12))),
                   Phi_cp=str(-3 * Phi(F(1, 3))))
    assert Phi(F(1, 3)) == F(-1, 6)
    return dict(instances=res, special=special, pass_=True)


# ------------------------------------------------------------ stdlib arithmetic checks
def arithmetic_checks(limit=30000):
    primes = [p for p in range(11, limit) if p % 6 == 5 and prime(p)]
    counts = dict(c1=0, mordell=0, gauss4p=0, conj_star=0, quarter=0, dirichlet_4p=0, dirichlet_3p=0, layouts=0)
    for p in primes:
        m, h, N, q = (p - 2) // 3, (p - 1) // 2, (p - 5) // 12, (p - 1) // 4
        f, fm, fN, fq = 1, None, None, None
        for j in range(1, h + 1):
            f = f * j % p
            if j == m: fm = f
            if j == N: fN = f
            if j == q: fq = f
        if N == 0: fN = 1
        H = f
        c_ref = 2 * pow(fm, 3 * (p - 2), p) % p
        P = 1
        for j in range(m + 1, h + 1):
            P = P * j % p
        assert fm * P % p == H and pow(H, 4, p) == 1 and 2 * H * pow(P, 3, p) % p == c_ref
        counts['c1'] += 1
        for layout in (1, 2):
            assert halfinterval_c(p, layout=layout)[0] == c_ref
            counts['layouts'] += 1
        if p % 4 == 3:
            assert half_factorial(p, 'mordell')[0] == H
            counts['mordell'] += 1
        else:
            S4 = sum(legendre(j, p) for j in range(1, q + 1))
            assert 2 * S4 == classno(-4 * p)
            counts['dirichlet_4p'] += 1
            S3 = sum(legendre(j, p) for j in range(1, m + 1))
            assert 2 * S3 == classno(-3 * p)
            counts['dirichlet_3p'] += 1
            assert half_factorial(p, 'h3p')[0] == H
            counts['conj_star'] += 1
            if p % 8 == 5:
                assert half_factorial(p, 'gauss4p')[0] == H
                counts['gauss4p'] += 1
                a = cornacchia_a(p)
                T = fm * fq * pow(fN, p - 2, p) % p
                assert pow(T, 4, p) == (-pow(4, p - 2, p)) % p
                X = fm * pow(fN, p - 2, p) % p
                assert pow(X, 4, p) == a * a % p
                counts['quarter'] += 1
            else:
                # quarter identity for p = 17 mod 24: a from brute decomposition
                a = next(x for x in range(1, int(p ** .5) + 1, 2) if int((p - x * x) ** .5) ** 2 == p - x * x)
                a = a if a % 4 == 1 else -a
                T = fm * fq * pow(fN, p - 2, p) % p
                X = fm * pow(fN, p - 2, p) % p
                assert pow(T, 4, p) == (-pow(4, p - 2, p)) % p and pow(X, 4, p) == a * a % p
                counts['quarter'] += 1
    return dict(primes=len(primes), limit=limit, counts=counts, pass_=True)


def flint_checks(limit=200000):
    try:
        from flint_backend import flint_factorial
    except Exception as exc:          # optional dependency
        return dict(skipped=str(exc))
    primes = [p for p in range(11, limit) if p % 6 == 5 and prime(p)]
    n = dict(mordell=0, gauss4p=0, conj_star=0)
    for p in primes:
        H = flint_factorial((p - 1) // 2, p)
        if p % 4 == 3:
            assert half_factorial(p, 'mordell')[0] == H; n['mordell'] += 1
        else:
            assert half_factorial(p, 'h3p')[0] == H; n['conj_star'] += 1
            if p % 8 == 5:
                assert half_factorial(p, 'gauss4p')[0] == H; n['gauss4p'] += 1
    return dict(primes=len(primes), limit=limit, counts=n, pass_=True)


def main():
    out = dict(role='Round-2 development; these inputs are excluded from confirmation',
               phi=phi_checks(), arithmetic=arithmetic_checks(), flint=flint_checks(),
               pilot_primes=[1000003, 10000019, 100000037, 1000000021, 100000007, 1000000007, 10000000019])
    (ROOT / 'evidence/charp').mkdir(parents=True, exist_ok=True)
    (ROOT / 'evidence/charp/DEVELOPMENT_CHARP.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: (v if k != 'phi' else v['special']) for k, v in out.items()}, indent=1))


if __name__ == '__main__':
    main()
