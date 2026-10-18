"""Round-3 amendment R3.1 frozen confirmation (fresh inputs).  Run after r3/FREEZE_R3_1.json.

Same structure and checks as r3/confirm_r3.py (frozen, unchanged), with three differences:
(i) the Jacobi sum is reconstructed by the R3.1 lattice chain (r3/jacobi_r31.py) and the API is
r3/acquire_r31.py; (ii) the ledger is r3/evidence/LEDGER_R3_1.json, which adds every prime that
the R3 rule selected in run 1 and every post-freeze development prime; (iii) new bounds:
  S  2.5e6 (q primes 5..47) | M 4e9 (q primes 5..89) | L 4e11 (q in 11, 23, 47, 89)
  E1 5e10 (two per class, no prime 5<=q<=89 divides p-1) | E2 4e9 (q^2 | p-1, q in 5, 7, 11)
  E3 3.5e5 (class A, two primes: some prime 5<=q<=89 divides p-1, none admissible)
  E4 2e10 (ten generic primes per class).
A separate, labelled REGRESSION block (not confirmation) reruns the run-1 failure (p = 3000013781,
q = 89) and the development miss (p = 920889975821, q = 89).
Writes r3/evidence/CONFIRMATION_R3_1.json.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from r3.common import (is_prime, params, flint_factorial, c_from_mfact, a_from_c, ClassNumberPolicy,
                       classno_forms, classno_grh)
from r3.research.ledger_r31 import excluded
from r3 import tal3
from r3.halfint import half_factorial3, halfinterval_c3
from r3.acquire_r31 import acquire_aL, admissible_q, nodal_flint_c, policy, tal_c
from r3.confirm_r3 import binom_aL, CachedPolicy

CLASSES = {'A': (12, 11), 'B': (24, 5), 'C': (24, 17)}
QS = [q for q in range(5, 48) if is_prime(q)]
QM = [q for q in range(5, 90) if is_prime(q)]
QL = [11, 23, 47, 89]


def verify(name):
    fr = json.loads((ROOT / name).read_text())
    for f, digest in fr['sha256'].items():
        if hashlib.sha256((ROOT / f).read_bytes()).hexdigest() != digest:
            raise SystemExit('%s mismatch: %s' % (name, f))
    return fr


def first(bound, mod, res, extra=lambda p: True, count=1):
    out, p = [], bound
    while len(out) < count:
        if p % mod == res and extra(p) and not excluded(p) and is_prime(p):
            out.append(p)
        p += 1
    return out


def select():
    sel = dict(S={}, M={}, L={}, E1={}, E2={}, E3={}, E4={})
    for X, (mo, r) in CLASSES.items():
        sel['S'][X] = {q: first(25 * 10 ** 5, mo, r, lambda p, q=q: p % q == 1)[0] for q in QS}
        sel['M'][X] = {q: first(4 * 10 ** 9, mo, r, lambda p, q=q: p % q == 1)[0] for q in QM}
        sel['L'][X] = {q: first(4 * 10 ** 11, mo, r, lambda p, q=q: p % q == 1)[0] for q in QL}
        sel['E1'][X] = first(5 * 10 ** 10, mo, r, lambda p: all((p - 1) % q for q in QM), 2)
        sel['E2'][X] = {q: first(4 * 10 ** 9, mo, r, lambda p, q=q: (p - 1) % (q * q) == 0)[0] for q in (5, 7, 11)}
        sel['E4'][X] = first(2 * 10 ** 10, mo, r, count=10)
    sel['E3']['A'] = first(35 * 10 ** 4, 12, 11,
                           lambda p: any((p - 1) % q == 0 for q in QM) and not admissible_q(p), 2)
    return sel


def check_prime(p, qlist, small=False):
    import atkin
    t0 = perf_counter()
    P = params(p)
    m = P['m']
    mf = flint_factorial(m, p)
    c_ref = c_from_mfact(p, mf)
    a_ref, D_ref = a_from_c(p, c_ref), atkin.derivative_from_c(p, c_ref)
    rec = dict(p=p, cls='A' if p % 12 == 11 else ('B' if p % 24 == 5 else 'C'), tal={}, hi={}, api={})
    if small:
        lin = 1
        for j in range(1, m + 1):
            lin = lin * j % p
        assert lin == mf, 'linear m!'
        assert binom_aL(p) == a_ref, 'defining binomial'
        assert atkin.wronskian_endpoint(p) == D_ref, 'Wronskian D'
        assert atkin.atkin_endpoint(p) == D_ref, 'Atkin recurrence D'
        rec['independent'] = ['linear m!', 'binom(2L,L)8^-L', 'Wronskian D', 'Atkin recurrence D']
    for q in qlist:
        if (p - 1) % q or (p - 1) // q < policy()['K_min']:
            continue
        for an in (['dup6', 'dup12'] if p % 12 == 5 else ['dup6']):
            c, md = tal_c(p, q, an)
            ok = (c == c_ref and tal3.mfact_from_c(p, c) == mf and a_from_c(p, c) == a_ref
                  and atkin.derivative_from_c(p, c) == D_ref)
            assert ok, ('tal', p, q, an)
            rec['tal']['%d/%s' % (q, an)] = dict(ok=True, k=md['k'], kind=md['anchor_kind'],
                                                 lengths=md['residual_lengths'])
    H_ref = flint_factorial(P['h'], p)
    unc = CachedPolicy(ClassNumberPolicy('unconditional'))
    routes = ['mordell'] if p % 4 == 3 else (['williams_currie', 'gauss4p'] if p % 8 == 5 else ['williams_currie'])
    for route in routes:
        H, hm = half_factorial3(p, unc, route)
        assert H == H_ref, ('H', p, route)
        D = hm.get('D')
        assert classno_grh(D) == hm['classno']
        xf = None
        if abs(D) < 2 * 10 ** 9:
            xf = classno_forms(D)
            assert xf == hm['classno']
        rec['hi'][route] = dict(ok=True, D=D, h=hm['classno'], backend=hm['backend'],
                                status=hm['classno_status'], forms_crosscheck=xf is not None)
    c, hm = halfinterval_c3(p, unc)
    assert c == c_ref
    c, hm2 = halfinterval_c3(p, ClassNumberPolicy('grh'))
    assert c == c_ref and hm2['status'] == 'GRH-conditional'
    assert nodal_flint_c(p) == c_ref
    rec['hi']['hi_uncond_status'] = hm['status']
    for mode in ('unconditional', 'grh'):
        r = acquire_aL(p, mode)
        assert (r['a_L'], r['c_p'], r['m_factorial'], r['D']) == (a_ref, c_ref, mf, D_ref)
        rec['api'][mode] = dict(route=r['route'], q=r['q'], status=r['status'], degraded=r['metadata']['degraded'])
    rec['seconds'] = perf_counter() - t0
    return rec


def main():
    import confirm, confirm_charp
    confirm.verify_freeze()
    confirm_charp.verify_freeze_charp()
    verify('r3/FREEZE_R3.json')
    fr = verify('r3/FREEZE_R3_1.json')
    sel = select()
    out = dict(status='RUNNING', python=sys.version, platform=platform.platform(),
               freeze_timestamp=fr['timestamp_utc'], selection=sel, cases=[], regression=[])
    jobs = []
    for X in CLASSES:
        jobs += [(p, [q], True, 'S') for q, p in sel['S'][X].items()]
        jobs += [(p, [q], False, 'M') for q, p in sel['M'][X].items()]
        jobs += [(p, [q], False, 'L') for q, p in sel['L'][X].items()]
        jobs += [(p, QM, False, 'E1') for p in sel['E1'][X]]
        jobs += [(p, [q], False, 'E2') for q, p in sel['E2'][X].items()]
        jobs += [(p, QM, False, 'E4') for p in sel['E4'][X]]
    jobs += [(p, QM, True, 'E3') for p in sel['E3']['A']]
    for p, ql, small, tag in jobs:
        rec = check_prime(p, ql, small)
        rec['set'] = tag
        if tag in ('E1', 'E3'):
            assert not admissible_q(p) and rec['api']['unconditional']['route'] != 'tal_split'
        out['cases'].append(rec)
        print(json.dumps(dict(set=tag, p=p, cls=rec['cls'], tal=len(rec['tal']), api=rec['api']['unconditional'],
                              s=round(rec['seconds'], 2))), flush=True)
    for p, q in ((3000013781, 89), (920889975821, 89)):
        rec = check_prime(p, [q], False)
        rec['set'] = 'REGRESSION (not confirmation)'
        out['regression'].append(rec)
        print(json.dumps(dict(set='REGRESSION', p=p, tal=rec['tal'])), flush=True)
    verify('r3/FREEZE_R3.json')
    verify('r3/FREEZE_R3_1.json')
    out['status'] = 'PASS'
    out['n_cases'] = len(out['cases'])
    out['n_tal_checks'] = sum(len(r['tal']) for r in out['cases'])
    (ROOT / 'r3/evidence/CONFIRMATION_R3_1.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
    print('PASS', out['n_cases'], 'primes', out['n_tal_checks'], 'tal checks')


if __name__ == '__main__':
    main()
