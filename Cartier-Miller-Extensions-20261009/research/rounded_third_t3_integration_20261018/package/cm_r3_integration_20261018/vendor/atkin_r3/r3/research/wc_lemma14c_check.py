"""Round-3 development: exact checks of Williams & Currie (1982) Lemma 14(c) and of the
algebraic equivalences used to promote round-2 identity (*).

For p = 1 mod 4 and p = 2 mod 3 (p = 5 mod 12), with q0 = (p-1)/4, hD = h(-3p), H = ((p-1)/2)!:
  (WC)   (-3)^{q0} = (-1)^{(hD-2)/4} H                         [Lemma 14(c), background]
  (H)    H = (-1)^{q0 + (hD-2)/4} 3^{q0}                         [rearrangement]
  (*)    H = (2/p) (m!/p) 3^{q0},  (m!/p) = (-1)^{(m - hD/2)/2}  [round-2 form]
  (S)    sum_{j<=m} (j/p) = hD/2                                 [Polya-Fourier + class number formula]
  (R)    hD = 2 mod 4                                            [Redei; needed for (WC) to make sense]
  (Q2)   (m!/N!)^2 = (-1)^{(hD-2)/4} a,  p = a^2+b^2, a = 1 mod 4 [quarter consequence]
Reference H from FLINT's n_factorial_fast_mod2_preinv; h(-3p) from PARI qfbclassno inside its
documented unconditional range, and from the reduced-form count on a subrange.
Usage: python3 -I r3/research/wc_lemma14c_check.py LIMIT FORMS_LIMIT OUT.json
"""
import json
import sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from r3.common import (is_prime, params, legendre, classno_qfb_unconditional, classno_forms,
                       flint_factorial)


def two_squares_a(p):
    """a with p = a^2 + b^2, a odd, a = 1 mod 4 (Cornacchia with a deterministic sqrt(-1))."""
    from math import isqrt
    # find a quadratic non-residue deterministically to get sqrt(-1)
    z = 2
    while legendre(z, p) != -1:
        z += 1
    r = pow(z, (p - 1) // 4, p)
    a0, b0 = p, min(r, p - r)
    lim = isqrt(p)
    while b0 > lim:
        a0, b0 = b0, a0 % b0
    x = b0
    y = isqrt(p - x * x)
    assert x * x + y * y == p
    a = x if x % 2 else y
    return a if a % 4 == 1 else -a


def main(limit, forms_limit, out):
    t0 = perf_counter()
    counts = dict(primes=0, forms_crosscheck=0)
    first_last = []
    for p in range(17, limit, 12):          # p = 5 mod 12, p >= 17
        if not is_prime(p):
            continue
        P = params(p)
        m, h, N, q0 = P['m'], P['h'], P['N'], P['q0']
        H = flint_factorial(h, p)
        hD = classno_qfb_unconditional(-3 * p)
        if p < forms_limit:
            assert classno_forms(-3 * p) == hD, p
            counts['forms_crosscheck'] += 1
        assert hD % 4 == 2, ('Redei', p, hD)                                   # (R)
        sgn = -1 if ((hD - 2) // 4) % 2 else 1
        assert pow(-3, q0, p) == sgn * H % p, ('WC', p)                         # (WC)
        sgn2 = -1 if (q0 + (hD - 2) // 4) % 2 else 1
        assert H == sgn2 * pow(3, q0, p) % p                                     # (H)
        mf = flint_factorial(m, p)
        S = None
        if p < 30000:
            sq = bytearray(p)
            for x in range(1, h + 1):
                sq[x * x % p] = 1
            S = sum(1 if sq[j] else -1 for j in range(1, m + 1))
        if S is not None:
            assert S == hD // 2                                                  # (S)
        lm = legendre(mf, p)
        assert lm == (-1 if ((m - hD // 2) // 2) % 2 else 1)                     # (m!/p)
        assert legendre(2, p) == (-1 if q0 % 2 else 1)                           # (2/p)=(-1)^q0
        assert H == legendre(2, p) * lm * pow(3, q0, p) % p                      # (*)
        a = two_squares_a(p)
        Nf = flint_factorial(N, p)
        r = mf * pow(Nf, p - 2, p) % p
        assert r * r % p == sgn * a % p, ('Q2', p)                               # (Q2)
        assert pow(r, 4, p) == a * a % p
        counts['primes'] += 1
        if counts['primes'] <= 3:
            first_last.append(p)
        last = p
    rec = dict(role='Round-3 development (background-theorem verification); inputs excluded from '
                    'round-3 confirmation',
               range='all primes p = 5 (mod 12), 17 <= p < %d' % limit,
               forms_crosscheck_below=forms_limit, counts=counts, first=first_last, last=last,
               checks=['R: h(-3p)=2 mod 4', 'WC: (-3)^q0 = (-1)^((h-2)/4) H', 'H rearranged',
                       'S: sum_{j<=m}(j/p)=h/2 (p<30000)', '(m!/p) from h',
                       '(2/p)=(-1)^q0', '(*) round-2 form', 'Q2: (m!/N!)^2 = (-1)^((h-2)/4) a',
                       '(m!/N!)^4=a^2'],
               reference='H, m!, N! from FLINT n_factorial_fast_mod2_preinv; h(-3p) from PARI '
                         'qfbclassno(D,0) with |D|<2e10, reduced-form count below forms limit',
               seconds=perf_counter() - t0, pass_=True)
    Path(out).write_text(json.dumps(rec, indent=2) + '\n')
    print(json.dumps({k: rec[k] for k in ('range', 'counts', 'seconds', 'pass_')}))


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
