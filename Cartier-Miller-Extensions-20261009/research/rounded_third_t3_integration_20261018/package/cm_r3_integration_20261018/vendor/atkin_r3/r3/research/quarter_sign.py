"""Round-3 DEVELOPMENT: the residual sign of the quarter identity (secondary target).

For p = 5 mod 12 put r = m!/N!.  Proved: r^2 = eps*a with eps = (-1)^{(h(-3p)-2)/4}, p = a^2+b^2,
a = 1 mod 4 (round-2 C5 + Williams-Currie).  The two candidates are +-r.
Class B (p = 5 mod 8): -1 is a square but not a fourth power, so the bit is carried by the quartic
character lambda = r^{(p-1)/4}; normalise by the class-number-known H (H^2 = -1):
    beta = lambda            if lambda in {+1,-1}
    beta = lambda / H        if lambda in {+H,-H}
Class C (p = 1 mod 8): use the character of order 2^v, v = v_2(p-1), normalised the same way by a
fixed generator of the 2-Sylow (eta2 = z^{(p-1)/2^v} for the least non-residue z).
Checks:
  (i)  r^2 = eps*a.
  (ii) Polya-Fourier form (class B): beta is determined by the Gaussian integer
       S4 = sum_{N<j<=m} chi_4(j) together with S2 = sum (j/p) and the length (exact identity).
  (iii) Whether beta is a function of cheap invariants: a, b mod 2^k and mod 3, h(-3p), h(-4p),
       h(-8p) mod 2^k, quartic symbols (2/p)_4, (3/p)_4.  The first collision (two primes with the
       same invariant tuple and opposite beta) is recorded as the exact failure for that tuple.
Usage: python3 r3/research/quarter_sign.py LIMIT OUT.json
"""
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from r3.common import is_prime, flint_factorial, classno_qfb_unconditional, legendre
from r3.research.wc_lemma14c_check import two_squares_a


def v2(n):
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


def main(limit, out):
    recs = []
    for p in range(17, limit, 12):
        if not is_prime(p):
            continue
        q0, m, N, h = (p - 1) // 4, (p - 2) // 3, (p - 5) // 12, (p - 1) // 2
        hD = classno_qfb_unconditional(-3 * p)
        eps = -1 if ((hD - 2) // 4) % 2 else 1
        a = two_squares_a(p)
        b = 0
        from math import isqrt
        b = isqrt(p - a * a)
        H = flint_factorial(h, p)
        # Williams-Currie normalisation of the sign of b: b = H a (mod p)
        if (b - H * a) % p:
            b = -b
        assert (b - H * a) % p == 0
        mf, Nf = flint_factorial(m, p), flint_factorial(N, p)
        r = mf * pow(Nf, p - 2, p) % p
        assert r * r % p == eps * a % p                                      # (i)
        v = v2(p - 1)
        z = 2
        while legendre(z, p) != -1:
            z += 1
        e = (p - 1) >> v
        lam = pow(r, e, p)                     # 2-Sylow component of r, order | 2^v
        # r -> -r multiplies lam by (-1)^e = -1 (e odd); normalise by a canonical 2^v-th root
        # of unity: the class of lam^2 is known (from r^2), take the root lam0 = (r^2)^{e*...}
        lam2 = pow(r * r % p, e, p)            # known quantity (depends only on eps*a)
        # canonical square root of lam2 inside the 2-Sylow: power of eta2 = z^e
        eta2 = pow(z, e, p)
        k = next(i for i in range(1 << v) if pow(eta2, 2 * i, p) == lam2)
        root = pow(eta2, k, p)                 # one of the two roots, chosen canonically
        beta = 1 if lam == root else -1
        assert lam in (root, p - root)
        rec = dict(p=p, cls='B' if p % 8 == 5 else 'C', beta=beta, eps=eps, a=a, b=b, h3p=hD,
                   v2=v)
        if p % 8 == 5:
            # (ii) Polya-Fourier: beta from S4, S2, length (class B only, p < 2e5)
            if p < 200000:
                chi = {}
                g = z                          # z is a non-residue; for p=5 mod 8 use quartic char
                # quartic character via x^{q0}: values in {1, I, -1, -I}, I = 2^{q0} (2 is a QNR)
                I = pow(2, q0, p)
                code = {1: 0, I: 1, p - 1: 2, p - I: 3}
                n = [0, 0, 0, 0]
                for j in range(N + 1, m + 1):
                    n[code[pow(j, q0, p)]] += 1
                lam_from_counts = pow(I, (n[1] + 2 * n[2] + 3 * n[3]) % 4, p)
                assert lam_from_counts == pow(r, q0, p)
                rec['S4'] = [n[0] - n[2], n[1] - n[3]]
                rec['S2'] = n[0] + n[2] - n[1] - n[3]
        recs.append(rec)
    # cheap-invariant collision test
    def feats(rec, kind):
        p, a, b = rec['p'], rec['a'], rec['b']
        if kind == 'ab_mod_24':
            return (a % 24, b % 24)
        if kind == 'ab_mod_48_h3p_mod_32':
            return (a % 48, b % 48, rec['h3p'] % 32)
        if kind == 'p_mod_96_ab_mod_24_h3p_mod_64':
            return (p % 96, a % 24, b % 24, rec['h3p'] % 64)
        if kind == 'quartic_23':
            q0 = (p - 1) // 4
            return (pow(2, q0, p) in (1, p - 1), pow(3, q0, p) in (1, p - 1), a % 8, b % 8, rec['h3p'] % 16)
        raise ValueError
    tests = {}
    for kind in ('ab_mod_24', 'ab_mod_48_h3p_mod_32', 'p_mod_96_ab_mod_24_h3p_mod_64', 'quartic_23'):
        for cls in ('B', 'C'):
            seen, first = {}, None
            for rec in recs:
                if rec['cls'] != cls:
                    continue
                f = feats(rec, kind)
                if f in seen and seen[f][0] != rec['beta'] and first is None:
                    first = dict(features=list(map(lambda x: x if not isinstance(x, bool) else int(x), f)),
                                 p1=seen[f][1], beta1=seen[f][0], p2=rec['p'], beta2=rec['beta'])
                seen.setdefault(f, (rec['beta'], rec['p']))
            groups = {}
            for rec in recs:
                if rec['cls'] == cls:
                    groups.setdefault(feats(rec, kind), []).append(rec['beta'])
            mixed = sum(1 for g in groups.values() if len(set(g)) > 1)
            tests['%s/%s' % (kind, cls)] = dict(groups=len(groups), mixed_groups=mixed,
                                                 primes=sum(len(g) for g in groups.values()),
                                                 first_collision=first)
    nB = sum(1 for r_ in recs if r_['cls'] == 'B')
    plusB = sum(1 for r_ in recs if r_['cls'] == 'B' and r_['beta'] == 1)
    res = dict(role='Round-3 development (secondary target); inputs excluded from confirmation',
               limit=limit, primes=len(recs), classB=nB, classB_beta_plus=plusB, tests=tests,
               polya_fourier_checked=sum(1 for r_ in recs if 'S4' in r_), records=recs)
    Path(out).write_text(json.dumps(res, indent=1) + '\n')
    print(json.dumps({k: v for k, v in res.items() if k != 'records'}, indent=1))


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
