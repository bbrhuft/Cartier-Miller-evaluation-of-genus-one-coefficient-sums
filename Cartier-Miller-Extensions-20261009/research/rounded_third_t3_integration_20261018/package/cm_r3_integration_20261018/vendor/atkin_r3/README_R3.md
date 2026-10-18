# Atkin endpoint, round 3 package

Start with `REPORT_R3.md`. It supersedes the round-2 `REPORT.md`, which is kept unchanged. Every round-1 and round-2 file is byte-identical to the round-2 archive. All round-3 material is new: `CANDIDATE_R3.md` and `CANDIDATE_R3_1.md` at the top level, and everything under `r3/`.

## Requirements

Python 3.10 or later, plus `pip install python-flint==0.9.0 cypari2 sympy`. The measured environment was Python 3.13.16, FLINT 3.6.0 and PARI 2.17.2. `python-flint` supplies the FLINT library, used through ctypes for the block engine and native factorials, and FLINT's LLL. `cypari2` supplies PARI class numbers and the HNF used to build relation plans.

## Commands

| Command | Purpose |
|---|---|
| `python3 audit.py` | inherited audit of the round-1 and round-2 freezes and manifest |
| `python3 r3/audit_r3.py` | inherited audit, both round-3 freezes and the round-3 manifest |
| `python3 -m r3.acquire_r31 P` | signed a_L, c_p, m!, D with route and status labels |
| `python3 r3/confirm_r3_1.py` | frozen R3.1 confirmation, about 20 min |
| `python3 r3/benchmark_r3_1.py` | frozen benchmarks, about 40 min; timings will differ |
| `python3 r3/research/wc_lemma14c_check.py 1000000 200000 OUT.json` | Williams–Currie development check |
| `python3 r3/research/quarter_sign.py 1000000 OUT.json` | quarter-sign experiment |
| `python3 r3/research/c6_audit.py OUT.json` | exact re-check of Theorem C6 |
| `python3 r3/research/dev_checks.py OUT.json` | archived development checks quoted in the report, about 1 min |

## Map of r3/

| File | Content |
|---|---|
| `common.py` | primality, class-number policy (unconditional, GRH, forms), FLINT references |
| `jacobi.py` (R3, frozen) | Jacobi sums: Stickelberger ideal, LLL, certificate, van Wamelen selection |
| `jacobi_r31.py` (R3.1) | repaired lattice chain |
| `tal3.py` | the rounded-third Tal split specialization (T3); `PLANS_R3.json` holds its p-independent plans |
| `halfint.py` | half-interval route with the Williams–Currie theorem |
| `acquire_r3.py` / `acquire_r31.py` | interfaces (R3 frozen; R3.1 is the one to use) |
| `POLICY_R3.json` / `POLICY_R3_1.json` | frozen selection constants |
| `confirm_r3.py`, `benchmark_r3.py` | frozen R3 rules |
| `confirm_r3_1.py`, `benchmark_r3_1.py` | R3.1 rules |
| `FREEZE_R3.json`, `FREEZE_R3_1.json`, `MANIFEST_R3.json` | hash commitments |
| `evidence/` | development, confirmation (including the failed run 1), benchmarks, ledgers |
| `research/` | development and audit scripts |
| `sources/` | the installed PARI documentation text |

Prime certification is the caller's contract; `r3.common.is_prime` is a deterministic proof below 3.3·10^24.
