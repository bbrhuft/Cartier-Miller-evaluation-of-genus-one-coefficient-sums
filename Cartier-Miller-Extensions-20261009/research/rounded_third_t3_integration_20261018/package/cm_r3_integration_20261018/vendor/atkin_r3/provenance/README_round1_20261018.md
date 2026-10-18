# Atkin global recurrence: partial progress

Read REPORT.md for the proof, outcome and limits. OPUS_HANDOVER.md is a ready-to-paste continuation prompt. The production and validation code is standard-library Python 3.10+.

```bash
python3 audit.py
python3 acquire_derivative.py 1013
python3 acquire_derivative.py 100000007 --method shared
python3 develop.py
python3 confirm.py
python3 benchmark.py
```

The first audit is for the delivered package; regenerated evidence has new timings. Source hashes in evidence/FREEZE.json remain independently checkable. Prime certification is a production input contract. The runners certify their experimental inputs by trial division outside timed acquisition.

atkin.py contains the homogeneous five-residue derivative recurrence, the scalar Wronskian endpoint product and a shared rising-product backend. Both c_p and A_n'(0) can be acquired, with conversions explicitly charged. All benchmark methods acquire the same c_p from the prime alone.

The Wronskian reduction removes the matrix product, but does not remove factorial-type arithmetic. The shared-product benchmark gain is an implementation-level constant factor, not a better asymptotic exponent. No experiment here evaluates a 1201-bit prime or supports an extrapolation to that size.

The immutable vendor code comes from the supplied Sol package. Reports under provenance/ remain unrefereed source inputs. Evidence under evidence/ was generated in this investigation. CANDIDATE.md describes the actual frozen claims and selection rules.

acquire_derivative.py is the thin production API. It calls the frozen acquisition core and performs the explicitly charged conversion from c_p to A_n'(0); it does not run a linear reference product. Its post-core-confirmation composition check is separately labelled in evidence/API_WRAPPER_CHECK.json. The atkin.py demonstration CLI additionally runs the linear Wronskian cross-check and should not be used as the fast timing entry point.
