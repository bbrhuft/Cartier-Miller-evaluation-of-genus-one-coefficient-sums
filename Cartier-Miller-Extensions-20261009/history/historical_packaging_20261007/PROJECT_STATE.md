# Current state after consolidation

7 October 2026. Status descriptions below supersede the earlier handover's trial-count and negative-status claims. The mathematical arguments remain unrefereed. The original manuscript and historical branches are preserved without revision.

| Question or component | Current status | Limits |
|---|---|---|
| One depth-three family from the ordinary A=0 seed | Explicit coefficients, normalized rooted chains, twist parameter and direct recognition retained | Classical CM curves; novelty of the computational presentation is unestablished |
| Parameter extraction and recognition | O(1) field work after prime validation; exact norms exclude eligible-prime denominator failures | Only this depth-three family and the explicitly combined prior families |
| Exact trace candidates | Retained proposition gives ±t₀ from 4p=t₀²+192f²; Cornacchia implementation | Depends on the reviewed CM/isogeny argument |
| Trace-sign success probability | New proper-subgroup derivation gives ≥1/5 per raw uniform-x trial | Requires a recognized family member and independent uniform draws |
| Unbounded sign test | At most five raw trials in expectation; almost-sure termination, zero-error output | Almost-sure completion is not a deterministic bound on every random execution |
| Default sign test | Cap 64; conservative inconclusive probability ≤(4/5)^64 | Returns no answer if exhausted; no automatic Schoof fallback |
| Sign witness | Stored point and candidate annihilation flags; deterministic re-verifier | Correct sign certificate uses the two-candidate theorem, not generic order certification |
| Complete preparation | Expected O(log²p) field operations plus polynomial integer work for the unbounded variant | Prototype prime guard restricts p<2^64; bit cost and prime validation are separately charged |
| Reconstructed K and root query | K=(β−bH/3)/a; supplied nonzero root query costs O(1) field operations | Root finding excluded; not a general every-stopping-index weighted-sum evaluator |
| Partial recognizer negative status | `not_in_implemented_families` | Does not rule out the deferred B=0 depth-three chain |
| Easy-seed sign obstruction | p=97, E:y²=x³+19, order 112, every point killed by 28 | Both candidates 84 and 112 annihilate every point; no generic sign-success theorem |
| Fresh validation | 1,215,024 nonsingular short models at ten primes, 2,640 coefficient pairs, 702 twists, 48 cubics and 96 branch queries | Finite support; counts overlap; correctness runs, not benchmarks |
| New independent arithmetic checks | Eight exact p=97 witnesses, 40 small-prime sampler representatives, forced retry exhaustion and status regressions | Same consolidation author, separate group-law implementation; not external human review |
| Historical PARI/symbolic checks | Original files retained | PARI and Sympy were not available for new cross-checks in this environment; no fresh PARI trace is claimed |
| Remaining research | B=0 seed depth three; higher depths; generic and supersingular K; deterministic trace-sign formula | No new result asserted here |

Normalize f=1+cw+bw²+aw³ by x=aw+b/3, y=av. This gives dw/v=dx/y, A=ac−b²/3, B=a²−abc/3+2b³/27 and β=aK+(b/3)H. The rooted quotient has differential scale +1 and β′=2β−qH. Its dual returns the square-scaled model (16A,64B). All scales and residue-free exact corrections remain explicit in the proof notes. At p=73, the normalized fixture f=1+4w+37w³ has short model (2,55), H=10, β=64, K=55 and T_f(9)=3; it is a square-scaled version of the original target (4,16), whose β is 4.

Schoof remains the unconditional deterministic theoretical trace setup. The new restricted-family CM route is a randomized alternative, not a replacement for the deterministic argument. No production SEA implementation is introduced. A fast claim for the original weighted sum still requires both B_L and a_L, identical moduli and outputs, charged preparation, CSVs, source hashes and environmental records. None of this work changes the higher-genus or precision-two branches.
