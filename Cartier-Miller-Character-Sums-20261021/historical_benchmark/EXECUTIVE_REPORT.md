# Executive report: Cartier–Miller weighted character sums against prior work and matched benchmarks

Prepared 21 October 2026 for David Jordan. Unrefereed and AI-assisted. Nothing was published; the manuscript and the inherited archive are unchanged. Full details and proofs are in REPORT.md; sources in SOURCE_LEDGER.md.

## Bottom line

1. **The exceptional case is prior work plus short adapters.** When the trace equals the character at the pole (τ = χ(f(a)) = ±1), the weighted sum C_f(a) = Σ_{x≠a} χ(f(x))/(x − a) follows directly from established results. Voloch's descent polynomial V is exactly the high part of f^{(p−1)/2} (Voloch 1990, Prop. 1.3; 1997, p. 2; n.d., p. 3). Semaev's differentiated Miller recurrence evaluates bV(a) in O(log p) (Semaev 1998, Lemmas 1–3). Combining them gives C_f(a) = f′(a)/(2b²) − α_p(P)/b for trace-one cubics. With a twist, a translation and one Riemann–Roch decomposition, this extends to all exceptional cubics and quartics, with no square root (formulas (A6), (A7)). The only normalization the sources leave open is the **sign**: Voloch (n.d., p. 4) says "up to sign", and Voloch (1997, p. 4) corrects the 1990 scale (dx/y → dx/(2y)). The sign is +1. It is fixed by the manuscript's (24)–(25) and Lemma 3, and confirmed here on every rational point of every anomalous model for p ≤ 59 (19,150 points; all other scalings failed).

2. **The general-trace case also has a short derivation.** For p ∤ #E(F_p), bV(a) = (A − 1)·α_p([p^{−1}]P), where A is the Hasse invariant (A7′). A five-line Cartier-operator proof is given, and the identity is also what Voloch's characteristic-p zeta function gives (1997, p. 2 and Prop. 2). It held on all 742,648 tested points. A complete evaluator built on it passed 11,866 direct checks and 160 checks at 30–62 bits against the frozen candidate. **Consequence:** after an exact trace, the O(log p) evaluation capability of Theorem 1 and Corollary 1.1 can be obtained from classical facts by a different, equally short chain. Theorem 1 remains a distinct formulation (two-pole residue divisor, annihilator M_χ, quadratic algebra), whose priority is unresolved: it was not located in the sources read.

3. **A genuine BGS comparator now exists, and it loses badly at scale.** C_f(a) is one selected coefficient of a high power of a fixed-degree polynomial (A2). The selected-coefficient adapter is derived here; Bostan–Gaudry–Schost do not state it. It runs through Harvey's published NTL interval-product kernel and through this package's transparent BGS (2007) implementation. Both were validated, and both need no trace. Measured cold first queries:

| bits | Cartier–Miller (Python, PARI trace included) | BGS (Harvey kernel) | best native linear method |
|---|---|---|---|
| 10 | 0.14 / 0.17 ms | 0.56 / 0.61 ms | 0.03–0.04 ms (**wins**) |
| 20 | 0.25 / 0.24 ms | 6.3 / 15 ms | 25 / 39 ms |
| 30 | 0.37 / 0.36 ms | 0.17 / 0.47 s | not run (predicted over budget) |
| 40 | 1.2 / 1.0 ms | 6.9 / 16 s | — |
| 62 | 132 / 134 ms (92% / 87% trace) | not run (ceiling) | — |

(cubic / quartic medians; one uncontrolled 2-vCPU host; named implementations, not algorithmic constants.)

4. **Reuse changes the picture only at small p or for dense queries.**
   * **Prepared 16-bit curve.** The full polynomial (2–8 ms) with Horner queries (13–76 µs each) beats Cartier–Miller queries (0.09–0.31 ms each) beyond 8–64 poles (cubic) or 64–512 poles (quartic).
   * **20–23 bits.** Cartier–Miller wins for every query count tested (up to 512).
   * **Dense queries** (p/16 to all poles of a 12–18-bit curve). The all-poles correlation, or the polynomial with multipoint evaluation, is 9–147× faster than Python Cartier–Miller.
   * **One weighted sum with up to 256 poles.** Cartier–Miller is fastest at every size; at 20 bits the polynomial route is 1.6–6.7× slower per sum, plus 55–135 ms of preparation.
   * **Coefficient-only changes** cost the same ~1 µs dot product for every method.

5. **Branch poles favour the trace-free route.** The inherited candidate's O(p) Python second-kind preparation takes about 1 s at 20 bits; BGS gives each branch value in 5–12 ms.

## Corrections

All review gates are resolved in `manuscript/PROPOSED_APPLICATION_SECTION_CORRECTED.tex` (compiles, 5 pp.), with a gate-by-gate record in CORRECTIONS_RESOLUTION.md and the itemized text changes C1–C15 in CHANGE_LOG.md. The corrections cover:

* the complete common domain (U = {μ₁, …, μ_s}, zero coefficients allowed; counterexample reproduced);
* the projective N∞ = 0 case;
* exact resonance conditions, with a new remark that the branch resonance k = (p + 1)/2 turns the term into a character sum on y² = (x − μ)f(x);
* sufficiency rather than necessity phrasing;
* the regularity and affine qualifiers;
* the storage distinction;
* the endpoint check taken from the chain itself;
* PARI's actual trace algorithm.

Implementation fixes are in the separately named variant `cmcs_v2`, which is validated. The frozen candidate is untouched.

## Recommendation for the paper

* Attribute the exceptional case to Voloch–Semaev with the explicit conversions (A6)/(A7), and cite pages.
* State that a general-trace O(log p)-after-trace evaluation follows from classical Cartier facts (e.g. (A7′)), and present Theorem 1 as one formulation. Withdraw any implication that the O(log p) query is itself new.
* Keep "not located; does not establish novelty" for the two-pole residue-divisor statement.
* Add the trace-free Õ(√p) selected-coefficient route as the natural comparator, with the measured crossovers.
* Adopt the corrected application section.

## Evidence and status

* **Validation:** development 140,636 + 7,630 checks; hash-seeded confirmation on primes disjoint from development and inherited lists 51,023 + 1,844 checks. All passed. Every timed output was checked outside the timers, with zero mismatches: 908,368 direct, 9,043,732 cross-family consensus, 9,621 internal checks and 33,894 traces; 108 one-family W4 outputs at 62 bits passed a separate internal check.
* **Run integrity:** a host restart interrupted the benchmark in its last workload (W5). The missing jobs were rerun with the unchanged harness and seeds, and the case pools were regenerated deterministically. Both are documented (REPORT §9.1, §12).
* **Inherited and not re-proved:** Theorem 1, Lemma 3.
* **New, needing specialist review:** (A2), (A6), (A7), (A7′), the 1/z decomposition.
* **Finite support:** the +1 constant, and the route evaluators.
* **Unresolved:** priority of the general-trace statement (several antecedents were not obtainable here; see the ledger).
* **Measured but not covered:** no SEA or Schoof trace provider, no native Cartier–Miller implementation, no many-primes workload, and BGS beyond 40 bits. The general-trace route (A7″) was timed only after the freeze, in an exploratory run: 1.1–2.1× faster per query than the frozen candidate in Python, with identical outputs (REPORT §9.10).
