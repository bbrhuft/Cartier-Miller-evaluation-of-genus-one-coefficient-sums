Cartier–Miller rounded-third integration: exact confirmation and workload-matched benchmarks

David Jordan research project, 18 October 2026. AI-assisted computational investigation; unrefereed. This is a standalone integration experiment, with original source packages and frozen kernels preserved. It makes no publication, priority, general optimality or improved-exponent claim.

The new boundary acquisition integrates successfully with the retained Cartier–Miller framework. At the nine tested inputs where automatic dispatch selected T3, the complete calculation was 1.67–6.52 times faster than native FLINT factorial plus the same Miller provider. At p=700,000,001,633, the median complete runtime fell from 5.833161 s to 0.895216 s, a 6.52× gain. The complete dense table is a different workload: the existing forest remains decisively faster. On sparse moderate-prime schedules, independent calls beat the forest. A useful integrated system must therefore select by workload, not replace every route with T3.

The implementation lives in integrated.py. RoundedThirdSession registers an exact custom reduction with the retained BoundaryEvaluator and delegates the final sum to the existing complete_sum function. Its B_L comes from the unchanged ThirdPointPrefixProvider. The explicit native comparator is registered through the same framework's factorial-backend interface and uses FLINT's n_factorial_fast_mod2_preinv. The T3 path uses the preserved R3.1 reconstruction, plans and anchor identities. There is no point-count or class-number preparation in this path, and no GRH or PARI dependency. The nodal anchor and native factorial provide exact fallbacks. This experiment supplies a standalone Python adapter and command, not an updated graphical workbench release.

The prime domain is 11 <= p < 2^63, p congruent to 5 modulo 6, with L=(p+1)/3 and m=L-1. The complete measured tuple is (p,B_L,a_L,U_p(L),G), G=m! modulo p. The adapter additionally reports B_m, a_m and U_p(m). The normalizations are

$$a_L=\frac32G^{-3},\quad a_m=-4a_L,\quad B_m=B_L+4a_L,$$

$$U_p(L)=4B_L-\frac{17}{3}G^{-3},\quad U_p(m)=4B_L-\frac{16}{3}G^{-3},\quad U_p(L)-U_p(m)=-\frac13G^{-3}.$$

MATHEMATICS.md gives the elementary telescoping and Wilson derivations. The final difference and the boundary never vanish. The boundary multiplier is 34/9, whose only zero here is p=17. Full boundary and factorial outputs are checked separately at that prime; a correct U alone would be insufficient. These are background/project identities and their elementary consequences, not newly discovered congruences.

The optional conductor q is a prime in [5,89] dividing p-1, with K=(p-1)/q. T3 uses exact Jacobi relations on grid factorials and short intervals of approximately K/3 and K/6, or K/3 and K/12. All accepted reconstructions are exactly certified. LLL success on every input is unproved; a miss causes an explicit error or an automatic fallback. Automatic dispatch uses native factorial below 10^7 and, above that bound, the source's frozen T3 predictor against its nodal predictor. Its class-number fallback has been replaced by the unconditional nodal route. This machine-independent policy can miss cheaper options and is not an optimality claim. The retained geometric prefix theorem remains unrefereed; numerical agreement does not replace its proof review.

The integration candidate and 196 source/evidence/vendor files were hash-frozen at 2026-10-18T08:09:50.466182+00:00, before confirmation selection. This is an internal commitment, not an external timestamp. Development checked all 1,135 admissible primes below 20,000: 3,405 complete method checks, 1,135 integer-binomial checks, 1,135 independent elliptic-prefix comparisons and 200 forced T3 calls. Three forest chunk counts agreed. Invalid domains/conductors, the p=17 case and injected lattice misses were exercised. The two relevant inherited unittest modules also passed, 19 test methods in 9.355 seconds; this count is not a count of distinct mathematical inputs.

Fresh confirmation passed at 17 distinct primes, up to p=7,000,000,009,553. Prior source development, confirmation and benchmark inputs were excluded by the frozen rule. Every case compared the complete adapter against native-factorial and nodal boundary routes and compared its prefix with the independently coded elliptic Miller provider. Declared q inputs were also checked through forced T3. The three approximately five-million cases received independent original-weighted-recurrence, scaled-binomial-prefix and direct modular-binomial-product checks. Above that tier, no linear-time original weighted sum was computed; the comparison uses the independent prefix implementation and native factorial boundary. Prime certification is included in the public API calls; no claim is made that these primes were never used elsewhere.

| Fresh prime | Tier | Automatic route | Selected q |
|---:|---|---|---:|
| 5,001,767 | small | native | — |
| 70,000,283 | medium | t3 | 11 |
| 7,000,002,851 | large | t3 | 23 |
| 700,000,000,031 | largest | t3 | 71 |
| 7,000,000,727 | no_small_factor | nodal | — |
| 5,000,381 | small | native | — |
| 70,000,613 | medium | t3 | 11 |
| 7,000,000,013 | large | t3 | 31 |
| 700,000,004,549 | largest | t3 | 31 |
| 7,000,000,277 | no_small_factor | nodal | — |
| 5,000,777 | small | native | — |
| 70,000,481 | medium | t3 | 11 |
| 7,000,011,929 | large | t3 | 13 |
| 700,000,001,633 | largest | t3 | 47 |
| 7,000,000,769 | no_small_factor | nodal | — |
| 7,000,010,201 | large_conductor | t3 | 5 |
| 7,000,000,009,553 | extension | t3 | 47 |

The largest exact confirmation returned (B_L,a_L,U_p(L),G)=(4770090998586, 303509152059, 6267107181755, 2406416797142). This approximately 43-bit confirmation is not a timing benchmark and does not establish practicality at cryptographic prime sizes.

The following timings are medians of three rotated cold samples per method, all on the same host. Cold calls rebuild every Jacobi context and product tree and rerun the Miller arithmetic; no complete answer is cached. Input validation, registry/provider setup, conductor discovery, certification, products, normalization, derived G and result collection are charged. Imports and prime-search selection are outside timing. The implementation's first use can still load a p-independent plan table or native-library handle. Raw samples and component times are retained; three samples describe this host and do not constitute a portable performance guarantee. Reference comparisons occur after the timer stops, so no reference factorial is accidentally charged to a comparator.

| Prime | Automatic route | q | Native + Miller (ms) | Nodal + Miller (ms) | Integrated auto (ms) | Native / auto |
|---:|---|---:|---:|---:|---:|---:|
| 70,000,283 | t3 | 11 | 11.244 | 9.716 | 6.745 | 1.67× |
| 7,000,002,851 | t3 | 23 | 259.000 | 214.838 | 63.885 | 4.05× |
| 700,000,000,031 | t3 | 71 | 5894.902 | 4909.134 | 1153.621 | 5.11× |
| 7,000,000,727 | nodal | — | 260.154 | 214.452 | 214.251 | 1.21× |
| 70,000,613 | t3 | 11 | 15.190 | 12.261 | 7.868 | 1.93× |
| 7,000,000,013 | t3 | 31 | 261.129 | 220.053 | 58.941 | 4.43× |
| 700,000,004,549 | t3 | 31 | 5751.378 | 4784.071 | 1014.534 | 5.67× |
| 7,000,000,277 | nodal | — | 256.361 | 214.941 | 214.746 | 1.19× |
| 70,000,481 | t3 | 11 | 11.351 | 9.547 | 5.879 | 1.93× |
| 7,000,011,929 | t3 | 13 | 266.407 | 232.299 | 77.799 | 3.42× |
| 700,000,001,633 | t3 | 47 | 5833.161 | 4760.048 | 895.216 | 6.52× |
| 7,000,000,769 | nodal | — | 263.522 | 217.327 | 225.696 | 1.17× |

At the strongest measured example, the Miller prefix accounts for approximately 0.48% of the new complete runtime, so accelerating the boundary transfers almost directly to the full result. The three no-small-factor cases use the nodal fallback. Their modest gain over native is a nodal-anchor gain, not T3 acceleration. Against the explicit nodal route, the automatic fallback is essentially the same algorithm, with small selection overhead and measurement variation. The frozen cost model occasionally chooses a conductor different from the one used to select the input; that discovery and selection are included.

For dense prime tables every method computes every admissible p below the same exclusive bound and returns the same complete tuple. Sieve, arithmetic, collection and canonical tuple hashing are charged; disk I/O is excluded. The Python and GMP forests are byte-identical retained recurrence machinery with different integer backends. They obtain prefix and boundary jointly and bypass the geometric prefix. No part of their gain is credited to T3 or to the original genus-one theorem. Auto selects native at every input in this small-prime benchmark range, so its timing is expected to match native up to overhead/noise.

| Exclusive bound | Tuples | Native + Miller (s) | Integrated auto (s) | Python forest (s) | GMP forest (s) | Native / GMP forest |
|---:|---:|---:|---:|---:|---:|---:|
| 2,000 | 152 | 0.120307 | 0.122290 | 0.001377 | 0.001255 | 95.8× |
| 20,000 | 1,135 | 1.273731 | 1.336106 | 0.015224 | 0.011338 | 112.3× |
| 100,000 | 4,805 | 6.677996 | 6.652261 | 0.157454 | 0.057797 | 115.5× |

The sparse moderate-prime schedule contains the sixteen explicitly recorded primes from 1,000,211 to 2,501,171. Every method receives precisely that schedule. Native independent calls took 0.037191 s, auto 0.037016 s, forced T3(q=5) 0.039155 s, the Python forest 8.171517 s and the GMP forest 0.689112 s. Forced T3 does not improve this smaller workload. The forest pays to construct its recurrence from zero to the last requested cutoff; it cannot receive that long initial state for free. Thus the GMP forest is 18.5 times slower than independent native calls here, despite its large advantage on dense tables. Very large sparse-prime forest requests are rejected by the declared maximum cutoff of 2,000,000; no hypothetical timing or general lower bound is assigned to them.

The exploratory survey generated 39,264 complete tuples for every admissible prime below 1,000,000. It checked the stated normalization and adjacent-sum residuals throughout, and found 0 zeros of U_p(L), 0 zeros of U_p(m), and 0 simultaneous zeros. No conclusion of universal nonvanishing follows: the attempted nonvanishing counterexample search had no counterexample in this finite range. The impossibility of simultaneous zeros follows separately from the exact nonzero difference above. All 1,135 rows below 20,000 received definition-level checks, and 64 seeded rows above that bound received both full definition checks and adapter comparisons. The other rows have the retained forest's proof and internal checks, not independent row-by-row verification. This is newly executed evidence on a previously studied range, not disjoint confirmation or a newly discovered dataset claim. Survey generation, residual checks, selected oracles and CSV output together took 7.404 seconds; that is not a matched million-bound timing comparison. The canonical tuple digest is 414f8c745e5f6f0eb200f7919639c31678cdd8ae7535bd754106de1096d069d3.

The recorded environment is 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ], Linux-6.18.55-x86_64-with-glibc2.39, CPU AMD EPYC 9V74 80-Core Processor; python-flint 0.9.0 and gmpy2 2.3.2. No concurrent number-theory process ran during benchmarks. CPU frequency and scheduler effects were not controlled. The inherited FLINT bridge calls Linux shared-library internals; Windows portability and newer ABI compatibility are not established. requirements.txt pins the executed dependency versions. The fixed conductor range preserves square-root dependence on p, and no new complexity exponent or cryptographic-size capability is inferred.

The appropriate practical rule from these bounded measurements is to use the integrated Jacobi route for suitable sparse large-prime queries, retain factorial/nodal alternatives and use the forest for dense tables. A calibrated production scheduler should also account for conductor cost, machine and available memory; this experiment does not automatically replace the workbench's existing many-prime dispatcher. An optimized compiled remainder forest, PARI/Magma/Sage systems, Tal's general reconstruction implementation and the earlier project Jacobi anchor are not directly benchmarked here. Therefore this is a reproducible improvement over the named matched comparators, not a new-best-algorithm claim. The rounded-third-specific increment over an unmodified Tal routine still needs its own matched comparison.

README.md gives commands. integrated.py is the API/CLI, oracles.py contains definition-level controls, experiment.py reproduces the frozen confirmation, benchmark and survey, and audit.py verifies the freeze, preserved vendors and final manifest. BENCHMARK_SUMMARY.csv gives analysis-ready timing summaries with raw samples; evidence/BENCHMARK.json retains the full measured data. The original freezes, source reports and implementations remain in vendor/, with provenance hashes. No external repository or published manuscript was changed.

The established background is the factorial and telescoping reductions, classical Jacobi reconstruction machinery, and retained forest strategy. The contribution of this experiment is the working registry integration, corrected fallback behavior, larger disjoint complete-output checks and workload-matched measurements. The next precise algorithmic question is whether guaranteed reconstruction at larger conductors can extend the successful sparse-query regime without its setup cost erasing the reduced interval work. Publication and priority remain subject to a completed specialist novelty audit.
