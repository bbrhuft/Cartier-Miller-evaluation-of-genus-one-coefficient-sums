# Native BGS evaluation modulo p squared

Implementation and complete Linux comparison for David, 1 October 2026. This research delivery is unrefereed; novelty and global optimality are not established.

The bounded native implementation is complete. It evaluates the quarter-family incomplete sum modulo $p^2$, recovers the precisely specified Witt residue $K_p\bmod p$ through the preserved W1/W2 identities, and evaluates the original rational $U_p(n)\bmod p^2$ through its own recurrence. It supports prime $p\ge13$, $p\equiv1\pmod4$, $n=(p-1)/4$ and $p<2^{32}$. It computes the incomplete sum to recover $K_p$; sum-avoiding extraction remains unresolved.

At $p=1{,}000{,}000{,}009$, complete Witt recovery took 95.979 ms against 299.664 ms for the matched native tree, a factor of 3.12. Original $U$ took 212.932 ms against 732.515 ms, a factor of 3.44. Near the supported cap, at $p=4{,}294{,}967{,}197$, the factors were 4.07 and 4.42. These are measured comparisons between the implementations delivered here, not a portable crossover or a claim against every current mathematics system.

## Exact outputs and method

The native BGS path builds matrix block values directly by shifted Lagrange interpolation and FLINT middle products. The matched native tree builds the same polynomial matrix block and evaluates it with FLINT's generic native multipoint tree. Both use the same unsigned-word arithmetic, matrix channels, width rule and final normalization. A separate carry-safe native Montgomery recurrence supplies the linear-work control. The client Python tree is also rerun on the same machine at the smaller rows; it uses Python integers in this environment, not the collaborator's optional GMP backend.

The weighted prefix has a two-dimensional lower-triangular recurrence, stored in three channels. It uses $N=n+1$ terms at $y=z^4$ to obtain the inclusive sum required by W1. The original rational sum has the preserved four-dimensional degree-one recurrence, stored in seven nonzero channels. Its denominator is $2^nn!$, while the prefix denominator is $4^NN!$; both are units. The original $U$ path bypasses a separate harmonic calculation without evaluating that correction from the geometric coefficient alone.

The exact Witt normalization is unchanged:

$$
F(w)=\prod_{j\ge1}(1-c_jw^j),\qquad K_p=\frac{c_p}{M\beta}\pmod p.
$$

It uses the fixed integral curve $E:y^2=x^3+2x$, its prime-to-$p$ torsion lift, traced annihilator, moving coordinate $z$, and normalized Miller quotient. Field setup, Cornacchia and its nonresidue scans, exact fixed-model trace, torsion lifting, Miller arithmetic, the boundary, the incomplete sum, certified digit extraction and W2 reconstruction are all inside complete Witt timings. Original-U timings have no unused elliptic setup. The different targets must be compared separately.

## Complete measurements

The table gives medians of five repetitions in milliseconds on one Linux VM with an AMD EPYC 9V74 virtual CPU, GCC, Python 3.12.14, python-flint 0.9.0 and FLINT 3.6.0. FLINT used one thread and the benchmark was pinned to one available Linux CPU. Methods were rotated per repetition. Imports, backend initialization and compilation are excluded from the hot table; certification is included, including the native guard. Each repetition constructs its own curve setup and arithmetic data. Result serialization is outside the hot query, identically for every method. Full samples, stage timings, values, CPU information and hashes are retained in JSON and CSV.

| Prime | Witt BGS ms | Witt native tree ms | Original U BGS ms | Original U native tree ms |
|---:|---:|---:|---:|---:|
| 65,537 | 0.462 | 0.434 | 0.234 | 0.370 |
| 1,048,589 | 2.735 | 3.392 | 1.843 | 3.086 |
| 16,777,289 | 8.409 | 13.170 | 15.165 | 28.606 |
| 268,435,493 | 42.840 | 102.063 | 94.295 | 250.748 |
| 1,000,000,009 | 95.979 | 299.664 | 212.932 | 732.515 |
| 4,294,967,197 | 229.964 | 936.049 | 506.914 | 2242.107 |

At $p=65{,}537$, the complete native direct Witt recurrence took 0.428 ms and the native tree 0.434 ms, against BGS at 0.462 ms. At $p=1{,}048{,}589$, BGS took 2.735 ms against direct at 3.965 ms. At $p=268{,}435{,}493$, Witt BGS took 42.840 ms against direct at 550.010 ms, and original-U BGS took 94.295 ms against direct at 908.598 ms. Thus the direct method remains useful at smaller inputs. No automatic dispatch threshold is inferred for Windows.

The Python tree comparison is deliberately capped at $16{,}777{,}289$, where complete Witt and original-U medians were 332.273 and 674.349 ms, against native BGS at 8.409 and 15.165 ms. This combines compilation, native polynomial arithmetic and the BGS improvement; the matched native tree isolates the BGS contribution more closely. Native direct measurements are capped at $268{,}435{,}493$. Larger table rows compare native BGS and native tree; omitted controls were not measured there.

An actual 100-prime batch from $16{,}777{,}289$ through $16{,}780{,}537$, with three complete repetitions and no retained per-prime setup, took median 0.845220 seconds for BGS and 1.478744 seconds for native tree. Every output matched. This measured saving is 0.633523 seconds for this batch; it is not evidence about overnight research workloads in general.

Fresh-interpreter comparisons include process launch, imports and backend loading, with three repetitions. At $p=1{,}000{,}000{,}009$, complete Witt wall medians were 165.390 ms for BGS and 363.733 ms for native tree; original-U medians were 290.116 and 837.324 ms. At $p=1{,}048{,}589$, fresh-process wall times were roughly 68–71 ms for either method, showing that launch and imports dominate there. Operating-system caches were not flushed; these are fresh-process timings, not cold-storage timings.

Fresh-process absolute peak RSS at $p=4{,}294{,}967{,}197$ was median 33.90 MiB for Witt BGS and 35.11 MiB for its tree control; original-U figures were 35.52 and 37.09 MiB. These include Python, imports and FLINT and use three repetitions. They are measured process peaks, not proofs of every backend's scratch-memory bound.

## Proofs and finite validation

DERIVATION.md proves the two recurrences, ordered block construction, offset conventions and interpolation unit conditions. It also explains unsigned multiplication, overflow-safe addition and carry-safe Montgomery reduction. For the quarter truncations the default $s=\lceil\sqrt N\rceil$ satisfies $s^2+2s<p$, which makes the fractional-shift reciprocal numerators units. Nonzero multiples of $p$ receive an explicit rejection rather than a prime-field inverse. The batch inverse is computed by extended Euclid. Dividing a certified numerator by $p$ occurs only for the Witt residue digit and is not ring inversion.

The finite audit passes for all 146 quarter-family primes from 13 through 2000. Every prefix and boundary agrees with exact integer binomial values. Original $U$ agrees with exact Fraction arithmetic at all 43 such primes through 500 and with a separate modular form of the original rational recurrence above that. There are 438 complete native W1/W2 comparisons across the three native methods and 856 forced-width checks. These counts overlap in their underlying primes.

The audit also passes 6,384 exact edge/random arithmetic cases, including Montgomery multiplication near the unsigned-word cap; 1,140 successful polynomial shift cases; 60 explicitly expected nonunit rejections; and 64 short-recurrence controls with large moduli. Independent correctly ordered full Miller-series Euler extraction matches at $p=13,17,29,37,41,73,97,101$. The known values $K_{13}=7$, $B_3=70\pmod{169}$ and $U_{17}(4)=179\pmod{289}$ are retained. Large complete BGS/tree outputs and reverse-Witt reconstruction agree at six stated primes through $4{,}294{,}967{,}197$. Direct and Python controls were additionally run through $16{,}777{,}289$ in that audit. The GCC undefined-behaviour-sanitized quick audit passes; it supplies no timing comparison and is not a memory-safety proof.

## Modulus limits and algorithmic status

The checked prime cap is $p<2^{32}$, so $q=p^2<2^{64}$. Public Python checks occur before ctypes conversion, and the native guard rejects wider primes before squaring. The tested near-cap modulus is genuinely 64-bit. The collaborator's $p=4{,}294{,}967{,}357$ requires a 65-bit square and returns `unsupported_word_modulus`. No multiprecision backend or automatic wider fallback is delivered. A separate width cap of 65536 bounds allocations; default supported quarter queries require at most 32768.

Bostan, Gaudry and Schost (2007), Theorem 14, supplies the established shift-based recurrence algorithm over rings under explicit unit conditions. The delivered kernel has a conservative cost $O(\mathsf M_R(\sqrt p)+\log^2p)$, with the latter charging this implementation's per-plan Euclidean inversions. Its explicit arrays occupy $O(\sqrt p)$ words, plus polynomial-multiplication scratch. The native tree has the conventional $O(\mathsf M_R(\sqrt p)\log p)$ bound. Complete Witt cost additionally contains the actual inherited setup; no unconditional polylogarithmic bound is asserted for its deterministic nonresidue scan. Growing-precision bit complexity and a sub-square-root theorem are not established.

This package is a specialized recurrence and Witt application. It does not compute a general Cartier–Manin operator. It makes no new claim about arbitrary-L special-family speedups, BBP, factorial lower bounds, factoring or general point counting. The positive quarter evaluation, maximal higher-genus prefix theorem and reviewed exceptional normalization retain their earlier status. No new higher-genus boundary formula or sum-avoiding Witt formula is supplied.

## Windows and delivery

The source-build installer uses standard CPython 3.12 x64, an isolated local virtual environment, the pinned wheel and existing MSVC x64 tools. It does not change QGIS/OSGeo4W or unrelated Python environments. Linux compilation and arithmetic pass. Windows compilation, actual precision-two arithmetic and this separate optional Tk explorer's visual display remain to be confirmed; the earlier fifth-point mod-p Windows results do not establish them.

After extraction, run setup_windows.bat, then benchmark_windows.bat. The latter runs hot, fresh-process, batch and memory comparisons. The optional explorer_windows.bat opens a visual query interface. Preserve results/benchmark_windows.json, results/audit_windows.json, results/memory_windows.json and build/build.log for review. Original inputs, source notes, mathematical derivation, exact controls, source hashes and Linux records are included in the ZIP. Integrity verification is separate from the mathematical audit.

## Reference

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. SIAM Journal on Computing, 36(6), 1777–1806. https://doi.org/10.1137/S0097539704443793 . The actual inspected source locations and inherited boundary/Witt provenance are recorded in SOURCE_NOTES.md.
