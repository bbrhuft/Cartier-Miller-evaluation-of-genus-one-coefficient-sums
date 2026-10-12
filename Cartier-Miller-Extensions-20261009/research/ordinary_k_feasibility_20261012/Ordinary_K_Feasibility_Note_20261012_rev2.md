# Ordinary Cartier slope from canonical-lift data: normalization, an integral comparison lemma, and the limits of the constructions examined

**Feasibility note, revision 2, 12 October 2026.** For David Jordan's Cartier–Miller extension programme.

This is an AI-assisted research note. It has not been refereed. It revises the first version of the same date after an independent review. Revision 1 worked from a description of that review; revision 2 incorporates the review document itself (`Ordinary_K_Feasibility_Review_20261012.md`) and its evidence ZIP, both preserved under `evidence/review_20261012/`. Revisions 0 and 1 are preserved unchanged in `evidence/`, and `CHANGES.md` lists every review statement with its resolution. The published manuscript, the completed CM extensions and the historical precision-two branch are untouched. Nothing was published and no repository was inspected or changed. Every numerical statement is observed output of the scripts in this package; §9 states which run family each number comes from.

Statements are labelled by kind. **Classical** means an established result used as input, with its verification status in §8. **Derived here** means a proof given in this note. **Executed** means a finite computation that was run. **Heuristic** means an unproved expectation. **Route-specific** means a limitation of one named construction, not of the problem.

## 0. Outcome

The defensible computational conclusion is narrow. The concrete constructions examined here did not yield a cheaper complete algorithm for κ = β/H. Whether canonical-lift or Serre–Tate data could give a shortcut by some other construction remains unresolved. Nothing here is a lower bound, nothing shows that a scalar equivalent to κ is hard to compute, and no generic speed-up or novelty is claimed.

In the assignment's terms, the outcome is a **conditional/oracle reduction** together with **route-specific obstructions** that apply only to the constructions named in §§6–7. With E supplied, κ is already mathematically determined, so every question here is computational. Several audited constructions build a large object, such as a full kernel polynomial or a whole torsion orbit. That does not show that the one scalar they contain cannot be computed without building it.

Two exact statements are derived here. The first (Theorem A) is that, in the low-pole basis with the column convention, the Frobenius matrix modulo p is [[0, −β],[0, H]]. So the handover's checkpoint κ = −b₀/d₀ holds with b₀ = −β and d₀ = H, and precision p suffices. The second (Lemma B) is an integral comparison for an arbitrary ordinary short Weierstrass lift Ẽ/Z_p. If σ_C is the sum of x-coordinates over the nonzero points of the canonical subgroup C of Ẽ, then σ_C ∈ pZ_p and κ ≡ σ_C/p (mod p). The automorphism, and in particular the sign, by which the chosen quotient identification reduces to Frobenius cancels in this ratio. Lemma B is proved from the classical inputs listed in §3.7, each with its verification status. As the review recommends, its integral-model and comparison steps should have specialist review before it is presented as a fully reviewed theorem.

Three further recovery formulas are derived and executed: Proposition C at the canonical lift, Proposition D on the étale side (β = −Σ_{E(F_p)} x and κ = −σ_V/t²), and Proposition E (β = ϑH with ϑ = 6B∂_A − (4/3)A²∂_B). Each one recovers κ from a scalar that is equivalent to κ once t is known. That equivalence is a statement about information, not about difficulty.

A separate, specific result is that at j = 0 and j = 1728 the coarse invariant j mod p² does not distinguish non-isomorphic lifts mod p². This is about those two values only. It says nothing about the generic computational question.

## 1. Input contract and conventions

The input is a certified prime p ≥ 7, a nonsingular short model E: y² = F(x) = x³+Ax+B over F_p, and its certified signed trace t with p ∤ t. Put h = (p−1)/2, H = [x^{p−1}]F^h = t mod p, β = [x^{p−2}]F^h and κ = β/H. The basis is ω = dx/y, η = x dx/y. These are read as classes in H¹_dR(E/F_p) through the low-pole Čech–de Rham convention: on the cover U₁ = E∖O, U₂ = E∖{y = 0}, [η] is the cocycle (η, η − dg; g) with primitive g = 2x²/y of pole order one at O. Pullbacks are written in the column convention f\*(ω₂,η₂) = (ω₁,η₁)M_f, so M_{f∘g} = M_g M_f. Over F_p the absolute Frobenius of E is the F_p-Frobenius endomorphism π, because E^{(p)} = E. The scaling isomorphism (x′,y′) ↦ (x′/u², y′/u³) from (u⁴A, u⁶B) to (A,B) has matrix diag(u, u⁻¹) (extension note, Lemma 2). Under (A,B) ↦ (d²A, d³B), κ ↦ dκ.

Field operations are counted in F_p or Z/p^N. Bit costs multiply by M(log p), or by M(N log p) at precision N. Extension degree k means work in F_{p^k}, whose operations cost Õ(k) F_p-operations.

## 2. Theorem A: the Frobenius matrix modulo p (derived here)

**Theorem A.** Let p ≥ 7 and let E: y² = x³+Ax+B be nonsingular over F_p, ordinary or supersingular. In the low-pole basis ([ω],[η]) of H¹_dR(E/F_p), with the column convention,

```math
F^{*} = \pi^{*} =
\begin{pmatrix}
0 & -\beta \\
0 & t-p
\end{pmatrix}
\equiv
\begin{pmatrix}
0 & -\beta \\
0 & H
\end{pmatrix}.
```

When H ≠ 0 the image of F\* is ⟨−βω + Hη⟩ = ⟨η − κω⟩, so κ = −b₀/d₀ with b₀ = −β, d₀ = H.

*Proof.* Pullback along endomorphisms is additive on H¹_dR: for endomorphisms a, b one has a + b = m∘(a,b), and m\* = pr₁\* + pr₂\* on H¹ (primitivity, classical), so (a+b)\* = a\* + b\*. The same holds on invariant differentials. In particular (π − 1)\* = π\* − 1 on H¹_dR, and α\*ω = π\*ω − ω. The endomorphism α = π − 1 is separable, since α\*ω = −ω. Its kernel G = E(F_p) is étale of order N = p+1−t. Write α = ι∘φ_G, with φ_G Vélu's normalized isogeny (φ_G\*ω′ = ω) and ι a scaling of scale u onto (A,B). Then α\*ω = uω forces u = −1, so the Vélu model is (A,B) itself.

To pass from forms to classes, represent a class by a meromorphic differential θ that is regular away from a finite set S, together with local primitives g_s at each s ∈ S of pole order below p. Two such data with the same θ define the same class whenever their primitives differ by regular functions. Two primitives of pole order at most one, whose difference has a regular differential, differ by a regular function, because a simple pole would give a double pole in the derivative.

Vélu's x-map x∘φ_G = x + Σ_{Q≠O}(τ_Q\*x − x(Q)), multiplied by ω = φ_G\*ω′, gives φ_G\*η′ = Σ_{Q∈G}τ_Q\*η − σ_Gω, with σ_G = Σ_{Q∈G∖O}x(Q). At each point Q ∈ G both sides use primitives of pole order one there: φ_G\*g′ on the left, and τ_{−Q}\*g (the only singular summand at Q) on the right. So the identity holds for classes. Translations act trivially on H¹_dR because H¹ classes are primitive (m\* = pr₁\* + pr₂\*), which is classical. Hence φ_G\*[η′] = N[η] − σ_G[ω], and

```math
\alpha^{*} =
\begin{pmatrix}
u & -\sigma_G/u \\
0 & N/u
\end{pmatrix}
=
\begin{pmatrix}
-1 & \sigma_G \\
0 & -N
\end{pmatrix},
\qquad
\pi^{*} = \alpha^{*} + I =
\begin{pmatrix}
0 & \sigma_G \\
0 & 1-N
\end{pmatrix}.
```

Counting points over each x gives σ_G = Σ_{x∈F_p}x(1+χ(F(x))) = Σ_x xF(x)^h = −β. This holds because Σ_{x∈F_p}x^m is −1 for m > 0 with (p−1) | m and 0 otherwise, and deg(xF^h) < 2(p−1). Finally 1−N = t−p ≡ H. ∎

**Alternate argument for ordinary E (classical inputs).** F\*[ω] = 0, and the image of F\* is the conjugate line ker 𝒞_dR = ⟨[η] − κ[ω]⟩ (Katz, 2019, §3). So the second column (b₀, d₀) is proportional to (−κ, 1). The trace of F\* on H¹_dR(E/F_p) is t mod p (classical comparison of crystalline Frobenius with the Frobenius trace; not re-read in this pass). Hence d₀ = H and b₀ = −κH = −β. This route uses those two classical facts; the Vélu proof above does not.

The low-pole convention is essential. Replacing g by g + s(x²/y)^p leaves η − dg unchanged but shifts [η] by (s/2)F\*[η], which changes the (1,2) entry. In the row convention the matrix is the transpose [[0,0],[−β,H]].

Independent confirmation (executed) uses two methods that involve neither Vélu's formulas nor point sums. The first is a direct Čech–de Rham computation over all **1,428** nonsingular models with 7 ≤ p ≤ 23, plus 30 random models at each of p = 29, 31, 37, 41. (The first version misquoted this exhaustive count as 1,418; it is 42+110+156+272+342+506 = 1,428.) The second is a Kedlaya–Monsky–Washnitzer computation of the integral Frobenius matrix. Scopes and the repaired runs are in §9.

**Corollary A.1.** The (1,2) entry of crystalline Frobenius modulo p is −β. Supplying it, or supplying M̄, is a β-oracle, and extracting κ from it costs O(1) field operations. That is an oracle reduction, not a cost reduction.

**Relation to p-adic E₂ (classical sources; conversion derived here).** Mazur, Stein and Tate (2006, §3.2) and Harvey (2008, §3) write the p-adic E₂ through the image of η under F^N. With F^N(η) = a_Nω + b_Nη, E₂(E, ω_std) ≡ −12a_N/b_N mod p^N, where ω_std = dx/(2y) on a short model. Combined with Theorem A this gives E₂(E, dx/(2y)) ≡ 12κ (mod p). The same relation follows from Katz (2019, Theorem 3.1) after the substitution y = 2y′. This conversion was not checked against an independent E₂ computation. Harvey's Theorem 1 computes E₂ mod p^N in Õ(p^{1/2}N^{5/2}) time when p > 6N. That is a published complete algorithmic bound for the whole unit-root direction.

## 3. Lemma B: the integral comparison for an arbitrary lift (derived here)

**Lemma B.** Let p ≥ 7, let E: y² = x³+Ax+B be ordinary over F_p, and let Ẽ: y² = x³+Ãx+B̃ with Ã, B̃ ∈ Z_p reduce to (A,B). Let C ⊂ Ẽ[p] be the connected subgroup and σ_C its generic-fibre kernel sum, both defined in §3.1. Then the following hold.

| Part | Statement |
|---|---|
| (i) | C(Q̄_p) is a Galois-stable subgroup of order p, and σ_C ∈ Q_p |
| (ii) | There are u ∈ Q_p^× and an integral short model Ẽ′ = (A′,B′) with (A′,B′) ≡ (A,B) mod p, such that Vélu's model of Ẽ_{Q_p}/C is (A_V,B_V) = (u⁴A′, u⁶B′) |
| (iii) | ψ′ = ι_u∘φ_V extends to a morphism Ẽ → Ẽ′ over Z_p, whose reduction is γ∘F for an automorphism γ of the model (A,B) acting as (x,y) ↦ (x/w², y/w³) with w⁴A = A and w⁶B = B |
| (iv) | In the integral low-pole bases ψ′\* has matrix V = [[u, −σ_C/u],[0, p/u]] ∈ M₂(Z_p), and V ≡ M̄·diag(w, w⁻¹) = [[0, −βw⁻¹],[0, Hw⁻¹]] mod p |
| (v) | Hence v(u) = 1, σ_C ∈ pZ_p, u ≡ pw/t (mod p²), and κ ≡ σ_C/p (mod p), independently of the lift and of γ |

In (ii), ι_u(x_V,y_V) = (x_V/u², y_V/u³). In (iii), w = ±1 when AB ≠ 0, and w = −1 means the identification reduces to −F.

### 3.1 The connected subgroup and its generic-fibre kernel sum

Every point of Ẽ(Q̄_p) extends to an integral point, because Ẽ is proper over Z_p, and so has a reduction in E(F̄_p). Reduction is a homomorphism whose kernel is the group of points of the formal group Ê. This is classical.

Define C(Q̄_p) as the set of p-torsion points reducing to O, i.e. Ê[p]. Because E is ordinary, Ê has height one. So the [p]-series pz + ⋯ has its first unit coefficient at z^p, and by Weierstrass preparation it has exactly p zeros in the open unit disc (classical). In the coordinate x these p−1 nonzero points have v(x(Q)) = −2/(p−1). The pilot checks the corresponding fact in every model: the reversed p-division polynomial is s^h times a polynomial with nonzero constant term modulo p.

Reduction and multiplication by p commute with Galois, so C(Q̄_p) is Galois-stable and defines a finite étale subgroup scheme C_{Q_p} of order p. Its schematic closure in Ẽ is the finite flat connected subgroup C = Ẽ[p]⁰ of the connected–étale sequence (classical). The kernel sum σ_C = Σ_{Q∈C(Q̄_p)∖O}x(Q) is a symmetric function of Galois-conjugate points, so σ_C ∈ Q_p. Its integrality is not assumed; it is part of the conclusion (v).

### 3.2 The quotient elliptic scheme and the raw Vélu equation

Over Q_p, Vélu's formulas for the kernel C_{Q_p} give a short model (A_V, B_V) of E″_{Q_p} = Ẽ_{Q_p}/C_{Q_p}, with a normalized isogeny φ_V (φ_V\*(dx_V/y_V) = dx/y). Its coefficients lie in Q_p because they are symmetric in the kernel points. In this "raw" equation one has A_V = Ã − 5t_C and B_V = B̃ − 7w_C, where t_C and w_C are the usual Vélu sums.

E″_{Q_p} has good reduction, because it is isogenous to Ẽ_{Q_p} and isogenous curves have the same reduction type (classical; §3.7). Let Ẽ″ be a minimal short model with unit discriminant. It is the good integral model of the quotient, and the quotient elliptic scheme Ẽ/C is Ẽ″. The raw Vélu equation and Ẽ″ are two short models of the same curve over Q_p, so (A_V,B_V) = (v⁴A″, v⁶B″) for some v ∈ Q_p^×. The raw equation is not minimal: (v) shows v(u) = 1, so A_V ≡ 0 mod p⁴ and B_V ≡ 0 mod p⁶. The pilot observes exactly these valuations, v(A_V) = 4 and v(B_V) = 6, whenever AB ≠ 0.

### 3.3 Why the rescaled quotient has the required reduction

Ẽ and Ẽ″ are smooth Weierstrass models over Z_p, hence Néron models of their generic fibres. So the isogeny ι_v∘φ_V extends uniquely to a homomorphism φ″: Ẽ → Ẽ″ (classical; §3.7). The same applies to its dual. Their composite extends [p], whose reduction is nonconstant, so the reduction φ″₀ is nonconstant.

On formal groups φ″ is a power series f(z) ∈ Z_p[[z]] vanishing at the p−1 nonzero points of C, all in the open disc. So f has at least p zeros there, and by Weierstrass preparation f′(0) ∈ pZ_p. Hence φ″₀\* kills the invariant differential, and φ″₀ is inseparable.

A nonconstant homomorphism of elliptic schemes over Z_p is finite and flat, with constant degree p. An inseparable isogeny of degree p factors as λ∘F with λ separable of degree one, i.e. an isomorphism λ: E^{(p)} = E → Ẽ″₀ (classical). So Ẽ″₀ ≅ E over F_p. An isomorphism of short Weierstrass curves over F_p in characteristic at least 5 is a scaling by some ω₀ ∈ F_p^×.

Lift ω₀ to a unit and rescale Ẽ″ by it. This gives an integral short model Ẽ′ = (A′,B′) with (A′,B′) ≡ (A,B) mod p and unit discriminant. Absorbing both scalings into one scale u gives (A_V,B_V) = (u⁴A′, u⁶B′) and ψ′ = ι_u∘φ_V: Ẽ → Ẽ′ over Z_p. Its reduction is ψ′₀ = γ∘F, where γ is the reduced rescaling composed with λ. Since γ is an automorphism of the fixed model (A,B), it is a scaling by w with w⁴A = A and w⁶B = B. That gives w = ±1 when AB ≠ 0, w ∈ μ₆ when A = 0 and w ∈ μ₄ when B = 0. Choosing the lift of ω₀ suitably makes γ = id; the proof below does not need that choice.

### 3.4 Integral low-pole bases

For a short model with Ã, B̃ ∈ Z_p and unit discriminant (p ≥ 5), H¹_dR(Ẽ/Z_p) is free of rank two with basis [dx/y], [x dx/y]. Katz (2019, §4) states this over Z[1/6N], and it was verified in that source. Concretely, take the cover U₁ = Ẽ∖O and U₂ = Ẽ∖{y = 0}. Both are affine over Z_p, since {y = 0} is finite étale over Z_p when the discriminant is a unit. The class [η̃] is the integral cocycle (η̃, η̃ − dg̃; g̃) with g̃ = 2x²/y. Here η̃ − dg̃ is regular along O because the expansions in z = −x/y have integral coefficients, w(z) ∈ Z_p[[z]], and the polar parts cancel. The independent pass found the multiplier 2 for every model.

The Čech–de Rham complex consists of flat Z_p-modules, and H⁰_dR and H²_dR are free of rank one (classical). So H¹_dR(Ẽ/Z_p) ⊗ F_p = H¹_dR(E/F_p) compatibly with pullbacks. The basis reduces to the low-pole basis ([ω],[η]), because the reduced primitive 2x²/y has pole order one, which is below p. The same holds for Ẽ′, which has the same reduction (A,B) and the same coordinates.

### 3.5 The comparison and the sign

Over Q_p the Vélu argument of Theorem A, now with |C| = p, gives ψ′\*[ω̃′] = u[ω̃] and ψ′\*[η̃′] = (p[η̃] − σ_C[ω̃])/u. So the matrix is V = [[u, −σ_C/u],[0, p/u]].

Because ψ′ is a morphism of smooth proper Z_p-schemes, ψ′\* maps the lattice H¹_dR(Ẽ′/Z_p) into H¹_dR(Ẽ/Z_p), so V ∈ M₂(Z_p). Reducing modulo p, V̄ is the matrix of (γ∘F)\* on H¹_dR(E/F_p) in ([ω],[η]). By the composition rule and Theorem A this is M_F M_γ = [[0,−β],[0,H]]·diag(w,w⁻¹) = [[0,−βw⁻¹],[0,Hw⁻¹]].

Compare entries. From (2,2), p/u ≡ Hw⁻¹ is a unit, so v(u) = 1 and u ≡ pw/H ≡ pw/t (mod p²). From (1,2), σ_C/u ∈ Z_p, so σ_C ∈ pZ_p, and σ_C/u ≡ βw⁻¹. Hence

$$\frac{\sigma_C}{p}=\frac{\sigma_C/u}{p/u}\equiv\frac{\beta w^{-1}}{Hw^{-1}}=\kappa\pmod p.$$

The factor w⁻¹ multiplies the whole second column of M_F M_γ, so it cancels. When the identification reduces to F (w = 1) one has V̄ = M̄. When it reduces to −F (w = −1) one has V̄ = −M̄. The ratio is the same in both cases. ∎

**Remark B.1 (crystalline form; not used in the proof).** Let c_Ẽ: H¹_cris(E/Z_p) → H¹_dR(Ẽ/Z_p) be the comparison isomorphism. Define the transport T = c_{Ẽ′}∘c_Ẽ⁻¹: H¹_dR(Ẽ/Z_p) → H¹_dR(Ẽ′/Z_p) by T(ω̃,η̃) = (ω̃′,η̃′)T. T is integral, as a composite of lattice isomorphisms. It reduces to the identity, because both comparisons reduce to H¹_dR(E/F_p) and both bases reduce to ([ω],[η]). Functoriality for the lift ψ′ of γ∘F gives VT = M·Γ, where M is the matrix of crystalline Frobenius in the Ẽ-basis and Γ that of γ^{\*cris}, with Γ ≡ diag(w,w⁻¹). In particular M = VT when ψ′ reduces to F, and M = −VT when it reduces to −F. This remark relies on the Berthelot–Ogus comparison, which was not re-read in this pass. The proof above needs only de Rham functoriality and base change.

### 3.6 Precision: the identity versus this implementation

The identity needs σ_C to absolute precision p², because σ_C ∈ pZ_p. Write G(s) = Π(s − 1/x(Q)) over one representative of each pair ±Q of nonzero points of C. G is monic with Z_p-coefficients, because v(1/x(Q)) = 2/(p−1) > 0, and v(G₀) = 1. Then σ_C = −2G₁/G₀ and σ_C/p = −2G₁/(pG₀). So it suffices to know G₀ mod p² and G₁ mod p³.

The repaired pilot confirms both sides of this bound. With working precision N = 3 it recovers κ in all 270 tested models with p ≤ 13. With N = 2 its precision tracking refuses all 270, instead of returning an unsupported digit.

The particular implementation uses much more than this. It builds the whole p-division polynomial over Z/p^N, of degree (p²−1)/2, and Hensel-lifts the canonical factor to N digits. Its codomain and scale checks need A_V mod p⁵ and B_V mod p⁷, losing up to three digits to divisions by G₀^k, and the Deligne–Tate and CM checks consume further digits. Hence N = 14 in the pilot. The independent formal-group route used six digits. These are costs of the verification code, not requirements of the identity.

### 3.7 Classical inputs and their verification status

| Input used in Lemma B | Where used | Verification in this pass |
|---|---|---|
| Isogenous curves over a local field have the same reduction type (Serre–Tate, 1968) | §3.2 | Statement read in Kofler's lecture notes, "Néron Models" (Cambridge); original not re-read |
| A smooth Weierstrass model is the Néron model; morphisms of generic fibres extend to Néron models | §3.3 | Read in Streng (2007), Prop. 2.2 and (1.2), Lemma 3.5; Stein (2003) Def. 1.6.2 for the mapping property |
| H¹_dR of y² = f(x) is free with basis dx/y, x dx/y where 6Δ is invertible | §3.4 | Read in Katz (2019), §4 |
| Reduction kernel = formal-group points; ordinary ⇔ height one; Weierstrass preparation | §3.1, §3.3 | Silverman, *AEC*, Ch. IV, V and VII; not re-read (checked numerically in every pilot model) |
| Inseparable degree-p isogeny factors through F; finite flatness and degree constancy over Z_p; isomorphisms of short models are scalings | §3.3 | Silverman, *AEC*, Ch. II–III; standard commutative algebra; not re-read |
| Translations act trivially on H¹_dR; H⁰, H² of the curve free; de Rham base change | §2, §3.4 | Classical (Katz 1970; Oda 1969); not re-read |
| Connected–étale sequence; C = Ẽ[p]⁰ is the closure of C_{Q_p} | §3.1 (naming only) | Tate (1997); not re-read; the proof uses only C(Q̄_p) |
| Crystalline comparison and functoriality | Remark B.1 only | Berthelot–Ogus (1978); not re-read; not used in the proof |

Lemma B is therefore proved modulo these classical inputs. Where a source was not re-read, the statement is the standard textbook one; if any of them failed, (ii)–(v) would become conditional at that step. No numerical agreement is used in place of a proof step. The 570 pilot models, the 1,026 independent model–lift pairs and the repaired reruns are corroboration only.

## 4. Propositions C, D and E (derived here)

**Proposition C (canonical lift).** If Ẽ = E_can is the canonical lift, the Deligne–Tate quotient is E_can itself, so Ẽ′ can be taken equal to Ẽ. Then ψ′ is the Frobenius-lifting endomorphism, with ψ′\*ω = λ̄ω, λ̄ = p/λ and λ the unit root of X² − tX + p (classical; Serre–Tate and Katz, not re-read). The unit-root line is U = ⟨η + cω⟩ with c = σ_C/(λ̄² − p) ∈ Z_p and c ≡ −κ (mod p). This is the eigenline of ψ′\* for the unit eigenvalue, by the extension note's Corollary 2.1.

Executed: at the rational CM models, which are the canonical lifts at split primes, c ≡ 1 (mod p³) for (−35,−98) at p = 11, 23, and c ≡ −1 (mod p³) for (−30,56) at p = 11, 17, 19. These match the reviewed D = −7 seed and D = −8 control.

These formulas compute the slope modulo p, and at the canonical lift the unit-root coordinate modulo higher powers of p. They do not solve the historical precision-two weighted-sum problem modulo p² (the Witt/Miller quantity K_p), which remains as recorded in the handover.

**Proposition D (étale side, characteristic p).** For ordinary E/F_p, β = −Σ_{P∈E(F_p)∖O}x(P), and κ = −σ_V/t² with σ_V = Σ_{Q∈E[p](F̄_p)∖O}x(Q). The first identity is the last step of Theorem A. For the second, the Verschiebung π̂ = t − π is separable with kernel the étale p-torsion. That kernel is a genuine étale subgroup defined over F_p as a group scheme; its nonzero points need not be rational, and no rational generator is required. Its Vélu matrix [[t, −σ_V/t],[0, p/t]] equals π̂\* = tI − M̄ = [[t, β],[0, t−H]] modulo p. This is an explicit recovery method. It is not shown to be the only way Serre–Tate or étale data could enter a computation.

**Proposition E (derivative form).** As polynomials in (A,B) over F_p, β ≡ ϑH with ϑ = 6B∂_A − (4/3)A²∂_B, so κ = ϑ log H. The proof uses ϑF = 6Bx − (4/3)A² = 6xF − ((4/3)A + 2x²)F′. That gives ϑ(F^h) = 6h·xF^h − ((4/3)A + 2x²)(F^h)′, and taking the coefficient of x^{p−1} yields the exact identity ϑH = (p+1)β − (4p/3)A[x^p]F^h over Z[1/3]. The independent pass found this proof and checked it for 5 ≤ p ≤ 71. Euler's relation 4A∂_AH + 6B∂_BH = −H shows that κ is one derivative of H transverse to scaling. A single value of t does not supply it, as the eight same-trace, distinct-slope pairs show. The identity is an exact algebraic derivation, not a conclusion from numerical agreement. Its relation to classical modular-form derivatives (b_p ≡ E_{p+1}/12 and the Serre derivative of E_{p−1}, via Katz 2019, Theorem 3.1) is very likely classical, and no novelty is claimed without a separate literature assessment.

## 5. Information audit

| Object | What it is | Identified recovery map | What is shown | What is not shown |
|---|---|---|---|---|
| Certified trace t | One integer; H = t mod p | None | t does not determine κ: eight exact same-trace, distinct-κ pairs (executed) | — |
| Unit-root eigenvalue λ mod p^k | Hensel root of X²−tX+p | None | Same pairs | — |
| j_can mod p² (AB ≠ 0) | Witt pair (j₀, j₁) of the canonical lift | None identified | Fixes E_can mod p² up to isomorphism (derived: for AB ≠ 0, ∂j/∂B ≠ 0, so the first-order variation of j vanishes only along the scaling direction) | That no useful map from j_can exists |
| j mod p² at j = 0, 1728 | Coarse invariant of a lift | — | Does not distinguish non-isomorphic lifts mod p²: j ≡ 0 mod p³ for every (pa₁, B), j ≡ 1728 mod p² for every (A, pb₁) (derived; 69 lifts executed) | Anything about generic j or about κ (which is 0 there by automorphisms) |
| Arbitrary integral lift | Any (Ã, B̃) reducing to (A, B) | With its canonical subgroup: κ = σ_C/p (Lemma B) | Canonicality is not needed for this map | That canonical-lift data cannot help some other map |
| Canonical-subgroup kernel sum σ_C mod p² | One element of pZ_p/p²Z_p | κ = σ_C/p | Equivalent to κ as information | Any statement about the difficulty of computing it |
| Frobenius lift on E_can | Endomorphism lifting π | c = σ_C/(λ̄²−p) (Prop. C) | Gives the unit-root line mod p^k | — |
| Serre–Tate parameter with markings | q(Ẽ) ∈ 1+pZ_p | None identified | q = 1 characterizes E_can (classical) | Whether q-data enter a cheaper map |
| Étale torsion data (§6) | Point, Kummer coordinate, kernel polynomial | κ = −σ_V/t² from the kernel sum (Prop. D) | One explicit method | Necessity of the kernel sum |
| Crystalline Frobenius mod p | Matrix in the low-pole basis | κ = −b₀/d₀ | b₀ = −β (Theorem A) | — |
| Fixed-D CM table | R_D(j) for fixed D | β/H = −(3B/2A)R_D(j) | Completed restricted case | Growing D |
| Transverse derivative of H | ϑH at (A,B) | κ = ϑH/H (Prop. E) | Exact identity | A cheap derivative oracle |

With E supplied, κ is already determined. Every "does not determine" entry above concerns a datum without E, and every recovery map is a question of computation, not of information.

## 6. Representations of étale and Serre–Tate data

The review asked to separate a full torsion point, its Kummer coordinate, a kernel polynomial and an intrinsic deformation description, and to charge each construction separately. A general Serre–Tate description need not materialize a torsion point or every kernel element. The sizes in the table are exact sizes of the stated encodings, not lower bounds for any algorithm. The construction costs are for the named constructions only.

| Representation | Encoding size (exact for this encoding) | A known construction and its cost | Relation to κ | Kind of statement |
|---|---|---|---|---|
| Étale p-torsion point P ∈ E(F_{p^k}) | 2k⌈log₂p⌉ bits, k = ord(t mod p) dividing p−1 | From t, #E(F_{p^k}) via the characteristic polynomial; random point times cofactor; expected Õ(k² log p) F_p-operations per attempt (randomized) | P alone: no identified map; all p−1 multiples give σ_V | Exact size; complete bound for this randomized construction; k ranges from 1 (t = 1) to p−1, and no claim about its distribution is made |
| Kummer coordinate x(P) | k′⌈log₂p⌉ bits, where k′ is the order of t in F_p^×/{±1} (k′ = k/2 if k is even, k′ = k if k is odd). Frobenius acts on ⟨P⟩ as t, so π^{k′}P = ±P and x(P) ∈ F_{p^{k′}}; for t = −1, x(P) ∈ F_p | x-only arithmetic over F_{p^{k′}}. When k is even, P is an F_{p^{k′}}-point of the quadratic twist, whose order p^{k′} + 1 + t_{k′} follows from t; random x-coordinate times cofactor, expected Õ(k′² log p) F_p-operations per attempt (randomized) | Same as P | Derived; executed: ψ_V factors into irreducibles of degree exactly k′ on all 1,363 ordinary models checked (842 with k even). Revision 1 wrongly gave this row the degree k |
| Verschiebung kernel polynomial ψ_V ∈ F_p[x] | (h+1)⌈log₂p⌉ bits for the whole polynomial, independent of k; only the subleading coefficient is needed | In this pilot, from ψ_p mod p, whose intermediate has degree ph; from P, Π(x − x(iP)) in Θ(kp) operations; other degree-p isogeny methods in characteristic p not examined | σ_V = −2[x^{h−1}]ψ_V, so one coefficient gives κ given t | Exact size; costs of named constructions only |
| Intrinsic deformation description: Serre–Tate coordinate q(Ẽ), or the class of E_can mod p^n | O(n log p) bits | Needs markings (étale and multiplicative Tate-module bases). Maiga–Robert (Lemma 5.2) characterize j_can mod p² by Ψ_{Ẽ,p}(P) ≡ 0 mod p², under j ∉ F_{p²}. This pilot used Deligne–Tate iteration through C | Locates E_can. Katz (1981, Main Theorems 3.7.1–3.7.2 and Thm 4.3.1) relates dlog q to the Kodaira–Spencer map and to the Frobenius-fixed (unit-root) splitting under the Gauss–Manin connection, with no torsion points materialized. Whether that gives a computation of κ at a single F_p-point without p-scale data is not examined here | Construction costs depend on the markings chosen; not established here |

## 7. Dependency and cost table

The "Bound type" column uses five labels. **Size** is the exact size of a stated encoding. **Theorem** is a published complete algorithmic bound under its hypotheses. **Construction** is the cost of a construction implemented or described here. **Oracle** means data assumed supplied. **Heuristic** means unproved or unverified.

| Route/object | Assumptions | Exact construction | Size | Cold cost | Cached cost | Reconstruction | Bound type | Status |
|---|---|---|---|---|---|---|---|---|
| Comparator: BGS | B ≠ 0; BGS Theorem 14 unit hypotheses | Order-3 recurrence for [x^n]F^h to n = p−2 | O(√p) words | Õ(√p) field operations | Same | O(1) | Theorem (not implemented here) | Justified comparator |
| Comparator: Harvey (2008) | p > 6N; E fixed (Harvey states his running times for a fixed curve over Q, integral coefficients, not necessarily minimal) | Kedlaya-type Frobenius on {dx/y, x dx/y} | O(√p) | Õ(p^{1/2}N^{5/2}) | Same | O(1) via Theorem A | Theorem (not implemented); uniformity in the lift's coefficient size not tracked | Justified comparator. His §3.1 uses a known trace and determinant only to fill one column, a speedup of at most a factor of two, with precision caveats |
| Frobenius fragment | M̄ or b₀ supplied | Read entries | 2 elements | Supplier's | O(1) | κ = −b₀/d₀ | Oracle | Oracle reduction; fragment is β |
| j_can mod p² via universal J₁ | AB ≠ 0, ordinary | Erdoğan–Finotti Witt function J₁ ∈ F_p(X) | Not established: Erdoğan gives existence only; Finotti describes J₁ through Φ_p(X,X^p)/p and a Kaneko–Zagier form with ss_p(X)² in the denominator | Via Φ_p: up to (p+2)² coefficients before reduction | Evaluation of a stored rational function; degree not established | No identified map to κ | Heuristic (size); Construction (Φ_p count) | No cheaper κ from this construction |
| j_can mod p² via Deligne–Tate | Ordinary, AB ≠ 0 | One step Ẽ ↦ Ẽ/C from any lift | As for σ_C | As for σ_C | — | Gives j_can, not κ | Construction | Uses the same object as Lemma B; no κ gain |
| j_can mod p² via CM | End(E) of discriminant D known | Root of H_D lifted mod p² | h(D) coefficients | Õ(\|D\|) CRT method under GRH (not re-verified), plus order discovery | O(h(D)) | No identified map to κ | Theorem (cited, not re-read) | \|D\| = (4p−t²)/f² for an index f; its size for a given curve can range widely; no typical-size claim made |
| Newton on Φ_p(X,X) | j ∈ F_p | Naive Newton step | — | — | — | — | Construction | That step is degenerate, since Φ_p(X,X) ≡ −(X^p−X)²; this says nothing about canonical lifting in general (canonical lifts of F_p-curves were computed here by Deligne–Tate iteration) |
| Maiga–Robert Thms 1.1–1.2 | j ∉ F_{p²} | As in the paper | — | Õ(mnp); Õ(mn log p + I(p,m,Z_q)) | — | Output E_can and trace | Theorem | The hypothesis excludes our inputs from these theorems; it does not exclude canonical lifting itself |
| Canonical-subgroup kernel sum σ_C | Ordinary; any lift | Canonical factor of reversed ψ_p (this pilot) or slope-1/(p−1) factor of [p]-series (independent pass) | Needed data: G₀ mod p² and G₁ mod p³, i.e. O(log p) bits; the constructions produce the whole factor | ψ_p route: Θ(p²) input coefficients; [p]-series route: about 2p terms | Same | κ = σ_C/p | Size (needed data) / Construction (cost) | Oracle-equivalent to κ; no cheaper construction found |
| Étale torsion representations | Ordinary | §6 | §6 | §6 | — | κ = −σ_V/t² | Size / Construction / Heuristic as in §6 | No cheaper construction found; necessity not shown |
| t = ±1 subclass | k ≤ 2, k′ = 1 | P rational (t = 1) or quadratic with rational Kummer coordinate (t = −1) | O(log p) | Polylog for P or x(P) | — | σ_V needs p−1 summands (h distinct x-values): Θ(p) naively; Õ(√p) by a √élu-type adaptation (unimplemented inference) | Construction / Heuristic | At best parity with the comparator for these constructions |
| π − 1 point sum | — | Σx over E(F_p) | p points | Θ(p) | — | β | Construction | Equivalent coefficient |
| Derivative ϑH | — | ∂_AH, ∂_BH | Θ(p) monomials of H | Θ(p) | Θ(p) | κ = ϑH/H | Size / Construction | Equivalent to β |

A per-prime cache of the slope for every j ∈ F_p makes later queries O(1) plus a chart conversion. That is a cached-query contract, not a cold single-curve algorithm, and it is not credited here.

## 8. Source audit

| Source | Access in this pass | What was verified | Inference added here |
|---|---|---|---|
| Katz, N. M. (2019). On a question of Zannier. *Experimental Mathematics* | Author PDF fetched; extraction drops minus signs | Thm 3.1; Cartier on dx/y, x dx/y; Im Frob = ker 𝒞; U spanned by x dx/y − (b_p/a_p)dx/y; §4 freeness of H¹_DR with basis dx/y, x dx/y; §6 character sums | Signs a_p ≡ −Σχ(f), b_p ≡ −Σtχ(f) checked on all models p ≤ 31; chart conversion ours |
| Katz, N. M. (1976). *Annals of Mathematics*, 104(3) | Scan; pp. 459–506 only | §1.3, Lemma 4.0.7 | §5.7, 8.0.9, 8.0.13 unreachable; not cited for any step |
| Erdoğan, A. arXiv:1211.1152v4 | Fetched | Thm 1.1 existence; j = 0, 1728 lift to themselves; no degree or cost bounds | No size estimate is attributed to this paper |
| Finotti, L. R. A. Lifting the j-invariant (author manuscript) | Fetched | J₁ ∈ F_p(X), regular at 0 and 1728; relation to Φ_p(X,X^p)/p; Kaneko–Zagier form with ss_p(X)² | No degree bound verified; venue not verified |
| Borger & Gurney, arXiv:1608.05912v1 | Fetched | Canonical lifts in families; no algorithm or complexity claim | — |
| Maiga & Robert (author manuscript) | Fetched twice | Thms 1.1–1.2, Cor. 1.4, §2.3, Lemma 5.2 hypotheses and costs | The exclusion of E/F_p follows from F_p ⊂ F_{p²} |
| Bostan, Gaudry & Schost (2007) | Author versions | Thm 14 cost and hypotheses; Thm 17 | Application to the order-3 recurrence is ours |
| Mazur, Stein & Tate (2006) | Author copy | §3.2 E₂ via F^n(η) | Chart conversion ours |
| Harvey (2008), *LMS JCM* 11 | arXiv and publisher page; §3.1 re-read for revision 2 | Thm 1 costs; E₂ = −12B/D; running times stated with E treated as fixed; §3.1: a known trace and determinant fill one column, a speedup of at most a factor of two, with precision caveats and a change of basis when the top-right entry is not a unit | Column reading ours (independent pass and review concur); uniform dependence on the curve not tracked |
| Katz, N. M. (1981). Serre–Tate local moduli (author scan) | Fetched for revision 2; OCR-degraded | Thm 2.1 (q as complete invariant of lifts); §4.5 canonical lift q = 1; Main Thms 3.7.1–3.7.2 (Kodaira–Spencer and dlog q); Thm 4.3.1 (Gauss–Manin on the Fix splitting) | Read as an intrinsic description that materializes no torsion points; its computational use for κ is not examined |
| Bernstein, De Feo, Leroux & Smith (2020), arXiv:2003.10118 | Abstract | Õ(√ℓ) for a rational kernel point of prime order | Kernel-sum adaptation is an unimplemented inference |
| Kofler, L. "Néron Models" (Cambridge lecture notes) | Fetched | "Isogenous abelian varieties have the same reduction type" | Used in §3.2 |
| Streng, M. (2007). Néron models of elliptic curves (Leiden notes) | Fetched | Prop. 2.2: smooth Weierstrass model is a Néron model; (1.2) and Lemma 3.5: morphisms extend | Used in §3.3 |
| Stein, W. (2003). Abelian varieties notes, §1.6 | Fetched | Def. 1.6.2: Néron mapping property | Used in §3.3 |
| Silverman, *AEC*; Tate (1997); Berthelot–Ogus (1978); Katz (1970); Oda (1969); Vélu (1971); Serre–Tate (1968) | Not re-read | — | Standard statements, labelled where used |

## 9. Validation and run families

There are four run families, and their numbers are kept separate.

| Family | When and by whom | Code | Exit-status reliability | Evidence |
|---|---|---|---|---|
| A. Original pilot runs | This study, before the review | `ordinary_k_pilot` v1 | Failures propagated. However, the retained fixed-D and same-trace controls would have been skipped silently had their environment variables been absent; in the recorded runs they were present (74 fixed-D agreements, 8 pairs) | `evidence/original_bundle_20261012_2039.zip` |
| B. Original independent pass | Separate agent without access to the pilot | `independent_check` v1 | Mismatches did not affect the exit status. With a comparator wrong for every model, the preserved original `c1_cech.py` reports 0/42 with a nonempty failure list and exits 0 (reproduced here). It also hard-coded `/home/claude/...` and relied on `assert` | `evidence/original_independent_check/` |
| C. Review's reruns | External review, on the revision-0 ZIP, under Python 3.12.14 | Revision-0 pilot; original independent drivers (fixture path edited in the review's copy only) | The review demonstrated the exit-0 defect with a wrong β comparator in c1_cech.py (0/42 matches, exit 0) | `evidence/review_20261012/` (review, evidence ZIP and its 14-entry manifest, verified) |
| D. Repaired runs | Revisions 1–2 | `ordinary_k_pilot` v2, `independent_check` v2 | Every disagreement exits 1, a missing dependency exits 2, a reduced scope exits 3, a vacuous run exits 4; both runners propagate | `ordinary_k_pilot/results/`, `independent_check/results_full/`, `independent_check/results_injection/` |

Family D results (executed in this revision):

| Check | Scope | Result |
|---|---|---|
| Pilot `run_all.py`: char-p identities, Serre derivative, Kummer degree, p-adic Lemma B pilot, retained dependency check, coverage | As in revision 0, plus new checks | All six steps PASS; counters identical to family A where comparable |
| Kummer-coordinate field of definition (revision 2) | All ordinary models 7 ≤ p ≤ 23 and 60 seeded models at each of p = 29, 31 (1,363) | ψ_V factors into irreducibles of degree k′ = ord of t in F_p^×/{±1} in every model; k′ = k/2 < k in all 842 models with k even |
| Lemma B precision floor | 270 models, p ≤ 13 | N = 3 recovers κ in all; N = 2 refused in all |
| Retained imports | Paths and hashes recorded in `retained_dependency_check.json` | `fixed_D_evaluator.py` (69ec09…) and `cm_tables.json` (66bbf3…) equal the extension manifest; the completed `depth_three_b0_recognize.py` (a7142c…), `depth_three_recognize.py` (b3bffe…) and their three dependencies equal the inherited manifest and are the modules actually imported |
| D = −256 control and exhaustive cross-check | (73; 16, 27); all models at p = 73, 89, 97, 113 | β/H = 44 = recognizer multiplier; every fixed-D slope and recognizer multiplier equals the coefficient target; D = −256 table hits coincide with B = 0 depth-three recognitions (288 at p = 73, 352 at p = 89, 448 at p = 113), and D = −192 hits with A = 0 recognitions (288 at p = 73, 384 at p = 97) |
| Pilot failure injection | Six wrong-mathematics trials (including the Kummer degree); four missing-dependency trials; one explicit reduced-scope trial | All detected (exit 1, 2 or 3 as designed); the runner propagates |
| Independent checks, full profile | Same scope as family B (§9.1) | 21 steps PASS; 46,213 checks; 0 failures |
| Independent failure injection | Defect reproduction on the preserved original; nine injected errors; missing targets; vacuous run; runner propagation | Original c1_cech with a wrong comparator: 0/42 matches, nonempty failure list, exit 0 (defect reproduced). Repaired: 9/9 injected errors exit 1; missing targets exit 2 (two drivers and the runner); vacuous run exits 4; runner exits 1 on an injected error |

The 288 and 352 recognitions at p = 73 and 89 are exactly the 640 exhaustive-model cases that the handover's D256_DEPENDENCY.md attributes to the older comparator. With the completed recognizer they agree, which is what that file predicts.

### 9.1 Repaired independent full-profile run

The repaired drivers were run at the scope of family B by `run_independent.py --profile full`. All 21 steps exited 0, with 46,213 recorded checks and no failures, in about 19 minutes of single-process time. The report, with every step's arguments, return code and counts, is `independent_check/results_full/RUN_REPORT.json`; each driver's JSON is beside it.

| Driver | Scope | Checks | Failures | Seconds |
|---|---|---|---|---|
| `c1_cech` | All nonsingular models for p = 7, 11, 13, 17, 19, 23 (1,428), plus 30 seeded random models at each of p = 29, 31, 37, 41 | 1,548 | 0 | 165.92 |
| `c1_kedlaya_p7_N2` | Kedlaya–Monsky–Washnitzer at p = 7, precision p^2, all nonsingular models; integrality, trace, determinant, reduction and stability | 210 | 0 | 1.92 |
| `c1_kedlaya_p11_N2` | Kedlaya–Monsky–Washnitzer at p = 11, precision p^2, all nonsingular models; integrality, trace, determinant, reduction and stability | 454 | 0 | 4.92 |
| `c1_kedlaya_p13_N2` | Kedlaya–Monsky–Washnitzer at p = 13, precision p^2, all nonsingular models; integrality, trace, determinant, reduction and stability | 646 | 0 | 9.7 |
| `c1_kedlaya_p17_N2` | Kedlaya–Monsky–Washnitzer at p = 17, precision p^2, all nonsingular models; integrality, trace, determinant, reduction and stability | 1,117 | 0 | 28.2 |
| `c1_kedlaya_p19_N2` | Kedlaya–Monsky–Washnitzer at p = 19, precision p^2, all nonsingular models; integrality, trace, determinant, reduction and stability | 1,403 | 0 | 43.58 |
| `c1_kedlaya_p23_N2` | Kedlaya–Monsky–Washnitzer at p = 23, precision p^2, all nonsingular models; integrality, trace, determinant, reduction and stability | 2,083 | 0 | 102.52 |
| `c1_kedlaya_p29_N2_s25` | Kedlaya–Monsky–Washnitzer at p = 29, precision p^2, 25 seeded random models; integrality, trace, determinant, reduction and stability | 125 | 0 | 23.95 |
| `c1_kedlaya_p31_N2_s25` | Kedlaya–Monsky–Washnitzer at p = 31, precision p^2, 25 seeded random models; integrality, trace, determinant, reduction and stability | 125 | 0 | 30.33 |
| `c1_kedlaya_p37_N2_s25` | Kedlaya–Monsky–Washnitzer at p = 37, precision p^2, 25 seeded random models; integrality, trace, determinant, reduction and stability | 125 | 0 | 45.69 |
| `c1_kedlaya_p7_N3` | Kedlaya–Monsky–Washnitzer at p = 7, precision p^3, all nonsingular models; integrality, trace, determinant, reduction and stability | 210 | 0 | 2.9 |
| `c1_extra` | Random integral lifts for every model at p = 7, 11, 13; rank-one check for 5 ≤ p ≤ 43; p = 5 recorded as informational only | 8,276 | 0 | 15.23 |
| `c2_formal_p7` | Formal-group canonical subgroup at p = 7, all ordinary models, trivial plus 3 random lifts each; p ∣ σ_C and σ_C/p ≡ κ | 288 | 0 | 5.34 |
| `c2_formal_p11` | Formal-group canonical subgroup at p = 11, all ordinary models, trivial plus 2 random lifts each; p ∣ σ_C and σ_C/p ≡ κ | 540 | 0 | 47.43 |
| `c2_formal_p13` | Formal-group canonical subgroup at p = 13, all ordinary models, trivial plus 2 random lifts each; p ∣ σ_C and σ_C/p ≡ κ | 864 | 0 | 120.16 |
| `c2_formal_p17` | Formal-group canonical subgroup at p = 17, 30 ordinary models, trivial plus 2 random lifts each; p ∣ σ_C and σ_C/p ≡ κ | 180 | 0 | 56.56 |
| `c2_formal_p19` | Formal-group canonical subgroup at p = 19, 15 ordinary models, trivial plus 2 random lifts each; p ∣ σ_C and σ_C/p ≡ κ | 90 | 0 | 45.37 |
| `c2_formal_p23` | Formal-group canonical subgroup at p = 23, 15 ordinary models, trivial plus 2 random lifts each; p ∣ σ_C and σ_C/p ≡ κ | 90 | 0 | 98.97 |
| `c3_etale` | All 1,256 ordinary target models for 7 ≤ p ≤ 23 with explicit étale points (field degree k up to 22), plus the self-test | 1,257 | 0 | 277.05 |
| `c4_c5` | 200 auxiliary-identity points; exact, mod-p and pointwise C4 identities for the 18 primes 5 ≤ p ≤ 71; C5 on all 19,948 nonsingular models with 7 ≤ p ≤ 61 | 20,202 | 0 | 14.61 |
| `l3_katz_signs` | a_p ≡ −S0 and b_p ≡ −S1 on all 3,190 nonsingular models for p = 5 to 31 | 6,380 | 0 | 0.32 |

Three differences from family B are deliberate. The exhaustive count is 1,428 (family B's report said 1,418). The Kedlaya stability sub-sample is now seeded, so the recomputed subset differs from family B's unseeded one. The formal-group check now also records the higher digits of σ_C/p: with two or three lifts per model they differed between lifts in every one of the 330 models, confirming that only κ mod p is lift-invariant. The model–lift pairs total 1,026, as in family B.

### 9.2 The review's reruns (family C)

The review verified all 51 SHA-256 entries of the revision-0 ZIP and reran it in a separate copy under Python 3.12.14. Its evidence ZIP was verified here against its own 14-entry manifest. The review's rerun CSVs (`rerun_charp_identities.csv`, `rerun_padic_lift_slopes.csv`) are byte-identical to the revision-2 pilot outputs, across Python 3.12 and 3.13.

| Review rerun | Observed result (as recorded by the review) |
|---|---|
| Main characteristic-p pilot | PASS; 1,574 ordinary models, 1,395 Verschiebung checks |
| Derivative pilot | PASS; 19,948 nonsingular models |
| p-adic pilot | PASS; 570 trivial, 570 random and 240 iterated canonical lifts; 74 retained fixed-D agreements |
| Original-cubic reconstruction | PASS; 507 cubic checks, 387 branch queries |
| Main-pilot planted errors | All three exited 1; the runner propagated failure |
| Original independent Čech code | PASS on all 1,428 nonsingular models for p = 7, 11, 13, 17, 19, 23 |
| Original independent étale-point code | PASS on all 126 ordinary models at p = 7, 11 |
| Original independent formal-group code | PASS on 8 model–lift pairs at p = 7 (bounded) |
| Original independent Kedlaya code | PASS on 4 sampled p = 7 models mod p² with 4 stability reruns (bounded) |
| Deliberately wrong β comparator in c1_cech.py | 0/42 matches, nonempty failure list, exit 0: the defect repaired in family D |

The independent drivers are not part of the pilot's `run_all.py`. They have their own runner, `independent_check/run_independent.py`, and their own failure injection.

## 10. Status separation

**Classical facts used** are those in §3.7 and §8, with the verification status stated there.

**Derived here**: Theorem A; Lemma B modulo the listed classical inputs, pending specialist review of its integral-model and comparison steps; Propositions C–E; the j mod p² failure at j = 0 and 1728; the field of definition F_{p^{k′}} of the Kummer coordinate of an étale p-torsion point.

**Executed prototypes**: the pilot and the repaired independent checks. They verify identities on finite scopes and are slower than the O(p) reference; none is a candidate algorithm.

**Heuristic or unverified**: any size estimate for the universal J₁; any statement about the typical size of k = ord(t mod p) or of CM discriminants; the √élu-type adaptation for Σx(kP); the E₂ chart conversion beyond the algebra shown.

**Route-specific obstructions**: the constructions in §§6–7 did not yield a cheaper complete algorithm. Each named construction builds the data listed for it, or reaches only square-root parity. This bounds nothing beyond those constructions: a scalar equivalent to κ might be computable without building the representation that contains it.

**Preserved failures and counterexamples**: the first π−1 check wrongly required w_G ≡ 0 (at p = 7, (0,1), w_G ≡ 2 while B − 7w_G ≡ B). The higher p-adic digits of σ_C/p are lift-dependent (515 of 570 trivial/random comparisons differ). The original independent drivers could exit 0 on mismatches. The first version miscounted 1,428 as 1,418, and overstated several conclusions (see `CHANGES.md`). Revision 1's representation table gave the Kummer coordinate the field degree k of the full point; the correct degree is k′, which is k/2 when k is even. The historical precision-two counterexamples are untouched and not generalized.

## 11. In plain language: what this adds to Cartier–Miller, and what is still open

The Cartier–Miller branch formula needs one hidden number per curve, the slope κ. Once you have it, the branch values T_f(μ) take only a few arithmetic steps. Point counting already gives the trace cheaply, but the trace alone cannot tell you κ: we have pairs of curves with the same trace and different slopes.

This study pins down exactly where κ lives. It is one entry of the Frobenius matrix, and that entry is the very coefficient we were looking for. The study also shows four other places where κ is written down: a sum over a special subgroup of any p-adic lift of the curve, a sum over the curve's points, a sum over its p-torsion, and a derivative of the Hasse invariant. All of these were proved, checked by computer, and checked again by an independent program, and the test machinery now fails loudly when something is wrong.

What we did not find is a faster way to get κ for a general curve. Every construction we tried either handles about p pieces of data or only matches the existing square-root method. That does not mean canonical lifts or Serre–Tate theory cannot help. It only means the ways we examined do not, and there is no proof that a shortcut is impossible. The sensible next step is narrower than "find a fast canonical lift": find a way to compute one of these exact single numbers without first building the whole polynomial or torsion orbit that contains it. Whether that can be done, and whether deeper structures such as Katz's Serre–Tate coordinates could do it, remains open.

## References

Bernstein, D. J., De Feo, L., Leroux, A., & Smith, B. (2020). *Faster computation of isogenies of large prime degree* (arXiv:2003.10118). https://arxiv.org/abs/2003.10118

Borger, J., & Gurney, L. (2016). *Canonical lifts of families of elliptic curves* (arXiv:1608.05912v1). https://arxiv.org/abs/1608.05912

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793

Erdoğan, A. (2013). *A universal formula for the j-invariant of the canonical lifting* (arXiv:1211.1152v4). https://arxiv.org/abs/1211.1152

Finotti, L. R. A. (n.d.). *Lifting the j-invariant: Questions of Mazur and Tate* [Author manuscript]. https://luisfinotti.org/math/papers/liftj.pdf

Harvey, D. (2008). Efficient computation of p-adic heights. *LMS Journal of Computation and Mathematics, 11*, 40–59. https://doi.org/10.1112/S1461157000000528

Katz, N. M. (1976). p-adic interpolation of real analytic Eisenstein series. *Annals of Mathematics, 104*(3), 459–571. https://web.math.princeton.edu/~nmk/old/padicinterp.pdf

Katz, N. M. (1981). Serre–Tate local moduli. In *Surfaces algébriques* (Lecture Notes in Mathematics 868), Exposé V bis. Springer. https://web.math.princeton.edu/~nmk/old/serretatelocmod.pdf (page range not verified)

Katz, N. M. (2019). On a question of Zannier. *Experimental Mathematics*. https://doi.org/10.1080/10586458.2018.1551818 (volume, issue and pages not verified)

Kofler, L. (n.d.). *Néron models* [Lecture notes, University of Cambridge]. https://www.dpmms.cam.ac.uk/~jcsl5/mazur/3.NeronModels.pdf

Maiga, A., & Robert, D. (n.d.). *Towards computing canonical lifts of ordinary elliptic curves in medium characteristic* [Author manuscript]. https://www.math.u-bordeaux.fr/~damienrobert/pro/publications/articles/fast_canonical_lift_g1.pdf

Mazur, B., Stein, W., & Tate, J. (2006). Computation of p-adic heights and log convergence. *Documenta Mathematica, Extra Volume: John H. Coates' Sixtieth Birthday*, 577–614. https://www.williamstein.org/papers/pheight/pheight.pdf

Stein, W. (2003). *Abelian varieties* [Lecture notes, 20 October 2003, §1.6]. https://williamstein.org/edu/Fall2003/252/lectures/10-20-03/10-20-03-Neron_models.pdf

Streng, M. (2007). *Néron models of elliptic curves* [Lecture notes, Leiden]. https://pub.math.leidenuniv.nl/~strengtc/neron.pdf

Vélu, J. (1971). Isogénies entre courbes elliptiques. *Comptes Rendus de l'Académie des Sciences de Paris, Série A, 273*, 238–241.
