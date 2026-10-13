# Review of the CM-to-Cartier extension, 12 October 2026

The bounded mathematical result receives a **qualified positive review**. I found no counterexample to the normalized CM-to-Cartier comparison under the submitted separation and integrality hypotheses, to the recovered six slope formulas, or to the new discriminant −7 evaluator. The sign and differential scale are correct. All eleven submitted scripts reran, and their mathematical outputs and validation counters passed inspection. Independent checks also passed. This is an unrefereed assessment, not a claim of specialist certification or priority.

Two statements need mathematical qualification, and the validation runner needs a concrete correction. These do not invalidate the −7 evaluator: its endomorphism has separated eigenvalues at every admitted prime, and its proof uses meromorphic Cartier commutation directly. I recommend retaining this as a separate extension note, applying the corrections below, and sending the result for human review before expanding the programme.

| Claim | Assessment | Limit |
|---|---|---|
| Characteristic-p eigen-equation, Theorem 1 | Correct: λᵖβ = μβ + νH; over F_p, β(λ−μ) = νH | A valid pullback identity and separability are required. Recovering the slope requires λ−μ ≠ 0. |
| Normalization β/H = −(3B/2A)s₂ | Correct under Theorem 5's explicit hypotheses | AB must be invertible for this quotient form. The coefficient is model-dependent; the dimensionless quantity Aβ/(BH) is invariant. |
| Six-family recovery | Exact endomorphism calculations reran and reproduce all six formulas | An alternative derivation sharing the normalized Vélu identity and existing path data, not six independent discoveries. |
| New discriminant −7 family | Sound bounded extension: β = −rH on (−35r²,−98r³) | Prime p ≥ 7, p mod 7 in {1,2,4}; supplied cubic/root conventions must be maintained. |
| Signed −7 trace | Correct classical CM formula, supported by source checks and independent direct counts | The written 2-adic route should be described as an alternative sign algorithm; it does not explicitly derive the displayed Legendre-mod-7 rule. |
| Discriminant −8 control | Correct slope β/H = r on (−30r²,56r³) at ordinary primes | The submission expressly does not certify a separate trace algorithm for this control. |
| Fixed-discriminant table | Correct for the eight supplied tables, including twists and conjugate pairing | This is a fixed-table evaluator, not a method for discovering a generic curve's CM order or treating growing discriminants cheaply. |
| New deterministic speed claim | None established beyond the stated cost contract | The native CM trace route still uses randomized nonresidue search at p ≡ 1 mod 8; Schoof remains the unconditional deterministic fallback. No benchmark was supplied or performed. |
| Novelty | Unresolved; underlying comparison and CM constants are classical | Present the application, normalization, certificates and implementation as the contribution. Do not describe the CM comparison itself as a new theorem of mathematics. |

The submitted note, ledger and archive were read locally. The two standalone Markdown files equal their archive copies byte-for-byte. All 42 manifest entries verified. The source extraction was preserved; execution took place in a separate copy. The retained handover, roadmap and current manuscript conventions were checked. No repository URL or commit was available, and no GitHub repository was inspected or changed. The manuscript and historical failed branches were preserved.

The important sign calculation can be checked without numerical evidence. For a normalized Vélu isogeny with kernel sum σ and degree ℓ, followed by the closing isomorphism (x′,y′) ↦ (x′/u²,y′/u³), the pullback matrix on (ω,η) is

$$M=\begin{pmatrix}u&-\sigma/u\\0&\ell/u\end{pmatrix}.$$

Here ω = dx/y and η = x dx/y. For a degree-two kernel at q the exact differential identity is

$$\phi^*\omega'=\omega,\qquad
\phi^*\eta'=(2x-q)\omega-2\,d\!\left(\frac{y}{x-q}\right).$$

Thus the differential scale is +1, the off-diagonal entry is −q, and applying Cartier gives

$$\beta(u-\ell/u)=-(\sigma/u)H,
\qquad\frac{\beta}{H}=\frac{\sigma}{\ell-u^2}.$$

In characteristic zero the antiholomorphic eigenline is η+cω, where

$$c=\frac{\sigma}{u^2-\ell}=G_2^*(\Lambda).$$

With x = ℘(z), y = ℘′(z)/2, one has ω = 2 dz, η = 2℘ dz, g₂ = −4A and g₃ = −4B. The full-period quasi-period law and the full-period Legendre relation give

$$G_2^*(\Lambda)=\frac{\pi^2}{3\lambda^2}E_2^*(\tau),\qquad
G_2^*(\Lambda)\frac{A}{B}=\frac32\frac{E_2^*E_4}{E_6}.$$

Consequently β/H = −c, with exactly the proposed minus sign and factor 3/2. This derivation depends on exact isogeny identities and the classical period law, not on agreement of approximate complex values. For the −7 seed, q = r(−7+e)/2 and u = (1+e)/2, e² = −7. Since 2−u² = (7−e)/2, q/(2−u²) = −r. For the −8 control, q = 4r and u² = −2, so q/(2−u²) = r. Both quotient equations and scales were checked independently with exact symbolic algebra.

Reduction requires the actual rational maps and closing scale to be integral and defined over the residue field, the degree to remain prime to p, and the two eigenvalues to remain distinct. Merely knowing that a characteristic-zero curve has CM is not a replacement for these conditions. The submitted loops meet them at their eligible primes. The assertion of ordinary reduction additionally uses classical reduction theory; the whole all-prime argument should not be advertised as a proof of CM reduction theory using only elementary algebra. Alternatively, the known fact that H and β have no common zero on a nonsingular short cubic, together with Theorem 1 and separated eigenvalues, gives ordinarity directly.

There is also an algebraic way to justify the class-polynomial identification without turning the analytic matching into a proof. Each exact loop gives an order of discriminant D inside End(E). The only possible overorders have conductor dividing 2, 4 or 8 in the same quadratic field. At depth one, j differs from the maximal-order seed value 0 or 1728. At depths two and three the exact irreducible j polynomial has degree 2 or 4, whereas all proper overorders have class number at most 1 or 2 respectively. The standard CM degree theorem then excludes them. The submitted j polynomial is therefore the class polynomial of the intended order. I independently checked irreducibility and these degree comparisons for all six families. This short argument should be included explicitly in the note; PARI polclass and the numerical form matching can then remain comparators.

For the signed −7 trace, the classical equation is 4p = t² + 7v². Class number one and units ±1 leave the two trace signs. For the base curve of conductor 49, the Hecke character has finite character the quadratic character modulo 7. Writing π = (t₀+v√−7)/2 gives its residue t₀/2 modulo √−7; because (2/7) = 1, the base trace is (t₀/7)t₀. The quadratic twist by r multiplies it by (r/p). This gives the submitted rule (t/7) = (r/p), including the sign. The minimal model [1,−1,0,−2,−1] has c₄ = 105, c₆ = 1323, Δ = −343 and short coefficients (−35/16,−98/64); scaling by u = 2 produces (−35,−98). Its conductor is 49. The official Magma documentation identifies this short curve as a model of 49a, and the LMFDB primary record agrees on the CM discriminant, model and conductor. A primary lecture derivation gives the Hecke character used here. The exact book theorem numbers that the author marked as unread were not all independently verified in this review; those bibliographic qualifications should remain.

The 2-adic argument is also consistent as an alternative sign-selection algorithm. Both 2-isogeny kernels are rational at admitted primes. The α-primary 2-adic Tate module is a rank-one module over Z₂; the nonzero kernel point is divisible by 2 in E(F_p) precisely when Frobenius is 1 modulo α². The halving test is whether the two differences from the other rational 2-torsion roots are squares. Comparing this bit with the two norm-equation candidates selects the trace sign. The written proof currently ends with that test; it does not finish an algebraic equivalence with the Legendre-mod-7 condition. Route (a) suffices for the displayed closed sign rule. Label route (b) accordingly, or supply the missing equivalence.

The original-cubic reconstruction is consistent. With f = 1+cw+bw²+aw³, x = aw+b/3 and y = av, one has dw/v = dx/y exactly, β = aK+(b/3)H and

$$K=\frac{\beta-(b/3)H}{a},\qquad
T_f(\mu)=\frac{a\mu(\mu H-K)}{f'(\mu)}.$$

This retains the boundary sign and the strict coefficient cutoff i < p. At p = 11, r = 1, the cubic f = 1+9w+w³ has H = 4, K = β = 7 and trace 4. Its three roots are 1, 3 and 7; the branch outputs are 8, 5 and 2 respectively. Dense polynomial expansion agrees. The independently generated cubic tests also checked the entire (H,K,T) output, rather than only the slope or trace.

| Correction | Exact issue or counterexample | Required change |
|---|---|---|
| Corollary 2.1: non-scalar is insufficient | On the −7 seed at p = 11, α = 1+11(1+√−7)/2 is non-scalar and separable, of degree 254. Both eigenvalues reduce to 1, the kernel sum reduces to 0, and the displayed quotient is 0/0. The actual slope is 10. | Add λ−μ ≠ 0, equivalently u² ≠ ℓ in F_p, to the corollary. Theorem 5 already contains the necessary unit condition. |
| Section 3.1: scope of “second kind” | On y² = x³+9x+1 over F₁₁, θ = x¹¹η has only a pole at O and has zero residue, but Cθ = 7η has a double pole. Thus θ is residue-free but is not in C⁻¹(H⁰Ω). | State that the one-dimensional quotient is for differentials locally exact modulo regular forms, using that stronger definition explicitly. It is not a statement about all residue-free meromorphic differentials modulo global exact forms. |
| Validation runner | Injecting R₋₇ = 1/3 into an isolated copy produced 2,372 reported failures, with process exit status 0. run_all.py also ends with status 0 even when a subprocess fails. | Make both validation scripts return nonzero on failure, and make the runner propagate failure. A tested optional patch is included. |
| Numerical period precision | period_check.py and quasiperiod_isogeny_check.py convert their discrepancies through Python complex. Recorded zero therefore means equality after rounding; the period check is not an 80-digit error certificate. | Describe these as floating-point corroboration. Use native high-precision subtraction and interval arithmetic if certified analytic error bounds are desired. |
| Complete trace provenance | The submitted large-prime CSV records r mod 7 and its quadratic character, rather than full r,A,B. This describes the relevant twist class but not the exact sampled model. | Record the full model in future validation CSVs. The independent large-prime CSV does so. |
| Minor implementation contract | fixed_D_evaluator.py uses p % abs(D) == 0 to test p dividing D. | Use D % p == 0. The present eight tables at p ≥ 7 do not give a new wrong-output counterexample from this typo; other filters exclude the problematic small cases. The function also assumes a certified prime input, unlike the D7 public preparer. |

The primitive g = G(x)/yᵖ in §3.1 is valid, and the warning about p-th-power polar terms is valuable. The issue is the surrounding terminology and the size of the space being quotiented. The example above preserves a real obstruction: zero residues alone do not imply local integrability in characteristic p. The core proofs in §§2 and 4–8 do not use the incorrect broader interpretation.

The full submitted run completed with zero recorded failures. The following are additional, independently written controls, not a relabeling of the submitted counts. “Models scanned” means an exhaustive coverage scan; the dense coefficient work was performed on the accepted table members, as stated separately.

| Independent check | Observed scope | Result |
|---|---|---|
| Direct base-curve point counts | 1,605 admitted primes through 30,000; 4,814 twist/sign checks | Both native trace rules agree; wrong opposite signs rejected |
| Sparse multinomial extraction of H and β | All r for p ≤ 503: 11,062 −7 members and 10,536 −8 members; dense base powers as a second reference | No disagreement |
| Exhaustive short-model scan | 989,668 nonsingular models over primes through 251 | No conflicting admitted table classes |
| Dense coefficient checks in that scan | 21,040 matched models | H nonzero and β equal to the table slope times H |
| Fresh original cubics | 143 cubics, 429 branch queries through 2,003 | Complete H,K,T agree with dense powers |
| Exact collision resultants | All 45 pairs among the eight tables and two seeds; independent factorization and multiplication back | No prime split in both relevant fields; no admitted −7 collision |
| Degree-five control | Both delivered kernel polynomials divide ψ₅, are prime to F, and are stable under the doubling map | Actual subgroup condition independently checked |
| Fresh large-prime traces | 20 full models at 20,32,44,56,63 bits | Both rules agree with PARI ellap, a practical comparator |
| Failure injection | Wrong −7 constant in a disposable copy | Real failure detected in JSON; missing exit propagation confirmed and patched |

Exact family-loop, symbolic Vélu, odd-degree control, CM-table rational coefficients and collision-resultant outputs from the rerun equal the submitted outputs. The scripts that merely print failure summaries were not trusted by exit status alone: I inspected their stored counters and mathematical data. Source hashes, package versions, commands, JSONs and CSVs are retained in the evidence bundle. The full suite used PARI 2.17.2, python-flint 0.9.0, SymPy 1.14.0, mpmath 1.3.0 and cypari2 2.2.4 under Python 3.12.14. Run duration is reproducibility information, not a comparative performance claim.

The literature audit supports the classical interpretation. Katz's author scan is accessible past the point at which the other AI's extraction stopped: Lemma 4.0.7, §5.7, Comparison Theorem 8.0.9 and Lemma 8.0.13 are present. His later paper *On a Question of Zannier* explicitly treats the first- and second-kind Cartier coefficients, the low-pole de Rham basis and the unit-root direction. These are direct prior context for the comparison, and should be cited with the appropriate normalization rather than treated as new background found by the tests.

The BOS warning is real for the literal arXiv v3 formula: the source expressly defines Φ_D = Φ_|D|. At discriminant −8, an element of norm 8 in Z[√−2] is ±2√−2, divisible by 2, and its kernel is not cyclic. Thus it does not yield the self-isogeny required by Φ₈. The submitted exact calculation of Φ₈(8000,8000) ≠ 0 reran. The correct primitive trace-zero element has norm 2, and the Φ₂ control gives s₂ = 5/14. Keep this as a source-convention problem requiring clarification, rather than a sweeping claim that the published theory is false. I did not obtain Masser's original appendix. The author-hosted discriminant −7 gamma polynomial has root 181/637875, reproducing the supplied s₂ = 5/21 after the stated conversion, so that CM value itself is explicitly prior published data.

Primary sources directly inspected in this review:

| Source | Location used | What it supports |
|---|---|---|
| [Katz, 1976 author scan](https://web.math.princeton.edu/~nmk/old/padicinterp.pdf) | Lemma 4.0.7; §5.7; 8.0.9; 8.0.13 | CM antiholomorphic eigenline and ordinary unit-root comparison |
| [Katz, On a Question of Zannier](https://web.math.princeton.edu/~nmk/zannier_publ.pdf) | §3, Theorem 3.1 and its proof | Coefficient Cartier data, low-pole de Rham realization, no common zero of the two coefficients |
| [Bruinier–Ono–Sutherland, arXiv v3](https://arxiv.org/pdf/1301.5672) | Definitions (1.2)–(1.3), §2.4, Lemma 2.3, Algorithm 1 | Gamma/s₂ conversion, literal polynomial convention and GRH-dependent precomputation bounds |
| [Sutherland, Lecture 21](https://math.mit.edu/classes/18.783/2023/LectureNotes21.pdf) | §21.5–21.6, Theorems 21.5 and 21.14 | Degree-one CM reduction, order preservation, class-polynomial roots |
| [Prasanna lectures, Horawa notes](https://people.maths.ox.ac.uk/horawa/math_678.pdf) | Example 7.18, printed p. 113 | The conductor-49 quadratic-field Hecke character used for the trace sign |
| [Magma official documentation](https://magma.maths.usyd.edu.au/magma/handbook/text/1649) | Example using 49a | Identification of y² = x³−35x−98 with the classical CM curve |
| [LMFDB primary record](https://www.lmfdb.org/EllipticCurve/Q/data/49.a4) | Curve/model and CM fields | Minimal coefficients, conductor 49, CM −7 and j = −3375 |
| [Sutherland's gamma table](https://math.mit.edu/~drew/Pfiles/Hgamma_7.txt) | Discriminant −7 | Exact published gamma constant, hence the converted s₂ constant |

Preparation and query costs remain separate. With a certified prime and the model coefficients supplied, recognition and slope reconstruction use a fixed number of field operations. Preparing the complete −7 evaluator also requires its signed trace, and therefore the square root, norm-equation reconstruction and twist sign, or a separately charged supplied-trace certificate. Tonelli–Shanks has a randomized nonresidue search for p ≡ 1 mod 8; this is an expected-polylogarithmic native preparation route, not the claimed removal of Schoof from unconditional theory. The deterministic fallback and its cost must remain visible. An individual supplied-root query is then O(1) field operations. Finding roots, primality certification, table loading/reduction and external trace computation are preparation work. The public D7 prototype validates only primes below 2⁶⁴; that implementation limit is separate from the all-prime mathematical statement. No timing comparison with BGS or a point-counting backend is claimed here.

For fixed D, the precomputed R_D(j) supplies the slope directly. This unifies the six existing recipes and adds a distinct family with a new CM field. It does not certify every ordinary curve cheaply: its CM order may have a growing discriminant, and finding that order and constructing its tables are separate costs. This work supplies neither a precision-two Witt correction nor a shortcut for the supersingular rounded-third boundary.

My recommendation is to accept the −7 extension and the normalized fixed-table comparison as sound candidates for human review, after correcting the scope and runner issues. Complete the short class-polynomial/order argument and clarify the role of the second trace proof. There is no need for a larger numerical sweep to resolve these writing and hypothesis issues. Whether the project-specific presentation or certificates are new should be decided by a literature-aware specialist; the current evidence supports usefulness, not priority.

In plain language: the earlier work found six special recipes for getting the missing Cartier–Miller ingredient quickly. This research explains why those recipes work, using a shared symmetry rule, and adds another family for which the missing ingredient is especially simple. After the curve is prepared, its branch-point answers take only a handful of calculations. That is a useful extension for special curves, with some corrections needed in the report and test machinery; it is not a shortcut for all curves or the rounded-third problem.
