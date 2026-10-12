"""Extra C1 checks: (i) Kedlaya matrix mod p is independent of the integral lift (random lifts A+p*r, B+p*s);
(ii) rank of M mod p is always 1, i.e. (H, beta) != (0, 0) (Katz's no-common-zero statement);
(iii) p = 5, outside the claim's range: recorded as INFORMATIONAL only, never counted as a pass."""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # explicit: python -I omits the script directory

import random
from common import *
from c1_kedlaya import frob_matrix, fr_mod
from c1_cech import frobenius_cech
from harness import base_parser, Run, run_main


def _main():
    ap = base_parser('C1 extra: lift independence, rank one, p = 5 informational')
    ap.add_argument('--lift-primes', type=int, nargs='*', default=[7, 11, 13])
    ap.add_argument('--rank-primes', type=int, nargs='*', default=[5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43])
    ap.add_argument('--seed', type=int, default=99)
    ap.add_argument('--skip-p5-informational', action='store_true')
    a = ap.parse_args()
    scope = vars(a).copy()
    scope.pop('out')

    def body(run):
        rng = random.Random(a.seed)
        for p in a.lift_primes:
            for A, B in all_models(p):
                H, beta = hasse_beta(p, A, B)
                At, Bt = A + p * rng.randrange(1, p ** 3), B + p * rng.randrange(1, p ** 3)
                M, prec = frob_matrix(p, At, Bt, 4, 6)
                Mi = [[fr_mod(M[r][c], p ** 2, p) for c in range(2)] for r in range(2)]
                t = trace(p, A, B)
                good = ((Mi[0][0] + Mi[1][1]) % p ** 2 == t % p ** 2
                        and (Mi[0][0] * Mi[1][1] - Mi[0][1] * Mi[1][0]) % p ** 2 == p
                        and [[x % p for x in r] for r in Mi] == [[0, (-beta) % p], [0, H]])
                run.check(good, {'p': p, 'A': A, 'B': B, 'lift': (At, Bt), 'M': Mi}, group=f'random_lift_p{p}')
        for p in a.rank_primes:
            for A, B in all_models(p):
                run.check(hasse_beta(p, A, B) != (0, 0), {'p': p, 'A': A, 'B': B}, group='rank_one')
        if not a.skip_p5_informational:
            p = 5
            okc = okk = n = 0
            nonint = []
            for A, B in all_models(p):
                H, beta = hasse_beta(p, A, B)
                c, Mc = frobenius_cech(p, A, B)
                n += 1
                okc += (Mc == [[0, (-beta) % p], [0, H]])
                M, prec = frob_matrix(p, A, B, 5, 8)
                try:
                    Mi = [[fr_mod(M[r][c], p ** 2, p) for c in range(2)] for r in range(2)]
                    okk += ([[x % p for x in r] for r in Mi] == [[0, (-beta) % p], [0, H]])
                except ValueError:
                    nonint.append((A, B))
            run.note('p5_outside_claim', {'models': n, 'cech_matches': okc, 'kedlaya_matches': okk,
                                          'nonintegral': nonint[:5]})

    run_main(lambda: Run('c1_extra', scope, a.out), body)


if __name__ == "__main__":
    _main()
