# Matched-output protocol

This document specifies experiments to perform. It contains no benchmark measurements.

## Mathematical outputs

The core output is C_f(a)=sum_(x in F_p, x!=a) chi(f(x))/(x-a), returned as an integer residue in [0,p). Let p>=7 be prime and f a squarefree exact-degree cubic or quartic. Character values and inverses belong to F_p. Preserve that output for every comparator.

For multiple poles the input is p,f,U={a_1,...,a_s}, coefficient vector v, and constant b. The primary output is sum_(x notin U) chi(f(x)) (b+sum_j v_j/(x-a_j)). The corresponding affine-point output is a secondary check. Specify whether any additional exclusions are represented by zero coefficients or by a separately supplied set. Validate their equivalence with the elementary baseline.

Cold and prepared nonbranch workloads exclude roots of f but include a=0 where appropriate; translation cost is charged. Branch values form a separately labelled workload with their extra coefficient preparation charged. Positive-degree polynomial weights and higher-order poles are optional secondary extensions after correcting their scope.

## Implementations

| Method | Matched output and required treatment |
|---|---|
| Original cmcs.Curve / RowSession | Preserve unchanged as a named baseline. Use an exact trace adapter for realistic cold measurements, or label the default direct count explicitly. |
| Efficient enumeration | Build character/fibre values and inverses efficiently; charge those tables when newly required. Avoid making per-term modular exponentiation the only baseline. |
| Linear reversed-coefficient recurrence | Supplied as a transparent O(p) correctness comparator; one final inversion in its scaled recurrence. Native optimization is allowed as a separately named implementation. |
| FLINT polynomial power | Compute f^h once; evaluate its high block or truncated low block. Use legitimate cached preparation across queries. Include a native recurrence/power implementation, not just slow Python expansion. |
| BGS/block-product adapter | Compute the specified reversed coefficient using the explicit fixed-order recurrence. A point counter or unrelated recurrence benchmark alone is insufficient. Prove and verify the adapter. |
| Earlier logarithmic-transfer methods | Establish exact domain and normalization first. Reusing the same Miller machinery is an equivalence/attribution check, not independent evidence for a new speed advantage. |

An implementation may use scalar, batch or cached modes, but every mode must have an explicit contract stating the supplied data and newly acquired data. A full polynomial need not be charged repeatedly when the workload permits reuse. A method needing no trace must not pay for one.

## Workloads

| Workload | Input changes | Required charges and output |
|---|---|---|
| W1 cold single query | New p,f,a each instance | Complete time including required trace, normalization, model, coefficient or character preparation; one C_f(a). |
| W2 prepared curve | Fixed p,f; Q varying admissible a | Report preparation, all Q outputs, query-only time and complete preparation-plus-query total for every method. Use Q ranging from small to moderate. |
| W3 fixed excluded set | Fixed p,f,U; changing v,b | Charge vector preparation once; report coefficient-only queries for all applicable methods. Their O(s) dot-product stage alone cannot demonstrate a new geometric advantage. |
| W4 varying pole count | Fixed p,f, increasing s and possibly new U | Return one matched weighted sum. Record scalar-oracle work, correction work, exclusions and total; include input size. |
| W5 dense queries | Q approaches p at feasible primes | Compare polynomial preparation plus fast multipoint evaluation with scalar Miller queries. Include end-to-end total and memory. Unimplemented fast multipoint evaluation must be recorded as a coverage gap. |
| W6 branch boundary, optional | Branch poles or second-kind weights | Include second-kind coefficient acquisition; report any factorial or CM shortcut with all necessary setup. Keep separate from nonbranch prepared logarithmic queries. |

## Case selection

Cover general cubics and quartics, both square classes of quartic leading coefficient, nonunit and zero constant terms, zero and nonzero poles, square and nonsquare fibres, and selected trace +1/-1 cases. Use both ordinary and supersingular examples. Avoid relying solely on j=0/j=1728 or a single unusually easy family.

Known-trace families may be included as a separately labelled workload, with proof and actual formula cost. Supplying a trace for free in W2 is an explicit preparation assumption, not an end-to-end result for W1.

Generate and freeze a deterministic development specification first. After validating and freezing the code, select confirmation inputs with a separate recorded rule and seed. State the sense in which primes or curves are disjoint. The prior archive’s sample is already known and is not a new blind confirmation set.

Prime ladders may span small enumeration-feasible values, medium block-product values, and the supported large-word domain for fast methods. Do not invent matching large-prime reference results where enumeration or polynomial expansion was not feasible. Use independent native comparisons or invariants, labelled accordingly.

## Timing boundaries

Use perf_counter_ns or an equivalent monotonic clock. Warm imports and process startup may be excluded consistently from all algorithm timings; document that choice. Report compilation and cold process costs separately where relevant. Include library/context initialization required by each cold instance and exact trace acquisition when required.

Use pilot measurements to select repetitions targeting approximately 20–100 milliseconds per timing block, with caps on repetitions and workload cost. Aim for at least nine blocks where practical. Randomize or rotate method order. Retain individual block samples and repetitions, not merely their average. Report medians and observed spread; do not present them as machine-independent confidence guarantees.

For W1 recreate the required per-instance state on every timed repetition. For W2 and W3, preparation is legitimately shared within the workload and charged once in its total. Repeated pole arguments must not accidentally turn a computation benchmark into a cached-answer lookup. Vary coefficient vectors where the contract requires new ones.

Correctness validation occurs outside the timer, but every timed returned residue or vector must be checked or compared by an exact retained mechanism. If using a checksum only for output collection, do not substitute it for the initial exact per-output validation. Prevent dead-code elimination in native code.

For optimized variants, report original-candidate and optimized-variant measurements separately. Both must pass the same confirmation set. State languages, integer widths, native arithmetic, threading and build flags. Neither Python-versus-C speed ratios nor cross-library defaults isolate pure algorithmic effects.

## Resource limits

Use initial per-case soft budgets of about 2 seconds and a 512 MiB working-memory ceiling, adjusted explicitly to the available machine. Exceeding a budget should yield a labelled skipped/timeout/budget outcome, not an extrapolated timing. Slow first-query trace measurements may use a separately declared longer budget. Do not run enormous linear baselines merely to force a dramatic speed ratio.

Measure peak memory with a consistent method, preferably isolated subprocesses for competing methods. Distinguish cached-data size, temporary allocation and process overhead. Record if resource measurements are approximate or platform-specific.

## Raw data and interpretation

Retain cases.csv or cases.json with exact p,f, poles, weights, trace provenance and expected outputs. Timing samples should identify case, workload, method, source hash, block, repetitions, measured nanoseconds, preparation/query/total stage, status and any exception. Record runtime, dependencies, CPU, core count, OS, compiler flags, threading and uncontrolled-host caveats.

Provide operation/bit bounds separately from observed time. Include additions, multiplications, inversions, trace preparation and s-dependence explicitly. Measurements over a bounded 64-bit implementation do not prove an asymptotic complexity theorem.

The deliverable must report actual crossovers, wins, ties, losses and coverage gaps. Do not announce superiority over all existing evaluations from a finite set of implementations or primes.
