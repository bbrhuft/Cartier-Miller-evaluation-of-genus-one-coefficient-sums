# Atkin endpoint study, round 2

Start with `REPORT.md` for results, proofs, status labels and limits. `OPUS_HANDOVER.md` is a ready-to-paste continuation prompt. Round-1 documents are kept unchanged under `provenance/`. The round-1 frozen candidate (`CANDIDATE.md`, `evidence/FREEZE.json`) is untouched and still verifies.

```bash
python3 audit.py                         # verifies both freezes and MANIFEST.json
python3 acquire_charp.py 2000000063      # half-interval c_p and A_n'(0), stdlib only
python3 acquire_charp.py 200000000171 --backend flint --classno pari
python3 develop_charp.py && python3 confirm_charp.py && python3 benchmark_charp.py
```

## Files

| Files | Role |
|---|---|
| `atkin.py`, `vendor/` | Round-1 core: Atkin recurrence, Wronskian product, nodal anchor, shared block engine. Frozen in round 1 |
| `charp.py` | Round-2 core (stdlib): class numbers by reduced forms, the routes for ((p−1)/2)!, half-interval c_p = 2HP³ |
| `flint_backend.py` | Optional optimized comparator through ctypes on the libflint bundled with python-flint: FLINT native factorial and a FLINT block engine with a shared evaluation tree |
| `CANDIDATE_CHARP.md`, `evidence/charp/FREEZE_CHARP.json` | Round-2 frozen statements, rules and source hashes, written before confirmation selection |
| `develop_charp.py`, `confirm_charp.py`, `benchmark_charp.py` | Round-2 development, frozen confirmation and matched benchmark runners |
| `acquire_charp.py` | Thin round-2 API. Rows for p ≡ 17 (mod 24) are flagged as conditional on conjecture (\*) |
| `research/` | C7 lattice evidence (needs python-flint and sympy), post-freeze proof-support checks, and independent round-1 audit scripts |
| `evidence/charp/` | Round-2 raw evidence: development, lattice, freeze, confirmation, benchmark, API check, post-freeze checks and audit outputs |

## Dependencies and contracts

- The production core needs only the standard library (Python 3.10+).
- The comparator needs `python-flint`, PARI class numbers need `cypari2`, and the research scripts also need `sympy`.
- Prime certification is the caller's input contract.
- PARI's `quadclassunit` is GRH-conditional. The stdlib class-number count is unconditional but costs O(|D|^{1/2}).

No result here changes the O(M(√p) log p) exponent. All gains are constant factors for the stated implementations.
