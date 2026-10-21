"""Post-freeze exploratory checks (not part of the frozen candidate).

1. Closed form of the branch-pole value (Theorem E'):
     C_f(mu) = (2/f'(mu)) [ mu (f4 mu + f3/2) c_{p-1} - (f3/2) c_{p-2} - f4 c_{p-3} ]
   checked against direct enumeration for cubics and quartics.
2. Jet counterexample: run the INHERITED Miller recurrence (cm_system miller_alpha and
   Model.to_short, unmodified) over the dual-number algebra F_p[e]/(e^2)[s]/(s^2 - f(mu+e)),
   with the annihilator M fixed.  The e^0 part reproduces T_f(mu); the e^1 part is the
   derivative of the fixed-M rational expression, compared with the formal derivative
   T_f'(mu).  Agreement is NOT expected and its failure illustrates why a pointwise
   identity cannot be differentiated.
3. Remark C4 (single-point exclusion): for y0^2 = f(mu) != 0,
     sum_{P != (mu, y0)} (y + y0)/(x - mu) = y0 C_f(mu) - f'(mu)/(2 y0),
   by enumeration of actual points (value at (mu, -y0) taken as the regular limit).
4. Exhaustive double poles at every nonbranch mu and polynomial parts x, x^2, x^3, through the
   frozen candidate cmcs.Curve, against direct enumeration (exact counts for the report).
5. The caller-supplied second-kind path (prepare_second_kind(supplied=...)), including the derived
   c_{p-4}, against FLINT coefficients and enumerated polynomial-part sums.
Usage (package root): python3 src/exploratory_jets_and_closed_forms.py
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reference as ref                                       # noqa: E402
import harness as H                                           # noqa: E402
from cm_system.backends.genus_one.curve import Model          # noqa: E402  (inherited)
from cm_system.backends.genus_one.miller import miller_alpha  # noqa: E402  (inherited)


class Degenerate(ArithmeticError):
    pass


class DualQuadCtx:
    """Elements (a0, a1, b0, b1) = (a0 + a1 e) + (b0 + b1 e) s,  e^2 = 0,  s^2 = d0 + d1 e."""

    def __init__(self, p, d0, d1):
        self.p, self.d0, self.d1 = p, d0 % p, d1 % p
        self.zero, self.one, self.gen = (0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0)

    def fromint(self, n):
        return (n % self.p, 0, 0, 0)

    def add(self, x, y):
        return tuple((u + v) % self.p for u, v in zip(x, y))

    def sub(self, x, y):
        return tuple((u - v) % self.p for u, v in zip(x, y))

    def neg(self, x):
        return tuple((-u) % self.p for u in x)

    @staticmethod
    def _dmul(a, b, p):          # dual numbers (u0 + u1 e)(v0 + v1 e)
        return (a[0] * b[0] % p, (a[0] * b[1] + a[1] * b[0]) % p)

    def mul(self, x, y):
        p = self.p
        A, B, C, D = (x[0], x[1]), (x[2], x[3]), (y[0], y[1]), (y[2], y[3])
        dd = (self.d0, self.d1)
        AC = self._dmul(A, C, p)
        BD = self._dmul(self._dmul(B, D, p), dd, p)
        AD = self._dmul(A, D, p)
        BC = self._dmul(B, C, p)
        return ((AC[0] + BD[0]) % p, (AC[1] + BD[1]) % p, (AD[0] + BC[0]) % p, (AD[1] + BC[1]) % p)

    def inv(self, x):
        p = self.p
        A, B = (x[0], x[1]), (x[2], x[3])
        dd = (self.d0, self.d1)
        N = self._dmul(A, A, p)
        BB = self._dmul(self._dmul(B, B, p), dd, p)
        N = ((N[0] - BB[0]) % p, (N[1] - BB[1]) % p)
        if N[0] == 0:
            raise Degenerate('non-invertible norm')
        n0i = pow(N[0], -1, p)
        Ninv = (n0i, (-N[1] * n0i * n0i) % p)
        a = self._dmul(A, Ninv, p)
        b = self._dmul(B, Ninv, p)
        return (a[0], a[1], (-b[0]) % p, (-b[1]) % p)

    def iszero(self, x):
        return all(u % self.p == 0 for u in x)

    def eq(self, x, y):
        return self.iszero(self.sub(x, y))


def closed_form_branch(f, mu, c, p):
    f = f + [0] * (5 - len(f))
    fd = sum(i * f[i] * pow(mu, i - 1, p) for i in range(1, 5)) % p
    half = pow(2, -1, p)
    inner = (mu * (f[4] * mu + f[3] * half) * c[p - 1] - f[3] * half * c[p - 2] - f[4] * c[p - 3]) % p
    return 2 * pow(fd, -1, p) * inner % p


def main():
    rng = random.Random(424242)
    out = {'closed_form_branch': {'checks': 0, 'failures': 0},
           'jets': {'queries': 0, 'value_matches': 0, 'derivative_matches': 0, 'degenerate_skipped': 0}}
    primes = H.primes_in(211, 400)
    for p in primes:
        for deg in (3, 4, 4):
            f = H.random_squarefree(p, deg, rng)
            c = ref.power_coefficients(f, p)
            ds = ref.DirectSums(p, f)
            for mu in range(p):
                if ref.peval(f, mu, p) == 0:
                    out['closed_form_branch']['checks'] += 1
                    if closed_form_branch(f, mu, c, p) != ds.character_sum(simple=[(mu, 1)]):
                        out['closed_form_branch']['failures'] += 1
    # jets: normalized curves (f(0) = 1), inherited model and Miller recurrence over dual numbers
    for p in H.primes_in(101, 200):
        for deg in (3, 4):
            f = H.random_squarefree(p, deg, rng, const=1)
            tau = ref.trace_pari(f, p)
            c = ref.power_coefficients(f, p)
            model = Model(f, p)
            Tder = [(m * c[m]) % p for m in range(1, p)]
            for mu in rng.sample(range(1, p), 12):
                d0 = ref.peval(f, mu, p)
                if d0 == 0:
                    continue
                d1 = sum(i * f[i] * pow(mu, i - 1, p) for i in range(1, len(f))) % p
                chi = ref.legendre(d0, p)
                M = p + 1 - chi * tau
                ctx = DualQuadCtx(p, d0, d1)
                w = (mu % p, 1, 0, 0)                       # mu + e
                try:
                    R = model.to_short(ctx, w, ctx.gen)
                    alpha, _ = miller_alpha(ctx, R, M, model.A)
                except (Degenerate, ZeroDivisionError, ArithmeticError):
                    out['jets']['degenerate_skipped'] += 1
                    continue
                # S = H + chi * B0 / lambda = H + chi * B0 * w ;  B0 = (alpha[2], alpha[3]) dual
                H0 = tau % p
                B0 = (alpha[2], alpha[3])
                val0 = (H0 + chi * B0[0] * mu) % p
                val1 = (chi * (B0[1] * mu + B0[0])) % p     # e-coefficient of chi * B0 * (mu + e)
                truth0 = ref.truncation_value(c, mu, p)
                truth1 = 0
                for m in range(p - 2, -1, -1):
                    truth1 = (truth1 * mu + Tder[m]) % p
                out['jets']['queries'] += 1
                out['jets']['value_matches'] += int(val0 == truth0)
                out['jets']['derivative_matches'] += int(val1 == truth1)
    out['pointwise_exclusion_remark'] = {'checks': 0, 'failures': 0}
    for p in H.primes_in(7, 120):
        sq = {}
        for y in range(p):
            sq.setdefault(y * y % p, []).append(y)
        for deg in (3, 4):
            f = H.random_squarefree(p, deg, rng)
            ds = ref.DirectSums(p, f)
            fdp = [(i * f[i]) % p for i in range(1, len(f))]
            for mu in range(p):
                d = ref.peval(f, mu, p)
                if d == 0 or ref.legendre(d, p) != 1:
                    continue
                y0 = sq[d][0]
                fd = ref.peval(fdp, mu, p)
                tot = 0
                for x in range(p):
                    for y in sq.get(ref.peval(f, x, p), []):
                        if x == mu:
                            if y != y0:
                                tot += fd * pow(2 * y, -1, p)
                        else:
                            tot += (y + y0) * pow(x - mu, -1, p)
                C = ds.character_sum(simple=[(mu, 1)])
                out['pointwise_exclusion_remark']['checks'] += 1
                if tot % p != (y0 * C - fd * pow(2 * y0, -1, p)) % p:
                    out['pointwise_exclusion_remark']['failures'] += 1
    import cmcs
    out['double_poles_and_polynomial_parts'] = {'double_checks': 0, 'poly_checks': 0, 'failures': 0,
                                                 'quartic_linear_via_miller': 0}
    for p in H.primes_in(101, 200):
        for deg in (3, 4):
            f = H.random_squarefree(p, deg, rng, const=rng.choice([None, 0, 1]))
            E = cmcs.Curve(p, f, trace=ref.trace_pari(f, p))
            E.prepare_second_kind()
            ds = ref.DirectSums(p, f)
            for mu in range(p):
                if E.is_branch(mu):
                    continue
                out['double_poles_and_polynomial_parts']['double_checks'] += 1
                if E.double_pole_value(mu) != ds.character_sum(double=[(mu, 1)]):
                    out['double_poles_and_polynomial_parts']['failures'] += 1
            for k in (1, 2, 3):
                v, how = E.poly_value(k)
                out['double_poles_and_polynomial_parts']['poly_checks'] += 1
                out['double_poles_and_polynomial_parts']['quartic_linear_via_miller'] += int(how == 'miller_pole_at_infinity')
                if v != ds.character_sum(poly=[0] * k + [1]):
                    out['double_poles_and_polynomial_parts']['failures'] += 1
    out['supplied_second_kind_path'] = {'checks': 0, 'failures': 0}
    for p in H.primes_in(7, 300):
        for deg in (3, 4):
            for const in (None, 0, 1):
                f = H.random_squarefree(p, deg, rng, const)
                c = ref.power_coefficients(f, p)
                E = cmcs.Curve(p, f, trace=ref.trace_pari(f, p))
                E.prepare_second_kind(supplied=(c[p - 1], c[p - 2], c[p - 3]))
                out['supplied_second_kind_path']['checks'] += 1
                if E.second_kind['low'] != [c[p - 1 - i] for i in range(4)]:
                    out['supplied_second_kind_path']['failures'] += 1
                ds = ref.DirectSums(p, f)
                for k in (1, 2, 3):
                    out['supplied_second_kind_path']['checks'] += 1
                    if E.poly_value(k)[0] != ds.character_sum(poly=[0] * k + [1]):
                        out['supplied_second_kind_path']['failures'] += 1
    path = os.path.join(os.path.dirname(HERE), 'results', 'exploratory_jets_and_closed_forms.json')
    with open(path, 'w') as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
