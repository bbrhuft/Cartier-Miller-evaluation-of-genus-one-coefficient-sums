# Live third-point prefix connection (introduced in version 0.2)

This release implements the next engineering step: combine the retained project prefix routines with the new boundary registry to compute complete original sums. It is a standalone package; it does not edit the earlier archive, manuscript, GitHub repository or your Windows source tree.

## Retained implementation

The source is `Cartier_Miller_Integration_Audit_20261013.zip`. Five implementation files are included unchanged: `ordinary_third.py`, `hyperelliptic_prefix.py`, and the genus-one `fields.py`, `curve.py`, `miller.py`. Only the containing package name changes in the new wrapper's imports. The relative imports inside those files are unchanged. The source archive and each copied implementation file are hashed in `SOURCE_PROVENANCE.json`.

The ordinary-third routine uses its existing undivided characteristic-p normalization, including exceptional trace/character equality. Its curve/trace constructor is reused. The rounded third calls the retained Cantor–Miller prefix with d = 3 and genus 1; it returns exactly the strict prefix at (p+1)/3. This specialization uses the known annihilator p+1 and does not acquire a trace by point counting. The supplied project theorem and implementation remain unrefereed. Independent finite checks support this integration; they do not establish novelty or specialist certification.

`RETAINED_HIGHER_GENUS_REPORT.md` is a byte-for-byte copy of the report inside the retained higher-genus archive. Its broad original claims are historical project context. The third-point service described here exposes its genus-one rounded-third specialization. Version 0.3 additionally connects its genus-two fifth-point specialization, documented separately in FIFTHS.md; it does not expose a general higher-genus service.

## Ordinary-third boundary reuse

For p = 1 modulo 3, put L = (p−1)/3. The earlier coefficient reduction a_L = −(L!)^(−3) remains implemented and can be forced with `boundary_policy="factorial"`. However, the retained geometric setup already supplies a_L as its Hasse/trace residue H.

Indeed, with h = (p−1)/2 and f(w) = 1−w³/2, expansion modulo p gives

$$f(w)^h=\sum_{i=0}^{h}a_iw^{3i}.$$

Thus [w^(p−1)]f(w)^h = a_L. The trace tau of v² = f(w) is minus the sum of its quadratic characters. Euler's criterion and the sums of powers over F_p show that this trace modulo p equals [w^(p−1)]f(w)^h: the constant term sums to p = 0, and the polynomial degree 3h is below 2(p−1), so only the exponent p−1 contributes. Therefore a_L = H = tau modulo p.

The wrapper registers this already-acquired scalar as an explicit zero-factorial reduction. It does not disguise trace acquisition as free work. The retained Cornacchia preparation is charged to cold evaluations; its deterministic cubic-nonresidue scan is not assigned an unconditional polylogarithmic worst-case bound. No caller-supplied trace option is added by this wrapper.

At the rounded third, that ordinary trace argument is unavailable: the wrapper obtains the strict prefix from the retained d = 3 routine and requests G = ((p−2)/3)! from the new boundary backend, then forms a_L = (3/2)G^(−3). Hence the factorial can still dominate the full rounded-third runtime. There is no claim of a logarithmic complete rounded-third algorithm.

## Interface and timing

`ThirdPointSession(p)` validates the prime, identifies its supported third index and prepares the prefix provider. `evaluate()` connects that provider to `complete_sum`. The ordinary default requests the trace boundary; `boundary_policy="factorial"` requests the original third-factorial plan. The rounded case uses the factorial plan under either policy. The final combination is the same independently checked original-sum identity from MATHEMATICS.md.

The ordinary retained routine also returns its own a_L and U. The wrapper checks agreement with those values. These checks catch assembly mismatches but are not independent proof because the retained U uses the same identity. The test suite instead checks B against an independent scaled binomial recurrence, a against exact integer binomials and U against the independently defined t recurrence.

Every prefix call reruns the Miller pass. There is no answer cache. A session retains ordinary curve/trace preparation only. `session_setup_seconds` records session construction; `warm_total_seconds` records one evaluate call; `cold_total_seconds` is their sum. Thus a warm result explicitly excludes earlier preparation, while cold timings include it. Imported modules, interpreter startup, JSON serialization, prime selection and file saving are excluded from the arithmetic benchmark.

The integrated benchmark compares identical U outputs. Its direct baseline evaluates the original rational t recurrence with denominators D_i = 2^i i! cleared: T_i = D_i t_i and S_i = D_i U_p(i). Then

$$T_{i+1}=(h+2+i)T_i,$$
$$S_{i+1}=2(i+1)\bigl(S_i+(h+1+i)T_i\bigr),\qquad D_{i+1}=2(i+1)D_i.$$

A single final inversion returns U. The baseline returns U only; the integrated route additionally returns B and a diagnostics. At smaller benchmark primes this scaled baseline is checked again against the original unscaled t recurrence. All cold samples create a fresh session. Warm samples exclude separately recorded preparation and rerun the arithmetic.

## Input and execution scope

Supported primes are 7 ≤ p < 2^64 with p = 1 modulo 3, and 11 ≤ p < 2^64 with p = 2 modulo 3. Each prime supports precisely its third index. The existing boundary CLI still supports arbitrary 0 ≤ L < p independently of this prefix restriction. Composite inputs, mismatched indices and prime-power requests fail explicitly. The configured boundary work limits still apply at rounded thirds and at forced ordinary factorial evaluations.

The retained code relies on assertions for internal algebraic checks. The integration rejects execution under Python optimization (`-O`) rather than running those kernels with their checks disabled. Unused optional-library helpers remain present in unchanged source files but are not called by this interface.

## Documentation correction

The version 0.1 README example for p = 23 incorrectly asserted U_p(8) = 15. Exact evaluation gives B_8 = 7, a_8 = 9 and U_p(8) = 17. Likewise p = 29 gives B_10 = 13, a_10 = 21 and U_p(10) = 21. These concrete inputs are now explicit regressions against the original sum. This correction concerns illustrative values; the version 0.1 arithmetic suite already checked the correct original sum. No published manuscript has been edited as part of this correction.
