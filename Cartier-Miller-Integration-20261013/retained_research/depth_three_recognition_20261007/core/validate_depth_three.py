"""Validation suite for the depth-three (discriminant -192) family recognizer.

Correctness only; elapsed times are not benchmarks. All independent checks use
exact integer multinomial coefficients, Legendre-symbol point counts, dense
polynomial powers and brute-force root scans, none of which import the
recognizer's transport or extraction formulas. PARI (cypari2) is used only as
an optional second trace source and is recorded when present.
Outputs validation.json and CSV files next to this script.
"""
from __future__ import annotations
import csv
import hashlib
import json
import platform
import random
import sys
import time
from collections import deque
from math import factorial, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from depth_three_recognize import (recognize_depth_three, recognize_short_through_depth_three,  # noqa: E402
                                   verify_supplied_certificate, prepare_from_trace, prepare_cm, family_member,
                                   cm_trace_candidates, decide_trace_sign, primary_prime_from_cornacchia, seed_trace_sextic, RecognizedPreparation, CMPreparation,
                                   ALPHA, GAMMA, MULTIPLIER, ev, FAMILY)
from branch_evaluator import linear_cartier_data, is_prime64  # noqa: E402
from isogeny_closure import short_model  # noqa: E402

SEED = 20261007
EXHAUSTIVE_PRIMES = [73, 97, 193, 241, 313, 337, 409, 433, 457, 577]
FULL_COEFFICIENT_PRIMES = [73, 97, 193, 241]
EXCLUDED_PRIMES = [11, 17, 23, 29, 41, 47, 53, 59, 71, 83, 89, 101, 113, 131, 149, 167, 173, 179, 191]
try:
    import cypari2
    PARI = cypari2.Pari()
    PARI.allocatemem(1 << 30)
except Exception:  # pragma: no cover
    PARI = None


# ---------- independent reference computations ----------

def invariant(A, B, p):
    disc = (4*A**3 + 27*B*B) % p
    assert disc
    return 1728*4*A**3*pow(disc, -1, p) % p


def coefficients(A, B, p):
    """Independent (H, beta) by exact integer multinomial coefficients."""
    h = (p-1)//2
    facts = [factorial(i) for i in range(h+1)]
    out = []
    for k in (p-1, p-2):
        total = 0
        for i in range(h+1):
            j = k-3*i
            ell = h-i-j
            if j >= 0 and ell >= 0:
                total += facts[h]//(facts[i]*facts[j]*facts[ell])*pow(A, j, p)*pow(B, ell, p)
        out.append(total % p)
    return tuple(out)


def legendre_trace(A, B, p):
    h = (p-1)//2
    total = 0
    for x in range(p):
        f = (x**3+A*x+B) % p
        total += 0 if f == 0 else (1 if pow(f, h, p) == 1 else -1)
    return -total


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
    """Tonelli-Shanks; returns a square root of n or None."""
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


def family_set(p):
    """Independent enumeration of {(alpha r^2, gamma r^3)} with exact-tuple arithmetic."""
    sq3 = [v for v in range(p) if v*v % p == 3]
    sq2 = [v for v in range(p) if v*v % p == 2]
    assert len(sq3) == 2 and len(sq2) == 2
    members = {}
    for e in sq3:
        for g in sq2:
            alpha = (-1095-540*e-540*g-420*e*g) % p
            gamma = (-22198-13860*e-16380*g-8820*e*g) % p
            for r in range(1, p):
                key = (alpha*r*r % p, gamma*r**3 % p)
                assert key not in members, 'parameter collision'
                members[key] = (e, g, r)
    return members


def nondual_depth3_from_A0(p):
    """All endpoints of nondual rational 2-isogeny paths of length exactly three
    starting at the exact seed models (0,B), with brute-force roots."""
    level = {(0, B): [] for B in range(1, p)}
    for _ in range(3):
        nxt = {}
        for (A, B), path in level.items():
            for q in brute_roots(A, B, p):
                if path and q == -2*path[-1] % p:
                    continue
                nxt.setdefault(ref_quotient(A, B, q, p), path+[q])
        level = nxt
    return level


def depth_le2_j_values(p):
    """j-values of the complete (unpruned) seeded closure through depth two."""
    seeds = []
    if p % 3 == 1:
        seeds += [(0, B) for B in range(1, p)]
    if p % 4 == 1:
        seeds += [(A, 0) for A in range(1, p)]
    seen = set(seeds)
    frontier = list(seeds)
    for _ in range(2):
        new = []
        for A, B in frontier:
            for q in brute_roots(A, B, p):
                t = ref_quotient(A, B, q, p)
                if t not in seen:
                    seen.add(t); new.append(t)
        frontier = new
    return {invariant(A, B, p) for A, B in seen}


def next_prime_1_mod_24(start):
    q = start + (1 - start) % 24
    while not is_prime64(q):
        q += 24
    return q


def write_csv(path, rows):
    if not rows:
        return
    with path.open('w', newline='') as handle:
        w = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def main():
    rng = random.Random(SEED)
    t_start = time.time()
    summary = {'status': 'running', 'seed': SEED}
    # ---- 1. retained fixtures ----
    fixture = json.loads((HERE.parents[2]/'fixtures/depth_three_p73.json').read_text())
    p = fixture['p']; t = fixture['short_target']; c = fixture['normalized_cubic']
    rec = recognize_depth_three(t['A'], t['B'], p)
    assert rec['status'] == 'recognized'
    cert = rec['matches'][0]
    assert cert['parameters']['e'] == 21 and cert['parameters']['g'] == 41 and cert['parameters']['r'] == 42
    assert cert['beta_multiplier'] == t['beta_multiplier']
    assert cert['forward_roots'] == t['forward_roots'] and cert['reverse_path']['roots'] == t['reverse_roots']
    assert cert['forward_models'] == t['forward_models'] and cert['reverse_path']['endpoint'] == t['reverse_models'][-1]
    prep = prepare_from_trace(p, c['coefficients_low_to_high'], t['trace'])
    assert isinstance(prep, RecognizedPreparation)
    assert (prep.evaluator.H, prep.evaluator.K) == (c['H'], c['K'])
    assert prep.evaluator.query(c['mu'])['T'] == c['T']
    assert prep.certificate['parameters']['r'] == 42*16 % p  # cubic's short model is the d=16 twist
    # audit certificates: A=0-seed rows at eligible primes recognized, others rejected
    audit_rows = []
    with (HERE.parents[2]/'fixtures/depth_three_four_certificates_20261006.csv').open() as handle:
        for row in csv.DictReader(handle):
            pp = int(row['p']); A, B = json.loads(row['target']); seed = json.loads(row['seed'])
            res = recognize_depth_three(A, B, pp)
            expect = 'recognized' if (int(row['depth']) == 3 and seed[0] == 0 and pp % 24 == 1) else ('not_eligible_prime' if pp % 24 != 1 else 'not_in_depth_three_family')
            assert res['status'] == expect, (row, res['status'])
            if res['status'] == 'recognized':
                m = res['matches'][0]
                assert m['beta_multiplier'] == int(row['inverse_beta_multiplier'])
                assert m['reverse_path']['roots'] == json.loads(row['inverse_roots'])
                assert m['forward_roots'] == json.loads(row['forward_roots'])
            audit_rows.append({'p': pp, 'depth': row['depth'], 'seed': row['seed'], 'target': row['target'], 'status': res['status'],
                               'expected': expect, 'seed_chain': 'A=0' if seed[0] == 0 else 'B=0'})
    summary['audit_certificates'] = {'rows': len(audit_rows),
                                     'recognized': sum(r['status'] == 'recognized' for r in audit_rows),
                                     'B0_chain_depth3_rejected_by_this_family': sum(r['seed_chain'] == 'B=0' and r['depth'] == '3' for r in audit_rows)}
    write_csv(HERE/'validation_audit_certificates.csv', audit_rows)
    # ---- 2. exhaustive recognition vs independent enumerations ----
    exhaustive = []
    member_rows = []
    twist_rows = []
    for p in EXHAUSTIVE_PRIMES:
        assert p % 24 == 1 and is_prime64(p)
        fam = family_set(p)
        d3 = nondual_depth3_from_A0(p)
        assert set(d3) == set(fam), 'nondual depth-3 endpoints from A=0 seeds differ from the family'
        for key, path in d3.items():
            e, g, r = fam[key]
            assert path == [r, (1+2*e)*r % p, (1+2*e+6*g+2*e*g)*r % p]
        low_j = depth_le2_j_values(p)
        fam_j = {invariant(A, B, p) for A, B in fam}
        assert len(fam_j) == 4 and not (fam_j & low_j)
        assert len(fam) == 4*(p-1)
        pos = neg = 0; through = 0
        for A in range(p):
            for B in range(p):
                if (4*A**3+27*B*B) % p == 0:
                    continue
                res = recognize_depth_three(A, B, p)
                if (A, B) in fam:
                    assert res['status'] == 'recognized', (p, A, B, res)
                    assert tuple(res['matches'][0]['parameters'][k] for k in 'egr') == fam[(A, B)]
                    pos += 1
                else:
                    assert res['status'] == 'not_in_depth_three_family', (p, A, B, res)
                    neg += 1
        # combined depth<=3 recognizer on a sample, including all family members at the smallest primes
        sample = list(fam) if p <= 97 else rng.sample(sorted(fam), 48)
        for A, B in sample:
            comb = recognize_short_through_depth_three(A, B, p)
            assert comb['status'] == 'recognized' and comb['depth_two_status'] == 'not_in_depth_at_most_two_closure'
            through += 1
        exhaustive.append({'p': p, 'nonsingular_models': pos+neg, 'family_members': len(fam), 'recognized_positives': pos,
                           'rejected_negatives': neg, 'family_j_values': len(fam_j), 'depth_le2_j_values': len(low_j),
                           'family_j_in_lower_depth': len(fam_j & low_j), 'combined_depth_le3_checked': through})
        # ---- 3. independent coefficient / trace checks ----
        members = sorted(fam) if p in FULL_COEFFICIENT_PRIMES else rng.sample(sorted(fam), 40)
        for A, B in members:
            e, g, r = fam[(A, B)]
            H, beta = coefficients(A, B, p)
            tau = legendre_trace(A, B, p)
            tp = pari_trace(A, B, p)
            mult = ev(MULTIPLIER, e, g, p)*r % p
            assert H == tau % p and H != 0 and beta == mult*H % p
            assert tp is None or tp == tau
            member_rows.append({'p': p, 'A': A, 'B': B, 'e': e, 'g': g, 'r': r, 'j': invariant(A, B, p), 'H': H, 'beta': beta,
                                'trace_legendre': tau, 'trace_pari': tp, 'beta_multiplier': mult, 'beta_equals_multiplier_H': True})
        # ---- 4. twists ----
        tw_members = rng.sample(sorted(fam), 6)
        ds = range(1, p) if p == 73 else [2, 3, p-1, rng.randrange(2, p), rng.randrange(2, p)]
        for A, B in tw_members:
            e, g, r = fam[(A, B)]
            H, beta = coefficients(A, B, p)
            for d in ds:
                Ad, Bd = d*d*A % p, d**3*B % p
                res = recognize_depth_three(Ad, Bd, p)
                assert res['status'] == 'recognized'
                prm = res['matches'][0]['parameters']
                assert (prm['e'], prm['g'], prm['r']) == (e, g, d*r % p)
                chi = pow(d, (p-1)//2, p)
                chi = 1 if chi == 1 else -1
                Hd, bd = coefficients(Ad, Bd, p)
                assert Hd == chi*H % p and bd == d*chi*beta % p
                assert res['matches'][0]['beta_multiplier'] == d*ev(MULTIPLIER, e, g, p)*r % p
                twist_rows.append({'p': p, 'A': A, 'B': B, 'd': d, 'chi_d': chi, 'A_d': Ad, 'B_d': Bd, 'r_d': prm['r'],
                                   'H_d': Hd, 'beta_d': bd, 'multiplier_d': res['matches'][0]['beta_multiplier']})
    write_csv(HERE/'validation_exhaustive.csv', exhaustive)
    write_csv(HERE/'validation_members.csv', member_rows)
    write_csv(HERE/'validation_twists.csv', twist_rows)
    summary['exhaustive'] = exhaustive
    summary['member_coefficient_checks'] = len(member_rows)
    summary['pari_trace_cross_checks'] = sum(r['trace_pari'] is not None for r in member_rows)
    summary['twist_checks'] = len(twist_rows)
    # ---- 5. tampered certificates ----
    tampered = []
    base = recognize_depth_three(4, 16, 73)['matches'][0]
    assert verify_supplied_certificate(73, 4, 16, base)['beta_multiplier'] == 15
    for label, change in [('e_negated', {'e': -21 % 73}), ('g_negated', {'g': -41 % 73}), ('r_scaled', {'r': 2*42 % 73}),
                          ('e_not_sqrt3', {'e': 5}), ('r_zero', {'r': 0})]:
        bad = json.loads(json.dumps(base)); bad['parameters'].update(change)
        try:
            verify_supplied_certificate(73, 4, 16, bad); ok = False
        except (ValueError, AssertionError) as err:
            ok = True; msg = str(err)
        assert ok
        tampered.append({'case': label, 'rejected': True, 'error': msg})
    for label, key, value in [('slope_altered', 'beta_multiplier', 16), ('roots_altered', 'forward_roots', [42, 54, 2])]:
        bad = json.loads(json.dumps(base)); bad[key] = value
        try:
            verify_supplied_certificate(73, 4, 16, bad); ok = False
        except (ValueError, AssertionError) as err:
            ok = True; msg = str(err)
        assert ok
        tampered.append({'case': label, 'rejected': True, 'error': msg})
    for label, path, value in [('reverse_endpoint_altered', ('reverse_path', 'endpoint'), [0, 8]),
                               ('reverse_roots_altered', ('reverse_path', 'roots'), [71, 6, 44]),
                               ('forward_models_altered', ('forward_models',), [[0, 7], [39, 8], [50, 22], [4, 17]]),
                               ('depth_altered', ('depth',), 2), ('forward_seed_altered', ('forward_seed',), [0, 8]),
                               ('unknown_field_added', ('bogus',), 1)]:
        bad = json.loads(json.dumps(base)); node = bad
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value
        try:
            verify_supplied_certificate(73, 4, 16, bad); ok = False
        except (ValueError, AssertionError) as err:
            ok = True; msg = str(err)
        assert ok, label
        tampered.append({'case': label, 'rejected': True, 'error': msg})
    bad = json.loads(json.dumps(base)); bad['family'] = 'depth2_0'
    try:
        verify_supplied_certificate(73, 4, 16, bad); ok = False
    except ValueError as err:
        ok = True; msg = str(err)
    assert ok
    tampered.append({'case': 'family_label_altered', 'rejected': True, 'error': msg})
    # wrong model for a valid certificate
    try:
        verify_supplied_certificate(73, 5, 16, base); ok = False
    except (ValueError, AssertionError) as err:
        ok = True; msg = str(err)
    assert ok
    tampered.append({'case': 'model_altered', 'rejected': True, 'error': msg})
    write_csv(HERE/'validation_tampered.csv', tampered)
    summary['tampered_certificates_rejected'] = len(tampered)
    # ---- 6. excluded primes and invalid inputs ----
    excluded = []
    inv = json.loads((HERE.parent/'theory/integer_invariants_depth3.json').read_text())
    degenerate = {row['p']: row for row in inv['degenerate_models_at_excluded_primes']}
    for p in EXCLUDED_PRIMES:
        assert p % 24 != 1
        rows = degenerate.get(p, {}).get('rational_parameter_models', [])
        statuses = set()
        for A in range(p):
            for B in range(p):
                if (4*A**3+27*B*B) % p:
                    statuses.add(recognize_depth_three(A, B, p)['status'])
        assert statuses == {'not_eligible_prime'}
        excluded.append({'p': p, 'p_mod_24': p % 24, 'recognizer_status': 'not_eligible_prime',
                         'rational_parameter_models': len(rows),
                         'alpha_zero': sum(r['alpha'] == 0 for r in rows), 'gamma_zero': sum(r['gamma'] == 0 for r in rows),
                         'singular': sum(r['Delta'] == 0 for r in rows)})
    write_csv(HERE/'validation_excluded_primes.csv', excluded)
    summary['excluded_primes'] = excluded
    invalid = 0
    for args in [(4, 16, 6), (4, 16, 75), (0, 0, 73), (4, 16, 2**64+13)]:
        try:
            recognize_depth_three(*args); raise AssertionError('accepted invalid input')
        except ValueError:
            invalid += 1
    try:
        prepare_from_trace(73, [1, 4, 0, 37], 20); raise AssertionError('accepted trace outside Hasse interval')
    except ValueError:
        invalid += 1
    try:
        prepare_from_trace(73, [1, 4, 0, 0], 10); raise AssertionError('accepted degenerate cubic')
    except ValueError:
        invalid += 1
    summary['invalid_inputs_rejected'] = invalid
    # ---- 7. original normalized cubics, K and branch queries ----
    cubic_rows = []
    for p in [73, 97, 193, 241, 313]:
        fam = family_set(p)
        for A, B in rng.sample(sorted(fam), 8 if p > 73 else 16):
            # random rational point (x0,y0) with y0 nonzero gives f = 1 + (F'(x0)/y0) w + 3 x0 w^2 + y0 w^3
            while True:
                x0 = rng.randrange(p); fx = (x0**3+A*x0+B) % p
                y0 = sqrt_mod(fx, p, rng)
                if y0:
                    break
            cval = (3*x0*x0+A)*pow(y0, -1, p) % p
            f = [1, cval, 3*x0 % p, y0]
            assert short_model(f, p) == (A, B)
            H_ref, K_ref = linear_cartier_data(tuple(f), p)
            tau = legendre_trace(A, B, p)
            assert H_ref == tau % p
            prep = prepare_from_trace(p, f, tau)
            assert isinstance(prep, RecognizedPreparation)
            assert prep.evaluator.K == K_ref and prep.evaluator.H == H_ref
            dense = dense_power(f, p)
            assert (dense[p-1], dense[p-2]) == (H_ref, K_ref)
            roots = [(q-x0)*pow(y0, -1, p) % p for q in brute_roots(A, B, p)]
            assert roots and all(mu for mu in roots)
            for mu in roots:
                T_ref = sum(dense[i]*pow(mu, i, p) for i in range(p)) % p
                out = prep.evaluator.query(mu)
                assert out['T'] == T_ref and out['status'] == 'computed_from_trusted_data'
                cubic_rows.append({'p': p, 'f': json.dumps(f), 'A': A, 'B': B, 'x0': x0, 'y0': y0, 'trace': tau, 'H': H_ref,
                                   'K_recurrence': K_ref, 'K_recognized': prep.evaluator.K, 'mu': mu, 'T_dense': T_ref, 'T_query': out['T']})
    write_csv(HERE/'validation_cubics.csv', cubic_rows)
    summary['original_cubic_branch_queries'] = len(cubic_rows)
    summary['original_cubic_curves'] = len({(r['p'], r['f']) for r in cubic_rows})
    # ---- 8. larger primes ----
    large_rows = []
    for size, full in [(10**5, True), (10**6, True), (2**31, False), (2**40, False), (2**62, False)]:
        p = next_prime_1_mod_24(rng.randrange(size, size+size//4))
        e = sqrt_mod(3, p, rng); g = sqrt_mod(2, p, rng)
        for _ in range(3):
            e_s = e if rng.random() < .5 else p-e
            g_s = g if rng.random() < .5 else p-g
            r = rng.randrange(1, p)
            A, B = family_member(p, e_s, g_s, r)
            res = recognize_depth_three(A, B, p)
            assert res['status'] == 'recognized'
            prm = res['matches'][0]['parameters']
            assert (prm['e'], prm['g'], prm['r']) == (e_s, g_s, r)
            mult = res['matches'][0]['beta_multiplier']
            row = {'p': p, 'bits': p.bit_length(), 'A': A, 'B': B, 'e': e_s, 'g': g_s, 'r': r, 'beta_multiplier': mult,
                   'reverse_roots': json.dumps(res['matches'][0]['reverse_path']['roots']), 'independent_H_K': full}
            tp = pari_trace(A, B, p)
            row['trace_pari'] = tp
            if full:
                # O(p) independent recurrence on a normalized cubic through a rational point
                while True:
                    x0 = rng.randrange(p); y0 = sqrt_mod((x0**3+A*x0+B) % p, p, rng)
                    if y0:
                        break
                f = [1, (3*x0*x0+A)*pow(y0, -1, p) % p, 3*x0 % p, y0]
                H_ref, K_ref = linear_cartier_data(tuple(f), p)
                tau = H_ref if H_ref <= 2*int(p**.5)+1 else H_ref-p
                assert tau*tau <= 4*p and tau % p == H_ref
                assert tp is None or tp == tau
                prep = prepare_from_trace(p, f, tau)
                assert prep.evaluator.K == K_ref
                row.update({'H': H_ref, 'K_recurrence': K_ref, 'K_recognized': prep.evaluator.K, 'trace_lifted_from_H': tau})
            else:
                row.update({'H': None if tp is None else tp % p, 'K_recurrence': None,
                            'K_recognized': None if tp is None else (mult*(tp % p)) % p, 'trace_lifted_from_H': None})
            # negative control: random nonsingular model at the same prime
            while True:
                An, Bn = rng.randrange(p), rng.randrange(p)
                if (4*An**3+27*Bn*Bn) % p and (An, Bn) != (A, B):
                    break
            row['random_negative_status'] = recognize_depth_three(An, Bn, p)['status']
            assert row['random_negative_status'] == 'not_in_depth_three_family'
            large_rows.append(row)
    write_csv(HERE/'validation_large_primes.csv', large_rows)
    summary['large_prime_recognitions'] = len(large_rows)
    summary['large_prime_independent_K_checks'] = sum(r['independent_H_K'] for r in large_rows)
    # ---- 9. CM trace candidates, sign decision and complete preparation ----
    cm_rows = []
    primes_1_24 = [q for q in range(73, 3000) if q % 24 == 1 and is_prime64(q)]
    for p in primes_1_24:
        t0, fc, info = cm_trace_candidates(p, rng)
        # uniqueness of 4p = t^2 + 192 f^2 with t, f > 0 by brute force
        sols = [(t, isqrt((4*p-t*t)//192)) for t in range(1, 2*isqrt(p)+2) if (4*p-t*t) > 0 and (4*p-t*t) % 192 == 0 and 192*isqrt((4*p-t*t)//192)**2 == 4*p-t*t]
        assert sols == [(t0, fc)], (p, sols, t0, fc)
        e = sqrt_mod(3, p, rng); g = sqrt_mod(2, p, rng)
        r = rng.randrange(1, p)
        A, B = family_member(p, e, g, r)
        tau = legendre_trace(A, B, p)
        assert abs(tau) == t0, (p, tau, t0)
        decided, sinfo = decide_trace_sign(A, B, p, t0, rng)
        assert decided == tau, (p, decided, tau)
        pi = primary_prime_from_cornacchia(p, info['x'], info['y'])
        sextic, _ = seed_trace_sextic(p, -pow(r, 3, p), pi)
        assert sextic == tau, (p, sextic, tau)
        cm_rows.append({'sign_sextic': sextic, 'p': p, 't0': t0, 'f': fc, 'x': info['x'], 'cubic_nonresidue_trials': info['cubic_nonresidue_trials'],
                        'A': A, 'B': B, 'trace_legendre': tau, 'sign_decided': decided, 'sign_trials': sinfo['trials']})
    write_csv(HERE/'validation_cm_trace.csv', cm_rows)
    summary['cm_trace_primes_checked'] = len(cm_rows)
    summary['cm_sign_trials_max'] = max(r['sign_trials'] for r in cm_rows)
    # Ireland-Rosen Theorem 4 for every y^2 = x^3 + D at every p = 1 mod 3 below 400 (independent of the family)
    sextic_rows = []
    for p in [q for q in range(7, 400) if q % 3 == 1 and is_prime64(q)]:
        # independent primary prime by exhaustive search
        pi = next((x, y) for x in range(-2*isqrt(p)-2, 2*isqrt(p)+3) for y in range(-2*isqrt(p)-2, 2*isqrt(p)+3)
                  if x*x-x*y+y*y == p and x % 3 == 2 and y % 3 == 0)
        agree = sum(seed_trace_sextic(p, D, pi)[0] == legendre_trace(0, D, p) for D in range(1, p))
        assert agree == p-1, (p, agree)
        sextic_rows.append({'p': p, 'primary_pi_a': pi[0], 'primary_pi_b': pi[1], 'D_values_checked': p-1, 'agree_with_legendre': agree})
    assert seed_trace_sextic(13, 1, (-1, 3))[0] == 2  # Ireland-Rosen worked example: N_13 = 12
    write_csv(HERE/'validation_sextic_sign.csv', sextic_rows)
    summary['sextic_theorem4_checks'] = {'primes': len(sextic_rows), 'curves': sum(r['D_values_checked'] for r in sextic_rows),
                                         'ireland_rosen_example_p13_D1': 'trace 2, N=12, reproduced'}
    # complete prepare_cm against trusted-trace preparation on cubics, including large primes with PARI traces
    cm_prep_rows = []
    for p in [73, 97, 193, 241, 577, 1009]:
        fam_e = sqrt_mod(3, p, rng); fam_g = sqrt_mod(2, p, rng)
        for _ in range(4):
            A, B = family_member(p, fam_e if rng.random() < .5 else p-fam_e, fam_g if rng.random() < .5 else p-fam_g, rng.randrange(1, p))
            while True:
                x0 = rng.randrange(p); y0 = sqrt_mod((x0**3+A*x0+B) % p, p, rng)
                if y0:
                    break
            f = [1, (3*x0*x0+A)*pow(y0, -1, p) % p, 3*x0 % p, y0]
            tau = legendre_trace(A, B, p)
            ref = prepare_from_trace(p, f, tau, verify_sign=True)
            got = prepare_cm(p, f, rng=rng)
            lv = prepare_cm(p, f, rng=rng, sign_method='las_vegas', max_trials=None)
            assert lv.exact_trace == got.exact_trace
            assert isinstance(got, CMPreparation) and isinstance(ref, RecognizedPreparation)
            assert got.exact_trace == tau and (got.evaluator.H, got.evaluator.K) == (ref.evaluator.H, ref.evaluator.K)
            H_ref, K_ref = linear_cartier_data(tuple(f), p)
            assert (got.evaluator.H, got.evaluator.K) == (H_ref, K_ref)
            cm_prep_rows.append({'p': p, 'f': json.dumps(f), 'trace_legendre': tau, 'trace_cm': got.exact_trace, 'H': H_ref, 'K_recurrence': K_ref,
                                 'K_cm': got.evaluator.K, 'sign_method': got.trace_preparation['sign_method'],
                                 'las_vegas_trials': lv.trace_preparation['sign_test']['trials'], 'trace_pari': pari_trace(A, B, p)})
    for size in (2**31, 2**40, 2**62):
        p = next_prime_1_mod_24(rng.randrange(size, size+size//4))
        e = sqrt_mod(3, p, rng); g = sqrt_mod(2, p, rng)
        A, B = family_member(p, e, g, rng.randrange(1, p))
        while True:
            x0 = rng.randrange(p); y0 = sqrt_mod((x0**3+A*x0+B) % p, p, rng)
            if y0:
                break
        f = [1, (3*x0*x0+A)*pow(y0, -1, p) % p, 3*x0 % p, y0]
        got = prepare_cm(p, f, rng=rng)
        lv = prepare_cm(p, f, rng=rng, sign_method='las_vegas', max_trials=None)
        assert isinstance(got, CMPreparation) and lv.exact_trace == got.exact_trace
        tp = pari_trace(A, B, p)
        assert tp is None or tp == got.exact_trace
        cm_prep_rows.append({'p': p, 'f': json.dumps(f), 'trace_legendre': None, 'trace_cm': got.exact_trace, 'H': got.evaluator.H,
                             'K_recurrence': None, 'K_cm': got.evaluator.K, 'sign_method': got.trace_preparation['sign_method'],
                             'las_vegas_trials': lv.trace_preparation['sign_test']['trials'], 'trace_pari': tp})
    write_csv(HERE/'validation_cm_preparation.csv', cm_prep_rows)
    summary['cm_complete_preparations'] = len(cm_prep_rows)
    # wrong supplied traces
    wrong = []
    for t, label in [(11, 'odd_impossible'), (0, 'zero_impossible'), (12, 'hasse_ok_but_not_192_form'), (-10, 'wrong_sign_sextic')]:
        try:
            prepare_from_trace(73, [1, 4, 0, 37], t, verify_sign=True, rng=rng); ok = False
        except ValueError as err:
            ok = True; msg = str(err)
        assert ok, label
        wrong.append({'trace': t, 'case': label, 'rejected': True, 'error': msg})
    try:
        prepare_from_trace(73, [1, 4, 0, 37], -10, verify_sign='las_vegas', rng=rng, max_trials=None); ok = False
    except ValueError as err:
        ok = True; msg = str(err)
    assert ok
    wrong.append({'trace': -10, 'case': 'wrong_sign_las_vegas', 'rejected': True, 'error': msg})
    assert isinstance(prepare_from_trace(73, [1, 4, 0, 37], 10, verify_sign=True, rng=rng), RecognizedPreparation)
    assert isinstance(prepare_from_trace(73, [1, 4, 0, 37], 10, verify_sign='las_vegas', rng=rng, max_trials=None), RecognizedPreparation)
    write_csv(HERE/'validation_wrong_traces.csv', wrong)
    summary['wrong_supplied_traces_rejected'] = len(wrong)
    # ---- summary ----
    summary.update({'status': 'passed', 'exhaustive_primes': EXHAUSTIVE_PRIMES, 'excluded_primes_tested': EXCLUDED_PRIMES,
                    'pari_available': PARI is not None,
                    'elapsed_seconds_not_benchmark': round(time.time()-t_start, 1),
                    'environment': {'python': sys.version, 'platform': platform.platform(), 'machine': platform.machine()},
                    'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                                      for name in ('depth_three_recognize.py', 'validate_depth_three.py', 'cli.py')},
                    'dependency_sha256': {'branch_evaluator.py': hashlib.sha256((HERE.parents[1]/'branch_point_20261006/branch_evaluator.py').read_bytes()).hexdigest(),
                                          'isogeny_closure.py': hashlib.sha256((HERE.parents[1]/'isogeny_closure_20261006/core/isogeny_closure.py').read_bytes()).hexdigest(),
                                          'recognize.py': hashlib.sha256((HERE.parents[1]/'depth_two_recognition_20261006/core/recognize.py').read_bytes()).hexdigest()},
                    'note': 'finite agreement is supporting evidence, not proof; counts overlap and are not disjoint coverage'})
    (HERE/'validation.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ('environment', 'source_sha256', 'dependency_sha256')}, indent=1))


if __name__ == '__main__':
    main()
