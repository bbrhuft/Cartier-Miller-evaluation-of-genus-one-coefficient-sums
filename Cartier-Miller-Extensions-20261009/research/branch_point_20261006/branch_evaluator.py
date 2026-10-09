"""Exact cubic branch queries modulo p; standard-library prototype.

Coefficients are low-to-high: [1,c,b,a]. Streaming preparation is O(p)
field operations and O(1) field elements. A query at a supplied rational
root is O(1). No polylogarithmic complete-run claim is made.
"""
from dataclasses import dataclass
import argparse
import json


def is_prime64(p):
    if not isinstance(p, int) or isinstance(p, bool) or p < 2 or p >= 2**64:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if p % q == 0:
            return p == q
    d, s = p - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        x = pow(base % p, d, p)
        if base % p == 0 or x in (1, p - 1):
            continue
        for _ in range(s - 1):
            x = x*x % p
            if x == p - 1:
                break
        else:
            return False
    return True


def eval_poly(f, x, p):
    answer = 0
    for c in reversed(f):
        answer = (answer*x+c) % p
    return answer


def check_cubic(f, p):
    if len(f) != 4 or any(not isinstance(x, int) for x in f):
        raise ValueError('Use four integer coefficients [1,c,b,a].')
    f = tuple(x % p for x in f)
    if f[0] != 1 or f[3] == 0:
        raise ValueError('Require f(0)=1 and degree exactly three.')
    d, c, b, a = f
    disc = b*b*c*c - 4*a*c*c*c - 4*b*b*b*d - 27*a*a*d*d + 18*a*b*c*d
    if disc % p == 0:
        raise ValueError('Cubic is not squarefree modulo p.')
    return f


def linear_cartier_data(f, p):
    """Return (H,K) using V_n=n!*(c_n,c_(n-1),c_(n-2)).

    Only three state elements are retained; no per-step inverse is used.
    At n=p-1, Wilson gives n!=-1, so negate the first two entries.
    p is assumed prime, f normalized; public prepare() validates inputs.
    """
    _, c, b, a = f
    h1 = (p+1)//2
    v0, v1, v2 = 1, 0, 0
    for n in range(1, p):
        t = ((h1-n)*c*v0+(2*h1-n)*b*v1+(3*h1-n)*a*v2) % p
        v0, v1, v2 = t, n*v0 % p, n*v1 % p
    return -v0 % p, -v1 % p


@dataclass(frozen=True)
class BranchEvaluator:
    p: int
    f: tuple
    H: int
    K: int
    preparation_method: str

    def query(self, mu):
        if not isinstance(mu, int):
            raise ValueError('mu must be an integer residue.')
        p, f = self.p, self.f
        mu %= p
        if mu == 0 or eval_poly(f, mu, p) != 0:
            raise ValueError('Require a supplied nonzero rational root of f.')
        derivative = (f[1]+2*f[2]*mu+3*f[3]*mu*mu) % p
        answer = f[3]*mu*pow(derivative, -1, p)*(mu*self.H-self.K) % p
        trusted = 'caller_supplied' in self.preparation_method
        return {'status': 'computed_from_trusted_data' if trusted else 'exact_mod_p',
                'p': p, 'f': list(f), 'mu': mu,
                'lambda': pow(mu, -1, p), 'H': self.H, 'K': self.K,
                'T': answer, 'S': answer,
                'ordinary': self.H != 0,
                'preparation_method': self.preparation_method,
                'query_field_operations': 'O(1)',
                'root_finding_included': False}


def prepare(p, f, *, trusted_cartier_data=None):
    """Prepare a normalized squarefree cubic, including prime validation.

    Supplied (H,K) are explicitly trusted, not certified here. The default
    computes both coefficients by the exact scaled recurrence. Root finding
    is outside the API: query() requires a supplied root and checks it.
    """
    if p < 7 or not is_prime64(p):
        raise ValueError('Require prime 7 <= p < 2^64.')
    f = check_cubic(f, p)
    if trusted_cartier_data is None:
        H, K = linear_cartier_data(f, p)
        method = 'streaming_scaled_recurrence_O(p)'
    else:
        if len(trusted_cartier_data) != 2:
            raise ValueError('Supply trusted (H,K).')
        H, K = (int(x) % p for x in trusted_cartier_data)
        method = 'caller_supplied_trusted_H_K'
    return BranchEvaluator(p, f, H, K, method)


def prepare_from_trace(p, f, trusted_exact_trace):
    """Cheap data recovery for ordinary j=0 or j=1728 short models.

    The exact trace is caller-supplied and NOT certified by Hasse bounds.
    No point-count backend is implemented by this function. The theorem
    uses Schoof for deterministic polynomial-time trace preparation.
    """
    if p < 7 or not is_prime64(p):
        raise ValueError('Require prime 7 <= p < 2^64.')
    f = check_cubic(f, p)
    _, c, b, a = f
    shift = b*pow(3, -1, p) % p
    A = (a*c-b*b*pow(3, -1, p)) % p
    B = (a*a-a*b*c*pow(3, -1, p)+2*b*b*b*pow(27, -1, p)) % p
    if not ((A == 0 and p % 3 == 1) or (B == 0 and p % 4 == 1)):
        raise ValueError('Trace-only recovery is supported only in the stated structural families.')
    if not isinstance(trusted_exact_trace, int) or trusted_exact_trace**2 > 4*p:
        raise ValueError('Supplied trace fails a necessary Hasse bound.')
    H = trusted_exact_trace % p
    K = -shift*H*pow(a, -1, p) % p
    return BranchEvaluator(p, f, H, K, 'structural_beta_zero_caller_supplied_exact_trace')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('p', type=int)
    parser.add_argument('coefficients', type=int, nargs=4, metavar='F')
    parser.add_argument('--roots', nargs='+', type=int, required=True)
    args = parser.parse_args()
    try:
        prepared = prepare(args.p, args.coefficients)
        print(json.dumps([prepared.query(mu) for mu in args.roots], indent=2))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
