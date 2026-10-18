"""Atkin endpoint acquisition; externally certified p>=11, p=5 mod6.

Standard library only. No factorial oracle in acquisition. These are costed
recurrence/product algorithms, not a polylogarithmic acquisition claim.
"""
from math import isqrt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent/'vendor'))
from block_factorial import Arithmetic


def parameters(p):
    if type(p) is not int or p < 11 or p % 6 != 5:
        raise ValueError('supply an externally certified prime p>=11, p=5 mod6')
    N = (p-5)//12
    eps = int(p % 12 == 11)
    return N, eps, N+1+eps


def derivative_from_c(p, c):
    N, eps, _ = parameters(p)
    chi = 1 if pow(6, (p-1)//2, p) == 1 else p-1
    product = -3*pow(4, p-2, p)*chi*pow(1728, N, p)*c % p
    return pow(-1, N, p)*pow(-1728, eps, p)*product % p


def c_from_derivative(p, derivative):
    N, eps, _ = parameters(p)
    chi = 1 if pow(6, (p-1)//2, p) == 1 else p-1
    denominator = 3*pow(1728, N, p)*pow(-1728, eps, p) % p
    return -4*chi*pow(-1, N, p)*derivative*pow(denominator, p-2, p) % p


def atkin_endpoint(p):
    """Homogeneous five-residue recurrence, one final scalar inverse.

    The four value/derivative residues have the same common denominator S.
    Clearing each recurrence denominator preserves O(1) field-element state.
    O(n_p) field operations; coefficient/index bit work is also charged in report.
    """
    _, _, target = parameters(p)
    a, b = 269280 % p, -720 % p
    d, e = -1640 % p, 1
    scale = 1
    for n in range(2, target):
        den = n*(n-1)*(2*n-1)**2*(2*n+1) % p
        an = 24*(144*n*n-29)*n*(n-1)*(2*n-1) % p
        bn = 36*(12*n-13)*(12*n-7)*(12*n-5)*(12*n+1)*(2*n+1) % p
        a, b, d, e = ((-an*a-bn*b) % p, den*a % p,
                      (den*a-an*d-bn*e) % p, den*d % p)
        scale = scale*den % p
    assert a == 0 and scale
    return d*pow(scale, p-2, p) % p


def wronskian_endpoint(p):
    """Endpoint product: (273/2) prod_{j=1}^{n_p-2} -6(12j+7)(12j+13)/((j+1)(2j+1))."""
    _, _, n = parameters(p)
    numerator = denominator = 1
    for j in range(1, n-1):
        numerator = numerator*((12*j+7)*(12*j+13) % p) % p
        denominator = denominator*((j+1)*(2*j+1) % p) % p
    return 273*pow(-6, n-2, p)*numerator*pow(2*denominator % p, p-2, p) % p


class SharedArithmetic(Arithmetic):
    """Matched generic product/remainder engine, sharing divisors across channels.

    Avoids powering the constant 1 in monic inversions for EVERY method. Uses
    the unchanged vendor polynomial multiplication backend. No hidden setup.
    """
    def __init__(self, p, backend='packed'):
        super().__init__(p, backend)
        self.series_inverse_calls = 0

    def inverse_series(self, a, n):
        if not a or not a[0]:
            raise ZeroDivisionError
        self.series_inverse_calls += 1
        if len(a) == 1:
            return (1,) if a[0] == 1 else (self.f.power(a[0], self.p-2),)
        x = (1,) if a[0] == 1 else (self.f.power(a[0], self.p-2),)
        precision = 1
        while precision < n:
            precision = min(2*precision, n)
            ax = self.mul(a, x, precision)
            x = self.mul(x, self.r.sub((2 % self.p,), ax), precision)
        return x

    def remainders(self, polynomials, divisor):
        needs = [max(0, len(a)-len(divisor)+1) for a in polynomials]
        if not max(needs):
            return polynomials
        inv = self.inverse_series(tuple(reversed(divisor)), max(needs))
        out = []
        for a, size in zip(polynomials, needs):
            if not size:
                out.append(a)
                continue
            qr = self.mul(tuple(reversed(a))[:size], inv, size)
            qr = list(qr)+[0]*(size-len(qr))
            q = tuple(reversed(qr))
            rem = self.r.sub(a, self.mul(q, divisor))
            assert len(rem) < len(divisor)
            out.append(rem)
        return out

    def evaluate_many(self, polynomials, tree):
        rems = self.remainders(polynomials, tree[0])
        if tree[1] is None:
            return [[v[0] if v else 0] for v in rems]
        left = self.evaluate_many(rems, tree[1])
        right = self.evaluate_many(rems, tree[2])
        return [a+b for a, b in zip(left, right)]

    def metadata(self):
        return dict(polynomial=dict(self.r.counts), scalar=self.f.counts(),
                    series_inverse_calls=self.series_inverse_calls)


def pochhammer_many(p, length, starts, shared=True, block_size=None):
    """Acquire several rising products, sharing the evaluation tree and inverses."""
    if length == 0:
        return [1]*len(starts), dict(block_size=0, blocks=0)
    ar = SharedArithmetic(p)
    width = block_size or max(1, isqrt(length))
    blocks = length//width
    polynomials = [ar.tree([(-(a+j)) % p for j in range(width)])[0] for a in starts]
    tree = ar.tree([j*width % p for j in range(blocks)])
    if shared:
        values = ar.evaluate_many(polynomials, tree)
    else:
        values = [ar.evaluate_many([poly], tree)[0] for poly in polynomials]
    products = []
    for a, samples in zip(starts, values):
        result = 1
        for value in samples:
            result = ar.f.mul(result, value)
        for j in range(width*blocks, length):
            result = ar.f.mul(result, (a+j) % p)
        products.append(result)
    return products, dict(block_size=width, blocks=blocks, channels=len(starts),
                          shared_inverses=shared, counts=ar.metadata())


def nodal_c(p, mode='shared', block_size=None):
    """Simplified nodal anchor: c=-(4/3)chi(6)(-1)^N (4/3)_N/N!."""
    N, _, _ = parameters(p)
    inv3 = pow(3, p-2, p)
    chi = 1 if pow(6, (p-1)//2, p) == 1 else p-1
    if mode == 'linear':
        numerator = denominator = 1
        # Integer arithmetic progressions; factors 3^N cancel.
        for j in range(N):
            numerator = numerator*(3*j+4) % p
            denominator = denominator*(3*j+3) % p
        meta = dict(N=N, linear_factor_multiplications=2*N)
    else:
        (numerator, denominator), meta = pochhammer_many(
            p, N, [4*inv3 % p, 1], shared=(mode == 'shared'), block_size=block_size)
    c = -4*inv3*chi*pow(-1, N, p)*numerator*pow(denominator, p-2, p) % p
    return c, meta


def factorial_c(p, mode='block'):
    parameters(p)
    m = (p-2)//3
    if mode == 'linear':
        g = 1
        for j in range(1, m+1):
            g = g*j % p
        meta = dict(m=m, linear_factor_multiplications=m)
    else:
        (g,), meta = pochhammer_many(p, m, [1])
    return 2*pow(g, 3*(p-2), p) % p, meta


if __name__ == '__main__':
    import argparse, json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('p', type=int)
    args = parser.parse_args()
    derivative = wronskian_endpoint(args.p)
    c, meta = nodal_c(args.p)
    assert derivative == derivative_from_c(args.p, c)
    print(json.dumps(dict(p=args.p, c=c, derivative=derivative, nodal_metadata=meta), indent=2))
