# Measured automatic dispatch

Version 0.8 adds opt-in `engine="auto"` to `ManyPrimeEvaluator` and the
many-prime CLI. A local profile selects among independently verified
complete-output implementations. It can choose a forest chunk count or an
independent boundary backend. Explicit forest/independent choices and the
earlier default forest behavior remain available.

## Calibrate and use on this computer

For a streamed rounded-third CSV:

```console
python calibrate_dispatch.py --bound 20000 --family rounded_third --collection streaming --profile laptop_dispatch.json
python many_primes.py --bound 20000 --family rounded_third --engine auto --profile laptop_dispatch.json --out rounded_thirds.csv
```

On Windows, `calibrate_and_run.bat` runs these two steps and checks their exit
statuses. Calibration is explicit and can take substantially longer than the
eventual selected evaluation because it runs every candidate repeatedly and
constructs independent references.

For collected JSON or Python results, omit `--collection streaming` during
calibration and omit `--out` during evaluation:

```console
python calibrate_dispatch.py --bound 3000 --family fifths --profile collected_dispatch.json
python many_primes.py --bound 3000 --family fifths --engine auto --profile collected_dispatch.json
```

```python
from many_primes import ManyPrimeEvaluator, range_queries
from calibrate_dispatch import calibrate

queries = range_queries(3000, "rounded_third")
calibrate(queries, "my_dispatch.json", repeats=3)
result = ManyPrimeEvaluator().evaluate(queries, engine="auto", profile="my_dispatch.json")
print(result["statistics"]["dispatch"])
```

Profiles are not automatically searched for or created by normal evaluation.
`profile=None`, a missing file or an unmatched workload uses the explicitly
labeled independent default. Its normal resource limits still apply; it is
not guaranteed to handle every request that a forest could handle. An
explicit engine bypasses profile loading entirely. Existing single-prime
interfaces and their conservative kernel cutoffs are unchanged. Measured
independent selections can override that cutoff by choosing a backend for
the complete calibrated workload.

## Exact matching and portability

| Matched property | Scope |
|---|---|
| Ordered request vector | All p/L pairs, input order and duplicates |
| Output contract | Full versus U-only |
| Collection contract | Collected results versus unique iterator consumption |
| Evaluator configuration | All kernel limits, direct cutoff and forest/request caps |
| Implementation | Release version and SHA-256 of runtime/calibration source files |
| Environment signature | Python version/implementation, OS/release, CPU/architecture information, logical CPUs, pointer width and optimization flag |

Changing any matched property invalidates reuse. There is no interpolation,
nearest-neighbor match or extrapolation. Environment matching is a practical
compatibility signature, not a unique hardware identity: equal machine
descriptions can still hide different clocks, power states, contention and
memory configurations. Timings remain predictions, not a guarantee of the
fastest method on every subsequent run.

The packaged `results/local_dispatch_profile.json` records the generating
Linux environment. It is evidence, not a universal tuning file. Generate a
new profile on the laptop. A Windows/Linux mismatch falls back with
`profile_environment_mismatch`; an edited implementation falls back with
`profile_implementation_mismatch`. Calibration refuses to overwrite an
incompatible existing profile and asks for a new filename in its error text.
Compatible records are preserved and a repeated workload is updated atomically.

## Calibration and verification

Calibration compares independent auto/direct/product_tree/bgs candidates
and forest candidates at 1, 8 and 32 requested chunks by default. Equivalent
forest schedules are measured once. Candidate order rotates between repeats
to reduce fixed-order warming/load bias. Every retained candidate has at
least three positive finite timing samples. Medians are recomputed from
those samples when selecting; stored aggregate medians are not trusted.

Every timed B/a/U row is checked against independent scaled coefficient and
original t recurrences. Collected order, duplicate values and output count
are checked. A wrong result aborts calibration and leaves the existing
profile unchanged. A candidate that exceeds its supported resource limits
is excluded with a reason; a profile with no completed candidates is not
published. Tests separately cover exact integer binomials and the original
retained forest.

The definition-level reference itself has a default 10,000,000-step guard,
counted as the sum of the largest requested cutoff at each prime. The API
and CLI expose `max_reference_steps` / `--max-reference-steps`. Repeats must
be 3..20. `--forest-chunks` can restrict the tested forest schedules; an empty
list deliberately calibrates independent implementations only. A result is
best only among measured eligible candidates, not among all conceivable
implementations or chunk counts.

Collected calibration times the complete evaluate call. Iterator calibration
fully consumes the unique iterator into a list, so it measures iterator
arithmetic plus materialization, not disk writing or CSV publication.
Constructor, imports, references, verification and profile I/O are excluded
from candidate times. Collected and iterator profiles remain separate.
Calibration is a same-process comparison; it does not reuse the earlier
fresh-process benchmark as if it were a local measurement.

## Selection policy and diagnostics

| Dispatch status | Meaning |
|---|---|
| measured_exact | Selected the lowest eligible measured median |
| measured_near_tie | Kept the independent baseline when the best candidate improved its median by less than 5% |
| fallback_untrained | No usable matching measurement; independent default chosen |
| explicit_override | Caller selected forest or independent; profile ignored |

The 5% tie margin is a stability policy, not a statistical confidence interval.
With `backend="auto"`, all measured independent kernels are eligible. An
explicit backend filters independent candidates to that kernel. Forest
choices do not use the field-product backend. Measured forest schedules
are checked against current resource guards again before selection. Explicit
`--engine forest --chunks N` fixes the forest schedule; under engine auto,
the selected measured chunk count takes precedence over the supplied default.

The dispatch record includes the selected method, backend/chunks, reason,
matching workload digest, median, sample count, eligible count and selection
overhead. Fallback reasons distinguish missing, malformed, stale and
unmeasured profiles. Profiles are bounded JSON data with method allowlists;
they contain no executable code or cached arithmetic answers. Corrupt data
does not trigger calibration or disable mathematical/resource validation.

Profile parsing, source hashing and selection add overhead. They are included
in actual auto-evaluation totals and held-out timings. For tiny workloads,
this overhead can outweigh the benefit of choosing a faster kernel; an
explicit method avoids it. Untrained auto chooses independent conservatively
to avoid automatically traversing a huge sparse recurrence. It can be much
slower than a forest for an uncalibrated dense range. The diagnostic says
fallback_untrained, so this is never labeled a measured optimum.

## Evidence and remaining scope

`test_dispatch.py` contains deterministic synthetic timing fixtures for policy
checks and separate real small-workload calibration checks. Synthetic values
are never reported as performance measurements. Tests cover source/environment
invalidation, output/collection/order matching, malformed samples, overrides,
tie handling, resource checks, no background training and atomic publication.

`benchmark_dispatch.py` performs real local calibration, then separate
verification runs of measured auto, the selected explicit implementation,
and untrained auto on the same workloads. These are held-out executions of
calibrated inputs, not evidence of generalization to new inputs. Its auto
timings include profile/selection overhead. RESULTS.md gives the actual
counts, selected routes and measurements. The earlier complete-output and
memory benchmarks remain runnable; historical evidence is separated by release.

This release does not train a universal hardware model, tune every standalone
factorial call, infer timings for unseen prime ranges, measure peak memory
again, add p-squared arithmetic, or change retained mathematical kernels.
