"""Exact (j, S) pairing tables, R_D(J) in Q[J]/(H_D), class-polynomial
cross-check against PARI polclass (practical comparator, not a certificate),
denominator/discriminant prime factorizations (trial division, multiplied
back), and analytic corroboration of S = s_2(tau_Q) at every complex
embedding with an explicit q-series tail bound.
"""
import json, sys, itertools, math
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/theory/', 1)[0] + '/theory')
sys.path.insert(0, __file__.rsplit('/theory/', 1)[0] + '/core')
import family_loops as FL
from mpmath import mp, mpf, mpc, sqrt as msqrt, pi, exp as mexp, log as mlog, fabs
mp.dps = 90

def factor_int(n):
    n = abs(int(n)); f = {}; d = 2
    if n == 0: return {'0': 1}
    while d*d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1; n //= d
        d += 1 if d == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def check_factor(n, f):
    p = 1
    for q, e in f.items(): p *= q**e
    return p == abs(n)

def is_prime_td(n):
    if n < 2: return False
    d = 2
    while d*d <= n:
        if n % d == 0: return False
        d += 1
    return True

def solve_rational(rows, rhs):
    """Exact least-squares-free solve of an overdetermined consistent system."""
    m = len(rows[0]); M = [list(r) + [b] for r, b in zip(rows, rhs)]
    piv = []; r = 0
    for col in range(m):
        k = next((i for i in range(r, len(M)) if M[i][col] != 0), None)
        if k is None: continue
        M[r], M[k] = M[k], M[r]
        inv = 1 / M[r][col]; M[r] = [v*inv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] != 0:
                fct = M[i][col]; M[i] = [a - fct*b for a, b in zip(M[i], M[r])]
        piv.append(col); r += 1
    for i in range(r, len(M)):
        if M[i][-1] != 0: raise ValueError('inconsistent system')
    sol = [Fr(0)]*m
    for i, col in enumerate(piv): sol[col] = M[i][-1]
    return sol, len(piv)

def reduced_forms(D):
    out = []; a = 1
    while 3*a*a <= -D:
        for b in range(-a+1, a+1):
            if (b*b - D) % (4*a): continue
            c = (b*b - D)//(4*a)
            if c < a: continue
            if b < 0 and (a == c): continue
            if math.gcd(math.gcd(a, abs(b)), c) != 1: continue
            out.append((a, b, c))
        a += 1
    return out

def eisenstein_with_bound(tau):
    q = mexp(2j*pi*tau); aq = fabs(q)
    N = 10
    while True:
        rho = (1 + mpf(1)/N)**5 * aq
        if rho < mpf(1)/2:
            tail = mpf(N)**5 * aq**N / ((1 - aq**N)*(1 - rho))
            if tail < mpf(10)**(-80): break
        N += 10
    s1 = s3 = s5 = mpc(0); qn = mpc(1)
    for n in range(1, N):
        qn *= q; t = qn/(1 - qn)
        s1 += n*t; s3 += n**3*t; s5 += n**5*t
    return 1 - 24*s1, 1 + 240*s3, 1 - 504*s5, N, 504*tail

def s2_and_j(tau):
    E2, E4, E6, N, tb = eisenstein_with_bound(tau)
    E2s = E2 - 3/(pi*tau.imag)
    return E2s*E4/E6, 1728*E4**3/(E4**3 - E6**2), N, tb

def embeddings(T):
    """All embeddings of the tower into C (sign choices per generator)."""
    out = []
    for signs in itertools.product([1, -1], repeat=len(T.d)):
        vals = []
        for k, d in enumerate(T.d):
            dv = mpc(T.evalc(d, vals)) if k else mpc(float(d) if not isinstance(d, tuple) else 0)
            if k == 0: dv = mpc(mpf(d.numerator)/d.denominator)
            vals.append(signs[k]*msqrt(dv))
        out.append((signs, vals))
    return out

def evalc(T, a, vals):
    if isinstance(a, tuple):
        n = T.level_of(a)
        return evalc(T, a[0], vals) + evalc(T, a[1], vals)*vals[n-1]
    return mpf(a.numerator)/a.denominator

def run(pari=None):
    tables = {}
    for name, rec in FL.results.items():
        if '_S' not in rec or name.endswith('conjugate_endomorphism') or 'seedfree' in name: continue
        T, S, j, D = rec['_T'], rec['_S'], rec['_j'], rec['D']
        forms = reduced_forms(D); h = len(forms)
        # minimal polynomial of j: relation among 1, j, ..., j^h
        pw = [T.const(1)]
        for _ in range(h): pw.append(T.mul(pw[-1], j))
        coords = [T.coords(x) for x in pw]
        nb = len(coords[0])
        rows = [[coords[k][r] for k in range(h)] for r in range(nb)]
        rhs = [-coords[h][r] for r in range(nb)]
        cf, rank = solve_rational(rows, rhs)
        assert rank == h, 'powers of j not independent: degree < h'
        HD = cf + [Fr(1)]             # monic, low-to-high
        assert all(c.denominator == 1 for c in HD)
        HD = [int(c) for c in HD]
        # R_D: S = sum r_k j^k
        rhsS = T.coords(S)
        RD, rankS = solve_rational(rows, rhsS)
        den = 1
        for c in RD: den = den*c.denominator//math.gcd(den, c.denominator)
        rec_out = {'D': D, 'class_number': h, 'reduced_forms': forms,
                   'H_D_low_to_high': HD, 'R_D_low_to_high': [str(c) for c in RD],
                   'R_D_common_denominator': den, 'R_D_denominator_factorization': {str(k): v for k, v in factor_int(den).items()},
                   'max_numerator_digits_R_D': max(len(str(abs(c.numerator))) for c in RD)}
        assert check_factor(den, factor_int(den))
        # discriminant of H_D via PARI if available
        if pari is not None:
            pc = pari(f'Vec(polclass({D}))')
            pc = [int(x) for x in pc][::-1]
            rec_out['polclass_matches'] = (pc == HD)
            disc = int(pari(f'poldisc(Pol({list(reversed(HD))}))'))
            fd = factor_int(disc) if abs(disc) < 10**40 else {int(k): int(v) for k, v in zip(*[list(x) for x in pari(f'factor({disc})')[0:2]])}
            rec_out['disc_H_D_factorization'] = {str(k): v for k, v in fd.items()}
        # analytic pairing check
        checks = []
        jvals = {f: s2_and_j(mpc(mpf(-f[1])/(2*f[0]), msqrt(-D)/(2*f[0]))) for f in forms}
        for signs, vals in embeddings(T):
            jv = evalc(T, j, vals); Sv = evalc(T, S, vals)
            best = min(forms, key=lambda f: fabs(jvals[f][1] - jv)/max(1, fabs(jv)))
            s2v, jt, N, tb = jvals[best]
            checks.append({'signs': signs, 'form': best,
                           'rel_err_j': mp.nstr(fabs(jt - jv)/max(1, fabs(jv)), 5),
                           'abs_err_S_vs_s2': mp.nstr(fabs(s2v - Sv), 5),
                           'q_terms': N, 'series_tail_bound': mp.nstr(tb, 3)})
        rec_out['embedding_checks'] = checks
        rec_out['max_abs_err_S_vs_s2'] = mp.nstr(max(fabs(evalc(T, S, v) - jvals[min(forms, key=lambda f: fabs(jvals[f][1]-evalc(T, j, v))/max(1, fabs(evalc(T, j, v))))][0]) for _, v in embeddings(T)), 5)
        forms_hit = sorted({tuple(c['form']) for c in checks})
        rec_out['every_form_paired'] = (len(forms_hit) == h)
        tables[name] = rec_out
    return tables

if __name__ == '__main__':
    try:
        import cypari2; pari = cypari2.Pari(); pari.allocatemem(10**9)
    except Exception:
        pari = None
    tabs = run(pari)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'embedding_checks'} for k, v in tabs.items()}, indent=1, default=str))
    if len(sys.argv) > 1:
        json.dump(tabs, open(sys.argv[1], 'w'), indent=1, default=str)
    ok = all(v['every_form_paired'] and v.get('polclass_matches', True) and float(v['max_abs_err_S_vs_s2']) < 1e-60 for v in tabs.values())
    print('TABLES_OK' if ok else 'TABLE_FAILURE')
    sys.exit(0 if ok else 1)
