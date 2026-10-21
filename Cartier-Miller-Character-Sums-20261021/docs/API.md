# Portable API and conventions

Import weighted_sums from src/. The module exposes single_pole, prepare_weights, PreparedWeights and WeightedSums. It uses the unchanged uniform_order.py engine. All field-valued outputs are Python integers from zero through p minus one.

## Supplied input

p is a supplied odd prime at least 5. The wrapper checks its integer type, parity and lower bound but does not certify primality. trace is the exact signed integer p+1 minus the number of points on the smooth projective model of y squared equals f(x). The Hasse interval is checked, but that check and the Miller endpoint are not a trace certificate. An arbitrary residue of the trace is insufficient.

coefficients gives f in increasing degree. Trailing zeros are reduced away modulo p; the resulting degree must be three or four and f must be squarefree. The original constant term may vanish. Scalars and coordinates must be integers; coordinates and coefficient values are reduced modulo p. A denominator factorization or partial-fraction decomposition is not performed.

## Single pole

single_pole(p, coefficients, pole, trace) returns C_f(pole). The pole must be nonbranch: f(pole) must be nonzero. At f(pole)=0, ValueError reports that the request is outside the current query contract. The current engine includes p=5 and does not use its predecessor's small-field enumeration fallback.

## Repeated weights on a complete domain

prepare_weights(p, coefficients, trace, excluded) constructs an immutable PreparedWeights state. The coordinates in excluded must be distinct modulo p. They enumerate the entire excluded set, rather than only the poles whose residues happen to be nonzero. All single-pole values and both correction vectors are prepared and cached. The weight is represented directly as c+sum_i residues[i]/(x-excluded[i]).

state.evaluate(residues, constant=0) requires exactly one residue for every excluded coordinate. A zero residue keeps its coordinate excluded from the domain of every other summand. A branch coordinate may be excluded, but its residue must remain zero. There is no fallback when an active branch residue is requested.

The returned WeightedSums record has character, affine_points and projective_points attributes. Character uses chi(f(x)) with chi(0)=0. Affine points are all rational affine points whose x coordinate is outside the excluded set. Projective points additionally retain all rational points at infinity, where this weight has value constant. A cubic has one rational infinity point. A quartic has zero or two, determined by the leading coefficient's quadratic character.

For an empty excluded set, evaluate([], constant=c) is a constant-weight query. If every field coordinate is excluded, the affine and character outputs are zero; the projective output is c times the rational infinity count. The public state constructor is prepare_weights; direct dataclass construction does not validate hypotheses.

## Memory and arithmetic

Preparation runs one scalar query at each nonbranch exclusion and constructs pairwise corrections with one batch inversion. It uses O(s log p+s^2) field operations, O(s^2) temporary field storage for the pair list and prefixes, and O(s) persistent field data. Coefficient-only queries use O(s) arithmetic and input-reading time. The current code implements the pairwise correction, not the asymptotically faster polynomial-tree construction proved in the paper.

## Current versus historical interfaces

The previous cmcs.Curve API and its bounded double-pole, polynomial and second-kind experiments are preserved under historical_benchmark/inherited/character_sums/. They are the historical benchmark implementation and are not silently substituted for this API. cm_character_route.value in src/ is also a preceding algorithm retained for comparison; current single-pole calls use uniform_order.value.
