# Fifth-point integration and shared boundaries

Version 0.3 connects the existing genus-two Cantor–Miller prefix routine and retained fifth/tenth-point boundary reductions. This is reuse and exact algorithm integration, not a claim of a new boundary theorem or exponent improvement. The retained project mathematics remains unrefereed. The independent checks and local benchmarks are recorded separately.

## Mathematical domain

Let p ≥ 19 be prime with p ≡ 4 modulo 5. Write

$$p=10\ell-1,\qquad L=\frac{p+1}{5}=2\ell,\qquad h=5\ell-1.$$

The two supported indices are L and 2L, both at most h. The targets are a_n = binom(2n,n)8^(−n), the strict prefixes B_n = sum_(i<n) a_i, and the original sums U_p(n) defined by the t recurrence in MATHEMATICS.md.

The retained routine `prefixes(p,5,all_prefixes=True)` computes both B_L and B_(2L) in one genus-two pass. It uses y² = 1−x⁵/2 and the known annihilator p+1, so no point-counting routine or caller-supplied trace is needed. Theorem HG in RETAINED_HIGHER_GENUS_REPORT.md supplies the project justification. Its implementation is copied unchanged, with a source hash.

## Retained boundary identities

The existing integration archive's `cm_system/api.py::fifth_boundaries` uses

$$a_L=(-1)^\ell 2^{-2L}\binom{2L-1}{\ell}\pmod p,$$
$$a_{2L}=(-1)^\ell\frac{2^{2L}}{16}\binom L\ell\pmod p.$$

Here is an elementary self-contained derivation. For 0 ≤ n ≤ h, separate even and odd factors of (2n)!. Since 2j−1 = −2(h+1−j) modulo p,

$$\boxed{(2n)!=(-4)^n n!\,\frac{h!}{(h-n)!}\pmod p.}$$

All factorials used below have indices less than p and are units. Applying this identity with n = 2ell gives

$$a_L=2^{-2\ell}\frac{h!}{(2\ell)!(3\ell-1)!}.$$

Applying it with n = ell gives h! = (−4)^(−ell)(2ell)!(4ell−1)!/ell!. Substitution yields

$$a_L=(-1)^\ell2^{-4\ell}\frac{(4\ell-1)!}{\ell!(3\ell-1)!},$$

the first identity. Applying the same duplication identity with n = 4ell, and substituting this expression for h!, gives

$$a_{2L}=2^{-4\ell}\frac{h!}{(4\ell)!(\ell-1)!}
=(-1)^\ell2^{-6\ell-2}\binom{2\ell}{\ell}.$$

Because p−1 = 10ell−2, Fermat's theorem gives 2^(−6ell−2) = 2^(4ell−4) modulo p, proving the second identity. These reductions and their implementation are not promoted as new discoveries in this release.

## Shared interval acquisition

Define the three half-length products

$$I_0=\prod_{j=1}^{\ell}j,\quad I_1=\prod_{j=3\ell}^{4\ell-1}j,\quad I_2=\prod_{j=\ell+1}^{2\ell}j.$$

Then a_L = (−1)^ell 2^(−2L) I_1/I_0 and a_(2L) = (−1)^ell 2^(2L) I_2/(16 I_0). A paired request computes precisely these three products and the common denominator inverse once. A single boundary needs I_0 and one numerator product. The phrase "one inverse" applies only to this shared denominator, not to all scalar powers or inversions inside the geometric prefix routine.

Interval products use the same exact polynomial kernels as the factorial backend. For an interval [start,start+n), set s = floor(sqrt(n)) and f(X) = product_(0≤j<s)(X+start+j). Evaluation at X = 0,s,...,(s−1)s gives the first s² factors, followed by a tail of at most 2s factors. The `product_tree` routine uses exact product/remainder trees and Kronecker-packed integer polynomial multiplication. Version 0.5 adds `bgs`, which builds the same block values by arithmetic-progression shifts and recursive doubling; BGS_BACKEND.md gives its proof and denominator checks. Direct loops remain available. Automatic dispatch selects direct through the configurable cutoff, BGS above it. Tal refinements remain separate.

At fixed genus the retained prefix pass has logarithmic field-operation length, but the complete calculation still includes interval products. With this product-tree backend the conventional polynomial-arithmetic bound is square-root scale up to logarithmic factors. Shared work improves constants and avoids duplicate acquisition; no new asymptotic exponent saving is asserted.

## Output contract and controls

`FifthPointSession(p).evaluate()` returns an `outputs` array for [L,2L], plus shared prefix/boundary diagnostics and cold/warm timings. `evaluate(indices)` accepts either index, preserves duplicates and order, and shares arithmetic within that call. Every nonempty call computes both native prefixes in one pass, even if only one is selected for return. Repeated calls recompute arithmetic; no complete-answer cache or persistent interval cache is used. An empty request does no prefix or boundary arithmetic.

The boundary-only `FifthBoundaryEvaluator` has the same supported indices and returns boundary values without computing any prefix. Integer and prime validation, supported-index checks, precision checks and resource caps occur before the prefix pass. Requests for p² are rejected; the displayed mod-p identities are not reused at higher precision. The retained kernels require assertion checks, so the integrated service rejects Python `-O` execution.

At p = 29 and n = 2L = 12, the U boundary multiplier vanishes. Full-output mode still computes and returns a_12 = 13 because its contract includes that diagnostic. B_12 = 17 gives U_29(12) = 10. Version 0.4 provides the separate `output_mode="u_only"` contract: the second output needs no boundary products, while the pair needs only the first output's two products. B and a are null in that output mode. See OUTPUT_MODES.md.

## Independent checks and benchmark fairness

Both boundary formulas are checked against Python's exact integer binomial at every supported prime through 10,000, using both numerical backends. Complete paired outputs are checked against an independent scaled binomial prefix and the original t recurrence. Single, duplicate, empty and invalid requests, actual prefix/interval call counts, resource failures and the p = 29 zero multiplier are also checked.

The paired benchmark includes preparation and compares both complete U outputs. Its direct baseline shares one pass of the original rational recurrence up to 2L. Its generic-boundary comparator also shares work: one genus-two prefix pass and three unique factorials L!, (2L)! and (4L)!, using Wilson reflection where appropriate. Thus it does not inflate the baseline by computing (2L)! twice. The separate-call comparison deliberately makes two calls and discloses that each computes both native prefixes. Results are local implementation measurements, not universal speedups or comparisons with optimized C/FLINT/Tal code.
