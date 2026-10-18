# Many-prime complete outputs

Version 0.7 connects the retained rounded-third remainder-forest machinery
to a common many-prime interface. It returns B_L, a_L and U_p(L), rather
than timing boundary acquisition alone. The new scheduler also supports
mixed stopping indices and several cutoffs at the same prime. This is an
integration of established machinery, not a new remainder-forest algorithm.

## Run the dense-prime path

```console
python many_primes.py --bound 20000 --family rounded_third --chunks 32 --out rounded_thirds.csv
python many_primes.py --bound 20000 --family thirds --chunks 32 --out thirds.csv
python many_primes.py --bound 20000 --family fifths --chunks 32 --out fifths.csv
python benchmark_many_primes.py --repeats 3
```

The upper bound is exclusive. `thirds` generates the appropriate ordinary
or rounded third at each supported prime p>=7. `ordinary_third` selects
p=1 modulo 3; `rounded_third` selects p>=11 with p=2 modulo 3. `fifths`
generates both supported fifth indices at p>=19 with p=4 modulo 5.
Prime enumeration and validation are included in the end-to-end benchmark.
The runtime requires only the standard library. No installation or compiler
is required for either engine.

## Arbitrary requests and order

```python
from many_primes import ManyPrimeEvaluator, PrimeQuery, range_queries

queries = [PrimeQuery(59, 24), PrimeQuery(11, 4), PrimeQuery(59, 6),
           PrimeQuery(59, 24)]
result = ManyPrimeEvaluator().evaluate(queries, engine="forest", chunks=8)
assert [(row["p"], row["L"]) for row in result["outputs"]] == [
    (59, 24), (11, 4), (59, 6), (59, 24)]

stats = {}
for row in ManyPrimeEvaluator().iter_evaluate(
        range_queries(20000, "rounded_third"), stats=stats):
    pass  # Consume or write the unique outputs without collecting the table.
assert stats["complete"]
```

`PrimeQuery(p,L)` requires an odd prime p<2**64 and 0<=L<p. Arbitrary
cutoffs, including 0 and the upper half, are mathematically supported by the
forest. This does not establish a fast isolated-prime arbitrary prefix.
The forest advances from recurrence index 0 to the largest requested L;
sparse requests at large cutoffs can be expensive.

`evaluate` preserves input order and duplicates. It collects the output
table and returns independent dictionary objects even for duplicates.
Each distinct (p,L) is computed once within that call. `iter_evaluate`
streams unique results, so it intentionally removes duplicate requests.
Forest streaming order is increasing (L,p), not increasing prime alone.
The independent iterator groups primes by their first encounter in that
ordering and returns increasing cutoffs within each group. These orders are
explicit in the returned statistics. Both iterators retain request metadata.

```console
python many_primes.py --queries 59:24 11:4 59:6 59:24
python many_primes.py --queries 1000037:333346 --engine independent --backend bgs
```

The first command collects JSON and preserves its duplicate and request
order. With `--out`, the CLI instead uses the unique streaming contract.
CSV fields are p,L,B_L,a_L,U_p_L. The CLI validates before opening an output
file, writes a temporary file in its destination directory, and replaces the
destination only after successful completion. A validation or runtime error
leaves a pre-existing destination intact and cleans up the temporary file.
The JSON printed alongside the CSV contains execution statistics.

## Forest engine and reuse

The forest imports the exact integer triangular-matrix multiplication,
balanced interval products and remainder-tree code from
`retained_cm/rounded_third_batch.py`. That file is copied byte-for-byte from
`Rounded_Third_Batch_Extension_20261014.zip`. SOURCE_PROVENANCE.json records
the archive and module hashes. RETAINED_FOREST_PROOF.md preserves its proof.
The old rounded-third public evaluator is still available unchanged and
is compared directly with the new wrapper in tests.

The new work is request validation, a schedule sorted by cutoff, support
for repeated primes at different cutoffs, resource preflight, a common
complete-output contract, streaming and an independent comparison route.
The retained native prefix theorems remain unrefereed; finite comparisons provide execution evidence, not external certification. The retained rounded-third engine already computed complete outputs; this
release does not present that older capability as newly discovered.

Write D_j=4^j*j!, A_j=D_j*a_j and C_j=D_j*B_j. The integer matrix is

\[
M_j=\begin{pmatrix}4(j+1)&4(j+1)\\0&2j+1\end{pmatrix},\qquad
\Pi_L=M_{L-1}\cdots M_0=
\begin{pmatrix}D_L&C_L\\0&A_L\end{pmatrix}.
\]

This identity follows from 4(j+1)a_(j+1)=(2j+1)a_j and
B_(j+1)=B_j+a_j. For every valid query L<p, D_L is a unit modulo p,
including when A_L is zero in the upper half. One inverse recovers B_L and
a_L. The retained identity U=4B-2L(2L+5)a then supplies U. Tests also use
the original t recurrence as an independent U oracle.

For sorted cutoffs L_1<=...<=L_n, each leaf is the exact matrix product
from the previous cutoff to the current one. Equal cutoffs give identity
leaves. A later interval multiplies on the left. Modulus leaves are the
corresponding query primes. The scheduler's remaining modulus is the product
of all unprocessed query moduli and its carry is the earlier prefix matrix
reduced modulo that product. The retained tree computes each inclusive
prefix residue. After a chunk, left-multiply the carry by its exact chunk
product and reduce modulo the remaining product.

Repeated primes are valid: the remaining modulus can contain powers of p.
The proof uses divisibility of child moduli into their parent, not pairwise
coprimality or a CRT inverse. The only modular inverse used to decode a row
is D_L^(-1), and L<p guarantees it exists. Duplicate (p,L) requests are
removed before building the schedule and restored only by the collecting API.

All chunks together traverse max(L) recurrence steps. There are
chunks_used-1 carry updates when the forest is nonempty. Chunk count is
requested, not assumed: equal prime/query-count chunks can have very
different recurrence spans, and rounding can use fewer chunks than requested.
No earlier chunk product or computed answer persists across calls.

## Independent engine and U-only output

`engine="independent"` groups requests by prime. It calls the retained
third-point session for the supported third index. If either or both fifth
indices occur, it uses one fifth-point session and one joint prefix pass,
preserving the existing sharing. Other indices use the explicit direct
reference prefix with the shared boundary service. Statistics distinguish
native third primes, native fifth primes and reference-prefix queries.
The ordinary third still reuses its native trace boundary. `backend` selects
the independent boundary kernel; it does not alter the forest's integer
matrix arithmetic. There is no automatic dense/sparse dispatch in this
release; both routes remain explicit for measured comparison.

```console
python many_primes.py --bound 20000 --family rounded_third --engine independent --backend bgs
python many_primes.py --queries 17:6 29:12 --output-mode u_only
```

U-only mode returns null B/a fields in JSON and empty B/a cells in CSV.
The forest computes these quantities jointly as part of the same matrix
recurrence; its rows say `boundary_status="computed_jointly"`. It does not
claim to skip boundary arithmetic at zero multipliers. The independent
native services retain their actual zero-multiplier acquisition skipping.
Every request, option, resource limit and precision is still validated.
Modulo p only is supported; modulus_power other than 1 is rejected.

## Resource preflight and memory accounting

| Guard | Default | Meaning |
|---|---:|---|
| max_queries | 100000 | Raw input requests, including duplicates |
| max_forest_index | 2000000 | Largest cutoff traversed by the forest |
| max_modulus_bits | 2000000 | Conservative sum of bit lengths of all distinct query moduli, with repeated primes counted once per distinct cutoff |
| max_chunk_product_bits | 32000000 | Conservative upper bound per exact matrix entry in the largest chunk |
| range_queries max_bound | 2000000 | Sieve allocation guard for generated prime ranges |

All integer guards reject booleans and negative values. Forest bounds are
checked before allocating its modulus product or any interval matrix.
The independent engine obeys the common request cap and the existing
prefix/kernel limits; forest-only guards do not restrict it.

For a chunk spanning g steps and ending at t, diagonal entries are at most
(4t)^g and its upper-right entry is less than twice the upper-left entry.
The latter follows by summing a geometric series with successive ratios
(2j+1)/(4(j+1))<1/2. The implementation therefore uses the safe bit bound
g*bit_length(4*max(1,t))+2. Every internal exact chunk product obeys that
bound as well. Actual largest chunk-entry and modulus sizes are recorded.

These are arithmetic-size guards, not a total-memory or RSS guarantee.
Retained product/modulus trees store several levels; multiplication and
carry updates allocate transient integers. Request lists, dictionaries,
Python object overhead, sieve generation and any collected output table
also consume memory. Carry products can temporarily have roughly the sum
of exact-chunk and remaining-modulus bit lengths. Forest streaming retains
one chunk of residues plus all request metadata and the remaining carry;
the collecting API additionally retains all output rows. The independent
iterator retains one prime group's results in addition to request metadata.

## Timing, measurement and partial streams

Statistics separate query validation/planning from execution. For
`evaluate`, total_seconds covers the complete method call, including result
collection, and excludes evaluator construction, import and serialization.
For `iter_evaluate`, execution time is charged while advancing the generator;
consumer pauses and CSV writing are excluded. Query generation is separate
and explicitly recorded by the CLI. `complete` becomes true only after
exhaustion; early cancellation leaves it false and records the rows emitted
and actual chunks processed. A partially consumed stream is not labeled a
completed evaluation.

The fresh-process benchmark includes evaluator construction, query
generation, validation, complete arithmetic and collection in timed samples.
It verifies ordered fingerprints of every B/a/U tuple against independent
scaled coefficient and original-t recurrences. Separate, untimed memory
samples use tracemalloc and, where available, process peak RSS. Traced Python
allocations exclude imports; whole-process RSS includes them. Both include
the collected output table. No streaming peak-memory claim is inferred from
those measurements. Imports, fingerprint serialization and reference
generation are excluded from timing.

Chunk count trades tree size against arithmetic overhead. The measured
sparse case is deliberately included because a forest may be slower than
the native BGS route on widely separated primes. Results apply to this
standard-library Python implementation and this machine. The broader
average-polynomial-time remainder-forest theory is established literature;
the retained proof gives conservative bounds for this particular integer
recurrence and does not assume CPython has asymptotically optimal integer
multiplication.

Harvey, D., & Sutherland, A. V. (2016). Computing Hasse–Witt matrices of
hyperelliptic curves in average polynomial time, II. *Contemporary
Mathematics, 663*. https://doi.org/10.1090/conm/663/13352.
Author offprint: https://math.mit.edu/~drew/conm13352.pdf.


## Version 0.8 measured selection

The engine auto option now applies exact local calibration profiles, with clear untrained fallbacks. Explicit routes and the original default forest remain available. MEASURED_DISPATCH.md defines collection/output matching, environment/source invalidation and timing overhead. Earlier statements in this note about no automatic dispatch describe the 0.7 release. Historical timing/memory evidence is preserved under evidence/history/v0_7/.
