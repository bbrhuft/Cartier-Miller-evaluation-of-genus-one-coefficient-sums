"""R3.1 ledger: LEDGER_R3.json plus every prime selected by the frozen R3 confirmation rule (run 1
selected them all, completed 88 cases, then failed) and every post-freeze development prime."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]

def collect(obj, out):
    if isinstance(obj, dict):
        for v in obj.values(): collect(v, out)
    elif isinstance(obj, list):
        for v in obj: collect(v, out)
    elif isinstance(obj, int) and obj > 10 ** 5:
        out.add(obj)

def main():
    L = json.loads((ROOT / 'r3/evidence/LEDGER_R3.json').read_text())
    sel = json.loads((ROOT / 'r3/evidence/CONFIRMATION_R3_RUN1_SUMMARY.json').read_text())['selection']
    r3sel = set(); collect(sel, r3sel)
    post = set()
    for r in json.loads((ROOT / 'r3/evidence/DEV_LLL_DELTA.json').read_text())['rows']:
        post |= set(r['primes'])
    for r in json.loads((ROOT / 'r3/evidence/DEV_SVP_TABLE_R31.json').read_text())['rows']:
        post.add(r['p'])
    L['explicit_r3_confirmation_run1_selection'] = sorted(r3sel)
    L['explicit_r3_postfreeze_dev'] = sorted(post)
    L['role'] = 'R3.1 ledger: R3 ledger + R3 run-1 selection + post-freeze development'
    (ROOT / 'r3/evidence/LEDGER_R3_1.json').write_text(json.dumps(L, indent=1) + '\n')
    print(len(r3sel), 'R3-selected;', len(post), 'post-freeze dev')

def excluded(p, _c=[]):
    if not _c:
        L = json.loads((ROOT / 'r3/evidence/LEDGER_R3_1.json').read_text())
        s = set()
        for k in ('explicit_round1_round2', 'explicit_round3_dev', 'explicit_r3_confirmation_run1_selection',
                  'explicit_r3_postfreeze_dev'):
            s |= set(L[k])
        _c.append(s)
    if p < 200000 or (p % 12 == 5 and p < 1000000):
        return True
    return p in _c[0]

if __name__ == '__main__':
    main()
