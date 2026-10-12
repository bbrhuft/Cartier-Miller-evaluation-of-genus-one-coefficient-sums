# Review of the ordinary Cartier-slope feasibility study

12 October 2026. Independent assessment of the submitted Opus 5.5 note, ledger and ZIP. Unrefereed. The submitted files, published manuscript and repository were not changed. No GitHub inspection or novelty claim was made.

## Assessment

This is a useful normalization and feasibility result. It gives several explicit, mutually consistent descriptions of the same ordinary Cartier slope, and a substantial collection of executable checks. It supplies no complete faster generic algorithm, no new restricted fast family, and no lower bound. The core identities appear sound on mathematical inspection and survived the reruns below. The canonical-subgroup argument merits specialist review of its integral model and crystalline-comparison lemmas before being presented as a fully reviewed theorem.

The principal conclusion should be: **the concrete constructions examined did not yield a cheaper complete computation of the slope.** The note's closing sentence that the canonical twin does not give a general shortcut is stronger than this study establishes. The failure of the examined approaches does not settle the broader possibility of a lift-based shortcut.

## Mathematics and normalization

For an ordinary nonsingular short model with p at least 7, use F=x^3+Ax+B, h=(p−1)/2, H=[x^(p−1)]F^h=t mod p, β=[x^(p−2)]F^h and κ=β/H. The low-pole basis is ω=dx/y, η=x dx/y. In the column convention the claimed reduction of crystalline Frobenius is

$$\overline M=\begin{pmatrix}0&-\beta\\0&H\end{pmatrix}.$$

The sign is consistent with both the unit-root line η−κω and the character sum. Indeed, the affine point multiplicity at x is 1+F(x)^h. Therefore the sum of the x-coordinates of all finite rational points is Σ_x xF(x)^h=−β: the degree is below 2(p−1), so only the x^(p−1) monomial contributes. The use of the separable endomorphism π−1 and translation invariance of H¹ gives the displayed Frobenius matrix. Additivity of endomorphism pullback on H¹ and the low-pole interpretation of translated second-kind forms should remain explicit. The alternate ordinary argument follows from the classical Cartier description and the trace of Frobenius.

The étale identity κ=−σ_V/t² follows by comparing the upper-right entries for Verschiebung t−π, whose normalized isogeny matrix has upper-right entry −σ_V/t. This requires a genuine étale kernel, but not a full rational generator over the base field.

The derivative identity is particularly transparent. With ϑ=6B∂_A−(4/3)A²∂_B and P=F^h, set R=(4/3)A+2x². Direct polynomial algebra gives ϑF=6xF−RF′ and hence

$$\vartheta H=(p+1)\beta-\frac{4p}{3}A[x^p]F^h.$$

Reduction gives β=ϑH and κ=(ϑH)/H. This is an exact algebraic derivation, not a conclusion from numerical agreement. It explains why the value H obtained from the trace does not by itself supply its transverse derivative. Its relation to classical modular-form derivatives must not be advertised as new without a separate literature assessment.

For the connected p-torsion subgroup of an arbitrary integral lift, Proposition B states κ≡σ_C/p mod p. Its proof is plausible and the two separate computational constructions support it. For a formal proof, state precisely the extension of the quotient isogeny to integral good models, the rescaling from its raw Vélu equation to a good model, and the crystalline transport between the lifts. The raw Vélu coefficients are not a good integral model merely because the source is one. In the proof's sign convention, choose the quotient identification reducing to F, then M=VT. If the identification reduces to −F, the comparison is −M=VT. The ratio yielding κ is unchanged, but the displayed equality must match the chosen sign. This clarification leaves the stated recovery identity intact.

At the canonical lift, u=p/λ gives the eigenline coordinate c=σ_C/(u²−p), with c≡−κ mod p. The algebra of this denominator and sign is consistent. These formulas compute the slope modulo p; they do not solve the earlier weighted-sum problem modulo p².

## Conclusions that require narrower wording

| Submitted claim | Review qualification |
|---|---|
| j_can modulo p² is insufficient; route closed | No cheap recovery map was identified. Lift independence of κ does not prove that canonical-lift data cannot help compute it. With E supplied, κ is already mathematically determined; the question is computational. The ramification examples at j=0,1728 establish failure of coarse j as a fine deformation invariant there, not generic computational impossibility. |
| Serre–Tate conversion is precisely the kernel sum and needs a p-torsion basis over degree ord_p(t) | The kernel sum is one explicit recovery method. Its universal necessity was not proved. A full nonzero p-torsion point has the stated field-of-definition requirement; Kummer coordinates can use a smaller field, and general Serre–Tate descriptions need not materialize that point or every kernel element. |
| All identified scalars require at least linear data, or the square-root trick | This describes the explicit full-polynomial or full-kernel representations audited. A large representation does not prove that one scalar cannot be computed without constructing it. Equality to the target is an equivalence, not a hardness theorem. |
| Θ(p) cost of universal j-lift formulas; generic discriminant and torsion-order assertions | State proved size bounds separately from inferred or heuristic typical-size claims, and distinguish representation size from the complete construction cost. Finotti's size inference is explicitly labelled conjectural/inferential in §9; the cost table should retain that qualification. |
| Every canonical-lift theorem is excluded on prime fields | The checked Maiga–Robert Theorems 1.1 and 1.2 require j not in F_(p²). They do not apply to E/F_p. This is a restriction of these theorems, not of canonical lifting itself. |

The report already acknowledges several of these limitations, but its outcome, ledger, tables and plain-language conclusion should use the same narrower scope throughout.

## What was rerun

All 51 SHA-256 entries in the submitted ZIP verified. The separately uploaded note and ledger match their ZIP copies. Execution took place in a separate copy; the original submission remains unchanged. Environment: Python 3.12.14, Linux 6.18.44, glibc 2.39, standard library only.

The main runner, coverage script and failure-injection script were rerun with the supplied handover, reviewed fixed-D source and completed −256 recognizer paths configured. The recognizers themselves are only hashed by this pilot, not executed; the fixed-D evaluator is actually used.

| Rerun | Observed result |
|---|---|
| Main characteristic-p pilot | PASS; 1,574 ordinary models and 1,395 Verschiebung checks |
| Derivative pilot | PASS; 19,948 nonsingular models |
| p-adic pilot | PASS; 570 trivial lifts, 570 random lifts and 240 iterated canonical lifts; 74 retained fixed-D agreements |
| Original-cubic reconstruction | PASS; 507 cubic checks and 387 branch queries |
| Main-pilot planted errors | All three erroneous scripts exited 1 and the runner propagated failure |
| Independent Čech code | PASS on all 1,428 nonsingular models at p=7,11,13,17,19,23, including supersingular controls |
| Independent explicit étale-point code | PASS on all 126 ordinary models at p=7,11 |
| Independent formal-group code | PASS on eight model/lift pairs at p=7 |
| Independent Kedlaya code | PASS on four sampled p=7 models modulo p², with four stability reruns |

The last two checks were bounded samples, not reruns of the full submitted independent formal-group or Kedlaya suites. A historical absolute fixture path in independent_check/common.py was changed only in the execution copy to point to the supplied handover. No mathematical source was altered for successful checks.

There are two concrete reproducibility corrections. The note reports 1,418 nonsingular models in the independent exhaustive suite, but the per-prime counts sum to **1,428**, and that is what the rerun covers. More seriously, the independent drivers print disagreement lists without guaranteeing a failing process status. A deliberately wrong β comparator in c1_cech.py yielded 0/42 matches and a nonempty failure list while exiting 0. Its raw log is retained in the review evidence. The main pilot correctly propagates failures; the extra independent drivers should do so too and should not be mistaken for part of run_all.py. This does not negate the successful mathematical checks, but it should be repaired before automated reuse.

No timing benchmark or generic fast implementation was established. The pilot's degree-(p²−1)/2 division polynomial is a checking device. It is much larger than the desired scalar output and does not furnish a cost improvement.

## Literature checked for this review

Katz's author copy, On a Question of Zannier, §3 and Theorem 3.1, identifies the direction β/H with the ordinary unit-root line and a reduction of the p-adic weight-two form P/12 in its own Weierstrass chart. With y_Katz=2y on the short model, dx/y_Katz=dx/(2y), and 4^h=1 mod p. Thus the conversion E₂(E,dx/(2y))≡12κ is consistent. Scaling the differential to dx/y divides a weight-two value by four, giving 3κ. This is a classical connection, not independent novelty evidence.

Harvey's author preprint, Efficient Computation of p-adic Heights, Theorem 1 and §3, explicitly supplies E₂ from the second column of powers of Frobenius and the square-root dependence on p at fixed precision. His §3.1 also discusses using a known trace and determinant for a constant-factor improvement, with precision and basis caveats. This directly supports the distinction between knowing the trace and obtaining the missing direction. The preprint treats E fixed in its complexity discussion; a fully uniform variable-curve claim should track lift coefficient sizes and reduction conditions.

Maiga–Robert's author manuscript Theorems 1.1 and 1.2 explicitly impose j not in F_(p²), confirming the prime-field applicability warning. Finotti's author manuscript establishes rational canonical-j coordinates and their poles; it does not, from the portions checked here, establish all of the cold-cost entries in the submission. Katz's Serre–Tate Local Moduli describes intrinsic deformation coordinates and their relation to Gauss–Manin/Kodaira–Spencer theory; it does not turn an explicit p-torsion construction into a universal requirement for every possible algorithm.

| Primary reference | Checked source |
|---|---|
| Harvey, D. (2008). Efficient computation of p-adic heights. LMS Journal of Computation and Mathematics, 11, 40–59. | https://arxiv.org/pdf/0708.3404, author preprint version |
| Katz, N. M. (2019, author-copy year). On a question of Zannier. Experimental Mathematics. DOI 10.1080/10586458.2018.1551818. | https://web.math.princeton.edu/~nmk/zannier_publ.pdf |
| Katz, N. M. Serre–Tate local moduli, Exposé Vbis, author scan. | https://web.math.princeton.edu/~nmk/old/serretatelocmod.pdf |
| Maiga, A., & Robert, D. (n.d.). Towards computing canonical lifts of ordinary elliptic curves in medium characteristic, author manuscript. | https://www.normalesup.org/~robert/pro/publications/articles/fast_canonical_lift_g1.pdf |
| Finotti, L. R. A. (n.d.). Lifting the j-invariant: Questions of Mazur and Tate, author manuscript. | https://luisfinotti.org/math/papers/liftj.pdf |

No source establishes a lower bound for generic ordinary κ. No literature novelty verdict is offered here.

## Research ledger disposition

| Field | Updated review status |
|---|---|
| Question | Can ordinary E plus certified trace give κ cheaply through canonical-lift data? |
| Derivation | Explicit Frobenius matrix, rational-point sum, étale-kernel sum, connected-kernel sum and Hasse derivative |
| Independent checks | Successful main-pilot rerun and bounded separate-method checks described above |
| Counterexample/obstruction | Same-trace distinct-slope pairs exclude trace alone; concrete full-polynomial and torsion constructions have charged costs; neither is a generic lower bound |
| Reproducibility issue | Independent driver accepts a failed comparator with exit 0; repair failure propagation and fixture path |
| Status | Useful, qualified normalization/recovery note; no general speed-up; broad canonical-lift question unresolved |
| Next bounded action | Tighten the negative conclusions and integral-comparison lemma, repair independent runners, and retain this as a separate reviewable extension note. Any future shortcut search should target computing one of the exact scalar outputs without constructing its full polynomial or kernel. |

## ELI5

We wanted the curve's ideal p-adic twin to reveal a hidden answer cheaply. This work shows exactly where that answer appears and gives several ways to check it. The methods tried still do substantial work to obtain it. We have a better mathematical map and reliable signposts, but no new general shortcut—and no proof that a shortcut is impossible.
