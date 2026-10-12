# Response to the independent adversarial review (12 October 2026)

The review ("Review of the CM-to-Cartier extension, 12 October 2026") gave a qualified positive assessment and recommended the corrections below before human review. Every item was applied. No mathematical result changed. The reviewed note and ledger are preserved unchanged in `history/`.

| Review item | Verification here | Change made |
|---|---|---|
| Corollary 2.1: non-scalar is insufficient (p = 11, α = 1 + 11(1+√−7)/2, degree 254, quotient 0/0) | Checked by hand: N(α) = (169+847)/4 = 254 ≡ 1 (mod 11); ι(α) ≡ ι(ᾱ) ≡ 1, so u² ≡ ℓ. Theorem 1 then forces σ_G ≡ 0. | Hypothesis λ ≠ μ (u² ≠ ℓ in F_p) added. Counterexample recorded in the note. |
| §3.1: residue-free ≠ second kind (y² = x³+9x+1 over F₁₁, θ = x¹¹η, 𝒞θ = 7η) | β = 7 for this curve (`results/char_p_exactness_demo.json`); 𝒞(x^pη) = x·𝒞η = βη has a double pole. | "Second kind" defined explicitly as locally exact modulo regular forms. Example added. The one-dimensionality claim is restricted to D₂/dK. |
| Validation exit status | Reproduced: the injected R₋₇ = 1/3 gave 2,372 failures, and before the fix the exit status was 0. | Both validation suites and every theory script now exit nonzero on failure. `run_all.py` propagates failure. Re-tested by injection: wrong slope sign gives exit 1; R₋₇ = 1/3 gives 2,372 failures and exit 1; `run_all.py` exits 1. |
| Period checks used double precision | Confirmed: differences were converted through Python `complex`, and PARI periods ran at default precision (errors about 10⁻²⁰). | Periods now computed at 320-bit precision with native differences: maximum 7.7·10⁻⁷³ and 1.3·10⁻⁷⁶. Described as floating-point corroboration, not interval-certified. |
| Large-prime CSV lacked the full model | Confirmed (it recorded r mod 7 and χ(r)). | The CSV now records p, bits, r, A, B, χ(r) and all three traces. |
| `fixed_D_evaluator.py`: `p % abs(D)` should be `D % p`; no prime check | Confirmed typo. As the review found, it produced no wrong output for the eight tables at p ≥ 7. | Fixed to `D % p == 0`. The function now validates p (deterministic for p < 2⁶⁴). |
| Include the algebraic class-polynomial/order argument | Implemented `theory/order_argument.py`: (λ−μ)² = D computed exactly per loop; H_D irreducible of degree h(D); overorders have class numbers 1, 1, (1,1), (1,1), (2,1,1), (2,1,1), and at depth one j ≠ 0, 1728. | Added to §7. PARI polclass and the analytic form matching are now comparators only. |
| Signed trace: route (b) does not derive the Legendre-mod-7 rule | Agreed. | Route (b) is relabelled as an independent sign-selection algorithm proved correct. The closed rule rests on route (a). |
| Ordinarity uses classical reduction theory; alternative via no common zero | Read Katz (2019) Thm 3.1 via extraction. Checked exactly: H ≡ E_{p−1}, β ≡ E_{p+1}/12 and no common zero on all 7,948 models at 7 ≤ p ≤ 43 (`theory/katz_zannier_check.py`). | Theorem 5 and Theorem 7 now give both routes. The "elementary" wording is qualified so the note does not claim a proof of CM reduction theory. |
| Six-family recovery shares the Vélu identity and path data | Agreed. | Reworded as an alternative derivation, not six independent discoveries. |
| Literature: Katz 1976 §5.7, 8.0.9, 8.0.13 present; Katz (2019) is direct prior context; −7 value published | Katz 2019 read via extraction. Sutherland γ table read (γ = 181/637875, which converts to 5/21). LMFDB 49.a4 read. Katz 1976 §VIII still beyond my tool's extraction. Horawa Ex. 7.18 not reachable. | Katz (2019) added as the closest prior art. The note now states that the comparison is not new; the contribution is the application, certificates and evaluators. Items I could not open are marked as reported by the review. |
| BOS warning: a convention issue, not a claim the theory is false | Agreed. | Reworded in §0 and §6. |

The re-run with corrections (`results/run_all_log.json`) completed with exit status 0. All 13 steps passed, the validation counts are unchanged (deterministic seeds), and there were zero failures.

The reviewer's own independent checks are listed in the note §10 with attribution: 989,668 models, 21,040 dense matches, 429 branch queries, direct trace counts to p = 30,000, and others. They were not rerun here.

Recommendation, agreeing with the review: submit the bounded result — the D = −7 evaluator, the fixed-table comparison and the six-family derivation — for human specialist review. The specialist question is novelty of the application and certificates. The comparison itself is classical (Katz 1976, 2019).
