"""Rationally weighted quadratic-character and elliptic-point sums (added 21 October 2026).

Service wrapper over backends/character_sums, the adapted copies of the
21 October 2026 supplement (Cartier-Miller-Character-Sums-20261021). The
arithmetic and its contract are those of weighted_sums.single_pole and
prepare_weights. This wrapper adds only cm_system's input conventions:
deterministic primality for 5 <= p < 2^64, rejection of Python booleans, an
explicit trust label for supplied traces, and an optional bounded direct point
count whose cost is reported. Outputs are residues modulo p.

Not covered: active branch poles, higher-order poles, polynomial parts,
nonrational or unfactored denominators, integer or interval character sums,
and nonlinear chi(R f) sums. None of these inherit the logarithmic bound.
"""
from .api import prime, integer, Budget, ResourceLimit, Unsupported
from .backends.character_sums import cm_character_route as arithmetic
from .backends.character_sums import weighted_sums as W

TARGET_SINGLE = 'single_pole_character_sum'
TARGET_WEIGHTED = 'weighted_character_and_point_sums'
SUPPLIED = ('caller-trusted exact signed projective trace; the Hasse interval and the '
            'Miller endpoint are necessary checks, not certificates')
COUNTED = ('direct point count: p quadratic-character evaluations, O(p log p) field '
           'operations, O(1) storage; not a logarithmic preparation')


def _coefficients(p, coefficients):
    coefficients = list(coefficients)
    for c in coefficients:
        integer(c, 'coefficient')
    f = arithmetic._trim([c % p for c in coefficients])
    if len(f) not in (4, 5) or not arithmetic.squarefree(f, p):
        raise ValueError('requires a squarefree cubic or quartic, coefficients low to high')
    return tuple(f)


def count_trace(p, f):
    """Exact signed projective trace of y^2=f(x) by enumeration (bounded by callers)."""
    f = list(f)
    s = sum(arithmetic.character(arithmetic.peval(f, x, p), p) for x in range(p))
    n_inf = 1 if len(f) == 4 else 1 + arithmetic.character(f[-1], p)
    return 1 - n_inf - s


class CharacterSumSession:
    """One curve y^2=f(x) over F_p and its exact trace, reused by every query.

    trace=None acquires the trace by a direct count when p <= budget.point_count_prime
    and otherwise raises ResourceLimit. A supplied trace is labelled trusted.
    """

    def __init__(self, p, coefficients, trace=None, budget=None):
        prime(p)
        self.p = p
        self.budget = budget or Budget()
        self.f = _coefficients(p, coefficients)
        if trace is None:
            if p > self.budget.point_count_prime:
                raise ResourceLimit('trace acquisition by direct count exceeds the point-count '
                                    'budget; supply an exact trace (for example from SEA or Schoof)')
            trace = count_trace(p, self.f)
            self.trace_source, self.trusted = COUNTED, False
        else:
            integer(trace, 'trace')
            self.trace_source, self.trusted = SUPPLIED, True
        W._curve(p, self.f, trace)  # the adapter's own Hasse, degree and squarefree checks
        self.trace = trace

    def _base(self, target):
        return {'p': self.p, 'coefficients': list(self.f), 'trace': self.trace,
                'trace_source': self.trace_source,
                'status': 'conditional_on_trusted_trace' if self.trusted else 'exact',
                'target': target, 'modulus': self.p,
                'input_certification': 'deterministic 64-bit primality test',
                'character_convention': 'chi(0)=0; no character value at infinity'}

    def _branch(self, a):
        return arithmetic.character(arithmetic.peval(list(self.f), a, self.p), self.p) == 0

    def single_pole(self, pole):
        """C_f(a)=sum_{x != a} chi(f(x))/(x-a) for a nonbranch pole a."""
        integer(pole, 'pole')
        a = pole % self.p
        if self._branch(a):
            raise Unsupported('active branch pole f(a)=0 is outside the fast contract')
        value = W.single_pole(self.p, self.f, a, self.trace)
        return {**self._base(TARGET_SINGLE), 'pole': a, 'value': value,
                'method': 'one differentiated Miller chain at N=p+1-chi(f(a))*trace',
                'query_cost': 'O(log p) field operations after trace acquisition'}

    def prepare(self, excluded=()):
        """Prepare the complete excluded set U once; see PreparedCharacterSums.evaluate."""
        excluded = list(excluded)
        for a in excluded:
            integer(a, 'excluded coordinate')
        return PreparedCharacterSums(self, W.prepare_weights(self.p, self.f, self.trace, excluded))


class PreparedCharacterSums:
    """Cached single-pole values and correction vectors for one excluded set."""

    def __init__(self, session, state):
        self.session = session
        self.state = state

    @property
    def excluded(self):
        return list(self.state.excluded)

    def evaluate(self, residues, constant=0):
        """Sums of R(x)=constant+sum_i residues[i]/(x-excluded[i]) over x outside U.

        A zero residue keeps its coordinate excluded. A branch coordinate may be
        excluded only with zero residue. Projective output adds constant times the
        number of rational points at infinity.
        """
        residues = list(residues)
        for r in residues:
            integer(r, 'residue')
        integer(constant, 'constant')
        p = self.session.p
        if len(residues) == len(self.state.excluded):
            for a, r, cb in zip(self.state.excluded, residues, self.state.character_basis):
                if r % p and cb is None:
                    raise Unsupported('active branch pole outside the fast contract: ' + str(a))
        z = self.state.evaluate(residues, constant)
        s = len(self.state.excluded)
        return {**self.session._base(TARGET_WEIGHTED), 'excluded': self.excluded,
                'residues': [r % p for r in residues], 'constant': constant % p,
                'character': z.character, 'affine_points': z.affine_points,
                'projective_points': z.projective_points,
                'rational_points_at_infinity': self.state.infinity_count,
                'preparation_cost': 'O(s log p+s^2) field operations, O(s^2) temporary and O(s) '
                                    'cached field storage, s=%d; pairwise batch inversion, '
                                    'not the proved polynomial-tree correction' % s,
                'query_cost': 'O(s) field operations for a new coefficient vector'}
