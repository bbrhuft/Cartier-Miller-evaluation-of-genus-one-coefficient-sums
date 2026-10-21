# Cartier–Miller evaluation of rationally weighted quadratic-character sums and elliptic-point sums

Research report, 20 October 2026. Prepared for David Jordan's Cartier–Miller programme. Unrefereed and AI-assisted. Nothing was published and the manuscript was not modified.

---

## 0. Status, provenance and labelling

**Labels used throughout.** Every statement carries one of:

| Label | Meaning |
|---|---|
| **[I]** | Inherited from the manuscript (claims audited, not independently peer-reviewed). |
| **[P]** | Inherited from earlier, unrefereed project work in the repository (not in the manuscript). |
| **[N]** | Deduction proved in this investigation (proof given here; not specialist-reviewed). |
| **[C]** | Computational observation (finite evidence; supports implementation, never replaces proof). |
| **[U]** | Unresolved. |

**Inputs and versions.**

| Item | Identification |
|---|---|
| Manuscript source | Attached `Cartier_Miller_Paper_Reviewed_20261018.tex`, SHA-256 `7419bfc0…a24cb9`. Its revision line reads **19 October 2026**, and its text matches the repository PDF `Cartier_Miller_Paper_Revised_20261019.pdf` (SHA-256 `dbed70d6…464d5`), not the repository's 18 October PDF. The file name is therefore one day behind its content. |
| Brief | `MATHEMATICAL_BRIEF.md`, SHA-256 `9aebd8ab…ec6c0` |
| Supplied verifier | `verify_character_identities.py`, SHA-256 `4326a945…f0e9`; run unchanged |
| Inherited implementation | `bbrhuft/cartier-miller-evaluation-of-genus-one-coefficient-sums`, commit `ef2307929b54f69611073b666cb212eb641660d9` (2026-10-20 10:44 +0100), directory `Cartier-Miller-Integration-20261013/cm_system`; vendored unmodified. Entry point audited and exercised: `cm_system.rows.RowSession.query` (quadratic algebra `QuadCtx`, resumable split, `miller_alpha_resumable`/`miller_continue`, `Model.to_short`, κ = −2). |
| Prior project work used | `Cartier-Miller-Extensions-20261009/research/branch_point_20261006` (cubic branch formula "B1", 6 October 2026) and the rounded-third note (a_L = 3/(2G³)) |
| Frozen candidate | `FREEZE.json`, digest `4302b56426a6160fbc5027659632bac7ad6cc0ab755c5fcb00d8c9502aa99bd3`, frozen 2026-10-20T18:57:17Z (local clock; no external timestamp) |

---

## 1. Summary of findings

1. **Single pole, every μ ∈ F_p [N].** A single polynomial-division identity (Theorem A) gives Σ_{x≠μ} χ(f(x))/(x−μ) for *every* μ ∈ F_p and *every* f of degree ≤ 4. It specializes to the manuscript's Corollary 1.1 at nonzero nonbranch μ, to T_f(μ)/μ at branch values, and to −c_p − c_1 at μ = 0. This proves Corollary 1.1 independently, without Miller functions.
2. **Point sums carry no extra arithmetic [N].** With one common domain x ∉ U, the affine point sum equals the character sum plus Σ_{x∉U} R(x) = −Σ_k r_k. This term depends only on the poles and coefficients, not on the curve (Theorem C). The brief's candidate correction formulas are correct as stated.
3. **Constants and infinity [N].** Constant weights enter through the integer 1 − N∞ − τ − Σ ε(μ_k), reduced mod p. Projective sums are defined only when the weight is regular at infinity; then P^proj = P^aff + b·N∞. With a positive-degree polynomial part, the projective sum is left undefined (Proposition C2).
4. **Coordinate restrictions are removable [N].** f(0) = 0, f(0) ≠ 1 and a pole at 0 are coordinate restrictions. A deterministic translation from at most deg f + s + 1 candidates, then normalization, removes them at constant overhead per query. The trace transfers as τ_g = χ(f(a))·τ_f. The annihilator M and exceptional status are invariant (Proposition D). As a by-product, T_f(μ) is computable in the *original* coordinates for f(0) = 0, which the manuscript excludes (Corollary A2).
5. **Branch poles are a genuine obstruction, sharply located [N; cubic case P].** A closed form covers cubics and quartics alike (Theorem E). One additional scalar per curve, beyond the trace, is needed: c_{p−2} for cubics, c_{p−3} for quartics. For quartics, c_{p−2} is itself obtainable by one Miller query at the pole at infinity (Corollary E2). Given that scalar, each branch pole costs O(1) field operations. No polylogarithmic way to acquire it is known. On y² = 1 − x³/2 with p ≡ 5 (mod 6), the single branch-pole sum equals μ₀G⁻³ with G = ⌊p/3⌋! mod p. A fast branch evaluator would therefore yield that Gauss factorial, which the manuscript lists as open (Corollary E3).
6. **Bounded extensions [N].** Double poles and polynomial parts reduce, by an exactness operator, to Miller values, the trace, and the same single second-kind scalar (Propositions F1–F3). Extension-field poles satisfy an explicit identity but need T_f at an F_{p²} point; that is unsupported here (Proposition F4). A dual-number experiment shows the pointwise identity cannot be differentiated: jet derivatives of the inherited Miller chain matched the formal derivative in 3 of 242 cases (Remark F5).
7. **Complexity [N].** For s supplied nonbranch simple poles on a prepared curve, the cost is O(sn + s²) field multiplications and O(sn + s) inversions. In bit operations this is O(s·n·(M(n)+I(n)) + s²·M(n)): O(sn³ + s²n²) classically and O(s n M(n) log n + s² M(n)) with fast arithmetic. A subproduct-tree method lowers the correction cost to O(M_pol(s) log s) field multiplications (Section 9).
8. **Implementation audit [C].** The inherited `RowSession` agreed with FLINT truncations on all 78,030 admissible queries in development and confirmation, and on all 3,288 queries of the extended verifier (which also include λ = 0 and cubic-branch cases). These included 12,579 exceptional (trace ±1, M_χ = p) queries and 8,892 split-algebra fallbacks. It never divides by an annihilator. It discards the Miller endpoint, which would give a free necessary check on caller-supplied traces (Section 10).
9. **Evidence [C].** The supplied verifier passes unchanged. The development suite ran 208,272 checks with 0 failures. The frozen candidate was then confirmed on a disjoint, hash-seeded sample of 261,423 checks with 0 failures. All counts are exact; finite agreement is not proof.

---

## 2. Setting and conventions

Let p ≥ 7 be prime, n = ⌈log₂ p⌉, h = (p−1)/2, and χ the quadratic character with χ(0) = 0. Let f ∈ F_p[x] be squarefree of exact degree D ∈ {3, 4}. Write f = Σ f_i x^i, ℓ = f_D, F = f^h = Σ c_m x^m, T_f(x) = Σ_{m<p} c_m x^m, and H = c_{p−1}.

Put ε(x) = χ(f(x)), the integer ν(x) = #{y : y² = f(x)} = 1 + ε(x), and τ = p + 1 − #E(F_p), where E is the smooth projective model of y² = f(x). Unless an integer is explicitly named, every sum below is formed in F_p. Character values ±1 are interpreted in F_p.

The letter D has three meanings, each fixed by its section: deg f (here and in Sections 6, 8 and 9), the denominator Π(x − μ_j) of R = N/D (Proposition C3), and the manuscript's divisor (Q₊) − (Q₋) (Section 7).

**Field-valued weights versus multiplicative characters.** Two different problems are easily confused.

* **The problem studied here.** The sum Σ_{x∉U} χ(f(x))·R(x) is F_p-valued and linear in the weight R. It is a coefficient-type functional of f^h. Theorem A identifies it with truncated polynomial-power data, which Cartier–Miller evaluates.
* **A different problem.** The sum Σ_{x∉U} χ(R(x) f(x)) is an integer. For R = N/D one has χ(R f) = χ(N D f) wherever D ≠ 0, since χ(D⁻¹) = χ(D). The sum is therefore a point count on the different curve y² = N(x)D(x)f(x), and it is not linear in R. For a cubic f and R = 1/(x−μ), it equals 1 − N′∞ − τ′, where τ′ is the trace of the genus-one quartic y² = (x−μ)f(x) [N, C: verified in 28 cases]. The field-valued sum differed from the residue of this integer in 26 of those 28 cases [C]. The Cartier–Miller oracle says nothing about the multiplicative problem.

---

## 3. Admissibility classification

"Implemented" means routed by `cmcs.py` and verified against enumeration. The domain is always one common set x ∉ U.

| Term in R, location | Character sum | Point sum | Route | Extra data beyond τ | Status |
|---|---|---|---|---|---|
| a/(x−μ), μ ≠ 0, f(μ) ≠ 0, f(0) = 1 | Thm A + manuscript Thm 1 | Prop B / Thm C | inherited Miller oracle | none | implemented [I+N] |
| a/(x−μ), f(μ) ≠ 0, with μ = 0, f(0) = 0 or f(0) ≠ 1 | Prop D | Thm C (rebuild ν, do not scale by α) | translation + normalization + oracle | none (τ reused × α) | implemented; coordinate restriction only [N] |
| a/(x−μ), f(μ) = 0 (branch) | Thm E | ν(μ) = 1, ε(μ) = 0 | closed form | cubic c_{p−2}; quartic c_{p−3} (c_{p−2} via Miller at ∞) | implemented given data; acquisition O(p); genuine obstruction [N; cubic P] |
| c/(x−μ)², f(μ) ≠ 0 | Prop F2 | Thm C | oracle + second-kind data | as for branch | exploratory, implemented [N] |
| c/(x−μ)², f(μ) = 0; any order ≥ 3 | Prop F1 (reduction exists) | — | — | second-kind | unsupported (UnsupportedCase) |
| constant b | Prop C2 | Prop C2 | trace | none | implemented [N] |
| e·x, quartic (poles at ∞±, unramified) | Cor E2 | affine only | Miller on y² = x⁴f(1/x) at 0 | none | implemented [N] |
| e·x, cubic (∞ ramified) | Prop F3 | affine only | second-kind | c_{p−2} | implemented given data [N] |
| e·x², e·x³ | Prop F3 | affine only | second-kind | cubic c_{p−2}; quartic c_{p−3} | implemented given data [N] |
| polynomial degree ≥ 4 | Prop F1 | — | — | — | unsupported |
| poles in F_{p²} \ F_p | Prop F4 identity | — | would need T_f at an F_{p²} point | manuscript Prop 2 over extensions when p∤M | unsupported [U] |
| projective sum with nonconstant polynomial part | undefined (pole at ∞) | — | — | — | rejected |
| U ∪ roots(f) = F_p | 0 | Σ_{x∉U} R(x) | direct | none | implemented [N] |

---

## 4. One pole

**Lemma 1 (power sums) [I; classical].** Σ_{x∈F_p} x^k equals −1 if k > 0 and (p−1) | k, and 0 otherwise, with 0⁰ = 1. Hence for a polynomial P, Σ_x P(x) = −Σ_{j≥1} [x^{j(p−1)}]P.

**Theorem A (polynomial-division identity) [N].** Let f ∈ F_p[x] have degree ≤ 4 (squarefree not needed). For every μ ∈ F_p,

$$C_f(\mu):=\sum_{x\ne\mu}\frac{\chi(f(x))}{x-\mu}= -\sum_{m\ge p}c_m\,\mu^{m-p}\;-\;F'(\mu),$$

where F′ is the formal derivative of F = f^h.

*Proof.* For every x ∈ F_p, F(x) = f(x)^h = χ(f(x)) in F_p (Euler; this includes f(x) = 0). Put Q = (F − F(μ))/(x − μ) ∈ F_p[x]. Then deg Q ≤ 4h − 1 = 2p − 3 and Q(μ) = F′(μ). For x ≠ μ, ε(x)/(x−μ) = Q(x) + F(μ)/(x−μ). Since Σ_{x≠μ}(x−μ)⁻¹ = Σ_{t≠0} t⁻¹ = 0, we get C_f(μ) = Σ_x Q(x) − Q(μ). By Lemma 1 and deg Q < 2p−2, Σ_x Q(x) = −[x^{p−1}]Q. Expanding (x^m − μ^m)/(x−μ) = Σ_{j<m} x^j μ^{m−1−j} gives [x^{p−1}]Q = Σ_{m≥p} c_m μ^{m−p}. ∎

**Corollary A1 [N].**
1. **μ ≠ 0, f(μ) ≠ 0.** Since μ^p = μ, Σ_{m≥p} c_m μ^{m−p} = μ⁻¹(F(μ) − T_f(μ)) = (ε(μ) − T_f(μ))/μ. Also F′(μ) = h f^{h−1}f′ = −ε(μ)f′(μ)/(2f(μ)), using h ≡ −1/2. This gives the manuscript's identity: C_f(μ) = (T_f(μ) − ε(μ))/μ + ε(μ)f′(μ)/(2f(μ)). Substituting Theorem 1 gives Corollary 1.1 (5).
2. **μ ≠ 0, f(μ) = 0.** Here F′(μ) = h f(μ)^{h−1}f′(μ) = 0 because h − 1 ≥ 2, so C_f(μ) = T_f(μ)/μ. The sum is well defined; whether it is *fast* is Section 7.
3. **μ = 0.** C_f(0) = −c_p − c₁. The coefficient c_p is not supplied by the evaluator, so translation is used instead (Section 6).

**Corollary A2 (unnormalized coefficient sums) [N].** For squarefree f of degree 3 or 4 with *any* constant term, and μ ∈ F_p^× with f(μ) ≠ 0:

$$T_f(\mu)=\mu\,C_f(\mu)-\mu\,\varepsilon(\mu)\frac{f'(\mu)}{2f(\mu)}+\varepsilon(\mu).$$

Since C_f(μ) is computable through a translated model (Proposition D), so is T_f(μ) in the original coordinates. This covers f(0) = 0, which manuscript Corollary 4 excludes. There T_f(μ) = μ^h Σ_{k≤h} [x^k]g^h μ^k for f = xg, a midpoint truncation of g^h. This does not change the statement of Theorem 1, which is still proved in the (0,1)-origin coordinates. [C] 4,174 (development) and 6,062 (confirmation) such truncations agreed with FLINT.

**Proposition B (affine point sums, the missing fibre and the kernel sign) [N].** Let P_f(μ) = Σ_{P affine, x(P)≠μ} 1/(x(P) − μ). Then P_f(μ) = Σ_{x≠μ} ν(x)/(x−μ) = Σ_{x≠μ}(x−μ)⁻¹ + C_f(μ) = C_f(μ).

The omitted fibre over μ contains exactly ν(μ) ∈ {0, 1, 2} points: none, the branch point (μ, 0), or the two rational points (μ, ±y₀). All are excluded because the weight has a pole there. For μ ≠ 0, the geometric kernel satisfies 1/(1 − x/μ) = −μ/(x − μ), so Σ_{P, x≠μ} 1/(1 − λx(P)) = −μ·P_f(μ) with λ = 1/μ. Substituting into manuscript (50) gives (51) and Corollary 1.1 [C: every nonzero nonbranch query in the reference families].

**Remark B1 (general functions on E) [N].** Any rational function on E has the form A(x) + yB(x). Summed over points whose x-coordinate avoids U, the yB(x) part cancels fibre by fibre: the points (x, ±y) pair up, and points with y = 0 contribute 0. So elliptic-point sums of arbitrary functions with full-fibre exclusions reduce to the x-pullback case. Excluding a *single* point changes this by an explicit local term. For y₀² = f(μ) ≠ 0,

$$\sum_{P\ne(\mu,y_0)}\frac{y+y_0}{x-\mu}=y_0C_f(\mu)-\frac{f'(\mu)}{2y_0},$$

where the value at (μ, −y₀) is the regular limit [N; C: 1,550 checks].

---

## 5. Several poles on one common domain

Let U ⊂ F_p be finite with |U| = s. Let μ₁, …, μ_s ∈ U be distinct and a_j ∈ F_p, where a_j = 0 is allowed and simply excludes a point. Put R = Σ_j a_j/(x−μ_j) and r_k = Σ_{j≠k} a_j/(μ_k − μ_j).

**Theorem C [N; confirms the brief's candidates].**

$$C_R:=\sum_{x\notin U}\varepsilon(x)R(x)=\sum_j a_jC_f(\mu_j)-\sum_k\varepsilon(\mu_k)r_k,\qquad P_R:=\sum_{x\notin U}\nu(x)R(x)=\sum_j a_jC_f(\mu_j)-\sum_k\nu(\mu_k)r_k.$$

Consequently P_R − C_R = Σ_{x∉U} R(x) = −Σ_k r_k = −Σ_{j<k}(a_j − a_k)/(μ_k − μ_j).

*Proof.* Σ_{x∉U} ε(x)/(x−μ_j) = C_f(μ_j) − Σ_{k≠j} ε(μ_k)/(μ_k − μ_j), because the oracle omits only its own pole. Multiply by a_j, sum, and exchange the order: Σ_j a_j Σ_{k≠j} ε(μ_k)/(μ_k−μ_j) = Σ_k ε(μ_k) r_k. Replacing ε by ν = 1 + ε adds Σ_j a_j Σ_{x∉U}(x−μ_j)⁻¹ = −Σ_k r_k. ∎

**Mathematical content of the two formulations.** The difference P_R − C_R is a rational expression in (μ, a) alone, independent of f. Each formulation therefore determines the other in O(s²) field operations (or O(M_pol(s) log s), Proposition C3), and neither carries arithmetic information the other lacks. Conceptually, the x-pullback weight splits into a part invariant under the hyperelliptic involution (Σ R over the x-line, which is elementary) and an anti-invariant part (the character sum). The single-pole equality P_f = C_f is the special case where the elementary part vanishes. It does **not** extend: with equal coefficients the correction is zero, but in general it is not [C: 128 development and 58 confirmation multi-pole cases had P_R ≠ C_R].

**Reuse form [N].** C_R = Σ_j a_j K_j with K_j := Σ_{x∉U} ε(x)/(x−μ_j) = C_f(μ_j) − Σ_{k≠j} ε(μ_k)/(μ_k − μ_j). For a fixed (f, p, U), the vector (K_j) is prepared once. Each new coefficient vector then costs O(s) multiplications. Adding or removing one pole updates every K_j in O(s), plus one oracle call.

**Proposition C2 (constants, cubic versus quartic, infinity) [N].**
1. **Points at infinity.** N∞ = 1 for a cubic and N∞ = 1 + χ(ℓ) for a quartic. Over ∞ the quartic model has the two points (y/x²)² = ℓ, which are rational exactly when ℓ is a square.
2. **Integer identities.** #E(F_p) = N∞ + p + Σ_x ε(x). Hence Σ_x ε(x) = 1 − N∞ − τ, and the integer count of affine points with x ∉ U is p + 1 − τ − N∞ − Σ_{u∈U} ν(u).
3. **Constant term.** For R_b = b + R, C_{R_b} = C_R + b·(1 − N∞ − τ − Σ_U ε(u)) and P_{R_b} = P_R + b·(p + 1 − τ − N∞ − Σ_U ν(u)). The bracketed quantities are integers, and only their residues enter. In F_p the point term reads b(1 − N∞ − τ − Σ_U ν(u)).
4. **Projective sum.** x has a pole of order 2 at the cubic's point at infinity and of order 1 at each of the quartic's two. So every (x−μ)^{−k} vanishes there, and R_b∘x extends *regularly* with value b. This is a proof, not a convention. Define P^proj_{R_b} := Σ_{P∈E(F_p), x(P)∉U} R_b(x(P)) = P_{R_b} + b·N∞. If R has a polynomial part of positive degree, R∘x has a pole at every point at infinity, and no projective sum is defined. The code rejects such requests: 427 development and 191 confirmation routings [C].

**Proposition C3 (finite parts by derivatives) [N, with classical algorithms].** Let D = Π_j(x − μ_j) and N = Σ_j a_j D/(x−μ_j), so R = N/D. Then

$$r_k=\frac{N'(\mu_k)-a_k D''(\mu_k)/2}{D'(\mu_k)}.$$

*Proof.* Taylor-expand N and D at μ_k to second order; this is valid in F_p[x] because 2 < p. Near μ_k, R = a_k/t + N′/D′ − a_k D″/(2D′) + O(t), with t = x − μ_k. ∎

With a subproduct tree, D and N cost O(M_pol(s) log s). Multipoint evaluation of N′, D′, D″ at the s poles costs O(M_pol(s) log s) (von zur Gathen & Gerhard, 2013, Ch. 10). Batch inversion of the D′(μ_k) costs one inversion plus 3(s−1) multiplications (Montgomery, 1987). Hence all r_k, and all K_j, cost O(M_pol(s) log s) multiplications and one inversion; M_pol(s) = O(s log s log log s) over F_p (Cantor & Kaltofen, 1991). The identity is verified [C: 324 + 144 configurations], but only the quadratic algorithm is implemented. The fast route is a proved bound, not a tested implementation.

---

## 6. Coordinate changes, normalization and the cached trace

**Proposition D (translation, normalization and twist) [N; confirms the brief's candidate].** Let a ∈ F_p with f(a) ≠ 0. Put g(z) = f(a+z)/f(a) and α = χ(f(a)).

1. g(0) = 1, g is squarefree of the same degree, and its leading coefficient is ℓ/f(a).
2. ε_f(a+z) = α·ε_g(z) for every z. Hence C_f(μ) = α·C_g(μ − a) for every μ, and branch status is preserved.
3. **Trace transfer:** τ_g = α·τ_f as integers. For a cubic, τ = −Σε, so τ_g = −αΣε_f = ατ_f. For a quartic, N∞(g) = 1 + αχ(ℓ), so τ_g = −αχ(ℓ) − αΣε_f = α(−χ(ℓ) − Σε_f) = ατ_f. Geometrically, E_g is E_f translated and twisted by f(a).
4. **Invariance of M and exceptional status:** for nonbranch μ, χ_g(μ−a) = α·χ_f(μ). Hence M_g = p + 1 − χ_gτ_g = p + 1 − χ_f(μ)τ_f = M_f, and τ_g = χ_g ⇔ τ_f = χ_f(μ).
5. **Point sums must be rebuilt:** ν_f(a+z) = 1 + α·ε_g(z), so P_R(f) = C_R(f) + Σ_{x∉U} R(x), and the elementary second term is *not* multiplied by α. For a single pole that term vanishes, so P_f(μ) = α·P_g(μ − a) happens to hold; with several poles or a constant it fails. [C: 348 nonsquare translations in the translation family; rebuilt point sums verified in every weighted configuration routed through a translation, including the 669 + 275 configurations with a pole at 0.]

**Cached trace.** One exact τ per (p, f) serves every translation and normalization through τ_g = α τ_f. The two annihilators M_{±1} = p + 1 ∓ τ and their binary expansions are reusable too.

**Bounded deterministic search.** Among the residues 0, 1, …, D + s (that is, D + s + 1 candidates when D + s + 1 ≤ p), at most s lie in U and at most D are roots of f. So one is valid. The first valid one is taken, with a = 0 preferred, which is just normalization. A single pole needs at most D + 2 ≤ 6 candidates. If D + s + 1 > p, the whole field is scanned in O(p) = O(s) steps. The search fails only if U ∪ roots(f) = F_p. Then the domain consists of roots, C_R = 0, and P_R = Σ_{x∉U} R(x) is elementary [C: 48 + 24 degenerate routes].

**Obstruction or coordinate restriction?**

| Feature | Invariant under x ↦ a + cx? | Classification |
|---|---|---|
| f(0) ≠ 1, f(0) = 0, pole at 0 | no | coordinate restriction of the (0,1)-origin convention; removed at O(1) overhead |
| branch pole f(μ) = 0 | yes | genuine: second-kind requirement (Section 7) |
| pole order ≥ 2 | yes | genuine: second-kind requirement (Section 8) |
| polynomial part, cubic | yes (∞ is ramified) | genuine: second-kind |
| linear polynomial part, quartic | becomes a finite nonbranch pole under x ↦ 1/x | coordinate restriction (Corollary E2) |
| pole outside F_p | yes | outside the base-field method (Prop F4) |

---

## 7. Poles above branch values

**What fails in the inherited chain [N, by inspection of the proof and code].** At f(μ) = 0:

1. Q₊ = Q₋ = (μ, 0), so D = (Q₊) − (Q₋) = 0, Ψ_M(D) = 0 and r = 1/(λv₀) is undefined. Formula (4) degenerates to 0·∞.
2. θ_λ has a residue-free double pole at (μ, 0): it is a differential of the second kind. No logarithmic differential cancels it, so the residue step of Proposition 2 is empty. Its de Rham class has a component whose Cartier image is not determined by H.
3. χ = 0, so the Frobenius eigen-relation π(D) = χD gives nothing.

The inherited `RowSession` refuses rather than dividing. Cubic branch arguments go to a second-kind service with an O(p) recurrence [P]. Quartic branch arguments raise `Unsupported` [C: 151 + 10 + 44 + 65 such routings, all as specified]. Theorem A shows the sum itself remains well defined: C_f(μ) = T_f(μ)/μ.

**Theorem E (branch values, closed form) [N; the cubic case is the project's formula B1, P].** Let f = Σ_{i≤4} f_i x^i be squarefree of degree 3 or 4 (f₄ = 0 for a cubic), with any constant term, and let f(μ) = 0. Then

$$\sum_{x\ne\mu}\frac{\chi(f(x))}{x-\mu}=\frac{2}{f'(\mu)}\Big[\mu\big(f_4\mu+\tfrac{f_3}{2}\big)c_{p-1}-\tfrac{f_3}{2}\,c_{p-2}-f_4\,c_{p-3}\Big],\qquad T_f(\mu)=\mu\cdot(\text{this}).$$

*Proof.* Define the exactness operator Δ(S) = fS′ + ½f′S on F_p(x). Using fF′ = hf′F and 1 + h ≡ ½, one gets F·Δ(S) = (fFS)′ (∗).

Put q = f/(x−μ), so q(μ) = f′(μ) ≠ 0, and W = (f′/2 − q + f′(μ)/2)/(x−μ) ∈ F_p[x]. The numerator vanishes at μ. Then Δ(1/(x−μ)) = (f′/2 − q)/(x−μ) = −f′(μ)/(2(x−μ)) + W. So for x ≠ μ, 1/(x−μ) = (2/f′(μ))[W(x) − Δ(1/(x−μ))(x)].

Multiply by ε(x) = F(x) and sum over x ≠ μ. By (∗), the Δ-term becomes Σ_{x≠μ}(qF)′(x) = Σ_x(qF)′(x) − (qF)′(μ). Here (qF)′(μ) = 0, since F vanishes to order h ≥ 2 at μ. By Lemma 1, Σ_x(qF)′ = Σ_{j≥2}(j−1)[x^{j(p−1)+1}](qF) = [x^{2p−1}](qF), using [x^k]G′ = (k+1)[x^{k+1}]G and deg qF ≤ 2p+1. Also Σ_{x≠μ}εW = Σ_x FW = −[x^{p−1}](FW) − [x^{2p−2}](FW), since ε(μ) = 0.

For a cubic, W = (f₃/2)(x−μ) and every degree-2p term vanishes. For a quartic, W = (x−μ)(f₄(x+μ) + f₃/2). The top coefficients are c_{2p−2} = κ := χ(ℓ), c_{2p−3} = −κf₃/(2f₄), and c_{2p−4} = κ(−f₂/(2f₄) + 3f₃²/(8f₄²)), from (ℓ+…)^h with binomial(h,2) ≡ 3/8. Collecting, [x^{2p−2}](FW) + [x^{2p−1}](qF) = 2f₄c_{2p−4} + (3f₃/2 + f₄μ)c_{2p−3} + (f₂ + f₃μ/2)c_{2p−2}, and this equals 0. The remaining term −[x^{p−1}](FW) gives the display. ∎

For a cubic the formula reads T_f(μ) = f₃μ(μH − c_{p−2})/f′(μ), which is the project's (B1). That note gives a differential proof and a Voloch-style polynomial proof; the proof above is a third, elementary route that also covers quartics. [C: 213 + 87 branch poles through the candidate code; 97 checks of the closed form; 114 + 27 + 51 cubic branch queries through the inherited service.]

**Corollary E2 (quartics: c_{p−2} by one Miller query at infinity) [N].** For a quartic, Σ_x ε(x)·x = −(c_{p−2} + c_{2p−3}). Under u = 1/x, y′ = u²y, this sum equals C_{f*}(0) with f*(u) = u⁴f(1/u) and f*(0) = ℓ ≠ 0. So it is a *nonbranch* single pole on an isomorphic model with the same trace. Hence c_{p−2} = −C_{f*}(0) + χ(ℓ)f₃/(2ℓ), and for quartics the only scalar not reachable by Miller is c_{p−3} [C: 324 + 144 checks, no second-kind data used].

**Preparation and query cost [N].** Given the second-kind scalar, a branch pole costs O(1) field operations including one inversion. The scalar is acquired by a streaming scaled recurrence in O(p) field operations, O(1) working elements and three final inversions; this is implemented, and its output is checked against c_{p−1} ≡ τ and Σ_j j f_j c_{p−j} = 0. Bostan–Gaudry–Schost recurrence evaluation gives Õ(√p) [P; not implemented here]. Branch status is coordinate-invariant, so translation cannot help. In the ordinary j = 0 and j = 1728 congruence families the second-kind coefficient vanishes in the short model, so the trace alone suffices there [P].

**Corollary E3 (rounded-third reduction) [N, combining I and P].** Let p ≡ 5 (mod 6), f = 1 − x³/2, μ₀ = 2^{(2p−1)/3} (the unique cube root of 2), m = (p−2)/3 and G = m! mod p. Then

$$\sum_{x\ne\mu_0}\frac{\chi(1-x^3/2)}{x-\mu_0}=\mu_0G^{-3},\qquad T_f(\mu_0)=\mu_0^2G^{-3}=(-1)^m\binom{(p-3)/2}{m}.$$

*Proof.* In Theorem E, take H = 0 [I], f₃ = −1/2, f′(μ₀) = −3μ₀²/2, and c_{p−2} = c_{3m} = a_m = −6G⁻³ (manuscript proof of (43) [I]). Then use μ₀³ = 2. The binomial form is T_f(μ₀) = Σ_{i≤m} (h choose i)(−1)^i = (−1)^m (h−1 choose m). ∎

Consequently, any algorithm returning this single branch-pole character sum in time t yields G = (μ₀/C)^{(2p−1)/3} in t + O(log p) field operations, and conversely. The manuscript records polylogarithmic acquisition of G as open. A uniform fast branch evaluator would therefore settle it. This is a reduction, not a lower bound [C: 220 + 150 primes, binomial identity; 220 direct character sums].

**Status [U].** What remains unsupported is a polylogarithmic acquisition of the per-curve second-kind scalar c_{p−2} (cubic) or c_{p−3} (quartic) for general curves.

---

## 8. Bounded exploratory extensions

**Proposition F1 (structure of all base-field-pole weights) [N].** Let R ∈ F_p(x) have all poles in U ⊂ F_p. Then Σ_{x∉U} ε(x)Δ(S)(x) = Σ_{x∉U}(fFS)′(x) for every S with poles in U, by (∗). This sum is *elementary*: it is determined by finitely many Taylor coefficients of F at points of U, computable from χ(f(u)) and the Taylor expansion of f, and by finitely many top coefficients of F. Three reduction moves apply:

1. **Order-k pole at a nonbranch μ.** Δ((x−μ)^{1−k}) has leading part −(k−1)f(μ)(x−μ)^{−k}, which is invertible for 2 ≤ k < p+1.
2. **Order-k pole at a branch μ.** Δ((x−μ)^{−k}) has leading part f′(μ)(1/2 − k)(x−μ)^{−k}, invertible for 2k ≢ 1 (mod p).
3. **Polynomial part.** Δ(x^j) has degree j + D − 1 and leading coefficient ℓ(j + D/2).

Hence, for pole orders and degrees well below p, Σ_{x∉U} εR = Σ_{nonbranch μ} γ_μ·(simple-pole oracle values) + e₀Σε + e₁Σεx + e₂Σεx² + (elementary), with e₂ = 0 for cubics. Σεx is Miller-accessible for quartics (Corollary E2). So **exactly one second-kind scalar per curve is needed beyond the trace and Miller values**: c_{p−2} for cubics, c_{p−3} for quartics. This matches the dimension of H¹_dR(E) and the project's description of κ = β/H as a single Frobenius entry [P].

**Proposition F2 (double pole, nonbranch μ) [N].** With d = f(μ), e = ε(μ), P₁ = (f′ − f′(μ))/(x−μ), P₂ = (f − d − f′(μ)(x−μ))/(x−μ)², P = P₁/2 − P₂, and K₀ = (f^{h+1} − ed)/(x−μ):

$$\sum_{x\ne\mu}\frac{\varepsilon(x)}{(x-\mu)^2}=\frac1d\Big[K_0'(\mu)-[x^{2p-1}]K_0-\tfrac{f'(\mu)}{2}C_f(\mu)+\sum_{x}\varepsilon P-eP(\mu)\Big],$$

where K₀′(μ) = (e/4)(f″(μ) − f′(μ)²/(2d)), [x^{2p−1}]K₀ = 0 for cubics, and Σ_x εP = −Σ_j [x^{j(p−1)}](FP). Requirements: one oracle value plus the second-kind data of Proposition F1. Cost after preparation: O(n) [C: 6,281 exhaustive checks; also inside the weighted-sum families].

**Proposition F3 (polynomial parts) [N].** Σ_x εx^k = −Σ_{j≥1} c_{j(p−1)−k}.

* **Cubic.** Σεx = −c_{p−2}; c_{p−3} = −(f₁H + 2f₂c_{p−2})/(3f₃) from the m = p recurrence identity Σ_j j f_j c_{p−j} = 0; c_{p−4} follows from the m = p − 1 recurrence. So degrees ≤ 3 need only c_{p−2}.
* **Quartic.** Degree 1 is Miller-accessible; degrees 2 and 3 need c_{p−3} (c_{p−4} = −(f₁H + 2f₂c_{p−2} + 3f₃c_{p−3})/(4f₄)).

[C: 126 checks plus the weighted families.] Projective sums with these terms are undefined (Proposition C2).

**Proposition F4 (extension-field poles) [N; evaluation U].** For μ ∈ F_{p²} \ F_p, Σ_{x∈F_p}(x−μ)⁻¹ = 1/(μ^p − μ), because Π_x(t − x) = t^p − t. The proof of Theorem A then gives

$$\sum_{x\in\mathbb F_p}\frac{\varepsilon(x)}{x-\mu}=\frac{F(\mu)}{\mu^p-\mu}-\mu^{-p}\big(F(\mu)-T_f(\mu)\big),\qquad T_f(\mu)=\sum_{m<p}c_m\mu^m\in\mathbb F_{p^2}.$$

[C: 120 + 48 checks.] Evaluation thus needs T_f(μ) = μ^{p−1}S_f(1/μ) at an F_{p²} argument. The manuscript's extension-field Proposition 2 gives S_f there only when p ∤ M = p² + 1 − e₂τ₂, and the base-field simplification does not apply. This route is not implemented or validated; the code rejects irreducible quadratic denominators explicitly [C: 43 + 16 routings].

**Remark F5 (why the pointwise identity cannot be differentiated) [N; C].** Theorem 1 holds at base-field λ because D is torsion with a Frobenius eigenvalue. For a transcendental λ the point Q₊ − Q₋ is a nonconstant point of a constant curve and has infinite order, so no annihilator M exists and there is no rational-function identity in λ to differentiate.

The double-pole formula is instead derived from the polynomial identity (∗). As a concrete check, the *inherited* `Model.to_short` and `miller_alpha` were run unchanged over F_p[e]/(e²)[s]/(s² − f(μ+e)) with M fixed. On 242 completed queries the e⁰ part reproduced T_f(μ) every time, but the e¹ part equalled the formal derivative T_f′(μ) only 3 times, about the 1/p chance rate. Another 260 attempts broke down because the deformed point leaves the torsion locus: a vertical step at e⁰ becomes a non-invertible e-difference. Local jet propagation through Miller arithmetic therefore does not compute global coefficients.

---

## 9. Complexity

**Cost model.** M(n) is the bit cost of n-bit integer multiplication: O(n²) classically, O(n log n) by Harvey and van der Hoeven (2021). A field multiplication costs O(M(n)), including reduction. I(n) is the bit cost of one inversion mod p: O(n²) by the classical extended Euclid algorithm, O(M(n) log n) by half-gcd (von zur Gathen & Gerhard, 2013, Ch. 11). **Inversions are counted separately and are not "field operations" in the multiplication count.** Exponentiation costs O(n) multiplications. M_pol(s) is the number of field operations to multiply degree-s polynomials over F_p.

**Theorem G (one prepared nonbranch query) [N; audits the I claim].** With τ, N∞ and the translated model cached, one single-pole value costs O(n) field multiplications and O(n) inversions:

* χ by Euler's criterion: ≤ 2n multiplications.
* The Miller chain: ⌊log₂ M⌋ ≤ n + 1 doublings and ≤ n + 1 additions, each with ≤ 1 algebra inversion (one F_p inversion plus O(1) multiplications for the norm) and O(1) algebra multiplications.
* At most one split, after which two F_p chains resume from the saved state, at most doubling the remaining cost.
* O(1) for the bridge to C_f.

Bit cost: O(n·M(n) + n·I(n)) = O(n³) classical, O(n M(n) log n) = O(n² log² n) fast. Working space: O(1) field elements, plus the O(n)-symbol operation list that the inherited code materializes. Projective coordinates would remove the per-step inversions; that is not implemented or claimed.

**Theorem H (s supplied simple nonbranch poles) [N].** The straightforward algorithm costs O(sn + s²) field multiplications and O(sn + s) inversions. The bit cost is O(s n (M(n) + I(n)) + s² M(n)), that is, O(sn³ + s²n²) classically and O(s n M(n) log n + s² M(n)) fast. For fixed s this is O(n) field multiplications, O(n³) classical and Õ(n²) fast bits. This refines the brief's O((sn + s²)(M + I)): the quadratic correction needs only s inversions after batching.

| Component | Field mults | Inversions | Bits (classical / fast) | Working space | Reusable when |
|---|---|---|---|---|---|
| Trace τ (deterministic Schoof) | — | — | O(n⁹) as stated in Schoof (1985); O(n⁸) in Schoof's 1995 survey; neither is claimed best | poly(n) | per (p, curve up to twist) |
| Curve preparation: primality (fixed-base Miller–Rabin, p < 2⁶⁴), squarefreeness, N∞, model per translation | O(n) | O(1) | O(n³) / O(n M(n) + I(n)) | O(1) | per (p, f, a) |
| Input reading and reduction (s pairs + b) | — | — | Θ(sn) | O(s) elements | per query |
| Pole distinctness | — | — | O(n s log s) by sorting (hashing in code, expected O(sn)) | O(s) | per U |
| Branch classification | O(s) | 0 | O(s M(n)) | O(1) | per U |
| Translation search | O(1) evaluations, O(s) comparisons | 1 (normalization) | O(sn + I(n)) | O(s) marks | while a ∉ U |
| s oracle calls | O(sn) | O(sn) | O(s n M(n) + s n I(n)) | O(1) each | per pole (cache C_f(μ)) |
| Exclusion corrections, straightforward | O(s²) | s | O(s² M(n) + s I(n)) | O(s) | per U |
| Exclusion corrections, subproduct tree | O(M_pol(s) log s) | 1 | O(M_pol(s) log s · M(n) + I(n)) | O(s log s) | per U |
| Constant term and output | O(s) | 0 | O(s M(n)) | O(1) | — |
| Optional partial fractions, roots supplied | O(s²) or O(M_pol(s) log s) | 1 | — | O(s) | per R |
| Root finding for an unfactored denominator | excluded (randomized polynomial time is standard; deterministic is not claimed) | | | | |
| Second-kind scalar (branch, double poles, cubic polynomial parts) | O(p) = O(2ⁿ) | 3 | O(p M(n)) | O(1) | per (p, f, coordinates) |

**Lockstep remark [N, not implemented].** The s Miller chains with the same M_χ share one operation sequence. Running them in lockstep and batching each step's inversions gives O(sn) multiplications and only O(n) inversions, or O(s n M(n) + n I(n)) bits.

**Many queries on a fixed curve [N].**

| Change between queries | Reusable | Recomputed |
|---|---|---|
| coefficients a_j only | τ, models, C_f(μ_j), ε(μ_j), K_j | one dot product: O(s) |
| one pole added or removed | the above; K_j updated in O(s) | one oracle call (switch translation if a ∈ U) |
| new pole set | τ, models | s oracle calls + corrections |
| f replaced by a translate or scalar multiple | τ via ×α | models |
| any other f | — | trace, models, second-kind data |
| prime p | — | everything |

For growing s, input reading Θ(sn) and the s oracle calls dominate unless s ≫ n, in which case the corrections dominate (straightforward) or O(M_pol(s) log s) does (fast). The case s ≥ p − D − 1 is degenerate and handled directly in O(p) = O(s).

---

## 10. Audit of the inherited implementation

All findings refer to commit `ef23079`, `Cartier-Miller-Integration-20261013/cm_system`.

1. **Agreement [C].** `RowSession.query` matched FLINT truncations on every λ tested: 32,998 + 8,673 (development), 35,471 + 888 (confirmation) and 3,288 (extended verifier). This included 4,696 + 1,259 + 6,311 + 154 + 159 exceptional queries, split over trace +1 and −1, and 3,947 + 1,099 + 3,321 + 68 + 457 split-algebra fallbacks.
2. **Intermediate identity and vertical steps.** Replaying the chain with the inherited `_add` found 6,425 + 483 + 1,995 + 4 chains with a step whose input was the identity, and 17,561 + 1,687 + 8,074 + 20 chains with a step whose result was O (a vertical line, or O + O). All of these queries were correct. The evaluation point is O, and (32) fixes every line function's local behaviour there. No line-function zero or pole collision arises beyond these identity and vertical conventions.
3. **Split algebra.** A zero-divisor witness is taken from inv(x₂−x₁), from 2y₁ or from y₁−y₂. The state *before* the failed operation is saved and resumed in both F_p components, as Algorithm 1 specifies. At most one split occurs per query.
4. **No division by an annihilator.** S = H − χ·rψ, and only κ, λ and the witness coordinate are inverted. M = p never causes a division (code inspection plus exceptional coverage).
5. **Traces are trusted.** Only |τ| ≤ 2√p is checked. The chain's endpoint [M]R₊ is computed and then discarded (`alpha, _ = …`). Checking that the endpoint is conjugation-invariant is free and necessary but not sufficient. A separate endpoint check detected every wrong trace in 162 + 72 + 12 + 12 trials (629 of 648 and 287 of 288 individual queries). **Recommendation:** return or assert the endpoint in `RowSession.query`.
6. **Branch routing.** Cubic branch arguments go to the inherited second-kind service, with an O(p) recurrence under a 500,000-term budget plus CM-table shortcuts. Quartic branch arguments raise `Unsupported`. Theorem E supplies the quartic closed form.
7. **Domain.** `RowSession` requires f(0) = 1 and λ ≠ ∞, i.e. μ ≠ 0. The translation layer in `cmcs.py` removes both restrictions.

---

## 11. Computational evidence

**Commands, run from the package root.**

```
python3 supplied/verify_character_identities.py      # supplied, unchanged
python3 src/verify_character_identities_extended.py  # same 132 models + p = 101 example, extended
python3 src/develop.py                                # development (seed 20261020)
python3 src/freeze.py                                 # writes FREEZE.json (refuses to overwrite)
python3 src/confirm.py                                # re-verifies hashes, hash-seeded disjoint sample
python3 src/exploratory_jets_and_closed_forms.py     # post-freeze exploratory checks
```

**Environment.** CPython 3.13.16 on Linux 6.18.44 (x86_64, glibc 2.39); Intel Xeon @ 2.10 GHz, 2 cores; numpy 2.5.3; python-flint 0.9.0 (FLINT); cypari2 2.2.4 (PARI 2.17.2). The candidate `cmcs.py` itself needs only the standard library and the vendored `cm_system`.

**Ground truth.** Three independent mechanisms supply the ground truth:

* character values from a table of squares, and fibres by counting actual y, not by Euler's criterion;
* FLINT powers f^h;
* PARI traces, via `hyperellcharpoly` for p < 5000 and otherwise ellap on the invariant Jacobian Y² = X³ − 27IX − 27J (Stoll & Cremona, 2002). For p < 5000 every call cross-checks the two PARI routes, and the families compare them with direct point counts wherever p allows enumeration.

**Supplied verifier.** PASS: 132 models plus the p = 101 example (character sum 48 at μ = 2); 4 models of trace +1 and 14 of trace −1. *Review notes:* it checks reference identities only. Its multi-pole checks use brute-force single-pole values, not the evaluator. It never tests μ = 0 beyond the point/character equality, never tests f(0) ≠ 1, never puts branch poles among several poles, and never touches Miller code.

**Extended verifier (same models).** PASS: 3,288 inherited queries (159 exceptional, 457 splits, 51 cubic-branch services, 65 quartic-branch `Unsupported`), 3,353 candidate single poles, 2,394 normalization changes and 2,394 multi-pole sums (affine, projective and character).

**Development (seed 20261020).** 208,272 checks, 0 failures, 211.8 s. Primes: all 42 primes 7–199; eleven medium primes (211 … 4999); 10007, 100003 and 1000003; four large primes up to 2⁶¹ − 1 and 10¹⁸ + 9; and, for the reference-only rounded-third family, all primes p ≡ 5 (mod 6) below 3000.

**Confirmation (frozen digest `4302b564…99bd3`, seed 4828621192244368911).** 261,423 checks, 0 failures, 519.4 s. Primes, all disjoint from development:

* 227, 239, 251, 263, 271, 281, 311, 347, 367, 419, 433, 491, 521, 541, 547, 569;
* 607, 2647, 2689, 2857, 3389, 4139, 4519, 4967;
* 911087, 728681, 5314391 (enumeration and FLINT ground truth);
* 717754976387, 952110247849697, 661479507218101589, 8984630942399791949 (internal consistency only);
* 150 primes p ≡ 5 (mod 6) in [3000, 40000).

| Family | Development checks | Confirmation checks | Selected counters (dev / conf) |
|---|---|---|---|
| Reference identities (Thm A, (50), (51), kernel sign, all μ) | 100,665 + 570 | 145,707 | nonbranch 16,515 / 24,193; branch 181 / 55; μ = 0 172 / 64 |
| Constants and infinity (integer vs residue) | 1,458 | 648 | P_R ≠ C_R 128 / 58 |
| Translation and twist (τ_g = ατ_f, M invariance) | 5,326 | 2,102 | nonsquare translations 247 / 101 |
| Extension poles; multiplicative contrast | 140 | 56 | field ≠ multiplicative residue 18 / 8 |
| Multipoint finite-part identity | 324 | 144 | — |
| Rounded-third reduction | 660 | 300 | primes 220 / 150 |
| Inherited RowSession (small + medium p) | 33,597 + 8,755 | 35,636 + 925 | exceptional 5,955 / 6,465; splits 5,046 / 3,389; trace ±1 curves 124 / 46 |
| Candidate single pole and truncation | 50,563 | 72,913 | oracle calls 49,836 / 72,627; f(0) = 0 truncations 4,174 / 6,062 |
| Candidate weighted sums | 4,595 | 2,041 | several poles 1,410 / 611; branch 560 / 206; pole 0 669 / 275 |
| Quartic pole at infinity | 324 | 144 | — |
| Degenerate and large-s domains | 96 | 48 | degenerate routes 48 / 24 |
| Trace endpoint check | 648 | 288 | wrong traces detected 162/162 / 72/72 |
| Partial-fraction route | 122 | 40 | extension poles routed 43 / 16 |
| Invalid and unsupported inputs | 30 | 30 | all 30 cases raised the specified exception |
| Medium-prime ground truth | 147 | 149 | p up to 1,000,003 / 5,314,391 |
| Large-prime internal consistency | 252 | 252 | splits at 40–63-bit primes 31 / 50 |

**Invalid inputs exercised.** Each of the following raised the exception class specified for it:

* composite p, p < 7, p ≥ 2⁶⁴, boolean p;
* degree 2 or 5, leading coefficient ≡ 0, non-squarefree f, float coefficients;
* trace outside the Hasse bound, non-integer trace, missing trace over budget;
* negative, out-of-range or boolean poles; repeated poles; non-integer weights; an unknown sum kind;
* a branch pole, a cubic linear part or a double pole without second-kind data;
* polynomial degree 4; a double pole at a branch value; a projective sum with a polynomial part;
* an extension-field denominator;
* inconsistent supplied second-kind data, and second-kind data contradicting τ;
* T_f(0) requested through the bridge; a quartic branch in the inherited RowSession; second-kind preparation over budget.

**Post-freeze exploratory checks.** These use their own seeds and primes up to 400, overlapping both earlier ranges, so they are not part of the confirmation:

* Theorem E closed form: 97/97;
* double poles: 6,281/6,281;
* polynomial parts: 126/126 (21 quartic-linear via Miller);
* single-point exclusion: 1,550/1,550;
* jets: 242 completed, values 242/242, derivatives 3/242, 260 degenerate;
* the caller-supplied second-kind path, including the derived c_{p−4}: 1,416/1,416. Neither suite had exercised this path with correct data before the freeze.

Raw machine-readable outputs are in `results/`.

---

## 12. Limitations

* **Finite checks.** All agreement is finite and computed in Python. Above about 5·10⁶ only internal consistency was checked: translation and twist invariance with independent PARI traces, and endpoints. No timings are claimed; matched benchmarks are a separate investigation.
* **Single author.** Development and confirmation were run by the same AI author. The freeze digest seeds the sample, but there is no external timestamp. None of this is human peer review.
* **Inherited proofs.** Theorem 1 and the exceptional normalization (Lemma 3) are inherited and were audited computationally, not re-proved. Every [N] proof here awaits specialist review.
* **Untested bounds.** The subproduct-tree, lockstep and BGS bounds are proved or inherited but not implemented. The endpoint check is necessary, not sufficient.
* **Coverage gaps.** Exceptional queries in the confirmation's candidate single-pole family happened to be 0. Exceptional coverage there comes from the inherited family (6,465) and the weighted family (54).
* **No novelty audit.** No claim of being first or best is made. Related constructions include Kedlaya-type reduction of differentials modulo exact forms, which the operator Δ resembles (Kedlaya, 2001); Cartier coefficient selection [I]; and the project's B1 note [P].

---

## 13. What belongs in the Cartier–Miller paper

**Recommended for an application section (about two pages; draft in `PROPOSED_APPLICATION_SECTION.tex`):**

* Theorem A, which subsumes (50)–(51) and covers branch values and μ = 0;
* Theorem C, with the P − C identity;
* Proposition C2 (constants and infinity, affine versus projective);
* Proposition D (translation and twist), extending Corollary 4 to f(0) = 0 and μ = 0, with Corollary A2;
* Theorem H's prepared-query bound.

**Recommended for the scope section:**

* Theorem E, replacing "the current division-free streaming fallback takes O(p)" with the precise requirement of one second-kind coefficient per curve, for cubics and quartics;
* Corollary E3, as a sharp illustration that links branch poles to the open rounded-third factorial;
* a one-line remark on the free endpoint check in Section "Computing the logarithmic derivative".

**Better kept outside the paper,** in an extension note or under Further questions: Propositions F1–F4, the double-pole formula, the multipoint and lockstep refinements, and the jet experiment.

---

## 14. Unresolved questions [U]

1. Is there a polylogarithmic acquisition of the second-kind scalar for any family beyond β = 0 [P]? Corollary E3 shows it would solve the rounded-third Gauss-factorial problem in one instance.
2. Extension-field poles: implement and validate S_f at F_{p²} arguments through manuscript Proposition 2 when p ∤ M, and treat the exceptional extension case.
3. A full implementation of Proposition F1 for arbitrary pole orders, including the elementary terms at branch points.
4. Whether lockstep batching or projective coordinates measurably change performance; this belongs to the separate benchmark study.

---

## References

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793

Cantor, D. G., & Kaltofen, E. (1991). On fast multiplication of polynomials over arbitrary algebras. *Acta Informatica, 28*(7), 693–701. https://doi.org/10.1007/BF01178683

Cremona, J. E. (2001). Classical invariants and 2-descent on elliptic curves. *Journal of Symbolic Computation, 31*(1–2), 71–87. https://doi.org/10.1006/jsco.1998.1004

Harvey, D., & van der Hoeven, J. (2021). Integer multiplication in time O(n log n). *Annals of Mathematics, 193*(2), 563–617. https://doi.org/10.4007/annals.2021.193.2.4

Jordan, D. (2026). *Cartier–Miller evaluation of genus-one coefficient sums* (Revision 19 October 2026) [Unrefereed manuscript]. Source file attached as `Cartier_Miller_Paper_Reviewed_20261018.tex`.

Jordan, D. (2026, October 6). *Cubic branch-point evaluation through second-kind Cartier data* [Unrefereed project note]. Repository path `Cartier-Miller-Extensions-20261009/research/branch_point_20261006`.

Kedlaya, K. S. (2001). Counting points on hyperelliptic curves using Monsky–Washnitzer cohomology. *Journal of the Ramanujan Mathematical Society, 16*(4), 323–338.

Montgomery, P. L. (1987). Speeding the Pollard and elliptic curve methods of factorization. *Mathematics of Computation, 48*(177), 243–264. https://doi.org/10.1090/S0025-5718-1987-0866113-7

Schoof, R. (1985). Elliptic curves over finite fields and the computation of square roots mod p. *Mathematics of Computation, 44*(170), 483–494. https://doi.org/10.1090/S0025-5718-1985-0777280-6

Schoof, R. (1995). Counting points on elliptic curves over finite fields. *Journal de Théorie des Nombres de Bordeaux, 7*(1), 219–254. https://doi.org/10.5802/jtnb.142

Stoll, M., & Cremona, J. E. (2002). Minimal models for 2-coverings of elliptic curves. *LMS Journal of Computation and Mathematics, 5*, 220–243. https://doi.org/10.1112/S1461157000000760

von zur Gathen, J., & Gerhard, J. (2013). *Modern computer algebra* (3rd ed.). Cambridge University Press. https://doi.org/10.1017/CBO9781139856065

The manuscript's own references (Cartier, 1957; Serre, 1958; Semaev, 1998; Voloch, 1997; Katz, n.d.; Della Dora et al., 1985) are relied on through the inherited results and are not repeated here.
