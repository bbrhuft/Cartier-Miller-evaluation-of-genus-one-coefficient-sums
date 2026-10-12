"""Exact validation suite for the D=-7 seed, the D=-8 control and
Theorem 1 (Cartier/endomorphism eigen-equation).

Independent references used:
  * dense polynomial powers F^h and f^h via python-flint nmod_poly (not the
    retained recurrence), with a pure-Python convolution spot check;
  * naive point counts (Legendre table) and PARI ellap (practical comparator);
  * the retained O(p) recurrence linear_cartier_data and BranchEvaluator
    (read-only import from the retained package) as a second reference;
  * the retained recognizers (depth <= 3) for disjointness.
Every numerical statement printed by this script is observed output.
"""
import csv, json, math, os, random, sys, time, hashlib, platform
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'core'))
RETAINED = os.environ.get('RETAINED_RESEARCH', os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))  # release research/
sys.path.insert(0, os.path.join(RETAINED, 'branch_point_20261006'))
sys.path.insert(0, os.path.join(RETAINED, 'depth_three_recognition_20261007/core'))
sys.path.insert(0, os.path.join(RETAINED, 'depth_two_recognition_20261006/core'))
sys.path.insert(0, os.path.join(RETAINED, 'isogeny_closure_20261006/core'))

import d7_seed as D7
import d8_control as D8
from flint import nmod_poly
import branch_evaluator as RB                      # retained (read-only)
from depth_three_recognize import recognize_short_through_depth_three as retained_recognize
import cypari2
pari = cypari2.Pari()
pari.allocatemem(10**9)

OUT = os.path.join(ROOT, 'results', 'validation')
os.makedirs(OUT, exist_ok=True)
rng = random.Random(20261012)
summary = {}
failures = []

def fail(test, **kw):
    failures.append(dict(test=test, **kw))

def primes_between(a, b):
    return [int(x) for x in pari(f'primes([{a},{b}])')]

def dense_Hbeta(A, B, p):
    P = nmod_poly([B % p, A % p, 0, 1], p) ** ((p - 1) // 2)
    return int(P[p - 1]), int(P[p - 2])

def dense_cubic(f, p):
    P = nmod_poly(list(f), p) ** ((p - 1) // 2)
    return [int(P[i]) for i in range(p)]

def naive_trace(A, B, p, sq):
    s = 0
    for x in range(p):
        s += sq[(x*x*x + A*x + B) % p]
    return -s

def sq_table(p):
    t = [-1]*p; t[0] = 0
    for x in range(1, (p+1)//2):
        t[x*x % p] = 1
    return t

def jinv(A, B, p):
    den = (4*A**3 + 27*B*B) % p
    return 1728*4*A**3*pow(den, -1, p) % p

def nonsquare(p):
    z = 2
    while D7.legendre(z, p) != -1:
        z += 1
    return z

t_start = time.time()
# ---------------------------------------------------------------- T0 dense spot check
def naive_pow(c, h, p):
    r = [1]
    for _ in range(h):
        n = [0]*(len(r)+len(c)-1)
        for i, a in enumerate(r):
            if a:
                for j, b in enumerate(c):
                    n[i+j] = (n[i+j]+a*b) % p
        r = n
    return r
cnt = 0
for p in [11, 23, 29, 37, 43]:
    for r in [1, nonsquare(p)]:
        A, B = D7.family_member(p, r)
        N = naive_pow([B, A, 0, 1], (p-1)//2, p)
        if (N[p-1], N[p-2]) != dense_Hbeta(A, B, p):
            fail('T0_flint_vs_naive', p=p, r=r)
        cnt += 1
summary['T0_flint_vs_naive_convolution'] = cnt

# ---------------------------------------------------------------- T1 full sweep
rows = []
cnt = 0; retained_hits = 0
T1_MAX = int(os.environ.get('T1_MAX', 700))
for p in primes_between(11, T1_MAX):
    if not D7.is_admissible(p):
        continue
    sq = sq_table(p)
    for r in range(1, p):
        A, B = D7.family_member(p, r)
        rec = D7.recognize_d7(A, B, p)
        if rec['status'] != 'recognized' or rec['matches'][0]['parameters']['r'] != r:
            fail('T1_recognition', p=p, r=r); continue
        H, beta = dense_Hbeta(A, B, p)
        if H == 0 or beta != (-r*H) % p:
            fail('T1_slope', p=p, r=r, H=H, beta=beta)
        tn = naive_trace(A, B, p, sq)
        th, _ = D7.signed_trace_d7(p, r, method='hecke', rng=rng)
        t2, _ = D7.signed_trace_d7(p, r, method='two_adic', rng=rng)
        if not (tn == th == t2) or H != tn % p:
            fail('T1_trace', p=p, r=r, naive=tn, hecke=th, two_adic=t2, H=H)
        if retained_recognize(A, B, p)['status'] == 'recognized':
            retained_hits += 1; fail('T1_retained_recognizer_accepts_D7_member', p=p, r=r)
        cnt += 1
        if r in (1, 2, nonsquare(p)):
            rows.append([p, r, D7.legendre(r, p), A, B, H, beta, (-r*H) % p, tn, th, t2])
with open(os.path.join(OUT, 'T1_full_sweep_samples.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['p', 'r', 'chi_r', 'A', 'B', 'H_dense', 'beta_dense', 'minus_r_H', 'trace_naive', 'trace_hecke', 'trace_two_adic']); w.writerows(rows)
summary['T1_full_sweep_members'] = cnt
summary['T1_bound'] = T1_MAX
summary['T1_retained_recognizer_false_accepts'] = retained_hits

# ---------------------------------------------------------------- T2 sampled sweep to 5000
cnt = 0; sqn = 0
T2_MAX = int(os.environ.get('T2_MAX', 20000))
for p in primes_between(T1_MAX + 1, T2_MAX):
    if not D7.is_admissible(p):
        continue
    sq = sq_table(p)
    rs = {1, nonsquare(p)} | {rng.randrange(1, p) for _ in range(2)}
    for r in rs:
        A, B = D7.family_member(p, r)
        H, beta = dense_Hbeta(A, B, p)
        if H == 0 or beta != (-r*H) % p:
            fail('T2_slope', p=p, r=r)
        tn = naive_trace(A, B, p, sq)
        th, _ = D7.signed_trace_d7(p, r, method='hecke', rng=rng)
        t2, _ = D7.signed_trace_d7(p, r, method='two_adic', rng=rng)
        if not (tn == th == t2) or H != tn % p:
            fail('T2_trace', p=p, r=r)
        cnt += 1; sqn += (D7.legendre(r, p) == -1)
summary['T2_sampled_members'] = cnt
summary['T2_range'] = [T1_MAX + 1, T2_MAX]
summary['T2_of_which_nonsquare_r'] = sqn

# ---------------------------------------------------------------- T3 exhaustive model scan
scan = []
T3_MAX = int(os.environ.get('T3_MAX', 151))
for p in primes_between(11, T3_MAX):
    acc = 0; jmatch = 0; both = 0; retained_acc = 0; total = 0
    adm = D7.is_admissible(p)
    for A in range(p):
        for B in range(p):
            if (4*A**3 + 27*B*B) % p == 0:
                continue
            total += 1
            rec = D7.recognize_d7(A, B, p)
            is_j = (jinv(A, B, p) == (-3375) % p) and A and B
            ok = rec['status'] == 'recognized'
            if adm and ok != bool(is_j):
                fail('T3_recognition_vs_j', p=p, A=A, B=B)
            if not adm and rec['status'] != 'not_eligible_prime':
                fail('T3_ineligible_status', p=p, A=A, B=B)
            ret = retained_recognize(A, B, p)['status'] == 'recognized'
            retained_acc += ret
            acc += ok; jmatch += bool(is_j); both += (ok and ret)
    if adm and acc != p - 1:
        fail('T3_count', p=p, accepted=acc)
    if both:
        fail('T3_overlap_with_retained', p=p, both=both)
    scan.append([p, int(adm), total, acc, jmatch, retained_acc, both])
with open(os.path.join(OUT, 'T3_exhaustive_scan.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['p', 'admissible', 'nonsingular_models', 'd7_accepted', 'j_eq_-3375_AB_nonzero', 'retained_depth_le3_accepted', 'accepted_by_both']); w.writerows(scan)
summary['T3_exhaustive_primes'] = len(scan)
summary['T3_bound'] = T3_MAX
summary['T3_models_scanned'] = sum(r[2] for r in scan)
summary['T3_d7_accepted'] = sum(r[3] for r in scan)
summary['T3_retained_accepted'] = sum(r[5] for r in scan)
summary['T3_overlaps'] = sum(r[6] for r in scan)

# ---------------------------------------------------------------- T4 inadmissible primes
ss = 0
for p in primes_between(11, 400):
    if D7.is_admissible(p):
        continue
    for r in [1, nonsquare(p)]:
        A, B = (-35*r*r) % p, (-98*r**3) % p
        if (4*A**3 + 27*B*B) % p == 0:
            fail('T4_singular', p=p); continue
        if D7.recognize_d7(A, B, p)['status'] != 'not_eligible_prime':
            fail('T4_status', p=p)
        H, beta = dense_Hbeta(A, B, p)
        if H != 0 or beta == 0:
            fail('T4_supersingular_expected', p=p, r=r, H=H, beta=beta)
        ss += 1
try:
    D7.recognize_d7(0, 0, 7); fail('T4_p7_accepted')
except ValueError:
    pass
summary['T4_inadmissible_supersingular_checks'] = ss
summary['T4_p7'] = 'model (-35r^2,-98r^3) = (0,0) mod 7 is singular; rejected'

# ---------------------------------------------------------------- T5 Theorem 1 universal check
def rational_roots(A, B, p):
    return [x for x in range(p) if (x**3 + A*x + B) % p == 0]
t5 = {'checks_lambda_ne_mu': 0, 'checks_lambda_eq_mu': 0, 'models': 0, 'supersingular_with_loop': 0}
T5_MAX = int(os.environ.get('T5_MAX', 67))
for p in primes_between(11, T5_MAX):
    for A in range(p):
        for B in range(p):
            if (4*A**3 + 27*B*B) % p == 0:
                continue
            H, beta = dense_Hbeta(A, B, p)
            t5['models'] += 1
            # walks of length 1..3; matrix entries (a, b, d) with a=1 for Velu steps
            stack = [(A, B, 0, 1, 0, 1)]  # model, depth, a, b, d
            while stack:
                a_, b_, dep, ma, mb, md = stack.pop()
                if dep >= 1:
                    for u in range(1, p):
                        if a_ == pow(u, 4, p)*A % p and b_ == pow(u, 6, p)*B % p:
                            ui = pow(u, -1, p)
                            lam = ma*u % p; nu = mb*ui % p; mu = md*ui % p
                            if (beta*(lam - mu) - nu*H) % p:
                                fail('T5_theorem1', p=p, A=A, B=B, lam=lam, mu=mu, nu=nu, H=H, beta=beta)
                            if lam != mu:
                                t5['checks_lambda_ne_mu'] += 1
                                if H == 0: t5['supersingular_with_loop'] += 1
                            else:
                                t5['checks_lambda_eq_mu'] += 1
                if dep < 3:
                    for q in rational_roots(a_, b_, p):
                        a2, b2 = (-4*a_ - 15*q*q) % p, (-8*a_*q - 22*q**3) % p
                        # [[ma,mb],[0,md]] * [[1,-q],[0,2]]
                        stack.append((a2, b2, dep+1, ma, (-ma*q + 2*mb) % p, 2*md % p))
t5['bound'] = T5_MAX
summary['T5_theorem1_universal'] = t5

# ---------------------------------------------------------------- T6 original cubics
cub = []; cnt6 = 0
for p in primes_between(11, 1200):
    if not D7.is_admissible(p):
        continue
    for trial in range(3 if p < 300 else 1):
        r = rng.randrange(1, p) if trial else nonsquare(p)
        A, B = D7.family_member(p, r)
        while True:
            xP = rng.randrange(p)
            rhs = (xP**3 + A*xP + B) % p
            if rhs and D7.legendre(rhs, p) == 1:
                yP = int(pari(f'lift(sqrt(Mod({rhs},{p})))')); break
        f = D7.cubic_from_point(p, r, xP, yP)
        dense = dense_cubic(f, p)
        Hd, Kd = dense[p-1], dense[p-2]
        Hr, Kr = RB.linear_cartier_data(f, p)
        for method in ('hecke', 'two_adic'):
            ev = D7.prepare_cm_d7(p, f, method=method, rng=rng)
            if (ev.H, ev.K) != (Hd, Kd) or (Hr, Kr) != (Hd, Kd):
                fail('T6_HK', p=p, f=f, method=method)
        # branch roots
        e = D7.sqrt_mod(-7, p, rng)
        roots_x = [7*r % p, r*(-7+e)*pow(2, -1, p) % p, r*(-7-e)*pow(2, -1, p) % p]
        _, c, b, a = f
        for ex in roots_x:
            mu = (ex - b*pow(3, -1, p)) * pow(a, -1, p) % p
            if D7.eval_poly(f, mu, p) != 0 or mu == 0:
                fail('T6_root', p=p); continue
            T_direct = sum(dense[i]*pow(mu, i, p) for i in range(p)) % p
            T_new = ev.query(mu)['T']
            T_ret = RB.BranchEvaluator(p, f, Hr, Kr, 'retained_recurrence').query(mu)['T']
            if not (T_direct == T_new == T_ret):
                fail('T6_branch', p=p, f=f, mu=mu, direct=T_direct, new=T_new, retained=T_ret)
            cnt6 += 1
            if len(cub) < 400:
                cub.append([p, r, D7.legendre(r, p), *f, mu, ev.H, ev.K, T_direct, T_new, T_ret])
with open(os.path.join(OUT, 'T6_original_cubic_branch_checks.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['p', 'r', 'chi_r', 'f0', 'c', 'b', 'a', 'mu', 'H', 'K', 'T_direct_dense', 'T_new_formula', 'T_retained_recurrence']); w.writerows(cub)
summary['T6_branch_queries_checked'] = cnt6

# ---------------------------------------------------------------- T7 wrong traces
rej = 0; acc = 0
for p in primes_between(11, 3000)[::7]:
    if not D7.is_admissible(p):
        continue
    r = rng.randrange(1, p)
    A, B = D7.family_member(p, r)
    while True:
        xP = rng.randrange(p); rhs = (xP**3 + A*xP + B) % p
        if rhs and D7.legendre(rhs, p) == 1:
            yP = int(pari(f'lift(sqrt(Mod({rhs},{p})))')); break
    f = D7.cubic_from_point(p, r, xP, yP)
    t, _ = D7.signed_trace_d7(p, r, rng=rng)
    D7.prepare_cm_d7(p, f, trace=t); acc += 1
    for bad in {-t, t + 2, t - 2, t + 14, t + 1, 0, math.isqrt(4*p) + 1}:
        if bad == t:
            continue
        try:
            D7.prepare_cm_d7(p, f, trace=bad); fail('T7_wrong_trace_accepted', p=p, t=t, bad=bad)
        except ValueError:
            rej += 1
summary['T7_correct_traces_accepted'] = acc
summary['T7_wrong_traces_rejected'] = rej

# ---------------------------------------------------------------- T8 altered certificates
rej8 = 0; ok8 = 0
for p in [11, 29, 43, 53, 107, 1009, 7351]:
    if not D7.is_admissible(p):
        continue
    for r in [1, nonsquare(p), rng.randrange(1, p)]:
        A, B = D7.family_member(p, r)
        cert = D7.recognize_d7(A, B, p)['matches'][0]
        D7.verify_supplied_certificate(p, A, B, cert); ok8 += 1
        tampered = []
        c1 = json.loads(json.dumps(cert)); c1['parameters']['r'] = (r + 1) % p; tampered.append(c1)
        c2 = json.loads(json.dumps(cert)); c2['parameters']['r'] = (-r) % p; tampered.append(c2)
        c3 = json.loads(json.dumps(cert)); c3['beta_multiplier'] = (c3['beta_multiplier'] + 1) % p; tampered.append(c3)
        c4 = json.loads(json.dumps(cert)); c4['extra'] = 1; tampered.append(c4)
        c5 = json.loads(json.dumps(cert)); c5['parameters']['s'] = 3; tampered.append(c5)
        c6 = json.loads(json.dumps(cert)); c6['family'] = 'depth1_0'; tampered.append(c6)
        c7 = json.loads(json.dumps(cert)); c7['cm_value_s2'] = '5/11'; tampered.append(c7)
        for c in tampered:
            try:
                D7.verify_supplied_certificate(p, A, B, c); fail('T8_tampered_accepted', p=p, cert=c)
            except (ValueError, KeyError):
                rej8 += 1
summary['T8_valid_certificates_verified'] = ok8
summary['T8_tampered_certificates_rejected'] = rej8

# ---------------------------------------------------------------- T9 large primes (trace sign)
large = []
for bits in [20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 62]:
    found = 0; n = rng.randrange(2**(bits-1), 2**bits)
    while found < 3:
        n = int(pari(f'nextprime({n}+1)'))
        if not D7.is_admissible(n):
            continue
        r = rng.randrange(1, n)
        A, B = D7.family_member(n, r)
        th, sh = D7.signed_trace_d7(n, r, method='hecke', rng=rng)
        t2, s2 = D7.signed_trace_d7(n, r, method='two_adic', rng=rng)
        ap = int(pari(f'ellap(ellinit([{A},{B}]),{n})'))
        if not (th == t2 == ap):
            fail('T9_large_trace', p=n, r=r, hecke=th, two_adic=t2, pari=ap)
        large.append([n, bits, r, A, B, D7.legendre(r, n), th, t2, ap])
        found += 1
with open(os.path.join(OUT, 'T9_large_prime_traces.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['p', 'bits', 'r', 'A', 'B', 'chi_r', 'trace_hecke', 'trace_two_adic', 'pari_ellap']); w.writerows(large)
summary['T9_large_prime_trace_checks'] = len(large)

# ---------------------------------------------------------------- T10 endomorphism certificates
cnt10 = 0
for p in primes_between(11, 2000):
    if not D7.is_admissible(p):
        continue
    e = D7.sqrt_mod(-7, p, rng)
    for r in [1, nonsquare(p), rng.randrange(1, p)]:
        A, B = D7.family_member(p, r)
        for ee in (e, p - e):     # both endomorphisms (1 +- sqrt(-7))/2
            c = D7.endomorphism_certificate(A, B, p, ee)
            cnt10 += 1
summary['T10_endomorphism_certificates'] = cnt10

# ---------------------------------------------------------------- T11 D=-8 control
cnt11 = 0
for p in primes_between(11, 400):
    if not D8.is_admissible(p):
        continue
    v = int(pari(f'lift(sqrt(Mod(-2,{p})))'))
    for r in range(1, p):
        A, B = (-30*r*r) % p, (56*r**3) % p
        rec = D8.recognize_d8(A, B, p)
        if rec['status'] != 'recognized' or rec['parameters']['r'] != r:
            fail('T11_recognition', p=p, r=r); continue
        H, beta = dense_Hbeta(A, B, p)
        if H == 0 or beta != r*H % p:
            fail('T11_slope', p=p, r=r)
        if r <= 3:
            D8.endomorphism_certificate(A, B, p, v)
        cnt11 += 1
summary['T11_D8_control_members'] = cnt11

# ---------------------------------------------------------------- T14 primality helper
cnt14 = 0
for _ in range(3000):
    n = rng.randrange(2, 2**64)
    if D7.is_prime64(n) != bool(pari(f'isprime({n})')):
        fail('T14_prime', n=n)
    cnt14 += 1
for n in [2**61 - 1, 2**64 - 59, 3215031751, 341550071728321, 3825123056546413051]:
    if D7.is_prime64(n) != bool(pari(f'isprime({n})')):
        fail('T14_prime_edge', n=n)
summary['T14_primality_cross_checks'] = cnt14 + 5

summary['failures'] = len(failures)
summary['elapsed_seconds'] = round(time.time() - t_start, 1)
env = {'python': sys.version.split()[0], 'platform': platform.platform(),
       'pari': str(pari('version()')), 'flint': __import__('flint').__version__}
src = {}
for path in [os.path.join(ROOT, 'core', 'd7_seed.py'), os.path.join(ROOT, 'core', 'd8_control.py'), os.path.abspath(__file__)]:
    src[os.path.relpath(path, ROOT)] = hashlib.sha256(open(path, 'rb').read()).hexdigest()
json.dump({'summary': summary, 'failures': failures[:200], 'environment': env, 'source_sha256': src},
          open(os.path.join(OUT, 'validation_summary.json'), 'w'), indent=1)
print(json.dumps(summary, indent=1))
print('FAILURES:', len(failures))
for f in failures[:20]:
    print(f)
sys.exit(1 if failures else 0)
