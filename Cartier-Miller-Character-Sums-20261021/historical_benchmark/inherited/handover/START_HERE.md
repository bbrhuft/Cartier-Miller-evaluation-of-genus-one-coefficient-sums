# Cartier–Miller: primary sources and matched-output benchmarks

Prepared for David Jordan, 20 October 2026. This is a handover package, not a completed literature audit or a performance result.

Read PROMPT.md, CORRECTIONS_AND_GATES.md, BENCHMARK_PROTOCOL.md, COMPARATOR_MATHEMATICS.md and PRIMARY_SOURCES.md. Read the inherited independent review, then extract inherited/Opus_Character_Sums_20261020.zip into a disposable working directory and read its REPORT.md, README.md and code. The unmodified source manuscript is included separately. Its SHA-256 matches the source identified in Opus’s provenance exactly; the internal revision is 19 October despite the older original filename.

The mathematics phase supports a nonbranch simple-pole framework and several bounded extensions. It is not an independent specialist verification of the inherited main theorem. Correct the statement issues before freezing any benchmark candidate. Keep the inherited archive immutable.

| File | Purpose |
|---|---|
| PROMPT.md | Complete instruction for the receiving research chat |
| CORRECTIONS_AND_GATES.md | Review findings to resolve before manuscript or benchmark claims |
| BENCHMARK_PROTOCOL.md | Exact outputs, workloads, charging rules and measurement requirements |
| COMPARATOR_MATHEMATICS.md | Matched scalar and an explicit recurrence for a BGS adapter |
| PRIMARY_SOURCES.md | Primary-source starting register and questions to check |
| comparators/reference_comparators.py | Pure-Python linear coefficient comparator, direct enumeration and polynomial-power references |
| verify_handover.py | Integrity check, reference comparisons, optional integration with the inherited evaluator |
| results/INITIAL_VALIDATION.json | Actual bounded handover validation; not benchmark timings |
| inherited/Independent_Review_20261020.md | Prior review, reproduced tests, explicit counterexamples and limitations |
| inherited/Cartier_Miller_Source_Revision_20261019.tex | Exact manuscript source used by Opus |
| inherited/Opus_Character_Sums_20261020.zip | Original mathematical report, implementation, vendor code and evidence |
| INPUT_PROVENANCE.json | Input identity and content hashes |
| SHA256SUMS.txt | Integrity manifest for this handover |

From this directory, run `python verify_handover.py`. This needs only the standard library. To also test the actual inherited application layer, run `python verify_handover.py --with-opus`. The optional integration test extracts the archive into a temporary directory, supplies traces by direct small-prime counting and calls the real candidate. It does not require PARI or FLINT and does not replace the original full-suite tests.

The linear reverse-coefficient implementation is supplied to make a fair comparison concrete. It is O(p), not a BGS algorithm, and is not optimized native code. Its validation is correctness evidence only. The new research should implement or adapt a genuine BGS block-product method, or explicitly report that comparator as unavailable.

Create a separate output package with a primary-source audit, corrected application text, reproducible benchmark implementations, exact confirmation results, raw timing samples, machine information and commands. Do not modify the original manuscript or publish anything.
