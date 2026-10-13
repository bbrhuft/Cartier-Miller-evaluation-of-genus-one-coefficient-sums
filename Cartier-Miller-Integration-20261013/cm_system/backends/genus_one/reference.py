"""Independent exact references for the row f^h and the weighted prefix S_f(lambda)."""
def row_recurrence(f, p):
    """c_0..c_{p-1} of f^h from f A' = h f' A:  m f0 c_m = sum_{j>=1} (h j - (m - j)) f_j c_{m-j}."""
    h = (p - 1)//2
    f = [c % p for c in f]
    d = len(f) - 1
    inv = [0, 1] + [0]*(p - 2)
    for i in range(2, p): inv[i] = (-(p//i) * inv[p % i]) % p
    c = [1] + [0]*(p - 1)
    for m in range(1, p):
        acc = 0
        for j in range(1, min(d, m) + 1):
            if f[j]: acc += (h*j - (m - j)) * f[j] * c[m - j]
        c[m] = acc % p * inv[m] % p
    return c

def row_power(f, p):
    """Independent check: truncated polynomial power by repeated squaring (FLINT)."""
    import flint
    ctx = flint.fmpz_mod_poly_ctx(p)
    P = ctx([c % p for c in f])
    R = P.pow_trunc((p - 1)//2, p)
    co = [int(x) for x in R.coeffs()]
    return co + [0]*(p - len(co))

def S_direct(c, lam, p):
    S = 0
    for cm in c: S = (S*lam + cm) % p           # Horner: sum c_m lam^{p-1-m}
    return S

def S_direct_ctx(c, lam, ctx):
    S = ctx.zero
    for cm in c: S = ctx.add(ctx.mul(S, lam), ctx.fromint(cm))
    return S
