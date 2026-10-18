# Cancellation-aware local algebra for the elliptic branch amplitude

David Jordan research project, 18 October 2026. AI-assisted, unrefereed mathematics with standard-library Python evidence. Work was done in a separate directory; no external repository was read from or modified, and nothing was published. Prior reports were treated as unrefereed inputs, and every statement below carries an explicit status label.

## 0. Result

No fast acquisition was found. The investigation produced neither a poly(log p) nor a sub-square-root signed-scale method. It did produce a sharply scoped local theorem explaining exactly why the chosen cancellation-aware mechanism fails, plus several new exact identities.

**One-shot cancellation theorem (S1, S3, S4; proved).** At the branch point, every division value in the multiplication chain has an explicit closed-form residue: it is a sign, times n/2 or 1, times a power of β = 3s². A leading-residue arithmetic with paired certificates (the R-state) is therefore exact at every gate except the last, where both inner summands have residue 1/4. The amplitude is then created in one step at depth h+1. In the two-dimensional local ring of the parameter plane at the branch point, the target f₂ₚ has initial form

$$c\,t\,(st+3s^2u)^h,\qquad z=s+u,$$

and every other chain state is a unit. Consequently no arc, ramified arc, blow-up chart or weighted chart centred at the branch can spread the cancellation over several gates. In each of them the critical gate jumps from units to order ≥ h+1, and the associated graded data keep c only as the scalar of the initial form.

**Signed normalization, independently proved (S2).** The identity M_p = f₂ₚ/f_p⁴ = y([p]P)/y(P) = (st)^h G_t(s), with valuation h+1 and leading coefficient s^h c, is proved twice. The second proof goes through the formal group: [p] = V(w^p), the tangent of V is the Hasse invariant (Katz, 1973, §3.6), and translation by the moving two-torsion point does the rest. It uses neither φ₁ = −cI nor the retained identity g₁(s) = c. An independent chord-and-tangent computation over F_p((q)) confirms y([p]P) = (c/s)q^{p+2} + O(q^{p+4}) coefficient by coefficient, with no division polynomial involved.

**What the extra information would have to be (S5, S6, S8).** The exact-demand sensitivities J_m show that the critical residue depends, with nonzero weight, on the depth-(h+1) coefficient of every chain state except a few explicit ones. The branch-chart paired identity is

$$U/V-1=\frac{4y(P)y([p]P)}{(x([p]P)-x(P))^2(x(P)-x([p-1]P))}=-4s^hc\,t^{h+1}+\dots$$

and every lower gate has a unit or valuation-separated normalized difference. So inside the chain there is no small defect to transport: the answer to Sol's transport question is negative in this precise sense. A tested branch-chart drift law, the analogue of Opus's critical drift, locates the amplitude in the p-adic carry of a degree-(p+1) index polynomial.

**A global anchor outside the circuit (S7; proved).** On the nodal fibre t = −3/4, the Hasse polynomial equals the Legendre symbol χ(6). Combined with a mod-p Chu–Vandermonde evaluation, this gives

$$c_p=\chi(6)\,\frac{(4/3)_N}{(-3/4)\,(4/3-b)_N},\qquad N=\lfloor k/2\rfloor\approx p/12.$$

It also gives two equivalences: acquiring c_p is polylog-equivalent to evaluating the normalized supersingular polynomial S_p at any single point, and also to computing the product of the supersingular j-invariants other than 0 and 1728:

$$\prod_{j\in SS_p\setminus\{0,1728\}} j=-\tfrac34\,\chi(6)\,1728^{N}\,c_p .$$

This is a costed, factorial-type comparator. It is not a local extraction, and it does not improve the square-root exponent.

**Calibration (background).** c_p = 2(m!)^{−3} = ±2Γ_p(1/3)^{−3} mod p. The most recent primary statement located on single-prime factorial-type complexity is Costa, Gerbicz and Harvey (2014): the best known algorithm for the Wilson quotient has complexity p^{1/2+ε}. A poly(log p) acquisition of c_p would therefore be a new algorithm for Γ_p(1/3) mod p at inert primes. This is a statement of where the bar sits, not a lower bound.

The strongest defensible contribution is the one-shot cancellation theorem with its exact first failure, the independent formal-group normalization, and the global-anchor equivalences. Novelty of the identities has not been established; Section 13 explains why.

## 1. Inputs, audit and baselines (newly executed)

From the delivered directory, `audit_package.py` passed all manifest hashes before anything was regenerated. `verify_baselines.py` then passed at 11, 17, 23, 29, and `--confirmation` passed at 41, 47 with c = 9, 23. `local_reference.py 17 --mode both` returned first orders 9 and 19 and recovered c = 2. I inspected `local_reference.py`, `support/stack_safe_beta.py` (copied unchanged, SHA-256 f4547c48…), `validation_oracles.py`, the retained branch proof, Sol's report and Opus's report v2. I checked the retained branch argument's dependencies; the new proof in §4 avoids them.

## 2. Conventions

Throughout, p = 6k+5 ≥ 11 is a certified prime. Put h = (p−1)/2, m = (p−2)/3 = 2k+1, B = 1/4 and s = (−B)^{(2p−1)/3}, so that s³ = −B; let β = 3s² and χ be the Legendre symbol. The family is E_t: y² = z³+tz+B over F_p[[t]], with F_t(z) = z³+tz+B. The invariant differential is ω = dz/(2y) and the formal parameter is w = −z/y; with these choices ω = (1+O(w))dw.

The division values use ψ₂ = 2y, with f_n = ψ_n for odd n and f_n = ψ_n/(2y) for even n, computed by the classical halving recurrences. For odd n = 2a+1, f_n = L−R with L = f_{a+2}f_a³ and R = f_{a−1}f_{a+1}³, and Q² = 16F² is multiplied onto L when a is even and onto R when a is odd. For even n = 2a, f_n = f_a(U−V) with U = f_{a+2}f_{a−1}² and V = f_{a−2}f_{a+1}². Write C(n) for the dependency closure of index n; it has O(log p) elements (retained window lemma).

H(t) = [z^{p−1}]F_t^h is the Hasse polynomial, and c = c_p = H′(0) = h!/(m!k!)·B^k = 2(m!)^{−3}. The latter equality is the retained Wilson computation and was rechecked against the factorial oracle at every tested prime. Relative Frobenius is (z,y) ↦ (X,Y) = (z^p,y^p) onto Y² = X³+t^pX+B, and Verschiebung is V(X,Y) = (Φ_t(X), Y G_t(X)). The moving root is r(t), with r³+tr+B = 0 and r(0) = s; the two-torsion section is T₀(t) = (r(t),0).

## 3. Lemma 1: division values at a two-torsion point (S1, proved)

**Lemma 1.** Let R be any commutative ring, consider y² = x³+ax+b over R, and let e ∈ R satisfy e³+ae+b = 0. Put β = 3e²+a, ε(n) = (−1)^{⌊(n−1)/2⌋}, and let ν(n) = 1 for odd n and n/2 for even n. Set E(n) = (n²−1)/4 for odd n and (n²−4)/4 for even n. Then for every n ≥ 1,

$$f_n(e)=\varepsilon(n)\,\nu(n)\,\beta^{E(n)}.$$

*Proof.* Substituting b = −e³−ae gives f₃(e) = −9e⁴−6ae²−a² = −β² and f₄(e) = 2(−27e⁶−27ae⁴−9a²e²−a³) = −2β³, which agree with the claim, as do f₁ = f₂ = 1. Since F(e) = 0, the factor Q² vanishes at e. The odd recurrence therefore becomes f_{2a+1} = −f_{a−1}f_{a+1}³ when a is even and f_{a+2}f_a³ when a is odd. The four cases are handled by strong induction.

1. *Odd n = 2a+1, a even.* The exponents add to E(a−1)+3E(a+1) = a²+a = E(n). The sign is −ε(a−1)ε(a+1) = −(−1)^{a−1} = +1 = ε(n).
2. *Odd n = 2a+1, a odd.* The exponents give E(a+2)+3E(a) = a²+a, and the sign is ε(a+2)ε(a) = −1 = ε(n).
3. *Even n = 2a, a odd.* U and V carry the same power β^{3(a²−1)/4} and the same sign ε(a±2), with index factors ((a−1)/2)² and ((a+1)/2)². Hence U−V = −a·ε(a+2)β^{3(a²−1)/4}. Multiplying by f_a, and using ε(a)ε(a+2) = −1, gives aβ^{a²−1} = ε(2a)ν(2a)β^{E(2a)}.
4. *Even n = 2a, a even.* The index factors are (a+2)/2 and (a−2)/2, so U−V = 2ε(a+2)β^{3a²/4}. Multiplying by f_a = ε(a)(a/2)β^{(a²−4)/4} gives −aβ^{a²−1}, which is again the claim.

Indices 5 and 6 follow from the base values, so the induction is complete. No division occurs, so the identity holds in every commutative ring. ∎

**At the branch.** Take e = s, a = 0, b = B, so β = 3s². Then f_n(s;0,B) = 0 exactly when 2p | n. In particular every odd multiple of p gives a unit.

For p itself, quadratic reciprocity gives χ(3) = (−1)^{k+1} and β^{(p²−1)/4} = χ(3)^{(p+1)/2} = (−1)^{k+1}. Since ε(p) = (−1)^k, it follows that f_p(s;0,B) = −1.

At the critical gate the same computation gives U(0) = ε(p+2)((p−1)/2)²β^{3(p²−1)/4} = 1/4, and likewise V(0) = 1/4.

*Evidence.* Checked for all n ≤ 4p+3 at 14 primes, and for n ≤ 300 at 10007 and 10037. It was also checked as a universal identity over F_P for generic curves: with P = 10⁹+7 and P = 10⁶+3 in development, and with P = 2⁶¹−1 for n ≤ 300 in confirmation.

*Novelty.* This is an elementary identity that is likely known in the elliptic-divisibility literature; no source was found in a short search.

## 4. Theorem A: signed normalization (S2, proved twice)

**Theorem A.** Let P = (s,y) with y² = F_t(s) = st.

- **(A1)** f_p(s;t,B) ∈ F_p[[t]]^× with constant −1.
- **(A2)** M_p := f₂ₚ/f_p⁴ = y([p]P)/y(P) = (st)^h G_t(s).
- **(A3)** v_t(M_p) = v_t(f₂ₚ) = h+1 and [t^{h+1}]M_p = [t^{h+1}]f₂ₚ = s^h c.
- **(A4)** On the arc t = q²/s with P(q) = (s,q), y([p]P) = q·M_p(q²/s) = (c/s)q^{p+2} + O(q^{p+4}).

**Common steps.** (A1) is Lemma 1. For (A2), the classical formula y([n]P) = ψ₂ₙ/(2ψₙ⁴) (Washington, 2008, §3.2) with ψ₂ = 2y gives y([p]P)/y(P) = f₂ₚ/f_p⁴ for odd p. Composing [p] = V∘F gives y([p]P) = y^p·G_t(z^p), and y^{p−1} = F_t(z)^h. At z = s this becomes (st)^h G_t(s). These are identities of rational functions, and f_p is a unit, so no square root of st is needed. Because f_p⁴ has constant 1, the two leading coefficients in (A3) coincide. (A3) and (A4) are equivalent through q^{p+1} = (st)^{h+1}.

**Proof I (retained dependencies).** G_t(X) = −F₀(X)^h + t g₁(X) + O(t²), and the retained expansion of the first-order curve identity at X = s+u gives g₁(s) = c/(2(h+1)) = c. Hence G_t(s) = ct + O(t²), which is (A3). This route depends on the retained derivation of φ₁′ = −cF₀^h.

**Proof II (formal group; independent of φ₁ and g₁).**

1. *The arc point and its formal parameter.* P(q) lies on E_t over K = F_p((q)) because s³+B = 0. Since r(t) = s − t/(3s) + O(t²), we have s − r = q²/(3s²) + O(q⁴). Translation by the two-torsion point T₀ is given by x(R+T₀) = r + F′(r)/(x(R)−r) and y(R+T₀) = −F′(r)y(R)/(x(R)−r)². It follows that Q := P − T₀ = P + T₀ has x(Q) of valuation −2, so Q lies in the formal group Ê(qF_p[[q]]), and w(Q) = q/(3s²) + O(q³).
2. *The p-series.* Since [p]T₀ = T₀, we get [p]P = T₀ + [p]Q. In the formal parameters w and W = −X/Y, relative Frobenius is exactly w ↦ w^p. Katz (1973, §3.6, Lemma 3.6.3 and Lemma 3.6.5) gives [p](w) = V(w^p), with the linear coefficient of V equal to tangent(V), which is the Hasse invariant A(E_t, dz/2y). In the Weierstrass basis this invariant is H(t) = [z^{p−1}]F_t^h; this identification was checked as [w^p][p](w) = H(τ) by an independent Laurent computation at τ ∈ {1, 2, 5} for 11 primes. Therefore [p](w) = H(t)w^p + O(w^{2p}).
3. *Evaluation on the arc.* With H(t) = ct + O(t²), which follows from the multinomial expansion, and (q/(3s²) + O(q³))^p = q^p/(3s²) + O(q^{3p}) in characteristic p, we get w([p]Q) = (c/(3s³))q^{p+2} + O(q^{p+4}).
4. *Back to y.* From the translation formula, y(R+T₀) = F′(r)·w(R)·(1+O(w(R)²)) as a power series over F_p[[t]]. With F′(r) = 3s² + O(q²), this gives y([p]P) = (c/s)q^{p+2} + O(q^{p+4}). ∎

Proof II uses only standard formal-group background and the two-torsion translation formulas. It is therefore independent of the retained φ₁ = −cI identity and of g₁(s) = c, and it re-derives the latter, since [t]G_t(s) = c follows from (A3).

**Executed evidence.** `check_signed_dense` verifies (A1)–(A3) on dense jets. Independently, `grouplaw_arc.py` computes [p]P by affine double-and-add over F_p((q)) with certified relative-precision Laurent arithmetic, and so shares no code with the division-polynomial recurrence. It returns valuation p+2, leading coefficient c/s, and q^{p+3} coefficient 0 at 21 primes up to 10037.

`check_arc_identity_full` also compares q·f₂ₚ/f_p⁴ with the chord-and-tangent y([p]P) coefficient by coefficient over every certified exponent, which is more than p+4 exponents, at 16 primes. That is an independent confirmation of the rational identity in (A2) on the arc.

**A further fact used in §6.** On E₀ the p-series is exact: [p]_{E₀}(w) = −w^{p²}. The reason is that π² = −p because the trace is 0, π acts by w ↦ w^p, and [−1] is w ↦ −w.

## 5. The mechanism: a relational leading-residue state (S3, proved)

The mechanism was defined, and its update theorem derived, before any large experiment was run.

**State.** For a nonzero a ∈ F_p[[t]], the state is ρ(a) = (v(a), lc(a)), recording the valuation and the leading coefficient; zero has its own state. Every subtraction gate also stores a **paired certificate** (ρ(L), ρ(R), status). Multiplication is exact: valuations add and residues multiply. Addition and subtraction are exact ('separated') when the valuations differ or the residues do not cancel. When the leading terms cancel, the status is set to 'CANCELLED' and no output is produced.

This is precisely the extra information that keeps a leading-term arithmetic honest. Exact certificates of known identities are carried as part of the state. The essential one is F(s;t,B) = ts *exactly*, because s³+B = 0; without it the R-state would wrongly report a cancellation inside F itself.

**Input acquisition.** B and s are obtained by counted powering, using O(log p) multiplications. Then β = 3s², and the residues of f₃, f₄ come from Lemma 1 using O(1) multiplications. The inputs are F = (1,s) and Q² = (2, 16s²).

**Theorem B (update theorem).**

1. **Odd gates.** At every odd gate in C(2p), one summand contains Q² and has valuation 2, while the other is a product of units. The gate is separated, and its output (0, f_n(s;0,B)) is exact.
2. **Even gates.** At every even gate 2a in C(2p) with a ≠ p, we have U(0)−V(0) = f₂ₐ(s;0,B)/f_a(s;0,B) = ε·a·β^{(·)} ≠ 0, so the gate is separated and exact.
3. **The critical gate.** At 2p, ρ(U) = ρ(V) = (0, 1/4) and the status is CANCELLED. By Theorem A, the true state of U−V = f₂ₚ/f_p is (h+1, −s^hc).
4. **Branch target.** The R-states of Φ_t(s) = s − 4F f_{p−1}f_{p+1}f_p^{−2} and of r(t) both equal (0,s). Their first-order coefficients also agree: Lemma 1 gives −4s·ε(p−1)ε(p+1)·((p²−1)/4)·β^{(p²−3)/2} = −1/(3s) = r′(0). The true state of the difference Φ_t(s) − r(t) is (p+2, c²/(3s)), by the retained branch theorem, which was confirmed again here.

*Proof.* Items 1 and 2 are Lemma 1 together with the exact certificate for F. Item 3 combines Lemma 1, the quadratic-reciprocity computation of §3, and Theorem A. For item 4, the term 4F⋯ has valuation 1, and the first-order coefficient follows from Lemma 1 with the same reciprocity computation; the depth p+2 is the retained theorem. ∎

**Information content.** Every R-output is the closed form ε(n)ν(n)β^{E(n)}. These outputs involve only n and β, so they contain no information about c. The mechanism is correct and costs O(log p), but it computes nothing about the amplitude. The critical cancellation is the arithmetic coincidence ((p−1)/2)² ≡ ((p+1)/2)² mod p, equivalently ν(2p) = p ≡ 0.

**Instrumented first failure (executed).** `instrumented_chain` runs the R-state and dense jets of precision h+2 gate by gate. At every development and confirmation prime, the R-state agreed with the dense leading state at every gate below 2p.

The first and only failure is at index 2p, an even gate, with stored data ρ(U) = ρ(V) = (0, 1/4 mod p). The true leading order is h+1 and the missing coefficient is −s^h c. Examples: (22; (6,5)) at p = 11; (2026; (507,38)) at p = 1013; (20074; (5019,1389)) at p = 10037. The pure R-state run at p = 1,000,037 uses 142 states, 827 residue multiplications and 56 setup multiplications, and reports CANCELLED at index 2,000,074.

## 6. Theorem C: chart independence and the initial form (S4, proved)

Let O = F_p[[u,t]], with z = s+u and m = (u,t). Put ℓ = st + 3s²u, the linear form of F_t(s+u).

**Theorem C.**

- **(C1)** f_n(s+u;t,B) ∈ O^× whenever 2p ∤ n.
- **(C2)** f₂ₚ(s+u;t,B) ∈ m^{h+1} \ m^{h+2}, with initial form c·t·ℓ^h.
- **(C3)** Let φ: O → F_p[[τ]] be any local homomorphism, with u ↦ ατ^e + … and t ↦ γτ^e + … where e ≥ 1 and (α,γ) ≠ (0,0). Then every state of C(2p) other than f₂ₚ maps to a unit, and the R-state is exact at every gate except 2p. Moreover

$$\varphi(f_{2p}) = c\gamma(s\gamma+3s^2\alpha)^h\,\tau^{(h+1)e}+O(\tau^{(h+1)e+1}).$$

- **(C4)** In the blow-up chart t = ut′, f₂ₚ = u^{h+1}·f̃ with f̃(0,t′) = c·t′(st′+3s²)^h. In the other chart, u = tu′, the factor is t^{h+1} with restriction c(s+3s²u′)^h.

*Proof.* (C1) is Lemma 1. For (C2), Theorem A gives f₂ₚ = F_t(s+u)^h·G_t((s+u)^p)·f_p⁴ in O, where G_t(X) is regular at (s,0) because its denominator is a power of the unit f_p. Now F^h ≡ ℓ^h mod m^{h+1}. Next, G_t(s+u^p) = −F₀(s+u^p)^h + t·g₁(s+u^p) + O(t²); here F₀(s+u^p) ∈ m^p and g₁(s) = c by Theorem A, so G ≡ ct mod m². Finally f_p⁴ ≡ 1. Since gr_m O = F_p[u,t] is a domain, the initial forms multiply. (C3) and (C4) follow by substituting into the initial form. Odd gates stay separated because φ(F) ∈ m and the other summand is a unit; even gates stay separated because the residue field is F_p. ∎

**Consequences for the requested charts.**

- *Ramified arc.* Here u = 0, t = q²/s, e = 2 and (α,γ) = (0,1/s), giving (c/s)q^{p+1}. This is Theorem A again.
- *Transversal arc.* The order is exactly h+1 unless the arc is tangent to the two-torsion locus ℓ = 0; along z = r(t) the target vanishes identically.
- *Blow-ups and weighted charts.* These change e and the restricted form, but not the fact that a single gate takes unit inputs to order ≥ (h+1)e.
- *Associated graded data.* The shape t·ℓ^h is forced by the geometry: t is the supersingular fibre and ℓ the two-torsion locus. Its scalar is exactly c, so obtaining the initial form is the same task as obtaining c.

**Formal-group representation.** Represent odd chain states by w([n]Q). Then [n](w) = nw + O(w²) for p ∤ n, so leading-residue arithmetic in w is closed until n = p. There, [p](w) = H(t)w^p + O(w^{2p}), and the missing datum is H mod t² = ct. On the arc, the coordinate change q ↦ w has the explicit, c-free Jacobian 1/(3s²), so the formal chart neither hides c nor supplies it.

In the Weierstrass parameter, [p]_{E₀}(w) = −w^{p²} exactly (§4). The Lubin–Tate deformation coordinate of this family, in the basis fixed by ω, is therefore H(t) itself to first order, and its t-Jacobian at 0 is c. Converting to formal moduli costs nothing here, and it acquires nothing: the deformation parameter is the disallowed Hasse-derivative input.

## 7. Proposition D: exact demand and refinement accounting (S5)

For m ∈ C(2p), let J_m be the derivative of the constant-level chain map f_m(s;0,B) ↦ f₂ₚ(s;0,B), computed by forward-mode dual numbers at t = 0.

**Proposition D (proved).** Replace f_m by f_m + δt^{h+1} and recompute every state above m. Then [t^{h+1}]f₂ₚ changes by exactly J_m·δ. The four critical inputs feed only the final gate, so their weights are explicit products of Lemma 1 residues, all nonzero:

$$J_{p+2}=f_pf_{p-1}^2,\quad J_{p-2}=-f_pf_{p+1}^2,\quad J_{p-1}=2f_pf_{p+2}f_{p-1},\quad J_{p+1}=-2f_pf_{p-2}f_{p+1}.$$

Here every f is evaluated at (s;0,B). Also J_p = U(0)−V(0) = 0.

*Proof.* Each recomputed state changes by δt^{h+1} times its constant-level derivative, plus O(t^{h+2}); summing over paths gives J_m. ∎

**Tested.** At all 16 tested primes, J_m ≠ 0 for every non-base state m ∈ C(2p) other than p, apart from two recorded accidental zeros: m = 6 at p = 17 and m = 62 at p = 1019. Among the base indices, which are exact inputs and are never refined, J₃ = J₄ = 0 at every tested prime, and J₁ = 0 at p = 23. In addition, dense perturbation runs reproduced J_m·δ for three states per prime at 14 primes.

**Model corollary.** Suppose a computation depends on some f_m with J_m ≠ 0 only modulo t^{h+1}. Then it returns the same answer for two input sets whose true critical residues differ by J_mδ, so it is wrong for one of them.

The refinement consequence is concrete. Lazy or relaxed evaluation, in the sense of van der Hoeven (2002), must take every state with J_m ≠ 0 to depth h+2. Because all states are units, demand propagates down the chain without shrinking. The total acquired precision is therefore at least (h+2)·#{m: J_m ≠ 0}, which is Θ(p log p) coefficients; dense evaluation attains this bound. This is the t-adic counterpart of differential precision tracking (Caruso, Roe and Vaccon, 2014): here the differential of the chain map is degenerate only along explicit directions.

## 8. Proposition E: the paired-unit identity in the branch chart (S6, proved)

**Proposition E.** U/V = (x(P) − x([p+1]P))/(x(P) − x([p−1]P)), and

$$\frac UV-1=\frac{4\,y(P)\,y([p]P)}{(x([p]P)-x(P))^2\,(x(P)-x([p-1]P))}=-4s^hc\,t^{h+1}+O(t^{h+2}).$$

*Proof.* The net relation ψ_{n+1}ψ_{n−1} = ψ_n²(x − x([n]P)), applied at n = p±1, gives the ratio once the common factor ψ_p is cancelled. The chord identity x(A−B) − x(A+B) = 4y_Ay_B/(x_A−x_B)² with A = [p]P and B = P gives the second form. The leading term follows from U(0) = V(0) = 1/4 (§3) and U−V = f₂ₚ/f_p = −s^hct^{h+1} + … (Theorem A). ∎

At every lower odd gate the summands are separated by valuation, 0 versus 2. At every lower even gate, U/V − 1 is a unit. So the normalized paired difference is either O(1) or valuation-separated below 2p, and it jumps to order t^{h+1} at the top.

This is the branch-chart counterpart of Sol's cusp identity L/R = 1 − (16/3)Tab^k. The identity is the same rational function, evaluated in two charts. Both deviations are y([p]P) times an explicit unit, and both amplitudes are c up to explicit units (c = 4^{−k}T; checked). No transition between the charts is claimed or used.

*Executed.* `check_paired_identity` compares the dense U/V with the right-hand side computed from the independent chord-and-tangent points on the arc, at 14 primes.

## 9. Relation to Opus's Theorem G and the branch drift law (S8, tested)

Opus's Theorem G concerns comparing a p-integral identity with its own p-adic index shift. Its weight-0 ingredients are the class values ε_π n. The R-state data are exactly the branch-chart weight-0 values ε(n)ν(n)β^{E(n)}, and the critical cancellation ν(2p) ≡ 0 is the branch counterpart of S ≡ 0. **So the R-state supplies no information beyond the covered comparison. It is weaker: it supplies no information about c at all.**

Information about c entered this investigation in only three ways:

- the actual initial states carried to full depth, which is what the dense, cusp and arc extractors do at Θ(p) precision;
- identities outside the circuit's algebra, namely the nodal character-sum anchor of §10;
- the p-adic carry between indices n and n+2p at depth h+1, described next.

**Conjecture F (tested only).** Let g_j(n) = [t^j]f_n(s;t,B)/f_n(s;0,B) for p ∤ n.

- For odd n: g_j(n+2p) = g_j(n) for 1 ≤ j ≤ h, and g_{h+1}(n+2p) − g_{h+1}(n) = −(4/3)s^{−h}c·n.
- For even n: g_j(n+2p) = g_j(n) for j ≤ h−1, and the drift is c(−(4/3)s^{−h}n + 2s^h/n).

A characteristic-0 proxy (F_P with P = 10⁹+7) shows that g_j is a polynomial of exact degree 2j in n, for each parity and for j ≤ 6. So the critical depth h+1 is the first depth at which the degree reaches p+1 > p, the analogue of Opus's critical weight.

The law is consistent with Proposition E. With α = −(4/3)s^{−h}, the critical deviation of log(U/V) is [g(p+2) − g(p−2)] + 2[g(p−1) − g(p+1)]. Extending the law to negative indices through f_{−n} = −f_n, so that g(−n) = g(n), predicts g(p+2) − g(p−2) = 2αc and g(p+1) − g(p−1) = (α+2s^h)c. The α-terms then cancel and leave −4s^hc, as proved.

These two predictions, together with agreement of the lower depths, were checked directly on positive indices at 11 primes. This was a post-freeze exploratory check, recorded in `evidence/POST_FREEZE_DRIFT_CONSISTENCY.json`, and is not counted as confirmation.

*Tested* at 17 primes for every p ∤ n < p+6, and at the 3 tier-B primes near 1000 for n < 40. A proof would need branch-chart index-polynomiality with p-integrality, via σ at a half period, together with a degree-(p+1) version of Opus's Lemma N. The odd-class integrality follows from Lemma N.4 once polynomiality is known. Neither is proved here.

## 10. Theorem N: a global anchor outside the circuit (S7, proved)

**Theorem N.**

- **(N1)** For τ ∈ F_p, H(τ) = −Σ_z χ(F_τ(z)). For nonsingular E_τ this is a_p(E_τ) mod p. At t_s = −3/4, F_{t_s}(z) = (z−1/2)²(z+1), so H(t_s) = χ(3/2) = χ(6).
- **(N2)** H(t) = c·t·S(t³/B²), where

$$S(x)=\sum_{n=0}^{N}\frac{m!\,k!}{(m-n)!\,(3n+1)!\,(k-2n)!}x^n={}_3F_2\!\left(-m,-\tfrac k2,\tfrac{1-k}2;\tfrac23,\tfrac43;-\tfrac{4x}{27}\right),\qquad S(0)=1,\ N=\lfloor k/2\rfloor .$$

- **(N3)** Modulo p, S(−27/4) = (C−b)_N/(C)_N, where C = 4/3 and b = (1−k)/2 if k is even, b = −k/2 if k is odd. Hence

$$c=\chi(6)\,(C)_N\,/\,\big(t_s\,(C-b)_N\big).$$

- **(N4)** For every τ₀ ∈ F_p^× with S(x₀) ≠ 0, where x₀ = τ₀³/B², c = H(τ₀)/(τ₀S(x₀)). With Schoof's (1985) polynomial-time point counting for H at nonsingular fibres, or χ(6) at the node, acquiring c and evaluating S at one point are equivalent up to poly(log p) work. The cube root τ₀ = (x₀B²)^{(2p−1)/3} is unique.
- **(N5)** Let SS_p be the set of supersingular j-invariants in F_{p²}. Then ∏_{j∈SS_p∖{0,1728}} j = −(3/4)χ(6)·1728^N·c, and |SS_p∖{0,1728}| = N.

*Proof.*

- *(N1).* Σ_z F(z)^h = −[z^{p−1}]F^h, because deg F^h = 3h < 2(p−1). Euler's criterion turns F(z)^h into χ(F(z)). The node is Σ_{z≠1/2}χ(z+1) = −χ(3/2).
- *(N2).* Expand the multinomial: 3i + u = p−1 with p−1 ≡ 1 mod 3 forces u = 1+3n, i = m−n and l = k−2n. Every factorial argument is below p.
- *(N3).* We have −m ≡ 2/3 mod p, and (2/3)_n is a unit for n ≤ N < m. So mod p the series is a terminating ₂F₁(−N, b; C; −4x/27), and at x = −27/4 its argument is 1. Chu–Vandermonde, ₂F₁(−N,b;C;1) = (C−b)_N/(C)_N, is an identity of rational functions for fixed N, and (C)_N is a p-unit because 4/3 + i ≢ 0 for i < N; so it may be reduced mod p.
- *(N4).* Immediate from (N1) and (N2).
- *(N5).* By the Hasse criterion over F_{p²} (Silverman, 2009, Theorem V.4.1), the roots of S are the x-values of supersingular E_τ with τ ≠ 0. The Möbius map x ↦ j = 6912x/(4x+27) sends x = ∞ to j = 1728. The count of supersingular j-invariants (op. cit., V.4.1(c)) makes the N roots distinct, which was also verified as S | X^{p²} − X. A short computation gives (x_i − x_s)/x_i = 1728/j_i, so S(x_s) = 1728^N/∏j_i. ∎

**Costed acquisition (comparator only).** The formula needs one Euler powering, two inverses and two Pochhammer products of length N ≈ p/12. The 'linear' version costs about p/6 multiplications. The 'block' version, a balanced product with remainder-tree evaluation reusing Sol's comparator unchanged, costs 2·O(M(√(p/12)) log p). Since 2√(p/12) = √(p/3), this matches the block factorial for m!: **the anchor removes no exponent.**

The anchor is outside the circuit's algebra, so it supplies information that Theorem G does not cover. That information is exactly a hypergeometric value at a special argument.

*Executed.* (N1)–(N3) were checked against the factorial oracle at 16 primes up to 10037 (`check_nodal_anchor`), and the acquisition `nodal_anchor.acquire_c` was checked with both backends at the 8 confirmation primes. (N2) was also checked coefficientwise (`check_hasse_factorisation`) at all 16 primes. (N5) was checked by direct enumeration of supersingular j in F_{p²}, with no use of S, at 11 primes.

## 11. Complexity and matched timings

Let b = ⌈log₂p⌉. A field operation is a multiplication or addition of b-bit residues, charged at μ_mod(b) bit operations. Jet products use exact Kronecker packing, with a digit width strictly greater than the bit length of min(L₁,L₂)(p−1)², so the bit cost is that of one integer product of O(L(b+log L)) bits plus L reductions. Setup powerings, inverses (Newton for jets, Fermat for scalars), Newton iterations for r(t), the Legendre symbol and the final normalizations are all charged. Prime certification is an input cost.

| Method | Output | Field-operation bound | Stored residues |
|---|---|---|---|
| R-state (this round) | failure record, no c | O(log p) | O(log p), or O(1) with a fixed window |
| Dense signed, f₂ₚ to depth h+1, division-free | c | O(M(p)·log p) | O(p log p) |
| Dense branch Φ−r | c² only; sign needs an anchor | O(M(p)·log p) plus Newton for r | O(p log p) |
| Cusp extractor (prior Sol) | c | O(M(p/6)·log p) | O(p log p) |
| Arc chord-and-tangent (§4) | c | O(M(p)·log p) Laurent operations | O(p) |
| m! linear | c | O(p) | O(1) |
| m! block (prior Sol) | c | O(M(√p)·log p) | O(√p log p) |
| Nodal anchor, linear / block | c | O(p/6) / 2·O(M(√(p/12))·log p) | O(1) / O(√p log p) |
| Batch: all p ≤ X (Costa et al., 2014, method) | all c_p | X log^{3+ε}X bit operations in total (for Wilson quotients) | not implemented |
| Scale known: cached return / one absolute I(x) | c / I(x) | O(1) / O(log p) | O(log p) |

Measured cold acquisitions use one interpreter (Python 3.13), the same machine and Python integer residues. Values are medians of 3 samples at p ≤ 10007 and single samples above; certification and oracles lie outside the timed regions. All outputs were correct. The raw data are in `evidence/BENCHMARK.json`.

| p | Dense signed | Dense branch (c² only) | Cusp, prior | Arc chord-and-tangent | m! linear | m! block, prior | Nodal linear | Nodal block | R-state (no c) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1,013 | 101.7 | 432.6 | 82.3 | 190.4 | 0.039 | 1.47 | 0.110 | 1.41 | 0.25 |
| 10,007 | 3,072 | 24,870 | 1,780 | 4,992 | 0.223 | 4.94 | 0.193 | 4.70 | 0.40 |
| 100,019 | 185,148 | — | 75,233 | 217,919 | 2.60 | 19.7 | 2.29 | 18.6 | 0.56 |
| 1,000,037 | — | — | — | — | 30.9 | 75.4 | 22.6 | 68.0 | 0.62 |

All times are in milliseconds.

**Sign.** The branch target yields only c². Turning it into c needs a square root (Tonelli–Shanks, O(log² p) field operations, charged) and a sign anchor. The sign of c is the sign of m!, because c = 2(m!)^{−3}, and no anchor for it was found inside the branch target. The signed targets avoid the issue: dense f₂ₚ, cusp and arc. The nodal anchor carries its sign through χ(6) and the Pochhammer ratio. Once the scale is known, a cached return costs O(1), and an absolute I(x) value — the normalized O(log p) circuit followed by one multiplication by 1/(3sc) — took 0.52, 0.64, 0.80 and 1.06 ms at the four primes.

The dense local methods are far slower than the factorial-type methods. The prior cusp extractor, the fastest of them, is 56–3,800 times slower than the block factorial and 2,100–29,000 times slower than the linear factorial loop across 1,013–100,019. In this interpreter, the linear loop also beats the block method up to 10⁶, so the block method's asymptotic advantage is not yet visible.

For p ≥ 10,007 the nodal anchor is within a factor 1.4 of the corresponding factorial method, and its linear backend is slightly faster, as the product lengths p/6 versus p/3 predict. At 1,013 the fixed cost of its Fermat inversions dominates the linear backend. Either way it changes no exponent. No extrapolation to 1,201-bit primes is made. The R-state is cheap precisely because it computes nothing about c.

## 12. Freeze and confirmation record

The candidate statements S1–S9, all sources, the initial-data code, the cost model and the confirmation **rule** were hashed into `evidence/FREEZE.json` at 2026-10-18T02:19:36+0100, before any confirmation prime was chosen.

The development inputs were 11, 17, 23, 29, 41, 47, 53, 59 for the full suite. Exploratory inputs were 71, 83, 89, 101, 107, 113 (drift), 71, 83, 101, 197, 401 (arc), 1,000,037 (R-state smoke run), and the generic fields F_P with P = 10⁹+7 and 10⁶+3. All are listed in `dev_run.py`.

The frozen rule then selected tier A = {131, 137, 149}, tier B = {1013, 1019, 1031} and tier C = {10007, 10037}, with P = 2⁶¹−1 for generic Lemma 1. Every frozen check passed (`evidence/CONFIRMATION.json`, status PASS).

These primes are disjoint from this candidate's development inputs. Some were used in earlier rounds; for example, 131 and 137 were Opus's confirmation primes and 1013 and 10007 appear in older benchmarks. No global novelty of any prime is claimed. The delivered handover confirmation at 41 and 47 is not counted as candidate confirmation.

## 13. Primary-literature applicability audit

Each source below was opened and the relevant statement read in this round, except where marked.

| Source | Exact statement used or checked | Applicability here |
|---|---|---|
| Katz (1973), §2.0, §3.6 (Lemmas 3.6.1, 3.6.3, 3.6.5; Prop. 3.6.6) | The Hasse invariant A(E,ω) is defined by Frobenius on H¹(O). In characteristic p, [p](X) = V(X^p) and tangent(V) = A(E,ω); also [p](X) = pX + aX^p + … with a ≡ A (mod p). Read through an OCR-garbled fetch. | The key input to Proof II of Theorem A, in equal characteristic over F_p-algebras. It identifies the amplitude but gives no algorithm for H′(0). |
| Debry (2014), Thm 1, Cor. 2, Prop. 3 | Generic: [x^{p(p−1)/2}]ψ_p ≡ [x^{p−1}]f^{(p−1)/2} mod p. Over a field: equality. Ordinary: ψ_p ∈ K[x^p]. | Consistent with H(t) as the Hasse coefficient. A coefficient identity, not cheap acquisition. |
| Stange (2016), Lemma 10, Thms 3 and 14 | Explicit valuations of elliptic divisibility sequences over finite extensions of Q_p (mixed characteristic only); the formal-group valuation comes from the Newton polygon of [p]. | Mixed characteristic. The equal-characteristic analogue gives orders (v([p]w) = 1 + p·v(w)) but no residues; Theorem C supplies the residue. |
| Stange (2026), Thm 3.3; §§5.1, 7.4 | Chain rule Ψ_{αβ} = (Ψ_α∘β)Ψ_β^{deg α} for unbiased isogenies; Ψ₂ = −2y; inseparable normalization by inseparable degree. | Opposite even-index sign convention. Our ψ_{jp} composition is the classical case (checked: `check_multiples`). No Hasse-derivative acquisition. |
| Katz (1977), §§I–V | Mixed characteristic (char 0, residue char p, ord p = 1): measures on T_pG; divisibility and congruences of Hurwitz-type c(n); Lemma 2 uses the X^p coefficient of [p]. | Explains why Opus's Hurwitz coefficient has v_p = −1. Not transferable to the t-adic family; gives no acquisition. |
| Costa, Gerbicz & Harvey (2014), Thms 1–2 | Wilson quotients for all p ≤ N in N log^{3+ε}N; "the best known algorithm for computing w_p has complexity p^{1/2+ε}". | Calibration: single-prime factorial-type quantities sit at p^{1/2+o(1)}. Batch regimes already have average polylog methods. |
| Bostan, Gaudry & Schost (2007), Thm 14 | Square-root selected-term recurrences, with unit hypotheses. Statement as audited by the prior Sol round; not re-read. | The single-prime comparator class. |
| Doliskani (2018) | Abstract re-checked. The O(M(d) log n) window algorithm (§2.1, Algorithm 1) is as audited by Sol. | Closest antecedent for the chain; the R-state is its depth-0 truncation. |
| Caruso, Roe & Vaccon (2014) | Precision of p-adic computations tracked through the differential of the map. Main lemma not re-read in full. | Closest methodological antecedent of Proposition D (t-adic analogue); not used as a theorem. |
| van der Hoeven (2002) | Relaxed multiplication to order n costs O(M(n) log n). | Lazy demand cannot reduce the required depth h+2 (Prop. D). |
| Schoof (1985) | Polynomial-time computation of #E(F_p). Bibliographic record checked; not re-read. | Used only in the equivalence (N4). |
| Silverman (2009), Thm V.4.1 | Hasse criterion; supersingular j ∈ F_{p²}; count ⌊p/12⌋ + {0,1,1,2}. Textbook; not re-read. | Background for (N5); simplicity verified computationally. |
| Kaneko & Zagier (1998) | Supersingular polynomials via hypergeometric series. Bibliographic record checked; not theorem-audited. | (N5) is plausibly derivable from their explicit formulas; novelty unsettled. |
| Lubin (1964) | Bibliographic only. | Foundational for formal-group normal forms (§6). |

**Closest actual algorithmic antecedents.** For the chain, the closest antecedent is Doliskani's window algorithm. For precision on demand, it is relaxed arithmetic and differential precision. For the scale, it is BGS-type selected-term products, with the batch remainder trees of Costa, Gerbicz and Harvey. This was a targeted applicability audit, not a novelty audit. In particular Lemma 1, the initial-form statement and Theorem N may be known in some form.

## 14. Status, strongest contribution, next question

| Claim | Status |
|---|---|
| Lemma 1 (two-torsion residues, any ring) | Proved here (elementary); probably known |
| Theorem A, both proofs; arc coefficient c/s | Proved. Proof II rests on cited Katz §3.6. Independent chord-and-tangent confirmation |
| Theorem B (R-state update theorem, exact first failure) | Proved; instrumented at 16 primes |
| Theorem C (initial form c·t·ℓ^h; chart independence; blow-ups) | Proved; checked bivariately at 11 primes |
| Proposition D (sensitivities, critical weights) | Proved; nonvanishing for deeper states tested only |
| Proposition E (branch paired identity) | Proved; cross-implementation checked |
| Theorem N (N1–N4); (N5) | Proved; (N5) proved from cited textbook background, enumeration-checked |
| Conjecture F (branch periodicity and drift) | Tested only |
| Benchmarks | Measured for these implementations only |
| Poly(log p) or sub-√p acquisition | Not found. Not claimed impossible |
| Novelty of any identity | Not established |

**What is not excluded.** Theorem C covers local homomorphisms centred at the branch point and representations built from chain states. It says nothing about:

- non-local substitutions, Frobenius twists, or compositions with other endomorphisms;
- evaluation of universal index polynomials at non-integral lifts (Opus F4 in the branch chart);
- representations of the depth-(h+1) coefficients that are not computed by the recurrence;
- global anchors at other special points.

No conclusion about all local algebras or all compressed representations is drawn.

**Strongest defensible contribution.** Within the chosen cancellation-aware mechanism, the investigation gives an exact, proved account of its failure. Every gate is exact except one; that one cancels from residue 1/4 to depth h+1 in every chart centred at the branch; and the missing information is the scalar of a forced initial form c·t·(st+3s²u)^h. Two companion results support it: an independent formal-group proof of the signed normalization, and a global anchor showing that c_p is polylog-equivalent to one value of the normalized supersingular polynomial, equivalently to the product of the supersingular j-invariants other than 0 and 1728.

**One precise next question.** For primes p ≡ 5 (mod 6), is there an algorithm computing N_p = ∏_{j∈SS_p∖{0,1728}} j ∈ F_p in o(p^{1/2}) bit operations by using the Deuring correspondence — for example class-set or isogeny-graph structure of maximal orders in B_{p,∞} — rather than the hypergeometric coefficient sequence? By (N5), any such algorithm yields c_p and m! mod p with O(log p) further work, and conversely. The structure in the supersingular locus is the one structure this round did not use. The factorial route cannot exploit it, and the local chain provably cannot reach it below depth h+1.

## 15. Reproduction

Python 3.10 or later and the standard library suffice. From this directory:

```
python3 reproduce.py --audit      # verify frozen hashes only
python3 reproduce.py --dev        # development suite  -> evidence/DEVELOPMENT.json
python3 reproduce.py --confirm    # frozen confirmation -> evidence/CONFIRMATION.json (~4 min)
python3 reproduce.py --bench      # timings            -> evidence/BENCHMARK.json (long)
python3 -c "import sys; sys.path.insert(0,'src'); from rstate import rstate_run; print(rstate_run(1000037))"
python3 -c "import sys; sys.path.insert(0,'src'); from nodal_anchor import acquire_c; print(acquire_c(10007,'linear'))"
```

`reproduce.py` puts the bundled unchanged copy of the handover's `validation_oracles.py` (validation only) on the path. Frozen files are never modified by reruns; evidence JSON files are regenerated and their timings will differ.

## References

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793

Caruso, X., Roe, D., & Vaccon, T. (2014). Tracking p-adic precision. *LMS Journal of Computation and Mathematics, 17*(A), 274–294. https://doi.org/10.1112/S1461157014000357

Costa, E., Gerbicz, R., & Harvey, D. (2014). A search for Wilson primes. *Mathematics of Computation, 83*(290), 3071–3091. https://doi.org/10.1090/S0025-5718-2014-02800-7 (preprint: https://arxiv.org/abs/1209.3436)

Debry, C. (2014). Beyond two criteria for supersingularity: Coefficients of division polynomials. *Journal de Théorie des Nombres de Bordeaux, 26*(3), 595–605. https://doi.org/10.5802/jtnb.881

Doliskani, J. (2018). On division polynomial PIT and supersingularity. *Applicable Algebra in Engineering, Communication and Computing, 29*, 393–407. https://doi.org/10.1007/s00200-018-0349-z (preprint: https://arxiv.org/abs/1801.02664)

Kaneko, M., & Zagier, D. (1998). Supersingular j-invariants, hypergeometric series, and Atkin's orthogonal polynomials. In *Computational perspectives on number theory* (AMS/IP Studies in Advanced Mathematics, Vol. 7, pp. 97–126). American Mathematical Society.

Katz, N. M. (1973). p-adic properties of modular schemes and modular forms. In *Modular functions of one variable III* (Lecture Notes in Mathematics, Vol. 350, pp. 69–190). Springer.

Katz, N. M. (1977). Formal groups and p-adic interpolation. *Astérisque, 41–42*, 55–65. https://www.numdam.org/article/AST_1977__41-42__55_0.pdf

Lubin, J. (1964). One-parameter formal Lie groups over p-adic integer rings. *Annals of Mathematics, 80*, 464–484.

Schoof, R. (1985). Elliptic curves over finite fields and the computation of square roots mod p. *Mathematics of Computation, 44*(170), 483–494. https://doi.org/10.1090/S0025-5718-1985-0777280-6

Silverman, J. H. (2009). *The arithmetic of elliptic curves* (2nd ed.). Springer.

Stange, K. E. (2016). Integral points on elliptic curves and explicit valuations of division polynomials. *Canadian Journal of Mathematics, 68*(5), 1120–1158. https://doi.org/10.4153/CJM-2015-005-0

Stange, K. E. (2026). Division polynomials for arbitrary isogenies. *Research in Number Theory, 12*, Article 53. https://doi.org/10.1007/s40993-026-00741-2

van der Hoeven, J. (2002). Relax, but don't be too lazy. *Journal of Symbolic Computation, 34*(6), 479–542. https://doi.org/10.1006/jsco.2002.0562

Washington, L. C. (2008). *Elliptic curves: Number theory and cryptography* (2nd ed.). Chapman & Hall/CRC.

Prior project inputs, all unrefereed: the retained normalized-beta report; Sol, *Structured Frobenius extraction* (17 Oct 2026); Opus, *Structured Frobenius descent, revision 2* (18 Oct 2026).
