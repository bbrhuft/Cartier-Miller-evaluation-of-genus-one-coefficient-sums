"""Round-3 interface, amendment R3.1: the signed a_L (and m!, c_p, D) from a certified prime p = 5 mod 6.

    python3 -m r3.acquire_r31 p [--mode unconditional|grh] [--q Q] [--route auto|tal|hi|nodal]

Identical to r3/acquire_r3.py (frozen) except that (i) the Jacobi sum is reconstructed with the
R3.1 lattice chain (r3/jacobi_r31.py), (ii) the policy constants come from POLICY_R3_1.json, and
(iii) if the lattice chain raises (it never returns an uncertified value) the call degrades to the
next admissible q and then to the fallback route, recording this in metadata['degraded'].

Status labels: 'unconditional' (tal_split with 5 <= q <= 89, half_interval with an unconditional
class number, nodal_flint); 'GRH-conditional' (half_interval with quadclassunit, mode 'grh');
'experimental' (tal_split with a user-forced q outside [5, 89]).
"""
import argparse
import json
import math
import sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from r3.common import params, ClassNumberPolicy, flint_rising, is_prime
from r3 import tal3
from r3.jacobi_r31 import JacobiContextR31
from r3.halfint import halfinterval_c3

POLICY_PATH = Path(__file__).resolve().parent / 'POLICY_R3_1.json'
_POLICY = []


def policy():
    if not _POLICY:
        _POLICY.append(json.loads(POLICY_PATH.read_text()))
    return _POLICY[0]


def svp_cost(q):
    return policy()['svp_table_s'][str(q)]


def interval_cost(L):
    m = policy()['interval_model']
    return 0.0 if L <= 0 else m['B'] * L ** m['gamma']


def tal_cost(p, q):
    R = tal3.residuals(p, q, tal3.default_anchor(p))
    return svp_cost(q) + interval_cost(R['len_m']) + interval_cost(R['len_a'])


def fallback(p, mode):
    D = p if p % 4 == 3 else 3 * p
    if mode == 'grh' or D < 2 * 10 ** 10:
        return 'half_interval', interval_cost((p + 1) // 6) + policy()['hi_classno_overhead_s']
    m = policy()['nodal_model']
    return 'nodal_flint', m['C'] * p ** m['delta']


def admissible_q(p):
    lo, hi = policy()['q_range']
    return [q for q in range(lo, hi + 1)
            if is_prime(q) and (p - 1) % q == 0 and (p - 1) // q >= policy()['K_min']]


def ranked(p, mode):
    """Admissible q cheaper than the fallback, best first; and the fallback."""
    fb = fallback(p, mode)
    cands = sorted(((tal_cost(p, q), -q, q) for q in admissible_q(p)))
    return [q for c, _, q in cands if c < fb[1]], fb, {q: c for c, _, q in cands}


def nodal_flint_c(p):
    P = params(p)
    N = P['N']
    inv3 = pow(3, p - 2, p)
    chi = 1 if pow(6, (p - 1) // 2, p) == 1 else p - 1
    (num, den), _ = flint_rising(p, N, [4 * inv3 % p, 1])
    return -4 * inv3 * chi * pow(-1, N, p) * num * pow(den, p - 2, p) % p


def tal_c(p, q, anchor=None):
    return tal3.acquire(p, q, anchor, ctx=JacobiContextR31(p, q))


def acquire_aL(p, mode='unconditional', q=None, route='auto'):
    import atkin
    t0 = perf_counter()
    params(p)
    if mode not in ('unconditional', 'grh'):
        raise ValueError(mode)
    meta, degraded = {}, []
    fb = fallback(p, mode)
    if route == 'auto' and q is None:
        order, fb, pred = ranked(p, mode)
        meta['policy_prediction_s'] = dict(tal={str(k): v for k, v in pred.items()}, fallback=list(fb))
        plan = [('tal_split', x) for x in order] + [(fb[0], None)]
    elif route in ('auto', 'tal', 'tal_split'):
        if q is None:
            qs = admissible_q(p)
            if not qs:
                raise ValueError('no admissible q in the frozen range divides p-1')
            q = min(qs, key=lambda x: (tal_cost(p, x), -x))
        plan = [('tal_split', q)]
    else:
        plan = [({'hi': 'half_interval', 'nodal': 'nodal_flint'}.get(route, route), None)]
    t_sel = perf_counter()
    c = None
    for rt, qq in plan:
        if rt == 'tal_split':
            try:
                c, m = tal_c(p, qq)
            except ArithmeticError as exc:
                degraded.append(dict(q=qq, error=str(exc)))
                continue
            lo, hi = policy()['q_range']
            status = 'unconditional' if lo <= qq <= hi else 'experimental'
            route, q = rt, qq
            meta.update(m)
            break
        if rt == 'half_interval':
            c, m = halfinterval_c3(p, ClassNumberPolicy('grh' if mode == 'grh' else 'unconditional'))
            status, route, q = m['status'], rt, None
            meta.update(m)
            break
        if rt == 'nodal_flint':
            c, status, route, q = nodal_flint_c(p), 'unconditional', rt, None
            break
        raise ValueError(rt)
    if c is None:
        raise ArithmeticError('all planned routes failed: %r' % degraded)
    aL = 3 * c * pow(4, p - 2, p) % p
    mf = tal3.mfact_from_c(p, c)
    D = atkin.derivative_from_c(p, c)
    t1 = perf_counter()
    meta['degraded'] = degraded
    return dict(p=p, a_L=aL, c_p=c, m_factorial=mf, D=D, route=route, q=q, status=status,
                mode=mode, seconds=dict(select=t_sel - t0, total=t1 - t0), metadata=meta)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('p', type=int)
    ap.add_argument('--mode', choices=['unconditional', 'grh'], default='unconditional')
    ap.add_argument('--q', type=int, default=None)
    ap.add_argument('--route', choices=['auto', 'tal', 'hi', 'nodal'], default='auto')
    a = ap.parse_args()
    if not is_prime(a.p) or a.p % 6 != 5 or a.p < 11:
        sys.exit('p must be a prime >= 11 with p = 5 mod 6')
    print(json.dumps(acquire_aL(a.p, a.mode, a.q, a.route), indent=2, default=str))
