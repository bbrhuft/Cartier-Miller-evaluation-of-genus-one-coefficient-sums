# Atkin endpoint, round 3: a rounded-third specialization of Tal's split construction

David Jordan research project, round 3, 18 October 2026. AI-assisted and unrefereed. This report supersedes the round-2 report, which is kept unchanged as `REPORT.md` inside the package. It claims no publication, no priority, no lower bound, no new exponent and no new best factorial algorithm. Status labels: **[background]** marks established literature; **[proved here]** marks complete arguments written in this investigation, with novelty unsettled; **[computed]** marks finite exact computations whose scope is stated; **[tested]** marks exact agreement on stated finite input sets; **[open]** marks unresolved questions.

## 1. Result in brief

The signed scalar at the rounded-third boundary can be acquired faster than by any route in rounds 1 and 2, exactly and unconditionally, whenever p − 1 has a suitable prime factor q. The gain is a divisor-dependent constant factor, up to about 7× over FLINT's native factorial in the matched benchmarks. The method is a specialization of the split case of Tal (2026, Theorem 1.1) to n = m = (p−2)/3, with one structural change that is specific to the rounded third. Tal's lower-half routine fixes the torsion of the grid by computing K! = ((p−1)/q)! as an interval product of length K. Here that interval is replaced by a short anchor interval at the 1/6-point, of length about K/6, or, when p ≡ 5 (mod 12), at a conductor-12 point, of length about K/12. These are tied to m! by Gauss's duplication formula and by the round-2 quarter identity. Only H² and a² enter, so no class number is needed. A single certified Jacobi sum J(χ, χ) ∈ Z[ζ_q] suffices for every prime q ≤ 89. It is reconstructed by lattice reduction, certified by J·J̄ = p, and its root of unity is fixed by van Wamelen's criterion. Galois evaluation then supplies all the binomial relations required. The total interval length becomes (p−1)/(2q) or 5(p−1)/(12q), against 4(p−1)/(3q) for Tal's routine at n = m and (p+1)/6 for the round-2 half-interval method.

This is a constant-factor result that depends on a divisor. It is not an exponent improvement, and it does not apply uniformly: by Dirichlet's theorem, 67.83% of primes p ≡ 5 (mod 6) have an admissible prime q ∈ [5, 89], 48.54% one in [11, 89] and 29.55% one in [23, 89]. Measured gains are given in Section 11. The candidate was frozen before confirmation. Its first confirmation run failed through an implementation defect in the lattice fallback; no wrong value was returned. That failure is recorded unedited. A strictly additive amendment (R3.1) was then frozen and passed a fresh confirmation of 164 primes and 255 exact checks of the new route.

Two corrections were made to round 2. Round-2 identity (\*) is Williams and Currie's (1982) Lemma 14(c), so the p ≡ 17 (mod 24) route is a theorem. PARI's `qfbclassno`, used only inside its documented unconditional range |D| < 2·10^10, restores the half-interval advantage without GRH near 2·10^9. The secondary target, the residual sign of the quarter identity, was reduced exactly to a 2-power residue-character value of m!/N!. The cheap invariants tested do not determine it, and the first exact collisions are recorded.

The target remains the signed scalar a_L = binom(2L, L) 8^{−L} = (3/4)c_p with c_p = 2(m!)^{−3}. A signed c_p gives a_L with one multiplication, and conversely the unique cube root in F_p (3 ∤ p − 1) recovers m! from 2/c_p with O(log p) further operations. This is an equivalence up to inexpensive operations, not a hardness statement. The endpoint derivative D = A_n′(0) of the Atkin polynomial at J = 0 is obtained from c_p by the audited round-1 normalization. The closed form D = 1728^N R_N (p ≡ 5 mod 12) and D = −1728^{N+1} R_N (p ≡ 11 mod 12), with R_N = (4/3)_N/N!, is background (Kaneko & Zagier, 1998, Proposition 5). D is a coefficient derivative of a polynomial; nothing here is a parameter derivative or a derivative of a Frobenius-composed value circuit, and no normalized-value circuit is used as an absolute-scale oracle.

## 2. Package, environment and provenance

The work was done in a fresh copy of the round-2 archive. The inherited `audit.py` passed on the delivered bytes before anything was regenerated, and it still passes. The round-1 freeze (`evidence/FREEZE.json`), the round-2 freeze (`evidence/charp/FREEZE_CHARP.json`) and every inherited file are byte-identical to the delivered archive. All round-3 code is new and lives in `r3/`; the candidate files are `CANDIDATE_R3.md` and `CANDIDATE_R3_1.md` at the top level.

| Item | SHA-256 |
|---|---|
| Atkin_Endpoint_Round2_20261018.zip (input) | 079ffdd4d7dfe92492eb331234e35360c72876fe98139195b12359c98e831edf |
| Atkin_Endpoint_Round2_REPORT_20261018.md (input, identical to the archive's REPORT.md) | 88c21737bda24685c8211cdf651a53086db40da02b7063a07c09e12d312fc727 |
| Round-3 revised prompt (input) | e0267848a2b630169ecd28f199b3808b4939281d3e86e965e3264ab7a9db90a8 |
| r3/FREEZE_R3.json (written 2026-10-18T06:03:32Z) | 942e3e408ccbd6b4c93d20b6ca5281a2e87a1fd293db34a3a5647d2ac6d79786 |
| r3/FREEZE_R3_1.json (written 2026-10-18T06:31:38Z) | fe5c9410302b12aee8dedeb41d4b676c2b9be4b98d4cfdcf20879321b175cbb2 |

The environment was a 2-core Intel Xeon at 2.10 GHz with 7 GB of RAM, running Linux 6.18 (x86_64, glibc 2.39). The software versions were Python 3.13.16, python-flint 0.9.0 (FLINT 3.6.0), cypari2 2.2.4 (PARI 2.17.2) and sympy 1.14.0, which is used only by the inherited audit scripts. These are the same library versions as in round 2. The machine is different, so absolute timings are not comparable across rounds. The freezes are internal hash commitments with no external timestamp, so they record the order of operations only as far as the package's own records do.

## 3. The Williams–Currie correction

**Source and verification limits.** The statement used is Williams and Currie (1982), Lemma 14, on printed page 986. Its hypotheses are p ≡ 1 (mod 4) and q ≡ 3 (mod 4), and part (c) is the case (p/3) = −1 with q = 3. The scan on the author's site has no text layer, and both that host and the ECCC host were blocked from the workspace shell by the network policy, so I could not view the scanned page image. I did read the publisher's PDF text layer (Cambridge Core) through a web fetcher. Its raw OCR of part (c) is `(c)if(p/3) = -1, (_3)(p-l)/4 ^ (_1)(»(-»,)-»)/4^Éj=jj , (mod/>)`, under the running head "986 K. S. WILLIAMS AND J. D. CURRIE". Its legible parts (the base −3, the exponent (p−1)/4, a power of −1 whose exponent ends in /4, the modulus p, and a trailing factorial) are consistent with

$$(-3)^{(p-1)/4}\equiv(-1)^{(h(-3p)-2)/4}\left(\tfrac{p-1}{2}\right)!\pmod p ,$$

where h(d) is, by the paper's notation section, the class number of the quadratic field of discriminant d. The OCR alone does not prove the transcription. I therefore also verified the statement exactly, as described below. A visual check of the printed page remains a small outstanding item.

**Algebraic equivalence [proved here from background].** Write q₀ = (p−1)/4 and h_D = h(−3p). Since (−1)^{−x} = (−1)^x, the lemma gives H = h! ≡ (−1)^{q₀+(h_D−2)/4} 3^{q₀}. For p = 12N + 5 one has q₀ = 3N + 1, and (2/p) = (−1)^{q₀}: if N is even then p ≡ 5 (mod 8) and q₀ is odd, and if N is odd then p ≡ 1 (mod 8) and q₀ is even. The Pólya–Fourier expansion of the even character χ = (·/p) gives Σ_{0<j<p/3} χ(j) = (√p/π)(√3/2) L(1, χχ_{−3}), with χχ_{−3} = χ_{−3p} odd and primitive. Dirichlet's formula L(1, χ_{−3p}) = π h(−3p)/√(3p) then turns this into Σ_{j≤m}(j/p) = h_D/2 (Berndt, 1976; Davenport, 2000). Hence (m!/p) = (−1)^{(m − h_D/2)/2}. Since m = 4N + 1, (m − h_D/2)/2 = 2N − (h_D − 2)/4, so (m!/p) = (−1)^{(h_D−2)/4}. Substituting both facts gives (2/p)(m!/p) 3^{q₀} = (−1)^{q₀+(h_D−2)/4} 3^{q₀} = H, which is round-2 identity (\*). The exponents are integers because h_D ≡ 2 (mod 4). This follows from Rédei's theorem: the 2-rank of the class group of −3p is 1, and its 4-rank vanishes because (p/3) = −1 (Rédei, 1934). The round-2 assertion that an elementary approach cannot settle (\*) is withdrawn.

**Quarter consequence.** The round-2 identity C5 gives (m!/N!)² ≡ −(2/p) a ι₃ H with ι₃ = 3^{q₀}. Substituting H = (2/p)(m!/p) ι₃ and using ι₃² = (3/p) = −1 gives (m!/N!)² ≡ (m!/p)·a = (−1)^{(h(−3p)−2)/4} a. This is the promoted quarter consequence. It fixes m!/N! up to one sign, the subject of Section 9.

**Evidence [tested].** For all 19 610 primes p ≡ 5 (mod 12) with 17 ≤ p < 10^6, five identities hold exactly: the lemma, its rearrangement, the round-2 form (\*), the congruence h(−3p) ≡ 2 (mod 4) and the quarter consequence. The checks use FLINT factorials and PARI `qfbclassno` inside its unconditional range. The class numbers agree with an independent reduced-form count at 4504 of these primes (p < 2·10^5), and the Pólya–Dirichlet sum was checked directly at 818 primes below 3·10^4 (`r3/research/wc_lemma14c_check.py`, `r3/evidence/WC_LEMMA14C_DEV.json`).

**Implementation.** `r3/halfint.py` replaces the conjectural `h3p` route by a `williams_currie` route for every p ≡ 1 (mod 4), labelled as a theorem. It refuses an h(−3p) that is not ≡ 2 (mod 4) as a backend failure, and keeps the Gauss route for p ≡ 5 (mod 8) as a cross-check. The frozen `charp.py` is unchanged. In confirmation, all three routes agreed with FLINT's h! at every applicable prime, with 108 Williams–Currie, 56 Mordell and 54 Gauss evaluations. The correction proves the identity; it does not certify a class-number computation.

## 4. Unconditional class numbers

The installed PARI 2.17.2 documentation for `qfbclassno(D, 0)` with D < 0 states that it implements part of Shanks's baby-step giant-step method. It says the result is "unconditionally correct" for |D| < 2·10^10 and may be wrong beyond that if the class group has many cyclic factors. The same documentation says `quadclassunit` is correct under GRH. The text is archived in `r3/sources/PARI_2.17.2_installed_doc.json`. The current online catalogue page was truncated by the fetcher before these entries, and the PARI git web view disallows robots, so the online text could not be compared; the installed text is the operative one for the installed code.

`ClassNumberPolicy('unconditional')` in `r3/common.py` calls `qfbclassno` only for −2·10^10 < D < 0 and uses the reduced-form count otherwise. The finite range is never extended silently, and no conditional output is used to certify another. A separately labelled GRH backend uses `quadclassunit`. The inherited form-count sieve cache is cleared before every cold call. The half-interval route needs h(−p) for p ≡ 3 (mod 4) and h(−3p) for p ≡ 1 (mod 4). It therefore runs unconditionally with `qfbclassno` for p < 2·10^10 in class A and for p < 6.67·10^9 in classes B and C. At the round-2 source primes near 2·10^9, `qfbclassno` costs 0.2 to 0.4 ms, less even than `quadclassunit`. So the round-2 half-interval advantage survives there without GRH (Section 11, set B3). Beyond the range the unconditional form count dominates: at 5·10^10 to 5·10^11 the unconditional half-interval route took 1.9 to 11.0 s per call (one disclosed sample each), and it then loses to every other method. Certification beyond the range was not attempted.

## 5. Audit of Tal (2026)

**Version and reading.** ECCC TR26-211 has one listed version, with header date 25 September 2026 and publication date 26 September 2026. It runs to at least 66 pages, with appendices A to H. I read it through a fetcher's text extraction, which is garbled in places; the appendices were not present in the extracted text. Every statement below is the paper's claim. It is unrefereed and was not re-proved here except where Section 6 proves what is used.

**Model.** Inputs are binary, and costs are bit operations "unless field operations are specified". Õ suppresses logarithmic factors without a fixed power, and no machine model is named. Interval products (Lemma 2.6) are costed in algebra operations, Õ(1 + √M) for a length-M product by a Bostan–Gaudry–Schost-type block method.

| Statement | Hypotheses | Claimed cost | Notes |
|---|---|---|---|
| Thm 1.1, split case | p prime, q supplied with q \| p−1, 0 ≤ n < p | Õ(q^c + √(p/q)), deterministic | c ≥ 1 an absolute constant, not given numerically |
| Thm 1.2 | as 1.1, modulus p², n < p² | same | |
| Thm 1.3, cyclotomic indices | r a fixed odd prime power; q \| Φ_r(p); a representation of F_{p^r} and a compatible order-q character supplied | Õ_r(k^{O_r(1)}(q^{c_r} + (Φ_r(p)/q)^{1/(2φ(r))})) | r = 3 gives the abstract's √p/q^{1/4} interval term |
| Thm 1.5, reconstruction | q \| p−1, 1 ≤ a < q | Õ(q^c), product representation of J_a(χ) and its residue | via Lenstra–Silverberg's polarized principal-ideal algorithm, then van Wamelen |
| Prop 1.6 | M with complete factorization, target T | polynomial | finds a near-largest divisor ≤ T |
| Prop 1.7, density | t fixed odd prime-power indices, windows p^{1/(24tc)} ≤ q ≤ p^{1/(12tc)} | failure proportion ≤ 2^{1−t+o(1)} on [X, 2X]; saving ≥ 1/(48 t max c_r φ(r)) | unconditional via Bombieri–Vinogradov; for indices r_i, not the split case |
| Remark 1.4 | | positive saving for a 1−ε proportion of p ≤ X | from Prop 1.7; larger windows rest on an unproved heuristic |
| Prop 4.3, logarithmic refinement | none (divisor-free) | about O(√p (log p)^{3/2} (log log p)^{1/2}) bit operations, deterministic | a √(log p/log log p) gain over BGS-type O(√p log² p); exact form garbled in extraction |

The setup steps carry their own costs. Factoring p − 1 costs p^{1/5+o(1)} deterministically (Harvey–Hittmeir) or expected p^{o(1)} (Lenstra–Pomerance). An element of order q costs p^{1/4+o(1)} candidates deterministically by power non-residues, or an expected q/φ(q) trials. Both are said to be absorbed because c/(2c+1) ≥ 1/3. For the split case itself the paper cites only a positive proportion of primes with a divisor of p − 1 in fixed windows (Koukoulopoulos). The excerpt states no restriction to an arithmetic progression and no explicit proportion.

Three points remain unverified here: the determinism of the Lenstra–Silverberg step as used, the Burgess-type exponent behind the deterministic setup, and anything in the appendices. Since c is unspecified, no numerical exponent follows from Theorem 1.1, and none is claimed here.

**Selected construction.** I selected the split case (Theorems 1.1 and 1.5 with Sections 4.1–4.2) over the cyclotomic Φ₃ construction. For the same q its interval term √(p/q) is far smaller than √p/q^{1/4}, it needs no extension field and no supplied representation of F_{p³}, and p splits completely in Q(ζ_q). Tal's lower-half routine for n ≤ (p−1)/2 chooses the nearest multiple bK of K = (p−1)/q. It then computes K! as an interval of length K, computes (bK)! = (−1)^{b−1} ρ(J_b(χ)) (K!)^b from an addition chain of binary Jacobi sums, and finishes with a correction interval of length at most K/2.

## 6. The rounded-third specialization

**Setting.** Let p ≡ 5 (mod 6) be prime, q ≥ 5 a prime dividing p − 1 (so q ≠ 3), K = (p−1)/q ≥ 4, and y_c = (cK)! for 0 ≤ c ≤ q. Let η ∈ F_p have order q; the implementation takes η = x^K for the least x ≥ 2 with x^K ≠ 1. Let ρ: Z[ζ_q] → F_p send ζ_q ↦ η, and let χ be the order-q character with ρ(χ(x)) = x^{−K}. Define J(χ^u, χ^v) = Σ_x χ^u(x) χ^v(1−x), with χ^k(0) = 0.

**Lemma 1 (binomial relation) [proved here; classical].** For u, v ≥ 1 with u + v < q, ρ(J(χ^u, χ^v)) = −binom((u+v)K, uK) in F_p. *Proof.* ρ(J) = Σ_{x≠0,1} x^{A}(1−x)^{B} with A = (q−u)K and B = (q−v)K. Expanding (1−x)^B, the only exponent A + k ≤ A + B < 2(p−1) that is divisible by p − 1 is k = uK, so ρ(J) = −(−1)^{uK} binom(B, uK). Then B ≡ −1 − vK (mod p) and binom(−1−vK, uK) = (−1)^{uK} binom((u+v)K, uK). ∎ Combined with Wilson's theorem in the form y_c y_{q−c} = (−1)^{cK+1}, this gives the triple form

$$y_u\,y_v\,y_x=\frac{(-1)^{(u+v)K}}{\rho\,J(\chi^u,\chi^v)}\qquad(u+v+x=q). \tag{6.1}$$

**Galois evaluation.** Since σ_t J(χ, χ^w) = J(χ^t, χ^{tw}) and ρ∘σ_t is evaluation at η^t, one algebraic integer J_w = J(χ, χ^w) yields (6.1) for every triple (⟨t⟩, ⟨tw⟩, ⟨−t(1+w)⟩) that sums to q. This is about (q−1)/2 relations per class w, at a cost of O(q) field operations each.

**Reconstruction [background with a certificate proved here].** By Stickelberger's theorem in the split case (Tal 2026, Proposition 2.4; van Wamelen 2002, Theorem 5), (J(χ^u, χ^v)) = ∏_{t∈S} 𝔭_t, where 𝔭_t = (p, ζ − η^t) and S = {t : ⟨ut⟩ + ⟨vt⟩ ≥ q}. The ideal lattice is the kernel of f ↦ (f(η^t))_{t∈S} mod p, with determinant p^{(q−1)/2}. Under the trace form, every nonzero x in the ideal satisfies Tr(x x̄) ≥ (q−1) N(x)^{2/(q−1)} ≥ (q−1)p, by the AM–GM inequality and N(x) ≥ N(𝔞). Equality holds exactly when x generates the ideal and all |σx|² = p, that is, for the 2q root-of-unity multiples of J (Kronecker). This is Lenstra's observation in van Wamelen's Section 7.

The implementation reduces the integral embedding E(x) = q(x, 0) − (Σx)·1 ∈ Z^q, for which |E(x)|² = q·Tr(x x̄), with FLINT's LLL. It accepts a vector only if x·x̄ = p holds exactly in Z[ζ_q], which together with membership certifies x = εJ with ε a root of unity. It then selects ε by van Wamelen's Theorems 6, 8 and 9. The lift of εJ of degree < q with value p − 2 at 1 is integral only for ε ∈ μ_q, and among those the coefficient condition Σ i·a_i ≡ 0 (mod q) holds only for ε = 1. The code enumerates the 2q twists at O(q²) integer cost and requires uniqueness. The representation is q − 1 integers of absolute value below about √((q−1)p). In the brute-force tests the reconstructed sums agreed coefficient by coefficient with direct summation for all 27 810 cases with p < 3000 and q ≤ 31, and every binomial relation held [tested]. Correctness never depends on LLL. If LLL misses the minimum the step fails loudly; it never returns a guess.

**Anchors [proved here from background].** Write Z = m! and let b be the grid index nearest m. Then Z = y_b I_m^{s_m}, where I_m is the product strictly between bK and m. Its length is exactly (K−1)/3 if q ≡ 1 (mod 3) and (K+1)/3 if q ≡ 2 (mod 3), since 3m = qK − 1. The torsion of the grid, the μ_q-ambiguity of K! left by Jacobi sums, is removed by one of two anchors. These replace Tal's interval of length K.

*Anchor dup6 (all p).* Gauss's multiplication formula with M = 2 at x = 1/3 (Robert, 2000, §7.1) gives Γ_p(1/6)Γ_p(2/3) = ε₂ 2^{1−R(1/3)} Γ_p(1/3). With reflection, R(1/3) = (p+1)/3, R(1/6) = (p+1)/6 and ε₂² = (−1)^{(p+1)/2}, this becomes

$$\left(\frac{((p-5)/6)!}{(m!)^2}\right)^{2}=(-1)^{(p+1)/2}\,4^{\,1-(p+1)/3}, \tag{6.2}$$

in which the sign of H has been squared away. The 1/6-point lies at distance (K∓4)/6 from the grid.

*Anchor dup12 (p ≡ 5 mod 12).* Round-2 C5 gives (m!/N!)⁴ = a² with a the odd part of p = a² + b². Squaring the product of its two Gauss-multiplication relations and using Wilson's theorem gives (m!·(5N+2)!)⁴ = (16a²)^{−1}. In that computation 3^{−6q₀} = −1, 2^{−(p−3)} = 4 and Γ_p(1/4)⁴ = −4a² from Gauss's congruence binom(2q₀, q₀) ≡ 2a. Whichever conductor-12 point lies at distance (K∓4)/12 from the grid is used: N! for q ≡ ±1 (mod 12) and (5N+2)! for q ≡ ±5 (mod 12). Both identities were checked at all 2408 primes p ≡ 5 (mod 12) below 10^5 [tested].

**Theorem T3 (exact signed acquisition) [proved here].** Let R be the integer matrix whose rows are the Wilson rows, the triple rows (6.1) of one or more Galois classes w, and one anchor row. The anchor row is 2e_{b₆} − 4e_b for dup6, or 4e_b ∓ 4e_{b₁₂} for dup12. Suppose λ ∈ Z^{rows} satisfies λ^T R = k e_b with k ∈ {1, 3}. Then y_b^k = ∏_i val_i^{λ_i}, where val_i is the known right-hand side of row i, and

$$c_p=2\big(y_b^{3}\,I_m^{3s_m}\big)^{-1},\qquad a_L=\tfrac34 c_p,\qquad m!=(2/c_p)^{(2p-1)/3}. \tag{6.3}$$

*Proof.* Each row is an exact multiplicative identity among the y_c in F_p^×, so the integer combination is exact. Then y_b³ is obtained as y_b³ directly (k = 3) or as the cube (k = 1); no root is extracted. The cube root in (6.3) is unique because 3 ∤ p − 1. ∎

**Theorem (existence of plans) [proved here].** For every prime q ≥ 5 and either anchor, a plan with k = 1 exists once all Galois classes are allowed. *Proof.* Let D₀ = {v : Σ_c c·v_c ≡ 0 (mod q)}. Every Wilson and triple row lies in D₀. Conversely, e_{j+1} − e_j − e₁ is the difference of the Wilson row for j + 1 and the triple row (j, 1, q−j−1). Hence e_a − a e₁ lies in the span, and so does q e₁ = (e₁ + e_{q−1}) − (e_{q−1} − (q−1)e₁). These elements generate D₀, so the span equals D₀. The anchor row has degree ≡ ±1 (mod q); for example 2b₆ − 4b = −(q ∓ 1). Hence e_b ≡ b e₁ ≡ ±b·(anchor) modulo D₀. ∎ The span equals D₀ exactly for every prime q ≤ 61 by integer HNF [computed]. Tal's addition-chain reconstruction needs O(log q) classes. The stronger *single-class* statement, that w = 1 alone suffices with k ∈ {1, 3}, was computed for every prime q ≤ 89 under both anchors and for q ≤ 97 under dup6. The plans are frozen in `r3/PLANS_R3.json` and re-checked in integers on every use. For larger q it is [open], but it can be checked in poly(q) time, and the theorem above gives a fallback.

**Cost (supplied q) [proved here].** The cost has five parts. The search for η takes at most the least non-q-th-power number of exponentiations. One certified Jacobi sum costs an O(q³) ideal basis, LLL in dimension q with entries below qp (poly(q, log p) bit operations; FLINT's `fmpz_lll` is an L²-type floating-point LLL in the sense of Nguyen and Stehlé, 2009), an O(q²) certificate and an O(q²) twist selection. Evaluation at all η^t costs O(q²) field operations. Two interval products, of lengths (K∓1)/3 and (K∓4)/6 or (K∓4)/12, cost O(M(√(p/q)) log p) field operations by the block engine. Assembly needs O(q log p) field operations, with the λ_i reduced modulo p − 1; they reach about 2^39 at q = 79. For bounded q the total is therefore O(M(√(p/q)) log p) field operations plus O_q(polylog p): a constant-factor gain, with no exponent change. Each field operation on a word-size p costs O(1) word operations in the implementation, and O(M_Z(log p)) bit operations in general.

For q growing with p, the LLL step is not proved to succeed. A rigorous Õ(q^c + √(p/q)) bound needs Tal's Theorem 1.5 (Lenstra–Silverberg) in place of LLL. That recovers Tal's Theorem 1.1 at n = m with the anchor saving in the interval term, and with exactly Tal's unspecified exponent.

**Interval work compared.** In the block-engine model, where a length-ℓ interval costs ∝ √ℓ, the interval costs in units of √K are as follows.

| Route at n = m | Interval lengths | Cost in units of √K |
|---|---|---|
| Native m! (single interval) | qK/3 | 0.577√q |
| Half-interval (round 2) | qK/6 + class number | 0.408√q |
| Tal's lower-half routine | K (for K!) + (K∓1)/3 | 1.577 |
| T3 with dup6 | (K∓1)/3 + (K∓4)/6 | 0.985 |
| T3 with dup12 | (K∓1)/3 + (K∓4)/12 | 0.866 |

**What the rounded third does and does not buy.** The rounded-third symmetry does not shorten the target interval. By the corollary of Theorem C6 (Section 8), any interval from the class of 1/3 to the q-grid has length at least p/(3q) − 1, and (K∓1)/3 attains this within one. A generic n lies at a distance spread over [0, K/2], with mean K/4, so the target m is a slightly harder than average instance. The saving is in the anchor. For a generic n the analogous torsion anchors would be the 1/2-point via H², at distance K/2, or the 1/4-point via a², at distance K/4. That generic refinement is a remark here, not implemented. For m, the duplication and quarter relations tie the 1/6 and 1/12 points to m! itself, and those points lie at K/6 and K/12. This is where the rounded third, the half-factorial anchor (through H²) and the nodal ratio (through N!) actually reduce work relative to Tal's generic routine. The class number H itself is not needed.

## 7. The p-only algorithm and its scope

`r3/acquire_r31.py` trial-divides p − 1 by the 22 primes 5 ≤ q ≤ 89 and admits q with K ≥ 10^4. It picks the q minimizing a frozen, development-calibrated cost prediction: a measured lattice-cost table plus f(L) = 1.93·10^{−7}·L^{0.673} s per interval. It uses T3 only if this beats the fallback prediction. The fallback is the unconditional half-interval route when its class number is in the `qfbclassno` range, otherwise the FLINT nodal route. In GRH mode the fallback is the GRH half-interval route. If the lattice chain raises, the call degrades to the next admissible q and then to the fallback, and records this. The policy affects only speed. Finding the divisor costs 22 divisions, and no factorization of p − 1 is needed.

**Proposition (density in the progression) [proved here].** The density, among primes p ≡ 5 (mod 6), of those for which p − 1 has a prime factor in a finite set Q of primes ≥ 5 is 1 − ∏_{q∈Q}(1 − 1/(q−1)). *Proof.* By the Chinese remainder theorem, the residue classes modulo 6∏q with p ≡ 5 (mod 6) and p ≢ 1 (mod q) for all q number ∏(q−2), out of ∏(q−1) classes with p ≡ 5 (mod 6). Dirichlet's theorem equidistributes primes among them. ∎ This gives 0.6783 for Q = [5, 89], 0.4854 for [11, 89] and 0.2955 for [23, 89]. It is a statement about admissibility, not about speed. No proportion theorem for a q growing with p is claimed within the progression.

## 8. Audit of Theorem C6 and what it does not prove

C6 was re-implemented independently in exact rational arithmetic (`r3/research/c6_audit.py`). Φ is independent of the auxiliary modulus and odd. It satisfies Raabe's multiplication relations for multipliers up to 12, and all 600 random Gross–Koblitz orbit sums vanish for primes p ≡ 2 (mod 3); Φ([1/3]) = −1/6. At the points used here, Φ([1/6]) = −1/3, Φ([1/12]) = Φ([7/12]) = −1/6 and Φ([11/12]) = 1/6. Φ vanishes at every q-grid point, at 1/2 and at 1/4. Hence every anchor relation in Section 6 is Φ-neutral, as it must be.

**What C6 proves.** In the Q-vector space on symbols [x], the class [1/3] does not lie in the span W of the reflection, multiplication and Gross–Koblitz relations of all conductors prime to p. Consequently no rational exponent vector built from those relations alone expresses Γ_p(1/3)^e with e ≠ 0. Any derivation of c_p in that calculus must contain an interval product between distinct classes, and an interval from a point of denominator M to one of denominator M′ has length at least p/(MM′) − 1.

**Translation to arithmetic mod p.** Four points arise in the translation. First, known constants: the multiplication formula carries ε_M = ∏Γ_p(i/M), which for even M involves Γ_p(1/2) = ±H. Its sign is a class-number quantity, so the formal relation is exact mod p only up to that sign, and this is why the anchors are used in squared form. Second, torsion: membership in W ⊗ Q is a rational statement. Mod p, a vector v with kv in the integer span determines its monomial only up to μ_{gcd(k, p−1)}. The q-torsion of the grid, invisible to C6, is the whole reason an anchor interval is needed, and C6 places no bound on that interval. Third, p-dependent exponents: the residues R(x) depend on p. They enter both the interval lengths, which are linear in p, and constants such as M^{1−R(x)}, which cost O(log p). Fourth, root extraction: dividing an exponent vector by an integer coprime to p − 1 is a rational rescaling, so it cannot circumvent Φ.

**What C6 does not prove.** C6 is not a lower bound for arbitrary algorithms. It does not bound the cost of evaluating an interval: BGS's √ℓ is an upper bound, and an interval might be obtained by a further identity, as in Tal's p + 1 recursion, which halves its argument stage by stage. It says nothing about the cost of the Jacobi sums that the calculus treats as free. It does not imply that a growing conductor is necessary for every sub-√p method; it implies this only for derivations in the stated calculus under the cost assumption ℓ ↦ √ℓ. C7 remains an empirical relation lattice at conductor 12 on finite prime ranges, not a proof of optimality. Within the calculus named here (q-grid relations, conductor-12 points and squared multiplication relations, with interval cost √ℓ), both T3 intervals are at the C6 corollary's minimum for their points.

## 9. Secondary target: the residual quarter sign

**Exact reformulation [proved here].** For p ≡ 5 (mod 12) let r = m!/N!. Then r² = (−1)^{(h(−3p)−2)/4} a (Section 3), so the two candidates are ±r. Write v = v₂(p−1) and e = (p−1)/2^v. Then r ↦ −r multiplies the 2-Sylow component r^e by (−1)^e = −1. The residual bit is therefore exactly the value of the character of order 2^v at r, relative to a canonical square root of the known (r²)^e. In class B (p ≡ 5 mod 8) this is the quartic character χ₄(m!/N!). If n_k counts the j ∈ (N, m] with χ₄(j) = i^k, then χ₄(r) = i^{n₁+2n₂+3n₃}. The exponent is fixed by the length, the Legendre sum S₂ and the Gaussian integer S₄ = Σ_{N<j≤m} χ₄(j); the identity was verified at 2250 primes. By the Pólya–Fourier expansion, S₄ is an explicit Z[i]-combination of the generalized Bernoulli numbers B_{1,χ₄ψ} with ψ running over characters modulo 12.

**First exact failure.** Class-number formulas give only norms: the relative class numbers of the quartic CM fields cut out by χ₄ψ are products of |B_{1,χ₄ψ}|². What the bit needs is the residue of the Gaussian integers themselves modulo a power of (1+i), that is, their phase, and no class-group computation found here supplies it. Direct computation is O(p). Empirically [tested, 19 610 development primes p ≡ 5 (mod 12) below 10^6], the bit is balanced (4857 of 9790 positive in class B, 4913 of 9820 in class C). It is not a function of any tested invariant tuple: (a, b) mod 24; (a, b) mod 48 with h(−3p) mod 32; p mod 96 with (a, b) mod 24 and h(−3p) mod 64; or quadratic and quartic data of 2 and 3 with (a, b) mod 8 and h(−3p) mod 16. Every invariant group contains both values. The first collisions are recorded in `r3/evidence/QUARTER_SIGN_DEV.json`; for (a, b) mod 24 in class B, p = 173 and p = 653 share (13, 2) but have opposite bits. Here b is normalized by Williams and Currie's convention b ≡ aH (mod p), which uses the now-proved H.

**Why it matters.** With the bit, the Tal grid would need only the conductor-12 interval of length about K/12, since (m!)⁴ follows from N! and a, against K/3 + K/12 now, an interval-cost reduction of 3.0×. The bit was not obtained.

## 10. Exact evidence

**Development (excluded from confirmation).** The complete input ledger is `r3/evidence/LEDGER_R3_1.json`. It holds all primes below 2·10^5, all primes p ≡ 5 (mod 12) below 10^6, the 199 explicit round-1 and round-2 primes, 61 explicit round-3 pre-freeze development primes (timing, lattice-cost and probe primes, including scratch probes regenerated from their rules), the 145 primes selected by the R3 rule in run 1, and 283 post-freeze development primes. Before the freeze, T3 was checked against FLINT on 8299 dup6 cases and 4182 dup12 cases with p < 2·10^5 and q ≤ 47, and the timing, layout and lattice-cost calibrations were run on development primes (`DEV_TIMING.json`, `DEV_LAYOUT.json`, `DEV_SVP_TABLE.json`). Separate channels were faster than a shared evaluation tree, or within 3% of it, in every layout test, and up to 1.4× faster for dup12, so the separate layout was frozen. The development checks quoted in Sections 6 and 10 were first run inline before the freeze (the R3.1 equivalence after it). They are archived, regenerated with their original rules and inputs, in `r3/research/dev_checks.py` and `r3/evidence/DEV_CHECKS.json`. These checks are the 27 810 brute-force Jacobi sums, the 12 481 development cases of T3, the 2408-prime anchor check, the lattice computations and the 2098-case equivalence.

**Freeze R3 and its failed confirmation.** `CANDIDATE_R3.md` and 31 further files were hash-frozen in `r3/FREEZE_R3.json` before any confirmation prime was selected. Run 1 completed 88 cases, all exact. It covered sets S, M, L, E1, E2 and E4 for class A, and S and M for class B with q ≤ 83. It then stopped at class B, q = 89, p = 3000013781. FLINT LLL with δ = 0.99 missed the minimum; its best vector had 18 times the minimal norm. The frozen exact-enumeration fallback (PARI `qfminim`, flag 0) is documented to require d·max|G|² < 2^53, so it rejected Gram entries of size (qp)². No value was returned. The frozen candidate therefore **did not pass** confirmation (`CONFIRMATION_R3_RUN1_SUMMARY.json`, `CONFIRMATION_R3_run1_FAILED.log`).

**Post-freeze development and amendment R3.1.** On 12 random development primes per prime q ≤ 89, LLL missed the minimum at δ = 0.99 for q = 83 (1 of 12) and q = 89 (3 of 12), and at δ = 0.999 for q = 89 (1 of 12), at 2–4% extra cost. `qfminim` with flag 2 did not finish within ten minutes on the failing case. Amendment R3.1 (`CANDIDATE_R3_1.md`, `r3/FREEZE_R3_1.json`) changes only the lattice step. It runs δ = 0.999, then δ = 0.9999, then up to four seeded re-randomised bases, each certified exactly, and otherwise raises. It also adds an interface that degrades instead of raising and a conservative cost table. It is strictly additive: every R3-frozen file still verifies. The chain recovered every observed miss, and its Jacobi sums were byte-identical to the frozen module's on 2098 development cases.

**Confirmation R3.1 (fresh; all PASS).** Every prime was the first one, outside the R3.1 ledger, at or above its bound in its class. Its m!, c_p, a_L and D were compared with FLINT's `n_factorial_fast_mod2_preinv` reference for T3 (every applicable anchor), for every half-interval route, for the nodal route and for the interface in both modes. Set S was also checked against an independent linear m! loop, the defining binomial binom(2L, L) 8^{−L}, the round-1 Wronskian product and the Atkin recurrence for D. Class numbers were cross-checked against `quadclassunit` everywhere and against the form count for |D| < 2·10^9.

| Set | Rule | Primes (A/B/C) | Result |
|---|---|---|---|
| S | ≥ 2.5·10^6, q ∈ primes 5–47, independent checks | 13/13/13 | PASS |
| M | ≥ 4·10^9, q ∈ primes 5–89 | 22/22/22 | PASS |
| L | ≥ 4·10^11, q ∈ {11, 23, 47, 89} | 4/4/4 | PASS |
| E1 | ≥ 5·10^10, no prime 5 ≤ q ≤ 89 divides p−1 | 2/2/2 | PASS, fallback route |
| E2 | ≥ 4·10^9, q² \| p−1, q ∈ {5, 7, 11} | 3/3/3 | PASS |
| E3 | class A, ≥ 3.5·10^5, divisor present but K < 10^4 | 2/–/– | PASS, fallback route |
| E4 | ≥ 2·10^10, ten generic primes per class | 10/10/10 | PASS |

The 164 primes gave 255 exact T3 checks. These covered every anchor kind and both plan types: dup6 with k = 1 (113) and k = 3 (39), N with k = 1 (30) and k = 3 (15), and 5N+2 with k = 1 (47) and k = 3 (11). Class numbers came from `qfbclassno` in 154 evaluations and from the form count in 64. The interface chose T3 for 123 primes, the half-interval route for 21 and the nodal route for 20, with no degradations. A labelled regression block reran the run-1 failure (p = 3000013781) and the development miss (p = 920889975821), both at q = 89 with both anchors; all four checks succeeded. This block is not counted as confirmation. These primes are disjoint from the recorded project inputs; nothing is claimed about their use elsewhere.

## 11. Matched benchmarks

**Policy.** Benchmarks ran only after the R3.1 confirmation passed, on the same single machine, under the frozen rule in `r3/benchmark_r3_1.py`. Every method returns c_p, and all input-dependent work is inside the timed region: the η search, lattice reduction, certificate, twist selection, intervals, assembly, class numbers, Cornacchia and the final normalization. The interface's divisor search and selection are included as well.

*Cold* means a fresh Jacobi context, fresh FLINT trees and the form-count sieve cleared before every call. Three items of p-independent process state were created before timing: the PARI interpreter object, the loaded FLINT library and the frozen plan table, whose plans are still re-checked in integers inside each call. *Warm* means a second call at the same p that reuses the cached Jacobi sum; it measures amortized use at a fixed p. The intervals are recomputed in warm calls, and warm calls are never mixed with cold rows.

Each method was sampled five times (three for set B2), with the method order rotated; all samples are in `r3/evidence/BENCHMARK_R3_1.json`. Medians in milliseconds are shown below. "HI uncond." is the half-interval route with the unconditional class-number policy. Outside the `qfbclassno` range it was timed once with the reduced-form count, marked "(forms, 1)". "T3" is the new route with the q given (supplied-q), and "API" is the p-only interface with its own choice of q or fallback. These are timings of these implementations on one machine, not universal speed ratios.

**Set B1, matched supplied-q (confirmation sets L near 4·10^11 and M near 4·10^9).**

| p | cls | q | native | block m! | nodal | HI (GRH) | HI uncond. | T3 dup6 | T3 dup12 | T3 warm | API (route q) | API | native/T3 | HI-GRH/T3 | native/API |
|---:|:-:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 400000002359 | A | 11 | 5001 | 5207 | 4153 | 3460 | 13073 (forms, 1) | 2019 | – | 1976 | T3 11 | 2050 | 2.48 | 1.71 | 2.44 |
| 400000002719 | A | 23 | 4935 | 5276 | 4383 | 3575 | 11758 (forms, 1) | 1318 | – | 1123 | T3 29 | 1157 | 3.74 | 2.71 | 4.26 |
| 400000015799 | A | 47 | 5141 | 5262 | 4221 | 3271 | 12576 (forms, 1) | 817 | – | 784 | T3 47 | 884 | 6.29 | 4.00 | 5.82 |
| 400000008503 | A | 89 | 4942 | 5265 | 3963 | 3297 | 11637 (forms, 1) | 2004 | – | 473 | T3 89 | 1953 | 2.47 | 1.65 | 2.53 |
| 400000000709 | B | 11 | 4852 | 4939 | 3980 | 3315 | 14035 (forms, 1) | 1943 | 1607 | 1538 | T3 11 | 1596 | 3.02 | 2.06 | 3.04 |
| 400000004237 | B | 23 | 5165 | 5108 | 4033 | 3268 | 14646 (forms, 1) | 1234 | 1005 | 997 | T3 47 | 723 | 5.14 | 3.25 | 7.15 |
| 400000004237 | B | 47 | 4883 | 5027 | 4089 | 3363 | 14808 (forms, 1) | 864 | 715 | 688 | T3 47 | 687 | 6.83 | 4.70 | 7.11 |
| 400000017581 | B | 89 | 4923 | 5124 | 4136 | 3469 | 13656 (forms, 1) | 2032 | 1901 | 415 | T3 89 | 1909 | 2.59 | 1.82 | 2.58 |
| 400000000577 | C | 11 | 4958 | 5157 | 4099 | 3521 | 13221 (forms, 1) | 1944 | 1746 | 1844 | T3 11 | 1608 | 2.84 | 2.02 | 3.08 |
| 400000000097 | C | 23 | 4905 | 5283 | 4183 | 3349 | 13071 (forms, 1) | 1247 | 1068 | 1082 | T3 23 | 1057 | 4.59 | 3.13 | 4.64 |
| 400000000289 | C | 47 | 5179 | 5245 | 4167 | 3217 | 11328 (forms, 1) | 838 | 761 | 626 | T3 47 | 685 | 6.81 | 4.23 | 7.56 |
| 400000069913 | C | 89 | 4953 | 5297 | 4033 | 3281 | 12566 (forms, 1) | 1970 | 1991 | 426 | T3 89 | 1959 | 2.51 | 1.67 | 2.53 |
| 4000000451 | A | 5 | 204 | 247 | 182 | 150 | 140 (qfb) | 128 | – | 127 | T3 29 | 47.7 | 1.60 | 1.18 | 4.28 |
| 4000001039 | A | 11 | 240 | 271 | 211 | 157 | 155 (qfb) | 79.8 | – | 75.4 | T3 11 | 82.5 | 3.00 | 1.96 | 2.91 |
| 4000000427 | A | 23 | 225 | 244 | 194 | 172 | 160 (qfb) | 52.7 | – | 44.1 | T3 23 | 62.1 | 4.27 | 3.26 | 3.63 |
| 4000000619 | A | 31 | 216 | 238 | 193 | 148 | 142 (qfb) | 50.4 | – | 36.2 | T3 31 | 50.0 | 4.29 | 2.94 | 4.33 |
| 4000018943 | A | 47 | 226 | 245 | 193 | 153 | 150 (qfb) | 106 | – | 30.3 | T3 47 | 96.6 | 2.14 | 1.45 | 2.35 |
| 4000004363 | A | 61 | 220 | 260 | 196 | 153 | 148 (qfb) | 242 | – | 33.6 | T3 37 | 63.3 | 0.91 | 0.63 | 3.48 |
| 4000008347 | A | 89 | 244 | 295 | 196 | 157 | 159 (qfb) | 1285 | – | 18.1 | HI  | 157 | 0.19 | 0.12 | 1.56 |
| 4000000661 | B | 5 | 241 | 248 | 185 | 155 | 149 (qfb) | 128 | 112 | 105 | T3 5 | 113 | 2.16 | 1.39 | 2.13 |
| 4000001501 | B | 11 | 221 | 227 | 178 | 138 | 148 (qfb) | 71.4 | 62.1 | 61.6 | T3 11 | 60.5 | 3.56 | 2.22 | 3.65 |
| 4000002221 | B | 23 | 282 | 261 | 220 | 163 | 158 (qfb) | 59.7 | 45.5 | 38.7 | T3 23 | 46.6 | 6.19 | 3.58 | 6.05 |
| 4000006013 | B | 31 | 229 | 257 | 200 | 144 | 154 (qfb) | 51.5 | 44.4 | 31.1 | T3 31 | 42.8 | 5.17 | 3.25 | 5.36 |
| 4000014149 | B | 47 | 227 | 249 | 184 | 148 | 146 (qfb) | 96.4 | 94.0 | 23.9 | T3 13 | 61.2 | 2.41 | 1.57 | 3.70 |
| 4000005461 | B | 61 | 217 | 234 | 190 | 159 | 148 (qfb) | 237 | 260 | 20.4 | T3 11 | 75.5 | 0.92 | 0.67 | 2.88 |
| 4000003541 | B | 89 | 226 | 246 | 189 | 154 | 152 (qfb) | 1295 | 1289 | 15.3 | T3 13 | 60.8 | 0.18 | 0.12 | 3.71 |
| 4000000241 | C | 5 | 228 | 245 | 177 | 148 | 145 (qfb) | 131 | 115 | 113 | T3 5 | 116 | 1.98 | 1.29 | 1.97 |
| 4000001897 | C | 11 | 240 | 262 | 215 | 163 | 155 (qfb) | 81.2 | 66.4 | 77.1 | T3 11 | 66.5 | 3.61 | 2.46 | 3.60 |
| 4000004153 | C | 23 | 240 | 270 | 180 | 145 | 143 (qfb) | 49.0 | 45.0 | 37.1 | T3 23 | 44.4 | 5.33 | 3.23 | 5.41 |
| 4000003409 | C | 31 | 223 | 242 | 193 | 151 | 153 (qfb) | 53.3 | 48.6 | 30.6 | T3 29 | 44.6 | 4.59 | 3.11 | 5.00 |
| 4000006817 | C | 47 | 222 | 251 | 208 | 152 | 144 (qfb) | 102 | 93.2 | 23.8 | T3 13 | 60.5 | 2.39 | 1.63 | 3.68 |
| 4000006193 | C | 61 | 226 | 262 | 198 | 162 | 165 (qfb) | 262 | 262 | 20.9 | T3 29 | 46.2 | 0.86 | 0.62 | 4.89 |
| 4000011017 | C | 89 | 226 | 245 | 190 | 161 | 149 (qfb) | 1277 | 1238 | 16.4 | T3 43 | 75.8 | 0.18 | 0.13 | 2.99 |

B1 summary: native/T3 0.18–6.83 (median 2.84); nodal/T3 0.15–5.71; HI-GRH/T3 0.12–4.70; native/API 1.56–7.56 (median 3.65). In the supplied-q rows, T3 wins at every q at 4·10^11. At 4·10^9 it loses for q = 61 (0.86–0.92× native) and badly for q = 89 (0.18–0.19×): there the cold lattice reduction (about 0.2 s and 1.3 s) dominates intervals that cost only about 15–35 ms, as the warm column shows. The p-only interface avoids every such loss by choosing a cheaper q or the half-interval route; its worst row is 1.56× native. The dup12 anchor beats dup6 in all 16 rows with p ≡ 5 (mod 12) and q ≤ 47, by 2.5–31% (median 15%). At q = 89 near 4·10^11 a warm call costs 0.42–0.47 s against about 2.0 s cold: a single certified J(χ, χ) serves every later factorial query at that p and q.

**Set B2, p-only distribution on generic primes (confirmation set E4 near 2·10^10, and E1 with no admissible q).**

| p | cls | generic | admissible q | API route (q) | native | nodal | HI (GRH) | API | native/API | nodal/API |
|---:|:-:|:-:|---|---|---:|---:|---:|---:|---:|---:|
| 20000000231 | A | yes | 5,7 | T3 7 | 797 | 556 | 492 | 366 | 2.17 | 1.52 |
| 20000000687 | A | yes | – | nodal  | 711 | 633 | 454 | 586 | 1.21 | 1.08 |
| 20000000747 | A | yes | 11 | T3 11 | 753 | 621 | 465 | 260 | 2.90 | 2.39 |
| 20000000903 | A | yes | 7 | T3 7 | 687 | 616 | 439 | 328 | 2.09 | 1.88 |
| 20000000927 | A | yes | – | nodal  | 706 | 570 | 492 | 566 | 1.25 | 1.01 |
| 20000001143 | A | yes | 11 | T3 11 | 688 | 630 | 430 | 244 | 2.82 | 2.58 |
| 20000001167 | A | yes | – | nodal  | 721 | 579 | 460 | 557 | 1.29 | 1.04 |
| 20000001311 | A | yes | 5,41 | T3 41 | 682 | 586 | 463 | 139 | 4.89 | 4.21 |
| 20000001383 | A | yes | – | nodal  | 679 | 566 | 453 | 572 | 1.19 | 0.99 |
| 20000001443 | A | yes | – | nodal  | 774 | 569 | 462 | 588 | 1.31 | 0.97 |
| 50000000423 | A | E1 | – | nodal  | 1227 | 1002 | 838 | 1041 | 1.18 | 0.96 |
| 50000000747 | A | E1 | – | nodal  | 1246 | 1056 | 917 | 1031 | 1.21 | 1.02 |
| 20000000333 | B | yes | 13 | T3 13 | 731 | 643 | 455 | 187 | 3.91 | 3.44 |
| 20000000357 | B | yes | 7,67 | T3 7 | 724 | 569 | 468 | 290 | 2.50 | 1.96 |
| 20000000549 | B | yes | 11,31 | T3 31 | 704 | 558 | 478 | 114 | 6.18 | 4.90 |
| 20000000789 | B | yes | – | nodal  | 731 | 636 | 498 | 589 | 1.24 | 1.08 |
| 20000001149 | B | yes | 29 | T3 29 | 741 | 563 | 454 | 124 | 5.96 | 4.53 |
| 20000001173 | B | yes | – | nodal  | 691 | 599 | 474 | 694 | 1.00 | 0.86 |
| 20000001221 | B | yes | 5,17 | T3 17 | 664 | 581 | 462 | 170 | 3.90 | 3.41 |
| 20000001533 | B | yes | 7,23 | T3 23 | 779 | 642 | 482 | 153 | 5.08 | 4.18 |
| 20000001677 | B | yes | – | nodal  | 739 | 603 | 530 | 572 | 1.29 | 1.05 |
| 20000001701 | B | yes | 5,7 | T3 7 | 708 | 679 | 555 | 309 | 2.29 | 2.20 |
| 50000000189 | B | E1 | – | nodal  | 1402 | 1135 | 877 | 1161 | 1.21 | 0.98 |
| 50000000333 | B | E1 | – | nodal  | 1275 | 1117 | 863 | 1040 | 1.23 | 1.07 |
| 20000000369 | C | yes | – | nodal  | 731 | 598 | 552 | 575 | 1.27 | 1.04 |
| 20000000561 | C | yes | 5 | T3 5 | 698 | 581 | 503 | 408 | 1.71 | 1.43 |
| 20000000873 | C | yes | 79 | nodal  | 715 | 651 | 487 | 589 | 1.22 | 1.11 |
| 20000001017 | C | yes | 17,37 | T3 37 | 709 | 563 | 486 | 119 | 5.96 | 4.73 |
| 20000001377 | C | yes | 83 | nodal  | 698 | 652 | 482 | 643 | 1.09 | 1.01 |
| 20000001473 | C | yes | 11 | T3 11 | 741 | 570 | 500 | 201 | 3.68 | 2.83 |
| 20000001569 | C | yes | – | nodal  | 682 | 593 | 445 | 601 | 1.13 | 0.99 |
| 20000001689 | C | yes | – | nodal  | 696 | 554 | 440 | 589 | 1.18 | 0.94 |
| 20000001809 | C | yes | 23 | T3 23 | 689 | 615 | 441 | 136 | 5.06 | 4.52 |
| 20000002313 | C | yes | – | nodal  | 672 | 563 | 485 | 578 | 1.16 | 0.97 |
| 50000000417 | C | E1 | – | nodal  | 1174 | 1027 | 899 | 1017 | 1.15 | 1.01 |
| 50000001137 | C | E1 | – | nodal  | 1223 | 1062 | 871 | 1031 | 1.19 | 1.03 |

B2 generic summary (30 primes): T3 chosen for 16; native/API median 1.90 (range 1.00–6.18); nodal/API median 1.47 (range 0.86–4.90). The losses in this set are rows where the interface fell back to the nodal route, so "API" and "nodal" are the same algorithm. The 0.86–1.08 spread of nodal/API there is run-to-run variation, with three samples each. Outside the `qfbclassno` range, the GRH half-interval route is 1.08–1.47× faster than the nodal fallback; the interface uses it only in mode 'grh', labelled conditional.

**Set B3, unconditional half-interval repair at the round-2 source primes near 2·10^9.** These primes were round-2 confirmation inputs; here they are benchmark inputs only.

| p | cls | native | nodal | HI uncond. (qfb) | HI (GRH) | HI forms (cold) | API (route q) | API | native/HI-qfb | nodal/HI-qfb |
|---:|:-:|---:|---:|---:|---:|---:|---|---:|---:|---:|
| 2000000063 | A | 126 | 110 | 93.6 | 91.9 | 323 | HI  | 96.1 | 1.35 | 1.17 |
| 2000000141 | B | 126 | 107 | 93.4 | 94.5 | 432 | T3 5 | 68.6 | 1.35 | 1.14 |
| 2000000033 | C | 130 | 110 | 95.5 | 96.5 | 316 | HI  | 96.1 | 1.36 | 1.15 |

At these primes `qfbclassno` gives exactly the GRH route's speed without GRH. The unconditional half-interval method is 1.35–1.36× faster than FLINT native and 1.14–1.17× faster than the FLINT nodal anchor, so the round-2 advantage survives unconditionally. The cold reduced-form count loses to every other method, as in round 2. The interface chose the new route for 2000000141, since 5 | p − 1.

**Set B4, small-p crossover (the first prime with an admissible q at or above 10^6, 10^7 and 10^8 per class).**

| p | cls | API route (q) | native | nodal | API | native/API |
|---:|:-:|---|---:|---:|---:|---:|
| 1000151 | A | T3 5 | 0.3 | 0.4 | 0.6 | 0.53 |
| 10000103 | A | T3 7 | 2.1 | 2.6 | 1.8 | 1.17 |
| 100000223 | A | T3 17 | 12.9 | 11.0 | 5.0 | 2.58 |
| 1000133 | B | T3 7 | 0.4 | 0.5 | 0.6 | 0.56 |
| 10000229 | B | T3 7 | 2.1 | 2.1 | 1.5 | 1.41 |
| 100000421 | B | T3 13 | 12.0 | 11.2 | 4.6 | 2.58 |
| 1000313 | C | HI  | 0.3 | 0.4 | 0.7 | 0.47 |
| 10000121 | C | T3 13 | 2.1 | 2.1 | 1.7 | 1.29 |
| 100000049 | C | HI  | 17.6 | 17.1 | 9.1 | 1.93 |

Near 10^6 the fixed costs lose to FLINT's native factorial: PARI and FLINT calls, the plan check and the lattice step for small q. At 10^6 the interface runs at 0.47–0.56 times native's speed. At 10^7 it is 1.17–1.41× faster and at 10^8 1.9–2.6× faster. The crossover therefore lies between 10^6 and 10^7 and was not located more precisely. The frozen policy does not model this regime, and near 10^6 the native factorial is the better choice. No timing is extrapolated beyond the measured range.

## 12. Interface

`python3 -m r3.acquire_r31 p [--mode unconditional|grh] [--q Q] [--route auto|tal|hi|nodal]`, or `acquire_aL(p, mode, q, route)` in Python. It returns a dictionary with `a_L`, `c_p`, `m_factorial`, `D` (the signed endpoint derivative A_n′(0) by the audited round-1 normalization), `route`, `q`, `status`, `seconds` and `metadata`. Status is `unconditional` for T3 with 5 ≤ q ≤ 89, the half-interval route with an unconditional class number, or the nodal route. It is `GRH-conditional` for the half-interval route with `quadclassunit`, and `experimental` for T3 with a user-forced q outside the frozen range. The metadata records the anchor, the plan type, the residual lengths, the policy's predictions, any degradation and the class-number backend. Primality is the caller's contract; `r3.common.is_prime` is a deterministic Miller–Rabin proof below 3.3·10^24 (Sorenson & Webster, 2017).

## 13. Status ledger

| Claim | Status |
|---|---|
| Round-2 (\*) and the p ≡ 17 (mod 24) route | [background] Williams & Currie (1982) Lemma 14(c), from OCR plus exact checks; algebraic equivalence and quarter consequence [proved here]; [tested] 19 610 primes |
| (m!/p) = (−1)^{(h(−3p)−2)/4}, h(−3p) ≡ 2 (mod 4) | [background] Pólya–Fourier with Dirichlet; Rédei |
| Unconditional qfbclassno backend, \|D\| < 2·10^10 | [background] PARI documentation; policy implemented |
| Lemma 1, the triple relations (6.1) and the Galois evaluation | [proved here]; classical in substance |
| Stickelberger factorization; van Wamelen's selection | [background]; [tested] 27 810 brute-force sums |
| Reconstruction certificate (AM–GM plus Kronecker) | [proved here] (Lenstra's idea, van Wamelen §7) |
| Anchor identities dup6 and dup12 | [proved here] from Gauss multiplication, C5, Wilson and Gauss's congruence; [tested] 2408 primes |
| T3 exact signed acquisition of m!, c_p, a_L and D | [proved here]; [tested] 12 481 development cases; confirmation R3.1 PASS (164 primes, 255 checks) |
| Plans exist with k = 1 for every prime q ≥ 5 (all classes) | [proved here] |
| Single-class plans for q ≤ 89 (both anchors) and q ≤ 97 (dup6) | [computed]; general q [open] |
| T3 cost, bounded q: O(M(√(p/q)) log p) plus O_q(polylog p) | [proved here]; constant factor only |
| T3 with growing q at a rigorous Õ(q^c + √(p/q)) | requires Tal Thm 1.5 (unrefereed) in place of LLL; exponent unspecified |
| Density 0.6783 of admissible p ≡ 5 (mod 6) | [proved here] by Dirichlet with CRT |
| Frozen R3 implementation | confirmation FAILED (lattice fallback defect), recorded |
| Tal's theorems as stated | [background, unrefereed]; audited from extracted text only |
| C6 functional and its corollary | [proved here] in round 2; re-checked; scope as in Section 8 |
| Quarter sign via cheap invariants | first exact failures recorded; [open] |
| Unconditional half-interval advantage near 2·10^9 (1.35× native, 1.14–1.17× nodal) | measured, single machine (Section 11, B3) |
| Measured T3 and interface speed-ups, crossover between 10^6 and 10^7 | single machine, these implementations (Section 11) |

## 14. Strongest defensible contribution and the remaining question

The strongest defensible contribution is an implemented, exact and unconditional acquisition of the signed a_L, together with m!, c_p and D. It is the split case of Tal's construction specialized to the rounded third, with the length-K torsion interval replaced by duplication or quarter anchors that exist because of the rounded-third structure. The reconstruction uses one certified Jacobi sum, and the method needs no class number. An admissible prime q ∈ [5, 89] exists for 68% of primes p ≡ 5 (mod 6), and the interface used the new route for 16 of 30 generic primes near 2·10^10. Where it is used at p ≥ 10^7, it gives divisor-dependent constant-factor speed-ups over every round-1 and round-2 route: the median is 1.90× over FLINT native on the generic sample, and the gain reaches 7.6× in matched rows (Section 11). Otherwise the interface falls back correctly to an exact route. Alongside it, the round-2 conjecture (\*) is now a theorem, the half-interval route's advantage near 2·10^9 is unconditional, and the one candidate failure is on record.

The precise remaining question is this. *For p ≡ 5 (mod 12), with v = v₂(p−1), can the value of the order-2^v residue character at m!/N!, equivalently Σ_{N<j≤m} χ₄(j) modulo a power of (1+i) for p ≡ 5 (mod 8), be computed in time p^{1/2−δ}, without an equivalent long product?* A positive answer would remove the K/3 interval from the specialization, leaving one interval of about K/12, and would also settle the round-2 quarter sign.

## 15. Reproduction

Install with `pip install python-flint==0.9.0 cypari2 sympy` (Python 3.10 or later; pip may need `--break-system-packages`). From the package directory, `python3 audit.py` checks the round-1 and round-2 freezes. `python3 r3/audit_r3.py` checks both round-3 freezes and the round-3 manifest. `python3 r3/confirm_r3_1.py` reruns the frozen R3.1 confirmation (about 20 minutes) and `python3 r3/benchmark_r3_1.py` the benchmarks (about 40 minutes; timings will differ). `python3 -m r3.acquire_r31 400000017581` runs the interface. The development scripts are in `r3/research/`. Regenerating evidence changes timings and output hashes but never a freeze. Do not overwrite a freeze to conceal a source change; the R3 freeze still verifies against the original bytes.

## References

Berndt, B. C. (1976). Classical theorems on quadratic residues. *L'Enseignement Mathématique, 22*, 261–304.

Berndt, B. C., Evans, R. J., & Williams, K. S. (1998). *Gauss and Jacobi sums*. Wiley.

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793

Davenport, H. (2000). *Multiplicative number theory* (3rd ed., revised by H. L. Montgomery; Graduate Texts in Mathematics, Vol. 74). Springer.

FLINT team. (2026). *FLINT: Fast Library for Number Theory* (Version 3.6.0, via python-flint 0.9.0) [Computer software]. https://flintlib.org

Kaneko, M., & Zagier, D. (1998). Supersingular j-invariants, hypergeometric series, and Atkin's orthogonal polynomials. In *Computational perspectives on number theory* (AMS/IP Studies in Advanced Mathematics, Vol. 7, pp. 97–126). American Mathematical Society.

Lenstra, A. K., Lenstra, H. W., Jr., & Lovász, L. (1982). Factoring polynomials with rational coefficients. *Mathematische Annalen, 261*, 515–534. https://doi.org/10.1007/BF01457454

Mordell, L. J. (1961). The congruence ((p−1)/2)! ≡ ±1 (mod p). *The American Mathematical Monthly, 68*(2), 145–146. https://doi.org/10.2307/2312481

Nguyen, P. Q., & Stehlé, D. (2009). An LLL algorithm with quadratic complexity. *SIAM Journal on Computing, 39*(3), 874–903. https://doi.org/10.1137/070705702

PARI Group. (2025). *PARI/GP* (Version 2.17.2, via cypari2 2.2.4) [Computer software]. https://pari.math.u-bordeaux.fr

Rédei, L. (1934). Arithmetischer Beweis des Satzes über die Anzahl der durch vier teilbaren Invarianten der absoluten Klassengruppe im quadratischen Zahlkörper. *Journal für die reine und angewandte Mathematik, 171*, 55–60.

Robert, A. M. (2000). *A course in p-adic analysis* (Graduate Texts in Mathematics, Vol. 198). Springer. https://doi.org/10.1007/978-1-4757-3254-2

Sorenson, J., & Webster, J. (2017). Strong pseudoprimes to twelve prime bases. *Mathematics of Computation, 86*(304), 985–1003. https://doi.org/10.1090/mcom/3134

Tal, Y. (2026). *Computing modular factorials below the square-root barrier* (ECCC Report TR26-211). Unrefereed. https://eccc.weizmann.ac.il/report/2026/211/

van Wamelen, P. (2002). Jacobi sums over finite fields. *Acta Arithmetica, 102*(1), 1–20. https://doi.org/10.4064/aa102-1-1

Washington, L. C. (1997). *Introduction to cyclotomic fields* (2nd ed., Graduate Texts in Mathematics, Vol. 83). Springer.

Williams, K. S., & Currie, J. D. (1982). Class numbers and biquadratic reciprocity. *Canadian Journal of Mathematics, 34*(4), 969–988. https://doi.org/10.4153/CJM-1982-070-x
