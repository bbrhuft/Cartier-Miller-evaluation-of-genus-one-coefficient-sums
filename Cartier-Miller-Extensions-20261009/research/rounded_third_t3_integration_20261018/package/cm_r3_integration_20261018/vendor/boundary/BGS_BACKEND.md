# Arithmetic-progression factorial/product backend

Version 0.5 adds `backend="bgs"` to boundary requests, third-point sessions,
fifth-point sessions and `IntervalProductEvaluator.product`. It implements the
scalar value-shift and recursive block construction of Bostan, Gaudry and
Schost, *Linear recurrences with polynomial coefficients and application to
integer factorization and Cartier–Manin operator*, Sections 3–4, Theorems 5
and 8. Primary text: https://cs.uwaterloo.ca/~eschost/publications/pollard.pdf
(dated 12 September 2006). This is a new implementation of published ideas,
with the collision handling described below; it is not a new factorial theorem.

## Interface and dispatch

```console
python integrated_thirds.py --p 1000037 --backend bgs
python integrated_thirds.py --p 100003 --boundary-policy factorial --backend bgs
python integrated_fifths.py --p 10000019 --backend bgs
python boundary_framework.py --p 101 --index 17 --family generic --backend bgs
python benchmark_bgs.py --repeats 3
```

```python
from boundary_framework import BGSFactorialBackend
from integrated_fifths import IntervalProductEvaluator

# These low-level APIs require an already validated prime.
factorial = BGSFactorialBackend().factorial(1000, 10007)
interval = IntervalProductEvaluator().product(10007, 7000, 1000, backend="bgs")
```

High-level boundary/session entry points retain deterministic prime validation
for p < 2**64. The backend supports modulo p only. Factorials require
0 <= n < p and use Wilson reflection before doing work. Interval factors lie
in 1..p-1: start >= 1, length >= 0, start+length <= p. An empty interval is 1.

Automatic dispatch now uses direct multiplication through the existing
262,144-term cutoff and BGS above it, for both factorials and intervals.
The cutoff remains configurable and conservative; it is not fitted as a
universal crossover. Explicit `direct`, `product_tree` and `bgs` overrides
remain available. Ordinary thirds still reuse the native trace unless
`boundary_policy="factorial"` is requested. U-only acquisition skipping is
unchanged. A generic ratio may choose different backends for its factorials.

The shared `max_degree` guard applies to BGS with degree floor(sqrt(length)),
after reflection for factorials. It is checked before allocating block arrays.
Default degree limit is 8192. Direct and tree resource guards retain their
meaning. No fallback silently bypasses a resource error.

## Shift identity and denominator audit

Let deg(P) <= d < p, with samples y_j=P(j) for j=0..d. Define

\[
w_j=\frac{(-1)^{d-j}y_j}{j!(d-j)!},\qquad
\Delta(t)=\prod_{j=0}^{d}(t-j).
\]

Lagrange interpolation gives, whenever t is not a sample node,

\[
P(t)=\Delta(t)\sum_{j=0}^{d}\frac{w_j}{t-j}.
\]

For t=alpha+i, form the kernel
K_r=(alpha-d+r)^(-1), 0<=r<=2d. The required sum is coefficient d+i of
the convolution of (w_j) with K. This indexing is part of the independent
Horner tests. The existing exact integer-packing polynomial multiplier
computes this convolution; polynomial coefficients of P and remainder trees
are never constructed by the BGS path.

The published general-ring shift theorem requires **all** alpha-d through
alpha+d, as well as the grid step and 2..d, to be units. The bound 2d+1<p
alone is not enough. Our field implementation checks the actual residues:
nonzero kernel entries are inverted by prefix/backward batch inversion;
zero entries are placeholders only. If t is a known node modulo p, its
sample is copied instead of applying the rational expression. At all other
targets every t-j is nonzero, so the expression is valid. Thus overlapping
and wrapped grids are handled without dividing by zero. Factorial weights
are valid because d<p. This explicit field-only extension does not claim a
shift algorithm over rings with zero divisors.

Delta products use a rolling nonzero product plus a zero count. This permits
the product to recover after a zero leaves the window; a naive recurrence
that divides a zero Delta would fail. The shift plan can be reused on a
second value array within one recursion level. There is no persistent cache.

## Block construction and correctness

For a unit interval of length N, set s=floor(sqrt(N)) and
F_k(X)=prod_(0<=j<k)(X+start+j). A recursive construction computes
F_k(i*s) for i=0..k. Its base is F_1(X)=X+start.

At k=2d, use the identity F_(2d)(X)=F_d(X)F_d(X+d).
Given d+1 samples of F_d on the grid with step s:

1. Shift by d+1 in normalized grid coordinates to extend the samples
   through index 2d+1.
2. Shift the original samples by d/s to obtain F_d(i*s+d).
3. Extend these shifted samples by d+1, reusing the first shift plan.
4. Multiply corresponding values through index k.

For odd k=2d+1, multiply each result by X+start+2d as well. Since
1<=s<p, normalization by s is valid. Internal block samples may be zero;
the construction never inverts them. They need not correspond to unit
intervals, even though the final requested product does.

Finally multiply F_s(i*s) for i=0..s-1, covering the first s*s factors,
and multiply the remaining N-s*s < 2s+1 factors directly. This proves the
interval result by induction. For factorials set start=1, then restore the
Wilson-reflected result with the existing sign (-1)^(n+1).

Each level performs three convolutions and linear work at a geometrically
increasing degree. Under the usual multiplication regularity assumptions,
this gives O(M(s)) arithmetic work plus O(log(s)) field inversions, with
O(s) live field elements. The actual bit cost depends on Python big-integer
multiplication and packing. Packing also uses O(s*(log(p)+log(s))) bits;
Python object overhead is additional. No FLINT-level performance or general
matrix/selected-term BGS implementation is claimed. Tal refinements,
prime-power arithmetic and many-prime remainder forests are separate work.

## Validation and measurement

`test_bgs_backend.py` checks every degree and every shift at odd primes
through 19, including collisions, wrapped grids and zero polynomials.
It also checks convolution-sized examples and a prime near 2**64 with
independent Horner evaluation. Block values are checked against literal
products for both even and odd degrees. Every unit interval at odd primes
through 43 is checked, as is every factorial index and generic boundary
index at odd primes through 257. Larger shifted intervals near p and square
length transitions are checked by direct multiplication. Complete forced
factorial thirds and fifth pairs are checked against the original sum
recurrence. Existing third/fifth binomial-reduction tests now include BGS.

`benchmark_bgs.py` compares all three kernels with the same input and cold
construction, then measures complete third outputs and fifth pairs against
the original scaled t recurrence. The complete third benchmark deliberately
forces factorial acquisition in all modes; ordinary default trace reuse is
still faster than acquiring an unnecessary factorial. Each timed result
is checked. See RESULTS.md and the machine-readable CSV/JSON for actual
measurements, platform, exclusions and the conservative dispatch policy.


Version 0.6 retains this backend unchanged apart from the package version. Historical BGS timings are preserved under evidence/history/v0_5/. The current RESULTS.md covers the new shared-batch measurements and current full validation. Running benchmark_bgs.py regenerates BGS kernel measurements for the current version.
