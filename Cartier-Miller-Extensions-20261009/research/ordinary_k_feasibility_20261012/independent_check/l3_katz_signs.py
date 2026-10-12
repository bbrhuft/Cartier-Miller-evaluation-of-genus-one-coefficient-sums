"""Signs in Katz's Section-6 character-sum formulas, in Katz's model y^2 = f(x) = 4x^3 - g2 x - g3,
a_p = [x^(p-1)] f^h, b_p = [x^(p-2)] f^h (mod p), nu the quadratic character with nu(0) = 0.
Checked claim: a_p == -S0 and b_p == -S1 for every nonsingular model.  The '+' agreements are
recorded as informational counts only (they occur exactly when the value is 0)."""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # explicit: python -I omits the script directory

from common import *
from harness import base_parser, Run, run_main


def _main():
    ap = base_parser('Katz Section 6 sign check')
    ap.add_argument('--primes', type=int, nargs='*', default=[5, 7, 11, 13, 17, 19, 23, 29, 31])
    a = ap.parse_args()
    scope = {'primes': a.primes, 'models': 'all nonsingular (g2, g3)'}

    def body(run):
        plus = {}
        for p in a.primes:
            h = (p - 1) // 2
            pc = {'a=+S0': 0, 'b=+S1': 0}
            for g2 in range(p):
                for g3 in range(p):
                    if (g2 ** 3 - 27 * g3 ** 2) % p == 0:
                        continue
                    f = ptrim([(-g3) % p, (-g2) % p, 0, 4])
                    fh = ppow(f, h, p)
                    av, bv = coeff(fh, p - 1), coeff(fh, p - 2)
                    S0 = sum(legendre(4 * t ** 3 - g2 * t - g3, p) for t in range(p)) % p
                    S1 = sum(t * legendre(4 * t ** 3 - g2 * t - g3, p) for t in range(p)) % p
                    run.check(av == (-S0) % p, {'p': p, 'g2': g2, 'g3': g3}, group='a_p == -S0')
                    run.check(bv == (-S1) % p, {'p': p, 'g2': g2, 'g3': g3}, group='b_p == -S1')
                    pc['a=+S0'] += av == S0
                    pc['b=+S1'] += bv == S1
            plus[p] = pc
        run.note('plus_sign_agreements_informational', plus)

    run_main(lambda: Run('l3_katz_signs', scope, a.out), body)


if __name__ == "__main__":
    _main()
