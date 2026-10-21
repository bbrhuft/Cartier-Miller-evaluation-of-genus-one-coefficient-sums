"""Companion to voloch_zeta_general_trace.py (post-freeze, separately hashed): tests
b T(a) = (A - 1) alpha_p([p^-1] P) in exactly the cases that script excludes, where the length-p
double-and-add chain passes through O, using Miller's conventions (vertical and identity steps
contribute 0).  Short Weierstrass curves y^2 = x^3 + A x + B, B even, 11 <= p < 60, p not | #E."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
src = open(os.path.join(HERE, 'voloch_zeta_general_trace.py')).read().split("EXP = int(")[0]
exec(compile(src, 'voloch_zeta_general_trace.py', 'exec'))
from cmbench import core
ok = bad = 0
for p in [q for q in range(11, 60) if core.is_prime_small(q)]:
    h = (p - 1) // 2
    for A_ in range(p):
        for B_ in range(0, p, 2):
            if (4 * A_ ** 3 + 27 * B_ * B_) % p == 0:
                continue
            F = [B_, A_, 0, 1]
            pts = [(x, y) for x in range(p) for y in range(p) if (y * y - core.peval(F, x, p)) % p == 0]
            n = len(pts) + 1
            if n % p == 0:
                continue
            c = [1]
            for _ in range(h):
                c2 = [0] * (len(c) + 3)
                for i, u in enumerate(c):
                    for j, v in enumerate(F):
                        c2[i + j] = (c2[i + j] + u * v) % p
                c = c2
            H, T = c[p - 1], c[p:]
            for (a, b) in pts:
                if b == 0:
                    continue
                P2 = mul((a, b), pow(p, -1, n), A_, p)
                al, hit = alpha(P2, p, A_, p)
                if not hit:
                    continue
                if b * core.peval(T, a, p) % p == (H - 1) * al % p:
                    ok += 1
                else:
                    bad += 1
res = {'chain_through_O_cases': ok + bad, 'identity_holds': ok, 'fails': bad, 'status': 'PASS' if bad == 0 else 'FAIL'}
print(json.dumps(res))
if len(sys.argv) > 1:
    json.dump(res, open(sys.argv[1], 'w'), indent=1)
