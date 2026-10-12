"""Control discriminant D = -8 (not the principal new result).
All short models with j = 8000 at primes p = 1 or 3 (mod 8):
(A, B) = (-30 r^2, 56 r^3), r = -15B/(28A), and beta/H = r = -15B/(28A).
Endomorphism used in the proof: sqrt(-2) = normalized 2-isogeny with the
rational kernel root q = 4r followed by the isomorphism with u^2 = -2;
de Rham matrix [[u, -q/u], [0, 2/u]], so beta/H = q/(2-u^2) = q/4 = r.
No trace route is certified here; the control is used for the slope only.
"""
from d7_seed import validate_prime, check_short, ProofViolation

FAMILY = 'cm_control_disc_-8'
A0, B0 = -30, 56


def is_admissible(p):
    return p % 8 in (1, 3)


def recognize_d8(A, B, p):
    validate_prime(p)
    A, B = check_short(A, B, p)
    base = {'p': p, 'short_model': [A, B], 'family': FAMILY}
    if not is_admissible(p):
        return dict(base, status='not_eligible_prime')
    if A == 0 or B == 0 or (392 * pow(A, 3, p) + 3375 * B * B) % p:
        return dict(base, status='not_in_family')
    r = -15 * B * pow(28 * A, -1, p) % p
    if r == 0 or A != A0 * r * r % p or B != B0 * r**3 % p:
        raise ProofViolation('j = 8000 with AB != 0 must give a member')
    return dict(base, status='recognized', parameters={'r': r}, beta_multiplier=r % p)


def endomorphism_certificate(A, B, p, v):
    """v: a square root of -2 mod p."""
    rec = recognize_d8(A, B, p)
    if rec['status'] != 'recognized':
        raise ValueError('not a member')
    r = rec['parameters']['r']
    if (v * v + 2) % p:
        raise ValueError('v is not sqrt(-2)')
    q = 4 * r % p
    if (q**3 + A*q + B) % p:
        raise ProofViolation('q not a root')
    A1, B1 = (-4*A - 15*q*q) % p, (-8*A*q - 22*q**3) % p
    if A1 != pow(v, 4, p) * A % p or B1 != pow(v, 6, p) * B % p:
        raise ProofViolation('quotient not (u^4A, u^6B)')
    lam, mu, nu = v % p, (-v) % p, (-q * pow(v, -1, p)) % p
    slope = nu * pow((lam - mu) % p, -1, p) % p
    if slope != r % p:
        raise ProofViolation('slope mismatch')
    return {'q': q, 'u': v % p, 'beta_over_H_from_endomorphism': slope}
