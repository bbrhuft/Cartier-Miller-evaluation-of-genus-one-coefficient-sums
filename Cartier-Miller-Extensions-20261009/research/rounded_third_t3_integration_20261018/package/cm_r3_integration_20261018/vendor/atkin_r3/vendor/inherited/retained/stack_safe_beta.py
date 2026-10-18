"""Stack-safe evaluator for a normalized polynomial integral over F_p.

Requires an already certified prime p >= 11 with p == 2 (mod 3).
The evaluator does not certify primality. Python standard library only.

I_p(X) = sum_{i=0}^h binom(h,i) (1/4)^(h-i) X^(3i+1)/(3i+1), h=(p-1)/2.
J_p(X) = I_p(X)/I_p(x_star), x_star^3 = -1/4.

The proposed correctness theorem is detailed in RESEARCH_BRIEF.md.
No factorial, binomial, dense polynomial, square root or point count is used
by this module. Evaluation is by scalar curve-parameter dual numbers.

The classical normalized division-polynomial recurrence is adapted from
Fable's supplied divpoly_jets.py. This is a new scalar implementation and
packaging, not an independent discovery of that recurrence.
"""
import argparse
import json


class Field:
    def __init__(self, p):
        self.p = p
        self.additions = 0
        self.multiplications = 0

    def add(self, a, b):
        self.additions += 1
        return (a + b) % self.p

    def sub(self, a, b):
        self.additions += 1
        return (a - b) % self.p

    def mul(self, a, b):
        self.multiplications += 1
        return a * b % self.p

    def power(self, a, n):
        out = 1
        while n:
            if n & 1:
                out = self.mul(out, a)
            n >>= 1
            if n:
                a = self.mul(a, a)
        return out

    def counts(self):
        return dict(additions=self.additions, multiplications=self.multiplications)


class Dual:
    """Pairs represent a + epsilon*b, epsilon^2 = 0; all work is counted."""
    def __init__(self, field):
        self.f = field
        self.zero = (0, 0)
        self.one = (1, 0)

    def c(self, n):
        return n % self.f.p, 0

    def add(self, a, b):
        return self.f.add(a[0], b[0]), self.f.add(a[1], b[1])

    def sub(self, a, b):
        return self.f.sub(a[0], b[0]), self.f.sub(a[1], b[1])

    def mul(self, a, b):
        f = self.f
        return f.mul(a[0], b[0]), f.add(f.mul(a[0], b[1]), f.mul(a[1], b[0]))


def division_values(r, indices, x, A, B):
    """f_n=psi_n for odd n, psi_n/(2y) for even n; no division by y.

    Three neighbouring requested indices share one memoized recursion.
    Arithmetic in this routine is over dual numbers, not polynomial arrays.
    """
    mul, add, sub, c = r.mul, r.add, r.sub, r.c
    square = lambda z: mul(z, z)
    cube = lambda z: mul(square(z), z)
    x2 = square(x)
    x3 = mul(x2, x)
    x4 = square(x2)
    x6 = square(x3)
    A2 = square(A)
    A3 = mul(A2, A)
    B2 = square(B)
    F = add(add(x3, mul(A, x)), B)
    fourF = mul(c(4), F)
    sixteenF2 = square(fourF)
    f3 = sub(add(add(mul(c(3), x4), mul(c(6), mul(A, x2))),
                 mul(c(12), mul(B, x))), A2)
    f4 = mul(c(2), sub(sub(sub(
        add(add(x6, mul(c(5), mul(A, x4))), mul(c(20), mul(B, x3))),
        mul(c(5), mul(A2, x2))), mul(c(4), mul(mul(A, B), x))),
        add(mul(c(8), B2), A3)))
    base = {0: r.zero, 1: r.one, 2: r.one, 3: f3, 4: f4}

    def compute(n):
        if n in base:
            return base[n]
        if n % 2:
            m = (n - 1) // 2
            left = mul(values_by_index[m + 2], cube(values_by_index[m]))
            right = mul(values_by_index[m - 1], cube(values_by_index[m + 1]))
            if m % 2 == 0:
                left = mul(sixteenF2, left)
            else:
                right = mul(sixteenF2, right)
            return sub(left, right)
        m = n // 2
        return mul(values_by_index[m], sub(mul(values_by_index[m + 2], square(values_by_index[m - 1])),
                             mul(values_by_index[m - 2], square(values_by_index[m + 1]))))

    def dependencies(n):
        if n <= 4:
            return ()
        m = n // 2
        return (m-1,m,m+1,m+2) if n%2 else (m-2,m-1,m,m+1,m+2)
    values_by_index = dict(base)
    seen = set()
    for requested in indices:
        stack = [(requested, False)]
        while stack:
            n, ready = stack.pop()
            seen.add(n)
            if n in values_by_index:
                continue
            if ready:
                values_by_index[n] = compute(n)
            else:
                seen.update(dependencies(n))
                stack.append((n, True))
                stack.extend((j,False) for j in dependencies(n) if j not in values_by_index)
    f = values_by_index.__getitem__

    values = {n: f(n) for n in indices}
    return values, F, len(seen)


class NormalizedBeta:
    """A fixed-prime context. Prime certification is a caller precondition."""
    def __init__(self, p):
        if type(p) is not int or p < 11 or p % 3 != 2:
            raise ValueError('require an already certified prime p>=11, p=2 mod 3')
        self.p = p
        self.field = Field(p)
        # Fermat inversion is charged as exponentiation; no inverse is hidden.
        self.B = self.field.power(4, p - 2)
        self.x_star = self.field.power((-self.B) % p, (2 * p - 1) // 3)
        self.setup_counts = self.field.counts()

    def evaluate(self, X):
        """Return J_p(X), endpoint derivative phi_1(X), and operation counts.

        In particular, X=0 and X=x_star are accepted by this recurrence.
        """
        p, field = self.p, self.field
        before = field.counts()
        r = Dual(field)
        x = r.c(X)
        A = (0, 1)
        values, F, states = division_values(r, (p - 1, p, p + 1), x, A, r.c(self.B))
        v = values[p]
        if v[0] != p - 1:
            raise ArithmeticError('supersingular psi_p=-1 precondition failed')
        # psi_p = -1 + epsilon*q, so psi_p^(-2) = 1 + 2*epsilon*q.
        inverse_square = (1, field.mul(2, v[1]))
        correction = r.mul(
            r.mul(r.mul(r.c(4), F), r.mul(values[p - 1], values[p + 1])),
            inverse_square,
        )
        endpoint = r.sub(x, correction)
        if endpoint[0] != X % p:
            raise ArithmeticError('specialized endpoint did not equal X')
        phi1 = endpoint[1]
        J = field.mul(field.mul((-3) % p, self.x_star), phi1)
        after = field.counts()
        return dict(
            p=p, X=X % p, x_star=self.x_star, J=J, phi1=phi1,
            arithmetic={key: after[key] - before[key] for key in before},
            setup_arithmetic=dict(self.setup_counts), cached_indices=states,
        )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('p', type=int, help='already certified prime >=11, p=2 mod 3')
    ap.add_argument('X', nargs='+', type=int, help='base-field evaluation coordinates')
    args = ap.parse_args()
    context = NormalizedBeta(args.p)
    for X in args.X:
        print(json.dumps(context.evaluate(X), sort_keys=True))


if __name__ == '__main__':
    main()
