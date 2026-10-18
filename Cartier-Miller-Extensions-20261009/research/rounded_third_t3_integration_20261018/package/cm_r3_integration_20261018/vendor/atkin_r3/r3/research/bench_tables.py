"""Turn r3/evidence/BENCHMARK_R3_1.json into the report's markdown tables (medians in ms)."""
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
b = json.loads((ROOT / 'r3/evidence/BENCHMARK_R3_1.json').read_text())


def ms(x):
    return '%.0f' % (x * 1e3) if x >= 0.1 else '%.1f' % (x * 1e3)


out = []
rows = [r for r in b['rows'] if r['set'] == 'B1']
out.append('| p | cls | q | native | block m! | nodal | HI (GRH) | HI uncond. | T3 dup6 | T3 dup12 | T3 warm | API (route q) | API | native/T3 | HI-GRH/T3 | native/API |')
out.append('|---:|:-:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|')
sp_nat, sp_nod, sp_hi = [], [], []
for r in rows:
    m = r['medians_s']
    hiu = m.get('hi_uncond_qfb')
    hiu_s = ms(hiu) + ' (qfb)' if hiu else ms(m['hi_uncond_forms_1sample']) + ' (forms, 1)'
    tal = min(v for k, v in m.items() if k.startswith('tal'))
    d12 = ms(m['tal_dup12']) if 'tal_dup12' in m else '–'
    out.append('| %d | %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s %s | %s | %.2f | %.2f | %.2f |' % (
        r['p'], r['cls'], r['q'], ms(m['native']), ms(m['block_factorial']), ms(m['nodal_flint']), ms(m['hi_grh']),
        hiu_s, ms(m['tal_dup6']), d12, ms(statistics.median(r['tal_warm_default_anchor_s'])),
        r['api_route'].replace('tal_split', 'T3').replace('half_interval', 'HI').replace('nodal_flint', 'nodal'),
        r['api_q'] if r['api_q'] else '', ms(m['api_unconditional']),
        m['native'] / tal, m['hi_grh'] / tal, m['native'] / m['api_unconditional']))
    sp_nat.append(m['native'] / tal); sp_nod.append(m['nodal_flint'] / tal); sp_hi.append(m['hi_grh'] / tal)
out.append('')
api_r = [r['medians_s']['native'] / r['medians_s']['api_unconditional'] for r in b['rows'] if r['set'] == 'B1']
out.append('B1 summary: native/T3 %.2f–%.2f (median %.2f); nodal/T3 %.2f–%.2f; HI-GRH/T3 %.2f–%.2f; native/API %.2f–%.2f (median %.2f).' % (
    min(sp_nat), max(sp_nat), statistics.median(sp_nat), min(sp_nod), max(sp_nod), min(sp_hi), max(sp_hi),
    min(api_r), max(api_r), statistics.median(api_r)))
out.append('')
rows = [r for r in b['rows'] if r['set'] == 'B2']
out.append('| p | cls | generic | admissible q | API route (q) | native | nodal | HI (GRH) | API | native/API | nodal/API |')
out.append('|---:|:-:|:-:|---|---|---:|---:|---:|---:|---:|---:|')
gen_nat, gen_nod, tal_cnt = [], [], 0
for r in rows:
    m = r['medians_s']
    out.append('| %d | %s | %s | %s | %s %s | %s | %s | %s | %s | %.2f | %.2f |' % (
        r['p'], r['cls'], 'yes' if r['generic'] else 'E1', ','.join(map(str, r['admissible'])) or '–',
        r['api_route'].replace('tal_split', 'T3').replace('half_interval', 'HI').replace('nodal_flint', 'nodal'),
        r['q'] or '', ms(m['native']), ms(m['nodal_flint']), ms(m['hi_grh']), ms(m['api_unconditional']),
        m['native'] / m['api_unconditional'], m['nodal_flint'] / m['api_unconditional']))
    if r['generic']:
        gen_nat.append(m['native'] / m['api_unconditional']); gen_nod.append(m['nodal_flint'] / m['api_unconditional'])
        tal_cnt += r['api_route'] == 'tal_split'
out.append('')
out.append('B2 generic summary (30 primes): T3 chosen for %d; native/API median %.2f (range %.2f–%.2f); nodal/API median %.2f (range %.2f–%.2f).' % (
    tal_cnt, statistics.median(gen_nat), min(gen_nat), max(gen_nat), statistics.median(gen_nod), min(gen_nod), max(gen_nod)))
out.append('')
rows = [r for r in b['rows'] if r['set'] == 'B3']
out.append('| p | cls | native | nodal | HI uncond. (qfb) | HI (GRH) | HI forms (cold) | API (route q) | API | native/HI-qfb | nodal/HI-qfb |')
out.append('|---:|:-:|---:|---:|---:|---:|---:|---|---:|---:|---:|')
for r in rows:
    m = r['medians_s']
    out.append('| %d | %s | %s | %s | %s | %s | %s | %s %s | %s | %.2f | %.2f |' % (
        r['p'], r['cls'], ms(m['native']), ms(m['nodal_flint']), ms(m['hi_uncond_qfb']), ms(m['hi_grh']),
        ms(m['hi_forms_cold']), r['api_route'].replace('tal_split', 'T3').replace('half_interval', 'HI'), r['q'] or '',
        ms(m['api_unconditional']), m['native'] / m['hi_uncond_qfb'], m['nodal_flint'] / m['hi_uncond_qfb']))
out.append('')
rows = [r for r in b['rows'] if r['set'] == 'B4']
out.append('| p | cls | API route (q) | native | nodal | API | native/API |')
out.append('|---:|:-:|---|---:|---:|---:|---:|')
for r in rows:
    m = r['medians_s']
    out.append('| %d | %s | %s %s | %s | %s | %s | %.2f |' % (
        r['p'], r['cls'], r['api_route'].replace('tal_split', 'T3').replace('half_interval', 'HI').replace('nodal_flint', 'nodal'),
        r['q'] or '', ms(m['native']), ms(m['nodal_flint']), ms(m['api_unconditional']), m['native'] / m['api_unconditional']))
Path(sys.argv[1]).write_text('\n'.join(out) + '\n')
print('\n'.join(out))
