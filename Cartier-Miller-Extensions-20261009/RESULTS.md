# Results: normalized isogeny closure, depth-three recognition and the rounded third point

This document is the technical summary of the release. The research is separate extension work on the Cartier–Miller manuscript, carried out with substantial generative-AI assistance; its proofs are unrefereed and its computational evidence is finite. The manuscript itself is not part of this release and is unchanged.

The research supplies explicitly normalized coefficient recovery for curves reachable from two ordinary easy seed families by rational degree-two isogenies. Direct recognition is complete through depth two for those seeds. At depth three, only the nondual family from the ordinary A=0 seed has been consolidated. The B=0 seed chain remains deferred. “Depth three” never means every elliptic curve or every possible depth-three family.

| Stage | Concrete result | Evidence and scope |
|---|---|---|
| Shared foundation | Branch formula, normalization and rooted Cartier transport | Separate algebraic derivations; linear general fallback; finite validation; human proof review pending |
| Depth one | Two explicit parameter families with beta=-rH | Ordinary seed restrictions, twists and checked model equations |
| Depth two | Two nondual parameter families; direct parameter recovery without square roots or graph search | Complete rational two-step classification from the specified easy seeds; exact exceptional-prime norms and collision checks |
| Depth three | One discriminant -192 family; relative-norm recognition and normalized reverse certificate | p congruent to 1 modulo 24; other seed chain deferred; finite evidence is not a general proof |
| Restricted CM preparation | Candidate traces from Cornacchia; deterministic sign by Ireland & Rosen, Ch. 18, Theorem 4 on the seed (10 October); alternative zero-error point test with at least 1/5 success per raw uniform-x draw | Classical theorem plus the family's trace proposition; only the cubic-nonresidue search for √−3 is randomized; the Las Vegas alternative has a family-specific unrefereed probability argument |
| Higher-depth audit | Additional classes at depths three and four in tested finite fields | Finite graph census, not a uniform depth bound |
| Rounded third point, p ≡ 2 mod 3 | Boundary a_L=3/(2(m!)³), m=⌊p/3⌋; complete weighted sum equivalent to ⌊p/3⌋! mod p (p≠17) | Elementary proof; checked for 1,136 primes; an obstruction, not a fast family |

For f=1+cw+bw²+aw³, p≥7 prime, a nonzero and f squarefree, set h=(p−1)/2, H=[w^(p−1)]f^h and K=[w^(p−2)]f^h. For a supplied nonzero rational root μ,

$$T_f(\mu)=S_f(1/\mu)=\frac{a\mu}{f'(\mu)}(\mu H-K).$$

The short model is x=aw+b/3, y=av, A=ac−b²/3, B=a²−abc/3+2b³/27, with dw/v=dx/y. Its second-kind coefficient is beta=aK+(b/3)H; H is the exact Frobenius trace modulo p. This normalization is distinct from the manuscript's rational-origin normalization.

At a rational kernel root q, the quotient is A'=-4A−15q², B'=-8Aq−22q³. The holomorphic differential scale is +1, and the exact correction is -2d(y/(x−q)); hence H'=H, beta'=2beta−qH. The dual returns (16A,64B), requiring square scaling. The proof notes explicitly track local poles and residue signs. For an input-to-easy-seed path, beta=H sum_i(q_i/2^(i+1)); no division by H is used.

| Family | Assumptions | A/r² | B/r³ | beta/(rH) |
|---|---|---|---|---|
| Depth one from B=0 | p=1 mod 4, r nonzero | -11 | -14 | -1 |
| Depth one from A=0 | p=1 mod 3, r nonzero | -15 | -22 | -1 |
| Depth two from B=0 | p=1 mod 8, e²=2, r nonzero | -91−60e | -462−308e | -(3+2e) |
| Depth two from A=0 | p=1 mod 12, e²=3, r nonzero | -135−60e | -694−420e | -(3+2e) |
| Consolidated depth three from A=0 | p=1 mod 24, e²=3, g²=2, r nonzero | -1095−540e−540g−420eg | -22198−13860e−16380g−8820eg | -(7+6e+6g+2eg) |

The displayed quotients beta/(rH) denote multipliers; the implementations multiply by H rather than divide by it. Quadratic twisting by d sends r to dr and uses the trace of the actual target model. Equal j-values alone do not identify base-field twists or the required differential normalization.

| Task | Preparation and query costs |
|---|---|
| General branch fallback | O(p) field preparation with constant working field elements; O(1) supplied-root query |
| Supplied m-edge path | O(m) verification and reconstruction after exact trace preparation |
| Fixed depth-one/two direct recognition | O(1) field work after prime validation; trace preparation charged separately |
| Deterministic theoretical complete preparation | Schoof exact trace setup plus recognition and reconstruction; no automatic production backend is asserted |
| Consolidated depth-three CM route | Default: expected O(log p) exponentiations for √−3, Cornacchia, then one exponentiation for the deterministic sign, plus reconstruction; Las Vegas alternative: unbounded variant expected O(log² p) field work |
| Prepared supported root query | O(1) field work; finding the root is excluded and must be charged if needed |

Since 10 October 2026 the default trace sign is deterministic (research/depth_three_recognition_20261007/DETERMINISTIC_TRACE_SIGN_20261010.md); the complete CM preparation is randomized only in the cubic-nonresidue search that supplies √−3. With `sign_method='las_vegas'` the zero-error point test is used instead: its default cap is 64 raw draws and may return inconclusive, with the conditional bound (4/5)^64, and its unbounded variant terminates almost surely with at most five raw draws in expectation under the recognized-family theorem and independent uniform draws. The prototype primality guard is restricted to p<2^64. This randomized route does not replace Schoof's unconditional deterministic theoretical setup. No production SEA or new benchmark is included.

Historical reports remain intact, including their superseded statements. The depth-one closure report predates the complete depth-two recognizer; its “not implemented” statements about that later classifier are historical. The original depth-three report predates the sign-success bound and status repairs. STATUS.md, docs/Depth_Three_Consolidation_Review_20261007.md, research/depth_three_recognition_20261007/TRACE_SIGN_BOUND_20261007.md and docs/LEDGER_20261009.md govern those points. Historic PARI/Sympy checks are distinguished from fresh standard-library checks; no new PARI run was available in consolidation.

Underlying CM curves and class polynomials, Cartier coefficient interpretations, the Cornacchia/random-point sign strategy and the Jacobi-sum trace formula of Ireland and Rosen used for the deterministic sign are classical. The ledger (docs/LEDGER_20261009.md) records primary sources previously checked, including Sutherland's 2023 CM lecture and Morain's 2004 preprint. The originality or nontriviality of the explicit recognition/coefficient-recovery combination remains unestablished. No major or previously unreported result is claimed.

Real obstructions are preserved: trace matching alone does not imply rational degree-two reachability; dual backtracking supplies only scaling; scalar trace finite differences do not give formal Hasse derivatives; supersingular transport does not determine an unknown beta amplitude; and the easy seed y²=x³+19 over F_97 makes both candidate orders annihilate every rational point, so a generic sign-success guarantee is false.

For the original weighted sum, both B_L and a_L are required. This work does not establish fast evaluation at every stopping index or a fast sum-avoiding precision-two Witt correction. The p=1 mod 3 third-point evaluator is already complete. Restricted higher-genus prefix and precision-two recurrence-product branches already exist and remain separate. For the rounded third point p=2 mod 3, the 9 October addition shows that a_L=3/(2(m!)^3) with m=⌊p/3⌋. Given the retained O(log p) prefix, the complete weighted sum is therefore equivalent to the Gauss factorial ⌊p/3⌋! mod p, equivalently Γ_p(1/3) mod p, except at p=17. The trace is zero, so CM data cannot supply the boundary. No polylogarithmic method is known: deterministic single-prime methods cost about √p up to logarithmic factors, and an unrefereed 2026 report (Tal, ECCC TR26-211) claims randomized p^{1/2−δ} for most primes. See research/rounded_third_boundary_20261009/Rounded_Third_Boundary_Note_20261009.md.

The branch-point/isogeny stage is parked for human review. Any future benchmark must charge necessary preparation and reconstruction, compare identical outputs and moduli, distinguish cached queries from complete runs, and preserve CSVs, source hashes, environment and validation.
