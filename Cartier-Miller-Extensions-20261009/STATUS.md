# Status

Status as of 10 October 2026. The research reported here was completed between 6 and 10 October 2026. Preparing the release added a replacement closure validator, two portability fixes and a full validation rerun. It made no change to any theorem, recognizer or evaluator.

| Component | Status |
|---|---|
| Branch formula and global normalization | Proved by two algebraic arguments in the branch-point report; unrefereed; the default evaluator is implemented with an O(p) general fallback |
| Rooted transport and dual normalization | Proved in the closure theory note; unrefereed; replacement finite validation passed |
| Depth one | Explicit ordinary-seed families and normalized path recovery; implemented; checked for every member below 200 |
| Depth two | Complete direct recognition for the rational degree-two closure of the specified ordinary easy seeds; parameter and twist certificates; unrefereed proof |
| Depth three | One A=0-seed, discriminant −192 family consolidated, with recognition, reverse certificate, CM trace candidates and a trace-sign bound; the B=0-seed chain is deferred; not a complete all-family recognizer |
| Trace sign and costs | Deterministic sign by Ireland & Rosen, Ch. 18, Theorem 4 is the default since 10 October (DETERMINISTIC_TRACE_SIGN_20261010.md); complete CM preparation is randomized only in the √−3 search; the Las Vegas alternative keeps the TRACE_SIGN_BOUND_20261007.md bound; Schoof remains the unconditional theoretical alternative; no production SEA |
| Negative recognizer outputs | not_in_implemented_families does not prove global or full depth-three nonreachability |
| Rounded third point, p ≡ 2 mod 3 | Boundary a_L=3/(2(m!)³), m=⌊p/3⌋; complete weighted sum equivalent to the Gauss factorial ⌊p/3⌋! mod p (p≠17); trace data cannot help; no polylogarithmic method; deterministic cost about √p up to log factors, with unrefereed randomized p^{1/2−δ} claims for most primes; parked as a precise obstruction; unrefereed |
| Validation | Every validator rerun in this layout on 9 October with no failures; the original retained evidence is kept unchanged; the rerun outputs are in evidence/rerun_20261009/ |
| Novelty | Unestablished; classical ingredients are acknowledged explicitly; prior-art searches were targeted, not exhaustive |
| Manuscript | Not included and not revised; its direct characteristic-p exceptional normalization governs |
| Licence | MIT for everything in this release; material under other terms is excluded (PROVENANCE.md) |

Open directions, none of them started, are: a batch remainder-tree evaluator of ⌊p/3⌋! mod p for many primes at once; the deferred B=0-seed depth-three chain; depth four; generic and supersingular K; and the higher-genus boundary. Earlier reports in research/ and history/ are chronological records, not competing current specifications. Where they conflict with this file, RESULTS.md or docs/LEDGER_20261009.md, the later documents govern.
