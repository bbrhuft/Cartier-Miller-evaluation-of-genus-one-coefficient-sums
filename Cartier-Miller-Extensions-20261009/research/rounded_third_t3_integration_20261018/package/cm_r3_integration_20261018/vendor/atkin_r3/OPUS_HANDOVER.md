# Continue the Atkin endpoint investigation (round 3)

Read REPORT.md, CANDIDATE_CHARP.md, charp.py and atkin.py, then run `python3 audit.py` before regenerating anything. Round-1 material is under provenance/ and the round-1 freeze. Keep source-report evidence separate from newly executed evidence. Never overwrite evidence/FREEZE.json or evidence/charp/FREEZE_CHARP.json to hide a code change.

## Established so far

- The endpoint derivative is implicit in Kaneko–Zagier Proposition 5: D = 1728^N R_N for p ≡ 5 (mod 12) and D = −1728^{N+1} R_N for p ≡ 11 (mod 12), with R_N = (4/3)_N/N!. Do not present it as new.
- Theorem C6: no Gross–Koblitz, Gauss-multiplication or reflection relation of any conductor determines Γ_p(1/3). With conductors ≤ Q, some interval product must have length ≥ p/Q² − 1. Bounded-conductor ideas therefore give constant factors only.
- The half-interval identity c_p = 2HP³, with H = ((p−1)/2)! taken from class numbers, is exact on 27 fresh primes up to 2·10¹¹. Its routes are:
  - Mordell for p ≡ 3 (mod 4);
  - Gauss–Dirichlet for p ≡ 5 (mod 8);
  - conjecture (\*) via h(−3p) for p ≡ 17 (mod 24).
- The half-interval identity beats FLINT's native factorial by 1.18–1.56×, and the FLINT nodal anchor by 1.03–1.26×. Both gains need PARI's GRH-conditional class number; they disappear with the unconditional Python class-number count and in the pure-Python engine.
- The quarter identity (m!/N!)⁴ ≡ a² leaves one sign undetermined. That is the recorded first exact failure.

## Next bounded target

Take the exponent question at the inert point 1/3. Read Tal (2026, ECCC TR26-211) closely. Then state one concrete specialization of its Jacobi-sum construction to m! = ((p−2)/3)! for p ≡ 5 (mod 6), using divisors q of 1 + p + p² (or of p ± 1). The statement must give:

- the conductor;
- how the Jacobi sums are computed, and how their root of unity is fixed (van Wamelen);
- the residual interval length;
- the full cost.

Check it against Theorem C6: the conductor must grow at least like p^δ. Develop a complete proof or record the first exact failure. Freeze the candidate before selecting disjoint confirmation inputs, and use the round-2 development and confirmation primes as exclusions.

Secondary bounded items, constant factor only:

- prove or refute (\*), equivalently (m!/N!)² ≡ a·(m!/p) for p ≡ 5 (mod 12). Williams & Currie (1982) is the first source to check;
- find the residual quarter-identity sign in o(√p), or show that a stated invariant class cannot supply it.

## Rules

- Do not count a growing product as a supplied scalar.
- Do not treat a low-dimensional state as polylogarithmic time.
- Do not cite C6 or C7 as a universal lower bound; C6 concerns derivations in a stated calculus, and C7 is finite evidence.
- Label every claim as background, proved here, finite evidence or conjecture.
- No publication or priority claim is authorized.
