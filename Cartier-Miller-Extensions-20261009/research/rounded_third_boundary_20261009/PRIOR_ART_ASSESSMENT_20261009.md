# Targeted prior-art assessment: rounded supersingular third point

9 October 2026. This was a targeted web literature search carried out in one session, not an exhaustive priority review. Sources are marked as read in part, consulted by abstract or secondary restatement only, or cited from established knowledge without being reopened. "Not located" means not found in this search; it does not mean the statement is absent from the literature.

## Questions asked

The search asked four things. Is the factorial form of the boundary a_{(p+1)/3}, or of C(2m,m) with m=(p−2)/3, known for p ≡ 2 (mod 3)? Is ⌊p/3⌋! mod p, equivalently Γ_p(1/3) mod p, known in closed form or by a fast method at these primes? Has the supersingular second-kind Cartier coefficient of the j=0 curve been identified with a Γ_p value? And what are the current best algorithms for factorials modulo a single prime and for many primes together?

## Findings

| Topic | Source and access | Finding | Effect on this work |
|---|---|---|---|
| p ≡ 1 (mod 3) companion | Cosgrave & Dilcher (2018), read via full-text extraction | Corollary 4.5 gives ((p−1)/3)!³ ≡ 1/r with 4p=r²+27s², from Jacobi's binomial theorem; the orders of ((p−1)/3)! define "Jacobi primes" | The elementary reflection C(2L,L) ≡ −1/(L!)³ is standard; Theorem R is its p ≡ 2 (mod 3) counterpart and is not new in substance |
| p ≡ 2 (mod 3) Gauss factorial | Same source | The paper gives no determination of ⌊(p−1)/3⌋! mod p for primes p ≡ 2 (mod 3); for moduli with no prime factor ≡ 1 (mod M) it says "This case seems utterly intractable" | Supports the obstruction; the remark concerns the structural determination of Gauss factorials, not algorithmic lower bounds |
| Earlier Gauss–Wilson extensions | Cosgrave & Dilcher (2008), read in part | M=2 is complete; M=3 and M=4 are only partial | Consistent with the above |
| Inert-prime Gauss factorials | Stokes (2022), arXiv:2207.07804, abstract | Uses Gauss factorials over ranges of length about p²/D for primes inert in Q(√−3) and links them to Iwasawa λ-invariants via Jacobi sums and Gross–Koblitz | Adjacent; consistent with F_{p²} being the level at which Jacobi sums live for these primes |
| Γ_p at rational arguments and Frobenius | Coleman (1990), cited via Kashio's published restatement (Annales de l'Institut Fourier; arXiv:1904.02879), Theorem 2.4 for odd p | Coleman computes the absolute Frobenius on Fermat curves in terms of Γ_p | The identification K ≡ −6/Γ_p(1/3)³ is plausibly a mod-p consequence; Coleman's paper was not read |
| p-adic Chowla–Selberg | Ogus (1990), bibliographic entry only | Title and venue confirmed; contents not read | Possible prior source for the supersingular period statement; needs a reviewer |
| Gross–Koblitz | Gross & Koblitz (1979), cited from established knowledge | Expresses Gauss sums through Γ_p | For cubic characters over F_{p²} with p ≡ 2 (mod 3) only Γ_p(1/3)Γ_p(2/3)=±1 enters; this assessment was made here and needs review |
| Mordell-type sign results | Mordell (1961); Elia (2013), via OEIS A265643 | ((p−1)/2)! ≡ ±1 at p ≡ 3 (mod 4), with the sign given by the class number h(−p) | Contrast only: no analogous constraint on (m!)³ was found or observed |
| Single-prime factorial algorithms | Bostan, Gaudry & Schost (2007), author PDF read in part | k! in a ring costs O(M(√k) log k) operations; the paper computes the Hasse–Witt matrix only, not second-kind data | Classical deterministic single-prime route for the boundary, about √p up to logarithmic factors |
| State of the art in 2026 (July) | Tal (2026a), arXiv:2607.29453, unrefereed, abstract and introduction | States that no classical worst-case single-input algorithm is known to break the square-root barrier; gives a conditional quantum algorithm | Superseded on this point by Tal (2026b); quantum results are outside scope |
| State of the art in 2026 (September), added 10 October | Tal (2026b), ECCC TR26-211, unrefereed, ECCC abstract only (the author read the report in full) | Classical randomized Õ(q^c+√p/q^{1/4}) for q ∣ 1+p+p², with variants for divisors of p±1, and p^{1/2−δ} for most primes; deterministic √(log p/log log p) improvement of Bostan et al. for every prime | Corrects the 9 October cost statement; no polylogarithmic method; the obstruction stands |
| Many primes together | Costa, Gerbicz & Harvey (2014), abstract; Harvey (2014), from established knowledge | (p−1)! mod p² for all primes up to a bound in average polynomial time, using remainder trees | The batch route for ⌊p/3⌋! is assessed as analogous but not verified |
| Factorial value sets | Hu (2026), arXiv:2608.01781, abstract | Lower bound |{k! mod p}| ≫ p^{8/15} | Not relevant to the computational question; noted to avoid confusion |
| Binomial-coefficient engines | IACR ePrint 2026/2111, abstract | C(N,R) mod m via tables and Gauss's generalisation of Wilson's theorem; no new factorial complexity | Not relevant |

## Not located

The search did not find, as an explicit statement, the equivalence between the complete weighted sum U_p((p+1)/3) and ⌊p/3⌋! mod p. It also did not find an evaluation of ⌊p/3⌋! mod p for p ≡ 2 (mod 3) by quadratic forms, class numbers or CM data. Nor did it find an explicit mod-p statement that K ≡ −6/Γ_p(1/3)³ for the curve v²=1−w³/2. The first is a short consequence of classical facts and the project's own identity (35), so no novelty or priority is claimed for it. The third should be checked against Coleman (1990) and Ogus (1990) before any manuscript text relies on it.

## Sources consulted

Cosgrave and Dilcher (2018) is at https://pu.edu.pk/images/journal/maths/PDF/Paper-1_50_4_2018.pdf, and Cosgrave and Dilcher (2008) at https://emis.univie.ac.at/journals/INTEGERS/papers/i39/i39.pdf. Cosgrave and Dilcher (2017), Mathematics of Computation 86, 899–933, was consulted by abstract at https://www.ams.org/journals/mcom/2017-86-304/S0025-5718-2016-03111-7. Stokes is arXiv:2207.07804, and Kashio is https://aif.centre-mersenne.org/item/10.5802/aif.3615.pdf and arXiv:1904.02879. The bibliographic entry for Ogus is at https://ftp.math.utah.edu/pub/tex/bib/idx/lnm1990/1454/0/319-341.html. Bostan, Gaudry and Schost is at https://cs.uwaterloo.ca/~eschost/publications/cartier.pdf. Costa, Gerbicz and Harvey is at https://arxiv.org/abs/1209.3436, Tal is at https://arxiv.org/abs/2607.29453, Hu is at https://arxiv.org/abs/2608.01781, and Mordell and Elia are cited via https://oeis.org/A265643. Full APA references are in Rounded_Third_Boundary_Note_20261009.md.
