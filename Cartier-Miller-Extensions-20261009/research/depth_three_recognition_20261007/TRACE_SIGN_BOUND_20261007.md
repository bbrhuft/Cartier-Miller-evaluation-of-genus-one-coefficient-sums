# Consolidated trace-sign bound for the depth-three family

7 October 2026. This is an unrefereed consolidation of the discriminant −192 extension, not a revision of the published Cartier–Miller manuscript. The family and recognition theorem are in the companion proof note. The new result below closes the trace-sign trial-count gap, conditional on that note's recognized-family trace proposition. No novelty or measured performance claim is made.

## Hypotheses and exact sign certificates

Let p be prime with p congruent to 1 modulo 24, and let E: y²=x³+Ax+B belong to the parameter-verified depth-three family from the ordinary j=0 seed. The retained trace proposition gives a unique pair of positive integers (t₀,f) with 4p=t₀²+192f² and the exact trace τ in {t₀,−t₀}. Set n₊=p+1−t₀, n₋=p+1+t₀ and g=gcd(n₊,n₋). All conclusions below use this two-candidate theorem. They are not certificates of arbitrary curve orders.

For a rational point P, if exactly one of [n₊]P and [n₋]P is the identity, that candidate is the true group order: the true order annihilates every rational point by Lagrange's theorem, and the other candidate demonstrably fails on P. This is an exact point witness, not a probabilistic inference from an annihilation test alone. The implementation now retains P, the candidate orders and their annihilation flags, and `verify_trace_sign_witness` rechecks the point equation and both scalar multiplications. If both vanish the trial is inconclusive. If neither vanishes the recognized-family trace premise or the implementation is wrong; this is reported as a proof violation.

Write G=E(F_p), N=#G=p+1−τ. The inconclusive subgroup is exactly K=G[g]. Indeed points killed by both n₊ and n₋ are killed by their gcd, by Bézout's identity, and the converse is immediate. Since the true N is one candidate, this is also the kernel of the other candidate acting on G.

## A proper subgroup at all large eligible primes

The standard finite-field group structure is G≅Z/n₁Z⊕Z/n₂Z, n₁|n₂, n₁n₂=N, with n₁|p−1. For completeness, the rank-two statement and p∤n₁ follow from torsion structure (Sutherland, 2025a, Corollary 6.4). All n₁² geometric n₁-torsion points are then rational, so the Weil pairing puts the n₁-th roots of unity in F_p and implies n₁|p−1 (Sutherland, 2025b, Corollary 23.24). Therefore

$$|K|=\gcd(n_1,g)\gcd(n_2,g).$$

Because g divides both N and 2τ, gcd(n₁,g) divides gcd(p−1,N,2τ). Any divisor of the latter divides N−(p−1)=2−τ and 2τ, and consequently divides 4. Hence

$$|K|\le4g\le8|\tau|\le16\sqrt p.$$

For p≥337, Hasse's bound gives N≥p+1−2√p>16√p; the last inequality follows from (p+1)²>324p. Thus K is a proper subgroup. This argument is uniform in p and uses no enumeration of family members or observed trial counts.

## The finite small-prime exception

The eligible primes below 337 are exactly 73, 97, 193, 241 and 313; trial division verifies this finite list. Their unique representations give the following exact integer data.

| p | t₀ | f | g | min(n₊,n₋) | Bound 4g |
|---|---|---|---|---|---|
| 73 | 10 | 1 | 4 | 64 | 16 |
| 97 | 14 | 1 | 28 | 84 | 112 |
| 193 | 2 | 2 | 4 | 192 | 16 |
| 241 | 14 | 2 | 4 | 228 | 16 |
| 313 | 22 | 2 | 4 | 292 | 16 |

The bound already proves K proper for four rows. Only p=97 requires point witnesses. Here √3∈{10,87}, √2∈{14,83}, and 5 is a quadratic nonresidue, since 5⁴⁸≡−1 modulo 97. Every nonzero r is either s² or 5s² for some s∈F_97*. The parameter model at r=r₀s² is isomorphic over F_97 to the model at r₀ by x↦s²x, y↦s³y. Thus the four embeddings and r₀∈{1,5} give eight representatives of all family models. The following exact witnesses are on those curves and are not killed by g=28.

| e | √2 | r₀ | (A,B) | P | [28]P |
|---|---|---|---|---|---|
| 10 | 14 | 1 | (89,26) | (2,55) | (12,94) |
| 10 | 14 | 5 | (91,49) | (0,90) | (80,66) |
| 10 | 83 | 1 | (16,30) | (3,69) | (43,54) |
| 10 | 83 | 5 | (12,64) | (0,89) | (35,0) |
| 87 | 14 | 1 | (61,77) | (3,53) | (43,57) |
| 87 | 14 | 5 | (70,22) | (1,53) | (0,64) |
| 87 | 83 | 1 | (13,24) | (0,86) | (12,68) |
| 87 | 83 | 5 | (34,90) | (3,92) | (73,0) |

These are finite algebraic certificates, not an extrapolation from numerical agreement. Each curve equation and displayed scalar multiplication is checked by an independent left-to-right group-law implementation in `core/validate_consolidation.py`. Isomorphisms preserve the property [28]P≠O, so this proves K proper for every family member at the single exceptional prime. The CSV `core/sign_bound_p97_witnesses.csv` retains the certificates in machine-readable form.

## Bound for the actual random-x sampler

At every eligible prime, K is proper, hence |K|≤N/2. The code samples x uniformly in F_p, computes a square root of x³+Ax+B if it exists, and rejects y=0. This does not sample uniformly from all points of G, so a point-based probability cannot be substituted without checking the sampler.

Since t₀ is even, both candidate orders are even. Thus O and all rational two-torsion points lie in K. Every point outside K has y≠0, and P and −P are either both outside or both inside K. The N−|K| successful affine points consequently correspond to exactly (N−|K|)/2 distinct x values; either square-root choice succeeds. One raw x draw has success probability

$$\frac{N-|K|}{2p}\ge\frac{N}{4p}\ge\frac15.$$

For p≥97, the last inequality follows from p+1−2√p≥4p/5. At the remaining eligible prime p=73 the exact candidates give N≥64>4p/5. All non-square and zero-right-hand-side draws are already charged in this bound.

With independent uniform draws, the unbounded algorithm has expected raw trial count at most 5 and terminates almost surely; the probability of still being inconclusive after k raw draws is at most (4/5)^k. The default cap is now 64, whose conservative inconclusive bound is about 6.28×10⁻⁷. This is a bound on returning no answer, not a probability of a wrong answer. `max_trials=None` and CLI `--unbounded-sign-test` expose the unbounded zero-error version. The capped version retains the explicit inconclusive status and does not guess or invoke an unseen fallback. Arbitrary user-supplied deterministic RNGs need not satisfy the uniformity assumption.

## Preparation and query costs

Put n=⌈log₂p⌉. Recognition after prime validation uses a constant number of field operations; this counts inversions as field operations and is not constant bit time. Cornacchia uses O(n) Euclidean divisions on O(n)-bit integers. A random cubic-nonresidue search has expected at most 3/2 exponentiation attempts. Tonelli–Shanks has O(n²) field operations per square-root attempt, including its loop, and its random nonresidue selection has expected at most two attempts. Each sign trial makes at most two O(n)-length scalar multiplications. The raw sign trial bound therefore yields expected O(n²) field operations plus polynomial integer work for complete unbounded preparation. Using elementary O(n²) multiplication and inversion, O(n⁴) bit operations is a conservative combined upper bound, not a sharp complexity claim.

| Operation | Charge and limitation |
|---|---|
| Prime validation in the prototype | Separately charged; deterministic validation only for 7≤p<2⁶⁴; the mathematical statement assumes a prime supplied or certified independently |
| Recognition, path checking and K reconstruction after the trace | O(1) field operations, including inversions |
| Complete unbounded CM preparation | Expected O(log²p) field operations and polynomial bit work; almost-sure termination under independent uniform draws |
| Default capped CM preparation | Same per-trial cost, at most 64 raw sign draws; may return an honest inconclusive status; internal nonresidue searches remain randomized |
| Supplied nonzero rational branch query after preparation | O(1) field operations, including root validation and output reconstruction; root finding is outside the query |
| Complete unconditional deterministic alternative | Schoof trace preparation plus O(1) field operations; the prototype does not automatically invoke this backend |

The expected bound is a theoretical derivation, not a timing result. It computes H, K and a supplied branch/root value. It does not claim an original weighted-sum evaluator for arbitrary stopping indices; such a claim still requires both B_L and a_L. It says nothing new about a sum-avoiding Witt correction.

## Preserved obstruction and mathematical scope

On the easy seed E:y²=x³+19 over F_97, exact enumeration gives #E=112 and τ=−14. Every rational point is killed by 28, so both candidate orders 84 and 112 annihilate every point. A sign algorithm on this seed could remain inconclusive forever. The independent enumeration and scalar-multiplication checks are retained in `core/sign_test_obstruction.json` and its generating validator. This obstructs applying the success theorem to arbitrary curves or to every easy seed, even when there are exactly two correct trace candidates. The implementation now checks the depth-three recognition premise before attaching the bound.

The retained differential normalization is unchanged. With t=−x/y at infinity, x=t⁻²+O(t²), y=−t⁻³+O(t), ω=2dt+O(t⁴)dt and η=2t⁻²dt+O(t²)dt. For the quotient rooted at q, u=F′(q), the primitive y/(x−q) has leading term −t⁻¹ at infinity. Thus −2d(y/(x−q)) contributes −2t⁻²dt, reducing the leading term of (2x−q)ω from +4t⁻²dt to +2t⁻²dt. At the kernel use z=y: x−q=z²/u+O(z⁴), ω=(2/u+O(z²))dz and the primitive is u/z+O(z), so the same exact correction has principal part +2u z⁻²dz. The quotient term x′ω has that same positive principal part there. Both poles have residue zero, and the differential scale remains +1. Cartier kills the global exact differential, yielding β′=2β−qH with the stated sign. These are local checks accompanying the retained global rational-function identity, not replacements for it.

The family-recognition proof, the CM trace proposition and this success-bound proof remain unrefereed. Their correctness and any priority claims need human review. The counterexample, finite certificates, retained historical validation and fresh checks have separate roles and must remain distinct.

## Primary sources checked for the new argument

Sutherland, A. V. (2025a). *18.783 Elliptic curves, Lecture 6: Torsion subgroups and endomorphism rings*. Massachusetts Institute of Technology. Corollary 6.4, pp. 1–2. https://math.mit.edu/classes/18.783/2025/LectureNotes6.pdf . Opened 7 October 2026; used for rank-two group structure and p∤n₁, not for the new probability bound.

Sutherland, A. V. (2025b). *18.783 Elliptic curves, Lecture 23*. Massachusetts Institute of Technology. Theorem 23.23 and Corollary 23.24, pp. 9–13. https://math.mit.edu/classes/18.783/2025/LectureNotes23.pdf . Opened 7 October 2026; used for the Weil-pairing implication E[n₁]⊆E(F_p)⇒n₁|p−1. These are authoritative course notes, not new research claims.

The prior note's CM trace argument uses Sutherland (2013), *Isogeny volcanoes*, Theorem 7(iv) and Remark 8, which were reopened in the preceding review. Hasse's bound, the recognized-family CM reduction, and all normalization assumptions are stated explicitly in the companion proof note. No deterministic sextic-character sign formula is asserted here.
