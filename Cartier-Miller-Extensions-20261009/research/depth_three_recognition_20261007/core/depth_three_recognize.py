"""Direct parameter certificate for ONE depth-three family: the nondual
rational degree-two closure of the ordinary j=0 easy seed at depth three
(complex multiplication by the order of discriminant -192).

Standard-library research prototype. No point-count backend. A supplied exact
trace remains caller-trusted; the certificate verifies the model equations and
an explicit reverse rooted path with differential scale +1 on every edge.

Family (e^2 = 3, g^2 = 2, r nonzero, p = 1 mod 24):
    A = alpha(e,g) r^2,  B = gamma(e,g) r^3,  beta = -(7+6e+6g+2eg) r H,
with alpha, gamma the integer 4-tuples below in the basis (1, e, g, eg).
Recognition extracts e and g by two relative norms of
    L = B^2 alpha^3 - A^3 gamma^2  in  F_p[e,g]/(e^2-3, g^2-2),
then r = alpha B / (gamma A), and verifies everything. O(1) field work.
"""
from pathlib import Path
from dataclasses import dataclass
from math import isqrt
import random
import sys
from itertools import count
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'isogeny_closure_20261006/core'))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'branch_point_20261006'))
from isogeny_closure import check_short, easy, quotient, verify_path, short_model  # noqa: E402
from branch_evaluator import BranchEvaluator, check_cubic, is_prime64  # noqa: E402

FAMILY = 'depth3_0_disc_-192'
# Exact integer data in the basis (1, e, g, eg); see theory/integer_invariants_depth3.json.
ALPHA = (-1095, -540, -540, -420)
GAMMA = (-22198, -13860, -16380, -8820)
MULTIPLIER = (-7, -6, -6, -2)          # beta / (r H)
ALPHA_CUBED = (-13988298375, -8054356500, -9859360500, -5708191500)
GAMMA_SQUARED = (2072413204, 1193214960, 1460677680, 845626320)
KERNEL_ROOTS = ((1, 0, 0, 0), (1, 2, 0, 0), (1, 2, 6, 2))   # q_i / r, forward from the seed
REVERSE_ROOTS = ((-2, -4, -12, -4), (-8, -16, 0, 0), (-32, 0, 0, 0))  # -2*4^i q_{2-i} / r


class ProofViolation(AssertionError):
    """Raised when a branch the proof excludes at an eligible prime is reached."""


def validate_prime(p):
    if not isinstance(p, int) or isinstance(p, bool) or p < 7 or not is_prime64(p):
        raise ValueError('require prime 7<=p<2^64')


def _int_pair(A, B):
    if any(isinstance(v, bool) or not isinstance(v, int) for v in (A, B)):
        raise ValueError('short coefficients must be integers')
    return A, B


def ev(t, e, g, p):
    return (t[0] + t[1]*e + t[2]*g + t[3]*e*g) % p


def _base(A, B, p, status, **extra):
    out = {'status': status, 'p': p, 'short_model': [A, B], 'family': FAMILY,
           'scope': 'nondual depth-three closure of the ordinary A=0 seed; p=1 mod 24; all quadratic twists',
           'graph_search_used': False, 'square_root_search_used': False}
    out.update(extra)
    return out


def _certificate(A, B, p, e, g, r):
    """Verify (e,g,r) reproduce (A,B), the forward path from the seed and the
    reverse path to a square-scaled easy seed. Raises on any failure."""
    e %= p; g %= p; r %= p
    if p % 24 != 1:
        raise ValueError('depth-three family requires p = 1 mod 24')
    if e*e % p != 3 or g*g % p != 2 or r == 0:
        raise ValueError('invalid depth-three parameters: need e^2=3, g^2=2, r nonzero')
    alpha = ev(ALPHA, e, g, p); gamma = ev(GAMMA, e, g, p)
    if alpha == 0 or gamma == 0:
        raise ProofViolation('excluded coefficient degeneration inside the eligible prime class')
    if A != alpha*r*r % p or B != gamma*r**3 % p:
        raise ValueError('parameters do not reproduce both short coefficients')
    # Forward path from the seed (0,-r^3): independent re-derivation by the quotient map.
    forward = [ev(t, e, g, p)*r % p for t in KERNEL_ROOTS]
    model = (0, -pow(r, 3, p) % p)
    forward_models = [list(model)]
    for i, q in enumerate(forward):
        if i and q == -2*forward[i-1] % p:
            raise AssertionError('forward step is an immediate dual')
        model = quotient(*model, q, p)
        forward_models.append(list(model))
    if model != (A, B):
        raise AssertionError('forward kernel path does not reach the input model')
    # Reverse path, verified by the retained path checker without dividing by H.
    reverse = [ev(t, e, g, p)*r % p for t in REVERSE_ROOTS]
    path = verify_path(A, B, p, reverse)
    d = pow(4, 3, p)
    if tuple(path['endpoint']) != (0, d**3 * (-pow(r, 3, p)) % p) or path['seed_family'] != 'A=0,p=1mod3':
        raise AssertionError('reverse path does not end at the 4^3-scaled seed')
    slope = ev(MULTIPLIER, e, g, p)*r % p
    if path['beta_multiplier'] != slope:
        raise AssertionError('independent reverse-path slope mismatch')
    return {'status': 'verified_parameter_certificate', 'p': p, 'short_model': [A, B], 'family': FAMILY,
            'parameters': {'e': e, 'g': g, 'r': r, 'e_squared': 3, 'g_squared': 2},
            'beta_multiplier': slope, 'depth': 3,
            'forward_seed': [0, -pow(r, 3, p) % p], 'forward_roots': forward, 'forward_models': forward_models,
            'reverse_path': path, 'reverse_square_scale': d,
            'recognition_field_work': 'O(1), excludes prime validation and trace preparation',
            'square_root_search_used': False}


def recognize_depth_three(A, B, p):
    """Direct recognition of the depth-three family. Returns a status record."""
    validate_prime(p); A, B = check_short(*_int_pair(A, B), p)
    if p % 24 != 1:
        return _base(A, B, p, 'not_eligible_prime', reason='family requires p = 1 mod 24 (ordinary A=0 seed and rational sqrt3, sqrt2)')
    if A == 0 or B == 0:
        return _base(A, B, p, 'not_in_depth_three_family', reason='j in {0,1728}; alpha and gamma are nonzero at eligible primes')
    A3 = pow(A, 3, p); B2 = B*B % p
    U0, U1, U2, U3 = [(B2*a - A3*c) % p for a, c in zip(ALPHA_CUBED, GAMMA_SQUARED)]
    # Relative norms of L = U0+U1 e+U2 g+U3 eg to F_p[e] and to F_p[g].
    P0 = (U0*U0 + 3*U1*U1 - 2*U2*U2 - 6*U3*U3) % p; P1 = 2*(U0*U1 - 2*U2*U3) % p
    Q0 = (U0*U0 - 3*U1*U1 + 2*U2*U2 - 6*U3*U3) % p; Q1 = 2*(U0*U2 - 3*U1*U3) % p
    if P1 == 0 or Q1 == 0:
        return _base(A, B, p, 'not_in_depth_three_family', reason='relative-norm extraction denominator vanishes (cannot happen for a family member at an eligible prime)')
    e = -P0*pow(P1, -1, p) % p
    g = -Q0*pow(Q1, -1, p) % p
    if e*e % p != 3 or g*g % p != 2:
        return _base(A, B, p, 'not_in_depth_three_family', reason='extracted parameters are not square roots of 3 and 2', extracted={'e': e, 'g': g})
    alpha = ev(ALPHA, e, g, p); gamma = ev(GAMMA, e, g, p)
    if alpha == 0 or gamma == 0:
        raise ProofViolation('excluded coefficient degeneration inside the eligible prime class')
    r = alpha*B*pow(gamma*A, -1, p) % p
    if r == 0 or A != alpha*r*r % p or B != gamma*r**3 % p:
        return _base(A, B, p, 'not_in_depth_three_family', reason='j may match a conjugate but both coefficient equations fail', extracted={'e': e, 'g': g, 'r': r})
    return _base(A, B, p, 'recognized', matches=[_certificate(A, B, p, e, g, r)])


def recognize_short_through_depth_three(A, B, p):
    """Combine the retained depth<=2 recognizer with the depth-three family.
    At eligible primes the classes are proved disjoint, so at most one depth
    can match; the assertion guards that proof with a runtime check."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'depth_two_recognition_20261006/core'))
    from recognize import recognize_short  # noqa: E402
    low = recognize_short(A, B, p)
    high = recognize_depth_three(A, B, p)
    matches = list(low['matches']) + list(high.get('matches', []))
    if low['status'] == 'recognized' and high['status'] == 'recognized':
        raise AssertionError('depth<=2 and depth-three certificates both accepted; contradicts collision exclusion')
    return {'status': 'recognized' if matches else 'not_in_implemented_families', 'p': p, 'short_model': [A % p, B % p],
            'matches': matches, 'depth_two_status': low['status'], 'depth_three_status': high['status'],
            'scope': 'retained depth<=2 closure plus the depth-three A=0-seed family only; the depth-three B=0-seed chain is not covered'}


def verify_supplied_certificate(p, A, B, certificate):
    """Reverify a stored certificate from its parameters; stored output is
    untrusted. Every field present in the stored record must equal the
    recomputed value (deep comparison), so an altered reverse path, model
    list, seed, depth or multiplier is rejected rather than silently repaired."""
    validate_prime(p); A, B = check_short(*_int_pair(A, B), p)
    if certificate.get('family') != FAMILY:
        raise ValueError('certificate family mismatch')
    params = certificate.get('parameters', {})
    if not isinstance(params, dict) or set(params)-{'e', 'g', 'r', 'e_squared', 'g_squared'}:
        raise ValueError('stored parameters carry an unknown field')
    if any(k not in params or not isinstance(params[k], int) or isinstance(params[k], bool) for k in ('e', 'g', 'r')):
        raise ValueError('stored parameters e, g, r must be integers')
    cert = _certificate(A, B, p, params['e'], params['g'], params['r'])
    for key, stored in certificate.items():
        if key not in cert:
            raise ValueError('stored certificate carries unknown field %s' % key)
        if key == 'parameters':
            if any(stored.get(k) is not None and stored[k] % p != cert[key][k] for k in ('e', 'g', 'r')) or \
               any(stored.get(k, cert[key][k]) != cert[key][k] for k in ('e_squared', 'g_squared')):
                raise ValueError('stored parameters disagree with recomputed certificate')
        elif stored != cert[key]:
            raise ValueError('stored %s disagrees with recomputed certificate' % key)
    return cert


# ---------------------------------------------------------------------------
# Trace of an accepted curve: CM candidates and a Las Vegas sign test.
# An accepted curve is 2^3-isogenous over F_p to its j=0 seed, so its exact
# trace t equals the seed's (H'=H and the Hasse bound). The seed's Frobenius
# lies in Z[omega], so 4p = t^2 + 3 s^2, and the verified non-backtracking
# length-three descent below the single-vertex surface j=0 of the 2-volcano
# forces 8 | s (Kohel's structure theorem as stated in Sutherland, Isogeny
# volcanoes, Theorem 7(iv) with Remark 8). Hence 4p = t^2 + 192 f^2, whose
# positive solution (t0, f) is unique (two rotations with 8 | s would force
# p even), and t = +-t0. Only the sign is left; it is decided by a random
# point. See the proof note for the argument and its cited dependencies.
# ---------------------------------------------------------------------------

def cm_trace_candidates(p, rng=None):
    """Return (t0, f, info) with 4p = t0^2 + 192 f^2, t0 > 0, f > 0, by Cornacchia.
    Needs sqrt(-3) mod p, obtained from a cubic nonresidue c: z = c^((p-1)/3)
    is a primitive cube root of unity and (2z+1)^2 = -3. The nonresidue search
    is randomized; its trial count is reported. Requires p = 1 mod 24."""
    validate_prime(p)
    if p % 24 != 1:
        raise ValueError('CM trace candidates are derived only for p = 1 mod 24')
    if rng is None:
        rng = random.SystemRandom()
    trials = 0
    while True:
        trials += 1
        c = rng.randrange(2, p)
        z = pow(c, (p-1)//3, p)
        if z != 1:
            break
    root = 4*(2*z+1) % p                       # sqrt(-48) mod p
    if root*root % p != (-48) % p:
        raise ProofViolation('square root of -48 failed')
    if root <= p//2:
        root = p-root
    a, b = p, root
    bound = isqrt(p)
    while b > bound:
        a, b = b, a % b
    x = b
    rem = p-x*x
    if rem <= 0 or rem % 48:
        raise ArithmeticError('Cornacchia found no representation p = x^2 + 48 y^2')
    y = isqrt(rem//48)
    if y*y*48 != rem or y == 0:
        raise ArithmeticError('Cornacchia found no representation p = x^2 + 48 y^2')
    t0, f = 2*x, y
    assert t0*t0+192*f*f == 4*p
    return t0, f, {'x': x, 'y': y, 'cubic_nonresidue_trials': trials, 'method': 'Cornacchia on p = x^2 + 48 y^2'}


def _ec_add(P, Q, A, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2:
        if (y1+y2) % p == 0:
            return None
        lam = (3*x1*x1+A)*pow(2*y1, -1, p) % p
    else:
        lam = (y2-y1)*pow(x2-x1, -1, p) % p
    x3 = (lam*lam-x1-x2) % p
    return x3, (lam*(x1-x3)-y1) % p


def _ec_mul(n, P, A, p):
    R = None
    while n:
        if n & 1:
            R = _ec_add(R, P, A, p)
        P = _ec_add(P, P, A, p)
        n >>= 1
    return R


def _sqrt_mod(n, p, rng):
    """Tonelli-Shanks with a random nonresidue; returns None for a nonsquare."""
    n %= p
    if n == 0:
        return 0
    if pow(n, (p-1)//2, p) != 1:
        return None
    q, s = p-1, 0
    while q % 2 == 0:
        q //= 2; s += 1
    z = rng.randrange(2, p)
    while pow(z, (p-1)//2, p) != p-1:
        z = rng.randrange(2, p)
    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q+1)//2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1:
            tt = tt*tt % p; i += 1
        b = pow(c, 1 << (m-i-1), p)
        m, c, t, r = i, b*b % p, t*b*b % p, r*b % p
    return r


def decide_trace_sign(A, B, p, t0, rng=None, max_trials=64):
    """Zero-error sign decision for a RECOGNIZED depth-three family member.

    With independent uniform x draws, each raw trial succeeds with probability
    at least 1/5 (see the consolidated sign-bound proof and p=97 certificates).
    The unbounded variant max_trials=None has expected <=5 raw trials and
    terminates almost surely. A positive cap returns an honest inconclusive
    status with probability <=(4/5)^cap; it never guesses the sign. The bound
    does not apply to arbitrary curves or even every j=0 easy seed.
    """
    validate_prime(p)
    A, B = check_short(*_int_pair(A, B), p)
    if recognize_depth_three(A, B, p)['status'] != 'recognized':
        raise ValueError('trace-sign success bound applies only to the recognized depth-three family')
    if not isinstance(t0, int) or isinstance(t0, bool) or t0 <= 0 or not _cm_necessary_check(p, t0):
        raise ValueError('require positive CM trace candidate with 4p-t0^2=192f^2')
    if max_trials is not None and (not isinstance(max_trials, int) or isinstance(max_trials, bool) or max_trials <= 0):
        raise ValueError('max_trials must be a positive integer or None')
    if rng is None:
        rng = random.SystemRandom()
    A %= p; B %= p
    n_plus, n_minus = p+1-t0, p+1+t0
    bound = {'uniform_raw_trial_success_lower_bound': '1/5',
             'expected_raw_trials_upper_bound': 5,
             'randomness_assumption': 'independent uniform randrange(p) draws',
             'max_trials': max_trials,
             'scope': FAMILY}
    for trial in count(1) if max_trials is None else range(1, max_trials+1):
        x = rng.randrange(p)
        y = _sqrt_mod(x**3+A*x+B, p, rng)
        if not y:
            continue
        P = (x, y)
        k_plus = _ec_mul(n_plus, P, A, p) is None
        k_minus = _ec_mul(n_minus, P, A, p) is None
        if k_plus and not k_minus:
            return t0, {**bound, 'status': 'conclusive', 'trials': trial,
                        'witness': {'point': [x, y], 'candidate_orders': [n_plus, n_minus], 'annihilated': [True, False]}}
        if k_minus and not k_plus:
            return -t0, {**bound, 'status': 'conclusive', 'trials': trial,
                         'witness': {'point': [x, y], 'candidate_orders': [n_plus, n_minus], 'annihilated': [False, True]}}
        if not k_plus and not k_minus:
            raise ProofViolation('neither candidate order kills a rational point; CM trace premise contradicted')
    return None, {**bound, 'status': 'inconclusive_after_max_trials', 'trials': max_trials,
                  'inconclusive_probability_upper_bound': '(4/5)^%d' % max_trials}


def verify_trace_sign_witness(A, B, p, t0, witness):
    """Recheck a decisive point witness; no randomness and no point count.

    Soundness uses the recognized family's theorem that its exact trace is
    one of +/-t0. This is not a generic certificate of the curve's order.
    """
    validate_prime(p)
    A, B = check_short(*_int_pair(A, B), p)
    if recognize_depth_three(A, B, p)['status'] != 'recognized' or not isinstance(t0, int) or isinstance(t0, bool) or t0 <= 0 or not _cm_necessary_check(p, t0):
        raise ValueError('witness requires a recognized family and a positive CM trace candidate')
    if not isinstance(witness, dict):
        raise ValueError('trace witness must be a record')
    point = witness.get('point')
    if not isinstance(point, (list, tuple)) or len(point) != 2 or any(not isinstance(v, int) or isinstance(v, bool) for v in point):
        raise ValueError('witness point must contain two integer residues')
    x, y = (v % p for v in point)
    if y*y % p != (x**3+A*x+B) % p:
        raise ValueError('trace witness point is not on the supplied curve')
    orders = [p+1-t0, p+1+t0]
    killed = [_ec_mul(n, (x, y), A, p) is None for n in orders]
    if killed not in ([True, False], [False, True]):
        raise ValueError('trace witness is not conclusive')
    if witness.get('candidate_orders') != orders or witness.get('annihilated') != killed:
        raise ValueError('stored witness data disagree with scalar multiplication')
    return t0 if killed[0] else -t0


def _cm_necessary_check(p, trace):
    """Necessary condition for the trace of a family member: 4p - t^2 = 192 f^2, f >= 1."""
    rem = 4*p-trace*trace
    if rem <= 0 or rem % 192:
        return False
    f = isqrt(rem//192)
    return f >= 1 and 192*f*f == rem


@dataclass(frozen=True)
class RecognizedPreparation:
    evaluator: BranchEvaluator
    certificate: dict
    trusted_exact_trace: int
    trace_sign_verification: dict | None = None


@dataclass(frozen=True)
class CMPreparation:
    evaluator: BranchEvaluator
    certificate: dict
    exact_trace: int
    trace_preparation: dict


def prepare_from_trace(p, f, trusted_exact_trace, *, verify_sign=False, rng=None, max_trials=64):
    """K reconstruction for a normalized cubic whose short model is in the
    family, from a caller-supplied exact trace. The supplied trace must pass
    the Hasse interval and the family's necessary CM condition
    4p - t^2 = 192 f^2. With verify_sign=True (or 'sextic') its sign is checked
    deterministically by Ireland-Rosen Theorem 4 on the seed; with
    verify_sign='las_vegas' the consolidated zero-error point test is used
    (capped by max_trials, None for unbounded). Otherwise the sign is trusted.
    Complete theoretical cost is trace preparation plus constant field work."""
    validate_prime(p); f = check_cubic(f, p)
    t = trusted_exact_trace
    if not isinstance(t, int) or isinstance(t, bool) or t*t > 4*p:
        raise ValueError('trace fails necessary Hasse interval; not a certification test')
    if verify_sign not in (False, True, 'sextic', 'las_vegas'):
        raise ValueError("verify_sign must be False, True, 'sextic' or 'las_vegas'")
    A, B = short_model(f, p)
    rec = recognize_depth_three(A, B, p)
    if rec['status'] != 'recognized':
        return rec
    if not _cm_necessary_check(p, t):
        raise ValueError('supplied trace violates the family condition 4p - t^2 = 192 f^2 with f >= 1')
    cert = rec['matches'][0]
    method = 'direct_depth_three_caller_supplied_exact_trace'
    info = None
    if verify_sign == 'las_vegas':
        decided, info = decide_trace_sign(A, B, p, abs(t), rng, max_trials)
        if decided is None:
            raise ValueError('sign verification inconclusive after %s trials' % max_trials)
        if decided != t:
            raise ValueError('supplied trace has the wrong sign: a rational point is killed only by p+1-(%d)' % decided)
        method = 'direct_depth_three_exact_trace_sign_verified_las_vegas'
    elif verify_sign:
        _, _, cinfo = cm_trace_candidates(p, rng)
        pi = primary_prime_from_cornacchia(p, cinfo['x'], cinfo['y'])
        decided, info = seed_trace_sextic(p, -pow(cert['parameters']['r'], 3, p), pi)
        if decided != t:
            raise ValueError('supplied trace %d is wrong: the verified trace is %d' % (t, decided))
        info.update({'status': 'deterministic', 'source': 'Ireland & Rosen (1990), Ch. 18, Sec. 3, Theorem 4, applied to the seed (0,-r^3)'})
        method = 'direct_depth_three_exact_trace_sign_verified_sextic'
    H = t % p
    beta = cert['beta_multiplier']*H % p
    _, _, b, a = f
    K = (beta - b*pow(3, -1, p)*H)*pow(a, -1, p) % p
    return RecognizedPreparation(BranchEvaluator(p, f, H, K, method), cert, t, info)


# ---------------------------------------------------------------------------
# Deterministic trace sign by Ireland & Rosen, Ch. 18, Section 3, Theorem 4:
# for p = 1 mod 3, p not dividing D, and p = pi*conj(pi) with pi in Z[omega],
# pi = 2 mod 3 (primary),
#     N_p(y^2 = x^3 + D) = p + 1 + conj((4D/pi)_6) pi + (4D/pi)_6 conj(pi),
# so the trace is a_p = -2 Re( conj((4D/pi)_6) pi ). The sextic residue
# symbol is (a/pi)_6 = zeta with zeta = a^((p-1)/6) mod pi, a sixth root of
# unity; mod pi one has omega = -a0/b0 for pi = a0 + b0 omega.
# An accepted curve has the trace of its seed y^2 = x^3 - r^3 (D = -r^3).
# ---------------------------------------------------------------------------

def _eis_mul(u, v):
    """(a + b w)(c + d w) in Z[w], w^2 = -1 - w."""
    a, b = u; c, d = v
    return (a*c - b*d, a*d + b*c - b*d)


def primary_prime_from_cornacchia(p, x, y):
    """From p = x^2 + 48 y^2 return primary pi = a + b w (a = 2, b = 0 mod 3)
    with norm a^2 - a b + b^2 = p. Uses sqrt(-3) = 1 + 2w, so
    x + 4y sqrt(-3) = (x + 4y) + 8y w, then fixes the unit among the six."""
    base = (x + 4*y, 8*y)
    unit = (1, 0)
    for _ in range(6):
        a, b = _eis_mul(base, unit)
        if a % 3 == 2 and b % 3 == 0:
            if a*a - a*b + b*b != p:
                raise ProofViolation('primary prime has wrong norm')
            return a, b
        unit = _eis_mul(unit, (1, 1))          # 1 + w = -w^2, a primitive sixth root
    raise ProofViolation('no primary associate found')


def seed_trace_sextic(p, D, pi):
    """Exact trace of y^2 = x^3 + D over F_p by Ireland-Rosen Theorem 4.
    Deterministic O(log p) field operations given the primary prime pi."""
    if p % 3 != 1 or D % p == 0:
        raise ValueError('Theorem 4 case requires p = 1 mod 3 and p not dividing D')
    a, b = pi
    if b % p == 0:
        raise ProofViolation('primary prime has b = 0 mod p')
    w = (-a*pow(b, -1, p)) % p              # image of omega modulo pi
    if (w*w + w + 1) % p:
        raise ProofViolation('omega image is not a cube root of unity')
    s = pow(4*D % p, (p-1)//6, p)
    zeta_mod = (1 + w) % p                  # image of 1 + w, primitive sixth root
    zeta = (1, 0); val = 1
    for k in range(6):
        if val == s:
            break
        zeta = _eis_mul(zeta, (1, 1)); val = val*zeta_mod % p
    else:
        raise ProofViolation('sextic residue symbol not a sixth root of unity')
    cz = (zeta[0] - zeta[1], -zeta[1])      # complex conjugate of c + d w is (c - d) - d w
    u0, u1 = _eis_mul(cz, (a, b))
    return -(2*u0 - u1), {'primary_pi': [a, b], 'sextic_symbol_power_of_1_plus_w': k}


def prepare_cm(p, f, *, rng=None, max_trials=64, sign_method='sextic'):
    """Complete preparation without any supplied trace: recognition, CM trace
    candidates by Cornacchia, the trace sign, then H, beta and K.
    sign_method='sextic' (default, 10 October 2026) fixes the sign
    deterministically by Ireland & Rosen Ch. 18 Theorem 4 applied to the seed
    (0,-r^3); the only randomized step left is the cubic-nonresidue search
    inside cm_trace_candidates that supplies sqrt(-3).
    sign_method='las_vegas' uses the consolidated zero-error point test: raw
    success probability >=1/5 per uniform draw, capped at max_trials (default
    64, may return trace_sign_inconclusive) or unbounded with max_trials=None.
    No deterministic Schoof fallback is invoked by this prototype."""
    validate_prime(p); f = check_cubic(f, p)
    if sign_method not in ('sextic', 'las_vegas'):
        raise ValueError('sign_method must be sextic or las_vegas')
    if rng is None:
        rng = random.SystemRandom()
    A, B = short_model(f, p)
    rec = recognize_depth_three(A, B, p)
    if rec['status'] != 'recognized':
        return rec
    cert = rec['matches'][0]
    t0, fcount, info = cm_trace_candidates(p, rng)
    if sign_method == 'sextic':
        pi = primary_prime_from_cornacchia(p, info['x'], info['y'])
        t, sign_info = seed_trace_sextic(p, -pow(cert['parameters']['r'], 3, p), pi)
        if abs(t) != t0:
            raise ProofViolation('sextic seed trace disagrees with the CM candidates')
        sign_info.update({'status': 'deterministic', 'source': 'Ireland & Rosen (1990), Ch. 18, Sec. 3, Theorem 4, applied to the seed (0,-r^3)'})
        method = 'direct_depth_three_cm_cornacchia_sextic_sign'
        sign_cost = 'deterministic: one exponentiation (4D)^((p-1)/6), O(log p) field operations'
    else:
        t, sign_info = decide_trace_sign(A, B, p, t0, rng, max_trials)
        if t is None:
            return {'status': 'trace_sign_inconclusive', 'p': p, 'candidates': [t0, -t0], 'cornacchia': info, 'sign_test': sign_info,
                    'certificate': cert}
        method = 'direct_depth_three_cm_cornacchia_las_vegas_sign'
        sign_cost = 'zero-error Las Vegas: <=5 expected raw trials, O(log p) field operations each'
    H = t % p
    beta = cert['beta_multiplier']*H % p
    _, _, b, a = f
    K = (beta - b*pow(3, -1, p)*H)*pow(a, -1, p) % p
    prep = {'trace_candidates': [t0, -t0], 'representation_4p': [t0, fcount], 'cornacchia': info, 'sign_test': sign_info,
            'sign_method': sign_method,
            'cost': 'after validated prime: recognition O(1); randomized cubic-nonresidue search for sqrt(-3); Cornacchia polynomial bit work; sign ' + sign_cost}
    return CMPreparation(BranchEvaluator(p, f, H, K, method), cert, t, prep)


def family_member(p, e, g, r):
    """Construct the family model for supplied parameters (checked)."""
    validate_prime(p)
    e %= p; g %= p; r %= p
    if p % 24 != 1 or e*e % p != 3 or g*g % p != 2 or r == 0:
        raise ValueError('need p=1 mod 24, e^2=3, g^2=2, r nonzero')
    return ev(ALPHA, e, g, p)*r*r % p, ev(GAMMA, e, g, p)*r**3 % p
