"""Coverage labels for the pilot rows: outside-table, trace +-1, A=0/B=0.

'Outside retained tables' uses the handover's labelling rule (A B != 0 and
H_D(j) != 0 for every supplied fixed-D table).  It is only a label: every
ordinary curve over F_p has CM by some order; nothing here says 'non-CM'.
"""
from pathlib import Path
import csv
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import okp_config  # noqa: E402

_args, _deps = okp_config.parse('coverage labels', needed=('handover',))
if 'handover' not in _deps['paths']:
    print('DEPENDENCY_MISSING: coverage labels need the handover tables')
    sys.exit(okp_config.EXIT_DEPENDENCY)
tables = json.loads((Path(_deps['paths']['handover']) / 'knowledge' / 'retained_CM_tables.json').read_text())


def outside(p, A, B, j):
    if A % p == 0 or B % p == 0:
        return False
    for v in tables.values():
        val = 0
        for c in reversed(v['H_D_low_to_high']):
            val = (val * j + int(c)) % p
        if val == 0:
            return False
    return True


def summarize(name, kappa_col):
    rows = list(csv.DictReader((HERE / 'results' / name).open()))
    rows = [r for r in rows if r.get(kappa_col) not in ('', None)]
    return {'rows_with_slope': len(rows),
            'outside_retained_tables': sum(outside(int(r['p']), int(r['A']), int(r['B']), int(r['j'])) for r in rows),
            'trace_plus_one': sum(int(r['trace']) == 1 for r in rows),
            'trace_minus_one': sum(int(r['trace']) == -1 for r in rows),
            'A_zero': sum(int(r['A']) == 0 for r in rows), 'B_zero': sum(int(r['B']) == 0 for r in rows)}


out = {'charp_identities.csv': summarize('charp_identities.csv', 'kappa'),
       'padic_lift_slopes.csv': summarize('padic_lift_slopes.csv', 'kappa_target'),
       'note': 'outside-table is a label from the supplied tables, not a non-CM claim'}
(HERE / 'results' / 'coverage.json').write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=1))
print('COVERAGE_DONE')
sys.exit(0)
