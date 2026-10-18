"""Development only; exact rational Wronskian and modular acquisition checks."""
from fractions import Fraction as F
from pathlib import Path
import json
from math import isqrt
from atkin import atkin_endpoint, wronskian_endpoint, c_from_derivative, nodal_c, factorial_c


def prime(p):
    return p >= 2 and all(p % j for j in range(2, isqrt(p)+1))


def rational_checks(limit=40):
    a = [F(1), F(-720), F(269280)]
    d = [F(0), F(1), F(-1640)]
    betas = [None, F(393120)]
    for n in range(2, limit+1):
        alpha = F(24*(144*n*n-29), (2*n+1)*(2*n-1))
        beta = F(36*(12*n-13)*(12*n-7)*(12*n-5)*(12*n+1), n*(n-1)*(2*n-1)**2)
        betas.append(beta)
        a.append(-alpha*a[-1]-beta*a[-2])
        d.append(a[-2]-alpha*d[-1]-beta*d[-2])
    product = F(1)
    for n in range(1, limit+1):
        product *= betas[n]
        r = F((12*n-1)*(12*n+5), 96*n)
        assert a[n]*d[n+1]-a[n+1]*d[n] == a[n]**2*r-product/4
    return dict(exact_rational_indices=limit, pass_=True)


def main():
    rational = rational_checks()
    primes = [p for p in range(11, 2000) if p % 6 == 5 and prime(p)]
    for p in primes:
        ref, _ = factorial_c(p, 'linear')
        assert c_from_derivative(p, atkin_endpoint(p)) == ref
        assert c_from_derivative(p, wronskian_endpoint(p)) == ref
        for mode in ('linear', 'separate', 'shared'):
            actual, _ = nodal_c(p, mode)
            assert actual == ref, (p, mode, actual, ref)
        actual, _ = factorial_c(p, 'block')
        assert actual == ref
    out = dict(status='PASS', rational=rational, primes=primes,
               role='Development for fixed candidate; these inputs must be excluded from confirmation')
    (Path(__file__).parent/'evidence/DEVELOPMENT.json').write_text(json.dumps(out, indent=2)+'\n')
    print({'status':'PASS','prime_cases':len(primes),'rational_indices':40})


if __name__ == '__main__':
    main()
