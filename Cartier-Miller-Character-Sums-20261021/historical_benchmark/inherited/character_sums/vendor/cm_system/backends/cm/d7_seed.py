"""Class-number-one seed D = -7: direct recognition, Cartier slope, signed
CM trace and original-cubic evaluator.  Standard library only.

Theorem (extension note, Theorem 4).  Let p be prime, p >= 11, p = 1, 2 or 4
(mod 7).  Every short model y^2 = x^3 + A x + B over F_p with A B != 0 and
28 A^3 + 125 B^2 = 0 (equivalently j = -3375) is (A, B) = (-35 r^2, -98 r^3)
with r = 5B/(14A) in F_p^*.  Its reduction is ordinary, and with
h = (p-1)/2, H = [x^(p-1)] F^h, beta = [x^(p-2)] F^h:

        beta = -r H = -(5B/(14A)) H,       H != 0.

Proof sketch (full proof in the note): the horizontal 2-isogeny with kernel
root q = r(-7+e)/2, e^2 = -7, followed by the isomorphism with scale
u = (1+e)/2, is an F_p-rational endomorphism with de Rham matrix
[[u, -q/u], [0, 2/u]]; Cartier commutes with it, giving
beta (u^2 - 2) = -q H, i.e. beta/H = q/(2 - u^2) = -r.

Signed trace (Theorem 5 in the note): t is the unique integer with
4p = t^2 + 7 v^2 (v integer) and Legendre symbol (t/7) = (r/p).
Two independent derivations are given in the note (Hecke character of
conductor (sqrt-7); 2-adic structure of E(F_p)); both are implemented here.

Conventions follow the retained project code: cubic f = 1 + c w + b w^2 + a w^3
given low-to-high as [1, c, b, a]; x = a w + b/3, y = a v;
A = a c - b^2/3, B = a^2 - a b c/3 + 2 b^3/27; beta = a K + (b/3) H;
T_f(mu) = sum_{i<p} d_i mu^i with f^h = sum d_i w^i; for a nonzero simple root
mu of f:  T_f(mu) = a mu (mu H - K) / f'(mu);  S_f(1/mu) = T_f(mu).
"""
from dataclasses import dataclass
from math import isqrt
import random

FAMILY = 'cm_seed_disc_-7'
A0, B0 = -35, -98                 # j = -3375, y^2 = x^3 - 35x - 98 (= 49a1 scaled by u = 2)
S2_VALUE = (5, 21)                # weight-zero CM value s_2((1+sqrt(-7))/2) = 5/21
ADMISSIBLE_RESIDUES_MOD_7 = (1, 2, 4)


class ProofViolation(AssertionError):
    """Raised if an identity proved in the note fails (would indicate a bug)."""


# ---------------------------------------------------------------- primes
def is_prime64(n):
    """Deterministic Miller-Rabin for n < 2^64 (bases of Jaeschke/Sinclair)."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 2 or n >= 2**64:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        x = pow(a % n, d, n)
        if a % n == 0 or x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def validate_prime(p):
    if not isinstance(p, int) or isinstance(p, bool) or p < 7 or not is_prime64(p):
        raise ValueError('require prime 7 <= p < 2^64')


def is_admissible(p):
    """(-7/p) = (p/7) = 1 and p != 7; p >= 11 is implied by p >= 7, p != 7."""
    return p != 7 and p % 7 in ADMISSIBLE_RESIDUES_MOD_7


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def legendre7(t):
    return {0: 0, 1: 1, 2: 1, 4: 1, 3: -1, 5: -1, 6: -1}[t % 7]


# ---------------------------------------------------------------- models
def check_short(A, B, p):
    if any(isinstance(v, bool) or not isinstance(v, int) for v in (A, B)):
        raise ValueError('short coefficients must be integers')
    A %= p
    B %= p
    if (4 * A**3 + 27 * B**2) % p == 0:
        raise ValueError('singular short cubic')
    return A, B


def check_cubic(f, p):
    if len(f) != 4 or any(isinstance(x, bool) or not isinstance(x, int) for x in f):
        raise ValueError('use four integer coefficients [1, c, b, a]')
    f = tuple(x % p for x in f)
    if f[0] != 1 or f[3] == 0:
        raise ValueError('require f(0) = 1 and degree exactly three')
    d, c, b, a = f
    disc = b*b*c*c - 4*a*c**3 - 4*b**3*d - 27*a*a*d*d + 18*a*b*c*d
    if disc % p == 0:
        raise ValueError('cubic is not squarefree modulo p')
    return f


def short_model(f, p):
    _, c, b, a = f
    i3 = pow(3, -1, p)
    return ((a*c - b*b*i3) % p, (a*a - a*b*c*i3 + 2*b**3*pow(27, -1, p)) % p)


def family_member(p, r):
    validate_prime(p)
    r %= p
    if r == 0:
        raise ValueError('r must be nonzero')
    return (A0 * r * r) % p, (B0 * r**3) % p


# ---------------------------------------------------------------- recognition
def _base(A, B, p, status, **extra):
    out = {'status': status, 'p': p, 'short_model': [A, B], 'family': FAMILY,
           'scope': 'all short models with j = -3375 (all quadratic twists) at primes p = 1,2,4 mod 7, p != 7',
           'square_root_search_used': False, 'point_counting_used': False}
    out.update(extra)
    return out


def _certificate(A, B, p, r):
    r %= p
    if not is_admissible(p):
        raise ValueError('D=-7 seed requires p = 1, 2 or 4 mod 7 and p != 7')
    if r == 0 or A != A0 * r * r % p or B != B0 * r**3 % p:
        raise ValueError('parameter r does not reproduce both short coefficients')
    slope = (-r) % p
    # Redundant closed form, computed independently of r:
    if slope != (-5 * B * pow(14 * A, -1, p)) % p:
        raise ProofViolation('closed form -5B/(14A) disagrees with -r')
    return {'status': 'verified_parameter_certificate', 'p': p, 'short_model': [A, B],
            'family': FAMILY, 'parameters': {'r': r}, 'beta_multiplier': slope,
            'cm_value_s2': '5/21', 'slope_formula': 'beta/H = -(3B/(2A)) * 5/21 = -5B/(14A) = -r',
            'recognition_field_work': 'O(1): one inversion and fixed products; excludes prime validation',
            'square_root_search_used': False}


def recognize_d7(A, B, p):
    """Direct recognition of the D=-7 seed family (all twists). O(1) field work
    after prime validation. Eligibility is a residue test of p modulo 7."""
    validate_prime(p)
    A, B = check_short(A, B, p)
    if not is_admissible(p):
        return _base(A, B, p, 'not_eligible_prime',
                     reason='need (-7/p) = (p/7) = 1 and p != 7; otherwise j=-3375 reduces to a supersingular or singular curve')
    if A == 0 or B == 0:
        return _base(A, B, p, 'not_in_family', reason='j in {0, 1728}; j=-3375 is neither at admissible primes')
    if (28 * pow(A, 3, p) + 125 * B * B) % p:
        return _base(A, B, p, 'not_in_family', reason='28 A^3 + 125 B^2 != 0, i.e. j != -3375')
    r = 5 * B * pow(14 * A, -1, p) % p
    if r == 0 or A != A0 * r * r % p or B != B0 * r**3 % p:
        raise ProofViolation('j = -3375 with AB != 0 must give a member; algebra failed')
    return _base(A, B, p, 'recognized', matches=[_certificate(A, B, p, r)])


def verify_supplied_certificate(p, A, B, certificate):
    """Reverify a stored certificate; every stored field must equal the
    recomputed value; unknown top-level or nested fields are rejected."""
    validate_prime(p)
    A, B = check_short(A, B, p)
    if certificate.get('family') != FAMILY:
        raise ValueError('certificate family mismatch')
    params = certificate.get('parameters', {})
    if set(params) - {'r'}:
        raise ValueError('unknown parameter field')
    cert = _certificate(A, B, p, params['r'])
    for key, stored in certificate.items():
        if key not in cert:
            raise ValueError('stored certificate carries unknown field %s' % key)
        if key == 'parameters':
            if stored['r'] % p != cert['parameters']['r']:
                raise ValueError('stored parameter r disagrees')
        elif stored != cert[key]:
            raise ValueError('stored %s disagrees with recomputed certificate' % key)
    return cert


# ---------------------------------------------------------------- square roots
def sqrt_mod(n, p, rng=None, stats=None):
    """Square root modulo p. Deterministic exponentiation for p = 3 mod 4 and
    p = 5 mod 8 (Atkin); otherwise Tonelli-Shanks with a randomized
    quadratic-nonresidue search whose trial count is recorded."""
    n %= p
    if stats is None:
        stats = {}
    if n == 0:
        return 0
    if legendre(n, p) != 1:
        raise ValueError('not a quadratic residue')
    if p % 4 == 3:
        stats['method'] = 'exponent (p+1)/4'
        x = pow(n, (p + 1) // 4, p)
    elif p % 8 == 5:
        stats['method'] = 'Atkin p=5 mod 8'
        g = pow(2 * n, (p - 5) // 8, p)
        i = 2 * n * g * g % p
        x = n * g * (i - 1) % p
    else:
        rng = rng or random.SystemRandom()
        trials = 0
        while True:
            trials += 1
            z = rng.randrange(2, p)
            if legendre(z, p) == -1:
                break
        stats['method'] = 'Tonelli-Shanks, randomized nonresidue search'
        stats['nonresidue_trials'] = trials
        q, s = p - 1, 0
        while q % 2 == 0:
            q //= 2
            s += 1
        m, c, t, x = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
        while t != 1:
            i, tt = 0, t
            while tt != 1:
                tt = tt * tt % p
                i += 1
            b = pow(c, 1 << (m - i - 1), p)
            m, c, t, x = i, b * b % p, t * b * b % p, x * b % p
    if x * x % p != n:
        raise ProofViolation('square root check failed')
    return x


# ---------------------------------------------------------------- endomorphism certificate
def endomorphism_certificate(A, B, p, e):
    """Check, from a supplied square root e of -7, the explicit endomorphism
    used in the proof and recompute beta/H = q/(2 - u^2) (Theorem 1)."""
    validate_prime(p)
    A, B = check_short(A, B, p)
    rec = recognize_d7(A, B, p)
    if rec['status'] != 'recognized':
        raise ValueError('model not in the D=-7 family')
    r = rec['matches'][0]['parameters']['r']
    e %= p
    if (e * e + 7) % p:
        raise ValueError('supplied e is not a square root of -7')
    i2 = pow(2, -1, p)
    q = r * (-7 + e) * i2 % p
    if (q**3 + A*q + B) % p:
        raise ProofViolation('kernel coordinate is not a root')
    A1 = (-4*A - 15*q*q) % p
    B1 = (-8*A*q - 22*q**3) % p
    u = (1 + e) * i2 % p
    if (u*u - u + 2) % p:
        raise ProofViolation('u^2 - u + 2 != 0')
    if A1 != pow(u, 4, p) * A % p or B1 != pow(u, 6, p) * B % p:
        raise ProofViolation('quotient is not (u^4 A, u^6 B)')
    lam, mu, nu = u, 2 * pow(u, -1, p) % p, (-q * pow(u, -1, p)) % p
    if lam == mu:
        raise ProofViolation('eigenvalues coincide (needs p != 7)')
    slope = nu * pow((lam - mu) % p, -1, p) % p
    if slope != (-r) % p:
        raise ProofViolation('Theorem 1 slope disagrees with -r')
    return {'kernel_root_q': q, 'quotient': [A1, B1], 'u': u, 'lambda': lam, 'mu': mu, 'nu': nu,
            'beta_over_H_from_endomorphism': slope, 'agrees_with_minus_r': True}


# ---------------------------------------------------------------- signed trace
def cornacchia_4p_7(p, e=None, rng=None, stats=None):
    """Return (t0, v0) > 0 with 4p = t0^2 + 7 v0^2 (Cohen, Alg. 1.5.3).
    e: optional square root of -7 mod p (else computed)."""
    if stats is None:
        stats = {}
    if e is None:
        e = sqrt_mod(-7, p, rng, stats)
    x0 = e % p
    if x0 % 2 == 0:            # need x0 = D = -7 = 1 (mod 2)
        x0 = p - x0
    a, b, bound = 2 * p, x0, isqrt(4 * p)
    while b > bound:
        a, b = b, a % b
    rem = 4 * p - b * b
    if rem <= 0 or rem % 7:
        raise ArithmeticError('Cornacchia failed (p not of the form required)')
    v = isqrt(rem // 7)
    if 7 * v * v != rem or v == 0:
        raise ArithmeticError('Cornacchia failed (p not of the form required)')
    stats['cornacchia'] = {'t0': b, 'v0': v}
    return b, v, e


def signed_trace_d7(p, r, *, method='hecke', e=None, rng=None):
    """Exact Frobenius trace of y^2 = x^3 - 35 r^2 x - 98 r^3 at admissible p.
    method='hecke': t = (r/p) * (t0/7) * t0   (Theorem 5(a));
    method='two_adic': 2-adic halving criterion (Theorem 5(b))."""
    validate_prime(p)
    if not is_admissible(p):
        raise ValueError('trace formula requires an admissible prime')
    r %= p
    if r == 0:
        raise ValueError('r must be nonzero')
    stats = {}
    t0, v0, e = cornacchia_4p_7(p, e, rng, stats)
    if method == 'hecke':
        t = t0 * legendre7(t0) * legendre(r, p)
        stats['sign_rule'] = '(t/7) = (r/p)'
    elif method == 'two_adic':
        i2 = pow(2, -1, p)
        q = r * (-7 + e) * i2 % p           # kernel root of alpha = (1+sqrt-7)/2 with u = (1+e)/2
        e2 = 7 * r % p
        e3 = r * (-7 - e) * i2 % p
        s1, s2 = legendre(q - e2, p), legendre(q - e3, p)
        if s1 != s2:
            raise ProofViolation('2-adic consistency s1 = s2 violated')
        # Frobenius pi = (t + v sqrt(-7))/2 lies in the prime above p fixed by sqrt(-7) -> e
        v = v0 if (t0 + v0 * e) % p == 0 else -v0
        if (t0 + v * e) % p:
            raise ProofViolation('no sign of v places pi in the prime of the embedding')
        x0, y0 = (t0 - v) // 2, v           # pi_+ = x0 + y0 * alpha, alpha = (1+sqrt-7)/2
        pi_plus_1_mod_q2 = (x0 % 2 == 1) and (((x0 - 1) // 2 + y0) % 2 == 0)
        t = t0 if (pi_plus_1_mod_q2 == (s1 == 1)) else -t0
        stats['sign_rule'] = '2-adic: (q,0) in 2E(F_p) iff Frobenius = 1 mod (alpha)^2'
        stats['halving_symbol'] = s1
    else:
        raise ValueError('method must be hecke or two_adic')
    if t * t + 7 * v0 * v0 != 4 * p:
        raise ProofViolation('trace fails 4p = t^2 + 7 v^2')
    return t, stats


def verify_supplied_trace(p, r, t):
    """Deterministic certification of a supplied trace for the D=-7 member
    with parameter r: Hasse bound, CM shape 4p - t^2 = 7 v^2, sign rule."""
    if not isinstance(t, int) or isinstance(t, bool):
        return False, 'trace must be an integer'
    if t * t > 4 * p:
        return False, 'Hasse bound violated'
    rem = 4 * p - t * t
    if rem % 7 or isqrt(rem // 7) ** 2 != rem // 7 or rem == 0:
        return False, 'CM shape 4p - t^2 = 7 v^2 violated'
    if legendre7(t) != legendre(r, p):
        return False, 'sign rule (t/7) = (r/p) violated'
    return True, 'certified'


# ---------------------------------------------------------------- evaluator
def eval_poly(f, x, p):
    s = 0
    for c in reversed(f):
        s = (s * x + c) % p
    return s


@dataclass(frozen=True)
class D7Evaluator:
    p: int
    f: tuple
    H: int
    K: int
    beta: int
    trace: int
    certificate: dict
    trace_info: dict

    def query(self, mu):
        """T_f(mu) = a mu (mu H - K)/f'(mu) at a supplied nonzero simple root."""
        if not isinstance(mu, int) or isinstance(mu, bool):
            raise ValueError('mu must be an integer residue')
        p, f = self.p, self.f
        mu %= p
        if mu == 0:
            raise ValueError('require a nonzero root')
        if eval_poly(f, mu, p) != 0:
            raise ValueError('mu is not a root of f')
        der = (f[1] + 2 * f[2] * mu + 3 * f[3] * mu * mu) % p
        if der == 0:
            raise ValueError('root is not simple')
        T = f[3] * mu * (mu * self.H - self.K) * pow(der, -1, p) % p
        return {'p': p, 'f': list(f), 'mu': mu, 'lambda': pow(mu, -1, p), 'T': T, 'S': T,
                'H': self.H, 'K': self.K, 'query_field_operations': 'O(1)'}


def prepare_cm_d7(p, f, *, trace=None, method='hecke', rng=None):
    """Complete preparation for a normalized cubic in the D=-7 family.
    trace=None: compute the signed trace (Cornacchia + sign rule).
    trace=int: certify the supplied trace (shape and sign); reject if wrong."""
    validate_prime(p)
    f = check_cubic(f, p)
    A, B = short_model(f, p)
    rec = recognize_d7(A, B, p)
    if rec['status'] != 'recognized':
        return rec
    cert = rec['matches'][0]
    r = cert['parameters']['r']
    if trace is None:
        t, info = signed_trace_d7(p, r, method=method, rng=rng)
    else:
        ok, why = verify_supplied_trace(p, r, trace)
        if not ok:
            raise ValueError('supplied trace rejected: ' + why)
        t, info = trace, {'supplied_trace': 'certified by shape and sign rule'}
    H = t % p
    if H == 0:
        raise ProofViolation('H = 0 at an admissible prime')
    beta = cert['beta_multiplier'] * H % p
    _, _, b, a = f
    K = (beta - b * pow(3, -1, p) * H) * pow(a, -1, p) % p
    return D7Evaluator(p, f, H, K, beta, t, cert, info)


def cubic_from_point(p, r, x_P, y_P):
    """Normalized cubic attached to the member with parameter r and a rational
    point P = (x_P, y_P) with y_P != 0: b = 3 x_P, a = y_P,
    c = (A + b^2/3)/a.  (f(0) = 1 corresponds to P.)"""
    A, B = family_member(p, r)
    if y_P % p == 0 or (y_P * y_P - (x_P**3 + A * x_P + B)) % p:
        raise ValueError('need a non-2-torsion rational point')
    b = 3 * x_P % p
    a = y_P % p
    c = (A + b * b * pow(3, -1, p)) * pow(a, -1, p) % p
    f = (1, c, b, a)
    if short_model(f, p) != (A, B):
        raise ProofViolation('cubic does not reproduce the model')
    return f
