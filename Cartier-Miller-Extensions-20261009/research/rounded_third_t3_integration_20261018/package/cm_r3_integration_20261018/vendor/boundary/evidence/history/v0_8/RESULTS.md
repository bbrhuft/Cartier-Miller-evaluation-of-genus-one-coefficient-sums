# Results: boundary framework 0.8.0

All 87 test methods passed with zero failures and errors in 74.108 seconds under Python 3.12.14 / Linux x86_64. The real dispatch benchmark verified all 81 calibration executions and 36 separate post-calibration executions. Five CLI subprocess checks passed. All retained arithmetic modules and the earlier single-prime services are unchanged; the many-prime scheduler now supports measured selection and shared schedule preflight.

## Regression and policy validation

The complete 75-test prior suite remains included. Twelve new dispatch tests cover exact profile matching, request order/duplicates, output/collection contracts, source/environment/configuration invalidation, malformed and nonfinite samples, median recomputation, backend constraints, tie policy, resource preflight, explicit overrides, no implicit calibration, real small-workload calibration, record upserts and preservation of an existing profile on failure.

Synthetic timing fixtures are used only for deterministic policy assertions. They are labeled in test_dispatch.py and are not included in performance evidence. The actual profile and timing report come from benchmark_dispatch.py, not those fixtures. Validation source hashes are in results/validation_results.json.

## Actual calibrated selections and subsequent timings

Median milliseconds of three subsequent executions of the same calibrated inputs:

| Case | Queries | Measured selection | Auto including selection ms | Explicit selected method ms | Untrained auto ms |
|---|---:|---|---:|---:|---:|
| rounded_dense | 1,135 | forest, auto, chunks 32 | 19.251 | 16.984 | 1598.439 |
| rounded_dense_stream | 1,135 | forest, auto, chunks 32 | 20.286 | 18.418 | 1627.655 |
| sparse | 3 | independent, direct, chunks 32 | 5.401 | 3.662 | 3.582 |
| fifth_pairs | 208 | forest, auto, chunks 1 | 3.452 | 2.185 | 177.046 |

Rounded dense cases cover every supported rounded-third prime below 20000. One case collects results and the other consumes the unique iterator into a list; they use separately calibrated profile entries. Fifth pairs cover both fifth outputs at primes below 3000. The sparse case uses rounded/ordinary third queries at primes 10007, 50021 and 100003. The forest was selected for dense work and independent evaluation for the sparse set.

Untrained auto means an explicit independent default, not the prior forest route and not a measured winner. Its status is fallback_untrained. The prior forest default remains available; auto must be requested. On these dense cases, the measured route avoids the much slower independent fallback. This is method selection using existing algorithms, not a new arithmetic speedup beyond the earlier forest implementation.

The sparse case is an important limit: measured auto took about 5.4 ms versus about 3.6 ms for an explicit independent call/untrained fallback. Profile reading, hashing and selection add overhead, and three calibration samples do not guarantee the best method on every subsequent run. Independent auto and direct choose essentially the same small factorial kernels here. This result supports avoiding automatic profile lookup for small latency-sensitive calls when the suitable explicit method is already known. The 5% tie margin is a stability policy, not a statistical confidence interval.

All actual auto timings include profile loading, environment/source checks, workload hashing, selection, complete arithmetic and output materialization. Imports, reference generation, calibration and JSON/CSV writing are excluded. This is a same-process local comparison, with candidate order rotated during calibration. It is not a new fresh-process or memory benchmark.

## Calibration coverage

The benchmark calibrates four exact workload/collection combinations. Candidates are independent auto/direct/product_tree/bgs and forests with 1, 8 and 32 requested chunks. Equivalent forest schedules in the three-query sparse case are measured once, giving 81 completed candidate runs at three repeats each. Every B/a/U row is compared with independent scaled coefficient and original t recurrences before retaining a timing.

The 36 later executions compare measured auto, the selected explicit implementation, and untrained auto. These are separate executions of calibrated inputs, not held-out prime ranges or evidence of generalization to unseen workloads. Complete ordered outputs and counts are checked. Results and the actual timing samples are in dispatch_benchmark_summary.json / dispatch_benchmark.csv, with local_dispatch_profile.json recording the generating environment and source signature.

## Laptop workflow and compatibility

Run calibrate_and_run.bat on Windows, or the two commands in MEASURED_DISPATCH.md. Calibration builds laptop_dispatch.json for the streamed rounded-third range and the following evaluation uses it to publish rounded_thirds.csv. Calibration is intentionally explicit, bounded and slower than a single evaluation; the normal evaluation path never trains in the background.

The packaged results/local_dispatch_profile.json is Linux evidence. A Windows environment mismatch rejects its measurements and uses the labeled independent fallback. Generate a new local profile instead of copying those timings into a laptop profile. Matching is exact over the ordered request vector, mode, collection, complete evaluator configuration, source implementation and environment signature. Compatible records can be updated atomically; incompatible existing profiles require a new filename.

Automatic selection remains opt-in. Explicit engines ignore profiles, and existing forest/independent entry points retain their behavior. Current resource checks remain active. An unmatched independent fallback can still encounter its normal prefix or kernel resource limits; the selector does not silently launch an unmeasured expensive forest. Existing standalone factorial/interval auto cutoffs are unchanged. Measured independent selections can choose a backend for the complete calibrated workload.

## Scope and reproducibility

MEASURED_DISPATCH.md describes profile validation, matching, fallback reasons, tie policy, timing boundaries and limitations. Profiles contain timings and metadata only, with no executable code or cached arithmetic answers. Tests supplement the previous mathematical validation; no new number-theoretic theorem or precision-two support is claimed.

Version 0.8 was executed on Linux. The user reported successful laptop execution of 0.7; current-version native Windows execution is not claimed. run_checks.bat now runs validation plus all eight benchmark scripts. Historical 0.5, 0.6 and 0.7 evidence is separated under results/prior_v0_5, prior_v0_6 and prior_v0_7. Only the dispatch calibration/verification benchmark was timed for this release; previous tests were all rerun. The earlier many-prime timing/memory benchmark remains runnable.
