"""Independent numerical check of the Voloch high-part / Semaev logarithmic-transfer normalization.

Written for the 20 October 2026 prior-work audit.  Uses NO inherited Cartier-Miller code.

Checks, on every rational point of every anomalous (trace 1) short Weierstrass curve
y^2 = F(x) = x^3 + A x + B over F_p for the primes listed:

 H1  b*T(a) == alpha_p(P),  P=(a,b) != O, where F^h = U + c_{p-1} x^{p-1} + x^p T(x), deg U <= p-2
     (Voloch 1990 eq. (2)/Prop. 1.3; Voloch 1997 p. 2 notation T; Voloch n.d. p. 3 notation M),
     and alpha_p(P) = [z^0] dlog f_{p,P}/dz at O, z = -x/y, i.e. Psi_p([(P)-(O)]) relative to
     omega_0 = dx/(2y), computed by a differentiated Miller chain with M = p.
 H1' the same constant from Semaev's evaluation at an auxiliary affine point R:
     phi(P) = (f'_{p,P}/f_{p,P})(R) (d/dx), so 2 y_R phi(P) should equal alpha_p(P).
 H2  P -> b T(a) is additive (homomorphism E(F_p) -> F_p).
 H3  C_F(a) := sum_{x != a} chi(F(x))/(x-a) == F'(a)/(2 b^2) - alpha_p(P)/b   (matched output).
 H4  trace -1 curves, chi(F(a)) = -1: C_F(a) == -d * C_G(d a), G = twist by d = F(a), and H3 on G.

Run: python3 -I voloch_semaev_normalization.py [--max-p 150] [--out results.json]
"""
import argparse, json, sys


def peval(c, x, p):
    v = 0
    for a in reversed(c):
        v = (v * x + a) % p
    return v


def polmul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        if u:
            for j, v in enumerate(b):
                r[i + j] = (r[i + j] + u * v) % p
    return r


def polpow(f, e, p):
    r, b = [1], list(f)
    while e:
        if e & 1:
            r = polmul(r, b, p)
        e >>= 1
        if e:
            b = polmul(b, b, p)
    return r


def legendre(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)


def sqrt_mod(a, p):
    a %= p
    for y in range(p):
        if y * y % p == a:
            return y
    raise ValueError


def ec_add(P, Q, A, p):
    """Chord-tangent addition on y^2 = x^3 + A x + B; returns (R, slope or None for vertical/identity)."""
    if P is None:
        return Q, None
    if Q is None:
        return P, None
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None, None
    if x1 == x2:
        lam = (3 * x1 * x1 + A) * pow(2 * y1, -1, p) % p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3), lam


def miller_alpha_at_O(P, M, A, p):
    """[z^0] dlog f_{M,P}/dz at O with z = -x/y.  Line y - lam x - nu = -z^{-3}(1 + lam z + ...)
    contributes +lam; verticals and identity steps contribute 0.  Left-to-right double-and-add."""
    T, alpha = P, 0
    for bit in bin(M)[3:]:
        T, lam = ec_add(T, T, A, p)
        alpha = (2 * alpha + (lam or 0)) % p
        if bit == '1':
            T, lam = ec_add(T, P, A, p)
            alpha = (alpha + (lam or 0)) % p
    return alpha, T


# --- dual numbers a + b*eps, eps^2 = 0, for Semaev-style evaluation at an affine point R
class Dual:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0):
        s.a, s.b = a, b


def dmul(u, v, p):
    return Dual(u.a * v.a % p, (u.a * v.b + u.b * v.a) % p)


def dinv(u, p):
    ia = pow(u.a, -1, p)
    return Dual(ia, (-u.b * ia * ia) % p)


def semaev_phi(P, M, A, p, R):
    """phi = (f'/f)(R) for f = f_{M,P} (div M(P) - ([M]P) - (M-1)(O)), derivative d/dx along E at R.
    Evaluates every Miller line ratio at the dual point R_eps = (x_R + eps, y_R + eps x'/...) and
    accumulates the logarithmic derivative.  f_{2n} = f_n^2 * l/v, f_{n+1} = f_n * l'/v'."""
    xr, yr = R
    dy = (3 * xr * xr + A) * pow(2 * yr, -1, p) % p          # dy/dx at R
    X, Y = Dual(xr, 1), Dual(yr, dy)

    def line_dlog(T1, T2):
        # returns (S, dlog(l/v) at R) where l is the chord/tangent through T1, T2 and v the vertical at S
        S, lam = ec_add(T1, T2, A, p)
        if T1 is None or T2 is None:
            return S, 0
        if S is None:                     # vertical line x - x1, no division
            l = Dual((xr - T1[0]) % p, 1)
            return S, l.b * pow(l.a, -1, p) % p
        x1, y1 = T1
        l = Dual((Y.a - y1 - lam * (X.a - x1)) % p, (Y.b - lam * X.b) % p)
        v = Dual((X.a - S[0]) % p, X.b)
        return S, (l.b * pow(l.a, -1, p) - v.b * pow(v.a, -1, p)) % p

    T, acc = P, 0
    for bit in bin(M)[3:]:
        T, d = line_dlog(T, T)
        acc = (2 * acc + d) % p
        if bit == '1':
            T, d = line_dlog(T, P)
            acc = (acc + d) % p
    return acc


def run(max_p):
    primes = [q for q in range(7, max_p + 1) if all(q % r for r in range(2, int(q ** .5) + 1))]
    out = {'primes': primes, 'anomalous_curves': 0, 'points': 0, 'H1_pass': 0, 'H1_fail': 0,
           'H1_semaev_pass': 0, 'H1_semaev_fail': 0, 'H1_semaev_skipped': 0,
           'H2_pairs': 0, 'H2_fail': 0, 'H3_pass': 0, 'H3_fail': 0,
           'trace_minus1_curves': 0, 'H4_points': 0, 'H4_fail': 0,
           'alternative_scalings_matching_H1': {}}
    alt = {'+1': 0, '-1': 0, '+2': 0, '-2': 0, '+1/2': 0, '-1/2': 0}
    for p in primes:
        h = (p - 1) // 2
        for A in range(p):
            for B in range(p):
                if (4 * A ** 3 + 27 * B * B) % p == 0:
                    continue
                F = [B, A, 0, 1]
                eps = [legendre(peval(F, x, p), p) for x in range(p)]
                tau = -sum(eps)                      # p + 1 - #E = -sum eps (one point at infinity)
                if tau not in (1, -1):
                    continue
                Fh = polpow(F, h, p)
                T = Fh[p:]                            # high part: coefficients c_p ... c_{3h}
                Fd = [A, 0, 3]
                pts = [(x, y) for x in range(p) for y in range(p) if (y * y - peval(F, x, p)) % p == 0]
                if tau == 1:
                    out['anomalous_curves'] += 1
                    vals = {}
                    for (a, b) in pts:
                        out['points'] += 1
                        alpha, end = miller_alpha_at_O((a, b), p, A, p)
                        assert end is None            # [p]P = O on an anomalous curve
                        lhs = b * peval(T, a, p) % p
                        vals[(a, b)] = lhs
                        if lhs == alpha:
                            out['H1_pass'] += 1
                        else:
                            out['H1_fail'] += 1
                        for k, c in (('+1', 1), ('-1', -1), ('+2', 2), ('-2', -2), ('+1/2', pow(2, -1, p)), ('-1/2', -pow(2, -1, p))):
                            alt[k] += (lhs == c * alpha % p)
                        # Semaev-style evaluation at an auxiliary affine point R not in the support
                        Rs = [R for R in pts if R[1] != 0 and R != (a, b) and R[0] != a]
                        if Rs:
                            R = Rs[0]
                            try:
                                phi = semaev_phi((a, b), p, A, p, R)
                                if 2 * R[1] * phi % p == alpha:
                                    out['H1_semaev_pass'] += 1
                                else:
                                    out['H1_semaev_fail'] += 1
                            except (ValueError, ZeroDivisionError):
                                out['H1_semaev_skipped'] += 1   # R met a zero/pole of a line
                        else:
                            out['H1_semaev_skipped'] += 1
                        # H3 matched weighted sum
                        if b:
                            C = sum(eps[x] * pow(x - a, -1, p) for x in range(p) if x != a) % p
                            pred = (peval(Fd, a, p) * pow(2 * b * b, -1, p) - alpha * pow(b, -1, p)) % p
                            out['H3_pass' if C == pred else 'H3_fail'] += 1
                    # H2 additivity on a sample of pairs (all pairs for small p)
                    plist = list(vals)
                    for i, P1 in enumerate(plist[:12]):
                        for P2 in plist[:12]:
                            S, _ = ec_add(P1, P2, A, p)
                            s = 0 if S is None else vals[S]
                            out['H2_pairs'] += 1
                            out['H2_fail'] += (s != (vals[P1] + vals[P2]) % p)
                else:
                    out['trace_minus1_curves'] += 1
                    for a in range(p):
                        d = peval(F, a, p)
                        if legendre(d, p) != -1:
                            continue
                        # twist by d: G(X) = d^3 F(X/d) = X^3 + A d^2 X + B d^3, point (d a, d^2), trace +1
                        G = [B * d ** 3 % p, A * d * d % p, 0, 1]
                        epsG = [legendre(peval(G, x, p), p) for x in range(p)]
                        assert -sum(epsG) == 1
                        Ca = sum(eps[x] * pow(x - a, -1, p) for x in range(p) if x != a) % p
                        X0, Y0 = d * a % p, d * d % p
                        assert (Y0 * Y0 - peval(G, X0, p)) % p == 0
                        alpha, end = miller_alpha_at_O((X0, Y0), p, G[1], p)
                        CG = (peval([G[1], 0, 3], X0, p) * pow(2 * Y0 * Y0, -1, p) - alpha * pow(Y0, -1, p)) % p
                        out['H4_points'] += 1
                        out['H4_fail'] += (Ca != (-d * CG) % p)
    out['alternative_scalings_matching_H1'] = alt
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-p', type=int, default=100)
    ap.add_argument('--out')
    args = ap.parse_args()
    res = run(args.max_p)
    res['status'] = 'PASS' if (res['H1_fail'] == res['H2_fail'] == res['H3_fail'] == res['H4_fail'] == res['H1_semaev_fail'] == 0) else 'FAIL'
    s = json.dumps(res, indent=1)
    print(s)
    if args.out:
        open(args.out, 'w').write(s + '\n')
