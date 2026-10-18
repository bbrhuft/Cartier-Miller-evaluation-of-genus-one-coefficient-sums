# Frozen candidate (round 2): characteristic-p half-interval acquisition

Frozen before any confirmation prime of this round is selected. It extends the frozen round-1 candidate (`CANDIDATE.md`, `evidence/FREEZE.json`), which is unchanged.

Input: a certified prime p >= 11 with p = 5 (mod 6). Put m = (p-2)/3, h = (p-1)/2, N = floor((p-5)/12), H = h! mod p, and P = prod_{j=m+1}^{h} j. The product P has (p+1)/6 factors.

## Statements to be confirmed

**C1. Exact identity.** m! = H/P, and H^4 = 1. Hence c_p = 2 (m!)^{-3} = 2 H P^3 (mod p).

**C2. Mordell route (theorem; Mordell 1961).** For p = 3 (mod 4), H = (-1)^{(h(-p)+1)/2}.

**C3. Gauss route (theorem; Gauss 1828 with Dirichlet's class number formula).** Take p = 5 (mod 8). Let q = (p-1)/4 and p = a^2 + b^2 with a = 1 (mod 4). The value lambda = (q!/p) equals (-1)^{(q - h(-4p)/2)/2}. Then H is the unique square root of -1 with H^q = lambda (2a)^q.

**C4. Conjecture (\*) (finite evidence only).** For p = 1 (mod 4) and p = 2 (mod 3), H = (2/p) (m!/p) 3^{(p-1)/4}, where (m!/p) = (-1)^{(m - h(-3p)/2)/2}. For p = 17 (mod 24) this is the only route used, so the method is conditional there.

**C5. Quarter identity (proved in the report).** For p = 5 (mod 12), (m! q!/N!)^4 = -1/4 and (m!/N!)^4 = a^2 (mod p). So N!, a product of about p/12 factors, determines c_p up to a 4th root of unity. Even with class-number Legendre symbols, one sign remains. That sign is the recorded first exact failure.

**C6. Formal obstruction (proved in the report).** Fix p = 2 (mod 3). The odd functional Phi([x]) = avg_u chi_{-3}(u) B1bar(ux) vanishes on reflection, Gauss multiplication and Gross–Koblitz orbit relations of every conductor prime to p, and Phi([1/3]) = -1/6. Consequently, an identity for Gamma_p(1/3)^e with e != 0 must contain a translation (an interval product). If every point it uses has conductor at most Q, that interval has length at least p/Q^2 - 2.

**C7. Conductor-12 exact relation lattice (finite evidence).** The lattice is computed empirically from the 11 grid factorials and the polylog constants -1, 2, 3, cube roots of 2 and 3, a, b, 3^{(p-1)/4} and parity signs. Without class-number constants, every exact representation of m!^{+-1} or m!^{+-3} by intervals between grid residues has total length at least 2N. Adding the class-number Legendre symbols of the grid factorials allows a single interval of length about p/6, but never a length-N interval.

## Operations and full cost

The cost charged consists of the following parts:

- one rising-product channel of length (p+1)/6 (layout 1), or two channels of length about (p+1)/12 sharing one tree (layout 2);
- one class number: h(-p) for p = 3 (mod 4), h(-4p) for p = 5 (mod 8), and h(-3p) for p = 17 (mod 24). The stdlib method counts reduced forms in O(|D|^{1/2} polylog) operations. The optional PARI quadclassunit is subexponential, but its correctness is conditional on GRH;
- for C3, Cornacchia with the deterministic square root of -1 = 2^{(p-1)/4};
- O(log p) powerings and the final normalization.

The asymptotic class stays O(M(sqrt p) log p). Any gain is a constant factor. The product's total length equals that of the nodal anchor (2N+O(1)), but here it sits in one channel instead of two.

## Development inputs (excluded from confirmation)

- All admissible primes below 200000, used in exploration, the lattice computations and the (\*) checks.
- Primes used in pilots or tests: 1000003, 10000019, 100000037, 1000000021, 100000007, 1000000007, 10000000019.
- All round-1 development and confirmation primes, as listed in evidence/FREEZE.json and evidence/CONFIRMATION.json.

## Confirmation rule

Use three classes: A (p = 11 mod 12), B (p = 5 mod 24) and C (p = 17 mod 24).

- Small set: the first 3 primes of each class above 300000 that are not development inputs.
- Large set: for each class and each k in {6,7,8,9,10,11}, the first prime of that class at or above 2*10^k that is not a development input.

Every case is checked as follows:

- c_p is compared with the reference 2(m!)^{-3}, where m! comes from FLINT's n_factorial_fast_mod2_preinv. For p <= 2*10^6 there is also an independent stdlib linear loop.
- H is compared with FLINT's h!.
- Every applicable route is evaluated. For class B, C3 and C4 are compared.
- The stdlib class number is compared with PARI's quadclassunit.
- Both layouts are evaluated, using the stdlib engine for p <= 2*10^9 and the FLINT engine for all p.

## Benchmark rule

The benchmark runs only after exact confirmation, on the large set. Each method gets five cold samples, with method order rotated. Every method returns c_p and includes all setup, the class number and the normalization.

- Stdlib engine (p <= 2*10^9): factorial block, nodal shared, HI layout 1 and HI layout 2, each with the forms class number.
- FLINT engine (all p): FLINT native factorial, FLINT block factorial, FLINT nodal (shared tree), and FLINT HI layouts 1 and 2. The class number for these comes from PARI quadclassunit; HI layout 1 is also timed with the forms class number.

All samples are recorded. Nothing is extrapolated beyond 2*10^11, and no claim is made against BGS-shifting implementations, which are not included.
