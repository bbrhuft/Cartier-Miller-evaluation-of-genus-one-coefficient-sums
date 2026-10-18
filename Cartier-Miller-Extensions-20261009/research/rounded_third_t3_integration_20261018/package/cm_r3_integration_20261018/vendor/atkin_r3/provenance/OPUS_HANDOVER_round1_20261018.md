# Continue the Atkin endpoint investigation

Read REPORT.md, CANDIDATE.md and atkin.py, and run audit.py before regenerating outputs. The prior Sol and Opus local reports are under provenance/. Run develop.py and confirm.py, distinguishing source-report evidence from newly executed evidence. The package has already completed development, a genuine source freeze, disjoint confirmation and matched cold benchmarks. Do not overwrite evidence/FREEZE.json to hide a code change.

The important progress is an exact endpoint collapse. With a_j=A_j(0), d_j=A_j'(0), the standard Atkin beta_j and beta_1=393120, the report proves

$$a_jd_{j+1}-a_{j+1}d_j
=\frac{(12j-1)(12j+5)}{96j}a_j^2-\frac14\prod_{i=1}^j\beta_i.$$

For the supersingular endpoint n=floor((p-5)/12)+1+epsilon, epsilon=1 for p=11 mod12 and 0 otherwise, the first term vanishes modulo p at j=n-1. This gives

$$A_n'(0)=\frac{273}{2}\prod_{j=1}^{n-2}
\frac{-6(12j+7)(12j+13)}{(j+1)(2j+1)}\pmod p.$$

The fixed-dimensional matrix product therefore collapses to a scalar hypergeometric product. No polylogarithmic acquisition was found. Do not propose generic matrix exponentiation as though the matrices were constant, or count a growing product as a supplied scalar.

The practical backend uses the simplified nodal anchor

$$c_p=-\frac43\chi(6)(-1)^N\frac{(4/3)_N}{N!},\qquad N=\lfloor(p-5)/12\rfloor.$$

It evaluates the two products through one common multipoint tree and shares reversed-divisor inverses. This gave 1.48-1.59-fold speedups over the best included factorial method at p near 10^7 and 10^8, but is not a new asymptotic result or a benchmark against optimized libraries. Raw samples, counters and setup are supplied. Both comparator and candidate receive the same monic-inverse optimization, polynomial backend and block-size rule.

First audit the exact Wronskian proof, signed endpoint normalization, denominator hypotheses and source freeze. Read Kaneko-Zagier Proposition 6 and El-Guindy-Ismail's associated-Jacobi representations closely to determine whether the endpoint formula is already implicit or explicit. Treat it as derived and proved in this investigation, with novelty unresolved.

The next bounded mathematical target is a genuinely characteristic-p block/interval identity for R_N=(4/3)_N/N! at the p-related index N. The report proves that no characteristic-zero rational function Q has Q(X+1)/Q(X)=(X+4/3)/(X+1); this excludes one simple rational telescoper, not finite-field identities. Seek a mechanism that uses characteristic-p endpoint structure and acquires every boundary constant. An identity whose constants are gamma values, Jacobi sums, selected factorials or normalized Frobenius entries must charge their acquisition and sign. Replacing one scalar product by another of comparable total length is a constant-factor result only.

Before starting a broad search, state one candidate identity or representation, its operations, initial data and full cost. Develop a complete proof or record its first exact failure. Freeze any new candidate before selecting disjoint confirmation inputs. Do not claim that low-dimensional state implies polylogarithmic time: this package's homogeneous direct recurrence has only five residues and still O(p) work. The earlier local chart and sensitivity theorems do not establish universal lower bounds.

A useful software continuation could optimize shared multi-channel rising products, compare with a serious optimized factorial backend, and preserve a portable API for signed-scale acquisition. A mathematical continuation must improve the cost of the actual scalar product rather than redevelop the eliminated Atkin derivative jet. If no faster exponent emerges, retain the exact theorem and measured constant-factor improvement as a separate reviewable note.

Deliver a corrected self-contained report, runnable code, raw evidence, complexity and benchmark comparison, precise prior-work attribution and one next question. Clearly label established background, proved new-to-this-investigation statements, finite evidence and conjectures. No publication or priority claim is authorized by this handover.
