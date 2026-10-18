# Shared boundary batches at one prime

Version 0.6 adds `BoundaryBatchSession` in `shared_boundaries.py`. It computes
a_L=binom(2L,L)*8^(-L) modulo one odd prime p<2**64 at any collection of
indices 0<=L<p. This extends sharing beyond the fixed fifth-point pair.
The existing boundary, third and fifth services retain their interfaces.

## Ready-to-run interface

```console
python shared_boundaries.py --p 59 --indices 6 12 24 20 6 --backend bgs
python shared_boundaries.py --p 29 --indices 6 12 --reference-prefix
python shared_boundaries.py --p 17 --indices 6 --reference-prefix --output-mode u_only
python benchmark_shared.py --repeats 3
```

```python
from shared_boundaries import BoundaryBatchSession
from boundary_framework import DirectReferencePrefix

session = BoundaryBatchSession(59)
batch = session.evaluate([6, 12, 24, 20, 6], backend="bgs")
assert batch["values"] == [14, 5, 30, 6, 14]
assert batch["product_acquisitions"] == 4
assert batch["denominator_inversions"] == 1

complete = session.complete_many([6, 12, 24, 20], DirectReferencePrefix())
# Complete U values require a provider that supports each strict prefix.
```

The last provider is a sequential correctness reference, not a fast
arbitrary-index prefix routine. Any provider obeying the existing
`name`, `assurance`, `supports(p,L)`, `prefix(p,L)` contract can be supplied
to `complete_many`. Each distinct requested prefix is computed once per
call. Provider support and canonical residues are checked. A caller-supplied
provider retains its assurance label; batching does not certify its values.

The retained `ThirdPointPrefixProvider` works directly for its supported
third index. For fast ordinary-third evaluation, `ThirdPointSession` remains
preferable: it already gets the boundary from the trace. The new batch
service computes boundary ratios and does not automatically acquire or reuse
that trace. `FifthPointSession` remains the native complete fifth-pair entry
point. Batch boundary support does not expand the native prefix domains.

## Family and output semantics

| Option | Meaning |
|---|---|
| `family="auto"` | Recognize ordinary third, rounded third and fifth points; otherwise generic |
| `family="generic"` | Use the defining factorial ratio at all nontrivial lower-half indices |
| Explicit `ordinary_third`, `rounded_third`, `fifth` | Every supplied index must satisfy that family's hypotheses |
| `backend="auto"` | Select direct through the configured length cutoff, BGS above it |
| Explicit `direct`, `product_tree`, `bgs` | Apply the chosen backend to each actual product acquisition |
| `sharing="adjacent"` | Share prefix products through sorted factorial gap intervals; default |
| `sharing="exact"` | Share identical product requests; acquire distinct factorials independently |
| `modulus_power=1` | Required; all other values fail before acquisition |

`indices` may be an iterable. Output order and duplicates are preserved.
Duplicate boundaries share arithmetic. Empty requests perform no product
acquisition or normalization inversion. Prime and option checks remain active
for empty requests. Booleans and nonintegral indices are rejected. The prime
is validated at session construction; it is common to every request.

`evaluate` returns actual boundary values, with no U-only option.
`complete_many(..., output_mode="u_only")` instead suppresses B and a and
skips boundary plans whose multiplier 2L(2L+5) is zero. Skipped and computed
boundaries are distinguished. All options, indices, family hypotheses and
prefix support are still validated. Full mode returns actual a values even
when their multiplier is zero. The CLI requires `--reference-prefix` when
U-only output is requested; this makes its reference-prefix cost explicit.

## Ratio plans and Wilson reflection

The built-in reductions are exactly the defining central-binomial ratio,
ordinary third -(L!)^(-3), rounded third (3/2)*((L-1)!)^(-3), and the two
retained fifth interval ratios. MATHEMATICS.md and FIFTHS.md give their proofs.
Index zero is 1; upper-half indices are zero modulo p. Explicit family
hypotheses are checked before those shortcuts.

Each nontrivial plan is a scalar times a product of unit interval products
raised to integer exponents. A prefix interval (1,n) means n!; its factors
are 1 through n. Before acquisition, factorials above (p-1)/2 are replaced
using Wilson's identity

\[
n!=(-1)^{n+1}\big((p-1-n)!\big)^{-1}\pmod p.
\]

The sign moves into the scalar and the exponent changes sign. Equal product
tokens have their exponents combined, and zero exponents are dropped. Only
canonical factorial indices at most (p-1)/2 reach a backend. Thus the
factorial backend itself performs no reflected-result inversion in this
service. The constant modular powers used in a plan have nonnegative
exponents reduced modulo p-1; denominator normalization is described below.

## Sharing and correctness

All plans are prepared before any product acquisition. Factorial indices
are collected across the entire batch, including fifth denominators, which
are themselves prefix intervals. With adjacent sharing, sort them as
n_1<...<n_k. Acquire n_1! once and extend by

\[
n_j!=n_{j-1}!\prod_{t=n_{j-1}+1}^{n_j}t\pmod p.
\]

The first acquisition uses an existing factorial backend; subsequent gaps
use `IntervalProductEvaluator`. Both inherit the BGS/direct/tree choices.
The derived full prefix products and actual gap products are available to
the other plans in that call. Equal arbitrary intervals are also acquired
once. This proves each acquired or derived product by induction, independently
of which valid backend supplies a primitive product.

At p=59 the requests 6,12,24,20 combine a generic index, both fifth points
and the rounded third. They need 6!,12!,19!, the first fifth numerator
18..23 and the second fifth numerator 7..12. Adjacent sharing acquires 6!,
7..12,13..19 and 18..23. The product 7..12 extends 6! to 12! and also supplies
the second fifth numerator. The fifth denominator reuses 6!.

Exact sharing has five acquisitions for that batch. Adjacent sharing has
four. Four separate single-index batch calls have seven acquisitions.
The tests intercept the actual backend calls to check these claims, rather
than inferring sharing from output labels. There is no persistent answer
cache: a repeated batch reruns product and prefix arithmetic.

This is a deterministic sharing heuristic, not a global cost optimum.
Partially overlapping arbitrary intervals are not partitioned unless one is
an exact factorial gap already acquired. Backends can have different costs
at different lengths and bit widths. `sharing="exact"` provides an explicit
alternative for matched comparison. Within the square-root model, gaps are
no longer than the corresponding independent factorial, but Python overhead
and backend cutoffs can alter wall time.

## Shared denominator normalization

For each unique boundary, put positive product powers in N_i and negative
powers in D_i. All acquired products are units, so every D_i is nonzero.
Equal denominator residues can share an inverse. The standard prefix-product
and backward-product identity obtains all remaining D_i^(-1) from one
inversion of their total product, with linear additional multiplications.
The final value is N_i*D_i^(-1). If all denominators equal 1, no such
inversion is needed. The resulting a values then enter the retained identity
U=4B-2L(2L+5)a in `complete_many`.

The `denominator_inversions` field counts this **ratio-normalization** work
only. It does not count inversions internal to BGS interpolation or the
polynomial arithmetic kernels, prime validation, or the supplied prefix
provider. Claiming one inversion for the entire BGS computation would be
incorrect. The factorial calls in this service are already reflected, so
there is no hidden Wilson restoration inversion among them.

## Resource, timing and extension scope

The existing `max_direct_terms` and `max_degree` guards apply separately to
each actual acquisition. A derived factorial may exceed the direct term
limit while its individual gap acquisitions do not. These are per-acquisition
guards, not a total-batch time, term or memory budget. Batching needs arrays
and dictionaries proportional to the number of plans and product tokens,
in addition to the current kernel's memory. No many-prime remainder forest
or persistent cache is introduced.

`product_calls` records actual factorial and interval acquisitions with their
backend results and timings. `factorial_derivations` records every gap-based
extension. Acquisition time includes planner materialization and backend
work after ratio preparation; normalization time includes ratio construction
and shared inversion. Warm totals cover the entire batch call; cold totals
add session construction and prime validation. Imports and serialization are
excluded. `complete_many` also records provider calls and time. Its provider
support check and boundary planning are included in the whole-call total.

The batch planner supports the documented built-in families. It does not
consume arbitrary callback reductions from a separately configured
`BoundaryEvaluator`; an opaque finish callback does not expose the product
exponents required for shared inversion. Custom callbacks remain available
through the original single-query interface.

`test_shared_boundaries.py` validates against exact integer binomials and
independent coefficient/sum recurrences, including real-sharing spies,
reflection, mixed families, duplicates, empty requests, U-only semantics,
resource limits and invalid inputs. `benchmark_shared.py` compares separate,
exact and adjacent modes on the same unique indices, matching backends and
reductions. Every mode constructs one session per sample; the separate
baseline reuses its validated session but recomputes each boundary. See
RESULTS.md for actual counts, timing evidence and platform limits.
