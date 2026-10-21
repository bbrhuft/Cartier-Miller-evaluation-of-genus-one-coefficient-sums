# Cartier–Miller audit: mathematical repairs and primary-source follow-up

21 October 2026

The exceptional normalization and general-trace identity now have a common symbolic proof. The corrected evaluator explicitly handles the adapted 2-torsion point, supports p=5 by bounded enumeration, and gives every intermediate Miller identity step a proved meaning. The new work supports retaining the sparse-query application while keeping publication priority provisional. No new performance campaign was run and no complete manuscript was edited.

The key mathematical step strengthens the audit's rational-point formula. For a rational nonbranch P=(a,b) on a short cubic, and any geometric Q with [p]Q=P, it proves

\[
bV(a)=A\alpha_p(Q)-\alpha_p(Q)^p.
\]

If p is coprime to the rational curve order, choose rational Q=[p^{-1}]P, recovering bV(a)=(A-1)alpha_p(Q). For integer trace one, the Frobenius relation gives Phi Q=Q-P. A divisor identity for Miller functions gives alpha_p(Q)^p=alpha_p(Q)-alpha_p(P), and hence bV(a)=alpha_p(P), with the positive sign fixed symbolically. This avoids the inherited exceptional-normalization lemma and the printed quasi-period sign convention. Full arguments are in PROOFS.md and its LaTeX/PDF versions.

The quartic decomposition is verified as an exact rational identity, and a separate negation argument covers nonzero 2-torsion R. The general proof applies to supersingular curves as well as ordinary curves when the rational group order is prime to p. The evaluator still assumes a prime field, a smooth cubic/quartic, a nonbranch pole, and a correct supplied signed trace. An endpoint test is not a trace certificate.

I also correct an overstatement in the preceding independent review: Opus's report globally specifies p>=7. The p=5 example was therefore not a counterexample to its stated theorem. It exposed an unguarded implementation boundary; the new API extends that boundary explicitly. For p=5, f=x^3+3x, a=1, trace=-4, the repaired code returns 1. For p>=7, the Hasse bound makes the trace-one case the only rational group order divisible by p.

## Reproducible evidence

| Check | Result |
|---|---:|
| Development direct weighted-sum comparisons | 13,264, all agreed |
| Included p=5 comparisons, all admissible degree-3/4 models and nonbranch poles | 10,000, all agreed |
| General cubic identity checks against explicitly powered high blocks | 45,720, all agreed |
| Exceptional positive-sign checks against explicitly powered high blocks | 1,992, all agreed |
| Explicit Miller-function local expansions versus slope accumulation | 19,200, all agreed |
| Miller-function addition identity checks | 46,352, all agreed |
| Confirmation after the three-file evaluator/verifier freeze | 3,840 values on 320 models, all agreed |
| Compatibility replacement checks | 225, all agreed |
| Symbolic model/decomposition/adapted-point checks over rational polynomial coefficients | Three exact zero remainders |

The confirmation run used primes 41, 103, 163, 251, 239, 113, 167, and 1009, disjoint from this repair's development primes. Its seed was the frozen source digest `1bf336f3c5b1ef6672f77cc30aed53178e691a8468d92b2173871d659e9911f0`. It includes 95 exceptional, 36 explicit 2-torsion, and 3,709 general-route values; 455 general/exceptional chain flags record passage through O, and 180 values have supersingular trace. These are bounded checks, not independent statistical samples or proof of universal correctness. The freeze covers the three files named in FREEZE.json, not the prose, symbolic checker, or compatibility patch. The final package manifest separately hashes all delivered files.

The main evaluator and numerical verifier use the Python standard library. The optional exact symbolic checker used SymPy 1.14.0. No PARI trace, native comparator, inherited Cartier–Miller implementation, or Sage installation is required for these repair checks.

## Complexity and benchmark interpretation

After the exact trace is supplied, the nonbranch query uses O(log p) field operations, counting inversions, and constant many field registers. With ell=ceil(log2 p), modular multiplication cost M(ell), modular inversion cost I(ell), and integer modular-inverse cost E(ell), a safe bit bound is

\[
O\left(E(\ell)+\ell\bigl(M(\ell)+I(\ell)+\ell\bigr)\right).
\]

This gives O(ell³) with classical arithmetic and soft-O(ell²) with fast arithmetic. Exact trace acquisition is added separately. These statements do not extend the same query bound to branch poles or arbitrary higher-order rational weights.

Harvey's Theorem 10, now read directly from the supplied paper, supplies the comparator's interval-product theorem with its order, disjoint-interval, unit, and interpolation-inverse hypotheses. Applying it to the cleared-denominator coefficient recurrence gives the trace-free soft-O(sqrt p) comparison. The original timing data remain unchanged. Correctness of the revised route is not a fresh timing result, and the new route's earlier post-freeze exploratory timings remain labelled exploratory.

## Historical conclusion and remaining access gaps

Miller's 2004 paper supplies the classical divisor recurrence. Galbraith's accessible Chapter 26 explicitly describes computing the p-torsion local coefficient by Miller's algorithm, strengthening the exceptional-case computational attribution. Cassels's scanned paper supplies the high-block Artin–Schreier antecedent and must be read with its corrigendum. Details and exact pages are in SOURCE_AUDIT_UPDATE.md.

No source read in this follow-up was found to state the complete general-trace weighted-sum evaluator with its adapters and cost. This does not prove novelty. It also does not support treating the new derivation as a demonstrated earlier publication. Gunji (1976), Blake–Seroussi–Smart Chapter V, and Rück's full body remain unread in this follow-up because the available routes did not provide access. The remaining primary-source audit is therefore not complete. The paper's novelty claim should not be substantially narrowed on the basis of those unread sources.

A defensible provisional statement is: the exceptional specialization has explicit classical computational antecedents; the general-trace evaluator is derived here from classical Cartier and Miller constructions; its publication priority remains unresolved. The new proof may simplify the project, but it does not by itself settle historical novelty.

## Delivered changes

`cm_character_route.py` is a standalone corrected evaluator. `patches/code/source_audit/voloch_zeta_route.py` is a compatible replacement for the post-freeze evaluator in Opus's package, with a unified diff alongside it. The frozen benchmark files and their measurements are not rewritten. `PROOFS.md`, `PROOFS.tex`, and `PROOFS.pdf` supply the argument in readable and editable forms; `MANUSCRIPT_ADDENDUM.tex` supplies an insertion fragment. `results/` and the numerical/symbolic verifiers preserve the new evidence. All paper references are listed in SOURCE_AUDIT_UPDATE.md.

The mathematical repair is complete for the stated nonbranch domain, subject to ordinary specialist review of the written proof. The historical priority audit remains open at the named access gaps.
