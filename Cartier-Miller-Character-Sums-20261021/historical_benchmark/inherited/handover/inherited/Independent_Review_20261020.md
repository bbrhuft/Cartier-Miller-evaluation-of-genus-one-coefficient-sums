# Review of Opus’s Cartier–Miller character-sum package

Prepared 20 October 2026 for David Jordan. Independent AI-assisted review; not specialist peer review. The supplied archive and manuscript insertion were not edited. This review does not establish novelty or performance superiority.

## Assessment

The package provides a coherent application framework, a working layer around the inherited Miller evaluator, and useful extensions beyond the original handover. The simple-pole, normalization and exclusion framework is suitable for development into an application section after the corrections below. Branch formulas and the reduction to the rounded-third factorial are worthwhile additions to the scope discussion. The broad higher-order-pole claim should remain in an extension note until its characteristic-p restrictions are made explicit.

The main positive development beyond Sol’s supplied summary is the closed branch formula for cubic and quartic models. In a quartic, a reciprocal coordinate change makes c_(p-2) accessible by a nonbranch Miller evaluation, leaving c_(p-3) as sufficient additional prepared data. The cubic uses c_(p-2). These are sufficient-data statements, not computational lower bounds.

The package itself distinguishes exploratory implementations from unimplemented asymptotic refinements. Its fast multipoint corrections and lockstep batching were not benchmarked or implemented here. No matched timing comparison has yet been established.

## Materials and integrity

The attached REPORT_Opus.md and PROPOSED_APPLICATION_SECTION.tex are byte-identical to the corresponding files inside the supplied ZIP.

The ZIP SHA-256 is 51fb45ac883dbf1e10ba5a647585424504ed9eaf95344f42a8c7f9675eeb49c6.

The report SHA-256 is 1403ef69591c45539e431d67258b51306752a4ea3161ca7196f4e596786f6b01.

The candidate src/cmcs.py SHA-256 is 763c86811e5b43bb0c00791f83083420c27232a04d131633c6a6c3552bb3e59c.

Every one of the 48 SHA256SUMS.txt entries matched before execution. The 32 frozen files matched FREEZE.json, including its aggregate digest 4302b56426a6160fbc5027659632bac7ad6cc0ab755c5fcb00d8c9502aa99bd3.

Hashes establish correspondence of the files reviewed; they do not independently establish execution history or an externally timestamped freeze. The manuscript and repository commit named in Opus’s provenance were not independently retrieved in this review.

## Independently rerun evidence

The runtime was CPython 3.12.14 with numpy and python-flint 0.9.0. PARI/cypari2 was unavailable. For the extended and exploratory suites, reference.trace_pari was replaced in memory by reference.trace_by_count; no source file was changed. All primes reaching that substitute in these runs are small enough for direct point enumeration. Therefore these runs validate the evaluator against direct point counts and FLINT, not the PARI adapter.

| Rerun | Results |
|---|---|
| Supplied standard-library verifier, unchanged | PASS; 132 generated models plus the p=101 example; four trace +1 and fourteen trace -1 generated models |
| Extended verifier | PASS; 133 models, 3,288 inherited returned queries, 159 exceptional queries, 457 split fallbacks, 51 cubic branch-service queries; 65 expected quartic branch refusals |
| Candidate checks in extended verifier | PASS; 3,353 single-pole values, 2,394 normalization checks, 2,394 multi-pole checks; no mismatches |
| Closed branch formula | 97 checks, zero failures |
| Double poles | 6,281 checks, zero failures |
| Polynomial parts | 126 checks, zero failures; 21 quartic linear sums used Miller |
| Single-point exclusion | 1,550 checks, zero failures |
| Supplied second-kind data path | 1,416 checks, zero failures |
| Dual-number experiment | All 242 completed value checks agree; only 3 formal-derivative comparisons agree; 260 attempts degenerate, reproducing the original result |

The extended verifier’s 8,141 application checks are the sum of its single-pole, normalization and multi-pole counters. These counts are checks, not distinct curves or statistical confidence estimates.

Opus’s archived development and confirmation files report 208,272 and 261,423 checks respectively, both with zero failures. Those two complete suites were not rerun. In particular, this review does not independently reproduce the large-prime PARI-dependent tests. The bounded reruns above reproduce the extended and exploratory suite counts precisely.

The dual-number result illustrates the failure of that attempted differentiation procedure. It does not prove an impossibility theorem for all derivative or coefficient-extraction algorithms.

## Corrections required before manuscript insertion

### Complete excluded set in the several-pole theorem

The report’s Theorem C and proposed Theorem A2 introduce distinct mu_1,...,mu_s belonging to U, but do not explicitly require that they enumerate U. Their displayed correction sums are correct when U={mu_1,...,mu_s}. They are generally false when U contains further omitted points not included in the correction indices.

A concrete squarefree example is p=7, f(x)=1+x+x^3, R(x)=1/(x-1), with U={1,2}. The unrestricted single-pole value C_f(1) is 0, whereas the common-domain sum omitting both 1 and 2 is 6 modulo 7. The extra missing term is chi(f(2))/(2-1)=1.

The simplest repair is to state U={mu_1,...,mu_s} explicitly and permit zero coefficients for additional exclusions, as the report already intends. Alternatively, index corrections over every u in U, using the regular finite part of R there. The candidate implementation already handles explicit additional exclusions, so this is a theorem-statement issue rather than an observed implementation failure.

### Projective sums and rational points at infinity

The report and proposed insertion say that no projective sum is defined for a positive-degree polynomial part because it has poles at infinity. This is too strong for a sum over E(F_p).

For a quartic with nonsquare leading coefficient, there are no F_p-rational points at infinity. A weight such as x has geometric poles at nonrational infinity points but is defined at every rational point included in the sum. The projective rational-point sum then equals the affine sum.

For example, p=7 and f(x)=1+3x^4 give a squarefree quartic with N_infinity=0. The sum of x over all rational points is well-defined and equals its affine value, 0 modulo 7. The candidate deliberately rejects this request under its stricter projective routing convention.

Either retain that stricter API and state that the investigation restricts projective weights to those regular at every geometric point at infinity, or allow polynomial weights when N_infinity=0. Do not describe the rational-point sum itself as undefined in that case. For a cubic, or a quartic with rational infinity points, a nonconstant polynomial weight does have poles at rational points that would otherwise be included.

### Quantify higher-order-pole and polynomial-degree restrictions

The proposed final scope paragraph omits the boundedness qualifications used earlier in the report. The exactness reduction has characteristic-p resonances. Its leading coefficients include -(k-1)f(mu) at a nonbranch pole, (1/2-k)f'(mu) at a branch pole, and ell(j+D/2) for polynomial reduction. They cannot be inverted when they vanish modulo p.

State precise nonvanishing conditions and the range proved. In particular the branch coefficient vanishes at k=(p+1)/2, and the cubic polynomial coefficient vanishes at j=(p-3)/2. Merely saying the orders are below p is insufficient. The implemented double-pole and degree-at-most-three checks do not validate a general reduction for arbitrary orders.

### Sufficiency is not necessity

Replace universal phrases such as “exactly one scalar is needed” and “the only scalar not reachable by Miller” by a precise sufficient-data statement: the proved reductions can be evaluated given the specified coefficient, trace and available Miller values. No general computational lower bound or impossibility of another Miller-based construction was established.

The rounded-third factorial reduction is a strong, concrete equivalence for that family. It does not turn an open acquisition problem into a proved lower bound. Likewise, “no polylogarithmic acquisition is known” should be qualified as a statement about the present investigation until the primary-literature audit is complete.

### Domains of general functions and single-point exclusion

The report’s fibrewise cancellation remark must assume that the rational function being summed is regular on the included fibres, with removable singularities evaluated by their limits. At a branch point, y=0 does not justify assigning 0 to yB(x) when B has a pole there.

The single-point-exclusion formula involving (y+y0)/(x-mu) should explicitly say “affine”: on a cubic this function has a pole at infinity, so an unrestricted projective interpretation is invalid. The supplied exploratory test uses affine points.

### Small bookkeeping corrections

The complexity discussion’s sentence that s>=p-D-1 is “degenerate” is not generally true. That inequality marks a range in which a full-field search costs O(s); degeneracy itself requires U union roots(f)=F_p. The code tests the actual coverage condition.

Cached model/session storage should be distinguished from temporary working storage when discussing an arbitrarily long sequence of changing pole sets.

The existing endpoint-check method reruns the Miller chain. The endpoint is already available during the original chain, so exposing/checking it there could be inexpensive; calling the separate method currently incurs additional work. Passing such a necessary check does not certify the trace.

## Recommended integration and next phase

Keep the all-point polynomial-division identity, nonbranch multi-pole theorem, normalization/trace transfer and explicit costs together in the application section. Integrate them with existing Corollary 1.1 and equations (50)–(51), avoiding duplicate proofs and claims.

Place the branch formula and the rounded-third factorial reduction in the scope discussion or a short linked proposition. Retain general higher-order poles, unimplemented multipoint batching and the jet experiment in the companion report until their scope is fully specified.

Proceed to primary-source comparisons and matched-output benchmarks after applying the statement corrections and freezing the resulting benchmark candidate. Essential comparisons include the Voloch/Semaev high-part and logarithmic-transfer constructions, generic polynomial-coefficient recurrences, and shared full-polynomial preparation for dense query workloads. Charge trace/model preparation separately and also report complete first-query costs. A point counter alone does not return the weighted sum and is not a matched comparator without an adapter.

No universal timing advantage or best-known bound is established by this review.

## Reproduction of this bounded review

Run from a disposable extracted copy of the Opus package, with numpy and python-flint installed. The sources remain unchanged; the original scripts write results into the disposable copy.

```bash
python supplied/verify_character_identities.py
python src/verify_freeze.py
```

For the implementation and exploratory reruns, execute the following separately, setting script to the desired path:

```python
import runpy
import sys
sys.path.insert(0, 'src')
import reference

def small_trace(f, p):
    if p >= 5000:
        raise ValueError('This review adapter is restricted to small primes')
    return reference.trace_by_count(f, p)

reference.trace_pari = small_trace
script = 'src/verify_character_identities_extended.py'
# Alternatively: script = 'src/exploratory_jets_and_closed_forms.py'
runpy.run_path(script, run_name='__main__')
```

This substitution intentionally does not verify the PARI adapter and must not be used to claim an unchanged full-suite reproduction.
