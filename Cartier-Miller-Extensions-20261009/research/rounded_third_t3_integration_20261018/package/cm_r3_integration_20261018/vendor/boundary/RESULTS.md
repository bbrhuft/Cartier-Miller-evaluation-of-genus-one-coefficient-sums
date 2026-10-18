# Release results: 1.0.0rc1

The full release capture passed on Linux with 95 regression methods, 11 public-command checks and all eight benchmark suites. The suites contain 1,051 checked timing/calibration/memory executions. Source integrity matched before and after the 343.00-second run. No current-candidate Windows execution is claimed.

The authoritative release interpretation is RELEASE_AUDIT.md. Raw records are under results/release_linux and the shareable results/release_linux.zip; the stage logs record exact commands and exit codes. All current suite summaries identify version 1.0.0rc1. Historical evidence is under evidence/history, with the original attached Windows logs under evidence/windows_v0_1.

| Suite | Checked runs |
|---|---:|
| boundary | 189 |
| thirds | 96 |
| fifths | 75 |
| output_modes | 42 |
| bgs | 342 |
| shared | 126 |
| many_primes | 64 |
| dispatch | 117 |
| Total | 1,051 |

The total includes 81 real calibration executions and 16 separately profiled memory executions. It is not a count of distinct inputs. Tests/smoke also perform small calibrations, which are outside this benchmark count. Timing, reference and memory scopes are specified in each JSON summary and in RELEASE_AUDIT.md.

The current measured examples and counterexamples are:

| Workload | Route A | Route B |
|---|---|---|
| Complete fifth pair, p=10,000,019 | Product tree 107.13 ms | BGS 25.65 ms |
| Sixteen nearby boundaries, p=10,000,019 | Separate BGS 300.43 ms | Adjacent sharing 16.53 ms |
| 1,135 rounded thirds below 20,000 | Independent 1506.85 ms | Forest 18.97 ms |
| Three sparse stopping queries up to p=1,000,037 | Independent 8.62 ms | Forest 4940.67 ms |
| Small sparse dispatch workload, max p=100,003 | Untrained independent 3.31 ms | Profile-based auto 4.37 ms |

These are local medians, not universal crossover rules. The sparse and profile-overhead controls remain material limitations. Retained source hashes, native-theorem assurance limits, precision restrictions and open platform/review evidence are documented explicitly in the audit.
