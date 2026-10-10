# Deterministic trace sign for the depth-three family

10 October 2026. This addendum to the depth-three proof note is unrefereed and makes no novelty claim. It replaces the default Las Vegas sign decision in the complete CM preparation with a deterministic rule from a classical theorem. The consolidated zero-error point test and its proved 1/5 success bound (TRACE_SIGN_BOUND_20261007.md) are kept as an alternative and as a cross-check. The rule itself is classical; what is recorded here is how it is applied to this family, the implementation, and the checks.

## The theorem used

Ireland and Rosen (1990, Ch. 18, §3, Theorem 4, p. 305) state the following. Let p ≡ 1 (mod 3) and p ∤ D. Write p = π π̄ with π ∈ ℤ[ω] primary, that is π ≡ 2 (mod 3). Then the number of projective points on y² = x³ + D over 𝔽_p is

$$N_p = p + 1 + \overline{\left(\tfrac{4D}{\pi}\right)_6}\,\pi + \left(\tfrac{4D}{\pi}\right)_6\,\bar\pi ,$$

so the trace is $\tau = -2\,\mathrm{Re}\bigl(\overline{(4D/\pi)_6}\,\pi\bigr)$. Here $(a/\pi)_6$ is the sextic residue symbol: the sixth root of unity congruent to $a^{(p-1)/6}$ modulo π. The proof in the book uses Jacobi sums. Its worked example is p = 13, D = 1, π = −1 + 3ω and N₁₃ = 12, which gives trace 2.

## Application to the family

By the trace proposition of the proof note, an accepted curve has exactly the trace of its j = 0 seed y² = x³ − r³, where r is the recognized parameter. Theorem 4 therefore applies with D = −r³. The condition p ∤ D holds because r ≠ 0, and p ≡ 1 (mod 24) implies p ≡ 1 (mod 3).

The primary prime comes from the Cornacchia step the preparation already performs. That step writes p = x² + 48y² using a square root of −3. With √−3 = 1 + 2ω, the element x + 4y√−3 = (x + 4y) + 8yω has norm x² + 48y² = p. Exactly one of its six unit multiples a + bω satisfies a ≡ 2 and b ≡ 0 (mod 3), and that is π. Modulo π one has ω ≡ −a/b, so the symbol is the power of the image of the primitive sixth root 1 + ω that equals (4D)^{(p−1)/6} mod p. The code checks that b is not divisible by p and that the image of ω is a cube root of unity. It also checks |τ| = t₀ against the Cornacchia candidate, and raises `ProofViolation` if any check fails.

## Cost and remaining randomness

Given π, the sign costs one exponentiation, which is O(log p) field operations, and it is deterministic. The complete CM preparation is now deterministic apart from one step: the search for a cubic nonresidue that yields √−3 for Cornacchia, with an expected 1.5 exponentiations. Making that step deterministic is a separate classical problem and is not addressed here. Schoof's algorithm remains the unconditional deterministic theoretical fallback, and the prototype does not invoke it.

## Implementation

`primary_prime_from_cornacchia` and `seed_trace_sextic` were added to core/depth_three_recognize.py. `prepare_cm` now defaults to `sign_method='sextic'`; `sign_method='las_vegas'` restores the consolidated zero-error test, including its `max_trials` cap or unbounded mode and its checkable point witness. In `prepare_from_trace`, `verify_sign=True` (or `'sextic'`) now verifies a supplied sign deterministically, while `verify_sign='las_vegas'` uses the point test. A trace whose sign has been verified is reported as exact rather than as trusted data. The CLI gains `--sign-method {sextic,las_vegas}`. The consolidated options `--max-sign-trials` and `--unbounded-sign-test` still apply to the Las Vegas method.

The update arrived as a branch of the original 7 October code, not of the consolidated version. It was merged onto the consolidated code so that the consolidation repairs were kept. Those repairs are the 1/5 sign bound and its witnesses, the stricter validation of certificate parameters, and the cautious `not_in_implemented_families` status.

## Checks

The depth-three validator compares Theorem 4 with Legendre-symbol traces for all 6,900 curves y² = x³ + D at the 37 primes p ≡ 1 (mod 3) below 400. It finds the primary prime by exhaustive search, independently of the Cornacchia route. It reproduces the book's p = 13 example. It checks that the sextic sign equals the family trace at all 46 eligible primes below 3,000. It checks that the sextic and Las Vegas methods give the same trace in all 27 complete preparations, at primes up to 63 bits, with PARI traces where available. It rejects the wrong-sign supplied trace −10 at p = 73 under both methods. The consolidation validator checks that the deterministic default ignores the retry cap.

independent/indep_sextic_theorem4_20261010.py implements Theorem 4 separately. It uses complex arithmetic in ℤ[ω], obtains primary primes from PARI's `qfbsolve`, and compares against PARI `ellap`. It agreed on 2,075 curves, at every prime p ≡ 1 (mod 3) below 3,000 and at nine primes of 40 to 52 bits. These finite checks support the implementation. Correctness rests on the cited theorem and on the trace proposition.

## Source

Ireland, K., & Rosen, M. (1990). *A classical introduction to modern number theory* (2nd ed., Graduate Texts in Mathematics 84), Chapter 18, Section 3, Theorem 4 and the example on p. 306. Springer. https://doi.org/10.1007/978-1-4757-2103-4. The author read this in a user-supplied scan of Chapter 18, pp. 297–307; the scan is not redistributed.
