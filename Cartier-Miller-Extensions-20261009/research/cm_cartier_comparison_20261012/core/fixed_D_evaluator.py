"""Uniform fixed-discriminant Cartier slope from exact CM data:

    beta/H = -(3B/(2A)) * R_D(j(E))  (mod p)

for E: y^2 = x^3 + A x + B over F_p with A B != 0, H_D(j(E)) = 0 (mod p),
(D/p) = 1, p not dividing D * den(R_D).  R_D in Q[J]/(H_D) is the exact
representation of the weight-zero CM value S = s_2(tau) = 2 A c/(3 B)
computed in results/cm_tables.json from characteristic-zero endomorphism
loops (no characteristic-p slope used).  The two seeds (j = 0, 1728) have
beta = 0 and are handled separately.

Cost for fixed D: computing j (one inversion), evaluating H_D and R_D
(O(h(D)) field operations each, h = class number), one inversion of 2A.
Table size grows with D (degree h, coefficient digits recorded in the
table); it is constant only because D is fixed.  The Kronecker test (D/p) is
a residue test for these D (quadratic reciprocity).
"""
import json, os, sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling d7_seed, also when loaded by path
from d7_seed import validate_prime  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TABLE_PATH = os.path.join(os.path.dirname(HERE), 'results', 'cm_tables.json')


def load_table(path=TABLE_PATH):
    raw = json.load(open(path))
    table = {}
    for name, v in raw.items():
        table[v['D']] = {'name': name, 'H': [int(c) for c in v['H_D_low_to_high']],
                         'R': [Fraction(c) for c in v['R_D_low_to_high']],
                         'den': int(v['R_D_common_denominator'])}
    return table


SPLIT_TEST = {  # (D/p) = 1 for p not dividing 2D, by quadratic reciprocity
    -7: lambda p: p % 7 in (1, 2, 4), -8: lambda p: p % 8 in (1, 3),
    -12: lambda p: p % 3 == 1, -48: lambda p: p % 3 == 1, -192: lambda p: p % 3 == 1,
    -16: lambda p: p % 4 == 1, -64: lambda p: p % 4 == 1, -256: lambda p: p % 4 == 1,
}


def _ev(poly, x, p):
    s = 0
    for c in reversed(poly):
        s = (s * x + c) % p
    return s


def _ev_frac(poly, x, p):
    s = 0
    for c in reversed(poly):
        s = (s * x + c.numerator * pow(c.denominator, -1, p)) % p
    return s


def slope_from_cm_table(A, B, p, table=None):
    """Return list of (D, beta/H) for every table discriminant whose class
    polynomial vanishes at j(E); raises on excluded primes."""
    validate_prime(p)
    table = table or load_table()
    A %= p
    B %= p
    if (4 * A**3 + 27 * B * B) % p == 0:
        raise ValueError('singular')
    if A == 0 or B == 0:
        return [('seed', 0)] if ((A == 0 and p % 3 == 1) or (B == 0 and p % 4 == 1)) else []
    j = 1728 * 4 * pow(A, 3, p) * pow((4 * pow(A, 3, p) + 27 * B * B) % p, -1, p) % p
    hits = []
    for D, t in table.items():
        if D % p == 0 or t['den'] % p == 0 or not SPLIT_TEST[D](p):
            continue
        if _ev(t['H'], j, p) != 0:
            continue
        S = _ev_frac(t['R'], j, p)
        slope = -3 * B * S * pow(2 * A, -1, p) % p
        hits.append((D, slope))
    return hits
