"""Exact arithmetic in a tower of quadratic extensions of Q.
Level 0 elements are fractions.Fraction. Level n elements are pairs (a, b)
meaning a + b*t_n with t_n^2 = d_n, d_n an element of level n-1.
Standard library only; used for exact characteristic-zero CM computations."""
from fractions import Fraction

class Tower:
    def __init__(self, names, squares):
        """names: generator names; squares[k] = t_k^2 as a level-k element
        (given as a function of the tower built so far, or a Fraction)."""
        self.names = list(names); self.d = []
        for k, sq in enumerate(squares):
            self.d.append(self.lift(sq, k) if not callable(sq) else sq(self))
    # ---- construction ----
    def lift(self, a, level):
        """Embed level-k element a (k<=level) or rational into given level."""
        if isinstance(a, (int, Fraction)):
            a = Fraction(a)
            for _ in range(level):
                a = (a, self.zero_at(len(self._shape(a))))
            return self._fix(a, level)
        return self._fix(a, level)
    def _shape(self, a):
        n = 0
        while isinstance(a, tuple):
            a = a[0]; n += 1
        return [0]*n
    def level_of(self, a):
        return len(self._shape(a))
    def zero_at(self, level):
        z = Fraction(0)
        for _ in range(level):
            z = (z, z if False else self._zero_like(z))
        return z
    def _zero_like(self, z):
        if isinstance(z, tuple):
            return (self._zero_like(z[0]), self._zero_like(z[1]))
        return Fraction(0)
    def _fix(self, a, level):
        while self.level_of(a) < level:
            a = (a, self._zero_like(a))
        return a
    def gen(self, k, level=None):
        level = len(self.d) if level is None else level
        g = (self._zero_like(self.lift(Fraction(0), k)), self.lift(Fraction(1), k))
        return self._fix(g, level)
    def const(self, c, level=None):
        level = len(self.d) if level is None else level
        return self.lift(Fraction(c), level)
    # ---- arithmetic (both operands at the same level) ----
    def add(self, a, b):
        if isinstance(a, tuple):
            return (self.add(a[0], b[0]), self.add(a[1], b[1]))
        return a + b
    def neg(self, a):
        if isinstance(a, tuple):
            return (self.neg(a[0]), self.neg(a[1]))
        return -a
    def sub(self, a, b):
        return self.add(a, self.neg(b))
    def mul(self, a, b):
        if isinstance(a, tuple):
            n = self.level_of(a); d = self.d[n-1]
            a0, a1 = a; b0, b1 = b
            return (self.add(self.mul(a0, b0), self.mul(self.mul(a1, b1), d)),
                    self.add(self.mul(a0, b1), self.mul(a1, b0)))
        return a * b
    def inv(self, a):
        if isinstance(a, tuple):
            n = self.level_of(a); d = self.d[n-1]
            a0, a1 = a
            den = self.sub(self.mul(a0, a0), self.mul(self.mul(a1, a1), d))
            di = self.inv(den)
            return (self.mul(a0, di), self.neg(self.mul(a1, di)))
        if a == 0:
            raise ZeroDivisionError('zero in tower')
        return 1 / a
    def div(self, a, b):
        return self.mul(a, self.inv(b))
    def pow(self, a, n):
        r = self.const(1, self.level_of(a))
        for _ in range(n):
            r = self.mul(r, a)
        return r
    def is_zero(self, a):
        if isinstance(a, tuple):
            return self.is_zero(a[0]) and self.is_zero(a[1])
        return a == 0
    def eq(self, a, b):
        return self.is_zero(self.sub(a, b))
    def coords(self, a):
        """Flatten to a list of Fractions in the monomial basis t^mask."""
        if isinstance(a, tuple):
            return self.coords(a[0]) + self.coords(a[1])
        return [a]
    def monomials(self):
        n = len(self.d); out = []
        for mask in range(2**n):
            out.append('*'.join(self.names[k] for k in range(n) if (mask >> k) & 1) or '1')
        return out
    def show(self, a):
        terms = []
        for c, m in zip(self.coords(a), self.monomials()):
            if c:
                terms.append(f'{c}' + ('' if m == '1' else f'*{m}'))
        return ' + '.join(terms) if terms else '0'
    def is_rational(self, a):
        cs = self.coords(a)
        return all(c == 0 for c in cs[1:])
    # numeric evaluation for a chosen embedding: values[k] = complex/float value of t_k
    def evalc(self, a, values):
        if isinstance(a, tuple):
            n = self.level_of(a)
            return self.evalc(a[0], values) + self.evalc(a[1], values) * values[n-1]
        return a
