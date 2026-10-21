# Cartier–Miller character and elliptic-point sums

This folder holds the rationally weighted quadratic-character-sum application of Cartier–Miller and its equivalent elliptic-point sums, dated 21 October 2026. It contains the proofs, the frozen evaluator and weighted adapter, their verification records, the primary-source comparison and the historical matched-output benchmark campaign. It came from `Cartier_Miller_Character_Sums_Supplement_20261021.zip`. The live interface is the `charsum` service of the integration layer, [`../Cartier-Miller-Integration-20261013/`](../Cartier-Miller-Integration-20261013/).

**Status:** unrefereed research software and evidence, prepared with substantial generative-AI assistance. The finite checks below support the formulas but do not replace specialist review of the proofs. Publication priority for the combined result is unresolved. No new elliptic-curve discrete-logarithm attack is claimed.

## What is computed

Let $p\ge5$ be prime and let $f\in\mathbb F_p[x]$ be a squarefree cubic or quartic with any constant term. Write $\chi$ for the quadratic character, with $\chi(0)=0$, and $\tau_f$ for the exact signed trace of the smooth projective curve $y^2=f(x)$. For a nonbranch pole $a$, so that $f(a)\ne0$, the single-pole output is the residue

$$
C_f(a)=\sum_{x\in\mathbb F_p,\ x\ne a}\frac{\chi(f(x))}{x-a}\in\mathbb F_p .
$$

Put $e=\chi(f(a))$, $g(z)=f(a+z)/f(a)$, $g_1=f'(a)/f(a)$ and $N=p+1-e\tau_f$, which is the number of rational points of the normalized twist. On the short model of $v^2=g(z)$ with origin $(0,1)$, let $R$ be the image of $(0,-1)$. Then

$$
C_f(a)=e\left(-\frac{g_1}{4}(N-2)-\frac{\alpha_N(R)}{2}\right),
$$

where $\alpha_N(R)$ is the Laurent constant at the origin of $d\log f_{N,R}$, and $f_{N,R}$ is the Miller function with divisor $N(R)-([N]R)-(N-1)(O)$. The formula rests on the identity $\alpha_{\#E(\mathbb F_p)}(P)=Y(P)V_W(X(P))$, proved in [`proofs/UNIFORM_ORDER_PROOF.md`](proofs/UNIFORM_ORDER_PROOF.md). It holds for every trace, including the anomalous and supersingular cases, rational two-torsion and $p=5$. It needs no square root and no inversion of $p$ modulo $N$, and one differentiated Miller chain computes it.

For a complete excluded set $U=\{a_1,\dots,a_s\}$, residues $r_i$ and a constant $c$, the prepared adapter returns three sums of the weight $R(x)=c+\sum_i r_i/(x-a_i)$:

- $\sum_{x\notin U}R(x)\chi(f(x))$;
- the sum of $R(x(P))$ over the affine rational points with $x(P)\notin U$;
- the projective point sum, which adds $c$ for each rational point at infinity. A cubic has one such point and a quartic has $1+\chi(\text{leading coefficient})$; no character value is assigned at infinity.

Every $a_i$ stays excluded even when $r_i=0$. A branch coordinate may be excluded, but only with zero residue. The common-domain correction formulas are in [`docs/MATHEMATICS.md`](docs/MATHEMATICS.md). All outputs are residues modulo $p$. They are not integer character sums, interval sums or discrete logarithms.

## Costs and scope

| Step | Cost |
|---|---|
| Exact signed trace | Separately charged, and a caller obligation in the portable API. The `charsum` service can count it directly in $O(p\log p)$ field operations, up to a budget |
| One nonbranch pole | $O(\log p)$ field operations after the trace, which is $O((\log p)^3)$ bit operations with classical arithmetic |
| Preparing $s$ exclusions | $O(s\log p+s^2)$ field operations, $O(s^2)$ temporary storage for the batch-inversion differences and $O(s)$ cached storage |
| Each later coefficient vector on the same set | $O(s)$ field operations |

The asymptotically faster polynomial-tree correction is proved in the manuscript but not implemented or measured here. Primality is also a caller obligation in the portable API, while the `charsum` service tests it deterministically below $2^{64}$. A Hasse-interval check or a Miller endpoint check does not certify a supplied trace.

The fast adapter does not cover active branch poles, higher-order poles, polynomial parts, nonrational poles or unfactored denominators, and none of these inherits the logarithmic bound. The historical framework in `historical_benchmark/inherited/` has bounded experiments on some of them. The trace-free selected-coefficient route of Bostan–Gaudry–Schost and Harvey covers branch poles with a different cost model, $\widetilde O(\sqrt p)$ for fixed degree.

## Where the code is

| Location | Role |
|---|---|
| `../Cartier-Miller-Integration-20261013/cm_system/character_sums.py` | Live service: `CharacterSumSession(p, coefficients, trace=None)`, `.single_pole(a)`, `.prepare(U).evaluate(residues, constant)`, and the `charsum` command |
| `../Cartier-Miller-Integration-20261013/cm_system/backends/character_sums/` | **Adapted** copies of `cm_character_route.py`, `uniform_order.py` and `weighted_sums.py`. Only their imports differ, and both hashes are recorded in that folder's `PROVENANCE.json` |
| `src/` | **Frozen** copies, byte-identical to the supplement: the three-file uniform-order freeze (`src/FREEZE.json`, digest e5bc2239…) and the weighted adapter |
| `tests/verify_weighted_adapter.py`, `verification/ADAPTER_FREEZE.json` | Adapter checks against direct enumeration and its separate source commitment (digest 8550b778…) |

| Source | Frozen SHA-256 | Adapted SHA-256 |
|---|---|---|
| `cm_character_route.py` | d85cb3f6f0977216e8f23e6fd8c020d0cdd55c8a147dba92881c58b9b5258b89 | identical |
| `uniform_order.py` | 7d1036ad5a2b8b27cf351ece92b073609d242ed497571bd988d29bb00c0a2fb4 | 0c4a248d84ff05bd802375120a117fafcbc02db689169af6ecbc843cd716e5aa |
| `weighted_sums.py` | 8ca4a398b7086caf22c3b3f9052d4e20cd96f3f9fd2779926869989f5bcd771d | c97991c8170800f0c768f677bfa7d180566dd2e71ea30352b08a45867bd9cf41 |

`cm_character_route.value` is the preceding evaluator, kept for comparison. Current single-pole calls go through `uniform_order.value`.

## Examples

Through the integration layer, run from `../Cartier-Miller-Integration-20261013/`:

```python
from cm_system.character_sums import CharacterSumSession

s = CharacterSumSession(7, [1, 1, 0, 1])          # f = 1 + x + x^3; trace counted directly
print(s.single_pole(1)["value"])                 # 0: sum over x != 1
z = s.prepare([1, 2]).evaluate([1, 0])            # same weight 1/(x-1), x = 2 also excluded
print(z["character"], z["affine_points"], z["projective_points"])   # 6 5 5
print(z["status"], "|", z["trace_source"])
```

```bash
python -m cm_system charsum 7 1 1 0 1 --pole 1
python -m cm_system charsum 7 1 1 0 1 --exclude 1 2 --residues 1 0 --constant 4 --trace 3
python -m cm_system charsum 5 0 3 0 1 --pole 1 --trace -4    # p=5, twisted curve order 2p
```

A counted trace is labelled `exact`. A supplied trace is labelled `conditional_on_trusted_trace`. Above `Budget.point_count_prime` (5000 by default) the service refuses to count and asks for an exact trace. A branch pole, or a nonzero residue at an excluded branch coordinate, raises `Unsupported`, which the command reports with exit status 2.

The frozen portable API has no 64-bit limit and leaves primality and the trace to the caller. From this folder:

```python
import sys
sys.path.insert(0, "src")
from weighted_sums import single_pole, prepare_weights

assert single_pole(5, [0, 3, 0, 1], 1, -4) == 1
state = prepare_weights(7, [1, 1, 0, 1], 3, excluded=[1, 2])
answer = state.evaluate([1, 0])
assert (answer.character, answer.affine_points, answer.projective_points) == (6, 5, 5)
```

## Verification

```bash
python verify.py            # about 10 s
python verify.py --full     # also repeats the development selections
python ../Cartier-Miller-Integration-20261013/validate_character_sums.py
```

`verify.py` runs the following checks, using the standard library only and writing to temporary directories:

- it checks every file against `SHA256SUMS.json`, and every supplement file against `MANIFEST.json`;
- it reruns the frozen uniform-order selections and the weighted-adapter selections and requires their outputs to equal the recorded JSON;
- it recomputes the 30 historical benchmark medians from the validated timing CSV;
- it checks both historical implementation freezes and runs the example;
- it runs the integration layer's `validate_character_sums.py`. That script compares the adapted service with an independent enumeration and with the frozen sources, including three supersingular curves at primes of 60–64 bits, and checks every refusal.

| Record | Content |
|---|---|
| `verification/uniform_order/development.json` | 2,762 models, 14,037 direct character-sum values, 47,712 cubic identity checks |
| `verification/uniform_order/confirmation.json` | 360 models, 5,400 values on nine primes disjoint from that verifier's development set |
| `verification/adapter/{development,confirmation}.json` | 120 models, 960 weighted plus 960 cached queries, 5,760 residue comparisons and 12 rejected inputs in each mode |
| `../Cartier-Miller-Integration-20261013/recorded_results/validation_character_sums_20261021.json` | Repository-adapted service: 1,044 single-pole and 1,056 weighted comparisons with enumeration, 600 frozen/adapted agreements and 14 refusals |

`verification/REPOSITORY_CHECK_20261021.json` records `python verify.py --full` in the repository layout, with the data asset extracted. The supplement's own release record is `verification/RELEASE_CHECK.json`. `tools/verify_supplement.py` is the handover's verifier. It needs the complete archive, including the manuscript snapshot that this repository does not redistribute, so `verify.py` is the entry point here. The repository has no CI configuration, and none was added.

## Historical benchmark

[`historical_benchmark/`](historical_benchmark/) preserves the matched-output campaign of 20–21 October 2026. It compared the **older frozen application framework** (`historical_benchmark/inherited/character_sums/src/cmcs.py`) with a Bostan–Gaudry–Schost selected-coefficient adapter through Harvey's interval-product kernel, and with native linear methods. Each comparison returned the same residue $C_f(a)$. The uniform-order engine and the weighted adapter in `src/` were **not** the implementations timed. No timing here describes them or the `charsum` service.

The manuscript's table of cold first-query medians can be recomputed without running a benchmark: `python tools/recompute_benchmark_table.py`. The source values are in `verification/BENCHMARK_TABLE_SOURCE.json`, and the full tables are in `historical_benchmark/results/analysis/tables.md`. Any summary of these measurements carries the following qualifications:

- **Host and run.** The measurements come from named implementations on one uncontrolled two-vCPU virtual machine. A host restart interrupted the last workload, and only the missing jobs were rerun with the unchanged harness. The case pools and run metadata were then regenerated deterministically.
- **Memory.** Thirteen polynomial and multipoint jobs exceeded the declared 512 MiB working-memory target, which was not enforced at run time.
- **Size ceiling.** No square-root comparator was run above its declared 40-bit ceiling.
- **Trace.** The cold Cartier–Miller timings include a PARI trace computed by its CM or baby-step giant-step paths, not a measured SEA or Schoof provider. At 62 bits the trace accounts for 87–92% of the median. Separate known-trace (`trace_supplied`) and exceptional-input adapters are reported as their own methods.
- **Crossovers.** These depend on the workload. Native linear methods win at 10 bits. Reuse favours polynomial methods for dense queries on small curves, and the trace-free route is preferable for branch poles.

The case pools, raw timing samples and per-job outputs are kept out of git; see [Data asset](#data-asset). [`docs/BENCHMARK_REPRODUCTION.md`](docs/BENCHMARK_REPRODUCTION.md) gives the optional dependencies and the reproduction commands. A fresh campaign takes several hours, is not part of any normal check, and needs packages that the correctness checks do not.

## Data asset

The repository does not track compiled binaries, and its folders stay compact. 657 supplement files, 127 MB uncompressed, are therefore kept in a separate archive, `Cartier-Miller-Character-Sums-20261021-data.zip` (51 MB, SHA-256 c830d9ac381ebfd4d01550c663fcd7872a51415b58119223d2dbb74ffce2328c). The archive is intended for the release tagged `character-sums-data-20261021`. Unzip it at the repository root. [`DATA_ASSET.json`](DATA_ASSET.json) lists every file with its hash and the reason it was kept out of git:

- 650 raw per-job outputs, 92 MB;
- the regenerated case pools, 29 MB;
- the unvalidated raw timing CSV;
- the 20 KB native library `libcmnative.so`, which is part of the comparator freeze;
- two nested archives, kept as received;
- two manuscript-source files.

Once the archive is extracted, `verify.py` checks those hashes and the full comparator freeze digest 09202ac1…. Without it, `verify.py` checks every other frozen file. The validated timing CSV, analysis, plots, validation reports and all code stay in the tree. The two benchmark logs in `historical_benchmark/results/bench/` are committed although the repository ignores `*.log`, because the manifests cover them.

The manuscript snapshot and the separate replacement prior-work section are not redistributed. Their hashes are recorded under `not_redistributed`.

## Attribution

The constructions are classical, and the manuscript's prior-work section and [`docs/PRIMARY_SOURCE_GUIDE.md`](docs/PRIMARY_SOURCE_GUIDE.md) give the details:

- **Miller.** Short programs for functions with prescribed divisors come from Miller's manuscript of 6 May 1986. Their divisor, addition and composition identities are expounded in Miller (2004, Section 4.1), and the uniform-order proof uses them.
- **Semaev (1998).** The differentiated Miller evaluation of the order-$p$ logarithmic transfer.
- **Rück (1999, p. 806).** The local-coefficient cocycle.
- **Earlier Cartier and high-block sources.** Cartier (1957), Serre (1958), Deuring (1941) through Voloch (1990, 1997), Cassels (1971) and Gunji (1976).

This project derives the complete trace-supplied scalar and weighted-sum formulas, with their adapters and costs. The bounded source comparison in [`proofs/SOURCE_LEDGER_FINAL.md`](proofs/SOURCE_LEDGER_FINAL.md) did not locate that combined result. It establishes neither its priority nor its prior publication.

## Status of the documents

[`docs/STATUS_AND_PROVENANCE.md`](docs/STATUS_AND_PROVENANCE.md) ranks the material, and its ranking overrides stronger statements in older reports. The current results are `proofs/UNIFORM_ORDER_PROOF.md`, the uniform-order freeze and the weighted adapter. `proofs/FOUNDATION_PROOFS.md` keeps the detailed Cartier, model-change and identity-step arguments, but its case-split evaluator is superseded.

`history/` and `historical_benchmark/REPORT.md` and `EXECUTIVE_REPORT.md` are retained for provenance. They contain superseded algorithm branches, earlier source-access gaps and historical novelty recommendations. The manuscript's main theorem keeps its $p\ge7$ statement, and its character-sum theorem separately proves the $p\ge5$ extension. The earlier $p=5$ failure lay outside the older report's theorem range.

`handover/SUPPLEMENT_README.md`, `NOTICE.md` and `OPUS_HANDOVER_PROMPT.md` are the supplement's own texts. Their layout notes describe the handover, not this repository.

## Licence

The author's code, data and documents in this folder are under the MIT [`LICENSE`](LICENSE). The inherited `cm_system` copy in `historical_benchmark/inherited/character_sums/vendor/` keeps its own MIT notice, `cm_system_LICENSE`. External benchmark libraries are runtime dependencies and are not bundled. They include python-flint, cypari2 and passagemath, whose Harvey kernel is GPL. The two manuscript-source files in the data asset remain the author's manuscript material under its own terms. No third-party paper texts are redistributed.
