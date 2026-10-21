"""Write FREEZE.json for the benchmark/validation implementations (refuses to overwrite).
digest = sha256 over sorted lines '<sha256>  <path>\\n' (same rule as the inherited freeze)."""
import hashlib, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ['cmbench/__init__.py', 'cmbench/core.py', 'cmbench/methods.py', 'cmbench/bgs07.py', 'cmbench/harvey.py',
         'cmbench/cases.py', 'cmbench/cmcs_v2.py', 'cmbench/validate.py', 'cmbench/native/cmnative.c',
         'cmbench/native/libcmnative.so', 'run_validate.py', 'run_validate_harvey.py', 'make_harvey_refs.py',
         'source_audit/voloch_semaev_normalization.py', 'freeze.py']
out = os.path.join(HERE, 'FREEZE.json')
if os.path.exists(out):
    sys.exit('FREEZE.json exists; refusing to overwrite')
files = {f: hashlib.sha256(open(os.path.join(HERE, f), 'rb').read()).hexdigest() for f in FILES}
lines = ''.join('%s  %s\n' % (files[k], k) for k in sorted(files))
rec = {'frozen_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'files': files,
       'digest': hashlib.sha256(lines.encode()).hexdigest(),
       'digest_rule': 'sha256 over sorted lines "<sha256>  <path>\\n"',
       'inherited_freeze_digest': '4302b56426a6160fbc5027659632bac7ad6cc0ab755c5fcb00d8c9502aa99bd3',
       'inherited_candidate_sha256': '763c86811e5b43bb0c00791f83083420c27232a04d131633c6a6c3552bb3e59c',
       'handover_reference_comparators_sha256': '212f37cf8b37456c1f2933dd3c2fcfc497f13cf2417c874eda4645ac419576d8',
       'build': 'gcc 13.3.0: gcc -O2 -fPIC -shared -o libcmnative.so cmnative.c',
       'timestamp_note': 'local clock only; no external timestamp',
       'confirmation_seed_rule': 'seed = digest; benchmark seed = sha256(digest + "|benchmark")'}
json.dump(rec, open(out, 'w'), indent=1)
print(rec['digest'])
