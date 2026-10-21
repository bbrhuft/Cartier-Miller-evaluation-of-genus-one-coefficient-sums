"""Exploratory test (post-freeze, separately hashed) of a general-trace route suggested by
Voloch (1997): z^p - A z = -yT(x) (p. 2) and z(P+Q) = z(P) + z(Q) + (y(Q)-y(P))/(x(Q)-x(P)) (Prop. 2).
If both hold as stated for rational points, then for P = (a, b) in E(F_p) with p not dividing #E(F_p):
    b T(a) = (A - 1) z(Q'),  [p]Q' = P,  and  z([p]Q'') = alpha_p(Q'')  (p = 0 in F_p),
so  b T(a) = (A - 1) alpha_p([p^-2] P)  whenever the length-p Miller chain on [p^-2]P avoids O.
If instead the coordinates in Prop. 2 are pulled back along V (z lives on E^(p); the slope term is the
chord slope of V(P), V(Q) on E), the same argument gives  b T(a) = (A - 1) alpha_p([p^-1] P).
Environment VZ_EXP selects the exponent (2 or 1).  This script tests both readings and sign/scale
variants on short Weierstrass curves for small p.  It tests a conjectured consequence, not a stated
theorem.  Written 21 October 2026, post-freeze, separately hashed."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from cmbench import core


def add(P, Q, A, p):
    if P is None: return Q, 0, False
    if Q is None: return P, 0, False
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None, 0, True
    lam = ((3 * x1 * x1 + A) * pow(2 * y1, -1, p) if x1 == x2 else (y2 - y1) * pow(x2 - x1, -1, p)) % p
    x3 = (lam * lam - x1 - x2) % p
    return (x3, (lam * (x1 - x3) - y1) % p), lam, False


def mul(P, n, A, p):
    R, Q = None, P
    while n:
        if n & 1: R, _, _ = add(R, Q, A, p)
        Q, _, _ = add(Q, Q, A, p); n >>= 1
    return R


def alpha(P, M, A, p):
    T, a, hit = P, 0, False
    for bit in bin(M)[3:]:
        T, lam, v = add(T, T, A, p); hit |= v or T is None; a = (2 * a + lam) % p
        if bit == '1':
            T, lam, v = add(T, P, A, p); hit |= v or T is None; a = (a + lam) % p
    return a, hit


EXP = int(os.environ.get('VZ_EXP', '1'))
res = {'exponent_of_p_inverse': EXP, 'curves': 0, 'points': 0, 'clean': 0, 'chain_hits_O': 0}
variants = {'+(A-1)': 0, '-(A-1)': 0, '+2(A-1)': 0, '-2(A-1)': 0, '+(A-1)/2': 0, '-(A-1)/2': 0}
for p in [q for q in range(11, 80) if core.is_prime_small(q)]:
    h = (p - 1) // 2
    for A_ in range(p):
        for B_ in range(0, p, 3):
            if (4 * A_ ** 3 + 27 * B_ * B_) % p == 0: continue
            F = [B_, A_, 0, 1]
            pts = [(x, y) for x in range(p) for y in range(p) if (y * y - core.peval(F, x, p)) % p == 0]
            n = len(pts) + 1
            if n % p == 0: continue
            # high part T and Hasse invariant H = c_{p-1}
            c = [1]
            for _ in range(h):
                c2 = [0] * (len(c) + 3)
                for i, u in enumerate(c):
                    for j, v in enumerate(F):
                        c2[i + j] = (c2[i + j] + u * v) % p
                c = c2
            H, T = c[p - 1], c[p:]
            res['curves'] += 1
            for (a, b) in pts:
                if b == 0: continue
                res['points'] += 1
                P2 = mul((a, b), pow(p, -EXP, n), A_, p)
                if P2 is None: continue
                al, hit = alpha(P2, p, A_, p)
                if hit:
                    res['chain_hits_O'] += 1; continue
                res['clean'] += 1
                lhs = b * core.peval(T, a, p) % p
                for k, c0 in (('+(A-1)', 1), ('-(A-1)', -1), ('+2(A-1)', 2), ('-2(A-1)', -2), ('+(A-1)/2', pow(2, -1, p)), ('-(A-1)/2', -pow(2, -1, p))):
                    variants[k] += lhs == c0 * (H - 1) * al % p
res['variants_matching'] = variants
print(json.dumps(res))
if len(sys.argv) > 1: json.dump(res, open(sys.argv[1], 'w'), indent=1)
