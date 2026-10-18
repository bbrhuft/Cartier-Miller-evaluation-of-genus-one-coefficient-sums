# Rounded third point: certified Jacobi boundary backend and workload-matched measurements (18 October 2026)

This folder records the 18 October 2026 rounded-third integration experiment. It follows the 9 October obstruction note in [`../rounded_third_boundary_20261009/`](../rounded_third_boundary_20261009/), which is unchanged and still governs the mathematics it states.

The 9 October note showed that, at the rounded third point, the missing boundary is a Gauss factorial. This experiment connects a certified Jacobi-sum route for that factorial ("T3") to the existing Miller prefix. It also measures, against matched comparators, when that route helps and when other routes are better.

The work is AI-assisted and unrefereed. Below, *proved* means proved in the project manuscript or a companion document, not accepted by a specialist. *Certified* means each accepted output carries an exact algebraic certificate. *Observed* means finite evidence only.

## Summary

- **One prime at a time:** a certified Jacobi boundary backend was integrated with the existing Miller prefix. It made complete evaluation faster on the stated inputs: 1.67–6.52× against native FLINT factorial plus the same Miller prefix, at the nine tested primes where automatic dispatch chose T3.
- **Dense tables of primes:** the existing remainder forest is much faster there.
- **Sparse schedules of moderate primes:** independent native calls are best there.
- **No uniform method:** no uniform polylogarithmic algorithm for the boundary is known, and none is claimed.

## Mathematical contract

Let $p\ge11$ be prime with $p\equiv2\pmod3$, and work in $\mathbb F_p$. Set

$$
h=\frac{p-1}{2},\qquad m=\frac{p-2}{3},\qquad L=m+1=\frac{p+1}{3},\qquad a_i=\binom{2i}{i}8^{-i},\qquad B_j=\sum_{0\le i<j}a_i .
$$

The prefix is strict: $B_L$ excludes $a_L$. The original weighted sum is defined independently of these identities by

$$
t_0=1,\qquad t_{i+1}=t_i\frac{h+2+i}{2i+2},\qquad U_p(j)=\sum_{0\le i<j}(h+1+i)t_i .
$$

**Boundary and factorial (proved, elementary).** With $G=m!\bmod p$:

$$
U_p(j)=4B_j-2j(2j+5)a_j,\qquad a_L=\frac{3}{2G^3},\qquad G=\Bigl(\frac{3}{2a_L}\Bigr)^{(2p-1)/3},\qquad a_m=-4a_L,\qquad B_m=B_L+4a_L .
$$

The proof uses Wilson reflection, $(2m)!\,L!=-1$, and the fact that cubing is a bijection of $\mathbb F_p$, because $\gcd(3,p-1)=1$. So acquiring $a_L$ and acquiring $G$ are equivalent up to $O(\log p)$ field operations. This is a reduction, not an intractability theorem.

**Complete and adjacent sums (proved).**

$$
U_p(L)=4B_L-\frac{17}{3}G^{-3},\qquad U_p(m)=4B_L-\frac{16}{3}G^{-3},\qquad U_p(L)-U_p(m)=-\frac13G^{-3}\neq0 .
$$

The two sums therefore never vanish together. That each one is nonzero for every admissible prime is *not* proved.

At $p=17$ the multiplier $2L(2L+5)=34/9$ vanishes in $\mathbb F_{17}$, so $U_{17}(6)=4B_6$. A correct weighted sum at $p=17$ therefore does not validate a boundary backend; $a_L$ and $G$ must be checked separately.

**What Cartier–Miller supplies (proved in the manuscript).**

- For $f(w)=1-w^3/2$, the coefficient of $w^{3i}$ in $f^h$ is $a_i$. Since $3m<p\le3L$, the truncation evaluated at $1$ is exactly $B_L$.
- The Hasse coefficient is $0$, so the trace is exactly $0$, and $f(1)=1/2\neq0$ makes the query admissible.
- The manuscript's theorem therefore gives $B_L$ in $O(\log p)$ field operations, with no point counting.
- The signed boundary $a_L$ is extra work. The logarithmic prefix bound is not a bound for the complete rounded-third sum, and field-operation counts are not bit-operation counts.

**Cohomological interpretation (companion, unrefereed).** Take $E:y^2=x^3+1/4$, with origin at infinity and $\omega=dx/y$, which equals $-dw/v$ in the original coordinates. In the specified Čech de Rham basis $(e_1,e_2)$:

- the Cartier operator has matrix $\begin{pmatrix}0&2a_L\\0&0\end{pmatrix}$;
- absolute Frobenius has matrix $\begin{pmatrix}0&-2a_L\\0&0\end{pmatrix}$;
- here $2a_L=3G^{-3}$.

The scalar lives in full de Rham cohomology, whereas the Cartier–Manin matrix on regular differentials is zero. Differential scale, origin and signs must accompany any copied formula. This interpretation does not extract the scalar efficiently, and it is not an impossibility theorem for future extraction methods.

## What was implemented

The package is in [`package/cm_r3_integration_20261018/`](package/cm_r3_integration_20261018/).

- **Adapter.** `integrated.py` provides `RoundedThirdSession`, which uses the retained `BoundaryEvaluator` registry and `complete_sum`.
  - It takes $B_L$ from the unchanged `ThirdPointPrefixProvider`.
  - It checks primality, for $11\le p<2^{63}$ with $p\equiv5\pmod6$.
  - It returns $B_L$, $a_L$, $U_p(L)$ and $G$, the adjacent outputs, and route metadata.
- **Scope of the 63-bit limit.** The mathematical statements have no 63-bit restriction; only this implementation does.

| Route | What it acquires |
|---|---|
| Native factorial + Miller | FLINT `n_factorial_fast_mod2_preinv` gives $G$; the retained Miller prefix gives $B_L$ |
| Nodal anchor + Miller | Exact factorial-ratio anchor through FLINT block products; an independent comparator and the final fallback |
| Certified T3 + Miller | Split Jacobi-sum reconstruction for a prime conductor $5\le\ell\le89$ dividing $p-1$ (code option `--q`), with $k_\ell=(p-1)/\ell$ and shortened anchor intervals of about $k_\ell/3$ and $k_\ell/6$ (or $k_\ell/3$ and $k_\ell/12$) |
| Remainder forest | Ordered integer recurrence products giving prefix and boundary jointly across a schedule of primes; no Miller pass |

**Certificates.** A T3 reconstruction in $\mathbb Z[\zeta_\ell]$ is accepted only after its algebraic and root-of-unity normalization certificates pass; $J\overline J=p$ alone is not enough. That reconstruction succeeds on every input is *not* proved. Forced T3 fails explicitly. Automatic mode records the miss and falls back to the nodal route.

**Dispatch.**

- Automatic mode uses native factorial below $10^7$.
- Above $10^7$, it uses a frozen cost model to rank conductors with $k_\ell\ge10^4$. It tries T3 only when T3 is predicted to be cheaper than the nodal route.
- No class numbers, PARI or GRH are needed.
- For a fixed conductor, the interval work still grows like $\sqrt p$, up to logarithmic and multiplication factors. The $10^7$ threshold is a tested policy, not a universal crossover.

**Forest recurrence.** The forest is the established batch strategy, specialized to this recurrence. With $\Delta_j=4^j j!$:

$$
\mathsf A_j=\begin{pmatrix}4(j+1)&4(j+1)\\0&2j+1\end{pmatrix},\qquad \mathsf A_{j-1}\cdots\mathsf A_0=\begin{pmatrix}\Delta_j&\Delta_jB_j\\0&\Delta_ja_j\end{pmatrix}.
$$

Dividing by $\Delta_L\neq0$ recovers the prefix and boundary, and $G=\Delta_L/(4^L L)$. Sparse schedules still pay for the products from index zero.

**Not changed.** The adapter does not update the existing GUI, the many-prime dispatcher, or this repository's integration layer.

## Evidence

The candidate was hash-frozen internally at 2026-10-18 08:09:50 UTC, before the fresh confirmation primes were selected. The freeze covers 196 source, evidence and vendor files. It has no external timestamp. The table gives the package's recorded evidence, and the counts overlap.

| Evidence class | Recorded result | Qualification |
|---|---|---|
| Earlier companion | 152 admissible primes below 2,000; 595 conductor values checked against direct character enumeration | Inherited |
| Integration development | All 1,135 admissible primes below 20,000: 3,405 complete method comparisons, 1,135 integer-binomial checks, 1,135 independent prefix comparisons, 200 forced T3 checks; invalid inputs, $p=17$, injected lattice misses and three forest chunk counts | Development inputs, not held out |
| Fresh confirmation | 17 primes excluded from earlier ledgers, up to 7,000,000,009,553 | Independent prefix code and native/nodal boundary comparisons throughout; direct weighted-sum controls only at the three primes near five million |
| Exploratory survey | All 39,264 admissible primes below $10^6$: no zero of $U_p(L)$ or $U_p(m)$ observed | Definition-level checks for the 1,135 rows below 20,000 and 64 seeded larger rows only; a range studied before; not a nonvanishing theorem |

At $p=7{,}000{,}000{,}009{,}553$ the confirmed tuple $(B_L,a_L,U_p(L),G)$ is $(4770090998586,\,303509152059,\,6267107181755,\,2406416797142)$. This is an approximately 43-bit correctness check. It is not a timing benchmark and not evidence of practicality at cryptographic sizes.

## Timing

The timings are medians of three rotated cold samples on one host, recorded in `package/.../evidence/BENCHMARK.json`.

| Workload | Median complete runtimes | Reading |
|---|---|---|
| One prime, $p=700{,}000{,}001{,}633$, T3 conductor 47 | native + Miller 5.833 s; nodal + Miller 4.760 s; automatic 0.895 s | 6.52× over native; Miller is about 0.48% of the new runtime |
| All 4,805 admissible primes below 100,000 | native + Miller 6.678 s; automatic 6.652 s; Python forest 0.157 s; GMP forest 0.058 s | About 115.5× for the GMP forest over native; a batch gain, not a faster Miller query, and not credited to T3 |
| Sixteen-prime schedule from 1,000,211 to 2,501,171 | native 0.0372 s; automatic 0.0370 s; forced T3 0.0392 s; GMP forest 0.689 s | Forest about 18.5× slower; forced T3 does not help here |

**Which primes the speedups cover.** The 1.67–6.52× native/automatic speedups come from the nine single-prime inputs where T3 was selected. The other three single-prime inputs used the nodal fallback, and their gains of about 1.2× are not T3 gains.

**Ranges.** For the strongest row, the observed ranges were 5.831–5.857 s for native and 0.869–0.901 s for automatic. Ranges are descriptive, not confidence intervals.

**Host.**

- Linux x86-64, AMD EPYC 9V74.
- Python 3.12.14, python-flint 0.9.0 (FLINT 3.6.0) and gmpy2 2.3.2 (GMP 6.3.0).
- CPU frequency and scheduling were not controlled.
- The FLINT bridge calls Linux shared-library internals; Windows and future-ABI portability are not validated.

**Not compared.** There was no matched comparison with:

- an unmodified Tal reconstruction;
- an optimized compiled forest;
- the earlier project Jacobi backend;
- complete PARI, SageMath or Magma systems.

**Not claimed.** These results are not a claim of global fastest performance, of a new complexity exponent, or of a guaranteed gain above any threshold.

## Rerun in this repository (18 October 2026)

The checks below ran on Python 3.12.3 with python-flint 0.9.0 and gmpy2 2.3.2, from copies of `package/`, so the frozen evidence was not overwritten. Their outputs are in [`repository_rerun_20261018/`](repository_rerun_20261018/).

| Check | Result |
|---|---|
| `python verify_import.py` (this folder) | Passed. All 196 freeze, 187 vendor and 215 manifest entries match, except the one PARI documentation file that is not redistributed (see [RELEASE_NOTE.md](RELEASE_NOTE.md)). It fails on tampering, extra files or any other missing file (tested by injection). |
| `python check_handover_controls.py` (this folder) | Passed. See the detail after this table. |
| `python integrated.py 700000001633` with `--method native` and `--method t3 --q 47` | All three return the same tuple. Automatic chose T3 with $q=47$. The values match the frozen `CONFIRMATION.json`. Wall times, including imports, were 1.4, 7.9 and 1.2 s. These were not benchmarked. |
| `python develop.py` | Passed. The record is identical to the frozen `DEVELOPMENT.json` apart from timings and environment. |
| Package `audit.py`, unmodified | Stops at the excluded PARI file, as expected. With the PARI file present (checked before exclusion), it passed. |

`check_handover_controls.py` recomputed two things:

- the four control rows (p = 11, 17, 23, 29), from integer binomials, the original recurrence and a direct factorial;
- at the 43-bit prime, the tuple's internal consistency, plus $B_L$ using this release's own `retained/elliptic_prefix.py`. $G$ itself was not recomputed.

The benchmark, survey and confirmation scripts were not rerun, because they overwrite frozen evidence.

## Paper synchronization

The handover maps its statements to the reviewed draft `Cartier_Miller_Paper_Reviewed_20261018.md`. That draft's SHA-256 is `561e8427a7b1de5e09a0dbc719601b59a7ca26731eac40d5be2b957b09fffd51`, and it is not yet in this repository. The equation numbers are version-specific, and they do **not** refer to `Cartier_Miller_Paper_Revised_20261015.pdf` at the repository root. They are pending a statement-by-statement reconciliation when the revised paper is uploaded.

| Research statement | Reviewed-draft location |
|---|---|
| Weighted-sum definitions and telescoping identity | Equations (37)–(40) |
| Factorial/boundary equivalence | Equation (43) (older label RT1) |
| De Rham basis and matrices | Proposition 5, equations (44)–(46) (RT2–RT4) |
| Adjacent cutoff and nonzero difference | Equations (47)–(48) (RT5 is (48)) |
| Joint forest recurrence | Equation (49) (RT6) |
| Workload distinctions | Table 3 |
| Single-prime, dense and sparse measurements | Appendix, Tables 5–7 |

Older sources write `q`, `K`, `D_j`, `M_j`, `T` and `S` where the reviewed paper writes $\ell$, $k_\ell$, $\Delta_j$, $\mathsf A_j$, $\mathcal T$ and $\mathcal S$. Code interfaces such as `--q` keep their names.

## Status and open questions

**Proved project results:** the factorial reduction and its transfer to the complete weighted sum.

**Prior frameworks:** the Jacobi-sum reconstruction and remainder-forest frameworks.

**The practical increment recorded here:**

- the certified anchor specialization;
- the registry integration and the unconditional fallback;
- the complete-output confirmation;
- the matched measurements.

**What did not work.** The project's selected-coefficient, local-jet and fixed-dimensional global-recurrence investigations found no uniform polylogarithmic extractor for the signed boundary. A search that found nothing is not an impossibility theorem.

**Open questions:**

- Whether guaranteed reconstruction at larger conductors can reduce the remaining interval work without the setup cost erasing the saving.
- A matched comparison with unmodified Tal reconstruction.
- A wider reproducible timing study.
- A production workload dispatcher.
- Portability.

The characteristic-$p$ proof does not establish evaluation modulo $p^2$. A persistent public archive or DOI and a completed specialist novelty audit are still outstanding.

## Contents

| Path | Contents |
|---|---|
| `Cartier_Miller_Rounded_Third_GitHub_Handover_20261018.md` | The repository handover, verbatim as received |
| `package/cm_r3_integration_20261018/` | The integration package, unchanged except as stated in RELEASE_NOTE.md; its `REPORT.md` is the integration report (byte-identical to the separately supplied `Cartier_Miller_T3_Integration_REPORT_20261018.md`) |
| `RELEASE_NOTE.md` | Received archives, hashes, the one restored and one excluded file, and how to verify |
| `verify_import.py` | Integrity check of the package against its own three hash lists |
| `check_handover_controls.py` | Regression check of the handover's quoted values |
| `repository_rerun_20261018/` | Outputs of the reruns above |

To reproduce, start in `package/cm_r3_integration_20261018/`, and work in a copy, because some scripts overwrite evidence:

```console
python -m pip install -r requirements.txt
python integrated.py 700000001633
python integrated.py 700000001633 --method native
python integrated.py 700000001633 --method t3 --q 47
python develop.py
```

Run Python without `-O`, because the retained prefix uses assertion checks. The package's own README lists the full reproduction commands. Rerunning the benchmark and survey changes evidence hashes. Archive the recorded evidence first, and never rewrite `evidence/FREEZE.json`.

## References

Harvey, D., & Sutherland, A. V. (2016). Computing Hasse–Witt matrices of hyperelliptic curves in average polynomial time, II. In *Frobenius distributions: Lang–Trotter and Sato–Tate conjectures* (Contemporary Mathematics, Vol. 663). American Mathematical Society. https://doi.org/10.1090/conm/663/13352

Tal, Y. (2026). *Computing modular factorials below the square-root barrier* [Unrefereed preprint]. ECCC TR26-211. https://eccc.weizmann.ac.il/report/2026/211/

van Wamelen, P. (2002). Jacobi sums over finite fields. *Acta Arithmetica, 102*(1), 1–20. https://doi.org/10.4064/aa102-1-1

The Tal attribution concerns the split $\ell\mid p-1$ construction. Bounds for the extension-field divisors of $1+p+p^2$ are not transferred without their hypotheses.
