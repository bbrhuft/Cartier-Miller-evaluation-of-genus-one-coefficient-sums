"""Direct parameter certificate for the depth-three family below the ordinary
B=0 (j=1728) seed: complex multiplication by the order of discriminant -256.

Standard-library research prototype; companion of depth_three_recognize.py
(the A=0 family). Arithmetic is in F_p[s]/(s^4-2), e = s^2 = sqrt(2).

Family (s^4 = 2 in F_p, r nonzero, p = x^2 + 64 y^2):
    A = alpha(s) r^2,  B = gamma(s) r^3,  beta = -(7+4s+6s^2+4s^3) r H.
Forward kernel roots from the seed (-r^2, 0): r, (1+2s^2) r, (1+4s+2s^2+4s^3) r.
Recognition: L = B^2 alpha^3 - A^3 gamma^2 = U0+U1 s+U2 s^2+U3 s^3; the
relative norm L(s)L(-s) = P0 + P1 e gives e = -P0/P1; then L is linear in s
over F_p[e], giving s = -(U0+U2 e)/(U1+U3 e); then r = alpha B/(gamma A).
Everything is verified, including forward and reverse rooted paths.

Exact trace (no point counting): the accepted curve has the trace of its seed
y^2 = x^3 - r^2 x, which by Ireland & Rosen (1990), Ch. 18, Sec. 4, Theorem 5
equals 2 (r/p) a, where p = a^2 + b^2 with pi = a + b i primary
(a odd, b even, a + b = 1 mod 4). Cornacchia gives (a, b) from sqrt(-1).
"""
from pathlib import Path
from dataclasses import dataclass
from math import isqrt
import random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from depth_three_recognize import (ProofViolation, validate_prime, _int_pair,  # noqa: E402
                                   RecognizedPreparation, CMPreparation, _ec_mul, _sqrt_mod)
from isogeny_closure import check_short, quotient, verify_path, short_model  # noqa: E402
from branch_evaluator import BranchEvaluator, check_cubic  # noqa: E402

FAMILY = 'depth3_1728_disc_-256'
# Exact integer data in the basis (1, s, s^2, s^3), s^4 = 2; see theory/b0/b0_family_constants.json.
ALPHA = (-731, -600, -540, -360)
GAMMA = (-14798, -11816, -10164, -8456)
MULTIPLIER = (-7, -4, -6, -4)          # beta / (r H)
ALPHA_CUBED = (-5570535491, -4681110600, -3938178420, -3310589880)
GAMMA_SQUARED = (825258980, 693493472, 583439472, 490459424)
KERNEL_ROOTS = ((1, 0, 0, 0), (1, 0, 2, 0), (1, 4, 2, 4))
REVERSE_ROOTS = ((-2, -8, -4, -8), (-8, 0, -16, 0), (-32, 0, 0, 0))


def ev(t, s, p):
    return (t[0] + t[1]*s + t[2]*s*s + t[3]*s*s*s) % p


def prime_is_eligible(p):
    """p = 1 mod 8 and 2 a quartic residue (equivalently p = x^2 + 64 y^2).
    Costs one exponentiation: no fixed modulus decides this (dihedral class field)."""
    return p % 8 == 1 and pow(2, (p-1)//4, p) == 1


def _base(A, B, p, status, **extra):
    out = {'status': status, 'p': p, 'short_model': [A, B], 'family': FAMILY,
           'scope': 'nondual depth-three closure of the ordinary B=0 seed; p = x^2+64y^2; all quadratic twists',
           'graph_search_used': False, 'square_root_search_used': False}
    out.update(extra)
    return out


def _certificate(A, B, p, s, r):
    s %= p; r %= p
    if p % 8 != 1:
        raise ValueError('depth-three B=0 family requires p = 1 mod 8')
    if (pow(s, 4, p) - 2) % p or r == 0:
        raise ValueError('invalid B=0 depth-three parameters: need s^4=2, r nonzero')
    alpha = ev(ALPHA, s, p); gamma = ev(GAMMA, s, p)
    if alpha == 0 or gamma == 0:
        raise ProofViolation('excluded coefficient degeneration inside the eligible prime class')
    if A != alpha*r*r % p or B != gamma*r**3 % p:
        raise ValueError('parameters do not reproduce both short coefficients')
    forward = [ev(t, s, p)*r % p for t in KERNEL_ROOTS]
    model = (-r*r % p, 0)
    forward_models = [list(model)]
    for i, q in enumerate(forward):
        if i and q == -2*forward[i-1] % p:
            raise AssertionError('forward step is an immediate dual')
        if q == 0:
            raise AssertionError('zero kernel root stays among the seeds')
        model = quotient(*model, q, p)
        forward_models.append(list(model))
    if model != (A, B):
        raise AssertionError('forward kernel path does not reach the input model')
    reverse = [ev(t, s, p)*r % p for t in REVERSE_ROOTS]
    path = verify_path(A, B, p, reverse)
    if tuple(path['endpoint']) != (-pow(64*r, 2, p) % p, 0) or path['seed_family'] != 'B=0,p=1mod4':
        raise AssertionError('reverse path does not end at the 4^3-scaled seed')
    slope = ev(MULTIPLIER, s, p)*r % p
    if path['beta_multiplier'] != slope:
        raise AssertionError('independent reverse-path slope mismatch')
    return {'status': 'verified_parameter_certificate', 'p': p, 'short_model': [A, B], 'family': FAMILY,
            'parameters': {'s': s, 'e': s*s % p, 'r': r, 's_fourth_power': 2},
            'beta_multiplier': slope, 'depth': 3,
            'forward_seed': [-r*r % p, 0], 'forward_roots': forward, 'forward_models': forward_models,
            'reverse_path': path, 'reverse_square_scale': pow(4, 3, p),
            'recognition_field_work': 'O(1), excludes prime validation, eligibility exponentiation and trace preparation',
            'square_root_search_used': False}


def recognize_depth_three_b0(A, B, p):
    """Direct recognition of the B=0 depth-three family; O(1) field work.
    For a status label on non-members at p = 1 mod 8 the eligibility test
    2^((p-1)/4) = 1 costs one exponentiation; it is not needed for acceptance."""
    validate_prime(p); A, B = check_short(*_int_pair(A, B), p)
    if p % 8 != 1:
        return _base(A, B, p, 'not_eligible_prime', reason='family requires p = 1 mod 8 and 2 a quartic residue')
    def reject(reason, **extra):
        status = 'not_in_depth_three_b0_family' if prime_is_eligible(p) else 'not_eligible_prime'
        return _base(A, B, p, status, reason=reason, **extra)
    if A == 0 or B == 0:
        return reject('j in {0,1728}; alpha and gamma are nonzero at eligible primes')
    A3 = pow(A, 3, p); B2 = B*B % p
    U0, U1, U2, U3 = [(B2*a - A3*c) % p for a, c in zip(ALPHA_CUBED, GAMMA_SQUARED)]
    P0 = (U0*U0 + 2*U2*U2 - 4*U1*U3) % p
    P1 = (2*U0*U2 - U1*U1 - 2*U3*U3) % p
    if P1 == 0:
        return reject('relative-norm denominator vanishes (impossible for a member at an eligible prime)')
    e = -P0*pow(P1, -1, p) % p
    if e*e % p != 2:
        return reject('extracted e is not a square root of 2', extracted={'e': e})
    den = (U1 + U3*e) % p
    if den == 0:
        return reject('linear-step denominator vanishes (impossible for a member at an eligible prime)', extracted={'e': e})
    s = -(U0 + U2*e)*pow(den, -1, p) % p
    if s*s % p != e:
        return reject('extracted s is not a square root of e', extracted={'e': e, 's': s})
    alpha = ev(ALPHA, s, p); gamma = ev(GAMMA, s, p)
    if alpha == 0 or gamma == 0:
        raise ProofViolation('excluded coefficient degeneration inside the eligible prime class')
    r = alpha*B*pow(gamma*A, -1, p) % p
    if r == 0 or A != alpha*r*r % p or B != gamma*r**3 % p:
        return reject('both coefficient equations fail', extracted={'e': e, 's': s, 'r': r})
    return _base(A, B, p, 'recognized', matches=[_certificate(A, B, p, s, r)])


def verify_supplied_certificate_b0(p, A, B, certificate):
    """Field-by-field reverification of a stored B=0 certificate."""
    validate_prime(p); A, B = check_short(*_int_pair(A, B), p)
    if certificate.get('family') != FAMILY:
        raise ValueError('certificate family mismatch')
    params = certificate.get('parameters', {})
    cert = _certificate(A, B, p, params['s'], params['r'])
    for key, stored in certificate.items():
        if key not in cert:
            raise ValueError('stored certificate carries unknown field %s' % key)
        if key == 'parameters':
            if not isinstance(stored, dict) or any(k not in cert[key] for k in stored):
                raise ValueError('stored parameters carry unknown field')
            if any(stored.get(k) is not None and stored[k] % p != cert[key][k] for k in ('s', 'e', 'r')) or \
               stored.get('s_fourth_power', 2) != 2:
                raise ValueError('stored parameters disagree with recomputed certificate')
        elif stored != cert[key]:
            raise ValueError('stored %s disagrees with recomputed certificate' % key)
    return cert


# ---------------------------------------------------------------------------
# Exact trace by Ireland & Rosen, Ch. 18, Sec. 4, Theorem 5: for p = 1 mod 4,
# p not dividing D, p = pi conj(pi) in Z[i] with pi = 1 mod (2+2i),
#     N_p(y^2 = x^3 - D x) = p + 1 - conj((D/pi)_4) pi - (D/pi)_4 conj(pi).
# For the seed D = r^2 the quartic symbol is (r^2/pi)_4 = (r/p), so the
# trace is 2 (r/p) a with pi = a + b i primary (a odd, b even, a+b = 1 mod 4).
# ---------------------------------------------------------------------------

def gaussian_prime_from_cornacchia(p, rng=None):
    """Return (a, b, info) with p = a^2 + b^2, a odd, b even and a + b = 1 mod 4.
    sqrt(-1) = c^((p-1)/4) for a quadratic nonresidue c found by random search."""
    validate_prime(p)
    if p % 4 != 1:
        raise ValueError('p must be 1 mod 4')
    if rng is None:
        rng = random.SystemRandom()
    trials = 0
    while True:
        trials += 1
        c = rng.randrange(2, p)
        if pow(c, (p-1)//2, p) == p-1:
            break
    i = pow(c, (p-1)//4, p)
    if i*i % p != p-1:
        raise ProofViolation('square root of -1 failed')
    if i <= p//2:
        i = p-i
    a0, b0 = p, i
    bound = isqrt(p)
    while b0 > bound:
        a0, b0 = b0, a0 % b0
    x = b0; y = isqrt(p-x*x)
    if x*x+y*y != p:
        raise ArithmeticError('Cornacchia failed for p = x^2 + y^2')
    a, b = (x, y) if x % 2 else (y, x)
    if (a+b) % 4 != 1:
        a = -a
    assert a*a+b*b == p and a % 2 and b % 2 == 0 and (a+b) % 4 == 1
    return a, b, {'a': a, 'b': b, 'nonresidue_trials': trials, 'method': 'Cornacchia on p = a^2 + b^2'}


def seed_trace_quartic(p, r, pi):
    """Exact trace of y^2 = x^3 - r^2 x by Ireland-Rosen Theorem 5 (D = r^2)."""
    a, b = pi
    if r % p == 0:
        raise ValueError('r must be nonzero')
    leg = 1 if pow(r % p, (p-1)//2, p) == 1 else -1
    return 2*leg*a, {'primary_pi': [a, b], 'legendre_r': leg}


def seed_trace_quartic_general(p, D, pi):
    """Theorem 5 for general D (validation helper): quartic symbol (D/pi)_4 = i^k
    with D^((p-1)/4) = i^k mod pi and i = -a/b mod pi."""
    a, b = pi
    im = (-a*pow(b, -1, p)) % p
    if (im*im+1) % p:
        raise ProofViolation('image of i is not a square root of -1')
    s = pow(D % p, (p-1)//4, p)
    powers = [1, im, p-1, p-im]
    k = powers.index(s)
    chi = [(1, 0), (0, 1), (-1, 0), (0, -1)][k]          # i^k as (re, im)
    cc = (chi[0], -chi[1])
    re = cc[0]*a - cc[1]*b                                 # Re(conj(chi) * pi)
    return 2*re


def _cm_necessary_check_b0(p, t):
    rem = 4*p - t*t
    if rem <= 0 or rem % 256:
        return False
    y = isqrt(rem//256)
    return y >= 1 and 256*y*y == rem


def prepare_from_trace_b0(p, f, trusted_exact_trace, *, verify_trace=False, rng=None):
    """K reconstruction for a normalized cubic whose short model is in the B=0
    family. The supplied trace must pass the Hasse interval and the necessary
    condition 4p - t^2 = 256 y^2, y >= 1; verify_trace=True recomputes it
    exactly by Theorem 5 and rejects any disagreement."""
    validate_prime(p); f = check_cubic(f, p)
    t = trusted_exact_trace
    if not isinstance(t, int) or isinstance(t, bool) or t*t > 4*p:
        raise ValueError('trace fails necessary Hasse interval; not a certification test')
    A, B = short_model(f, p)
    rec = recognize_depth_three_b0(A, B, p)
    if rec['status'] != 'recognized':
        return rec
    if not _cm_necessary_check_b0(p, t):
        raise ValueError('supplied trace violates the family condition 4p - t^2 = 256 y^2 with y >= 1')
    cert = rec['matches'][0]
    method = 'direct_depth_three_b0_caller_supplied_exact_trace'
    if verify_trace:
        a, b, _ = gaussian_prime_from_cornacchia(p, rng)
        exact, _ = seed_trace_quartic(p, cert['parameters']['r'], (a, b))
        if exact != t:
            raise ValueError('supplied trace %d is wrong: the verified trace is %d' % (t, exact))
        method = 'direct_depth_three_b0_caller_supplied_exact_trace_verified'
    H = t % p
    beta = cert['beta_multiplier']*H % p
    _, _, bb, aa = f
    K = (beta - bb*pow(3, -1, p)*H)*pow(aa, -1, p) % p
    return RecognizedPreparation(BranchEvaluator(p, f, H, K, method), cert, t)


def _las_vegas_sign_b0(A, B, p, t0, rng, max_trials):
    """Las Vegas choice between traces +t0 and -t0 for a recognized B=0-seed
    member (added on integration into the consolidated release, 12 October 2026).
    The consolidated A=0 routine decide_trace_sign is restricted to its own family
    because its 1/5 success bound is proved only there; no success bound is claimed
    here. A trial is conclusive when exactly one candidate order kills a random
    rational point; both killing it is inconclusive; neither contradicts the
    classical two-candidate statement and raises ProofViolation."""
    A %= p; B %= p
    n_plus, n_minus = p+1-t0, p+1+t0
    from itertools import count
    for trial in (count(1) if max_trials is None else range(1, max_trials+1)):
        x = rng.randrange(p)
        y = _sqrt_mod(x**3+A*x+B, p, rng)
        if not y:
            continue
        P = (x, y)
        k_plus = _ec_mul(n_plus, P, A, p) is None
        k_minus = _ec_mul(n_minus, P, A, p) is None
        if k_plus and not k_minus:
            return t0, {'status': 'conclusive', 'trials': trial, 'success_bound': 'none claimed for this family'}
        if k_minus and not k_plus:
            return -t0, {'status': 'conclusive', 'trials': trial, 'success_bound': 'none claimed for this family'}
        if not k_plus and not k_minus:
            raise ProofViolation('neither candidate order kills a rational point')
    return None, {'status': 'inconclusive_after_max_trials', 'trials': max_trials}


def prepare_cm_b0(p, f, *, rng=None, sign_method='quartic', max_trials=32):
    """Complete preparation with no supplied trace: recognition, Cornacchia on
    p = a^2 + b^2, exact trace 2 (r/p) a by Theorem 5 (default), or the Las
    Vegas point test between +-2|a| (sign_method='las_vegas'); then H, beta, K.
    Randomized only in the quadratic-nonresidue search for sqrt(-1)."""
    validate_prime(p); f = check_cubic(f, p)
    if rng is None:
        rng = random.SystemRandom()
    if sign_method not in ('quartic', 'las_vegas'):
        raise ValueError('sign_method must be quartic or las_vegas')
    A, B = short_model(f, p)
    rec = recognize_depth_three_b0(A, B, p)
    if rec['status'] != 'recognized':
        return rec
    cert = rec['matches'][0]
    a, b, info = gaussian_prime_from_cornacchia(p, rng)
    if b % 8:
        raise ProofViolation('depth-three curve but 8 does not divide b in p = a^2 + b^2')
    t0 = 2*abs(a)
    if sign_method == 'quartic':
        t, sign_info = seed_trace_quartic(p, cert['parameters']['r'], (a, b))
        sign_info.update({'status': 'deterministic',
                          'source': 'Ireland & Rosen (1990), Ch. 18, Sec. 4, Theorem 5, applied to the seed (-r^2, 0)'})
        method = 'direct_depth_three_b0_cm_cornacchia_quartic_trace'
    else:
        t, sign_info = _las_vegas_sign_b0(A, B, p, t0, rng, max_trials)
        if t is None:
            return {'status': 'trace_sign_inconclusive', 'p': p, 'candidates': [t0, -t0], 'cornacchia': info,
                    'sign_test': sign_info, 'certificate': cert}
        method = 'direct_depth_three_b0_cm_cornacchia_las_vegas_sign'
    H = t % p
    beta = cert['beta_multiplier']*H % p
    _, _, bb, aa = f
    K = (beta - bb*pow(3, -1, p)*H)*pow(aa, -1, p) % p
    prep = {'trace_candidates': [t0, -t0], 'representation_p': [a, b], 'cornacchia': info, 'sign_test': sign_info,
            'cost': 'recognition O(1); randomized nonresidue search for sqrt(-1); Cornacchia O(log p) word steps; '
                    'trace: one Legendre symbol, O(log p) field operations'}
    return CMPreparation(BranchEvaluator(p, f, H, K, method), cert, t, prep)


def family_member_b0(p, s, r):
    validate_prime(p)
    s %= p; r %= p
    if p % 8 != 1 or (pow(s, 4, p)-2) % p or r == 0:
        raise ValueError('need p = 1 mod 8, s^4 = 2, r nonzero')
    return ev(ALPHA, s, p)*r*r % p, ev(GAMMA, s, p)*r**3 % p
