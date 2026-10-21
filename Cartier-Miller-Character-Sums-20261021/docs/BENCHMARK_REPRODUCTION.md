# Historical matched-output benchmark reproduction

This directory preserves an executed campaign, rather than a newly benchmarked version of the uniform-order evaluator. The main cold-query comparison returned exactly the same finite-field residue C_f(a) for the same input class. Multiple-pole comparisons matched both weights and complete excluded domains. Source reports explain sparse, dense and coefficient-only workloads separately.

The recorded host was an uncontrolled two-vCPU Intel Xeon Linux VM. The recorded environment used CPython 3.13.16, GCC 13.3.0, python-flint 0.9.0/FLINT 3.6.0, cypari2 2.2.4/PARI 2.17.2 without SEA data, and the Harvey kernel through passagemath-ntl 10.8.13. These versions describe the historical environment, not a claim that current packaging tools have identical versions. The current portable query and tests do not depend on them.

The current paper's Table 8 is reproducible directly from the archived validated CSV without executing any benchmark:

```bash
python3 tools/recompute_benchmark_table.py
```

It checks the CSV SHA-256, recomputes the ten cubic/quartic classes and compares 30 recorded method medians. It charges the actual per-block repetition counts. No extrapolated or skipped timing is turned into a measurement. The main report contains the complete observed classes and explicit timeout, budget and size-ceiling labels.

## Historical code and dependencies

The original benchmark scripts and README are retained unchanged under historical_benchmark/. That README's input-extraction instructions describe the original archive layout. The inherited files are also already extracted here, so the two path variables can be set from this supplement's root:

```bash
export CM_INHERITED_SRC="$(pwd)/historical_benchmark/inherited/character_sums/src"
export CM_HANDOVER_COMPARATORS="$(pwd)/historical_benchmark/inherited/handover/comparators"
cd historical_benchmark/code
python3 verify_freeze.py
```

For an optional fresh measurement, build a suitable environment with python-flint, cypari2, NumPy and Matplotlib. The Harvey adapter additionally requires the recorded Sage/passagemath components or an appropriately adapted current Sage installation; set CMBENCH_SAGE_PYTHON to that interpreter. The historical README records exact packages and commands. On another platform rebuild the native C library from cmbench/native/cmnative.c with the appropriate toolchain and record its new hash. Do not rewrite the historical freeze to make a different binary appear identical.

Only after that optional environment is ready, a bounded smoke benchmark can be invoked from historical_benchmark/code:

```bash
python3 bench.py --quick --out /tmp/cm-character-benchmark-smoke
```

The full command and separate Harvey reference-validation workflow are documented in the preserved README. Keep new outputs in a new directory. Verify the trace provider and dependency behavior actually used on the new platform, rather than copying the old performance interpretation. The historical code contains old comments about PARI's general possibilities; the executed campaign used CM or baby-step/giant-step paths, not a measured Schoof/SEA provider.

## Evidence qualifications

The uniform-order engine and the new weighted adapter were not the implementations timed in the archived campaign. The separate post-freeze alternative-route timing is exploratory. No timing from either campaign has been reassigned to a newly adapted repository implementation.

The archive documents the host restart, rerun of only missing jobs, deterministic reconstruction of case metadata and limited source-freeze scope. Thirteen polynomial/multipoint jobs exceeded the nominal 512 MiB working-memory target. The target was not enforced at runtime, and those jobs do not show performance within it. No square-root comparator was measured above its declared 40-bit ceiling. These limitations and the workload-dependent crossovers belong with published numerical summaries.

Raw per-job outputs and case pools are included to allow a later full audit. They can be placed in a supplementary-data release or another repository-appropriate location if the main source tree should remain compact. Retaining their hashes and provenance is more important than mirroring this handover's folder layout.
