# Current task and knowledge status

| Item | Status and limits |
|---|---|
| Cubic branch/root identity and explicit second-kind normalization | Derived in retained proof notes, independently checked in finite fields; review signs, differential normalization and hypotheses |
| Degree-two transport | Retained normalized formula and working path evaluator; reverse dual requires square coordinate scaling, not literal equality of displayed models |
| Ordinary easy seeds | A=0 with p congruent to 1 modulo 3; B=0 with p congruent to 1 modulo 4; beta=0, including permitted twists |
| Depth at most two | Explicit families, direct parameter-checked recognition and proof argument retained; tested exhaustively over all nonsingular short models at primes 7 through 127 |
| Depth three and four | Explicit new examples and finite class audit; no uniform depth-three direct recognition certificate or universal depth bound proved |
| Modulo-73 target | (4,16), H=10, beta=4; input-to-easy path gives multiplier 15; not in retained depth-two closure |
| Automatic bounded path search | Working randomized fixed-degree root splitting with failure status and unpruned BFS; the sharper dual-pruned complexity discussed in theory is not production implementation |
| General k recovery | Open beyond justified families; formal derivative reduction and finite differences do not provide a fast oracle |
| Unreachable ordinary component | Retained p=13 example (A,B)=(1,1); same trace as an easy curve does not imply rational two-isogeny reachability |
| Third-point case p congruent to 1 modulo 3 | Already has a complete evaluator in original handover; do not repeat it |
| Restricted higher genus | Already has fast prefix prototypes; not a uniform every-index result |
| Precision-two Witt/BGS | Already computes complete weighted sums by recurrence products; fast sum-avoiding correction remains unproved |
| Trace backends | Original experimental exact Schoof and point-count BSGS sources are retained; no production SEA backend |

The prior finite audit covered 51 primes from 7 through 251 and 12,288 true base-field isomorphism classes. It found 64 newly reached depth-three classes and 32 at depth four. Saturation by depth four in that range is finite evidence only. Base-field isomorphism uses square scaling; equal j or equal trace does not identify all relevant twists or components. See the audit note for precise definitions and counts.

For f=1+cw+bw²+aw³, define H=[w^(p−1)]f^((p−1)/2) and K=[w^(p−2)]f^((p−1)/2). Use x=aw+b/3 and y=av, giving A=ac−b²/3, B=a²−abc/3+2b³/27, dw/v=dx/y and beta=aK+(b/3)H. These are not the differential scales from a separate rational-origin normalization. For a supplied nonzero root mu, the retained identity is T_f(mu)=a mu(mu H−K)/f'(mu). A verified input-to-easy path yields beta=H sum_i q_i/2^(i+1); it does not divide by H.

The ordinary depth-two families use e²=2 or e²=3 with appropriate prime conditions. Their coefficients, exact integer invariants, exceptional reductions and reverse certificates are in the theory note. Do not assume that one more path step preserves those conditions or gives a unique recoverable parameter. The new question is to derive and verify the next step for one chosen family, including its actual rationality and collision conditions.

For benchmarks, compare identical outputs and moduli, charge mandatory preparation and reconstruction, and distinguish complete runs from cached queries. An original weighted-sum result needs B_L and a_L. No new timing claim is made by this handover. Preserve literature, proof and novelty review as separate obligations. Schoof provides the deterministic theoretical trace setup; a trusted trace fixture is not a trace-certification algorithm.
