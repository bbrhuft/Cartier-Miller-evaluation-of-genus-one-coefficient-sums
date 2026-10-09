# Cartier–Miller extension research ledger

Date: 6 October 2026. Research stage: first bounded extension derived and implemented. The initial-selection entry below is retained as historical context; the new branch-point entry at the end records the current status. No new performance benchmark has been run. The published manuscript is unchanged. Repository URL and commit are unknown; GitHub has not been inspected.

## Authority and evidence

Read START_HERE.md, PROJECT_STATE.md, EXTENSION_ROADMAP.md, SOURCE_STATUS.md, REPRODUCTION.md and the current manuscript's complete convenience transcription; checked the release PDF text for the normalization and excluded-input discussion. The retained October 5 PDF/DOCX govern manuscript scope. Direct characteristic-p exceptional normalization supersedes canonical-lift descriptions still present in historical comments. Proof correctness and novelty remain subject to independent critical review.

New checks in this conversation: package SHA-256 verification passed for 170 files. The supplied smoke check passed seven quarter/third comparisons, including the third-point exceptional prime 61; its trace checks at 97 agreed. These finite checks concern the existing implementations, not a new theorem. No higher-genus or precision-two validation suite was rerun.

## Existing work and duplicate-work guard

| Direction | Evidence inspected | Status and limitation |
|---|---|---|
| Generic admissible genus-one query | Manuscript; retained cmpkg/evaluator.py; quarter implementation | Formula is a manuscript theorem claim with retained finite evidence, not independently certified here. Residue divisor and differential scale must be retained. |
| Third point, p congruent to 1 modulo 3 | Standalone README and third_point.py; fresh smoke checks | Complete B,a,U evaluator exists. No reason to reimplement this endpoint as an extension. |
| Third point, p congruent to 2 modulo 3 | elliptic_prefix.py third() | Existing routine returns B at L=(p+1)/3, trace zero, boundary None and U None. A complete weighted result is missing. |
| Restricted higher genus | Historical ledger; hyperelliptic_prefix.py | Cantor–Miller prefix prototypes exist for odd d=2g+1 dividing p+1. Boundaries remain missing. Family maximality requires the retained geometric argument, not just a zero Cartier matrix. |
| Precision two | Historical p-adic ledger and p=13 record; Witt report; unpacked witt_bgs.py and native.c | Native recurrence products already evaluate the sum; complete() then recovers K from that sum. Original U has a separate original-recurrence path. Neither is sum-avoiding Witt extraction. |
| Extension fields | Manuscript regular formula; evaluator.py query_ext | Regular extension-field formula and code already exist. A proposed extension must focus on uncovered exceptional cases or verified output normalization. |
| Branch points | Manuscript excluded-input discussion; evaluator.py _rphi | Generic code rejects d=0. No fast branch evaluator found in the inspected sources; manuscript retains linear streaming fallback. |

## Bounded question assessment

| Candidate | Concrete missing question | Assessment |
|---|---|---|
| Rational branch point on a cubic | Can the excluded coefficient query be reduced explicitly to first/second-kind Cartier data, and can the additional data be computed cheaply? | Recommended first mathematical target. Fixed genus, fixed cutoff, one excluded input type; a precise obstruction is a useful outcome. |
| Rounded supersingular third point | For p congruent to 2 modulo 3, L=(p+1)/3, recover a_L cheaply alongside existing B_L | Preferred alternative when complete original U is the immediate goal. Boundary, not prefix, is the new research problem. |
| Genus-two boundary | d=5, p congruent to -1 modulo 5, L=(p+1)/5; recover a_L cheaply | Useful but a harder arithmetic boundary problem. Begin with one endpoint; do not repeat the prefix prototype. |
| Precision-two correction | Obtain specified Witt coordinate without first evaluating B, and account for U's harmonic correction | Higher risk. Existing lifted coefficient and recurrence code are starting points, not a fast higher-modulus theorem. |
| Projective differentiated Miller arithmetic | Reduce inversion cost while preserving all normalizations and split/exceptional paths | Bounded implementation alternative. Any result is initially a constant-factor improvement, measured on identical outputs. |

## Recommended first target and assumptions

Question: for prime p at least 7, squarefree cubic f over F_p with f(0)=1, and a specified nonzero rational root mu, derive an exact expression for S_f(1/mu)=T_f(mu), preserving the coefficient cutoff p-1. Determine the minimal extra second-kind Cartier data and whether a bounded-cost geometric computation supplies it. Initially exclude quartics and extension-field arguments. Ordinary and supersingular cubic cases must be distinguished, not silently omitted.

The first deliverable is a separate proof note with explicit normalizations, plus independent finite checks after the derivation. Fast evaluation is an open goal, not an assumption. If the missing coefficient cannot be recovered cheaply by the proposed mechanism, retain the reduction and the obstruction and stop that mechanism. No all-stopping-index or complete-U consequence follows automatically.

## Derivation checkpoint and sign conventions

At the branch Q=(mu,0), take local parameter z=v. Squarefreeness gives w=mu+z^2/f'(mu)+O(z^4). Hence omega=dw/v=(2/f'(mu)+O(z^2))dz and

    theta = dw / ((1-w/mu)v) = -2mu*z^(-2) dz + O(1) dz.

This is a residue-free second-kind pole; the old residues -r,+r and r=mu/v0 are undefined when v0=0. The principal part equals d(2mu/z). This local equality does not prove a global fast evaluation formula: a global exact subtraction and its other poles must be tracked. No limit substitution into the admissible formula is justified here.

For the retained admissible formula, theta has residues -r at Q+ and +r at Q-, while div(F_D)=M(Q+-Q-). Thus M theta+r dlog(F_D) cancels residues. The retained model has omega=-2 dX/(2Y); nonvertical Miller lines contribute positive slope with z=-X/Y, so Psi=(alpha_plus-alpha_minus)/(-2). These conventions constrain any new formula but are not themselves a new proof audit.

Katz's standard cubic basis uses omega0=dX/Y and eta=X dX/Y with C(eta)=beta omega0, beta=[X^(p-2)]F(X)^((p-1)/2). His published paper was retrieved from the author's Princeton page and Section 1 inspected. This verifies the additional coefficient framework, not a fast algorithm or novelty. The scale relative to dw/v and the new second-kind representative must be derived explicitly; beta is not automatically supplied by a point count.

Source: Katz, N. M., On a Question of Zannier, published author-hosted PDF, https://web.math.princeton.edu/~nmk/zannier_publ.pdf, DOI 10.1080/10586458.2018.1551818. Accessed 6 October 2026. Only the stated Section 1 coefficient facts are used at this stage. Broader citation tracing remains pending. A guessed Voloch PDF URL failed retrieval and supplies no evidence.

## Independent checks, counterexamples and status

| Item | Evidence category | Current status |
|---|---|---|
| Local principal-part calculation above | New algebraic derivation | Direct substitution gives the displayed sign and scale. Not yet independently checked by symbolic or finite-field expansion. |
| Additional second-kind coefficient | Verified primary-source statement | Katz Section 1 identifies beta; no inexpensive recovery established here. |
| Existing quarter and third outputs | Newly rerun finite evidence | Seven smoke comparisons passed. Does not prove manuscript theorem or novelty. |
| Naive precision-two lift | Historical counterexample | Preserved report says p=13 predicts B=44 rather than 70 modulo 169; counterexample JSON retains actual B=70. Not rerun here. Failure excludes the tested formula, not every lift. |
| Universal higher-genus p+1 annihilator | Historical failed approach | Retained ledger records degree-five counterexamples at p=7,11,13. Not rerun here; do not extend the maximal-family claim to arbitrary curves. |
| Uniform fast U for all L | Unestablished stronger claim | No proof or prototype here establishes it. Both B_L and a_L are required. |
| Sum-avoiding fast Witt correction | Open research question | Existing source computes sum first; source inspection confirms that ordering. |

## Validation and benchmark contract

Before any extension implementation, inspect its relevant historical branch and source. Compare direct polynomial expansion with a separately derived expression on small squarefree cubics and all rational branch points in the chosen range; record seeds, exclusions, ordinary/supersingular coverage and counterexamples. Expand the range only after debugging and an independent derivation. Finite agreement is never labelled proof.

Any eventual original-U benchmark computes B_L, a_L and U modulo the same modulus as its comparator. Charge trace/model preparation, new second-kind preparation, reconstruction and certification as appropriate. Distinguish cached queries, complete per-input arithmetic runs and fresh-process wall times. Preserve raw CSV samples, source hashes, environment and validation records. Schoof remains the theoretical deterministic setup; the experimental Schoof/point-count BSGS sources are not production SEA. No new performance claim is made in this ledger.

## Reproduction and provenance

Fresh commands ran at the extracted root: python verify_package.py; python smoke_check.py. Both passed as described above. Historical timing CSVs and validation outputs are unchanged. The source fingerprint below identifies inspected inputs; it does not identify any GitHub commit.

```json
{
  "environment": {
    "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
    "platform": "Linux-6.18.44-x86_64-with-glibc2.39",
    "machine": "x86_64"
  },
  "sha256": {
    "START_HERE.md": "5f3fcb5edb8a467684b9d9dcd2c380db8dd7546488580b7fca1bdbfac79afab6",
    "PROJECT_STATE.md": "7a821cc813119ac47b81a396b8db8cb4d5e6f4936b2ce0ad31acc72f69c07538",
    "EXTENSION_ROADMAP.md": "9f20a976d8016903e01e6f5100ea0e027cf5dfe4af44f6071dc24fc0e042747a",
    "manuscript/Cartier_Miller_Paper_Revised_20261005.pdf": "196800df388896700e63d4733b4fc3de2cc9541158e1308cfe2523033ff9d700",
    "manuscript/Cartier_Miller_Paper_Revised_20261005.docx": "bd22ff7a6a8b780345ddd5f0ecac496de86db8d1a5628092038282ab738477ea",
    "code/third_point/third_point.py": "3301345fbaf29538fb55e852fe4da6f51cae2169800be9c46c131da8a66cd4b7",
    "code/quarter_benchmark_gui/elliptic_prefix.py": "3e79d82c931f41f3091e98f6f65783ce958f13851e2c6f05283efa2152c0634d",
    "proof/high_part_verification/retained/cmpkg/evaluator.py": "f8a14a311f3f608ec377a64e540a59f307158a0d1c43fb68d34c5155e492717f",
    "historical/higher_genus_20260928/scripts/hyperelliptic_prefix.py": "fc3b4b01ca4b28e85b927a55dfa2d341ba508dbef5c807e70272caef30a9b2ee",
    "historical/Witt_BGS_Precision_Two_20261001.zip": "4469f014a3d10b16368cb93775548b1618d724dd475b33fb02ae013f73c38ce4"
  }
}
```

## Branch-point investigation: completed bounded stage, 6 October 2026

Question and assumptions: p≥7 prime, squarefree cubic f=1+cw+bw²+aw³ over F_p with a≠0, and a supplied nonzero rational root μ. Evaluate the fixed-cutoff T_f(μ)=S_f(1/μ), with differential and coefficient conventions explicit and preparation separate from query work.

Derived result: H=[w^(p−1)]f^h, K=[w^(p−2)]f^h and T_f(μ)=aμ(μH−K)/f′(μ). The global exact subtraction is qμ=2μv/(f′(μ)(w−μ)), giving θμ=dqμ+(aμ/f′(μ))(μ−w)dw/v. The local principal part is −2μ z⁻²dz at z=v. Cartier kills dqμ and selects (H,K). A separate polynomial proof derives f′R+2fR′=aK−aHw from the high part of f^h. These proofs are in the separate note; human mathematical review remains pending.

Classical overlap: Voloch's Section 2 lemma already gives the monic high-part identity. The author-hosted manuscript was read; journal metadata were checked at the publisher, whose PDF endpoint returned 403. Katz's published author-hosted Section 1 and Theorem 3.1 confirm the Cartier coefficients and the no-common-zero statement. No novelty is claimed for the branch corollary. The independently written algebraic proof does not depend on the quasi-period signs discussed elsewhere in those sources.

Normalization: x=aw+b/3, y=av gives the short cubic with infinity origin and dw/v=dx/y=2dx/(2y). Its second-kind scalar β satisfies β=aK+(b/3)H. This is a different model from the retained construction with rational origin and κ=−2. The old model and manuscript are unchanged. A rational branch gives rational 2-torsion, so the trace is even; no trace ±1 exceptional normalization is needed by this extension.

Implementation: branch_evaluator.py computes H,K using V_n=n!(c_n,c_(n−1),c_(n−2)) and a 3×3 degree-one matrix product, streamed with three retained elements. Wilson gives H,K by negating the first two final entries. Default preparation is O(p) field operations and constant working field elements; the supplied-root query is O(1). The 64-bit prime guard follows the retained third-point implementation. Supplied Cartier data and supplied exact traces are explicitly marked trusted; a Hasse-bound check alone does not certify a trace. No production Schoof/SEA or fast BGS backend has been added.

Established-cost consequence: the explicit matrix falls within the existing polynomial-block/BGS recurrence framework, giving soft-O(√p) preparation with fast polynomial arithmetic. That backend was not implemented or benchmarked here. Generic polylogarithmic K recovery remains unresolved; point counting alone does not establish it. There are at most three rational branches per cubic, so query amortization must not hide setup.

Bounded fast subfamily: on the short model, A=0 with p≡1 mod 3 or B=0 with p≡1 mod 4 forces β=0 by exponent support. Thus K=−bH/(3a) and T=μH(aμ+b/3)/f′(μ). Exact trace preparation through Schoof gives a deterministic polynomial-time complete-run consequence. prepare_from_trace() implements only coefficient recovery from a trusted supplied trace. It was checked on 527 curve cases and 1,181 branch queries overlapping the main tests.

Independent checks: exhaustive normalized cubics at p=7,11,13,17,19,23 include 26,292 candidates, 1,344 singular rejections, 24,948 squarefree curves, 9,240 without rational roots and 15,708 branch-bearing curves. All 22,260 rational branches were checked. Held-out seed 202610062106 constructs 16 cases at each of 45 primes from 29 through 251; 712 squarefree cases supply 1,476 queries, after eight singular cases. All 23,736 queries pass dense polynomial power and coefficient-functional comparisons. Additional checks cover the cleared global differential identity, full high-part identity, direct point counts, short-model scale/conversion and 1,972 unreduced integer powers. Coverage includes 2,892 exhaustive and 45 held-out supersingular curve cases. Six expected invalid inputs are rejected. Validation elapsed time is not benchmark evidence. Source hashes, environment and raw validation CSV are retained.

Counterexamples and stopped shortcuts: at p=7, f=1+4w+w²+w³, μ=1, H=0,K=3,T=2. Dropping K gives zero; dividing by H fails; extending β=0 to supersingular j=1728 also fails. At the same prime, f=1+w³ and f=1+w+w²+w³ have the same trace −4 and root μ=6, but K=0 and 5 and T=1 and 4. This shows trace alone does not determine K; it is not a lower bound on algorithms receiving the full curve. The attempted counterexample key initially also fixed f′(μ), which overconstrained the normalized cubic and could not yield distinct curves; the final key uses trace, root and leading coefficient. An invalid-input test initially treated 2 as a nonroot of 1−w³ modulo 7; that fixture was corrected to 3. Neither issue was a mathematical formula failure.

Rounded-third bridge: for p≡2 mod 3, f=1−w³/2, L=(p+1)/3 and μ³=2, K=a_(L−1) and a_L=(3μ/4)T_f(μ). All 47 applicable primes from 7 through 499 passed a separate direct boundary recurrence comparison. This relates the missing boundary to the supersingular branch problem; the linear implementation supplies no new fast complete-U theorem.

Current status: the explicitly normalized branch formula is proved in the separate unrefereed note and its complete linear prototype passes finite checks. The ordinary structural fast corollary is proved by sparsity and its trusted-trace route is checked. General fast K preparation beyond established recurrence bounds remains open. The published manuscript has not been revised, GitHub has not been inspected, and no new timing comparison is asserted.


## Parallel K-recovery investigation, 6 October 2026

Question: recover the missing coefficient K quickly beyond the already completed ordinary beta=0 cases. Two user-authorized complementary branches investigated low-degree isogeny transport and formal Hasse jets, after checking retained implementations and historical branches. The structural derivation proves beta'_short=2beta_short-(t/3)H for the displayed normalized degree-two map, with holomorphic scale +1 and explicit global exact term -2d(y/x). It yields beta=-rH for A=-11r^2,B=-14r^3 at p congruent to 1 modulo 4. Thus K=-(r+b/3)H/a, with constant reconstruction after exact trace preparation; the trusted-trace prototype is implemented. Complete theoretical preparation remains T_Schoof+O(1), not a cached-query timing claim. A second j=54000 corollary is algebraically derived but not implemented.

General derivation: Delta H_A=-A^2H+(9/2)B beta and Delta H_B=-(9/2)BH-3A beta. Explicit global differential identities prove both signs. These identities include supersingular inputs and make the first-jet and missing-coefficient problems equivalent up to constant work once H is known. No faster generic jet oracle is established. Finite differences of scalar traces fail (p=13,A=0,B=1: H_B=4, finite difference=6). Rational values do not specify formal derivatives without the canonical polynomial; nilpotent Frobenius and transverse CM derivatives obstruct the naive shortcuts. No lower bound or general impossibility claim follows. The initial scratch B-derivative signs were corrected by a p=7 fixture, exhaustive checks and independent parent algebra before delivery.

Independent checks: structural agent 7,688 transport pairs, 184 normalized family curves and 344 branch queries; parent independent multinomial transport check 15,872 pairs including 1,996 supersingular cases. General agent 3,682 cubics including 366 supersingular; parent differentiated multinomial check 16,288 including 1,360 supersingular. Counts overlap and are not added. All passed. Supersingular extension of the family rule fails at p=7,r=1: H=0,beta=6. Numerical agreement is supporting evidence, not proof. CSVs, environment summaries, source hashes and independent scripts are retained in K_Recovery_Parallel_Research_20261006.zip.

Current status: one modest additional structural family has an unrefereed proof and tested reconstruction prototype; general fast K remains open. Recommended next bounded target is rational degree-two isogeny closure of known ordinary families, charging chain search separately and working out all coordinate scales. Primary Sutherland, Katz, BGS and Schoof sources were verified, but no novelty claim is made. The published manuscript and original scope are unchanged; no GitHub inspection, uniform stopping-index result or fast sum-avoiding Witt claim is asserted. See K_Recovery_Parallel_Research_20261006.md and the two branch notes for full assumptions, derivations and obstructions.


## Bounded rational degree-two closure, 6 October 2026

Question and assumptions: extend trace-only second-kind recovery to curves with verified rational degree-two paths to the existing ordinary beta-zero seeds. Prime p>=7, squarefree normalized cubic, exact supplied trace, roots in each displayed short model. Two authorized complementary branches independently studied theory and graph coverage; retained implementations/histories were checked before the new core implementation.

Derivation: a short rational root q gives A'=-4A-15q^2,B'=-8Aq-22q^3; the global pullbacks are omega'=omega and eta'=(2x-q)omega-2d(y/(x-q)). Hence H'=H,beta'=2beta-qH, with differential scale+1. For an input-to-seed chain, beta_input=H sum q_i/2^(i+1), then K=(beta-bH/3)/a. A supplied m-edge certificate costs O(m) field work after exact trace preparation; supplied-root branch queries remain O(1).

Implemented prototype: exact-model breadth-first search, depth2 by default, uses gcd(F,x^p-x) and randomized fixed-degree linear-factor splitting. All returned roots are verified against that gcd. Uncapped expected discovery cost is O(3^d log p) field operations; the capped implementation has explicit incomplete_root_splitting and no O(p) scan fallback. Successful paths are checked. Completed negative searches cover only the selected depth; no global coverage claim. Deterministic supplied-path setup remains T_Schoof+O(m); automatic discovery is a separate randomized cost. The caller's trace is trusted, not certified by the Hasse bound.

Additional explicit family: for e^2=2,p=1mod8,r nonzero, the nondual depth2 quotient of y^2=x^3-r^2x has A=(-91-60e)r^2,B=(-462-308e)r^3,beta=-(3+2e)rH. It has an unrefereed proof and1504 parameter checks. A sqrt3 j0 analogue is algebraically derived but not parameter-validated in this pass. General twists have H_d=chi(d)H,beta_d=d chi(d)beta. Dual backtracking returns16A,64B,4beta and no new constraint. A nondegenerate supplied closed-chain coefficient certificate is a proved separate corollary with225 checked instances, not integrated into core search; discovery is unresolved and supersingular denominators necessarily degenerate.

Independent checks: core7948 nonsingular short cubics at primes7..43;760 found (276depth0,276depth1,208depth2),7188 bounded misses;186 normalized cubics and330 original branch queries pass independent dense sums and exact direct traces.7688 rooted/dual and15896 twists also pass. Independent dense graph audit7420edges/4960models through p127 identifies genuine new depth2 j classes at ten tested primes. Theory multinomial audit15872rooted/dual,47616twists,3600prefixes,1504familyparameters,225closedchaininstances passes. Counts overlap/repeat and are not added. CSVs, JSON, seeds, environments and hashes are retained. Finite checks are supporting evidence, not proofs.

Concrete example: p13 short(12,10),roots5,12 leads to(6,7) theneasy(0,5),H11,beta2,j6 outside allseed/depth1 jsets. Normalized f=1+12w+9w^3 has short(4,3),roots11,3,H11,K8,mu7,T2. A retained miss p13 short(1,1),j7 is outside the depth-at-most-two closure. Ordinary seed classes are unavailable at p=11mod12. Root splitting exhaustion remains distinct from a completed miss.

Implementation repairs retained: normalize zero polynomial input in gcd; ensure new preparation-method string carries caller_supplied so queries report computed_from_trusted_data. All330 final query status checks pass. Neither was a mathematical transport failure. Real obstructions remain dual scaling, j-only normalization ambiguity, supersingular unknown amplitude and potentially expensive deeper search.

Current status: reviewable proof notes, tested supplied-path recovery and bounded randomized discovery are complete. No novelty, benchmark, generic fast K, all-stopping-index theorem or fast sum-avoiding Witt claim. Primary Sutherland,Katz and vonzurGathen-Panario texts checked. Manuscript unchanged; GitHub uninspected. Next bounded target: direct parameter certificates for depth2 families and their twists, followed by depth3 coverage accounting for dual steps; closed-chain discovery remains a separate exploratory question. See Degree_Two_Closure_Report_20261006.md and Degree_Two_Closure_Research_20261006.zip.


## Direct depth-two recognition and higher-depth audit, 6 October 2026

Question: derive parameter-checked certificates for the depth-two ordinary families including twists/exceptional reductions, and determine which higher-depth paths add classes after removing dual scaling. Retained sources and previous closure prototypes checked before implementation. Two authorized complementary branches supplied theory and a true-Fp-class graph audit; the parent derived independent constants and implemented a separate recognizer.

Algebraic result: complete rational easy-seed closure throughdepth2 consists of the full ordinary A0/B0 seeds, twoone-step families and the two nondual families e²2,p1mod8 and e²3,p1mod12. Writing alpha³=a0+a1e,gamma²=g0+g1e gives U=a0B²-g0A³,V=a1B²-g1A³,e=-U/V,r=alpha B/(gamma A). Verify congruence,e²=n,r nonzero,bothcoefficients and reversepath. Everyquadratic twist is absorbed by r->dr. Recognition needs O1fieldwork,no square-root or graphsearch. Complete unconditional acceptedinput preparation is T_Schoof+O1; suppliedtraces remain trusted. Queries O1 withsupplied originalbranchroot.

Differential/pole audit: rootedglobalcorrection -2d(y/(x-q)), holomorphicscale+1. Infinityparameter t=-x/y gives eta+2t^-2dt; kernelparameter z=y gives primitiveF'(q)/z and exactcorrection+2F'(q)z^-2dz; both residueszero. No local-only normalization substituted. K=(beta-bH/3)/a retained.

Exceptional reductions: exactnorm/determinant/resultant factors excludeeverycoefficientzero, extractionfailure, conjugate/lowerdepth/mixedcollision ateligibleordinaryprimes>=7. Actualoutside-rangecollapses retained atp7,p11,p23. Bothjpolynomials agreewithclassicalCMtables discriminants-64/-48; no newcurve/classpolynomial claim. Proofnotes unrefereed and requirehumanreview.

Prototype/evidence: directrecognizer all137086nonsingularshortinputs throughp127 vsindependentdepth2seedgraph gives4960positives/132126negatives.4960Hbeta pairs,9920twistcertificates,66normalizedcubics/154branchqueries pass. Independenttheory5208parametercases,1176pairs,69192family-specificmembershipdecisions and56exceptionalrows pass; exactintegerauditchecksallfactoredidentities. Counts overlap and arenotadded.

Higherdepth finitefindings: all12288 trueFpisomorphismclasses at51primes7..251 counted via square-coordinate scaling, preservingnonsquaretwists. Pruned/unprunedminimumdistances andfullfiniteclosure agree. Depth3adds64classes/32jvalues,depth4adds32classes/16jvalues acrosstheseprimes; noclassafter4inthisinterval,no uniformradiusclaim. Explicitp73target4,16 H10,beta4,j20 withreversekernels71,6,43; normalizedf1+4w+37w³,K55,mu9,T3 checkedindependently. p193depth4target131,85 H191,beta81,j61 withreverse81,21,2,160.

Retainedrealobstruction: p13short1,1 τ-4,H9,beta8 shares an easyseedtrace but complete rational2component hasonlyclasses1,1 and2,3, connectedbyroot7 thenimmediatedual12 withsquare-scaledreturn3,12. Bothquadraticresidualdiscriminants nonsquare,so noother rationaledges. Thus traceplusrational2torsion doesnotcertifyseedreachability. Finitecensus780ordinaryseed-tracematchedunreachableclasses includes496withrational2torsion. This isnotalowerboundforotherKmethods.

Searchcost: theoreticaldual-prunedtree has1+3(2^d-1)vertices andexpectedO(2^d logp)fixed-degreefactorwork. Retained productionfinder remainsunprunedO(3^d logp); no implemented/timingimprovementclaimed. Auditroot/isomorphism scans arevalidationonly. CSVs,allcertificates,JSON,environments,seeds,hashes retained inDepth_Two_Recognition_Research_20261006.zip.

Currentstatus: directdepth2recognitionproof/prototypecomplete,higherdepthfiniteauditcomplete, generic/supersingularKopen. No manuscriptrevision,GitHubinspection,uniformstoppingindex orfastsum-avoidingWittclaim. Nextboundedtarget: oneexplicitdepth3parametercertificate,usingclassicalCMcontextwithoutdiscardingthecoordinatefactor. SeeDepth_Two_Recognition_and_Higher_Depth_Report_20261006.md.
