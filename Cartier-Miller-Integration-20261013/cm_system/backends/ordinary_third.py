"""Complete third-point evaluation for primes p >= 7, p = 1 (mod 3).

Standard-library-only Python 3.8+. Uses the paper's undivided formula,
including exceptional trace = character. No changes to quarter-point code.
"""
import argparse
import csv
import json
from math import isqrt
from pathlib import Path
import sys


from .genus_one.fields import FpCtx, QuadCtx, legendre
from .genus_one.curve import Model
from .genus_one.miller import Resume, miller_alpha_resumable, miller_continue


def is_prime(p):
    """Deterministic Miller-Rabin on unsigned 64-bit integers."""
    if not isinstance(p, int) or p < 2 or p >= 2**64:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if p % q == 0:
            return p == q
    d, s = p - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        x = pow(a % p, d, p)
        if a % p == 0 or x in (1, p - 1):
            continue
        for _ in range(s - 1):
            x = x*x % p
            if x == p - 1:
                break
        else:
            return False
    return True


def cornacchia_trace(p):
    """Trace of v^2 = 1-w^3/2, equivalently Y^2 = X^3+1/4.

    Select r = 1 mod 3 in 4p = r^2+27s^2; trace = -r.
    The deterministic cubic-nonresidue scan is NOT assigned an
    unconditional polylogarithmic worst-case complexity bound.
    """
    c, trials = 2, 0
    while True:
        trials += 1
        z = pow(c, (p - 1)//3, p)
        if z != 1:
            break
        c += 1
    root = (2*z + 1) % p
    assert root*root % p == p - 3
    u, v = p, root
    while v*v > p:
        u, v = v, u % v
    rem = p - v*v
    w = isqrt(rem//3)
    if v*v + 3*w*w != p:
        raise ArithmeticError('Cornacchia representation failed')
    for r, t in ((2*v, 2*w), (v + 3*w, v - w), (v - 3*w, v + w)):
        if t % 3 == 0:
            if r % 3 != 1:
                r = -r
            s = abs(t)//3
            assert r*r + 27*s*s == 4*p
            return -r, {'r': r, 's': s, 'root_trials': trials}
    raise ArithmeticError('Cornacchia normalization failed')


class ThirdPointEvaluator:
    """Cached curve/trace setup; evaluate lambda=1 to obtain B_L,a_L,U_L.

    An optional trace must be the exact trace of THIS curve, supplied by
    a trusted point counter. Its correctness is the caller's responsibility.
    """
    def __init__(self, p, trace=None):
        if not is_prime(p) or p < 7 or p % 3 != 1:
            raise ValueError('require prime 7 <= p < 2^64 with p = 1 (mod 3)')
        self.p, self.L = p, (p - 1)//3
        if trace is None:
            trace, self.preparation = cornacchia_trace(p)
            self.trace_source = 'Cornacchia/classical cubic-binomial normalization'
        else:
            self.preparation = {'r': None, 's': None, 'root_trials': 0}
            self.trace_source = 'caller-supplied exact trace'
        if not isinstance(trace, int) or trace*trace > 4*p or trace % 3 != 2:
            raise ValueError('trace fails necessary Hasse/3-torsion conditions')
        self.trace, self.H = trace, trace % p
        self.chi = legendre(pow(2, -1, p), p)
        self.M = p + 1 - self.chi*trace
        self.model = Model([1, 0, 0, -pow(2, -1, p)], p)

    def evaluate(self):
        p, m = self.p, self.model
        k = QuadCtx(p, pow(2, -1, p))
        R = m.to_short(k, k.one, k.gen)
        x, y = R
        assert k.eq(k.mul(y, y), k.add(k.add(k.mul(k.mul(x, x), x),
                      k.mul(k.fromint(m.A), x)), k.fromint(m.B)))
        split = False
        try:
            alpha, endpoint = miller_alpha_resumable(k, R, self.M, m.A)
            # M kills Q+ - Q-, not necessarily Q+ individually in this model.
            assert endpoint is None or all(e[1] == 0 for e in endpoint)
            r_phi = 2*alpha[1] % p
        except Resume as state:
            split = True
            root = k.sqrt_from_witness(state.witness)
            F = FpCtx(p)
            def component(e, sign):
                return (e[0] + sign*e[1]*root) % p
            alphas, endpoints = [], []
            for sign in (1, -1):
                point = tuple(component(e, sign) for e in R)
                T = None if state.T is None else tuple(component(e, sign) for e in state.T)
                a, endpoint = miller_continue(F, point, self.M, m.A, T,
                                component(state.alpha, sign), state.j)
                alphas.append(a)
                endpoints.append(endpoint)
            assert endpoints[0] == endpoints[1]
            r_phi = (alphas[0] - alphas[1])*pow(root, -1, p) % p
        r_psi = r_phi*pow(m.kappa, -1, p) % p
        S = (self.H - self.chi*r_psi) % p
        B = (S - self.H) % p
        a = self.H
        U = (4*B - 2*self.L*(2*self.L + 5)*a) % p
        return {'p': p, 'L': self.L, 'B': B, 'a': a, 'U': U, 'S': S,
                'trace': self.trace, 'chi': self.chi, 'M': self.M,
                'exceptional': self.trace == self.chi, 'split_fallback': split,
                'trace_source': self.trace_source, **self.preparation}


def third(p, trace=None):
    return ThirdPointEvaluator(p, trace).evaluate()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('primes', nargs='*', type=int, default=[97])
    parser.add_argument('--csv', type=Path, help='save modular answers (not benchmark timings)')
    parser.add_argument('--trace', type=int, help='trusted exact trace; one prime only')
    args = parser.parse_args()
    if args.trace is not None and len(args.primes) != 1:
        parser.error('--trace requires exactly one prime')
    try:
        rows = [third(p, args.trace) for p in args.primes]
    except ValueError as error:
        parser.error(str(error))
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open('w', newline='', encoding='utf-8-sig') as out:
            writer = csv.DictWriter(out, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
