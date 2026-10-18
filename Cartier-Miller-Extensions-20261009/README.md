# Cartier–Miller extensions

**Normalized 2-isogeny closure, depth-three CM recognition, the CM-to-Cartier comparison, the rounded-third obstruction and its certified boundary backend**

This release collects extension research on David Jordan's manuscript *Cartier–Miller evaluation of genus-one coefficient sums* (revised 5 October 2026). The manuscript evaluates the truncation $T_f=f^{(p-1)/2}\bmod w^p$ of a genus-one polynomial power at a base-field point. It does this through the exact Frobenius trace and a differentiated Miller recurrence, at a cost of $O(\log p)$ field operations after trace preparation. Branch points $f(\mu)=0$ are excluded there, because they need one additional second-kind coefficient $K$. The work here asks when that coefficient, and with it the branch value, can be recovered cheaply. It also records where it cannot.

The research was carried out between 6 and 18 October 2026 with substantial generative-AI assistance. Every proof is unrefereed, and every computational check is finite evidence, not a proof. Novelty is not claimed: the underlying CM curves, class polynomials, Cartier coefficients and the Cornacchia/random-point trace strategy are classical. The question of what, if anything, is a useful original contribution is open and is posed in [HUMAN_REVIEW.md](HUMAN_REVIEW.md). Specialist review is invited.

## Results at a glance

| Stage | Result | Evidence and scope |
|---|---|---|
| Branch formula | For a squarefree cubic $f=1+cw+bw^2+aw^3$ and a rational root $\mu$, $T_f(\mu)=\frac{a\mu}{f'(\mu)}(\mu H-K)$, with $H,K$ the coefficients of $w^{p-1},w^{p-2}$ in $f^{(p-1)/2}$ | Two algebraic derivations; 23,736 branch queries checked against dense powers; the general fallback is $O(p)$ |
| Rooted transport | At a rational kernel root $q$: $A'=-4A-15q^2$, $B'=-8Aq-22q^3$, $H'=H$, $\beta'=2\beta-qH$, with the dual returning $(16A,64B)$ | Proof note; 15,872 exhaustive cases for $7\le p<60$ plus duals and chains (replacement validator) |
| Depth one | Two explicit families with $\beta=-rH$, from the ordinary seeds $B=0$ and $A=0$ | Checked for every member below 200 |
| Depth two | Two nondual families; direct recognition without square roots or graph search; complete for rational two-step paths from the stated seeds | Integer certificates, exceptional-prime norms, collision checks |
| Depth three | One discriminant $-192$ family from the $A=0$ seed ($p\equiv1\bmod 24$), with relative-norm recognition, a reverse certificate and a CM trace preparation whose sign step is deterministic (Ireland & Rosen, Ch. 18, Theorem 4), with a proved zero-error Las Vegas alternative | Proof note and sign-bound appendix; 2,640 members cross-checked against PARI `ellap` |
| Depth three from $B=0$ | The companion discriminant $-256$ family, for $p=x^2+64y^2$, over $\mathbb Z[s]/(s^4-2)$, with direct recognition and an exact trace by Ireland & Rosen, Ch. 18, Theorem 5 (12 October) | Unrefereed proof; passed an independent adversarial AI review (1,885,840 models classified independently); validator passes with PARI |
| CM-to-Cartier comparison | For a CM curve, $\beta/H\equiv-\frac{3B}{2A}s_2(\tau)$ mod p with $s_2=E_2^*E_4/E_6$, via Cartier commutation with an endomorphism; this re-derives all six family slopes and gives a fixed-discriminant table $\beta/H=-\frac{3B}{2A}R_D(j)$ (12 October) | The comparison is classical in substance (Katz 1976, 2019); the application, certificates and evaluators are the candidate contribution; passed an independent adversarial AI review |
| New seed at $D=-7$ | For $p\equiv1,2,4\bmod7$: every $j=-3375$ curve is $(-35r^2,-98r^3)$ with $\beta=-rH$; signed trace from $4p=t^2+7v^2$ and $(t/7)=(r/p)$; original-cubic evaluator; $D=-8$ control | 19,602 members swept exhaustively for $p\le700$, plus large-prime PARI checks; reproduced independently |
| Generic ordinary slope (feasibility, 12 October) | In the low-pole basis Frobenius mod $p$ is $\begin{pmatrix}0&-\beta\\0&H\end{pmatrix}$, so $\kappa=\beta/H$ is one Frobenius entry; for any ordinary lift, $\kappa\equiv\sigma_C/p$ with $\sigma_C$ the canonical-subgroup kernel sum. The canonical-lift, étale and Serre–Tate constructions examined give no cheaper complete algorithm than the $\tilde O(\sqrt p)$ methods | Unrefereed; Lemma B awaits specialist review; pilot and an independently written check (46,213 checks) pass; no lower bound, speed-up or novelty claimed |
| Rounded third point | For $p\equiv2\bmod3$, the missing boundary is $a_{(p+1)/3}\equiv 3/(2(m!)^3)$ with $m=\lfloor p/3\rfloor$, so the complete weighted sum is equivalent to the Gauss factorial $\lfloor p/3\rfloor!\bmod p$ (for $p\neq17$) | Elementary proof; 1,136 primes checked; an obstruction, not a fast family |
| Rounded third, certified boundary backend (18 October) | A certified Jacobi-sum (T3) route for $\lfloor p/3\rfloor!$ is integrated with the retained Miller prefix, with exact nodal and native fallbacks; complete $(B_L,a_L,U_p(L),G)$ for $11\le p<2^{63}$, $p\equiv5\bmod6$ | 1.67–6.52× faster than native FLINT factorial plus Miller at the nine tested primes where T3 was selected; the remainder forest wins on dense prime tables, native calls on the tested sparse schedule; 17 fresh confirmation primes up to $7\cdot10^{12}$; still $\sqrt p$-type for a fixed conductor, with no polylogarithmic method |

| Family | Assumptions | $A/r^2$ | $B/r^3$ | $\beta/(rH)$ |
|---|---|---|---|---|
| Depth one from $B=0$ | $p\equiv1\bmod4$ | $-11$ | $-14$ | $-1$ |
| Depth one from $A=0$ | $p\equiv1\bmod3$ | $-15$ | $-22$ | $-1$ |
| Depth two from $B=0$ | $p\equiv1\bmod8$, $e^2=2$ | $-91-60e$ | $-462-308e$ | $-(3+2e)$ |
| Depth two from $A=0$ | $p\equiv1\bmod12$, $e^2=3$ | $-135-60e$ | $-694-420e$ | $-(3+2e)$ |
| Depth three from $A=0$ | $p\equiv1\bmod24$, $e^2=3$, $g^2=2$ | $-1095-540e-540g-420eg$ | $-22198-13860e-16380g-8820eg$ | $-(7+6e+6g+2eg)$ |
| Depth three from $B=0$ | $p\equiv1\bmod8$, $s^4=2$ (equivalently $p=x^2+64y^2$) | $-731-600s-540s^2-360s^3$ | $-14798-11816s-10164s^2-8456s^3$ | $-(7+4s+6s^2+4s^3)$ |
| CM seed $D=-7$ | $p\equiv1,2,4\bmod7$ | $-35$ | $-98$ | $-1$ |
| CM control $D=-8$ | $p\equiv1,3\bmod8$ | $-30$ | $56$ | $+1$ |

![Visualisaiton of 2-Isogeny](https://github.com/bbrhuft/Cartier-Miller-evaluation-of-genus-one-coefficient-sums/blob/main/Cartier-Miller-Extensions-20261009/Walk%20the%20Volcano.png) 

The short model is $y^2=x^3+Ax+B$ with $\beta=\lbrack x^{p-2}\rbrack\,(x^3+Ax+B)^{(p-1)/2}$ and $r\neq0$. The quotients $\beta/(rH)$ are multipliers: the implementations multiply by $H$ and never divide by it. Quadratic twisting by $d$ sends $r$ to $dr$. [RESULTS.md](RESULTS.md) states the normalization, costs and limitations in full.

## Quick start

Python 3.10 or later and the standard library are enough for the verifier, the recognizers and the main validators. Run commands from the repository root.

```bash
python verify_release.py
python research/depth_two_recognition_20261006/core/cli.py --p 13 --f 1 12 0 9 --trusted-trace -2 --mu 7
python research/depth_three_recognition_20261007/core/cli.py --p 73 --f 1 4 0 37 --cm --mu 9
```

The verifier checks every file hash in [SHA256SUMS.json](SHA256SUMS.json) and runs small independent fixture checks in under a second. The two CLI examples return $H=11,K=8,T=2$ and $H=10,K=55,T=3$. The first trusts the supplied trace; the second prepares the trace by the restricted CM route. [REPRODUCTION.md](REPRODUCTION.md) lists every full validation command, the optional dependencies (SymPy and cypari2/PARI) and the measured run times.

## Reading order

| Document | Purpose |
|---|---|
| [RESULTS.md](RESULTS.md) | Technical summary: normalization, transport, families, costs, obstructions |
| [STATUS.md](STATUS.md) | What is proved, implemented, tested, deferred or unresolved |
| [HUMAN_REVIEW.md](HUMAN_REVIEW.md) | Concrete questions for mathematical reviewers |
| research/branch_point_20261006/Cubic_Branch_Point_Report_20261006.md | Branch formula and its obstructions |
| research/isogeny_closure_20261006/theory/ISOGENY_CLOSURE_THEORY.md | Normalized rooted transport, depth one and initial depth two |
| research/depth_two_recognition_20261006/theory/RECOGNITION_THEORY.md | Direct depth-two recognizer and integer certificates |
| docs/Depth_Three_Consolidated_Proof_Note_20261007.md | Depth-three family proof with the trace-sign bound |
| research/depth_three_recognition_20261007/DETERMINISTIC_TRACE_SIGN_20261010.md | Deterministic trace sign, the default since 10 October |
| research/depth_three_recognition_20261007/B0_SEED_FAMILY_20261012.md | Depth-three family below the $B=0$ seed, with review notes |
| research/cm_cartier_comparison_20261012/CM_Cartier_Extension_Note_20261012_rev1.md | CM-to-Cartier comparison, recovery of the six families, the $D=-7$ seed; `REVIEW_RESPONSE.md` beside it lists the review corrections |
| research/ordinary_k_feasibility_20261012/Ordinary_K_Feasibility_Note_20261012_rev2.md | Generic ordinary slope from canonical-lift data: Theorem A, Lemma B, information audit and the limits of the constructions examined; `CHANGES.md` beside it lists the review corrections |
| research/rounded_third_boundary_20261009/Rounded_Third_Boundary_Note_20261009.md | Rounded-third boundary as a Gauss factorial |
| research/rounded_third_t3_integration_20261018/README.md | Certified Jacobi boundary backend for the rounded third point, its evidence and workload-matched timings; `RELEASE_NOTE.md` beside it records the import |
| [docs/LEDGER_20261009.md](docs/LEDGER_20261009.md) | Chronological research ledger with prior-art assessments |
| [PROVENANCE.md](PROVENANCE.md) | Origin, layout changes, exclusions and AI assistance |

## Repository layout

| Path | Contents |
|---|---|
| research/branch_point_20261006/ | Branch evaluator, validator, results and report |
| research/isogeny_closure_20261006/ | Path and closure prototype, theory, replacement validator |
| research/depth_two_recognition_20261006/ | Direct depth-two recognizer, theory checks, finite higher-depth graph audit |
| research/depth_three_recognition_20261007/ | Depth-three recognizers for both seeds and CLI, validators, sign-bound witnesses, independent checks |
| research/cm_cartier_comparison_20261012/ | CM-to-Cartier note and ledger, $D=-7$ and $D=-8$ modules, fixed-discriminant evaluator, theory scripts, validators and results |
| research/ordinary_k_feasibility_20261012/ | Ordinary-slope feasibility note, change record and ledger, pilot and independent checks with their failure injection, results and review evidence |
| research/rounded_third_boundary_20261009/ | Rounded-third note, prior-art assessment, validators and results |
| research/rounded_third_t3_integration_20261018/ | Rounded-third T3 integration: research page, handover, the integration package with frozen evidence and benchmarks, import verifier, control check and repository rerun |
| retained/ | An unchanged copy of the parent project's `elliptic_prefix.py`, which supplies the fast third-point prefix |
| fixtures/ | Small fixtures used by the verifier and validators |
| evidence/rerun_20261009/, evidence/rerun_20261012/ | Logs and outputs from rerunning every validator in this layout |
| docs/ | Depth-three proof note, consolidation review, current ledger |
| history/ | Earlier ledgers, superseded reports, the two 12 October adversarial reviews' records, historical validation snapshots and AI-handover records, kept for provenance |

The research directories keep their original relative import layout. Move Python files only after checking their `sys.path` dependencies.

## Scope and known obstructions

Depth two is complete only for rational degree-two paths from the two stated ordinary easy seeds. Depth three covers the two nondual families below the $A=0$ and $B=0$ seeds, not depth four and not arbitrary curves. The CM-to-Cartier comparison gives slopes from fixed precomputed tables only; it is not a method for discovering a generic curve's CM order, whose discriminant is typically about as large as $p$. A negative recognizer answer does not prove global nonreachability. For a generic ordinary curve, the 12 October feasibility study locates $\kappa=\beta/H$ exactly (one entry of Frobenius mod $p$; a canonical-subgroup kernel sum of any lift) but finds no construction cheaper than the $\tilde O(\sqrt p)$ methods; it proves no lower bound. Several obstructions are recorded as results. Trace matching alone does not imply rational degree-two reachability. Dual backtracking supplies only scaling. Scalar trace finite differences do not give formal Hasse derivatives. Supersingular transport does not determine an unknown $\beta$. And the easy seed $y^2=x^3+19$ over $\mathbb F_{97}$ makes both candidate orders annihilate every rational point, so a generic sign-success guarantee is false.

At the rounded third point the trace is identically zero, so CM data cannot supply the boundary. The boundary is $\Gamma_p(1/3)^{-3}$ up to a constant, and no polylogarithmic algorithm is known. The 18 October T3 backend makes the boundary cheaper in practice at suitable large primes, but for a fixed conductor its cost is still of square-root type, and certified reconstruction is not proved to succeed on every input. Deterministic methods cost about $\sqrt p$ up to logarithmic factors, and an unrefereed 2026 report claims randomized $p^{1/2-\delta}$ for most primes. The weighted sum still requires both the prefix $B_L$ and the boundary $a_L$. This release establishes no fast evaluation at every stopping index and no sum-avoiding precision-two Witt correction. The randomized CM route does not replace Schoof's deterministic theoretical setup. No production SEA backend is included. The only benchmarks are the rounded-third T3 measurements recorded in research/rounded_third_t3_integration_20261018/, which are host-specific and compare only the named comparators.

## Validation performed for this release

On 9 October 2026 every validator was rerun in this layout from a scratch copy, so that the retained evidence files were not overwritten. All 17 jobs passed, with SymPy 1.14.0 and PARI 2.17.2 available. That run added the first PARI trace cross-checks of the depth-three family members. The original closure validator was not retained in the source archive, so a replacement reconstructing its documented scope was written and passed. The details are in [evidence/rerun_20261009/README.md](evidence/rerun_20261009/README.md) and [PROVENANCE.md](PROVENANCE.md). On 10 October the deterministic trace-sign rule was merged in. The depth-three validators were rerun in place for the new code and passed, and a further independent PARI check of Ireland and Rosen's Theorem 4 passed on 2,075 curves. On 12 October the $B=0$-seed family and the CM-to-Cartier package were integrated. Every validator was rerun from a scratch copy of the updated layout, including all 13 steps of the CM package's own suite; see [evidence/rerun_20261012/README.md](evidence/rerun_20261012/README.md). On 18 October the rounded-third T3 package was imported. Its integrity check, development checks, CLI examples and a recomputation of the handover's control values were rerun from copies; benchmarks, survey and confirmation were not rerun (research/rounded_third_t3_integration_20261018/README.md).

## Licence

This release is distributed under the [MIT License](LICENSE), copyright 2026 David Jordan. It deliberately excludes material from the parent project that carries other terms or belongs to the paper. The excluded items are the GPL-licensed David Harvey interval-product sources and the GPL-noticed benchmark GUI, adapter and harness; the manuscript and its editorial records; and the September 2026 historical archives, which were not re-reviewed. Those items remain under their existing terms wherever they are published. [PROVENANCE.md](PROVENANCE.md) lists every exclusion.

## Citation and AI assistance

Citation metadata is in [CITATION.cff](CITATION.cff). The derivations, code and reports were produced with substantial generative-AI assistance under the author's direction, and they have not yet been independently refereed. Verification by people, not numerical agreement, is what will establish the mathematics. Corrections and review comments are welcome as GitHub issues.
