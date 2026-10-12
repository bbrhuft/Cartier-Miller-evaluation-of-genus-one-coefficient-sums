"""Validation suite for the B=0-seed depth-three (discriminant -256) recognizer.

Correctness only; elapsed time is not a benchmark. Independent references:
brute-force nondual chains from every (A,0) seed with brute-force root scans,
the set of all models whose j is a root of H_{-256} mod p, exact integer
multinomial (H, beta), Legendre-symbol traces, dense polynomial powers, the
retained O(p) recurrence for K, and PARI ellap/polclass when cypari2 exists.
Outputs validation_b0.json and validation_b0_*.csv next to this script.
"""
from __future__ import annotations
import csv
import hashlib
import json
import platform
import random
import sys
import time
from math import factorial, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from depth_three_b0_recognize import (recognize_depth_three_b0, verify_supplied_certificate_b0,  # noqa: E402
                                      prepare_from_trace_b0, prepare_cm_b0, family_member_b0,
                                      gaussian_prime_from_cornacchia, seed_trace_quartic,
                                      seed_trace_quartic_general, prime_is_eligible, ev, MULTIPLIER)
from depth_three_recognize import (recognize_depth_three, recognize_short_through_depth_three,  # noqa: E402
                                   RecognizedPreparation, CMPreparation)
from branch_evaluator import linear_cartier_data, is_prime64  # noqa: E402
from isogeny_closure import short_model  # noqa: E402

SEED = 20261012
try:
    import cypari2
    PARI = cypari2.Pari()
    PARI.allocatemem(1 << 30)
except Exception:  # pragma: no cover
    PARI = None

H256 = [-1064410681181869521037208505239142408, 26925623396663008311375890966784,
        -1826592673506207200904172752, -6761166974781862161312, 1]


def invariant(A, B, p):
    return 1728*4*A**3*pow((4*A**3+27*B*B) % p, -1, p) % p


def coefficients(A, B, p):
    h = (p-1)//2
    facts = [factorial(i) for i in range(h+1)]
    out = []
    for k in (p-1, p-2):
        total = 0
        for i in range(h+1):
            j = k-3*i; ell = h-i-j
            if j >= 0 and ell >= 0:
                total += facts[h]//(facts[i]*facts[j]*facts[ell])*pow(A, j, p)*pow(B, ell, p)
        out.append(total % p)
    return tuple(out)


def legendre_trace(A, B, p):
    h = (p-1)//2
    return -sum(0 if (x**3+A*x+B) % p == 0 else (1 if pow((x**3+A*x+B) % p, h, p) == 1 else -1) for x in range(p))


def pari_trace(A, B, p):
    if PARI is None:
        return None
    return int(PARI.ellap(PARI.ellinit([0, 0, 0, A, B]), p))


def brute_roots(A, B, p):
    return [q for q in range(p) if (q**3+A*q+B) % p == 0]


def ref_quotient(A, B, q, p):
    return ((-4*A-15*q*q) % p, (-8*A*q-22*q**3) % p)


def dense_power(coeff, p):
    v = [1]
    for _ in range((p-1)//2):
        n = [0]*(len(v)+len(coeff)-1)
        for i, a in enumerate(v):
            if a:
                for j, b in enumerate(coeff):
                    n[i+j] = (n[i+j]+a*b) % p
        v = n
    return v


def sqrt_mod(n, p, rng):
    n %= p
    if n == 0:
        return 0
    if pow(n, (p-1)//2, p) != 1:
        return None
    q, s = p-1, 0
    while q % 2 == 0:
        q //= 2; s += 1
    z = 2
    while pow(z, (p-1)//2, p) != p-1:
        z = rng.randrange(2, p)
    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q+1)//2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1:
            tt = tt*tt % p; i += 1
        b = pow(c, 1 << (m-i-1), p)
        m, c, t, r = i, b*b % p, t*b*b % p, r*b % p
    return r


def nondual_depth3_from_B0(p):
    """Endpoints of nondual length-3 chains from every seed (A,0) whose first
    kernel root is nonzero (a zero first root only moves to another seed)."""
    level = {}
    for A in range(1, p):
        for q in brute_roots(A, 0, p):
            if q:
                level.setdefault(ref_quotient(A, 0, q, p), [q])
    for _ in range(2):
        nxt = {}
        for (A, B), path in level.items():
            for q in brute_roots(A, B, p):
                if q == -2*path[-1] % p:
                    continue
                nxt.setdefault(ref_quotient(A, B, q, p), path+[q])
        level = nxt
    return level


def roots_mod(poly, p):
    return [x for x in range(p) if sum(c*pow(x, i, p) for i, c in enumerate(poly)) % p == 0]


def lower_depth_j_values(p):
    """j-values of the complete unpruned closure of both seed types through depth two."""
    seeds = []
    if p % 3 == 1:
        seeds += [(0, B) for B in range(1, p)]
    if p % 4 == 1:
        seeds += [(A, 0) for A in range(1, p)]
    seen = set(seeds); frontier = list(seeds)
    for _ in range(2):
        new = []
        for A, B in frontier:
            for q in brute_roots(A, B, p):
                t = ref_quotient(A, B, q, p)
                if t not in seen:
                    seen.add(t); new.append(t)
        frontier = new
    return {invariant(A, B, p) for A, B in seen}


def write_csv(path, rows):
    if not rows:
        return
    keys = []
    for row in rows:
        for k in row:
            if k not in keys:
                keys.append(k)
    with path.open('w', newline='') as handle:
        w = csv.DictWriter(handle, fieldnames=keys)
        w.writeheader(); w.writerows(rows)


def expect_reject(fn, *args, **kw):
    try:
        fn(*args, **kw)
    except (ValueError, AssertionError, KeyError) as err:
        return str(err) or type(err).__name__
    raise AssertionError('accepted invalid input %r' % (args,))


def main():
    rng = random.Random(SEED)
    t_start = time.time()
    summary = {'status': 'running', 'seed': SEED}
    eligible_small = [p for p in range(7, 700) if is_prime64(p) and prime_is_eligible(p)]
    summary['eligible_primes_below_700'] = eligible_small
    # independent eligibility characterisation p = x^2 + 64 y^2
    for p in range(7, 5000):
        if is_prime64(p):
            form = any(isqrt(p-64*y*y)**2 == p-64*y*y for y in range(1, isqrt(p//64)+1))
            assert form == prime_is_eligible(p), p
    # ---- 1. retained audit certificates ----
    audit = []
    with (HERE.parents[2]/'fixtures/depth_three_four_certificates_20261006.csv').open() as handle:
        for row in csv.DictReader(handle):
            p = int(row['p']); A, B = json.loads(row['target']); seed = json.loads(row['seed'])
            res = recognize_depth_three_b0(A, B, p)
            is_b0_depth3 = int(row['depth']) == 3 and seed[1] == 0
            if is_b0_depth3:
                assert res['status'] == 'recognized', row
                m = res['matches'][0]
                assert m['forward_roots'] == json.loads(row['forward_roots'])
                assert m['reverse_path']['roots'] == json.loads(row['inverse_roots'])
                assert m['beta_multiplier'] == int(row['inverse_beta_multiplier'])
                assert m['forward_models'] == json.loads(row['forward_models'])
                assert recognize_depth_three(A, B, p)['status'] != 'recognized'
            else:
                assert res['status'] in ('not_in_depth_three_b0_family', 'not_eligible_prime'), (row, res['status'])
            audit.append({'p': p, 'depth': row['depth'], 'seed': row['seed'], 'target': row['target'],
                          'b0_status': res['status'], 'seed_chain': 'B=0' if seed[1] == 0 else 'A=0'})
    write_csv(HERE/'validation_b0_audit_certificates.csv', audit)
    summary['audit_certificates'] = {'rows': len(audit), 'b0_recognized': sum(r['b0_status'] == 'recognized' for r in audit),
                                     'a0_depth3_rows_rejected': sum(r['seed_chain'] == 'A=0' and r['depth'] == '3' for r in audit),
                                     'depth4_rows_rejected': sum(r['depth'] == '4' for r in audit)}
    # ---- 2. exhaustive classification at eligible primes ----
    exhaustive = []; members_by_p = {}
    for p in [73, 89, 113, 233, 257, 281, 337, 353]:
        assert prime_is_eligible(p)
        chains = nondual_depth3_from_B0(p)
        Hroots = roots_mod(H256, p)
        if PARI is not None:
            assert sorted(int(x) for x in PARI.polrootsmod(PARI('polclass(-256)'), p)) == sorted(Hroots)
        assert len(Hroots) == 4
        by_j = {(A, B) for A in range(1, p) for B in range(1, p)
                if (4*A**3+27*B*B) % p and invariant(A, B, p) in Hroots}
        assert set(chains) == by_j and len(by_j) == 4*(p-1)
        low_j = lower_depth_j_values(p)
        assert not (set(Hroots) & low_j)
        accepted = {}
        pos = neg = 0
        for A in range(p):
            for B in range(p):
                if (4*A**3+27*B*B) % p == 0:
                    continue
                res = recognize_depth_three_b0(A, B, p)
                if (A, B) in by_j:
                    assert res['status'] == 'recognized', (p, A, B, res)
                    m = res['matches'][0]
                    prm = m['parameters']
                    assert m['forward_roots'] == chains[(A, B)]
                    accepted[(A, B)] = (prm['s'], prm['r'], m['beta_multiplier'])
                    pos += 1
                else:
                    assert res['status'] == 'not_in_depth_three_b0_family', (p, A, B, res)
                    neg += 1
        # parameter injectivity: all (s, r) give distinct models
        assert len({v[:2] for v in accepted.values()}) == len(accepted) == 4*(p-1)
        members_by_p[p] = accepted
        co = 0
        if p in (73, 337):   # both depth-three families eligible: combined recognizer, exhaustive
            for A in range(p):
                for B in range(p):
                    if (4*A**3+27*B*B) % p:
                        comb = recognize_short_through_depth_three(A, B, p)
                        co += comb['status'] == 'recognized'
        exhaustive.append({'p': p, 'p_mod_24': p % 24, 'nonsingular_models': pos+neg, 'recognized': pos, 'rejected': neg,
                           'brute_force_chain_endpoints': len(chains), 'models_with_j_root_of_H256': len(by_j),
                           'H256_roots_mod_p': json.dumps(sorted(Hroots)), 'family_j_in_lower_depth': 0,
                           'combined_depth_le3_recognized': co if p in (73, 337) else ''})
    write_csv(HERE/'validation_b0_exhaustive.csv', exhaustive)
    summary['exhaustive'] = exhaustive
    # ---- 3. exact coefficients and Theorem 5 traces of members ----
    member_rows = []
    for p, acc in members_by_p.items():
        a, b, _ = gaussian_prime_from_cornacchia(p, rng)
        assert b % 8 == 0
        items = sorted(acc.items()) if p in (73, 89, 113) else rng.sample(sorted(acc.items()), 32)
        for (A, B), (s, r, mult) in items:
            H, beta = coefficients(A, B, p)
            tau = legendre_trace(A, B, p)
            tq, _ = seed_trace_quartic(p, r, (a, b))
            tp = pari_trace(A, B, p)
            assert H == tau % p and H and beta == mult*H % p and tq == tau and (tp is None or tp == tau)
            assert mult == ev(MULTIPLIER, s, p)*r % p
            member_rows.append({'p': p, 'A': A, 'B': B, 's': s, 'r': r, 'H': H, 'beta': beta, 'beta_multiplier': mult,
                                'trace_legendre': tau, 'trace_theorem5': tq, 'trace_pari': tp})
    write_csv(HERE/'validation_b0_members.csv', member_rows)
    summary['member_coefficient_checks'] = len(member_rows)
    # ---- 4. Theorem 5 for every y^2 = x^3 - D x, p = 1 mod 4 below 400 ----
    t5 = []
    for p in [q for q in range(5, 400) if q % 4 == 1 and is_prime64(q)]:
        pi = next((x, y) for x in range(-isqrt(p)-1, isqrt(p)+2) for y in range(-isqrt(p)-1, isqrt(p)+2)
                  if x*x+y*y == p and x % 2 and y % 2 == 0 and (x+y) % 4 == 1)
        agree = sum(seed_trace_quartic_general(p, D, pi) == legendre_trace(-D % p, 0, p) for D in range(1, p))
        assert agree == p-1, (p, agree)
        sq = sum(seed_trace_quartic(p, r, pi)[0] == legendre_trace(-r*r % p, 0, p) for r in range(1, p))
        assert sq == p-1
        t5.append({'p': p, 'primary_pi': json.dumps(list(pi)), 'D_checked': p-1, 'agree': agree, 'r_checked_D_eq_r2': sq})
    assert seed_trace_quartic_general(13, 1, (3, 2)) == 6     # Ireland-Rosen example: y^2 = x^3 - x, N_13 = 8
    write_csv(HERE/'validation_b0_theorem5.csv', t5)
    summary['theorem5_checks'] = {'primes': len(t5), 'curves': sum(r['D_checked'] for r in t5),
                                  'ireland_rosen_example_p13': 'y^2=x^3-x, trace 6, N=8, reproduced'}
    # ---- 5. trace proposition at all eligible primes below 5000 ----
    trace_rows = []
    for p in [q for q in range(7, 5000) if is_prime64(q) and prime_is_eligible(q)]:
        a, b, info = gaussian_prime_from_cornacchia(p, rng)
        assert b % 8 == 0
        sols = [t for t in range(1, 2*isqrt(p)+1) if (4*p-t*t) % 256 == 0 and 4*p-t*t > 0 and isqrt((4*p-t*t)//256)**2 == (4*p-t*t)//256]
        assert sols == [2*abs(a)], (p, sols, a)
        s = next(x for x in range(p) if (pow(x, 4, p)-2) % p == 0)
        r = rng.randrange(1, p)
        A, B = family_member_b0(p, s, r)
        tau = legendre_trace(A, B, p)
        tq, _ = seed_trace_quartic(p, r, (a, b))
        assert tq == tau == legendre_trace(-r*r % p, 0, p)
        trace_rows.append({'p': p, 'a': a, 'b': b, 'trace_family_member': tau, 'trace_theorem5': tq,
                           'nonresidue_trials': info['nonresidue_trials']})
    write_csv(HERE/'validation_b0_trace.csv', trace_rows)
    summary['trace_proposition_primes'] = len(trace_rows)
    # ---- 6. twists ----
    twist_rows = []
    for p, acc in members_by_p.items():
        sample = rng.sample(sorted(acc.items()), 4)
        ds = range(1, p) if p == 73 else [2, 3, p-1, rng.randrange(2, p)]
        for (A, B), (s, r, mult) in sample:
            H, beta = coefficients(A, B, p) if p <= 113 else (None, None)
            for d in ds:
                Ad, Bd = d*d*A % p, d**3*B % p
                res = recognize_depth_three_b0(Ad, Bd, p)
                assert res['status'] == 'recognized'
                prm = res['matches'][0]['parameters']
                assert (prm['s'], prm['r']) == (s, d*r % p)
                assert res['matches'][0]['beta_multiplier'] == d*mult % p
                row = {'p': p, 'A': A, 'B': B, 'd': d, 'r_d': prm['r']}
                if H is not None and p == 73:
                    chi = 1 if pow(d, (p-1)//2, p) == 1 else -1
                    Hd, bd = coefficients(Ad, Bd, p)
                    assert Hd == chi*H % p and bd == d*chi*beta % p
                    row.update({'chi_d': chi, 'H_d': Hd, 'beta_d': bd})
                twist_rows.append(row)
    write_csv(HERE/'validation_b0_twists.csv', twist_rows)
    summary['twist_checks'] = len(twist_rows)
    # ---- 7. tampered certificates ----
    base = recognize_depth_three_b0(16, 27, 73)['matches'][0]
    assert verify_supplied_certificate_b0(73, 16, 27, base)['beta_multiplier'] == 44
    tampered = []
    i73 = 27   # sqrt(-1) mod 73
    for label, change in [('s_negated', {'s': -18 % 73}), ('s_times_i', {'s': 18*i73 % 73}), ('r_scaled', {'r': 2*27 % 73}),
                          ('r_negated', {'r': -27 % 73}), ('s_not_fourth_root', {'s': 5}), ('r_zero', {'r': 0}),
                          ('e_inconsistent', {'e': 41})]:
        bad = json.loads(json.dumps(base)); bad['parameters'].update(change)
        tampered.append({'case': label, 'error': expect_reject(verify_supplied_certificate_b0, 73, 16, 27, bad)})
    for label, path, value in [('multiplier', ('beta_multiplier',), 45), ('forward_roots', ('forward_roots',), [27, 3, 62]),
                               ('reverse_roots', ('reverse_path', 'roots'), [24, 49, 13]),
                               ('reverse_endpoint', ('reverse_path', 'endpoint'), [8, 1]),
                               ('forward_seed', ('forward_seed',), [2, 0]), ('depth', ('depth',), 2), ('unknown_field', ('bogus',), 1),
                               ('family_label', ('family',), 'depth3_0_disc_-192')]:
        bad = json.loads(json.dumps(base)); node = bad
        for k in path[:-1]:
            node = node[k]
        node[path[-1]] = value
        tampered.append({'case': label, 'error': expect_reject(verify_supplied_certificate_b0, 73, 16, 27, bad)})
    tampered.append({'case': 'certificate_on_twist', 'error': expect_reject(verify_supplied_certificate_b0, 73, 64, 70, base)})
    tampered.append({'case': 'certificate_on_other_model', 'error': expect_reject(verify_supplied_certificate_b0, 73, 2, 59, base)})
    write_csv(HERE/'validation_b0_tampered.csv', tampered)
    summary['tampered_certificates_rejected'] = len(tampered)
    # ---- 8. ineligible primes ----
    inel = []
    for p in [11, 13, 17, 23, 29, 37, 41, 71, 97, 137, 167, 191, 193, 241, 313, 401, 409]:
        assert not prime_is_eligible(p)
        statuses = set()
        for A in range(p):
            for B in range(p):
                if (4*A**3+27*B*B) % p:
                    statuses.add(recognize_depth_three_b0(A, B, p)['status'])
        assert statuses == {'not_eligible_prime'}, (p, statuses)
        fourth_roots = [x for x in range(p) if (pow(x, 4, p)-2) % p == 0]
        deg = [{'s': s, 'alpha': ev((-731, -600, -540, -360), s, p), 'gamma': ev((-14798, -11816, -10164, -8456), s, p)} for s in fourth_roots]
        has_root = bool(roots_mod(H256, p))
        inel.append({'p': p, 'p_mod_8': p % 8, 'fourth_roots_of_2': len(fourth_roots),
                     'alpha_zero': sum(d['alpha'] == 0 for d in deg), 'gamma_zero': sum(d['gamma'] == 0 for d in deg),
                     'H256_has_root_mod_p': has_root, 'recognizer_status': 'not_eligible_prime'})
    write_csv(HERE/'validation_b0_ineligible.csv', inel)
    summary['ineligible_primes'] = inel
    # ---- 9. original normalized cubics: K and branch queries ----
    cubic_rows = []
    for p in [73, 89, 113, 233, 257]:
        acc = members_by_p[p]
        for (A, B) in rng.sample(sorted(acc), 8 if p > 73 else 16):
            while True:
                x0 = rng.randrange(p); y0 = sqrt_mod((x0**3+A*x0+B) % p, p, rng)
                if y0:
                    break
            f = [1, (3*x0*x0+A)*pow(y0, -1, p) % p, 3*x0 % p, y0]
            assert short_model(f, p) == (A, B)
            H_ref, K_ref = linear_cartier_data(tuple(f), p)
            tau = legendre_trace(A, B, p)
            prep = prepare_from_trace_b0(p, f, tau, verify_trace=True, rng=rng)
            cm = prepare_cm_b0(p, f, rng=rng)
            lv = prepare_cm_b0(p, f, rng=rng, sign_method='las_vegas')
            assert isinstance(prep, RecognizedPreparation) and isinstance(cm, CMPreparation)
            assert (prep.evaluator.H, prep.evaluator.K) == (H_ref, K_ref) == (cm.evaluator.H, cm.evaluator.K)
            assert cm.exact_trace == tau == lv.exact_trace
            dense = dense_power(f, p)
            assert (dense[p-1], dense[p-2]) == (H_ref, K_ref)
            for mu in [(q-x0)*pow(y0, -1, p) % p for q in brute_roots(A, B, p)]:
                T_ref = sum(dense[i]*pow(mu, i, p) for i in range(p)) % p
                assert cm.evaluator.query(mu)['T'] == T_ref
                cubic_rows.append({'p': p, 'f': json.dumps(f), 'trace': tau, 'H': H_ref, 'K_recurrence': K_ref,
                                   'K_cm': cm.evaluator.K, 'mu': mu, 'T_dense': T_ref})
    write_csv(HERE/'validation_b0_cubics.csv', cubic_rows)
    summary['original_cubic_branch_queries'] = len(cubic_rows)
    summary['original_cubic_curves'] = len({(r['p'], r['f']) for r in cubic_rows})
    # ---- 10. wrong supplied traces ----
    wrong = []
    for t, label in [(7, 'odd'), (0, 'zero'), (10, 'not_256_form'), (6, 'wrong_sign')]:
        wrong.append({'trace': t, 'case': label,
                      'error': expect_reject(prepare_from_trace_b0, 73, [1, 60, 0, 10], t, verify_trace=True, rng=rng)})
    assert isinstance(prepare_from_trace_b0(73, [1, 60, 0, 10], -6, verify_trace=True, rng=rng), RecognizedPreparation)
    write_csv(HERE/'validation_b0_wrong_traces.csv', wrong)
    summary['wrong_supplied_traces_rejected'] = len(wrong)
    # ---- 11. larger primes ----
    large = []
    for size, full in [(10**5, True), (10**6, True), (2**31, False), (2**40, False), (2**62, False)]:
        p = rng.randrange(size, size+size//4) | 1
        while not (is_prime64(p) and prime_is_eligible(p)):
            p += 2
        e = sqrt_mod(2, p, rng); s = sqrt_mod(e, p, rng)
        if s is None:
            e = p-e; s = sqrt_mod(e, p, rng)
        for _ in range(3):
            s_c = rng.choice([s, p-s]); r = rng.randrange(1, p)
            A, B = family_member_b0(p, s_c, r)
            res = recognize_depth_three_b0(A, B, p)
            assert res['status'] == 'recognized'
            prm = res['matches'][0]['parameters']
            assert (prm['s'], prm['r']) == (s_c, r)
            while True:
                x0 = rng.randrange(p); y0 = sqrt_mod((x0**3+A*x0+B) % p, p, rng)
                if y0:
                    break
            f = [1, (3*x0*x0+A)*pow(y0, -1, p) % p, 3*x0 % p, y0]
            cm = prepare_cm_b0(p, f, rng=rng)
            tp = pari_trace(A, B, p)
            assert tp is None or tp == cm.exact_trace
            row = {'p': p, 'bits': p.bit_length(), 'A': A, 'B': B, 's': s_c, 'r': r, 'trace_theorem5': cm.exact_trace,
                   'trace_pari': tp, 'K_cm': cm.evaluator.K, 'K_recurrence': None}
            if full:
                Hr, Kr = linear_cartier_data(tuple(f), p)
                assert (Hr, Kr) == (cm.evaluator.H, cm.evaluator.K)
                row['K_recurrence'] = Kr
            while True:
                An, Bn = rng.randrange(p), rng.randrange(p)
                if (4*An**3+27*Bn*Bn) % p and (An, Bn) != (A, B):
                    break
            row['random_negative'] = recognize_depth_three_b0(An, Bn, p)['status']
            assert row['random_negative'] == 'not_in_depth_three_b0_family'
            large.append(row)
    write_csv(HERE/'validation_b0_large_primes.csv', large)
    summary['large_prime_recognitions'] = len(large)
    summary.update({'status': 'passed', 'pari_available': PARI is not None,
                    'elapsed_seconds_not_benchmark': round(time.time()-t_start, 1),
                    'environment': {'python': sys.version, 'platform': platform.platform()},
                    'source_sha256': {n: hashlib.sha256((HERE/n).read_bytes()).hexdigest()
                                      for n in ('depth_three_b0_recognize.py', 'validate_depth_three_b0.py', 'depth_three_recognize.py', 'cli.py')},
                    'note': 'finite agreement is supporting evidence, not proof; counts overlap'})
    (HERE/'validation_b0.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ('environment', 'source_sha256', 'ineligible_primes')}, indent=1))


if __name__ == '__main__':
    main()
