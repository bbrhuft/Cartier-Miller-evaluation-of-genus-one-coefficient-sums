"""Pointwise check of the decomposition used in (A7) / cmbench.methods.VolochSemaev:

  on v^2 = g(z), g(0) = 1 (cubic or quartic), with the Connell short model (X, Y), origin P+ = (0, 1),
  and R = image of P- = (0, -1):     1/z = (1/2) (Y + Y_R)/(X - X_R) - g_1/4

at every affine point (z, v), z != 0, whose image has X != X_R.  Independent of the inherited code
(uses cmbench.methods.connell_short only for A, B, R and re-implements the point map).
Also checks the summed identity sum_{P != O, R} (Y+Y_R)/(X-X_R) = -alpha_p(R) on anomalous curves.
Written 21 October 2026 (post-freeze; separately hashed, not part of FREEZE.json)."""
import json, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from cmbench import core
from cmbench.methods import connell_short, miller_transfer


def to_short(g, p, z, v):
    g = list(g) + [0] * (5 - len(g))
    f1, f2, f3 = g[1], g[2], g[3]
    i = lambda n: pow(n, -1, p)
    x = (2 * (v + 1) + f1 * z) * i(z * z) % p
    y = (4 * (v + 1) + 2 * (f1 * z + f2 * z * z) - f1 * f1 * z * z * i(2)) * i(z ** 3) % p
    a1, a2, a3 = f1, (f2 - f1 * f1 * i(4)) % p, 2 * f3 % p
    b2 = (a1 * a1 + 4 * a2) % p
    return (x + b2 * i(12)) % p, (y + (a1 * x + a3) * i(2)) % p


rng = random.Random(20261021)
out = {'pointwise_checks': 0, 'pointwise_fail': 0, 'on_curve_fail': 0, 'sum_checks': 0, 'sum_fail': 0}
for p in [q for q in range(11, 400) if core.is_prime_small(q)]:
    for d in (3, 4):
        for _ in range(3):
            while True:
                g = [1] + [rng.randrange(p) for _ in range(d - 1)] + [rng.randrange(1, p)]
                if core.squarefree(g, p):
                    break
            A, B, R = connell_short(g, p)
            sq = {}
            for y in range(p):
                sq.setdefault(y * y % p, []).append(y)
            S = 0
            npts = 0
            for z in range(1, p):
                gv = core.peval(g, z, p)
                for v in sq.get(gv, []):
                    X, Y = to_short(g, p, z, v)
                    if (Y * Y - (X ** 3 + A * X + B)) % p:
                        out['on_curve_fail'] += 1
                    if X == R[0]:
                        continue
                    hR = (Y + R[1]) * pow(X - R[0], -1, p) % p
                    out['pointwise_checks'] += 1
                    if (pow(z, -1, p) - (hR * pow(2, -1, p) - g[1] * pow(4, -1, p))) % p:
                        out['pointwise_fail'] += 1
            # summed identity on the short model when it is anomalous
            W = [B, A, 0, 1]
            eps = [core.legendre(core.peval(W, x, p), p) for x in range(p)]
            if -sum(eps) == 1:
                tot = 0
                for x in range(p):
                    for y in sq.get(core.peval(W, x, p), []):
                        if (x, y) == R:
                            continue
                        if x == R[0]:       # the point -R: regular limit W'(X_R)/(-2 Y_R)
                            tot += (3 * x * x + A) * pow(-2 * R[1], -1, p)
                        else:
                            tot += (y + R[1]) * pow(x - R[0], -1, p)
                alpha, end = miller_transfer(R, p, A, p)
                out['sum_checks'] += 1
                out['sum_fail'] += (tot - (-alpha)) % p != 0
out['status'] = 'PASS' if not (out['pointwise_fail'] or out['on_curve_fail'] or out['sum_fail']) else 'FAIL'
print(json.dumps(out))
if len(sys.argv) > 1:
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
