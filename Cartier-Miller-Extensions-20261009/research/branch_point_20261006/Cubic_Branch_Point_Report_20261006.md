# Cubic branch-point evaluation through second-kind Cartier data

David Jordan research project, 6 October 2026. Separate extension note; the published Cartier–Miller manuscript and source snapshots are unchanged. The repository URL and commit remain unknown. This is an unrefereed, AI-assisted derivation with executable finite checks, not a novelty or performance-priority claim.

## Result and scope

Let p≥7 be prime, let f(w)=1+cw+bw²+aw³ be squarefree over F_p, with a≠0, and let μ∈F_p× satisfy f(μ)=0. Put h=(p−1)/2 and write f(w)^h=Σ c_m w^m. Define

$$H=c_{p-1},\qquad K=c_{p-2},\qquad T_f(w)=\sum_{m=0}^{p-1}c_mw^m.$$

Then the branch query has the exact formula

$$\boxed{T_f(\mu)=S_f(1/\mu)=\frac{a\mu}{f'(\mu)}(\mu H-K)\quad\text{in }\mathbb F_p.} \tag{B1}$$

Here f′(μ) is nonzero by squarefreeness. No inverse of H, trace, annihilator or square root appears. The formula covers ordinary and supersingular curves. Once (H,K) have been prepared in the specified coordinate, a supplied branch root requires O(1) field operations, including its input checks. The present complete prototype prepares both coefficients in O(p) field operations and O(1) working field elements. Existing polynomial-recurrence machinery gives a square-root preparation bound; a general polylogarithmic preparation of K has not been established here.

The reduction is a direct consequence of the characteristic-p high-part identity already present in Voloch’s work. Its usefulness here is the explicit normalization for the retained truncation and the separation of preparation from query cost. No new general second-kind theory is claimed.

## Differential proof with signs and scale

On C:v²=f(w), use ω=dw/v and η=wω. The branch differential is

$$\theta_\mu=\frac{dw}{(1-w/\mu)v}=-\frac{\mu}{w-\mu}\omega.$$

At Q=(μ,0), the coordinate z=v is a uniformizer. Because f′(μ)≠0,

$$w=\mu+\frac{z^2}{f'(\mu)}+O(z^4),\qquad \omega=\left(\frac{2}{f'(\mu)}+O(z^2)\right)dz.$$

Consequently θμ=−2μ z⁻² dz+O(1)dz. There is no z⁻¹ term and hence no residue. The old quantities r=μ/v₀ and the divisor of two distinct simple poles are unavailable at v₀=0. In particular, this computation is not a limiting substitution into the admissible Miller identity.

Factor f=(w−μ)g. The quadratic polynomial g has leading coefficient a and g(μ)=f′(μ). Define the global rational function

$$q_\mu=\frac{2\mu}{f'(\mu)}\frac{v}{w-\mu}.$$

Its local leading term at Q is 2μ/z. Direct differentiation gives

$$d\left(\frac{v}{w-\mu}\right)=\frac12\left(g'(w)-\frac{g(w)}{w-\mu}\right)\omega.$$

For a quadratic g,

$$(g(w)-g(\mu))/(w-\mu)-g'(w)=a(\mu-w).$$

Therefore the global identity, with no omitted holomorphic term, is

$$\boxed{\theta_\mu=dq_\mu+\frac{a\mu}{f'(\mu)}(\mu-w)\omega.} \tag{B2}$$

This also tracks the global poles: qμ has a simple pole at Q and a simple pole at the cubic’s point at infinity. It is regular at the other branch points. The remaining η term has its second-kind pole at infinity; the poles there cancel in (B2). Merely subtracting the local expression d(2μ/z) would not establish this global equality.

Use absolute Cartier with C(Σ b_n z^n dz)=Σ b_{pj+p−1}^{1/p}z^j dz. Exact differentials are killed. The relation v^{p−1}=f^h and the degree bound 3h+1<2p−1 show

$$C(\omega)=H\omega,\qquad C(\eta)=K\omega.$$

All scalars in (B2) lie in F_p, so their inverse-Frobenius powers are themselves. Applying Cartier yields

$$C(\theta_\mu)=\frac{a\mu}{f'(\mu)}(\mu H-K)\omega.$$

At P₊=(0,1), w is a local coordinate and

$$\theta_\mu=v^{-p}\frac{f^h}{1-w/\mu}\,dw.$$

The coefficient selection at w=0 therefore gives (Cθμ/ω)(P₊)=[w^{p−1}]f^h/(1−w/μ)=S_f(1/μ). Finally μ^{p−1}=1 identifies this coefficient functional with T_f(μ). This proves (B1); finite checks below are supporting evidence, not the proof.

## Independent polynomial proof and prior work

Write

$$P=f^h=U+Hw^{p-1}+w^pR,\qquad\deg U\le p-2.$$

Since 2h=−1 in F_p, f′P+2fP′=0. Substitution and comparison of the only possible surviving coefficients in degrees p and p+1 give

$$\boxed{f'(w)R(w)+2f(w)R'(w)=aK-aHw.} \tag{B3}$$

At w=μ, f′(μ)R(μ)=a(K−μH). Also P(μ)=0 and μ^p=μ, so T_f(μ)=−μR(μ), which again gives (B1). This second proof fixes the sign independently of the geometric notation.

Voloch (1997), Section 2, gives the monic-cubic identity f′T+2fT′=−Ax+B, where A and B are his coefficients in degrees p−1 and p−2. His T is the high-part polynomial, not our truncated T_f. The author-hosted manuscript was read directly; journal metadata were verified at the publisher, whose download endpoint returned 403. The algebraic proof above is self-contained and extends the displayed monic identity to leading coefficient a without appealing to any disputed quasi-period sign. Voloch’s adjacent ζ-function discussion uses dx/(2y) and explicitly notes scale and sign corrections to earlier work; those quasi-period conventions are not imported into (B1).

Katz’s published author-hosted article, Section 1 and Theorem 3.1, identifies the coefficients of C(dx/y) and C(x dx/y) with the degrees p−1 and p−2 polynomial-power coefficients. These are classical Cartier data. His no-common-zero statement implies that in the supersingular case the second coefficient is nonzero after any invertible model change. Novelty of the particular truncation corollary is not asserted; comprehensive citation tracing has not been completed.

## Coordinate normalization

The coefficient K depends on the affine coordinate. It must not be reused from an unrelated Weierstrass model without conversion. For the cubic model with origin at infinity, use

$$x=aw+b/3,\qquad y=av.$$

Then y²=x³+Ax+B, where

$$A=ac-b^2/3,\qquad B=a^2-abc/3+2b^3/27,$$

and ω=dw/v=dx/y=2ω∞ with ω∞=dx/(2y). If

$$\beta=[x^{p-2}](x^3+Ax+B)^h,$$

then

$$\beta=aK+(b/3)H,\qquad K=(\beta-(b/3)H)/a. \tag{B4}$$

Both bases ω∞, xω∞ and dx/y, x dx/y have Cartier scalar pair (H,β), because scaling both differentials by 2∈F_p× cancels in their scalar equations. This model has origin at infinity. It is different from the retained rational-point-to-origin construction with κ=−2; no change is made to that construction. In the present proof the displayed scale is +2 and there is no Miller slope accumulator.

The trace relation H=τ mod p remains valid. A rational cubic branch is nonidentity rational 2-torsion when infinity is the origin, so the group order and τ are even. Thus the trace ±1 exceptional cases of the original admissible theorem do not arise for a cubic in this branch-input family. Formula (B1) does not use the exceptional theorem in any case.

## Preparation and query cost

Let M(d) denote polynomial-multiplication cost over F_p. The table separates the proved formula, the implemented preparation and an established recurrence-method option.

| Input and route | Preparation | Branch query | Status |
|---|---|---|---|
| Supplied certified (H,K) | Charged to the provider | O(1) field operations | Exact formula (B1); supplied root checked |
| Default standalone prototype | O(p) field operations, O(1) working field elements | O(1) | Implemented and checked; no trace counter needed |
| General polynomial-block recurrence | O(M(√p) log p) field operations with fast polynomial multiplication | O(1) | Established conventional BSGS route applied to the matrix below; not implemented or benchmarked here |
| Optimized Bostan–Gaudry–Schost recurrence | O(√p+M(√p)) field operations for fixed matrix dimension | O(1) | Theorem 14 supplies the bound under its unit prerequisites; not implemented or benchmarked here |
| Existing trace plus missing K | T_trace+T_K | O(1) | Schoof supplies τ, but does not by itself supply K |
| Structural β=0 families below | T_Schoof+O(1) field operations outside point counting | O(1) | Deterministic polynomial-time consequence; API accepts trusted external exact trace |

For completeness, if c_n=[w^n]f^h, then

$$n c_n=\sum_{j=1}^3((h+1)j-n)f_jc_{n-j},\quad 1\le n<p,$$

where c₋₁=c₋₂=0. Set V_n=n!(c_n,c_{n−1},c_{n−2})ᵀ. It obeys the degree-one polynomial matrix recurrence

$$V_n=\begin{pmatrix}
(h+1-n)c & (2(h+1)-n)b & (3(h+1)-n)a\\
n&0&0\\
0&n&0
\end{pmatrix}V_{n-1},\qquad V_0=(1,0,0)^T.$$

Wilson’s identity (p−1)!=−1 means that H and K are just the negatives of the first two coordinates of V_{p−1}. No factorial table or per-step inversion is required. The executable linear preparation retains exactly three state elements. Primality checking and fixed-degree squarefreeness are included in its public API; its 64-bit input guard and primality base set follow the retained standalone third-point implementation. The mathematical theorem has no 64-bit restriction.

This explicit linear matrix also puts the data into the established BGS framework. Here N=p−1 and the relevant small-integer unit range is below p, so the field has the required units. A quasi-linear polynomial backend gives soft-O(√p) preparation. This is an application of established recurrence evaluation, not a new bound below that baseline. No timings for an unimplemented backend are reported.

There are at most three rational branch roots on one cubic. Thus constant-time cached queries alone do not establish a large-workload speedup: the data-preparation cost must be charged even if all branches are evaluated. Root finding is outside the API because the question specifies μ; query() verifies the supplied root. The formula handles no arbitrary stopping index and supplies no new general complete-U result.

## A genuinely bounded fast subfamily

Equation (B4) becomes especially simple when β=0. For a nonsingular short cubic with A=0 and p≡1 mod 3, every exponent of (x³+B)^h is divisible by 3, whereas p−2 is not, so β=0. For B=0 and p≡1 mod 4, h is even and every exponent of x^h(x²+A)^h is even, whereas p−2 is odd, again giving β=0. These are the ordinary j=0 and j=1728 congruence classes.

In either family K=−bH/(3a), and (B1) reduces to

$$\boxed{T_f(\mu)=\frac{\mu H}{f'(\mu)}(a\mu+b/3).} \tag{B5}$$

An exact trace then provides all required preparation data; Schoof gives an unconditional deterministic polynomial-time complete-run consequence. The implementation prepare_from_trace() recovers these data in constant field operations, but trusts the externally supplied exact trace. Its Hasse-range check is necessary and does not certify the trace. It does not call the retained fixed-quarter Schoof backend on a different curve, and no production SEA backend is claimed.

The proof is the elementary sparsity argument above, not numerical recognition of complex multiplication. It must not be extended to supersingular congruence classes: β need not vanish there.

## Obstructions and explicit examples

At p=7, f=1+4w+w²+w³ and μ=1, direct expansion gives H=0, K=3, f′(1)=2, and T_f(1)=2. Dropping K predicts 0 and fails. The short model has A=−1, B=0, so this also disproves extending the β=0 j=1728 rule to p≡3 mod 4. Dividing by H would be undefined. This counterexample narrows those proposed shortcuts; it is not a lower bound on every possible algorithm.

At p=7, the two cubics 1+w³ and 1+w+w²+w³ have the same exact trace −4 and the same branch μ=6, but K is respectively 0 and 5 and the branch answers are 1 and 4. Thus K is not determined by the trace alone. The full input includes the curve coefficients; this example does not show that a fast curve-dependent algorithm is impossible.

Given H and a branch value, the extra coefficient can be recovered in O(1):

$$K=\mu H-\frac{f'(\mu)}{a\mu}T_f(\mu).$$

Consequently generic branch evaluation and K recovery are equivalent with that supplied trace data. This identifies the remaining problem exactly without asserting a complexity lower bound. If two distinct branches are given, their normalized answers Zμ=f′(μ)T_f(μ)/(aμ) lie on the affine line Zμ=μH−K, which also yields a consistency check for three rational roots.

## Link to the deferred rounded third point

For p≡2 mod 3, take f=1−w³/2 and L=(p+1)/3. The unique rational branch satisfies μ³=2 and can be computed by μ=2^{3⁻¹ mod (p−1)}. Here H=0 and K=a_{L−1}, with a_i=binom(2i,i)8⁻ⁱ. Formula (B1) gives T_f(μ)=−K/(3μ). The boundary recurrence has a_L=−a_{L−1}/4, so

$$\boxed{a_L=(3\mu/4)T_f(\mu).} \tag{B6}$$

This is an exact bridge to the other shortlisted extension. A fast branch evaluator for this supersingular family would supply its missing rounded-third boundary and, together with the already retained fast B_L routine, complete U. The current linear preparation does not beat the existing boundary baseline, so no such complete fast result is claimed. The bridge was checked independently at all 47 applicable primes from 7 through 499.

## Computational evidence and reproducibility

The main validator enumerates every normalized cubic with nonzero leading coefficient at p=7,11,13,17,19,23. There are 26,292 candidates; 1,344 are singular and 24,948 are squarefree. Of the squarefree cubics, 9,240 have no rational branch; all 15,708 remaining cubics and all their 22,260 rational branches are checked. The held-out stage constructs 16 root-specified cubics at each of 45 primes from 29 through 251, using seed 202610062106. Eight generated cases are singular; the other 712 curve cases supply 1,476 branch queries. Held-out cases are sampled, not claimed to be distinct within every prime.

All 23,736 branch queries agree with direct dense polynomial expansion and a separately evaluated coefficient functional. The validator also checks the global cleared differential identity, the high-part polynomial identity, direct point counts, the short-model coefficient transformation, and 1,972 unreduced integer polynomial expansions. Ordinary and supersingular coverage is explicit: 12,816 ordinary and 2,892 supersingular exhaustive branch-bearing cubics; 667 ordinary and 45 supersingular held-out curve cases. The structural trace route is checked on 527 of these curve cases and 1,181 branch queries; these overlap the main totals. Six invalid-input cases are rejected. The bridge’s 47 primes form a separate supplemental check, with no claim that they are disjoint from every main prime.

The final validation records are in results/validation.json and results/validation.csv. Runtime information and source hashes are retained. Validation elapsed time is labelled non-benchmark data. No new performance comparisons or speedup ratios are reported. An initial invalid-input test mistakenly used μ=2 as a nonroot of 1−w³ over F₇, although it is a root; that fixture was corrected to μ=3. This was a validator fixture error, not a formula counterexample.

Run `python validate.py` and `python third_boundary_bridge.py` from the package directory. The CLI example `python branch_evaluator.py 7 1 4 1 1 --roots 1` returns T=S=2. The Python API is `prepare(p, [1,c,b,a]).query(mu)`. It needs only Python’s standard library. Testing was on hosted Linux; no Windows execution is claimed. The API is platform-independent Python, but does not impose a practical runtime cap on its O(p) default preparation.

## Current status

| Claim | Status |
|---|---|
| General cubic branch formula and global normalization | Proved in this note by two algebraic arguments; unrefereed |
| Default complete evaluator | Implemented; finite checks passed |
| Ordinary j=0/j=1728 trace-only corollary | Proved by sparsity; trusted-trace implementation checked |
| General soft-square-root preparation | Established recurrence-method consequence; not a new implemented benchmark |
| General polylogarithmic K recovery | Unresolved |
| Fast rounded-third complete weighted sum | Unresolved; exact bridge (B6) recorded |
| Novelty of the branch corollary | Not claimed; closely follows Voloch’s existing identity |

## Verified references

Voloch, J. F. (1997). An analogue of the Weierstrass ζ-function in characteristic p. Acta Arithmetica, 79(1), 1–6. https://doi.org/10.4064/aa-79-1-1-6. The Section 2 lemma was read in the author manuscript https://www.math.canterbury.ac.nz/~f.voloch/Pdfs/zeta3.pdf; journal metadata were verified at the publisher. This note does not rely on its quasi-period/logarithmic-transfer sign.

Katz, N. M. On a question of Zannier. Experimental Mathematics. https://doi.org/10.1080/10586458.2018.1551818. Published author-hosted text https://web.math.princeton.edu/~nmk/zannier_publ.pdf; Section 1, Theorem 3.1 and the de Rham discussion were checked. The host text carries 2019 copyright/online publication information; final issue-date metadata were not independently resolved here.

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. SIAM Journal on Computing, 36(6), 1777–1806. https://doi.org/10.1137/S0097539704443793. Author-hosted published PDF https://specfun.inria.fr/bostan/publications/BoGaSc07.pdf; Section 6, Theorem 14 and the matrix-recurrence construction were checked.

Schoof, R. (1995). Counting points on elliptic curves over finite fields. Journal de Théorie des Nombres de Bordeaux, 7(1), 219–254. https://www.numdam.org/item/JTNB_1995__7_1_219_0/. The original article’s archive abstract explicitly states the deterministic polynomial-time point-counting result and separates practical Atkin–Elkies improvements. It supports the trace-setup consequence, not second-kind data recovery.
