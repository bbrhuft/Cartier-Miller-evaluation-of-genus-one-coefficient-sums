# Cartier–Miller rounded-third extension handover

David Jordan research project · 18 October 2026 · Research-record snapshot

## Purpose and instructions for the repository maintainer

Use this file to maintain a concise GitHub research record consistent with the revised Cartier–Miller paper. David will upload the revised paper separately. This handover records the extension, its implemented integration, evidence and limits; it is not a replacement manuscript or a complete software distribution. No repository was changed while preparing it.

Read the repository’s current documentation and conventions before editing. Update its existing rounded-third research page, extension ledger and changelog, or propose an equivalent location if none exists. Keep the original genus-one evaluator, its quarter-point application and this extension distinguishable. Preserve earlier reports and their provenance. Reconcile the equation references below against the paper David eventually supplies, using the mathematical statements as the stable identifiers. Do not replace the published paper with an inferred or reconstructed draft. Identify missing companion files explicitly rather than implying their contents have been independently checked.

The strongest supported account is that a certified Jacobi boundary backend has been integrated with the existing Miller prefix and improves complete evaluation on the stated individual-prime inputs. An existing remainder forest is preferable on the tested dense schedules. A uniform polylogarithmic algorithm for the boundary remains open. The work is AI-assisted and unrefereed; “proved” below means proved in the project manuscript or companion, not independently accepted by a specialist.

## Canonical mathematical contract

Let $p\ge11$ be prime with $p\equiv2\pmod3$, and work in $\mathbb F_p$. Set

$$
h=\frac{p-1}{2},\qquad m=\frac{p-2}{3},\qquad L=m+1=\frac{p+1}{3},\qquad
a_i=\binom{2i}{i}8^{-i},\qquad B_j=\sum_{0\le i<j}a_i.
$$

The prefix is strict: $B_L$ excludes $a_L$. The original weighted sum is defined independently by

$$
t_0=1,\qquad t_{i+1}=t_i\frac{h+2+i}{2i+2},\qquad
U_p(j)=\sum_{0\le i<j}(h+1+i)t_i.
$$

The telescoping identity and rounded-third normalization are

$$
U_p(j)=4B_j-2j(2j+5)a_j,\qquad G=m!\bmod p,
$$

$$
a_L=\frac{3}{2G^3},\qquad
G=\left(\frac{3}{2a_L}\right)^{(2p-1)/3},\qquad
a_m=-4a_L,\qquad B_m=B_L+4a_L.
$$

Wilson reflection gives $(2m)!L!=-1$, hence $(2m)!=-3G^{-1}$. Together with $8^m=1/2$ and $a_L/a_m=-1/4$, this proves the boundary formula. Cubing is bijective because $\gcd(3,p-1)=1$, proving the inverse formula. Acquiring $a_L$ and acquiring $G$ are therefore equivalent up to $O(\log p)$ additional field operations. This is a reduction, not an intractability theorem.

The complete and adjacent outputs satisfy

$$
U_p(L)=4B_L-\frac{17}{3}G^{-3},\qquad
U_p(m)=4B_L-\frac{16}{3}G^{-3},\qquad
U_p(L)-U_p(m)=-\frac13G^{-3}\ne0.
$$

Thus the two sums cannot vanish simultaneously. Individual nonvanishing for all admissible primes is not proved. At $p=17$, $2L(2L+5)=34/9=0$ in the field and $U_{17}(6)=4B_6$. A correct weighted sum at that prime does not validate its boundary backend: check $a_L$ and $G$ separately.

These controls were recomputed from integer binomial coefficients, the original weighted recurrence and a direct factorial while preparing this handover. They are small regression inputs, not fresh held-out confirmation. In particular, use these definition-level values when reconciling older conversational examples.

| $p$ | $B_L$ | $a_L$ | $U_p(L)$ | $G$ | $U_p(m)$ |
|---|---|---|---|---|---|
| 11 | 8 | 1 | 5 | 6 | 4 |
| 17 | 6 | 10 | 7 | 1 | 13 |
| 23 | 7 | 9 | 17 | 3 | 19 |
| 29 | 13 | 21 | 21 | 3 | 16 |

## What Cartier–Miller supplies

For $f(w)=1-w^3/2$, the coefficients of $f(w)^h$ at $w^{3i}$ equal $a_i$. Since $3m<p\le3L$, the truncation at degree $p-1$ evaluated at $1$ is exactly $B_L$. Its Hasse coefficient $H=[w^{p-1}]f^h$ is zero. The Hasse–Witt congruence and Hasse bound give exact trace zero; $f(1)=1/2\ne0$ makes the query admissible.

Theorem 1 therefore supplies $B_L$ with $O(\log p)$ field operations, with no point-counting search in this family. The signed boundary $a_L$ is additional arithmetic. The complete single-prime computation combines these outputs through the displayed identities. The logarithmic prefix bound is not a logarithmic bound for the complete rounded-third sum, and field-operation counts are not bit-operation counts.

## Cohomological interpretation and normalization

Use $E:y^2=x^3+1/4$, obtained by $x=-w/2$, $y=v/2$. In this subsection the origin is infinity and $\omega=dx/y$; this equals $-dw/v$ under the change of coordinates. It differs from $dx/(2y)$ as well. Differential scale, origin and signs must accompany any copied formula.

Write $F=x^3+1/4$ and $F^h=\mathcal T+x^p\mathcal S$, with $\deg\mathcal T<p$. Let $U=E\setminus\{O\}$ and $W=E\setminus\{(0,1/2),(0,-1/2)\}$. With the Čech convention $\alpha_U-\alpha_W=dg$, use

$$
e_1=[(\omega,\omega,0)],\qquad
e_2=\left[\left(x\omega,\frac{\omega}{2x^2},\frac{2y}{x}\right)\right].
$$

Proposition 5 gives a basis $(e_1,e_2)$ and

$$
d(y\mathcal S)=a_L\omega,\qquad
\mathcal C\omega=0,\qquad
\mathcal C(x\omega)=\mathcal C\left(\frac{\omega}{2x^2}\right)=2a_L\omega.
$$

For $V_{\mathcal C}[(\alpha_U,\alpha_W,g)]=[(\mathcal C\alpha_U,\mathcal C\alpha_W,0)]$ and $F_{\mathrm{abs}}[(\alpha_U,\alpha_W,g)]=[(0,0,g^p)]$, columns representing images give

$$
[V_{\mathcal C}]=\begin{pmatrix}0&2a_L\\0&0\end{pmatrix},\qquad
[F_{\mathrm{abs}}]=\begin{pmatrix}0&-2a_L\\0&0\end{pmatrix}.
$$

These are $\mathbb F_p$-linear maps with the specified conventions; extension-field semilinearity needs separate conventions. The nonzero scalar $2a_L=3G^{-3}$ belongs to full de Rham cohomology, whereas the Cartier–Manin matrix on regular differentials alone is zero. The rational primitive has poles, so function-field exactness does not give global exactness on the projective curve. The companion supplies the regularity and basis arguments. This interpretation does not extract the scalar efficiently and supplies no impossibility theorem for a future extraction method.

## Implemented acquisition and workload selection

The standalone adapter `integrated.py` uses `RoundedThirdSession`, the retained `BoundaryEvaluator` registry and `complete_sum`. Its unchanged `ThirdPointPrefixProvider` supplies $B_L$. The public adapter checks primality in the implemented range $11\le p<2^{63}$, $p\equiv5\pmod6$, and returns $B_L,a_L,U_p(L),G$, with adjacent outputs and route metadata. The mathematical statements are not restricted to 63-bit primes; this implementation is.

| Route | Acquired quantities and scope |
|---|---|
| Native factorial plus Miller | FLINT `n_factorial_fast_mod2_preinv` acquires $G$; the same retained Miller prefix completes the tuple |
| Nodal anchor plus Miller | Exact factorial-ratio anchor evaluated through FLINT block products; independent comparator and fallback |
| Certified T3 plus Miller | Split Jacobi reconstruction, exact certificates and shortened rounded-third anchor intervals acquire the signed boundary |
| Remainder forest | Ordered integer recurrence products acquire prefix and boundary jointly across a prime schedule; no Miller pass |

T3 uses a prime conductor $5\le\ell\le89$ dividing $p-1$, with $k_\ell=(p-1)/\ell$. Forced calls require $k_\ell\ge4$. Jacobi reconstruction in $\mathbb Z[\zeta_\ell]$ is accepted only after algebraic and root-of-unity normalization certificates; $J\overline J=p$ alone is insufficient. Relation plans are checked on use. Approximate interval lengths are $k_\ell/3$ and $k_\ell/6$, or $k_\ell/3$ and $k_\ell/12$ for the available denominator-12 anchor. That anchor uses a factorial index $N=\lfloor(p-5)/12\rfloor$ or $5N+2$; it does not require $12\mid p-1$.

Automatic mode uses native factorial below $10^7$. Above it, a frozen cost model ranks eligible conductors with $k_\ell\ge10^4$ and attempts T3 when predicted cheaper than nodal acquisition. Uncertified reconstructions are recorded and skipped; nodal acquisition is the final fallback. Forced T3 fails explicitly if certification fails. Exact acceptance is established by the supplied certificates; reconstruction success on every input is not proved. The integrated route needs neither class numbers, PARI nor GRH. Earlier class-number-dependent half-interval results describe a different route and must not be merged into these timings.

For fixed conductor the interval work retains square-root dependence on $p$, up to logarithmic and multiplication factors. The threshold is a tested implementation policy, not a universal crossover or a new exponent bound. Tal attribution here concerns the split $\ell\mid p-1$ construction; do not transfer bounds from his extension-field divisors of $1+p+p^2$ without their hypotheses.

The forest uses $\Delta_j=4^j j!$, $\widehat B_j=\Delta_jB_j$, $\widehat a_j=\Delta_ja_j$ and

$$
\mathsf A_j=\begin{pmatrix}4(j+1)&4(j+1)\\0&2j+1\end{pmatrix},\qquad
\mathsf A_{j-1}\cdots\mathsf A_0=
\begin{pmatrix}\Delta_j&\widehat B_j\\0&\widehat a_j\end{pmatrix}.
$$

The order of multiplication matters. At $j=L<p$, divide by the nonzero $\Delta_L$, and recover $G=\Delta_L/(4^LL)$. Product and remainder trees share recurrence work across primes; a forest processes smaller trees with a reduced carry to control storage. Its improvement is established batch amortization specialized to this recurrence. Sparse schedules still pay for products from index zero. The adapter does not automatically update the existing GUI or many-prime dispatcher.

## Evidence and defensible performance claims

The integration candidate was internally hash-frozen on 18 October 2026 at 08:09:50 UTC, before confirmation selection. The freeze covers 196 source, evidence and vendor files; it has no external timestamp. Its preserved-source and final-manifest audit passed again during this handover. No new full benchmark or large-prime confirmation was run for this handover.

| Evidence class | Recorded result and qualification |
|---|---|
| Earlier companion | 152 admissible primes below 2,000; 595 reconstructed conductor values checked against direct character enumeration; separate inherited factorial and batch checks |
| Integration development | All 1,135 admissible primes below 20,000; 3,405 complete method comparisons, 1,135 independent binomial checks, 1,135 independent elliptic-prefix comparisons, 200 forced T3 checks; invalid inputs, $p=17$, injected misses and three forest chunk counts checked |
| Fresh confirmation | 17 distinct primes excluded from the recorded prior ledgers, reaching 7,000,000,009,553; independent prefix code and native/nodal boundary comparisons throughout; direct linear weighted-sum controls only on the three approximately five-million inputs |
| Exploratory survey | All 39,264 admissible primes below one million; zero observed individual or simultaneous zeros; independent definition-level checks for all 1,135 rows below 20,000 and 64 seeded larger rows; remaining rows had internal residual checks |
| Timing experiment | Twelve individual primes, three dense bounds and one sixteen-prime sparse schedule; complete matched outputs; three rotated samples per method |

At the largest confirmation prime the tuple $(B_L,a_L,U_p(L),G)$ is $(4770090998586,303509152059,6267107181755,2406416797142)$. This approximately 43-bit correctness check is not a timing benchmark or evidence of cryptographic-size practicality. The million-bound survey is exploratory evidence on a previously studied range, not disjoint confirmation or a universal nonvanishing result. The review AI’s additional unprovided test counts were not promoted to independently verified evidence.

| Workload | Complete median runtimes in seconds | Interpretation |
|---|---|---|
| One prime 700,000,001,633; T3 conductor 47 | Native + Miller: 5.833161; nodal + Miller: 4.760048; automatic + Miller: 0.895216 | 6.52× over native; Miller accounts for about 0.48% of the new runtime |
| Every admissible prime below 100,000; 4,805 tuples | Native + Miller: 6.677996; automatic: 6.652261; Python forest: 0.157454; GMP forest: 0.057797 | About 115.5× native/GMP-forest; batch gain, not a faster Miller query |
| Recorded sixteen-prime schedule from 1,000,211 to 2,501,171 | Native: 0.037191; automatic: 0.037016; forced T3: 0.039155; GMP forest: 0.689112 | Forest about 18.5× slower than native; forced T3 does not help this workload |

Across the nine individual inputs selecting T3, native/automatic median speedups were 1.67–6.52×. The other three selected nodal fallback; their gains are not T3 gains. For the strongest row, observed native and automatic ranges were [5.831019, 5.857249] and [0.868507, 0.900682] seconds. The paper reports the remaining observed ranges; raw samples are in `evidence/BENCHMARK.json`. These ranges are descriptive, not confidence intervals.

The host was Linux x86-64, AMD EPYC 9V74, Python 3.12.14, python-flint 0.9.0/FLINT 3.6.0 and gmpy2 2.3.2/GMP 6.3.0. CPU frequency and scheduling were uncontrolled. Single-prime timings charge primality checks, registry/provider setup, conductor discovery, reconstruction and certification, products, normalization, Miller and collection; imports and prime selection are excluded. Dense timings also charge sieving and tuple hashing but exclude disk I/O. Prime-independent plan tables or library handles can remain loaded. No complete output is cached. The Linux shared-library bridge has no validated Windows or future-ABI portability.

No matched comparison was made with unmodified Tal reconstruction, an optimized compiled forest, the earlier project Jacobi backend or complete PARI/SageMath/Magma systems. Do not describe these results as globally fastest, a new complexity exponent or a guaranteed gain above a particular prime threshold.

## Paper synchronization map

The source snapshot is `Cartier_Miller_Paper_Reviewed_20261018.md`, revision following technical review. Its exact-byte SHA-256 is `561e8427a7b1de5e09a0dbc719601b59a7ca26731eac40d5be2b957b09fffd51`. Library text retrieval omits the final newline; the local saved source has it. Treat these equation numbers as version-specific.

| Research statement | Reviewed paper location |
|---|---|
| Weighted-sum definitions and telescoping identity | Equations (37)–(40) |
| Factorial/boundary equivalence | Rounded-third section, equation (43) |
| Specified de Rham basis and matrices | Proposition 5, equations (44)–(46) |
| Adjacent cutoff and nonzero difference | Equations (47)–(48) and following text |
| Joint forest recurrence | Equation (49) |
| Workload distinctions | Table 3 |
| Complete single-prime, dense and sparse measurements | Appendix, Tables 5–7 |

Older sources use `q`, `K`, `D_j`, `M_j`, `T` and `S` for the conductor, grid step, cleared denominator, recurrence matrix and cubic-power parts. The reviewed paper uses $\ell,k_\ell,\Delta_j,\mathsf A_j,\mathcal T,\mathcal S$. Retain actual API names such as `--q`; do not silently change code interfaces to match prose notation. Older labels RT1–RT6 map respectively to (43), (44), (45), (46), (48), (49). Equation (47) is the separately numbered adjacent-cutoff display.

## Source package and reproducibility

The implementation/evidence archive is `Cartier_Miller_T3_Integration_20261018.zip`; its accompanying report is `Cartier_Miller_T3_Integration_REPORT_20261018.md`. The report SHA-256 is `00a73b60ed6a1f673330876d7b882760b9ef3390084dbd9cdb2f14dd52fce2d1`. Request the archive from David if it is absent; this compact file cannot reproduce its certificate implementation. Preserve `vendor/`, `provenance/`, `CANDIDATE.md`, `evidence/FREEZE.json` and `MANIFEST.json` when importing the package.

`MATHEMATICS.md` records the elementary identities, and `provenance/RETAINED_NORMALIZED_PROPOSITION.md` and `provenance/RETAINED_BATCH_PROOF.md` retain the normalization and batch proofs. `integrated.py` is the API/CLI, `oracles.py` contains independent controls, `experiment.py` generates evidence, and `audit.py` verifies recorded hashes. `evidence/DEVELOPMENT.json`, `CONFIRMATION.json`, `BENCHMARK.json`, `SURVEY.json` and `SURVEY.csv` distinguish the evidence classes above. `requirements.txt` pins executed dependency versions.

Run from the extracted package directory in its supported environment, without Python’s `-O` flag because the retained prefix uses assertions:

```console
python -m pip install -r requirements.txt
python audit.py
python integrated.py 700000001633
python integrated.py 700000001633 --method native
python integrated.py 700000001633 --method t3 --q 47
```

Reproduction commands are `python develop.py`, `python experiment.py confirm`, `python experiment.py benchmark` and `python experiment.py survey`. Reruns overwrite generated evidence and change hashes; archive the recorded evidence first, run benchmarks and surveys separately, and regenerate only the final manifest when appropriate. Never rewrite an original freeze to conceal differences. Repeated confirmation inputs remain repeated evidence.

## Status and next research question

The factorial reduction and transfer to the complete weighted sum are proved project results; the Jacobi reconstruction and remainder-forest frameworks are prior work. The specific certified anchor specialization, registry integration, unconditional fallback, complete-output confirmation and matched measurements are the practical increment recorded here. The project’s reported selected-coefficient, local-jet and fixed-dimensional global-recurrence investigations did not supply a uniform polylogarithmic signed-scale extractor. An unsuccessful search is not a general impossibility theorem.

The precise next algorithmic question is whether guaranteed reconstruction at larger conductors can reduce the remaining interval work without its setup cost erasing the saving. A matched unmodified-Tal comparison, wider reproducible timing study, production workload dispatcher and portability work remain useful implementation tasks. The characteristic-$p$ proof does not establish evaluation modulo $p^2$.

For repository synchronization, retain the distinction between manuscript proofs, certified computations, finite observations and open questions in every summary. Link authentic companion files and commits when available. A persistent public archive/DOI and a completed specialist novelty audit remain outstanding for this integration package. David’s later paper upload should trigger a statement-by-statement reconciliation and an updated revision/hash record, rather than retrospective alteration of frozen experimental evidence.

## Primary antecedents named in the paper

Harvey, D., & Sutherland, A. V. (2016). Computing Hasse–Witt matrices of hyperelliptic curves in average polynomial time, II. In *Frobenius distributions: Lang–Trotter and Sato–Tate conjectures* (Contemporary Mathematics, Vol. 663). American Mathematical Society. <https://doi.org/10.1090/conm/663/13352>

Tal, Y. (2026). *Computing modular factorials below the square-root barrier* [Unrefereed preprint]. ECCC TR26-211. <https://eccc.weizmann.ac.il/report/2026/211/>

van Wamelen, P. (2002). Jacobi sums over finite fields. *Acta Arithmetica, 102*(1), 1–20. <https://doi.org/10.4064/aa102-1-1>
