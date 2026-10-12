"""C3: kappa == -sigma_V / t^2 (mod p), sigma_V = sum of x(Q) over the p-1 nonzero points of E[p](F_p-bar).

Method: Frobenius acts on E[p](F_p-bar) (cyclic of order p, ordinary) through the unit root, which is == t mod p,
so E[p] is rational over F_{p^k}, k = ord(t mod p).  Build F_{p^k} = F_p[X]/(f) with f irreducible
(Rabin test), #E(F_{p^k}) from s_k = alpha^k + beta^k, take a random x with F(x) a square in F_{p^k}
(Euler criterion), kill the prime-to-p part and reduce to an exact-order-p point using x-only Montgomery
ladder arithmetic (projective X:Z, Brier-Joye formulas, validated against affine arithmetic over F_p),
then sum x(iQ), i=1..p-1 (= 2 * sum_{i=1}^{(p-1)/2}).  Checks: sigma_V lies in F_p; p*Q = O; iQ != O.
"""
import sys, random
from common import *


class GF:
    def __init__(self, p, k):
        self.p, self.k = p, k
        self.f = self.find_irreducible() if k > 1 else [0, 1]
        self.q = p ** k

    # elements: tuples of length k (little endian)
    def mul(self, a, b):
        p, k, f = self.p, self.k, self.f
        r = [0] * (2 * k - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        r[i + j] += x * y
        # reduce mod f (monic degree k)
        for d in range(2 * k - 2, k - 1, -1):
            c = r[d] % p
            if c:
                for j in range(k):
                    r[d - k + j] -= c * f[j]
            r[d] = 0
        return tuple(x % p for x in r[:k])

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def sub(self, a, b):
        return tuple((x - y) % self.p for x, y in zip(a, b))

    def scal(self, c, a):
        return tuple((c * x) % self.p for x in a)

    def const(self, c):
        return tuple([c % self.p] + [0] * (self.k - 1))

    def zero(self):
        return self.const(0)

    def one(self):
        return self.const(1)

    def pow(self, a, e):
        r = self.one()
        while e:
            if e & 1:
                r = self.mul(r, a)
            e >>= 1
            if e:
                a = self.mul(a, a)
        return r

    def inv(self, a):
        return self.pow(a, self.q - 2)

    def rand(self):
        return tuple(random.randrange(self.p) for _ in range(self.k))

    def find_irreducible(self):
        p, k = self.p, self.k
        while True:
            f = [random.randrange(p) for _ in range(k)] + [1]
            if f[0] == 0:
                continue
            if self.rabin(f):
                return f

    def rabin(self, f):
        p, k = self.p, self.k
        # x^(p^k) == x mod f, and gcd(x^(p^(k/r)) - x, f) = 1 for primes r | k
        def polymulmod(a, b):
            r = pmul(a, b, p)
            return pdivmod_monic(r, f, p)[1]
        def frob_iter(n):
            # x^(p^n) mod f
            xp = [0, 1]
            for _ in range(n):
                # raise to p-th power
                res = [1]
                base = xp
                e = p
                while e:
                    if e & 1:
                        res = polymulmod(res, base)
                    e >>= 1
                    if e:
                        base = polymulmod(base, base)
                xp = res
            return xp
        if psub(frob_iter(k), [0, 1], p):
            return False
        primes = [r for r in range(2, k + 1) if k % r == 0 and is_prime(r)]
        for r in primes:
            g = psub(frob_iter(k // r), [0, 1], p)
            if not g:
                return False
            # gcd(g, f)
            a, b = f[:], g[:]
            while b:
                lc = pow(b[-1], -1, p)
                bm = pscale(b, lc, p)
                a, b = b, pdivmod_monic(a, bm, p)[1]
            if len(a) > 1:
                return False
        return True


# x-only arithmetic on y^2 = x^3 + a x + b, points as (X, Z)
def xdbl(K, P, a, b):
    X, Z = P
    X2 = K.mul(X, X); Z2 = K.mul(Z, Z)
    t = K.sub(X2, K.mul(K.const(a), Z2))
    XZ3 = K.mul(K.mul(X, Z), Z2)
    Xn = K.sub(K.mul(t, t), K.scal(8 * b, XZ3))
    inner = K.add(K.add(K.mul(X2, X), K.mul(K.const(a), K.mul(X, Z2))), K.scal(b, K.mul(Z2, Z)))
    Zn = K.scal(4, K.mul(Z, inner))
    return (Xn, Zn)


def xadd(K, P, Q, D, a, b):
    """x(P+Q) from x(P), x(Q), x(P-Q)=D (projective)"""
    XP, ZP = P; XQ, ZQ = Q; XD, ZD = D
    t1 = K.sub(K.mul(XP, XQ), K.mul(K.const(a), K.mul(ZP, ZQ)))
    ZZ = K.mul(ZP, ZQ)
    s = K.add(K.mul(XP, ZQ), K.mul(XQ, ZP))
    Xn = K.mul(ZD, K.sub(K.mul(t1, t1), K.scal(4 * b, K.mul(ZZ, s))))
    d = K.sub(K.mul(XP, ZQ), K.mul(XQ, ZP))
    Zn = K.mul(XD, K.mul(d, d))
    return (Xn, Zn)


def ladder(K, n, P, a, b):
    """x([n]P), n >= 1, P projective with Z != 0 (difference point P must be affine-ish)"""
    if n == 0:
        return (K.one(), K.zero())
    R0, R1 = P, xdbl(K, P, a, b)
    for bit in bin(n)[3:]:
        if bit == '1':
            R0, R1 = xadd(K, R1, R0, P, a, b), xdbl(K, R1, a, b)
        else:
            R0, R1 = xdbl(K, R0, a, b), xadd(K, R1, R0, P, a, b)
    return R0


def is_zero(K, P):
    return all(c == 0 for c in P[1])


def sigma_V(p, A, B, t):
    k = 1
    while pow(t, k, p) != 1:
        k += 1
    K = GF(p, k)
    # #E(F_{p^k})
    s0, s1 = 2, t
    for _ in range(k - 1):
        s0, s1 = s1, t * s1 - p * s0
    sk = s1 if k >= 1 else 2
    N = p ** k + 1 - sk
    v = 0
    m = N
    while m % p == 0:
        m //= p
        v += 1
    assert v >= 1
    for attempt in range(200):
        x = K.rand()
        if all(c == 0 for c in x):
            continue
        rhs = K.add(K.add(K.mul(K.mul(x, x), x), K.mul(K.const(A), x)), K.const(B))
        if all(c == 0 for c in rhs):
            continue
        if K.pow(rhs, (K.q - 1) // 2) != K.one():
            continue
        P = (x, K.one())
        R = ladder(K, m, P, A, B)
        if is_zero(K, R):
            continue
        # normalize, then multiply by p until order p
        bad = False
        for _ in range(v):
            zi = K.inv(R[1])
            Raff = (K.mul(R[0], zi), K.one())
            if all(c == 0 for c in Raff[0]):
                bad = True
                break
            S = ladder(K, p, Raff, A, B)
            if is_zero(K, S):
                break
            R = S
        if bad:
            continue
        zi = K.inv(R[1])
        Qpt = (K.mul(R[0], zi), K.one())
        if all(c == 0 for c in Qpt[0]):
            R = xdbl(K, Qpt, A, B)  # 2Q generates the same subgroup and has x != 0
            zi = K.inv(R[1])
            Qpt = (K.mul(R[0], zi), K.one())
        assert is_zero(K, ladder(K, p, Qpt, A, B))
        tot = K.zero()
        for i in range(1, (p - 1) // 2 + 1):
            Pi = ladder(K, i, Qpt, A, B)
            assert not is_zero(K, Pi)
            tot = K.add(tot, K.mul(Pi[0], K.inv(Pi[1])))
        tot = K.scal(2, tot)
        assert all(c == 0 for c in tot[1:]), "sigma_V not in F_p"
        return tot[0], k
    raise RuntimeError("no point found")


def selftest():
    # validate x-only formulas against affine arithmetic over F_p
    random.seed(5)
    p = 101
    K = GF(p, 1)
    for _ in range(20):
        A, B = random.randrange(p), random.randrange(p)
        if not nonsingular(p, A, B):
            continue
        pts = [(x, y) for x in range(p) for y in range(p) if (y * y - x ** 3 - A * x - B) % p == 0]
        P = random.choice(pts)
        if P[0] == 0:
            continue  # x-only differential addition degenerates when the difference point has x = 0
        def add(P1, P2):
            if P1 is None: return P2
            if P2 is None: return P1
            (x1, y1), (x2, y2) = P1, P2
            if x1 == x2 and (y1 + y2) % p == 0: return None
            if P1 == P2:
                l = (3 * x1 * x1 + A) * pow(2 * y1, -1, p) % p
            else:
                l = (y2 - y1) * pow(x2 - x1, -1, p) % p
            x3 = (l * l - x1 - x2) % p
            return (x3, (l * (x1 - x3) - y1) % p)
        Rr = None
        for n in range(1, 30):
            Rr = add(Rr, P)
            X = ladder(K, n, (K.const(P[0]), K.one()), A, B)
            if Rr is None:
                assert is_zero(K, X)
            else:
                assert not is_zero(K, X) and (X[0][0] * pow(X[1][0], -1, p)) % p == Rr[0], (n,)
    print("x-only ladder selftest OK")


if __name__ == "__main__":
    selftest()
    random.seed(2026)
    primes = [int(a) for a in sys.argv[1:]] or [7, 11, 13, 17, 19, 23]
    rows = load_targets()
    out = open("c3_results.txt", "a")
    for p in primes:
        ok = n = 0
        fails = []
        ks = {}
        for r in rows:
            if r['p'] != p:
                continue
            A, B, t, kap = r['A'], r['B'], r['trace'], r['kappa']
            sV, k = sigma_V(p, A, B, t)
            ks[k] = ks.get(k, 0) + 1
            pred = (-sV * pow(t * t, -1, p)) % p
            n += 1
            if pred == kap:
                ok += 1
            else:
                fails.append((A, B, t, sV, pred, kap))
        line = f"p={p}: ordinary models={n}, kappa == -sigma_V/t^2: {ok}/{n}; field degrees k used: {dict(sorted(ks.items()))}; fails={fails[:5]}"
        print(line, flush=True)
        out.write(line + "\n")
    out.close()
