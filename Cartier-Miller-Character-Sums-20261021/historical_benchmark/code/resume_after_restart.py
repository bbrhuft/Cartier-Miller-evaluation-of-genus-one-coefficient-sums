"""Resume the W5 workload after the host restart of 21 Oct 2026 ~02:13 (VM reboot killed the run).

Runs only the (group, method) jobs absent from timing_samples.csv, with the unchanged as-run harness
bench.py (sha256 eb46a6e0...d0b40d2) and the same seeds, budgets and rules; appends to the same CSV.
Then regenerates the deterministic case pools (never written because the run did not reach its end)
into cases_regenerated.json and writes a reconstructed run-metadata file.
python3 -I resume_after_restart.py RESULTS_BENCH_DIR
"""
import csv, hashlib, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bench as B

out = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else 'resume+cases'
csv_path = os.path.join(out, 'timing_samples.csv')
done = {}
for r in csv.DictReader(open(csv_path)):
    done.setdefault((r['workload'], r['group']), set()).add(r['method'])
W5M = ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'flint_power+multipoint', 'polyrec_c+multipoint', 'enum_conv', 'enum_c', 'bgs_harvey']
logf = open(os.path.join(out, 'bench_resume.log'), 'a')


def log(msg):
    line = time.strftime('%H:%M:%S ') + msg
    print(line, flush=True)
    logf.write(line + '\n'); logf.flush()


pools = {}
if 'resume' in mode:
    fh = open(csv_path, 'a', newline='')
    w = csv.writer(fh)
    log('=== resume W5 after host restart')
    for spec in B.w5_specs(False):
        miss = [m for m in W5M if m not in done.get(('W5', spec['gid']), set())]
        if miss:
            log('group %s: running %s' % (spec['gid'], miss))
            B.run_prepared('W5', [spec], miss, w, out, log, pools)
            fh.flush()
    fh.close()
if 'cases' in mode:
    cases = {}
    for (W, gid, bits, d) in B.w1_groups(False):
        for wl in ('W1', 'TRACE'):
            r = B.rng('%s|%s' % (wl, gid))
            pr = B.rng('%s|%s|pilot' % (wl, gid))
            pool = [B.make_instance(r, bits, d, i) for i in range(9 * B.MAX_REPS)]
            ppool = [B.make_instance(pr, bits, d, i) for i in range(3)]
            cases[wl + ':' + gid] = {'pool': pool, 'pilot': ppool, 'bits': bits, 'd': d}
    for wl, fn in (('W2', B.w2_specs), ('W3', B.w3_specs), ('W4', B.w4_specs), ('W5', B.w5_specs), ('W6', B.w6_specs)):
        for spec in fn(False):
            cases[wl + ':' + spec['gid']] = spec
    json.dump(cases, open(os.path.join(out, 'cases_regenerated.json'), 'w'))
    meta = {'bench_seed': B.BENCH_SEED, 'freeze_digest': B.FREEZE['digest'],
            'bench_py_sha256': hashlib.sha256(open(os.path.join(HERE, 'bench.py'), 'rb').read()).hexdigest(),
            'worker_sha256': hashlib.sha256(open(os.path.join(HERE, 'bench_worker.py'), 'rb').read()).hexdigest(),
            'started_local': '2026-10-20 23:55:46 (from bench.log)', 'interrupted_local': '2026-10-21 ~02:13 (host restart; uptime reset)',
            'resumed': 'W5 missing jobs only, same harness and seeds (bench_resume.log)',
            'pools_note': 'pools regenerated deterministically by this script (cases_regenerated.json); '
                          'validity is checked by validate_outputs.py against direct enumeration and consensus',
            'soft_budget_s': B.SOFT_BUDGET_S, 'extended_budget_s': B.EXTENDED_BUDGET_S, 'extended_methods': sorted(B.EXTENDED),
            'mem_ceiling_kib': B.MEM_CEILING_KIB, 'as_limit_bytes': B.AS_LIMIT, 'block_target_s': B.BLOCK_TARGET_S,
            'max_reps': B.MAX_REPS, 'job_cap_s': B.JOB_CAP_S, 'max_bits': B.MAX_BITS,
            'concurrent_activity': 'low-priority (nice 19) validation scripts ran on the second core between about '
                                   '00:14 and 00:20 local (W1 40-62 bit classes, early W7) and analysis scripts briefly around 01:33'}
    json.dump(meta, open(os.path.join(out, 'bench_meta.json'), 'w'), indent=1)
    log('cases regenerated: %d groups' % len(cases))
