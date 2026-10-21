"""Adapters for supplied constant-plus-simple-pole weights over a prime field.

Uses the unchanged uniform_order evaluator. This adapter was added while
packaging the completed research; it has correctness tests, not timings.
Prime p>=5 and the exact signed projective trace are caller obligations.
Coefficients have increasing degree. Outputs are residues in [0,p).
"""
from dataclasses import dataclass
from math import isqrt
from operator import index

from . import cm_character_route as arithmetic
from . import uniform_order


def _integer(value, name):
    try:
        return index(value)
    except TypeError as exc:
        raise TypeError(name + ' must be an integer') from exc


def _curve(p, coefficients, trace):
    p = _integer(p, 'p')
    trace = _integer(trace, 'trace')
    if p < 5 or p % 2 == 0:
        raise ValueError('requires a supplied odd prime p>=5')
    if abs(trace) > isqrt(4*p):
        raise ValueError('exact signed trace must lie in the Hasse interval')
    f = arithmetic._trim([_integer(c, 'coefficient') % p for c in coefficients])
    if len(f) not in (4, 5) or not arithmetic.squarefree(f, p):
        raise ValueError('requires a squarefree cubic or quartic')
    return p, tuple(f), trace


def single_pole(p, coefficients, pole, trace):
    """Return sum_{x!=a} chi(f(x))/(x-a) for a nonbranch pole a.

    A branch pole raises ValueError. No enumeration, trace acquisition,
    denominator factorization, or primality certification is performed.
    """
    p, f, trace = _curve(p, coefficients, trace)
    a = _integer(pole, 'pole') % p
    return uniform_order.value(p, f, a, trace)


@dataclass(frozen=True)
class WeightedSums:
    character: int
    affine_points: int
    projective_points: int


@dataclass(frozen=True)
class PreparedWeights:
    """Cached complete excluded domain and single-pole correction vectors.

    Construct through prepare_weights. A branch exclusion is retained but
    must have zero residue at every evaluation. Projective output retains
    all rational infinity points, where this weight has value constant.
    """
    p: int
    coefficients: tuple
    trace: int
    excluded: tuple
    characters: tuple
    character_basis: tuple
    affine_basis: tuple
    constant_character: int
    constant_affine: int
    infinity_count: int

    def evaluate(self, residues, constant=0):
        """Evaluate R=c+sum_i residues[i]/(x-excluded[i]), x outside U.

        A zero residue still excludes its point from every term. Changing
        coefficients on the same prepared set costs O(s) field operations.
        """
        p = self.p
        r = tuple(_integer(v, 'residue') % p for v in residues)
        if len(r) != len(self.excluded):
            raise ValueError('one residue per excluded point is required')
        c = _integer(constant, 'constant') % p
        ch = c*self.constant_character
        aff = c*self.constant_affine
        for a, weight, cb, pb in zip(self.excluded, r, self.character_basis,
                                      self.affine_basis):
            if weight == 0:
                continue
            if cb is None:
                raise ValueError('active branch pole outside the fast contract: '+str(a))
            ch += weight*cb
            aff += weight*pb
        return WeightedSums(ch % p, aff % p, (aff+c*self.infinity_count) % p)


def prepare_weights(p, coefficients, trace, excluded=()):
    """Prepare a complete excluded set in O(s log p+s^2) field operations.

    The trace is supplied. Pairwise corrections use batched inversion of
    distinct differences; the faster polynomial-tree construction is only
    proved in this supplement, not implemented here.
    """
    p, f, trace = _curve(p, coefficients, trace)
    poles = tuple(_integer(a, 'excluded coordinate') % p for a in excluded)
    if len(set(poles)) != len(poles):
        raise ValueError('excluded points must be distinct modulo p')
    w = tuple(arithmetic.character(arithmetic.peval(f, a, p), p) for a in poles)
    n_inf = 1 if len(f) == 4 else 1+arithmetic.character(f[-1], p)
    k = 1-n_inf-trace
    # One batch inversion for all unordered pairwise differences.
    pairs = [(i, j, (poles[i]-poles[j]) % p)
             for i in range(len(poles)) for j in range(i)]
    prefixes = [1]
    for _, _, delta in pairs:
        prefixes.append(prefixes[-1]*delta % p)
    inv = pow(prefixes[-1], -1, p) if pairs else 1
    dw, dp = [0]*len(poles), [0]*len(poles)
    for pos in range(len(pairs)-1, -1, -1):
        i, j, delta = pairs[pos]
        reciprocal = inv*prefixes[pos] % p
        inv = inv*delta % p
        dw[i] = (dw[i]+w[j]*reciprocal) % p
        dw[j] = (dw[j]-w[i]*reciprocal) % p
        dp[i] = (dp[i]+(1+w[j])*reciprocal) % p
        dp[j] = (dp[j]-(1+w[i])*reciprocal) % p
    cb, pb = [], []
    for i, a in enumerate(poles):
        if w[i] == 0:
            cb.append(None); pb.append(None)
        else:
            value = uniform_order.value(p, f, a, trace)
            cb.append((value+dw[i]) % p)
            pb.append((value+dp[i]) % p)
    return PreparedWeights(p, f, trace, poles, w, tuple(cb), tuple(pb),
                           (k-sum(w)) % p, (k-len(poles)-sum(w)) % p, n_inf)
