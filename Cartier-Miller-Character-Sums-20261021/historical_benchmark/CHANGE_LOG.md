# Change log: inherited draft → corrected proposed application section

Base text: `PROPOSED_APPLICATION_SECTION.tex` inside the inherited archive (unchanged; part of the archive manifest). New text: `manuscript/PROPOSED_APPLICATION_SECTION_CORRECTED.tex`. Tags are renumbered (A1)–(A11); the old Theorem A2, Corollary A3, Proposition A4 and Proposition A5 become A3, A4, A5 and A8.

| ID | Location | Change | Reason |
|---|---|---|---|
| C1 | Opening paragraph | Integer incomplete interval sums added to the list of different problems. | Protocol: matched outputs only. |
| C2 | New display (A2) | H(μ) = [z^N] G_μ(z)^h, N = Dh − p < p, with proof. | It defines the trace-free comparators and explains branch values. |
| C3 | Theorem A3 (old A2) | U = {μ₁, …, μ_s} stated explicitly; zero coefficients allowed; counterexample included; proof wording now says "all other points of U". | Gate G1. |
| C4 | Corollary A4 (old A3) | "No projective sum is defined" replaced by the N∞ > 0 / N∞ = 0 distinction; the strict implementation interface is stated as a choice; example p = 7, f = 1 + 3w⁴. | Gate G2. |
| C5 | Proposition A5 (old A4) | The O(s) full scan is separated from degeneracy (U ∪ roots(f) = F_p). | Gate G5c. |
| C6 | New subsection "Relation to the Voloch–Semaev constructions" | (A6): the cubic trace-one conversion C_f(a) = f′(a)/(2b²) − α_p(P)/b. (A7): all exceptional cases (cubic or quartic, τ = ±1) as χ(f′(a)/(2f(a)) − α_p(R)/2), with no square root. Page-level attribution to Voloch (1990, Prop. 1.3), Voloch (1997, pp. 2, 4), Voloch (n.d., pp. 3–4) and Semaev (1998, Lemmas 1–3). Explicit statement that the anomalous (descent/Semaev) constructions do not reach the regular case τ ≠ χ; see C15 for the general-trace route. | Primary-source audit (REPORT §4). |
| C7 | Prop. A8 (old A5) and its remarks | "One additional scalar per curve is needed" → "is sufficient data"; "no polylogarithmic acquisition is known" → removed in favour of the Õ(√p) selected-coefficient route; the rounded-third reduction is called an equivalence and not a lower bound. | Gate G4. |
| C8 | New paragraph "Generic coefficient recurrences" | (A10) recurrence, companion matrix, denominators k!g₀^k, O(p) and Õ(√p) (BGS/Harvey) trace-free costs; it states that the adapter is derived here and is not in BGS. | Comparator mathematics; attribution. |
| C9 | Cost paragraph | Cached versus temporary storage; PARI's actual trace algorithm (CM formula, or BSGS Õ(p^{1/4}) below about 30 digits) versus Schoof's deterministic bound; chain-endpoint test called necessary and not sufficient; p < 2⁶⁴ implementation domain. | Gates G5d, G5e, G5f; PARI 2.17.2 documentation. |
| C10 | Scope paragraph | Exact resonance conditions for nonbranch poles, branch poles and polynomial parts; remark on the branch-resonance character weight; implemented-coverage statement. | Gate G3. |
| C11 | Scope paragraph | Regularity on included fibres for the yB cancellation. | Gate G5a. |
| C12 | (A11) | The single-point-exclusion identity is labelled affine. | Gate G5b. |
| C13 | Removed | "No polylogarithmic acquisition … is known" (universal phrasing). | Gate G4. |
| C15 | New Proposition A7′ and display (A7″) | General-trace evaluation by division by p: bV(a) = (A − 1)α_p([p^{−1}]P), with a short Cartier-operator proof and its consistency with Voloch's zeta function (V97 p. 2, Prop. 2). The manuscript's evaluation capability (Theorem 1, Corollary 1.1, Corollary 4) is then obtainable after an exact trace from classical facts by a different chain; the priority statement is narrowed accordingly. | Primary-source audit; REPORT §4.4. |
| C14 | Throughout | "We have not located … ; that observation does not establish novelty" replaces any implicit novelty claim. | Prompt requirement. |

Code-level changes are confined to `code/cmbench/cmcs_v2.py` (V2-1, V2-2, V2-3) and are described in its module docstring. The frozen inherited `cmcs.py` is imported unchanged.
