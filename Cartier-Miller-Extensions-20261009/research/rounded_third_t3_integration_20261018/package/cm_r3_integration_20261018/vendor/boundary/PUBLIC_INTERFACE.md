# Public interface: 1.0.0rc1

`cartier_miller.py` is the consolidated import and command entry point.
The earlier modules remain available. This facade delegates their existing
interfaces and does not silently convert a boundary request into a prefix
calculation or a modulo-p request into a prime-power calculation.

## Python imports

```python
from cartier_miller import (
    BoundaryRequest, BoundaryEvaluator, BoundaryBatchSession,
    ThirdPointSession, FifthPointSession,
    ManyPrimeEvaluator, PrimeQuery, range_queries, calibrate,
)

assert ThirdPointSession(23).evaluate()["U_p_L"] == 17
assert [r["U_p_L"] for r in FifthPointSession(29).evaluate()["outputs"]] == [8, 10]

batch = BoundaryBatchSession(59).evaluate([6, 12, 24, 20, 6], backend="bgs")
assert batch["values"] == [14, 5, 30, 6, 14]

queries = [PrimeQuery(17, 6), PrimeQuery(19, 8), PrimeQuery(17, 6)]
many = ManyPrimeEvaluator().evaluate(queries, engine="independent")
assert [r["U_p_L"] for r in many["outputs"]] == [7, 13, 7]
```

| Export | Contract |
|---|---|
| BoundaryRequest / BoundaryEvaluator / BoundaryResult | One boundary a_L; third/generic reductions, registry support and exact backend diagnostics |
| BoundaryBatchSession | Boundary-only mixed batches at one prime, including fifth reductions; optional complete_many with a supported strict-prefix provider |
| ThirdPointSession / ThirdPointPrefixProvider | One supported native ordinary/rounded third; ordinary trace reuse retained |
| FifthPointSession / FifthBoundaryEvaluator | One or both supported fifth indices; paired work shared |
| PrimeQuery / ManyPrimeEvaluator / range_queries | Many-prime complete outputs, explicit forest/independent routes and opt-in exact measured dispatch |
| calibrate | Explicit local profile training with definition-level output checks |
| PrefixProvider / DirectReferencePrefix / SuppliedPrefix / complete_sum | Existing strict-prefix extension contract; supplied values retain their unverified label |
| DirectFactorialBackend / ProductTreeFactorialBackend / BGSFactorialBackend | Low-level kernels expect an already validated prime |
| BoundaryError / ResourceLimitError / UnsupportedPrefixError | Public exception types |
| __version__ | Release identifier |

Keyword arguments, return structures and timing definitions are those in the
underlying documented services. Results are canonical residues. The facade
does not confer independent certification on custom providers or backends.

## Commands

| Command | Delegated interface |
|---|---|
| `python cartier_miller.py boundary ...` | Existing single-boundary CLI |
| `python cartier_miller.py boundaries ...` | Shared boundary batches; use --indices |
| `python cartier_miller.py third ...` | Native complete third |
| `python cartier_miller.py fifth ...` | Native complete fifth selection/pair |
| `python cartier_miller.py many ...` | Many-prime JSON or unique streamed CSV |
| `python cartier_miller.py calibrate ...` | Explicit workload calibration |
| `python cartier_miller.py validate --output PATH` | Mathematical and interface regression suite |
| `python cartier_miller.py check ...` | Runtime integrity plus reproducible release evidence |

Append `--help` after a command to see that service's full options. Numeric
commands preserve the old JSON/status behavior; argument-parser errors use
standard argparse exit status 2. The check command additionally prints
progress and a final evidence location. It returns 1 for failed checks and
2 for invalid runner setup. It is not a pure-JSON streaming endpoint.

```console
python cartier_miller.py third --p 17
python cartier_miller.py fifth --p 29 --output-mode u_only
python cartier_miller.py boundaries --p 59 --indices 6 12 24 20 6 --backend bgs
python cartier_miller.py many --bound 20000 --family rounded_third --chunks 32 --out rounded_thirds.csv
python cartier_miller.py check --benchmarks smoke
```

## Domain and output distinctions

| Path | Supported indices/quantities |
|---|---|
| General boundary | Odd prime p<2**64, 0<=L<p; a_L only without a provider |
| Native ordinary third | p>=7, p=1 mod 3; L=(p-1)/3 |
| Native rounded third | p>=11, p=2 mod 3; L=(p+1)/3 |
| Native fifths | p>=19, p=4 mod 5; L=(p+1)/5 and 2L |
| Many-prime forest | Valid arbitrary (p,L) pairs within explicit resource guards; complete B/a/U by an amortized integer recurrence |
| Independent many-prime route | Native stopping points where supported; labeled direct-reference prefix otherwise |

Everything in this release is modulo p. Fast arbitrary-index *boundaries*
do not imply a fast isolated-prime arbitrary prefix. A forest can supply
general prefixes amortized across queries, but sparse high-cutoff queries
can be much slower than a native stopping-point call.

The collecting many-prime API preserves input order and duplicates. The
iterator and CSV contract emits unique queries in the documented execution
order. Shared single-prime batches preserve order and duplicates. U-only
fields are null/empty rather than zero. The forest labels boundary work
computed_jointly; native services retain actual separate-acquisition skipping.

Automatic engine selection is opt-in. A profile must match the exact ordered
requests, output/collection contract, source version, machine signature and
configuration. Unknown workloads use a labeled independent fallback, which
still obeys its normal resource limits. Explicit engines bypass profiles.
The existing default many-prime engine remains forest.

## Reproducible evidence

`release_check.bat` runs the default validation and facade smoke checks on
Windows. `run_checks.bat` runs the full eight-suite benchmark capture.
Equivalent commands work with standard Python on Linux/macOS:

```console
python cartier_miller.py check --benchmarks smoke
python cartier_miller.py check --benchmarks all
```

Each run creates a fresh timestamped directory and ZIP under results. The
bundle includes environment information, a source-manifest fingerprint,
retained-source checks, validation, command logs, selected benchmark records
and checksums. Failed checks also produce a bundle marked passed=false.
An integrity-only run explicitly says integrity_only and does not imply that
mathematical tests or benchmarks were executed.

RUNTIME_MANIFEST.json pins root Python/batch files, retained Python modules
and SOURCE_PROVENANCE.json. It excludes prose and generated results so audit
reports can summarize a frozen runtime run. Package SHA256SUMS.txt covers
the delivered files, including prose/evidence, except itself. Hashes detect
change against a supplied manifest; they are not a digital signature or
third-party attestation. The evidence runner never regenerates the manifest.

Run normal Python without -O: the retained native kernels require assertion
checks. The active arithmetic paths use only the standard library. Old
optional extension-field/GMP helpers are not required by these interfaces.
