"""Extension of the supplied verify_character_identities.py on the SAME 132 models + p=101 example.

The supplied script (supplied/verify_character_identities.py, unchanged) checks reference
identities only.  This extension regenerates exactly its models (same seed, same rejection
loop) and adds, per model:
  1. the inherited Miller evaluator RowSession.query at every lambda in F_p, against the
     truncation computed by FLINT (independent of the supplied script's own power routine);
  2. the candidate single-pole route at every mu (incl. mu = 0 and branch values);
  3. normalization changes: scaling by a nonsquare and translations, with PARI traces;
  4. several omitted poles incl. 0 and branch values, constants, affine/projective sums,
     against direct enumeration.
Usage (package root): python3 src/verify_character_identities_extended.py
"""
import importlib.util
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import reference as ref       # noqa: E402
import cmcs                   # noqa: E402
from cm_system.rows import RowSession                        # noqa: E402  (inherited)
from cm_system.api import Unsupported as InheritedUnsupported  # noqa: E402

spec = importlib.util.spec_from_file_location('supplied', os.path.join(ROOT, 'supplied', 'verify_character_identities.py'))
sup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sup)


def supplied_models():
    rng = random.Random(20261020)
    models = []
    for p in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        for degree in (3, 4):
            accepted = 0
            while accepted < 6:
                f = [1] + [rng.randrange(p) for _ in range(degree - 1)] + [rng.randrange(1, p)]
                if not sup.squarefree(f, p):
                    continue
                models.append((p, f))
                accepted += 1
    models.append((101, [1, 1, 0, 1]))
    return models


def main():
    rng = random.Random(7)
    stats = {'models': 0, 'inherited_queries': 0, 'inherited_exceptional': 0, 'inherited_split': 0,
             'inherited_cubic_branch': 0, 'inherited_quartic_branch_unsupported': 0,
             'candidate_single': 0, 'normalization_checks': 0, 'multi_checks': 0, 'failures': []}
    for p, f in supplied_models():
        stats['models'] += 1
        tau = ref.trace_pari(f, p)
        c = ref.power_coefficients(f, p)
        row = RowSession(p, f, trace=tau)
        for lam in range(p):
            mu = pow(lam, -1, p) if lam else None
            try:
                res = row.query(lam)
            except InheritedUnsupported:
                stats['inherited_quartic_branch_unsupported'] += 1
                if not (len(f) == 5 and ref.peval(f, mu, p) == 0):
                    stats['failures'].append(('unsupported', p, f, lam))
                continue
            truth = c[p - 1] if lam == 0 else ref.truncation_value(c, mu, p)
            stats['inherited_queries'] += 1
            if res['S'] != truth:
                stats['failures'].append(('inherited', p, f, lam))
            stats['inherited_exceptional'] += int(bool(res.get('exceptional')))
            stats['inherited_split'] += int(bool(res.get('split_fallback')))
            stats['inherited_cubic_branch'] += int(res.get('method') == 'cubic_branch_service')
        E = cmcs.Curve(p, f, trace=tau)
        E.prepare_second_kind()
        ds = ref.DirectSums(p, f)
        for mu in range(p):
            stats['candidate_single'] += 1
            if E.single_pole(mu) != ds.character_sum(simple=[(mu, 1)]):
                stats['failures'].append(('single', p, f, mu))
        # normalization changes
        nr = next(x for x in range(2, p) if ref.legendre(x, p) == -1)
        for a in (0, 1, p - 1):
            g = [0] * len(f)
            for i, ci in enumerate(f):
                for k in range(i + 1):
                    from math import comb
                    g[k] = (g[k] + ci * comb(i, k) * pow(a, i - k, p)) % p
            g = [x * nr % p for x in g]
            if g[-1] == 0:
                continue
            try:
                Eg = cmcs.Curve(p, g, trace=ref.trace_pari(g, p))
            except cmcs.InputError:
                continue
            Eg.prepare_second_kind()
            dg = ref.DirectSums(p, g)
            for mu in rng.sample(range(p), min(6, p)):
                stats['normalization_checks'] += 1
                if Eg.single_pole(mu) != dg.character_sum(simple=[(mu, 1)]):
                    stats['failures'].append(('normalization', p, g, mu))
        # several omitted poles, including 0 and branch values, constants
        roots = [x for x in range(p) if ref.peval(f, x, p) == 0]
        for t in range(6):
            U = set(rng.sample(range(p), min(4, p)))
            U.add(0)
            if roots:
                U.add(roots[0])
            simple = [(u, rng.randrange(1, p)) for u in sorted(U)]
            b = rng.randrange(p)
            for kind in ('character', 'affine_points', 'projective_points'):
                v, _ = E.weighted_sum(simple=simple, b=b, kind=kind)
                if kind == 'character':
                    w = ds.character_sum(simple=simple, b=b)
                else:
                    w = ds.affine_point_sum(simple=simple, b=b)
                    if kind == 'projective_points':
                        n_inf = 1 if len(f) == 4 else int(ref.square_counts(p)[f[4]])
                        w = (w + b * n_inf) % p
                stats['multi_checks'] += 1
                if v != w:
                    stats['failures'].append(('multi', kind, p, f, simple, b))
    stats['status'] = 'PASS' if not stats['failures'] else 'FAIL'
    out = os.path.join(ROOT, 'results', 'extended_verifier_output.json')
    with open(out, 'w') as fh:
        json.dump(stats, fh, indent=1)
    print(json.dumps({k: v for k, v in stats.items() if k != 'failures'}, indent=1),
          'failures:', len(stats['failures']))
    return 0 if not stats['failures'] else 1


if __name__ == '__main__':
    sys.exit(main())
