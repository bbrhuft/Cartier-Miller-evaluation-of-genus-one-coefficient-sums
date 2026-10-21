# Cartier–Miller: final requested primary-source check

21 October 2026

The four supplied sources close the specific access gaps previously identified. They strengthen the attribution to classical mathematics, particularly Rück's explicit local-coefficient cocycle. They do not, on this targeted examination, establish that the complete general-trace weighted-sum formula has already appeared. Publication priority remains unresolved; absence from these sources is not a priority proof.

Gunji's entire article, Rück's entire article, and Semaev's entire article were examined. The book comparison covers Chapter V's pairing and anomalous-curve sections, particularly printed pp. 88–91, supplemented by text searches. It is not a review of the entire book. Exact pages, equations, differential conventions, and references are in SOURCE_LEDGER_FINAL.md.

## What changes mathematically

The source comparison led to a simpler proof and evaluator. On a short Weierstrass model over F_p, use omega=dx/(2y), t=-x/y, and write

\[
W(x)^{(p-1)/2}=U(x)+A x^{p-1}+x^pV(x).
\]

If N is the exact rational curve order and alpha_N(P) is the Laurent constant of the logarithmic derivative of the Miller function with divisor N(P)-N(O), then

\[
\boxed{\alpha_N(P)=bV(a),\qquad P=(a,b)\in E(\mathbb F_p).}
\]

The proof uses the Cartier identity, the Frobenius trace relation, and a Miller composition identity. It holds for every trace, including supersingular and anomalous curves. A rational point of order two has both sides zero. No geometric division point is constructed by the algorithm.

For an admissible nonbranch pole a of a squarefree cubic or quartic f, put e=chi(f(a)), g(z)=f(a+z)/f(a), g_1=f'(a)/f(a), and N=p+1-e*tau_f. Let R be the image of (0,-1) on the short model whose origin is (0,1). The character-sum query is

\[
\boxed{C_f(a)=e\left(-\frac{g_1}{4}(N-2)-\frac{\alpha_N(R)}2\right).}
\]

This replaces the previous evaluator's trace case split with one Miller chain at the curve order. It also explains the trace-dependent annihilator already used by Cartier–Miller. The new implementation covers p=5 without the previous bounded enumeration fallback. Opus's original report assumed p>=7; the p=5 extension is not a counterexample to that report. Full normalization, the factor of two for the divisor (P)-(-P), and the proof appear in UNIFORM_ORDER_PROOF.md.

After separately charged exact-trace acquisition, the query uses O(log p) field operations. With classical arithmetic the stated bit bound is O((log p)^3); with fast arithmetic it is soft-O((log p)^2). These are conditional query bounds, not end-to-end point-counting bounds. No new timing benchmark or cryptanalytic improvement is claimed.

## Computational evidence

The final standard-library verifier passed 14,037 development character-sum comparisons and 5,400 confirmation comparisons, totaling 19,437. Each compares the uniform evaluator with direct finite-field enumeration and the previous corrected evaluator. Development additionally checked the cubic scalar identity at 47,712 nonbranch rational points. There were no failed comparisons.

Development exhaustively includes squarefree degree-three and degree-four polynomials over F_5 with nonzero leading coefficient and every nonbranch pole. Other tests include rational two-torsion model images, intermediate Miller endpoints at the identity, trace-one twists, and supersingular curves. These counters overlap and should not be added as independent samples. Confirmation uses nine primes disjoint from this verifier's development prime set, with 360 cubic/quartic models and up to 15 poles per model. The three executable source files were hashed before confirmation; the digest is recorded in FREEZE.json. The archived outputs are in results/. The numerical tests support the proof; they do not establish publication priority.

## Recommended manuscript treatment

The local-coefficient cocycle and differentiated Miller construction should be explicitly attributed to Rück and Semaev, with Gunji credited for earlier Cartier and logarithmic-differential structure. The book supplies context for the classical anomalous attack. Avoid presenting those devices, or logarithmic-time p-torsion transfer itself, as new.

The defensible mathematical focus is the proved connection to the selected high coefficient and rationally weighted character sum, together with the normalization, trace accounting, model changes, and exclusions. The uniform curve-order identity gives a cleaner presentation of that connection. It is a derivation in this project whose publication priority has not been established.

A suitable integration order is: classical construction and attribution; uniform scalar lemma with proof; cubic/quartic adapter; multiple-pole exclusions and point-sum interpretation; field-operation and bit costs; then matched-output computational comparisons. Branch poles and higher-order poles remain outside the accelerated nonbranch simple-pole evaluator unless their additional coefficient oracles are separately proved. Do not widen the claim to arbitrary rational weights merely because a direct finite-sum identity exists.

The four requested texts no longer block a qualified revision. The full manuscript has not been edited in this task. This package supplies the proof, source ledger, and reproducible evidence for that revision.
