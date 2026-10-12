"""Confirm that the retained fixed-D evaluator and the completed D = -256 recognizer
are the intended imports, record their actual paths and hashes, and execute them.

Checks (exit 1 on any failure, 2 on a missing dependency):
  * file hashes equal the entries of the retained manifests (extension SHA256SUMS.json,
    inherited research SHA256SUMS.json);
  * the extension's cm_tables.json H_D data equal the handover's retained_CM_tables.json;
  * the imported combined recognizer exposes the completed B = 0 depth-three family;
  * the D = -256 control (p, A, B) = (73, 16, 27) is recognized with beta/H = 44, equal to
    the coefficient target;
  * exhaustively at p = 73, 89, 97, 113: every fixed-D slope and every recognizer
    multiplier equals the coefficient target, and fixed-D D = -256 (resp. -192) hits
    coincide exactly with recognizer matches of the B = 0 (resp. A = 0) depth-three family.
A recognizer lacking the B = 0 family would fail the last check at p = 73, 89, 113.
"""
from pathlib import Path
import importlib.util
import json
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from okp_common import CheckFailure, require, nonsingular, H_beta_recurrence, sha256_file, environment  # noqa: E402
import okp_config  # noqa: E402


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(deps):
    t0 = time.time()
    P = {k: Path(v) for k, v in deps['paths'].items()}
    rec = {'paths': deps['paths'], 'files': {}, 'manifest_agreement': {}, 'counts': {}}
    ext_manifest = json.loads((P['extension'] / 'SHA256SUMS.json').read_text())
    for rel in ('core/fixed_D_evaluator.py', 'results/cm_tables.json'):
        h = sha256_file(P['extension'] / rel)
        rec['files']['extension/' + rel] = {'path': str(P['extension'] / rel), 'sha256': h}
        require(ext_manifest.get(rel) == h, f'extension manifest disagrees for {rel}')
        rec['manifest_agreement']['extension/' + rel] = True
    inherited_manifest = json.loads((P['retained'].parent / 'SHA256SUMS.json').read_text())
    for rel in okp_config.EXPECTED['retained']:
        h = sha256_file(P['retained'] / rel)
        rec['files']['retained/' + rel] = {'path': str(P['retained'] / rel), 'sha256': h}
        require(inherited_manifest.get('research/' + rel) == h, f'inherited manifest disagrees for {rel}')
        rec['manifest_agreement']['retained/' + rel] = True
    patched = P['retained'].parent.parent / 'review' / 'patched' / 'depth_three_b0_recognize.py'
    if patched.is_file():
        rec['files']['review_patched_depth_three_b0_recognize.py'] = {
            'path': str(patched), 'sha256': sha256_file(patched),
            'note': 'review copy, recorded only; the imported module is the research-tree file named in D256_DEPENDENCY.md'}
    # table identity between the extension and the handover knowledge copy
    ext_tab = json.loads((P['extension'] / 'results' / 'cm_tables.json').read_text())
    hand_tab = json.loads((P['handover'] / 'knowledge' / 'retained_CM_tables.json').read_text())
    ext_H = {int(v['D']): [int(c) for c in v['H_D_low_to_high']] for v in ext_tab.values()}
    hand_H = {}
    for k, v in hand_tab.items():
        D = int(v['D']) if 'D' in v else None
        if D is not None:
            hand_H[D] = [int(c) for c in v['H_D_low_to_high']]
    if hand_H:
        require(all(ext_H.get(D) == H for D, H in hand_H.items()), 'handover tables differ from extension tables')
        rec['manifest_agreement']['handover_tables_equal_extension_tables'] = sorted(hand_H)
    else:
        hand_polys = sorted(json.dumps([int(c) for c in v['H_D_low_to_high']]) for v in hand_tab.values())
        ext_polys = sorted(json.dumps(H) for H in ext_H.values())
        require(hand_polys == ext_polys, 'handover H_D polynomials differ from extension tables')
        rec['manifest_agreement']['handover_tables_equal_extension_tables'] = 'H_D polynomial multisets equal'
    rec['manifest_agreement']['full_table_json_equal'] = (ext_tab == hand_tab)
    fixedD = load('retained_fixed_D_evaluator', P['extension'] / 'core' / 'fixed_D_evaluator.py')
    core_dir = P['retained'] / 'depth_three_recognition_20261007' / 'core'
    # The combined recognizer imports its B = 0 sibling by bare name; put the COMPLETED tree first
    # on sys.path and verify below that the module actually loaded is that file.
    sys.path.insert(0, str(core_dir))
    for stale in ('depth_three_b0_recognize', 'recognize', 'isogeny_closure', 'branch_evaluator'):
        sys.modules.pop(stale, None)
    combined = load('retained_depth_three_recognize', core_dir / 'depth_three_recognize.py')
    require(hasattr(combined, 'recognize_short_through_depth_three'), 'combined recognizer entry point missing')
    b0 = sys.modules.get('depth_three_b0_recognize')
    r = combined.recognize_short_through_depth_three(16, 27, 73)
    b0 = sys.modules.get('depth_three_b0_recognize')
    require(b0 is not None and hasattr(b0, 'recognize_depth_three_b0'), 'completed B=0 recognizer not imported')
    require(Path(b0.__file__).resolve() == (core_dir / 'depth_three_b0_recognize.py').resolve(),
            f'B=0 recognizer imported from an unexpected path: {b0.__file__}')
    for name, rel in (('recognize', 'depth_two_recognition_20261006/core/recognize.py'),
                      ('isogeny_closure', 'isogeny_closure_20261006/core/isogeny_closure.py'),
                      ('branch_evaluator', 'branch_point_20261006/branch_evaluator.py')):
        m = sys.modules.get(name)
        require(m is not None and Path(m.__file__).resolve() == (P['retained'] / rel).resolve(),
                f'{name} imported from an unexpected path: {getattr(m, "__file__", None)}')
    rec['imported_modules'] = {name: {'__file__': m.__file__, 'sha256': sha256_file(m.__file__)}
                               for name, m in (('fixed_D_evaluator', fixedD), ('depth_three_recognize', combined),
                                               ('depth_three_b0_recognize', b0),
                                               ('recognize', sys.modules.get('recognize')),
                                               ('isogeny_closure', sys.modules.get('isogeny_closure')),
                                               ('branch_evaluator', sys.modules.get('branch_evaluator'))) if m}
    H, beta = H_beta_recurrence(16, 27, 73)
    kap = beta * pow(H, -1, 73) % 73
    require(r['status'] == 'recognized' and r['matches'][0]['family'] == 'depth3_1728_disc_-256'
            and r['matches'][0]['beta_multiplier'] == 44 == kap, 'D=-256 control (73;16,27) failed')
    require((H, beta) == (67, 28), 'D=-256 control coefficients differ from the handover note')
    rec['D256_control'] = {'p': 73, 'A': 16, 'B': 27, 'H': H, 'beta': beta, 'kappa': kap,
                           'family': r['matches'][0]['family'], 'beta_multiplier': r['matches'][0]['beta_multiplier']}
    table = fixedD.load_table()
    fam = {-256: 'depth3_1728_disc_-256', -192: 'depth3_0_disc_-192'}
    for p in (73, 89, 97, 113):
        c = {'models': 0, 'ordinary': 0, 'fixedD_hits': 0, 'recognizer_matches': 0, 'D-256_hits': 0, 'D-192_hits': 0}
        for A in range(p):
            for B in range(p):
                if not nonsingular(A, B, p):
                    continue
                c['models'] += 1
                H, beta = H_beta_recurrence(A, B, p)
                hits = fixedD.slope_from_cm_table(A, B, p, table)
                res = combined.recognize_short_through_depth_three(A, B, p)
                fams = [m.get('family') for m in res['matches']]
                for D, slope in hits:
                    if D == 'seed':
                        continue
                    require(H != 0 and slope == beta * pow(H, -1, p) % p, f'fixed-D slope wrong at {(p, A, B, D)}')
                    c['fixedD_hits'] += 1
                for m in res['matches']:
                    require(H != 0 and m['beta_multiplier'] == beta * pow(H, -1, p) % p,
                            f'recognizer multiplier wrong at {(p, A, B)}')
                    c['recognizer_matches'] += 1
                for D, name in fam.items():
                    in_table = any(D == d for d, _ in hits)
                    in_rec = name in fams
                    require(in_table == in_rec, f'D={D} table/recognizer disagreement at {(p, A, B)}')
                    if in_table:
                        c[f'D{D}_hits'] += 1
                c['ordinary'] += H != 0
        rec['counts'][p] = c
    require(sum(c['D-256_hits'] for c in rec['counts'].values()) > 0, 'no D=-256 members exercised')
    require(sum(c['D-192_hits'] for c in rec['counts'].values()) > 0, 'no D=-192 members exercised')
    rec.update({'status': 'PASS', 'environment': environment(), 'seconds': round(time.time() - t0, 1),
                'source_sha256': sha256_file(__file__)})
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results' / 'retained_dependency_check.json').write_text(json.dumps(rec, indent=2, default=str))
    print(json.dumps({'counts': rec['counts'], 'D256_control': rec['D256_control']}, indent=1))
    print('RETAINED_DEPENDENCY_PASS')


if __name__ == '__main__':
    _args, _deps = okp_config.parse('retained dependency confirmation')
    if _deps['missing']:
        print('DEPENDENCY_MISSING:', _deps['missing'])
        sys.exit(okp_config.EXIT_DEPENDENCY)
    try:
        main(_deps)
    except CheckFailure as exc:
        print('FAIL:', exc)
        sys.exit(1)
