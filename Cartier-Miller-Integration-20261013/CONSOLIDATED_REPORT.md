# Cartier–Miller: consolidation and integration audit

David Jordan research programme, 13 October 2026. Separate, unrefereed, AI-assisted assessment and runnable prototype. This audit preserves the published manuscript, supplied research archives and review qualifications. It does not establish novelty, external specialist certification or a new generic fast algorithm.

## Principal finding

The extensions can be assembled into a coherent exact evaluation system now. Its organising principle should be the requested mathematical output and modulus, with curve arithmetic and coefficient extraction treated as reusable services. The branches do not need a single universal formula to form a useful system.

The audit delivered a standard-library Python prototype covering original sums modulo $p$ and $p^2$, the main genus-one row theorem, cubic branch queries, fixed-discriminant Cartier data, weighted binomial prefixes and explicit higher-genus hybrids. Preparation is reusable through a per-prime Session. Exact fallbacks, trust labels and budgets keep unresolved research dependencies visible.

The project already contained Cartier–Miller Studio, an integration demonstration from September. This delivery therefore supplies a common arithmetic/specification layer and the later capabilities rather than another GUI. It leaves the Studio interface and existing Windows environments unchanged.

## What the overview changes

| Audit finding | Practical consequence |
|---|---|
| Several modules use the name K or kappa for different quantities | Keep ordinary slope, cubic coefficient, Witt residue and model differential scale explicitly distinct |
| Both depth-three families are completed, including D=-256 | Use the corrected recognizers and tables; the older missing-family comparator is not authoritative |
| The maximal higher-genus theorem includes its setup and requires no point count | Preserve this advantage; separately charge its boundary acquisition |
| Later fifth-point work already supplies reduced boundary products and native comparisons | Fifth points have an existing complete hybrid, not only a prefix theorem |
| Native precision-two work already computes complete sums | Preserve it as an engineering backend; it recovers Witt data by computing sums and does not solve sum-avoiding extraction |
| The formal-weight derivative bridge was already analysed in the fifth-point report | Do not restart it as an untried shortcut; any continuation must account for the infinitesimal endpoint |
| The old third-point divided routine rejects exceptional inputs | Use the later undivided implementation, whose retained normalization is proved directly in characteristic p |
| A boundary multiplier can vanish | Skip boundary acquisition when the original sum does not require it |

The newly integrated prototype uses package-relative imports and a single input/modulus contract. It avoids reliance on historical absolute paths. Its validator fails with a nonzero process exit on a discrepancy. An externally supplied trace remains visibly trusted unless the implemented D=-7 certificate verifies it; a Hasse interval is not trace certification.

## Capability map

| Capability | Mathematical status within the supplied project | Live integration status |
|---|---|---|
| Main genus-one row evaluation | Retained theorem, including exceptional normalization | Cubic/quartic prime-field queries; slow direct trace setup or explicit trusted trace |
| Complete quarter-point original sum modulo p | Retained complete family | Integrated and automatically recognised |
| Ordinary third point modulo p | Retained complete family, including exceptional case | Integrated and automatically recognised |
| Rounded third point | Fast prefix and factorial-equivalent boundary | Complete explicit hybrid with product boundary; no new exponent gain |
| Fifth points | Fast genus-two prefix and accepted tenth-point boundary reduction | Complete explicit hybrid; three intervals shared for the pair |
| Seventh and higher fractions | Fast special-family prefixes | Complete explicit hybrids with generic product boundaries |
| CM seeds and depths one through three | Restricted ordinary slope formulas with review qualifications | Fixed-D service; corrected depth recognizers cross-checked against it |
| Generic ordinary Cartier scalar | Local necessary equations do not select it; efficient acquisition unresolved | Exact streaming coefficient fallback, not a new fast solver |
| Quarter local lift modulo p squared | Retained fast coefficient lift after setup | Diagnostic service available |
| Complete original sum modulo p squared | Retained recurrence-product algorithms | Portable product-tree fallback and correction diagnostics; native source retained separately |
| Fast sum-avoiding Witt correction | Unresolved | Not advertised as an implemented feature |
| Polynomial weights | Retained recurrence identities | Falling-factorial weighted binomial prefix service |
| General binomial weights | Retained maximal-family extension | Prefix service, with no derivative oracle |
| Extension-field row queries and restricted base-p digits | Earlier implementations and separate contracts exist | Retained internally/evidence; not widened into the public prime-field original-sum contract |
| Tal factorial routes | Conditional theoretical transfer, unrefereed report and implementation gaps | Research dependency only; no live Tal backend |

The native FLINT paths are retained as source and evidence, with their domain and ABI limits. They were not rebuilt here because the required FLINT backend was absent. Their historical timing claims are not mixed into this audit's new measurements. The portable fallback instead reuses the existing Python-integer polynomial product/remainder tree. It is useful for exact assembly and comparison but not a replacement claim against the stronger native implementations.

## Independent checks and focused measurements

The integrated validator passed 12,798 complete original-sum comparisons and 580 exact Fraction controls. It also passed 7,226 main row queries, including 283 exceptional queries and 1,043 split-algebra queries; 175 complete higher-genus outputs; 533 short-model coefficient comparisons and 533 model-scaling checks; and 101 branch queries. Both corrected depth-three families agreed with the CM table. Twenty quarter precision-two cases agreed with independent complete sums and full Miller-series Witt extraction. These counts overlap in underlying inputs and are not counts of independent proofs.

Retained negative controls include the p=13 predictions 44 and 83 versus the true prefix 70 modulo 169; the p=17 original sum 179 modulo 289; and the unchanged full-block failure at p=7. The derivative-value ambiguity at p=19 is also retained. Input rejection, budget limits, duplicate indices, cache flags and nonzero CLI failures were checked.

The following are medians of five complete evaluations from the final prototype. Imports and serialization are excluded; prime validation and arithmetic acquisition are included. Each sample starts with a fresh Session. Exact original-recurrence references independently checked every benchmark output. All times are milliseconds on this Linux runtime.

| Complete original-sum workload | Structural/hybrid method | Shared direct recurrence | Product-tree recurrence |
|---|---:|---:|---:|
| Quarter, p=1,048,589 | 0.303 | 81.387 | 77.538 |
| Ordinary third, p=100,003 | 0.202 | 9.930 | 20.856 |
| Both fifth points, p=1,000,039 | 29.827 | 116.749 | 160.282 |
| All three seventh points, p=10,009 | 9.784 | 1.185 | 13.066 |
| Arbitrary L=12,345, p=100,003 | Not applicable | 3.854 | 10.885 |
| Quarter original U modulo p squared, p=1,048,589 | No fast geometric complete method | 100.718 | 94.951 |

The paired direct comparison shares one pass. The higher-genus comparison shares one prefix pass and the applicable boundary intervals. The original-sum product-tree baseline uses separate products per index; its paired time is not an optimally shared baseline. These are comparisons of the delivered Python implementations, not of every current BGS implementation or a portable dispatch threshold. The seventh-point result is particularly useful: a structurally faster prefix does not guarantee the fastest complete calculation at that size.

Fresh-process memory measurements are in the raw JSON. At the paired fifth workload, the hybrid's Python traced peak was about 0.303 MiB versus 0.986 MiB for the separate product trees; absolute process RSS was about 14.63 versus 17.02 MiB. The direct method used constant arithmetic state. These observations include interpreter/import effects in RSS and are not universal memory bounds. Timing and memory probes were separate.

Cached repeated-answer lookup and fresh-interpreter timing were recorded separately. The cached quarter result is an exact answer-cache lookup, not a new arithmetic speedup for another input. Operating-system caches were not flushed.

## Research priorities after integration

The immediate engineering priority is to use this common contract layer as the specification for a guarded native backend, then obtain actual Windows execution evidence. The retained native fifth and precision-two work already contains stronger algorithms than this dependency-free fallback. Bringing those into one interface could improve practical performance without pretending to remove any mathematical barrier. A graphical interface can follow the arithmetic contracts rather than acquiring another independent implementation.

The next mathematical investigation should choose one missing acquisition task. For complete higher-genus original sums, fifth-point boundary extraction has the best existing proof, reductions and comparator infrastructure. The supplied fifth-point report identifies the missing coefficients as Cartier images of specified second-kind differential representatives; the zero holomorphic Cartier matrix does not compute those images. Any derivative continuation must derive and cost its endpoint correction. Merely having fast values at finite-field weights is insufficient.

For higher-modulus original sums, the precise combined correction

$$J_p=\mathcal H_n-2a-4K_p-8d(b+a)\pmod p$$

is worth retaining as a bounded target because

$$U_p(n)=4\Gamma+\frac94a_n+pJ_p\pmod{p^2}.$$

This reformulation leaves room for cancellation. It is not evidence that the combined quantity is easier than its components. The prototype currently recovers it from complete sums, so it is a diagnostic reduction rather than an extraction algorithm.

Generic ordinary slope research remains separate. The local compatibility audit rules out selection by its enumerated necessary equations, not every possible arithmetic method. A proposed bridge from that slope to a higher-genus boundary or Witt correction must be proved and fully costed before the branches can share such an oracle.

Tal's 2026 report remains relevant to factorial backends but retains the supplied audit's unrefereed-theorem, representation, divisor-search and reconstruction qualifications. The official record was checked during this audit; the algorithm was not independently re-proved or implemented. BGS remains the delivered conventional baseline here, not a proved lower bound (Bostan et al., 2007; Tal, 2026).

## Decision

Retain the extensions as modules with different exact outputs, linked through shared preparation and explicit reconstruction identities. The new prototype demonstrates that a coherent system is possible now, with complete outputs and honest fallbacks. It also shows precisely which desired speedups require additional mathematics. No manuscript revision, GitHub publication, global optimality claim or new factoring/BBP implication follows from this audit.

In plain language, the project already has several good engines. This audit supplies a common set of controls, connects the engines that can complete the same calculation, and labels where an engine still needs an expensive extra part. The useful next advance can now be chosen against a tested system rather than against isolated reports.

## References and evidence

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793.

Hesselholt, L. (n.d.). *Lecture notes on Witt vectors*. https://math.mit.edu/~larsh/papers/s03/wittsurvey.pdf.

Tal, Y. (2026). *Computing modular factorials below the square-root barrier* (ECCC TR26-211). Unrefereed report. https://eccc.weizmann.ac.il/report/2026/211/.

The project reports, corrected CM review, local ordinary audit, later fifth-point reports, supplied archives, source hashes and raw results are retained in the supporting archive. `SOURCE_AUDIT.md` distinguishes sources checked now from inherited source audits and from unimplemented algorithms.
