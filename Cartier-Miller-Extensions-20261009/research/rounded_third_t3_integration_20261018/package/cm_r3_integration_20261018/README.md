Cartier–Miller rounded-third integration experiment

This standalone research adapter connects the certified T3 boundary routine to the existing Cartier–Miller boundary registry and retained Miller prefix provider. It computes B_L, a_L, U_p(L) and G for a prime p congruent to 5 modulo 6, with L=(p+1)/3 and G=((p-2)/3)! modulo p. The original workbench, source reports and frozen vendor kernels are preserved. This package does not alter the workbench GUI or publish a repository change.

The tested runtime is 64-bit Linux and Python 3.12. The inherited FLINT comparator uses Linux shared-library internals through ctypes; this package is not a tested Windows build. The supported prime range is 11 <= p < 2^63. Primality is checked at the public adapter boundary. The mathematical prefix theorem remains unrefereed project work; exact arithmetic and finite tests are not specialist proof review. Run without Python's -O option, because the retained prefix kernel requires its assertion checks.

Install the recorded dependencies in your preferred Python environment, from this folder:

```console
python -m pip install -r requirements.txt
python audit.py
python integrated.py 700000001633
python integrated.py 700000001633 --method native
python integrated.py 700000001633 --method t3 --q 47
```

The default interface uses a fresh Jacobi context on every call. It uses native FLINT below 10^7, then the source R3.1 conductor cost predictor with an exact nodal fallback. No PARI installation or GRH backend is needed. This is a conservative experiment policy, not a machine-independent optimal dispatcher. The optional forced T3 route raises if reconstruction cannot be certified; automatic mode records the miss and falls back.

The public Python entry point delegates complete-sum assembly to the retained framework:

```python
from integrated import evaluate, RoundedThirdSession

r = evaluate(700000001633)
print(r['B_L'], r['a_L'], r['U_p_L'], r['G'])
print(r['boundary_acquisition']['route'])
print(r['boundary_acquisition']['q'])

session = RoundedThirdSession(700000001633)
r_again = session.evaluate()  # reruns arithmetic; no complete-answer cache
```

The meaningful validation checks the original weighted t recurrence independently of the reconstruction identity, checks binomial coefficients independently of rounded-third factorial reductions, compares two independently coded Miller prefixes, checks every component at p=17, and injects a lattice miss to exercise fallback. The development command repeats already recorded development inputs; it does not create new held-out evidence.

```console
python develop.py
python experiment.py confirm
python experiment.py benchmark
python experiment.py survey
python audit.py
```

Run benchmark alone, after confirmation. Benchmark and survey are separate workloads and must not run concurrently. The commands overwrite their generated evidence, never a freeze; the final manifest consequently needs regeneration if evidence bytes change. The original source freeze and vendor checks remain verifiable. Repeating timing runs changes times and file hashes naturally.

The benchmark compares the identical complete tuple (p,B_L,a_L,U_p(L),G). Single-prime methods charge the retained Miller pass, input validation, registry/provider setup, divisor discovery, reconstruction, products, normalization and result collection. Dense methods charge the sieve and canonical tuple hashing too. Python and GMP forests are the same preserved recurrence engine with different integer backends. They bypass Miller and acquire prefixes and boundaries jointly, so their speed is attributed to the forest rather than to T3 or the geometric theorem. Sparse forests pay the integer recurrence from index zero. Very large sparse-prime forests are outside the declared resource cap and receive no invented timings.

REPORT.md explains results and mathematical scope. CANDIDATE.md and evidence/FREEZE.json record the candidate before fresh confirmation selection. evidence/CONFIRMATION.json holds the 17 fresh cases; evidence/BENCHMARK.json contains all raw samples; evidence/SURVEY.csv is the million-bound exact output table. evidence/SURVEY.json distinguishes algebraic consistency checks from independently verified definition-level rows. Vendor code, reports and previous evidence live under vendor/; provenance records their original identities and hashes.
