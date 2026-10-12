"""p-adic pilot: the slope from the canonical subgroup of an arbitrary lift.

Derived identity (feasibility note, Proposition 4): for ANY short Weierstrass
lift E~ = (A~, B~) over Z_p of an ordinary E/F_p, with C = E~[p]^0 its
canonical (connected) subgroup and sigma_C = sum_{Q in C - O} x(Q),

        sigma_C == 0 (mod p)      and      kappa == sigma_C / p (mod p).

The canonical lift is NOT needed for this identity.  This script computes C
by Hensel-factoring the reversed p-division polynomial Psi(s) = s^d f_p(1/s)
(s = 1/x) as G(s) R(s) with G == s^h (mod p), then tests the identity for the
trivial lift, a random lift and the canonical lift (obtained by Deligne-Tate
iteration E~ -> E~/C).  It also tests the Frobenius-lift scale (d0 = t),
CM-over-Q canonical lifts, retained fixed-D tables, AB = 0 insufficiency of
j mod p^2, original-cubic (H, K, T) reconstruction, twists and same-trace
pairs.  This is a verification pilot built from degree-(p^2-1)/2 data; it is
NOT a proposed fast algorithm.  Exit status is nonzero on any failure.
"""
from pathlib import Path
import csv
import importlib.util
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from okp_common import (CheckFailure, require, PAdic, nonsingular, trace_by_count,  # noqa: E402
                        j_invariant, H_beta_recurrence, division_polynomial_odd, points,
                        cubic_from_point, short_model_of_cubic, branch_outputs_from_kappa,
                        branch_outputs_direct, sha256_file, environment, pmul)
import okp_config  # noqa: E402

OUT = HERE / 'results'


# ---------------------------------------------------------------- canonical subgroup
def canonical_factor(At, Bt, p, N):
    """Monic G(s) in (Z/p^N)[s], deg h, G == s^h mod p, with G | Psi, Psi(s) = s^d f_p(1/s).
    Roots of G are s = 1/x(Q), one per pair {Q, -Q} of C - O."""
    M = p ** N
    h = (p - 1) // 2
    d = (p * p - 1) // 2
    f = division_polynomial_odd(p, At, Bt, M)
    f = f + [0] * (d + 1 - len(f))
    require(len(f) == d + 1 and f[d] % M == p % M, 'p-division polynomial degree/leading coefficient')
    Psi = [f[d - i] % M for i in range(d + 1)]
    require(all(Psi[i] % p == 0 for i in range(h)) and Psi[h] % p != 0,
            'Psi mod p is not s^h times a unit-constant polynomial (not ordinary?)')
    R1 = [Psi[h + i] % p for i in range(d - h + 1)]
    # b = R1^{-1} mod s^h (mod p)
    b = [0] * h
    inv0 = pow(R1[0], -1, p)
    b[0] = inv0
    for k in range(1, h):
        s = sum(R1[i] * b[k - i] for i in range(1, min(k, len(R1) - 1) + 1)) % p
        b[k] = (-s * inv0) % p
    G = [0] * h + [1]
    R = list(R1)
    for k in range(1, N):
        pk = p ** k
        modk1 = pk * p
        # E = (Psi - G R)/p^k mod p ; G has degree h, R degree d - h
        GR = [0] * (d + 1)
        for i, g in enumerate(G):
            if g % modk1:
                for jj, r in enumerate(R):
                    GR[i + jj] += g * r
        E = []
        for i in range(d + 1):
            diff = (Psi[i] - GR[i]) % modk1
            require(diff % pk == 0, 'Hensel invariant broken')
            E.append(diff // pk % p)
        dG = [sum(b[i] * E[k2 - i] for i in range(k2 + 1)) % p for k2 in range(h)]
        RdG = pmul(R1, dG, p)
        resid = [(E[i] - (RdG[i] if i < len(RdG) else 0)) % p for i in range(d + 1)]
        require(all(resid[i] == 0 for i in range(h)), 'Hensel division not exact')
        dR = resid[h:]
        G = [(G[i] + pk * (dG[i] if i < h else 0)) % M for i in range(h + 1)]
        R = [(R[i] + pk * dR[i]) % M for i in range(d - h + 1)]
    # final verification of the factorization modulo p^N
    GR = [0] * (d + 1)
    for i, g in enumerate(G):
        for jj, r in enumerate(R):
            GR[i + jj] += g * r
    require(all((GR[i] - Psi[i]) % M == 0 for i in range(d + 1)), 'final factorization check failed')
    return G


def subgroup_data(At, Bt, p, N):
    """sigma_C, kappa_C and the Vélu codomain (A', B') of E~ -> E~/C, as p-adic numbers."""
    G = canonical_factor(At, Bt, p, N)
    h = (p - 1) // 2
    P = lambda n: PAdic.from_int(p, n, N)  # noqa: E731
    g = [P(c) for c in G]
    require(g[0].val == 1, f'v(G(0)) = {g[0].val}, expected 1')
    c = [None] + [g[k] / g[0] for k in range(1, 4)]
    S1 = -c[1]
    S2 = -(c[1] * S1) - 2 * c[2]
    S3 = -(c[1] * S2) - c[2] * S1 - 3 * c[3]
    sigma = 2 * S1
    require(sigma.is_zero() or sigma.val >= 1, f'sigma_C not divisible by p (val {sigma.val})')
    At_, Bt_ = P(At), P(Bt)
    tC = 6 * S2 + 2 * h * At_
    wC = 10 * S3 + 6 * At_ * S1 + 4 * h * Bt_
    A1 = At_ - 5 * tC
    B1 = Bt_ - 7 * wC
    return {'G': G, 'sigma': sigma, 'kappa_C': (sigma / p).residue(1), 'sigma_over_p_mod_p2': (sigma / p).residue(2)
            if (sigma / p).aprec >= 2 else None, 'A1': A1, 'B1': B1, 'S1': S1}


def lift_slope(At, Bt, p, N):
    return subgroup_data(At, Bt, p, N)['kappa_C']


def kappa_identity_only(At, Bt, p, N):
    """kappa_C from the canonical factor alone at working precision p^N (no codomain data).
    The identity needs G_0 mod p^2 and G_1 mod p^3, so N = 3 must suffice and N = 2 must
    be refused by the precision tracking rather than return an unsupported digit."""
    G = canonical_factor(At, Bt, p, N)
    g0, g1 = PAdic.from_int(p, G[0], N), PAdic.from_int(p, G[1], N)
    require(g0.val == 1, 'v(G0) != 1')
    sigma = 2 * (-(g1 / g0))
    return (sigma / p).residue(1)


def deligne_tate_step(At, Bt, p, N):
    """E~ -> E~/C, rescaled to a model reducing to (At mod p, Bt mod p). Requires A B != 0 mod p."""
    sd = subgroup_data(At, Bt, p, N)
    A1, B1 = sd['A1'], sd['B1']
    require(A1.val >= 4 and B1.val >= 6, f'codomain valuations ({A1.val},{B1.val}) not >= (4,6)')
    alpha = A1 / p ** 4
    betap = B1 / p ** 6
    mu = (betap / alpha) * (PAdic.from_int(p, At, N) / PAdic.from_int(p, Bt, N))
    An = alpha / (mu * mu)
    Bn = betap / (mu * mu * mu)
    return sd, alpha, betap, mu, An, Bn


def j_padic(Ap, Bp):
    return 6912 * Ap * Ap * Ap / (4 * Ap * Ap * Ap + 27 * Bp * Bp)


def unit_root(t, p, k):
    """Unit root lambda of X^2 - t X + p modulo p^k (lambda == t mod p)."""
    M = p ** k
    lam = t % p
    for _ in range(k + 2):
        f = (lam * lam - t * lam + p) % M
        fp = (2 * lam - t) % M
        lam = (lam - f * pow(fp, -1, M)) % M
    require((lam * lam - t * lam + p) % M == 0, 'unit root Hensel failed')
    return lam


def canonical_lift_by_iteration(A, B, p, N, steps):
    At, Bt = A % p, B % p
    js = []
    record = None
    for k in range(steps):
        sd, alpha, betap, mu, An, Bn = deligne_tate_step(At, Bt, p, N)
        js.append(j_padic(PAdic.from_int(p, At, N), PAdic.from_int(p, Bt, N)))
        prec = min(N, An.aprec, Bn.aprec)
        At, Bt = An.residue(prec), Bn.residue(prec)
        record = (sd, alpha, betap, mu)
    js.append(j_padic(PAdic.from_int(p, At, N), PAdic.from_int(p, Bt, N)))
    return At, Bt, js, record


# ---------------------------------------------------------------- retained positive controls
def load_retained(deps):
    paths = deps['paths']
    info = {'paths': paths, 'missing': deps['missing'], 'modules': {}}
    mods = {}
    if 'extension' in paths:
        path = Path(paths['extension']) / 'core' / 'fixed_D_evaluator.py'
        spec = importlib.util.spec_from_file_location('retained_fixed_D_evaluator', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mods['fixed_D'] = mod
        info['modules']['fixed_D_evaluator'] = {'__file__': mod.__file__, 'sha256': sha256_file(mod.__file__),
                                                'table': mod.TABLE_PATH, 'table_sha256': sha256_file(mod.TABLE_PATH)}
    if 'retained' in paths:
        core = Path(paths['retained']) / 'depth_three_recognition_20261007' / 'core'
        for name in ('depth_three_recognize', 'depth_three_b0_recognize'):
            fpath = core / f'{name}.py'
            info['modules'][name] = {'__file__': str(fpath), 'sha256': sha256_file(fpath),
                                     'note': 'hash recorded here; executed by retained_dependency_check.py'}
    return mods, info


# ---------------------------------------------------------------- main checks
def main(deps):
    t_start = time.time()
    OUT.mkdir(exist_ok=True)
    rng = random.Random(1012)
    mods, retained_info = load_retained(deps)
    fixedD = mods.get('fixed_D')
    table = fixedD.load_table() if fixedD else None
    rows = []
    counters = {k: 0 for k in ('lift_checks', 'trivial', 'random', 'canonical', 'scale_checks',
                               'dt_convergence_checks', 'cubic_HKT_checks', 'branch_queries',
                               'retained_fixedD_agreements', 'HD_root_checks', 'twist_checks',
                               'second_digit_differs', 'second_digit_same',
                               'precision_floor_N3_agreements', 'precision_floor_N2_refusals')}
    N = 14
    plan = [(7, 'exhaustive'), (11, 'exhaustive'), (13, 'exhaustive'), (17, 'exhaustive'), (19, 40), (23, 25)]
    for p, mode in plan:
        models = [(A, B) for A in range(p) for B in range(p) if nonsingular(A, B, p)]
        if mode != 'exhaustive':
            models = rng.sample(models, mode)
        for A, B in models:
            H, beta = H_beta_recurrence(A, B, p)
            if H == 0:
                continue
            t = trace_by_count(A, B, p)
            kappa = beta * pow(H, -1, p) % p
            row = {'p': p, 'A': A, 'B': B, 'j': j_invariant(A, B, p), 'trace': t, 'kappa_target': kappa}
            # trivial lift
            sd0 = subgroup_data(A, B, p, N)
            require(sd0['kappa_C'] == kappa, f'trivial-lift kappa_C {sd0["kappa_C"]} != {kappa} at {(p, A, B)}')
            counters['trivial'] += 1
            # Frobenius-lift scale: alpha t^4 == A, beta' t^6 == B (mod p), i.e. d0 = p/u == +-t
            A1, B1 = sd0['A1'], sd0['B1']
            if A % p:
                require(A1.val == 4 and ((A1 / p ** 4) * t ** 4).residue(1) == A % p, f'scale check A at {(p, A, B)}')
            else:
                require(A1.val >= 5, 'A=0: codomain A not divisible by p^5')
            if B % p:
                require(B1.val == 6 and ((B1 / p ** 6) * t ** 6).residue(1) == B % p, f'scale check B at {(p, A, B)}')
            else:
                require(B1.val >= 7, 'B=0: codomain B not divisible by p^7')
            counters['scale_checks'] += 1
            # random lift
            Ar = A + p * rng.randrange(p ** (N - 1))
            Br = B + p * rng.randrange(p ** (N - 1))
            sdr = subgroup_data(Ar, Br, p, N)
            require(sdr['kappa_C'] == kappa, f'random-lift kappa_C != kappa at {(p, A, B)}')
            counters['random'] += 1
            if sdr['sigma_over_p_mod_p2'] != sd0['sigma_over_p_mod_p2']:
                counters['second_digit_differs'] += 1
            else:
                counters['second_digit_same'] += 1
            if p <= 13:
                require(kappa_identity_only(A, B, p, 3) == kappa, f'N=3 precision floor fails at {(p, A, B)}')
                counters['precision_floor_N3_agreements'] += 1
                try:
                    kappa_identity_only(A, B, p, 2)
                    raise CheckFailure(f'N=2 returned a digit without justified precision at {(p, A, B)}')
                except CheckFailure as exc:
                    require('insufficient precision' in str(exc), f'unexpected N=2 failure: {exc}')
                    counters['precision_floor_N2_refusals'] += 1
            row.update({'kappa_trivial_lift': sd0['kappa_C'], 'kappa_random_lift': sdr['kappa_C'],
                        'sigma_over_p_mod_p2_trivial': sd0['sigma_over_p_mod_p2'],
                        'sigma_over_p_mod_p2_random': sdr['sigma_over_p_mod_p2']})
            # canonical lift by Deligne-Tate iteration (A B != 0 only)
            if A % p and B % p and p <= 13:
                Ac, Bc, js, rec = canonical_lift_by_iteration(A, B, p, N, steps=3)
                for k in range(1, len(js)):
                    require((js[k] - js[k - 1]).is_zero() or (js[k] - js[k - 1]).val >= k,
                            f'DT iteration not converging at {(p, A, B)}')
                    counters['dt_convergence_checks'] += 1
                sdc = subgroup_data(Ac, Bc, p, N)
                require(sdc['kappa_C'] == kappa, f'canonical-lift kappa_C != kappa at {(p, A, B)}')
                counters['canonical'] += 1
                # mu * lambda^2 == 1 (mod p^2) at the (approximate) canonical lift
                _, alpha, betap, mu = rec[0], rec[1], rec[2], rec[3]
                lam = unit_root(t, p, 3)
                require((mu * lam * lam - 1).is_zero() or (mu * lam * lam - 1).val >= 2,
                        f'Frobenius-lift scale u^2 != (p/lambda)^2 at {(p, A, B)}')
                jc = js[-1]
                row.update({'kappa_canonical_lift': sdc['kappa_C'], 'j_can_mod_p3': jc.residue(3)})
                if table is not None:
                    for D, slope in fixedD.slope_from_cm_table(A, B, p, table):
                        require(slope == kappa, 'retained fixed-D slope disagrees with coefficient target')
                        counters['retained_fixedD_agreements'] += 1
                        HD = table[D]['H']
                        val = sum(PAdic.from_int(p, cf, N) * (jc ** i if i else 1) for i, cf in enumerate(HD))
                        require(val.is_zero() or val.val >= 3, f'H_D(j_can) not 0 mod p^3 for D={D} at {(p, A, B)}')
                        counters['HD_root_checks'] += 1
                        row.setdefault('retained_D', []).append(D)
            # twist law on the lift route
            if p <= 13:
                d = 2
                kt = lift_slope(A * d * d % p, B * d ** 3 % p, p, N)
                require(kt == d * kappa % p, f'twist law fails on lift route at {(p, A, B)}')
                counters['twist_checks'] += 1
            # original cubic reconstruction from the lift-route slope only
            if p <= 13:
                for (x0, y0) in points(A, B, p)[:2]:
                    if y0 == 0:
                        continue
                    f = cubic_from_point(A, B, p, x0, y0)
                    require(short_model_of_cubic(f, p) == (A % p, B % p), 'cubic conversion')
                    K, T = branch_outputs_from_kappa(f, t % p, sd0['kappa_C'], p)
                    Hd, Kd, Td = branch_outputs_direct(f, p)
                    require(Hd == t % p and Kd == K and Td == T, f'(H,K,T) reconstruction mismatch at {(p, A, B)}')
                    counters['cubic_HKT_checks'] += 1
                    counters['branch_queries'] += len(T)
            counters['lift_checks'] += 1
            rows.append(row)

    # ------------------------------------------------ CM-over-Q canonical lifts (j in Z)
    cm_rows = []
    # (label, A, B, known unit-root coordinate c with U = <eta + c omega>, or None)
    cm_models = [('D-3_j0', 0, 1, 0), ('D-4_j1728', 1, 0, 0), ('D-7', -35, -98, 1), ('D-8', -30, 56, -1)]
    for jv, lab in ((-32768, 'D-11'), (54000, 'D-12'), (287496, 'D-16'), (-884736, 'D-19'),
                    (-12288000, 'D-27'), (16581375, 'D-28'), (-884736000, 'D-43')):
        cm_models.append((lab, 3 * jv * (1728 - jv), 2 * jv * (1728 - jv) ** 2, None))
    for lab, A0, B0, cknown in cm_models:
        for p in [q for q in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43) if q > 5]:
            if not nonsingular(A0, B0, p):
                continue
            Ap, Bp = A0 % p, B0 % p
            H, beta = H_beta_recurrence(Ap, Bp, p)
            if H == 0:
                continue
            if p > 23:
                continue
            t = trace_by_count(Ap, Bp, p)
            kappa = beta * pow(H, -1, p) % p
            Nc = 12
            sd = subgroup_data(A0 % p ** Nc, B0 % p ** Nc, p, Nc)  # the rational CM model = canonical lift
            require(sd['kappa_C'] == kappa, f'CM canonical lift kappa_C mismatch {lab} p={p}')
            rec = {'label': lab, 'p': p, 'A': A0, 'B': B0, 'trace': t, 'kappa': kappa}
            A1, B1 = sd['A1'], sd['B1']
            if A0 % p and B0 % p:
                alpha, betap = A1 / p ** 4, B1 / p ** 6
                PA, PB = PAdic.from_int(p, A0, Nc), PAdic.from_int(p, B0, Nc)
                # exact canonical lift: codomain is (u^4 A, u^6 B): j(E/C) == j(E) to high precision
                jdiff = j_padic(alpha, betap) - j_padic(PA, PB)
                require(jdiff.is_zero() or jdiff.val >= 5, f'CM model not fixed by Deligne-Tate {lab} p={p}')
                mu = (betap / alpha) * (PA / PB)
                lam = unit_root(t, p, 6)
                ul = mu * lam * lam - 1
                require(ul.is_zero() or ul.val >= 4, f'u^2 != (p/lambda)^2 for CM lift {lab} p={p}')
                c_can = (sd['sigma'] / p) / (p * mu - 1)
                rec['c_unit_root_mod_p3'] = c_can.residue(3)
                if cknown is not None:
                    require((c_can - cknown).is_zero() or (c_can - cknown).val >= 3,
                            f'unit-root coordinate {c_can.residue(3)} != CM value {cknown} mod p^3 ({lab}, p={p})')
                    rec['c_matches_CM_value_mod_p3'] = True
                # Deligne-Tate from a random NON-canonical lift recovers j_CM mod p^2
                Ar = (A0 + p * rng.randrange(1, p)) % p ** Nc
                Br = (B0 + p * rng.randrange(1, p)) % p ** Nc
                _, alpha2, betap2, _, _, _ = deligne_tate_step(Ar, Br, p, Nc)
                jd = j_padic(alpha2, betap2) - j_padic(PA, PB)
                require(jd.is_zero() or jd.val >= 2, f'DT image of random lift != j_CM mod p^2 ({lab}, p={p})')
                jr = j_padic(PAdic.from_int(p, Ar, Nc), PAdic.from_int(p, Br, Nc)) - j_padic(PA, PB)
                rec['random_lift_j_minus_jCM_val'] = jr.val
                rec['DT_image_j_minus_jCM_val'] = min(jd.val, jd.aprec)
            else:
                rec['c_unit_root_mod_p3'] = 'n/a (A B = 0: kappa = 0 by automorphism)'
            cm_rows.append(rec)

    # ------------------------------------------------ AB = 0: j mod p^2 does not see the deformation
    ab0 = []
    for p in (7, 13, 19):  # p = 1 mod 3: j = 0 ordinary
        B = 1
        if H_beta_recurrence(0, B, p)[0] == 0:
            continue
        for a1 in range(p):
            At = p * a1
            Nn = 10
            PA, PB = PAdic.from_int(p, At, Nn), PAdic.from_int(p, B, Nn)
            jv = j_padic(PA, PB)
            sd = subgroup_data(At, B, p, Nn)
            require(sd['kappa_C'] == 0, 'A=0 lift: kappa_C != 0')
            require(jv.is_zero() or jv.val >= 3, 'A=0 lift: j not 0 mod p^3')
            # DT image is the canonical class: its A-coefficient has valuation >= 4 + 2
            require(sd['A1'].is_zero() or sd['A1'].val >= 6, 'A=0: DT image not canonical mod p^2')
            ab0.append({'p': p, 'model': 'A=0', 'lift_A': At, 'lift_B': B, 'deformation_a1': a1,
                        'j_lift_valuation': min(jv.val, jv.aprec), 'kappa_C': sd['kappa_C'],
                        'DT_image_A_valuation': min(sd['A1'].val, sd['A1'].aprec)})
    for p in (13, 17):  # p = 1 mod 4: j = 1728 ordinary
        A = 1
        if H_beta_recurrence(A, 0, p)[0] == 0:
            continue
        for b1 in range(p):
            Bt = p * b1
            Nn = 10
            PA, PB = PAdic.from_int(p, A, Nn), PAdic.from_int(p, Bt, Nn)
            jv = j_padic(PA, PB) - 1728
            sd = subgroup_data(A, Bt, p, Nn)
            require(sd['kappa_C'] == 0, 'B=0 lift: kappa_C != 0')
            require(jv.is_zero() or jv.val >= 2, 'B=0 lift: j not 1728 mod p^2')
            require(sd['B1'].is_zero() or sd['B1'].val >= 8, 'B=0: DT image not canonical mod p^2')
            ab0.append({'p': p, 'model': 'B=0', 'lift_A': A, 'lift_B': Bt, 'deformation_b1': b1,
                        'j_minus_1728_valuation': min(jv.val, jv.aprec), 'kappa_C': sd['kappa_C'],
                        'DT_image_B_valuation': min(sd['B1'].val, sd['B1'].aprec)})

    # ------------------------------------------------ same-trace pairs (handover fixture)
    pairs_out = []
    fixture = (Path(deps['paths']['handover']) / 'validation' / 'results' / 'same_trace_different_slopes.json'
               if 'handover' in deps['paths'] else None)
    if fixture is not None:
        for pr in json.loads(fixture.read_text()):
            p = pr['p']
            if p > 23:
                continue
            k1 = lift_slope(pr['curve_1']['A'], pr['curve_1']['B'], p, N)
            k2 = lift_slope(pr['curve_2']['A'], pr['curve_2']['B'], p, N)
            require(k1 == pr['curve_1']['kappa'] and k2 == pr['curve_2']['kappa'] and k1 != k2,
                    'same-trace pair: lift route disagrees')
            pairs_out.append({'p': p, 'trace': pr['trace'], 'kappa_C_1': k1, 'kappa_C_2': k2})

    # ------------------------------------------------ write outputs
    cols = ['p', 'A', 'B', 'j', 'trace', 'kappa_target', 'kappa_trivial_lift', 'kappa_random_lift',
            'kappa_canonical_lift', 'sigma_over_p_mod_p2_trivial', 'sigma_over_p_mod_p2_random',
            'j_can_mod_p3', 'retained_D']
    with (OUT / 'padic_lift_slopes.csv').open('w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in cols})
    (OUT / 'padic_cm_canonical_lifts.json').write_text(json.dumps(cm_rows, indent=1))
    (OUT / 'padic_AB0_j_insufficiency.json').write_text(json.dumps(ab0, indent=1))
    (OUT / 'padic_same_trace_pairs.json').write_text(json.dumps(pairs_out, indent=1))
    sizes = [{'p': p, 'division_polynomial_degree': (p * p - 1) // 2, 'canonical_factor_degree': (p - 1) // 2,
              'padic_digits_N': N} for p, _ in plan]
    reduced = deps['missing']
    summary = {'status': 'REDUCED_SCOPE' if reduced else 'PASS', 'failures': 0, 'counters': counters,
               'reduced_scope_reasons': reduced,
               'ordinary_models': len(rows), 'cm_canonical_lift_records': len(cm_rows),
               'ab0_records': len(ab0), 'same_trace_pairs': len(pairs_out),
               'trace_plus_one_models': sum(1 for r in rows if r['trace'] == 1),
               'trace_minus_one_models': sum(1 for r in rows if r['trace'] == -1),
               'data_sizes_of_this_verification_route': sizes,
               'retained': retained_info,
               'source_sha256': {n: sha256_file(HERE / n) for n in ('padic_canonical_subgroup.py', 'okp_common.py')},
               'environment': environment(), 'seconds': round(time.time() - t_start, 1),
               'scope': 'Verification of derived identities from degree-(p^2-1)/2 division-polynomial data; '
                        'not a fast algorithm, not a benchmark, not a proof.'}
    (OUT / 'padic_summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: summary[k] for k in ('status', 'counters', 'ordinary_models', 'cm_canonical_lift_records',
                                               'ab0_records', 'same_trace_pairs', 'trace_plus_one_models',
                                               'trace_minus_one_models', 'seconds')}, indent=1))
    if reduced:
        print('PADIC_PILOT_REDUCED_SCOPE (explicitly allowed missing dependencies):', reduced)
        sys.exit(3)
    print('PADIC_PILOT_PASS')


if __name__ == '__main__':
    _args, _deps = okp_config.parse('p-adic canonical-subgroup pilot')
    try:
        main(_deps)
    except CheckFailure as exc:
        print('FAIL:', exc)
        sys.exit(1)
