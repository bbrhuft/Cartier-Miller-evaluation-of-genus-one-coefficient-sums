# Cartier–Miller boundary framework: final consolidation and release audit

Candidate 1.0.0rc1. Prepared 15 October 2026. Bounded AI-assisted self-audit of the implementation and evidence; this is not an independent specialist referee report.

## Verdict

**Suitable for a bounded research release candidate in the documented modulo-p domain.** No blocking implementation defect was found in the completed checks. All 95 regression methods, 11 public-command checks and all eight benchmark suites passed. The benchmark suites checked 1,051 executions, including 81 calibration and 16 separate memory-profiling runs. These are execution counts, not 1,051 distinct mathematical inputs or independent proofs.

The designation remains a candidate because the retained native prefix theorems are unrefereed and current-candidate Windows execution has not been inspected. This Linux run is direct evidence; reported laptop successes and the older attached Windows logs are recorded separately. Neither finite checking nor this self-audit is presented as external certification.

The scope is the boundary framework developed through versions 0.1–0.8. The separate original manuscript, CUDA work, historical prime-power experiments and other research extensions are outside this consolidation's change scope.

## Consolidated delivery

cartier_miller.py is the single public import and command facade. PUBLIC_INTERFACE.md defines supported exports, domains, output order, precision, provider trust, timing and error behavior. Earlier modules remain available; the facade delegates their tested implementations rather than introducing another mathematical evaluator.

The candidate includes source code, retained proof notes, independent regression oracles, all eight benchmark scripts, fresh current-version evidence, historical evidence, an audit ledger and a portable evidence runner. The six retained implementation files match their original provenance hashes. The two source archives available locally also match the archive hashes recorded in SOURCE_PROVENANCE.json; SOURCE_ARCHIVE_AUDIT.json records that check.

The runtime manifest pins 43 Python/batch/provenance files. Its fingerprint was identical before and after the full run:

`07d53a406d46e44504ecb5ceab5c52cf5ea520df34815dc5c9418f6a58cbabd1`

The manifest excludes prose and generated results so this report can summarize a frozen runtime run. Final package checksums cover prose/evidence as well. Hash consistency detects changes against the supplied manifest; it is not a signed authenticity claim or third-party attestation.

## Mathematical contract and proof review

The release computes a_L=binom(2L,L)*8^(-L) modulo an odd prime p<2**64, with 0<=L<p. B_L is strict: it sums a_i for i<L. Complete outputs use U=4B_L-2L(2L+5)a_L, checked against the independently defined original t recurrence. These definitions control every golden case and comparison.

| Component | Audit conclusion and assurance limit |
|---|---|
| General boundary | Generic factorial ratio valid in the lower half; a_0=1 and upper-half a_L=0 modulo p follow directly. The upper-half shortcut is not a p-squared claim. |
| Wilson reflection | Sign (-1)^(n+1) checked algebraically and exhaustively on small factorials; the survey's opposite sign was not retained. |
| Ordinary third | p>=7, p=1 mod 3, L=(p-1)/3; elementary a_L=-(L!)^(-3). Native trace-boundary reuse is retained and independently cross-checked numerically. |
| Rounded third | p>=11, p=2 mod 3, L=(p+1)/3; a_L=(3/2)*((L-1)!)^(-3). Prefix and boundary acquisition remain distinct. |
| Fifth points | p>=19, p=4 mod 5; L=(p+1)/5 and 2L. Retained interval ratios have a self-contained derivation in FIFTHS.md and independent binomial checks. |
| Native prefix routines | Genus-one thirds and the fixed genus-two fifth specialization are reused unchanged. Their project theorems remain unrefereed. Finite testing does not prove the entire geometric construction. |
| Scalar BGS backend | Value shifts and recursive block construction use exact integer-packed convolution. Known-node collisions are copied; all other interpolation denominators are nonzero field elements. This is a field-specific scalar implementation, not general matrix/ring BGS or Tal refinement. |
| Shared one-prime boundaries | Wilson normalization, identical products and sorted factorial gaps reuse work. One normalization inversion means the ratio denominators only; kernel/provider inversions are separate. The planner is not a global optimization of arbitrary overlaps. |
| Many-prime forest | Ordered triangular integer products and remaining-modulus carry are classical retained machinery. Sorting by cutoff supports arbitrary valid query pairs and repeated prime moduli; the proof uses divisibility, not a pairwise-coprime CRT inverse. |
| Dispatch | Exact local measurements choose among existing valid methods. They add no new mathematical theorem, unseen-input prediction or higher-precision support. |

The elementary domain, Wilson, third/fifth reductions, combination identity, block products and reuse invariants were reconciled with the source and proof notes. Primality uses the established seven-base bounded Miller–Rabin set also present in SymPy's official source, with independent sieve and pseudoprime-control checks. Those finite primality tests alone do not prove the full 64-bit witness theorem.

Rounded-third boundary extraction remains factorial-equivalent in the stated sense: the cube map is bijective when p=2 modulo 3, so a_L determines G=(L-1)! through the displayed relation with logarithmic additional modular powering. At ordinary thirds, the cube map is not injective and the available trace boundary does not by itself select the full factorial. This explains why ordinary trace reuse does not supply the missing uniform rounded-third factorial algorithm. No impossibility or lower-bound claim is made.

All public paths reject modulus powers other than one. None of the reductions, forest output combination or trace reuse is silently lifted to p-squared. Fixed-family fast prefixes also do not imply a fast isolated-prime prefix at arbitrary L; the general forest is an amortized calculation whose cost can be poor on sparse inputs.

## Current execution evidence

The full runner completed in 343.00 seconds on Python 3.12.14 / Linux x86_64. Regression tests took 76.52 seconds, with zero failures and errors. Source and retained-file integrity passed before/after execution. The evidence directory and its independently checksummed ZIP are under results/release_linux and results/release_linux.zip.

| Evidence | Current result |
|---|---|
| Regression methods | 95 passed; complete prior suite plus eight release/facade/error-handling/evidence tests |
| Public facade subprocesses | 11 passed, including calibration, actual profile matching, invalid prime and precision rejection |
| Retained implementation files | Six hashes matched; eight retained Python files including package initializers are included in validation source hashes |
| Frozen runtime files | 43 checked before and after execution |
| Benchmark suites | Eight completed sequentially at version 1.0.0rc1 |

| Suite | Checked runs |
|---|---:|
| boundary | 189 |
| thirds | 96 |
| fifths | 75 |
| output_modes | 42 |
| bgs | 342 |
| shared | 126 |
| many_primes | 64 |
| dispatch | 117 |
| Total | 1,051 |

The boundary-only benchmark compares against the direct boundary route; independent exact binomial checks are supplied by regression tests. Complete third/fifth and many-prime comparisons use the original weighted-sum recurrence. BGS kernels use direct-product controls; sharing uses an independent coefficient recurrence; dispatch verifies complete outputs during calibration and subsequent executions. The benchmark count therefore should not be mislabeled as 1,051 independent full-output proofs.

The full suite retains exhaustive small-prime factorial/boundary checks, all 1,226 third-family and 303 fifth-family primes through 10,000, Horner/schoolbook polynomial controls, larger held-out cases, exceptional normalizations, duplicates, empty requests, output modes, real sharing spies, repeated prime moduli, streaming cancellation, resource errors and atomic publication failures. Test source hashes, including retained modules, are in the current validation record.

## Performance and memory claims reconciled

Representative medians of three actual current-version samples, in milliseconds:

| Workload | Route A | Route B |
|---|---|---|
| Complete fifth pair, p=10,000,019 | Product tree 107.13 ms | BGS 25.65 ms |
| Sixteen nearby boundaries, p=10,000,019 | Separate BGS 300.43 ms | Adjacent sharing 16.53 ms |
| 1,135 rounded thirds below 20,000 | Independent 1506.85 ms | Forest 18.97 ms |
| Three sparse stopping queries up to p=1,000,037 | Independent 8.62 ms | Forest 4940.67 ms |
| Small sparse dispatch workload, max p=100,003 | Untrained independent 3.31 ms | Profile-based auto 4.37 ms |

The first two examples concern fixed arithmetic outputs; the dense many-prime example is amortized across a prime range. The sparse forest counterexample is material: it still traverses the integer recurrence to the largest cutoff. It must not be hidden behind a universal speedup claim. Profile lookup can also outweigh kernel selection on small calls; an explicit method remains useful.

The shared nearby case retains 32 acquisitions, but replaces large repeated products with two large products and 30 small gaps. Its benefit is product length reduction, not a false claim that the number of acquisitions became two. Shared mixed-family cases do reduce acquisition counts, with real backend calls intercepted in tests. Native ordinary defaults still avoid factorial acquisition altogether, and fifth comparators share their prefix/denominator work.

Many-prime timings include complete B/a/U outputs and use fresh subprocesses. Its 16 memory samples are separate from the 48 timing samples: traced Python peaks exclude imports, while process RSS includes imports. Both include collected result storage; neither is a measured streaming-memory guarantee. Arithmetic bit bounds are explicit resource guards, not a total-memory or optimal-memory theorem.

Dispatch calibration is a separate same-process measurement with rotated candidate order. The 36 later dispatch runs are new executions of calibrated workloads, not evidence of extrapolation to unseen prime ranges. Actual auto timings include profile loading, hashing and selection. Standalone kernel cutoffs remain conservative unless the complete calibrated independent route selects an explicit backend. Profiles are local evidence and must be regenerated on another machine/version.

## Findings and resolutions

| ID | Status | Finding/action |
|---|---|---|
| A01 | Resolved | Added one documented public facade while retaining delegated contracts. |
| A02 | Resolved | Deep malformed JSON now reaches the documented invalid-profile fallback; regression added. |
| A03 | Resolved | Unavailable profile implementation source now produces a source-unavailable fallback; regression added. |
| A04 | Resolved | Added portable capture, source freeze checks, retained-source verification and failed-run evidence ZIPs. |
| A05 | Reconciled | Reran all suites at the candidate version; historical records are separated and timing scopes made explicit. |
| A06 | Open evidence item | Current native Windows execution not inspected. The delivered runner makes the next evidence capture concrete. |
| A07 | Open review item | Independent specialist review of retained native prefix mathematics is still absent. |
| A08 | Documented limit | Sparse forests, untrained dense fallback and small-call profile overhead can be unfavorable. |
| A09 | Documented scope | Modulo p only; no accidental higher-precision transfer or new stopping families. |

AUDIT_LEDGER.json records these findings in machine-readable form. No additional mathematical feature is required to complete the current documented boundary interface. Further families, Tal refinements, checkpoint/resume, broader dispatch models and precision-two integration are separate extensions.

## Platform attribution and next evidence

| Platform/version evidence | What it supports |
|---|---|
| This candidate on Linux | Direct current execution of all stated tests, facade checks and suites |
| Attached Windows 0.1 logs | Inspectable historical Windows 11 / Python 3.12.10 execution, 13 tests; not execution of this candidate |
| Later laptop successes reported during iteration | Useful user reports, including 0.6–0.8; not substituted for inspected current-candidate logs |
| Candidate on native Windows | Pending external execution; no simulated or inferred Windows result is claimed |

Run release_check.bat on the laptop for validation and command checks, or run_checks.bat for the complete suite capture. Each creates a timestamped shareable evidence ZIP under results. Failed runs retain their source fingerprint, environment and logs with passed=false. Integrity-only capture is labeled separately and cannot be read as a successful mathematical run. The runner never regenerates its own baseline manifest.

This audit supports freezing the boundary feature set and retaining the candidate for reproducible research use. Independent mathematical review and current native Windows evidence remain distinct from implementation completion; neither is supplied by adding more features.

## Sources and review limits

The implementation and delivered proof notes are the principal audit objects. The six retained source modules come from the two user-supplied project archives identified by name/hash in SOURCE_PROVENANCE.json. They remain project research sources, not newly refereed publications.

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793. Author manuscript: https://cs.uwaterloo.ca/~eschost/publications/pollard.pdf.

Harvey, D., & Sutherland, A. V. (2016). Computing Hasse–Witt matrices of hyperelliptic curves in average polynomial time, II. *Contemporary Mathematics, 663*. https://doi.org/10.1090/conm/663/13352. Author offprint: https://math.mit.edu/~drew/conm13352.pdf.

SymPy development team. (n.d.). *Primality testing source: primetest.py*. Retrieved 15 October 2026 from https://github.com/sympy/sympy/blob/master/sympy/ntheory/primetest.py. Used to verify the stated bounded witness set; SymPy is not a dependency.

This is a bounded self-audit of code, contracts, mathematical derivations and execution evidence. It does not establish novelty, formal machine verification, optimal asymptotic performance, completeness of the entire research programme or independent human certification.
