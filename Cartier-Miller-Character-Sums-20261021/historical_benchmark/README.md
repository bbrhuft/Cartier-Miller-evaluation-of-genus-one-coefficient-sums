# Cartier–Miller prior-work audit and matched-output benchmarks — results package

Prepared 20–21 October 2026 for David Jordan. Unrefereed, AI-assisted. Nothing was published; the supplied manuscript and the inherited archive are unchanged and are included only as read-only inputs.

| Path | Content |
|---|---|
| `EXECUTIVE_REPORT.md` | Two-page summary and recommendation |
| `REPORT.md` | Full report: findings, proofs of the new deductions, comparator mathematics, validation, benchmark results, recommendation, limitations, references |
| `SOURCE_LEDGER.md` | Primary-source ledger (what was read, version, pages, claims; unread items) |
| `COMPARISON_MATRIX.md` | Classification of prior constructions against the target scalar |
| `CORRECTIONS_RESOLUTION.md`, `CHANGE_LOG.md` | Gate-by-gate resolution and itemized text changes |
| `manuscript/PROPOSED_APPLICATION_SECTION_CORRECTED.tex` | Corrected proposed section (+ stand-alone wrapper and compiled PDF) |
| `code/` | Frozen comparator package `cmbench/`, native C kernels, validation suites, benchmark harness, analysis, post-freeze source-audit checks |
| `code/FREEZE.json` | Freeze of the implementations (digest `09202ac1…28ac0`); `verify_freeze.py` |
| `results/handover/` | Outputs of the supplied `verify_handover.py` (plain and `--with-opus`) |
| `results/validation/` | Development, confirmation, Harvey-kernel and source-audit check outputs (JSON) |
| `results/bench/` | Raw timing samples (`timing_samples.csv`, validated copy `timing_samples_validated.csv`), per-job outputs (`outputs/`; group ids containing `/` appear as subdirectories), regenerated case pools (`cases_regenerated.json`), W7 pools, output validation, logs (`bench.log`, `bench_resume.log`), metadata (`bench_meta.json`) |
| `results/bench_quick/` | Pre-run smoke test of the harness (`bench.py --quick`); not used in any reported result |
| `results/analysis/` | `tables.md`, `summary.json`, `plots/` (each plot carries its source CSV hash) |
| `results/environment.json` | Software and hardware record |
| `sources/kernel_src/` | Saved source files of the BGS kernel (hypellfrob) and FLINT/python-flint routines, with hashes in SOURCE_LEDGER.md |
| `inputs/` | The handover ZIP as received (read-only) |
| `SHA256SUMS.txt` | Hashes of every file in this package |

## Rebuilding and rerunning

Requirements: Linux x86-64, Python ≥ 3.10 (3.13.16 used), gcc, and:

```
pip install python-flint==0.9.0 cypari2==2.2.4 numpy matplotlib
python3 -m venv venv_sage && venv_sage/bin/pip install passagemath-ntl==10.8.13 passagemath-modules \
    passagemath-flint passagemath-linbox passagemath-pari passagemath-schemes      # Harvey kernel only
cd code/cmbench/native && gcc -O2 -fPIC -shared -o libcmnative.so cmnative.c && cd ../..
```

The prebuilt `libcmnative.so` is part of the freeze. A rebuild with another compiler changes its hash; record that if you rebuild.

Environment variables:

* `CM_INHERITED_SRC` = path to `src/` of a fresh extraction of `inputs/…/inherited/Opus_Character_Sums_20261020.zip` (`verify_handover.py --with-opus` shows the safe extraction).
* `CM_HANDOVER_COMPARATORS` = path to the handover `comparators/`.
* `CMBENCH_SAGE_PYTHON` = the passagemath interpreter. The default is `../../venv_sage/bin/python` relative to `code/`.

```
cd code
python3 -I verify_freeze.py
python3 -I run_validate.py --mode development --seed 20261020-dev --out ../results/validation/development.json
python3 -I make_harvey_refs.py --seed 20261020-dev --label development --out ../results/validation/harvey_refs_development.json
$CMBENCH_SAGE_PYTHON run_validate_harvey.py --mode development --seed 20261020-dev \
    --refs ../results/validation/harvey_refs_development.json --out ../results/validation/harvey_development.json
D=$(python3 -c "import json;print(json.load(open('FREEZE.json'))['digest'])")
python3 -I run_validate.py --mode confirmation --seed $D --out ../results/validation/confirmation.json
python3 -I make_harvey_refs.py --seed $D --label confirmation --out ../results/validation/harvey_refs_confirmation.json
$CMBENCH_SAGE_PYTHON run_validate_harvey.py --mode confirmation --seed $D \
    --refs ../results/validation/harvey_refs_confirmation.json --out ../results/validation/harvey_confirmation.json
python3 -I make_w7_pools.py ../results/bench/w7_pools.json
python3 -I bench.py --workloads TRACE,W1,W7,W2,W3,W4,W6,W5 --out ../results/bench      # ~2-3 h on 2 vCPUs
# The recorded run was cut by a host restart during W5 (21 Oct ~02:13, before bench.py wrote its pools and
# metadata).  resume_after_restart.py runs only the missing (group, method) jobs with the unchanged harness,
# then regenerates the deterministic case pools (cases_regenerated.json) and bench_meta.json.
# An uninterrupted bench.py run writes cases_*.json itself and needs neither step.
python3 -I resume_after_restart.py ../results/bench resume
python3 -I resume_after_restart.py ../results/bench cases
python3 -I validate_outputs.py ../results/bench
python3 -I validate_w4_internal.py ../results/bench        # internal check of the one-family 62-bit W4 outputs
python3 -I analyze.py ../results/bench ../results/analysis
# source-audit checks (post-freeze, separately hashed)
python3 -I source_audit/voloch_semaev_normalization.py --max-p 60 --out ../results/validation/voloch_semaev_normalization.json
python3 -I source_audit/quartic_adapter_check.py ../results/validation/quartic_adapter_check.json
VZ_EXP=1 python3 -I source_audit/voloch_zeta_general_trace.py ../results/validation/voloch_zeta_general_trace_exp1.json
VZ_EXP=2 python3 -I source_audit/voloch_zeta_general_trace.py ../results/validation/voloch_zeta_general_trace_exp2.json
python3 -I source_audit/voloch_zeta_chain_through_O.py ../results/validation/voloch_zeta_chain_through_O.json
python3 -I source_audit/voloch_zeta_route.py ../results/validation/voloch_zeta_route.json 7
python3 -I source_audit/time_zeta_route.py ../results/validation/zeta_route_timing.json     # exploratory, post-freeze
```

Timings will differ on other machines. Pilot-based repetition counts, budgets and the method order are recomputed deterministically from the benchmark seed and the pilot measurements.
