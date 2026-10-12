# B=0 depth-three family: independent adversarial review

12 October 2026. David Jordan's Cartier–Miller extension programme. Unrefereed, AI-assisted review of the supplied 12 October handover, proof note and ledger. The manuscript and supplied originals are preserved. No GitHub repository or commit was supplied or inspected. No novelty or wall-time performance claim is made.

The attempt appears successful for its stated bounded ordinary family. I found no flaw in the family formulas, normalized second-kind coefficient, direct recognition, twist coverage, eligible-prime collision exclusions, or exact classical trace preparation. The mathematical argument survives independent derivation and considerably enlarged finite checks. The material needs some scope corrections and a verified source for its eligibility equivalence; that missing source is supplied in the companion proof-review addendum. A minor certificate-schema defect has a minimal optional patch.

## Assessment by claim

| Claim | Review result | Evidence category |
|---|---|---|
| Family alpha(s), gamma(s), s^4=2, and the three kernel roots | Independently re-derived exactly from the two-torsion quotient | Exact algebra, unrefereed |
| beta=-(7+4s+6s^2+4s^3)rH | Correct, using differential scale +1 and beta'=2beta-qH on each edge; reverse path agrees | Explicit differential and Cartier derivation |
| Sound, complete and unique parameter extraction | Correct at every eligible prime; all extraction denominators excluded by exact integer arithmetic | Algebraic proof plus independently verified finite integer certificate |
| Every quadratic twist | Included by r->dr; coefficient and trace signs independently checked | Algebra and finite controls |
| Eligibility p=1 modulo 8 with 2 a quartic residue iff p=x^2+64y^2 | Correct; the inherited numerical evidence has been supplemented by a directly read classical reciprocity proof | Verified primary source, with explicit deduction |
| No collisions with the retained lower-depth and A=0 depth-three families | Exact norms, class-polynomial evaluations and resultants independently recomputed; none has an eligible prime factor | Exact integer exclusions |
| Exact target trace 2(r/p)a | Correct classical formula; Theorem 5's signs and conjugations visually verified | Ireland–Rosen theorem and explicit specialization |
| Complete preparation without point counting | Correct for recognized members; randomized nonresidue search remains | Implemented route; expected, not deterministic, complete complexity |
| Identification with polclass(-256) | Exact determinant polynomial independently verified against retained coefficients; no fresh PARI run in this environment | Algebra checked; PARI identification retained |
| Ready to claim novelty or general K recovery | No | Separate literature and human review required |

## Independent computational checks

| Check | Fresh result |
|---|---|
| Original package verification | 272 hashed files; smoke checks passed |
| Delivered B=0 validation suite | Passed, reproducing the 461,760-model eight-prime classification and its other controls; PARI unavailable in this rerun |
| Delivered exact derivation suite | Passed |
| Independent exhaustive classification | 1,885,840 nonsingular short models at twelve eligible primes through 617; exactly 16,448 accepted |
| All parameters and twists at those primes | Four conjugates times every nonzero r; injective, accepted, correct forward endpoints and nonzero denominators |
| Independent graph reference | Keeps previous dual root in its state; all brute-force nondual endpoints coincide with the family |
| Independent H, beta and exact point counts | 1,268 member checks; complete coverage at p=73,89,113 and fresh samples at the other primes |
| Original normalized cubics | 60 branch queries from 36 independently constructed cubics; H,K and strict-block T checked against dense polynomial powers |
| Ineligible inputs | 2,456 fresh nonsingular inputs at 25 ineligible primes, including supersingular quartic-root cases |
| Prime-eligibility controls | Every prime between 7 and 5,000; 81 eligible; independent integer representation matches the quartic test |
| Large-prime controls | 15 independent group-arithmetic trace-sign witnesses on retained examples up to 63 bits; all four parameter conjugates also checked |
| Integer proof certificate | 14 exact identities; all factors independently trial-divided, maximum factor 12,263, every product multiplied back |

The large-prime witnesses check that p+1-tau annihilates a point while p+1+tau does not. With the classically justified two candidate traces, this verifies the sign. It is not an independent general point-counting algorithm. The output CSVs preserve the actual points and outcomes. Finite agreement is implementation evidence, not a proof of the all-prime statement.

## Findings requiring correction

The proof note's opening outcome paragraph still calls the B=0 family deferred. Its title, START_HERE's introductory description and README's concluding eligibility sentence also retain the former A=0-only scope. These are material handover inconsistencies but do not affect the new formulas or code.

The inherited eligibility paragraph explicitly had only finite validation of the representation equivalence and an unopened Cox pointer. The companion addendum now establishes it from Lemmermeyer's directly read Gauss criterion: for p=a^2+b^2=1 modulo 8, (2/p)_4=(-1)^(b/4). Consequently 2 is a fourth power iff 8 divides b, giving p=a^2+64y^2. The Cornacchia divisibility guard and trace-magnitude condition therefore have a verified justification independent of those numerical checks.

The certificate verifier rejects unknown top-level fields but silently ignores unknown nested parameter fields. The injected counterexample is parameters.unverified_note='deliberately injected' on the valid p=73 certificate. The returned certificate is recomputed and mathematically sound; this is a strict-schema issue, not a false mathematical acceptance. PATCH_VALIDATION.json and the optional patch show that valid certificates still pass and that the unknown key is rejected.

An opposite caller-supplied trace passes the documented necessary condition if verify_trace=False. At p=73, supplying +6 to the fixture whose true trace is -6 yields H=6 instead of H=67. This is expected for an explicitly trusted input, not a bug. verify_trace=True rejects it. Any independent-input or benchmark contract must certify the supplied trace or charge the complete classical preparation.

The API's positive extraction is fixed field work, but rejecting a non-member at p=1 modulo 8 computes a quartic-residue exponentiation for its status label. A blanket constant-time claim for the entire API would therefore be inaccurate. Prime validation also lies outside the constant extraction count. Full preparation remains randomized only in the nonresidue search, with expected polylogarithmic work; the deterministic trace formula must not be described as a deterministic complete preparation.

## Consequence for Cartier–Miller

This closes the previously deferred ordinary B=0 depth-three recognition question in the same bounded sense as the earlier A=0 result. For accepted cubics it supplies the original-model second-kind coefficient beta and hence K, and prepares H through the classical seed trace. Supplied nonzero rational branch queries then use fixed field work. The new source bridge, clear costs and strict-schema patch make the review concrete and reproducible.

The result does not compute the missing rounded-third boundary a_L, give a uniform method at every stopping index, provide generic/supersingular K, extend to depth four, or establish a sum-avoiding precision-two Witt correction. Both depth-three families and their CM class polynomials are classical objects. The possible contribution is the explicit normalized coefficient transport and parameter-checked recognition for this application; its novelty remains unassessed.

I would describe the extension as having passed an independent adversarial AI review, with the small corrections above, and submit the algebraic note and evidence to human specialists. This is stronger than numerical agreement alone and weaker than a refereed proof.

The exact derivation, literature conventions, cost contract and source references are in PROOF_REVIEW_ADDENDUM.md. RESEARCH_LEDGER.md records the question, assumptions, checks, counterexamples and remaining limits. The archive includes the original handover, independent script and CSVs, input hashes, environment information, rerun results and optional patch. No arithmetic benchmark was conducted.
