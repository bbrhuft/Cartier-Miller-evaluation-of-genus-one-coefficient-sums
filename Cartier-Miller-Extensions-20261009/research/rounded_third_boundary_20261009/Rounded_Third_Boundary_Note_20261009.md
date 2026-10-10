# The rounded supersingular third point: the boundary is a Gauss factorial

Research note, 9 October 2026. This note is unrefereed and was prepared with substantial generative-AI assistance. It records elementary derivations, an equivalence statement, finite computational evidence and a targeted prior-art assessment. It adds no fast algorithm, no new implementation of a complete weighted sum and no benchmark. The published manuscript is unchanged. The companion assessment PRIOR_ART_ASSESSMENT_20261009.md gives the sources behind the literature statements made here.

## Summary

For a prime p ≡ 2 (mod 3), the original weighted central-binomial sum at the rounded third point needs the prefix B_L, which the retained elliptic routine already evaluates in O(log p) field operations, and the boundary a_L, which had no cheap method. This note shows by an elementary Wilson-reflection argument that

$$a_{(p+1)/3}\equiv\frac{3}{2\,(m!)^3}\pmod p,\qquad m=\frac{p-2}{3}=\left\lfloor\frac p3\right\rfloor .$$

Because cubing is a bijection of F_p when p ≡ 2 (mod 3), computing the boundary, computing the complete weighted sum U_p((p+1)/3) when p ≠ 17, computing the complete weighted sum at the floor endpoint, evaluating the supersingular branch value in the bridge identity (B6), and computing the Gauss factorial ⌊p/3⌋! mod p are all equivalent up to O(log p) field operations. The same factorial is Morita's Γ_p(1/3) modulo p. No closed form for this Gauss factorial has been located. The case is described as "utterly intractable" in the Gauss-factorial literature, and no polylogarithmic algorithm is known for factorials modulo p. The best deterministic bound for every prime is about √p up to logarithmic factors; an unrefereed 2026 report claims randomized p^{1/2−δ} for most primes (correction of 10 October 2026, see below). The rounded third point is therefore not a new fast complete-U family unless an advance on Gauss factorials is made. The obstruction is precise, and it answers the roadmap's question of whether CM trace data suffices: it does not, because the trace is identically zero.

## Setting and the integer endpoint

Let p ≥ 5 be prime with p ≡ 2 (mod 3), and put h=(p−1)/2, m=(p−2)/3 and L=m+1=(p+1)/3. Thus m=⌊p/3⌋=⌊(p−1)/3⌋ and L=⌈p/3⌉. Since p is odd and p−2 is odd, m is odd. The inequality L ≤ h holds exactly when p ≥ 5, so manuscript equation (32) defines U_p(L) and U_p(m) without denominators divisible by p.

As in the manuscript, a_i = C(2i,i)8^{−i} ≡ C(h,i)(−1/2)^i, and B_N = Σ_{i<N} a_i is the strict prefix. With f(w) = 1 − w³/2 we have f^h = Σ_i a_i w^{3i}. Every exponent 3i ≤ p−1 has i ≤ m, so

$$S_f(1)=\sum_{k\le p-1}c_k=\sum_{i\le m}a_i=B_L,\qquad H=c_{p-1}=0,\qquad K=c_{p-2}=a_m .$$

The upper endpoint L=(p+1)/3 is therefore the one at which the prefix is exactly the manuscript's non-branch query S_f(1). The argument λ=1 is admissible because f(1)=1/2. The curve has j=0, and its trace is exactly zero because cubing permutes F_p (Theorem T′ in the parent project's historical FINAL_U_p_L_REPORT.md, not included in this release). Theorem 1 applies with H=0 and M_χ=p+1, so no exceptional normalization occurs. The retained function elliptic_prefix.third(p), copied unchanged into retained/, returns this B_L with trace 0 and U=None. This note uses that routine as the existing fast prefix and does not modify it.

Manuscript identity (35), U_p(N) ≡ 4B_N − 2N(2N+5)a_N, holds for 0 ≤ N ≤ h. Since L ≡ 1/3 and m ≡ −2/3 in F_p, the two rounding choices give

$$U_p(L)\equiv 4B_L-\tfrac{34}{9}a_L,\qquad U_p(m)\equiv 4B_m+\tfrac{44}{9}a_m=4B_L+\tfrac{8}{9}a_m .$$

The second form uses B_m=B_L−a_m. Either rounding needs a boundary coefficient that the prefix does not provide.

## Theorem R: factorial form of the boundary

**Lemma 1.** In F_p, 8^m = 1/2. *Proof.* We have 3m=p−2, so 8^m=2^{p−2}=2^{p−1}/2 ≡ 1/2. ∎

**Lemma 2 (Wilson reflection).** For 0 ≤ n ≤ p−1, n!(p−1−n)! ≡ (−1)^{n+1} (mod p). *Proof.* Write (p−1)! = n!·∏_{k=1}^{p−1−n}(p−k) ≡ n!(−1)^{p−1−n}(p−1−n)!. Wilson's theorem gives (p−1)! ≡ −1, and p is odd. ∎

**Theorem R.** For p ≡ 2 (mod 3), p ≥ 5,

$$\binom{2m}{m}\equiv-\frac{3}{(m!)^3},\qquad a_m\equiv-\frac{6}{(m!)^3},\qquad a_L\equiv\frac{3}{2\,(m!)^3}\pmod p .$$

*Proof.* Take n=2m in Lemma 2. Then p−1−2m=(p+1)/3=m+1, so (2m)!(m+1)! ≡ −1. Since 3(m+1)=p+1, we have m+1 ≡ 1/3 and (m+1)! ≡ m!/3, which gives (2m)! ≡ −3/m!. Dividing by (m!)² gives the binomial congruence. Lemma 1 turns 8^{−m} into 2, which gives a_m. The ratio a_L/a_m=(2m+1)/(4(m+1)) has 2m+1=(2p−1)/3 ≡ −1/3 and 4(m+1) ≡ 4/3, so the ratio is −1/4 and a_L ≡ 3/(2(m!)³). Since m<p, the factorial is a unit, and so are both boundary coefficients. ∎

**Corollary U.** In F_p,

$$U_p\!\left(\tfrac{p+1}{3}\right)\equiv 4B_L-\frac{17}{3\,(m!)^3},\qquad U_p\!\left(\tfrac{p-2}{3}\right)\equiv 4B_L-\frac{16}{3\,(m!)^3}.$$

For contrast, at p ≡ 1 (mod 3) and L=(p−1)/3, the same reflection with n=2L gives C(2L,L) ≡ −1/(L!)³. In that case Jacobi's congruence evaluates the binomial as −r, where 4p=r²+27s² and r ≡ 1 (mod 3), so (L!)³ ≡ 1/r. Cosgrave and Dilcher (2018, Corollary 4.5) state that cube relation. It is exactly what makes the existing p ≡ 1 (mod 3) third-point evaluator complete through Cornacchia. For p ≡ 2 (mod 3) there is no corresponding representation, and the cube (m!)³ remains unevaluated.

## Theorem E: equivalence of the missing boundary with a Gauss factorial

For each prime p ≡ 2 (mod 3), p ≥ 7, consider six quantities in F_p:

| Quantity | Description |
|---|---|
| G(p) | the Gauss factorial ⌊p/3⌋! mod p |
| A(p) | the boundary a_L, L=(p+1)/3 |
| A′(p) | the floor boundary a_m |
| U(p) | the complete weighted sum U_p((p+1)/3) |
| U′(p) | the complete weighted sum U_p((p−2)/3) |
| T(p) | the branch value T_f(μ) at the unique root μ of f(w)=1−w³/2 |

**Theorem E.** These quantities are mutually computable with O(log p) additional field operations, with one exception: U(p) does not determine the others when p=17. More precisely, G gives A by A=3/(2G³), using O(1) operations and one inversion. A gives G by G=(3/(2A))^{(2p−1)/3}. A′=−4A. U=4B_L−(34/9)A and U′=4B_L−(32/9)A, and for p ≠ 17 the first inverts to A=(9/34)(4B_L−U). The second inverts for every p ≥ 7 as A′=(9/8)(U′−4B_L). Finally μ=2^{−m}, T=−A′/(3μ) and A=(3μ/4)T.

*Proof.* Since gcd(3,p−1)=1, the map x ↦ x³ is a bijection of F_p^×. Its inverse is x ↦ x^e with 3e ≡ 1 (mod p−1), and e=(2p−1)/3 works because 3e=2(p−1)+1. Theorem R then gives the first two conversions. The two weighted-sum relations follow from Corollary U and Theorem R. They use B_L, which manuscript Theorem 1, with trace zero and M_χ=p+1, supplies in O(log p) field operations without any trace preparation. The quadratic character χ=(2/p) is read from p mod 8. The constant 34=2·17 is a unit unless p ∈ {2,17}. At p=17 the coefficient of a_L vanishes, so U_p(6) ≡ 4B_6 is already fast there and carries no boundary information. The branch statements are Proposition B below. ∎

The direction "fast boundary implies fast weighted sum" uses the manuscript's Theorem 1 and the retained prefix routine, both of which still await human review. The direction "fast weighted sum or fast branch value implies fast Gauss factorial" uses only Theorem R, Proposition B and elementary field arithmetic, together with the same fast prefix for U. Consequently, an O(polylog p) method for either complete weighted sum at the rounded third point, or for this supersingular branch value, would give an O(polylog p) method for ⌊p/3⌋! mod p. This is a one-way implication about what such a method would achieve. It is not a lower bound and does not prove that no fast method exists.

## Proposition B: an elementary recheck of the bridge (B6)

The branch-point report (Cubic_Branch_Point_Report_20261006.md, equation B6) derived a_L=(3μ/4)T_f(μ) from the general branch formula T_f(μ)=(aμ/f′(μ))(μH−K), which is unrefereed. In this family the bridge can be checked without that formula.

**Proposition B.** For p ≡ 2 (mod 3), p ≥ 5, the unique μ ∈ F_p with μ³=2 is μ=2^{−m}, and

$$T_f(\mu)=\sum_{i=0}^{m}\binom{2i}{i}4^{-i}=(2m+1)\binom{2m}{m}4^{-m}=-\frac{a_m}{3\mu},\qquad a_L=\frac{3\mu}{4}\,T_f(\mu).$$

*Proof.* We have μ³=2^{−3m}=2^{2−p} ≡ 2, and the root is unique because cubing is bijective. The sparse expansion gives T_f(μ)=Σ_{i≤m}a_iμ^{3i}=Σ_{i≤m}a_i2^i=Σ_{i≤m}C(2i,i)4^{−i}. The classical telescoping identity Σ_{i=0}^n C(2i,i)4^{−i}=(2n+1)C(2n,n)4^{−n} holds in Z[1/2], by induction from C(2n+2,n+1)=C(2n,n)·2(2n+1)/(n+1), and therefore holds in F_p. Next, 2m+1 ≡ −1/3, and a_m/μ=C(2m,m)8^{−m}2^m=C(2m,m)4^{−m}, which gives the third expression. Finally a_L=−a_m/4. ∎

The general branch formula with a=−1/2, f′(μ)=−3μ²/2, H=0 and K=a_m gives T_f(μ)=−K/(3μ). This agrees with Proposition B, so it is an independent consistency check of that formula on one family. It is not a proof of the general branch formula. The validator also recomputes H, K and T_f(μ) from a dense power of f for 57 primes up to 600 without assuming sparsity.

## Relation to Γ_p and to classical Frobenius data

Morita's p-adic gamma function satisfies Γ_p(n)=(−1)^n∏_{0<j<n,\,p∤j}j for positive integers n, and Γ_p(x) ≡ Γ_p(y) (mod p) whenever x ≡ y (mod p) in Z_p, for odd p (Robert, 2000). Since m+1=(p+1)/3 ≡ 1/3 (mod p) and m is odd, m! = Γ_p(m+1) ≡ Γ_p(1/3) (mod p). Hence

$$a_{(p+1)/3}\equiv\frac{3}{2\,\Gamma_p(1/3)^3},\qquad K=a_m\equiv-\frac{6}{\Gamma_p(1/3)^3}\pmod p .$$

The second-kind coefficient K of the supersingular j=0 curve is thus a reduction of a Γ_p(1/3) value. Coleman (1990) expresses the absolute Frobenius on de Rham cohomology of Fermat curves through Γ_p for odd primes, and Ogus (1990) gives a p-adic Chowla–Selberg formula. This identification is therefore plausibly a mod-p shadow of known results. Those papers were not read here, and the claim needs specialist confirmation. In either case it does not make the coefficient computable, because Γ_p(1/3) mod p is the same factorial.

The Jacobi-sum route that works at p ≡ 1 (mod 3) does not transfer. For p ≡ 2 (mod 3), cubic characters exist only on F_{p²}, where the Gross–Koblitz formula (Gross & Koblitz, 1979) involves the product Γ_p(1/3)Γ_p(2/3). That product is ±1 by the reflection formula. This is an assessment made here, consistent with Stickelberger's evaluation of pure Gauss sums, and it should be confirmed by a reviewer. The trace supplies nothing either, since it is 0 for every such p. The behaviour also differs from Mordell's ((p−1)/2)! ≡ ±1 for p ≡ 3 (mod 4) (Mordell, 1961): there the square is forced to be ±1, whereas here the cube is unconstrained. In the validated range (m!)³ ≡ ±1 occurs only for p=5, 17 and 5987.

## Algorithms and honest costs

| Route | Field-operation cost for the boundary, hence for complete U | Status |
|---|---|---|
| Direct recurrence for a_L (the retained baseline) | Θ(p) | Implemented in the validators |
| Factorial ⌊p/3⌋! by polynomial-coefficient recurrences | O(M(√p) log p), where M(n) is the cost of multiplying degree-n polynomials (Bostan et al., 2007); about √p up to logarithmic factors | Known algorithm; not implemented here |
| All primes p ≤ N together, using accumulating remainder trees | Average polynomial in log N per prime, assessed by analogy with Costa et al. (2014) and Harvey (2014) | Assessment only; not implemented or verified here |
| Closed form from CM, trace or Jacobi-sum data | None known | Obstructed as above |
| Classical, randomized, conditional on divisors of p (Tal, 2026b) | Õ(q^c + √p/q^{1/4}) for q ∣ 1+p+p², with variants for divisors of p−1 and p+1; p^{1/2−δ+o(1)} for at least a 1−ε fraction of primes; c not explicit | Unrefereed ECCC report; abstract checked only; not implemented |
| Classical, deterministic, every prime (Tal, 2026b) | Bostan et al. (2007) improved by a factor √(log p / log log p) | Unrefereed; abstract checked only |
| Quantum, conditional on a divisor of p−1 (Tal, 2026a) | Below exponent 1/2 according to an unrefereed preprint | Outside the project's scope; noted only |

Correction, 10 October 2026: the 9 October version of this note cited Tal (2026a), a July preprint, for the statement that no classical worst-case single-input algorithm breaks the square-root barrier. A later classical report by the same author (Tal, 2026b, ECCC TR26-211, 26 September 2026) claims randomized algorithms below that barrier for primes with suitable divisors, at least a 1−ε fraction of primes, and a deterministic logarithmic-factor improvement of Bostan et al. (2007) for every prime. These claims are unrefereed and only the abstract was checked here. For p ≡ 2 (mod 3) note that 3 ∣ p+1, one of the divisor shapes the report treats; whether any of its constructions applies usefully to ⌊p/3⌋! has not been investigated. None of this changes Theorem E or gives a polylogarithmic method. A complete U_p((p+1)/3) at one prime therefore currently costs about √p field operations up to logarithmic factors deterministically, possibly p^{1/2−δ} by the claimed randomized methods, whereas the prefix alone costs O(log p). Any future benchmark must charge the factorial and must not report the cached O(log p) prefix as the complete cost.

## Evidence

The validator validate_rounded_third.py uses only the standard library. Run from the repository root, it checked every prime 5 ≤ p ≤ 20,000 with p ≡ 2 (mod 3), 1,136 primes in all. For each prime it computed a_m, a_L, B_L and both weighted sums from the original t_i recurrence of manuscript equation (32), independently of identity (35). It compared these with Theorem R, Corollary U and both inversions of Theorem E, including recovery of m! from a_L. It checked Proposition B, with exhaustive uniqueness of the cube root below 2,000, and confirmed that elliptic_prefix.third(p) returns the same B_L. Dense powers of f were checked for the 57 primes up to 600. The validator also checked the companion relation C(2L,L) ≡ −1/(L!)³ ≡ −r at the 330 primes p ≡ 1 (mod 3) below 5,000, with r found by brute force. There were no failures. The degenerate prime p=17 is recorded separately. The results are in results/validation.json and results/rounded_third_values.csv. They are finite evidence, not proofs, and contain no timings.

## Status

| Claim | Status |
|---|---|
| Endpoint L=(p+1)/3 and B_L=S_f(1) with H=0 | Elementary; checked |
| Theorem R and Corollary U | Elementary proof here; checked for 1,136 primes; classical in substance |
| Theorem E (equivalence, with the p=17 exception) | Proof here; the weighted-sum directions rely on unrefereed manuscript Theorem 1 for B_L |
| Proposition B (elementary proof of B6 in this family) | Proof here; agrees with the general branch formula; does not prove that formula generally |
| a_L ≡ 3/(2Γ_p(1/3)³) and the link to Coleman and Ogus | Congruence follows from standard Γ_p properties; the link to Frobenius data is a plausible but unchecked attribution |
| Fast complete U at the rounded third point | Not achieved; equivalent to an open problem on Gauss factorials; Õ(√p) per prime deterministically, with unrefereed randomized p^{1/2−δ} claims for most primes (Tal, 2026b); no polylogarithmic route known |
| Novelty | Not claimed; the reduction is short, and its ingredients are classical |

The rounded third point should be parked with this obstruction recorded, unless a batch workload over many primes is wanted. In that case the remainder-tree route is the natural next bounded task.

## Questions for human review

A reviewer should check six things. First, whether manuscript identity (35) and the reduction convention apply at N=(p+1)/3 and N=(p−2)/3 for all p ≥ 5. Second, whether the use of Theorem 1 with trace zero for B_L needs any separate hypothesis at p=5. Third, whether the Γ_p continuity and parity step is stated with the correct sign. Fourth, whether the Gross–Koblitz assessment for cubic characters over F_{p²} is correct. Fifth, whether Coleman (1990) or Ogus (1990) already contain the mod-p identification of the supersingular second-kind coefficient. Sixth, whether the Gauss-factorial literature contains any evaluation of ⌊p/3⌋! mod p for p ≡ 2 (mod 3) beyond those located.

## References

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793

Coleman, R. F. (1990). On the Frobenius matrices of Fermat curves. In F. Baldassarri, S. Bosch, & B. Dwork (Eds.), *p-adic analysis* (Lecture Notes in Mathematics, Vol. 1454, pp. 173–193). Springer.

Cosgrave, J. B., & Dilcher, K. (2018). Gauss factorials, Jacobi primes, and generalized Fermat numbers. *Punjab University Journal of Mathematics, 50*(4), 1–21.

Costa, E., Gerbicz, R., & Harvey, D. (2014). A search for Wilson primes. *Mathematics of Computation, 83*(290), 3071–3091. https://doi.org/10.1090/S0025-5718-2014-02800-7

Gross, B. H., & Koblitz, N. (1979). Gauss sums and the p-adic Γ-function. *Annals of Mathematics, 109*(3), 569–581.

Harvey, D. (2014). Counting points on hyperelliptic curves in average polynomial time. *Annals of Mathematics, 179*(2), 783–803.

Mordell, L. J. (1961). The congruence ((p−1)/2)! ≡ ±1 (mod p). *The American Mathematical Monthly, 68*(2), 145–146.

Ogus, A. (1990). A p-adic analogue of the Chowla–Selberg formula. In F. Baldassarri, S. Bosch, & B. Dwork (Eds.), *p-adic analysis* (Lecture Notes in Mathematics, Vol. 1454, pp. 319–341). Springer. https://doi.org/10.1007/BFb0091147

Robert, A. M. (2000). *A course in p-adic analysis* (Graduate Texts in Mathematics, Vol. 198). Springer.

Tal, Y. (2026a). *Quantum algorithms for modular factorials* (arXiv:2607.29453) [Preprint]. arXiv.

Tal, Y. (2026b). *Computing modular factorials below the square-root barrier* (ECCC Report TR26-211). Electronic Colloquium on Computational Complexity. https://eccc.weizmann.ac.il/report/2026/211/
