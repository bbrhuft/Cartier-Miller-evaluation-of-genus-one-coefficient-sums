"""
Cheap candidate quantities b_j(p), all computable in time polynomial in log p.
The basis is fixed by the pre-registration (prereg.json); nothing here is tuned.
"""
from fractions import Fraction
from math import isqrt
from .core import cornacchia, inv, legendre


def fermat_quotient(a, p):
    return (pow(a, p - 1, p * p) - 1) // p % p


def small_primes_of(q):
    """Odd primes dividing numerator or denominator of a rational q (q != 0)."""
    q = Fraction(q)
    out = set()
    for n in (abs(q.numerator), q.denominator):
        d = 2
        while d * d <= n:
            while n % d == 0:
                out.add(d)
                n //= d
            d += 1
        if n > 1:
            out.add(n)
    out.discard(2)
    return out


def ell_set(z):
    """Odd primes attached to z for the Round 2 extras: primes of z and of 1 - 4z."""
    z = Fraction(z)
    return sorted(small_primes_of(z) | small_primes_of(1 - 4 * z))


def strat_primes(z):
    """Primes whose quadratic symbol is not fixed by p mod 24 (used to stratify)."""
    return [l for l in ell_set(z) if l not in (3,)]


def class_key(p, z, round_no):
    strat = strat_primes(z) if round_no == 2 else []
    return (p % 24,) + tuple(legendre(l, p) for l in strat)


def cm_u(p):
    """p = u^2 + s^2 with u odd, u = 1 (mod 4)."""
    x, y = cornacchia(1, p)
    u = x if x % 2 else y
    return u if u % 4 == 1 else -u


def cm_r(p):
    """4p = r^2 + 27 s^2 with r = 1 (mod 3)."""
    a, b = cornacchia(3, p)
    for x in (2 * a, a + 3 * b, a - 3 * b):
        rem = 4 * p - x * x
        if rem >= 0 and rem % 27 == 0:
            s2 = rem // 27
            s = isqrt(s2)                 # exact integer square root (any size)
            if s * s == s2:
                return x if x % 3 == 1 else -x
    raise RuntimeError("no representation 4p = r^2 + 27 s^2")


def basis(p, z, round_no):
    """Ordered list of (name, value mod p)."""
    q = {a: fermat_quotient(a, p) for a in (2, 3, 5, 7)}
    B = [("1", 1),
         ("q2", q[2]), ("q3", q[3]), ("q5", q[5]), ("q7", q[7]),
         ("q2^2", q[2] * q[2] % p), ("q2*q3", q[2] * q[3] % p), ("q3^2", q[3] * q[3] % p)]
    if p % 4 == 1:
        u = cm_u(p) % p
        ui = inv(u, p)
        rho = pow(2, (p - 1) // 4, p)
        B += [("u", u), ("1/u", ui), ("u^2", u * u % p), ("rho", rho),
              ("rho*u", rho * u % p), ("rho/u", rho * ui % p),
              ("u*q2", u * q[2] % p), ("u*q3", u * q[3] % p)]
    if p % 3 == 1:
        r = cm_r(p) % p
        w = pow(2, (p - 1) // 3, p)
        B += [("r", r), ("1/r", inv(r, p)), ("r^2", r * r % p), ("w", w),
              ("w*r", w * r % p), ("w^2*r", w * w % p * r % p),
              ("r*q2", r * q[2] % p), ("r*q3", r * q[3] % p)]
    else:
        g = pow(2, (2 * p - 1) // 3, p)
        B += [("g", g), ("g^2", g * g % p), ("g*q2", g * q[2] % p),
              ("g^2*q2", g * g % p * q[2] % p)]
    if round_no == 2:
        for l in ell_set(z):
            if p % 4 == 1:
                B.append((f"{l}^((p-1)/4)", pow(l, (p - 1) // 4, p)))
            if p % 3 == 1:
                B.append((f"{l}^((p-1)/3)", pow(l, (p - 1) // 3, p)))
            else:
                B.append((f"{l}^((2p-1)/3)", pow(l, (2 * p - 1) // 3, p)))
    return B
