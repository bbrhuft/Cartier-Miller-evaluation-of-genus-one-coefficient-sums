"""Post-confirmation tally (analysis only; no result changes): which R3.1 lattice stage each
confirmation (p, q) pair needed.  Usage: python3 r3/research/lll_stage_tally.py OUT.json"""
import json, sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from r3.jacobi_r31 import JacobiContextR31
c = json.loads((ROOT / 'r3/evidence/CONFIRMATION_R3_1.json').read_text())
pairs = sorted({(r['p'], int(k.split('/')[0])) for r in c['cases'] for k in r['tal']})
rows, tally = [], collections.Counter()
for p, q in pairs:
    ctx = JacobiContextR31(p, q); ctx.J(1, 1)
    rows.append(dict(p=p, q=q, stage=ctx.stats['lll_stage'], attempts=ctx.stats['lll_attempts']))
    tally[(q >= 83, ctx.stats['lll_stage'])] += 1
out = dict(role='post-confirmation analysis of R3.1 lattice stages', pairs=len(pairs),
           tally={'%s/%s' % ('q>=83' if a else 'q<83', s): n for (a, s), n in tally.items()}, rows=rows)
(Path(sys.argv[1])).write_text(json.dumps(out, indent=1) + '\n')
print(out['pairs'], out['tally'])
