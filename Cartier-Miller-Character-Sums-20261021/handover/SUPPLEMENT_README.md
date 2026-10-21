# Cartier–Miller character and elliptic-point sums

This supplement accompanies the rationally weighted quadratic-character-sum and elliptic-point-sum application of Cartier–Miller. It contains the current uniform curve-order evaluator, a small tested adapter for complete excluded domains, the mathematical proofs, primary-source comparisons, manuscript references, and the historical matched-output benchmark campaign with its raw data. The folder layout is for handover; the repository maintainer may choose the final locations.

For a supplied prime p at least 5, squarefree cubic or quartic f, nonbranch pole a, and exact signed projective trace, the single-pole output is the residue

\[
C_f(a)=\sum_{x\in\mathbb F_p,\ x\ne a}\frac{\chi(f(x))}{x-a}\in\mathbb F_p.
\]

For a supplied weight R(x)=c+sum_i r_i/(x-a_i), the prepared adapter returns the character sum, the corresponding affine-point sum, and the projective-point sum retaining all rational points at infinity. Every a_i is excluded even if r_i is zero. The point and character outputs differ by the proved elementary baseline. These are residues modulo p, not unreduced integer character sums, interval sums or discrete logarithms.

## Run the portable supplement

Python 3.8 or later and the standard library are sufficient for the current evaluator and its tests. No point-counting backend is bundled into the current query API: the exact signed trace and primality are supplied obligations. Polynomial coefficients are listed in increasing degree.

```bash
python3 examples/weighted_sum_example.py
python3 tools/verify_supplement.py
python3 tools/verify_supplement.py --full
```

The verifier checks every file against MANIFEST.json, reruns the frozen uniform confirmation and the new weighted-adapter confirmation, checks both historical implementation freezes, and recomputes the displayed benchmark medians. The full option also reruns the development selections. Calculations that create results use temporary paths; recorded evidence is not overwritten. No historical timing campaign runs automatically.

```python
import sys
sys.path.insert(0, "src")
from weighted_sums import single_pole, prepare_weights

assert single_pole(5, [0, 3, 0, 1], 1, -4) == 1
state = prepare_weights(7, [1, 1, 0, 1], 3, excluded=[1, 2])
answer = state.evaluate([1, 0])
assert (answer.character, answer.affine_points, answer.projective_points) == (6, 5, 5)
```

This flat source layout keeps the frozen evaluator bytes unchanged. Opus may adapt imports to the repository's package namespace, retaining the original frozen copies and recording any adapted source hashes.

## Contents

| Path | Purpose |
|---|---|
| OPUS_HANDOVER_PROMPT.md | Instructions for integrating this work into the existing repository |
| src/uniform_order.py | Current nonbranch evaluator, one Miller chain at the normalized twist's curve order |
| src/cm_character_route.py | Shared arithmetic and the preceding evaluator, retained unchanged for verification |
| src/weighted_sums.py | Newly packaged constant-plus-simple-pole and elliptic-point adapter |
| proofs/UNIFORM_ORDER_PROOF.md | Current all-trace proof, sign, model change, and query bounds |
| proofs/FOUNDATION_PROOFS.md | Detailed Cartier and model-change proofs; its older evaluation strategy is superseded |
| proofs/SOURCE_LEDGER_FINAL.md | Direct examination of Gunji, Rück, Semaev, and the book |
| docs/MATHEMATICS.md and docs/API.md | Precise mathematical and software contracts |
| docs/STATUS_AND_PROVENANCE.md | Current versus historical results, source hashes and manuscript status |
| docs/BENCHMARK_REPRODUCTION.md | Historical dependencies, setup, limitations and reproduction commands |
| verification/ | Frozen results, adapter results, benchmark table source, and release check |
| historical_benchmark/ | Preserved benchmark code, inherited implementation, case pools, raw outputs, validation and timing records |
| history/ | Earlier normalization repair and independent review, with supersession explained |
| manuscript_reference/ | The available 21 October paper snapshot and the later replacement prior-work section |

## Scope and costs

After separately charged exact-trace acquisition, a nonbranch scalar uses O(log p) field operations and O((log p)^3) bit operations with classical arithmetic, or soft-O((log p)^2) with fast arithmetic. The new adapter prepares s exclusions in O(s log p+s^2) field operations and evaluates each later coefficient vector in O(s). Its pairwise batch-inversion implementation uses O(s^2) temporary field storage and O(s) cached storage. The faster polynomial-tree correction is proved but is not implemented or benchmarked here.

An excluded branch value is allowed only with zero residue in the fast adapter. Active branch poles, higher-order poles, arbitrary polynomial parts, nonrational poles and unfactored denominators are outside this API. Historical experiments on some of those cases remain separate. The trace-free selected-coefficient BGS/Harvey route covers branch queries with a different cost model. Passing a Miller endpoint check does not certify a supplied trace.

The historical benchmark measures the older frozen implementation, not uniform_order.py or the new weighted adapter. It is retained to support the paper's matched-output observations. Priority for the combined general-trace scalar identity and weighted-sum adapters remains unresolved; Miller's circuit, the logarithmic transfer, and Rück's coefficient cocycle are classical. This is unrefereed research software and evidence, not specialist proof review.
