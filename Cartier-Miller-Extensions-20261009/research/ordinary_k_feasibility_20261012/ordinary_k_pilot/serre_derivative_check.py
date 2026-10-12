"""Check of Proposition 6:  beta == theta(H) (mod p),  theta = 6B d/dA - (4/3) A^2 d/dB.

Hence kappa = theta(H)/H = theta log H: the slope is the logarithmic Serre
derivative of the Hasse invariant polynomial H(A, B).  The proof in the note is
three coefficient relations; this script checks every nonsingular short model
(ordinary and supersingular) for 7 <= p <= 61 and the Euler relation
4A H_A + 6B H_B == -H.  Exit status is nonzero on failure.
"""
from pathlib import Path
from math import factorial
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from okp_common import (CheckFailure, require, primes_between, nonsingular, H_beta_recurrence,  # noqa: E402
                        sha256_file, environment)


def hasse_polynomial(p):
    """H(A,B) = sum over i+j+k=h, 3i+j=p-1 of h!/(i!j!k!) A^j B^k  (mod p)."""
    h = (p - 1) // 2
    terms = {}
    for i in range(h + 1):
        j = p - 1 - 3 * i
        k = h - i - j
        if 0 <= j <= h and 0 <= k <= h:
            terms[(j, k)] = factorial(h) // (factorial(i) * factorial(j) * factorial(k)) % p
    return terms


def ev(terms, A, B, p):
    return sum(c * pow(A, j, p) * pow(B, k, p) for (j, k), c in terms.items()) % p


def main():
    counts = {'models': 0, 'ordinary': 0, 'supersingular': 0, 'monomials_by_p': {}}
    for p in primes_between(7, 61):
        T = hasse_polynomial(p)
        TA = {(j - 1, k): c * j % p for (j, k), c in T.items() if j}
        TB = {(j, k - 1): c * k % p for (j, k), c in T.items() if k}
        counts['monomials_by_p'][p] = len(T)
        i3 = pow(3, -1, p)
        for A in range(p):
            for B in range(p):
                if not nonsingular(A, B, p):
                    continue
                H, beta = H_beta_recurrence(A, B, p)
                require(ev(T, A, B, p) == H, f'Hasse polynomial mismatch at {(p, A, B)}')
                HA, HB = ev(TA, A, B, p), ev(TB, A, B, p)
                require((4 * A * HA + 6 * B * HB + H) % p == 0, f'Euler relation fails at {(p, A, B)}')
                require((6 * B * HA - 4 * i3 * A * A * HB) % p == beta, f'theta(H) != beta at {(p, A, B)}')
                counts['models'] += 1
                counts['ordinary' if H else 'supersingular'] += 1
    out = {'status': 'PASS', 'failures': 0, **counts,
           'identity': 'beta == (6B dH/dA - (4/3) A^2 dH/dB) mod p; Euler 4A H_A + 6B H_B == -H',
           'source_sha256': {n: sha256_file(HERE / n) for n in ('serre_derivative_check.py', 'okp_common.py')},
           'environment': environment()}
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results' / 'serre_derivative_summary.json').write_text(json.dumps(out, indent=2))
    print(json.dumps({k: out[k] for k in ('status', 'models', 'ordinary', 'supersingular')}))
    print('SERRE_DERIVATIVE_PASS')


if __name__ == '__main__':
    try:
        main()
    except CheckFailure as exc:
        print('FAIL:', exc)
        sys.exit(1)
