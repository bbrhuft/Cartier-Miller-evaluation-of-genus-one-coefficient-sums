"""Amendment R3.1 of the Jacobi-sum reconstruction (r3/jacobi.py is frozen and unchanged).

Reason: frozen confirmation run 1 stopped at p = 3000013781, q = 89 (class B): FLINT LLL with
delta 0.99 missed the minimum and the frozen fallback, PARI qfminim with flag 0, cannot accept
Gram entries of size (qp)^2 (its documented floating-point mode needs d*max|G|^2 < 2^53).
Change: the lattice step only.  Deterministic chain, every candidate certified exactly
(x in the ideal, x*xbar = p in Z[zeta_q], van Wamelen selection), as before:
  1. FLINT LLL, delta 0.999, on the integral embedding E(x) = q(x,0) - (sum x) 1;
  2. FLINT LLL, delta 0.9999, applied to the output of step 1;
  3. up to RETRIES re-randomised bases (each basis row plus or minus one other row, choices from
     random.Random(hash of (p, q, S, attempt))), each reduced with delta 0.999;
  4. otherwise raise ArithmeticError (callers fall back; no value is ever guessed).
No enumeration is used.  Correctness never depends on LLL: only termination does.
"""
import random

from .jacobi import JacobiContext, ideal_basis

RETRIES = 4


class JacobiContextR31(JacobiContext):
    def __init__(self, p, q, eta=None):
        super().__init__(p, q, eta=eta, method='flint')
        self.stats.update(lll_stage=None, lll_attempts=0)

    def _svp(self, S, method='flint'):
        from time import perf_counter
        import flint
        p, q = self.p, self.q
        d = q - 1
        target = q * d * p                      # |E(x)|^2 = q Tr(x xbar) = q (q-1) p

        def emb(b):
            s = sum(b)
            return [q * v - s for v in b] + [-s]

        def hit(R):
            for i in range(R.nrows()):
                row = [int(R[i, j]) for j in range(q)]
                if sum(v * v for v in row) == target:
                    s = -row[q - 1]
                    return [(row[j] + s) // q for j in range(d)]
            return None

        B = ideal_basis(p, q, self.eta, S)
        t0 = perf_counter()
        R = flint.fmpz_mat([emb(b) for b in B]).lll(delta=0.999)
        self.stats['lll_attempts'] += 1
        x = hit(R)
        stage = 'delta0.999'
        if x is None:
            R = R.lll(delta=0.9999)
            self.stats['lll_attempts'] += 1
            x = hit(R)
            stage = 'delta0.9999'
        k = 0
        while x is None and k < RETRIES:
            rng = random.Random(hash((p, q, tuple(S), k)) & ((1 << 61) - 1))
            rows = [list(b) for b in B]
            for i in range(d):
                j = rng.randrange(d)
                if j != i:
                    c = rng.choice((-1, 1))
                    rows[i] = [a + c * b for a, b in zip(rows[i], rows[j])]
            R = flint.fmpz_mat([emb(b) for b in rows]).lll(delta=0.999)
            self.stats['lll_attempts'] += 1
            x = hit(R)
            k += 1
            stage = 'rerandomised%d' % k
        self.stats['lll_seconds'] += perf_counter() - t0
        if x is None:
            self.stats['enumeration_fallbacks'] += 1
            raise ArithmeticError('R3.1 lattice chain did not reach the minimum (q=%d)' % q)
        self.stats['lll_stage'] = stage
        return x
