# Research instruction: literature audit and matched-output evaluation

Investigate prior work and computational performance for Cartier–Miller evaluation of field-valued rationally weighted quadratic-character sums and equivalent elliptic-point sums. Proceed beyond planning into primary-source reading, mathematical comparison, implementation and reproducible measurements. Produce files, not only a conversational summary. Do not publish, modify an external repository, contact authors, or overwrite the supplied manuscript.

Start by reading START_HERE.md and all five technical briefing documents in this package. Verify the handover hashes, run verify_handover.py and its optional integration test, and inspect the supplied code before relying on it. Extract the inherited Opus archive into a separate working directory. Identify the exact manuscript revision, candidate and vendor hashes. No previous chat context is required.

Treat the mathematics phase as supported but conditional on the inherited main theorem. Resolve every finding in CORRECTIONS_AND_GATES.md explicitly. Supply corrected proposed application text in a separate file and a change log. Preserve the original candidate and its freeze. Make any implementation fixes or optimizations in named, separately hashed variants. Do not silently repair code and attribute its new behaviour to the frozen version.

## Primary-source comparison

Read the original papers, not only abstracts, search snippets, secondary summaries or the project’s existing reference section. Begin with PRIMARY_SOURCES.md and follow substantive antecedents. Include both historical constructions and later algorithms that could already evaluate the same normalized scalar. Search by mathematical mechanism as well as by “character sum”; the relevant prior output may be described as a logarithmic transfer, descent map, Cartier coefficient, quasi-period or third-kind differential.

Compare the exact input and output, field of definition, trace and ordinarity assumptions, divisor representative, differential scale, normalization constants, exceptional cases, preparation, query work and storage. In particular, determine when the high-part function in Voloch’s descent construction, evaluated by Semaev’s differentiated Miller machinery, already yields this weighted sum. Give an explicit conversion or identify the precise unresolved normalization step. A different original application does not make an algorithm mathematically different.

Create a source ledger recording author, publication, DOI or primary URL, version, pages, proposition numbers, what was actually read and the exact claim supported. Distinguish original results from later expositions and note corrections or errata. Record unavailable papers and resulting limits. An unsuccessful keyword search is not evidence of novelty. Derive any claimed adapter in the report rather than implying the source already states it.

Produce a comparison matrix classifying each relation as an exact prior algorithm, a provable consequence with an adapter, a special-case overlap, an adjacent result or unresolved. State separately what is established for general admissible cubics/quartics and what is established only for trace-one curves, twists, CM families or supplied traces. Do not claim a new best-known bound until the closest constructions have been compared at the correct scalar normalization.

## Matched computational work

Follow BENCHMARK_PROTOCOL.md. Every headline comparison must return the same specified residue modulo p for the same input and excluded set. A point counter, Hasse–Witt entry or prefix value alone is not a matched output without the required adapter and its charged cost. Character weights outside the character differ from characters of rational functions; integer incomplete sums over intervals are a separate problem.

Implement or adapt the comparator in COMPARATOR_MATHEMATICS.md. The supplied scalar recurrence is a correctness reference, not a completed BGS implementation. A balanced product tree with a linear number of recurrence steps is not automatically a square-root algorithm. Demonstrate the actual block-product construction, handle every denominator and document which native library or published kernel is used. If a reliable BGS adapter cannot be completed, say so and retain it as an explicit gap; do not substitute a weaker method while retaining the BGS label.

Compare the unchanged Python candidate, efficient direct enumeration, the linear coefficient recurrence, FLINT polynomial-power preparation with appropriate evaluation reuse, and a genuine BGS adapter where available. Treat native and Python implementations honestly as named implementations rather than isolating pure algorithmic effects. If a prior logarithmic-transfer evaluator has the same core recurrence, its role may be equivalence verification rather than an independent speed competitor.

Cover cold first-query cost, prepared changing-pole queries, multiple-pole sums, fixed-domain coefficient-only queries and a dense-query workload at feasible primes. Give all reusable-data methods their legitimate preparation and reuse. For dense queries include fast multipoint evaluation where feasible; repeated scalar Horner evaluation alone is not a sufficient comparison against a reusable full polynomial. Keep branch and higher-order weights in a secondary experiment with their extra data acquisition charged.

For cold general curves, charge an exact trace provider to Cartier–Miller. The current candidate’s default direct count is not a practical Schoof/SEA implementation. If supplying PARI ellap or a Jacobian adapter, implement and verify it, charge its actual work and preserve its arithmetic conventions. A comparator that does not require a trace must not be charged for point counting. Distinguish genuinely known-trace families from traces supplied for free as a workload assumption.

Freeze code and validation rules before selecting confirmation cases. Use deterministic recorded selection rules, with development and confirmation primes/curves separated as appropriate. Use fresh instances where preparation is charged. Do not cache complete answers across timing repetitions. Keep correctness comparisons outside timed regions but validate every timed output. Record failure, refusal, timeout and budget outcomes without deleting inconvenient cases.

Measure only workloads the machine can actually support, with predetermined time and memory limits. Use pilot timings to size blocks rather than forcing huge enumerations. Retain raw per-block samples, implementation versions, build flags, hardware, arithmetic sizes and scheduling caveats. Compare complete workload totals and their components. Do not infer asymptotic exponents from a few tiny timings or use independent queries as independent machine replications.

## Required outcome

Return a self-contained primary-source audit, corrected proposed application section, precise adapted algorithms and complexity proofs, benchmark source and dependency/build instructions, machine-readable validation and timing results, plots with raw-data provenance, and a concise recommendation for the current paper. Provide an archive containing everything needed to rerun the reported experiments, plus an executive report as a separately accessible file.

The recommendation must say what is inherited, what is newly derived here, what has only finite computational support, what has been measured, and what remains unresolved. Report negative or limited performance results plainly. If the literature already supplies the same evaluation in some or all cases, preserve that finding and narrow the paper’s claim accordingly.

If attachments or execution become unavailable, complete the independently accessible reading and mathematics, record the blocker, and make no claims of file inspection, execution, benchmarking or saved deliverables that did not occur. Never invent timing data or present theoretical operation counts as measured speedups.
