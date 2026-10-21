"""Assemble the reproducibility archive: copies the package tree (excluding caches and temporary
job files), writes SHA256SUMS.txt over every file, and zips it.

python3 -I build_archive.py PACKAGE_DIR OUT_ZIP
"""
import hashlib, os, sys, zipfile

pkg, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
SKIP_DIRS = {'__pycache__', 'tmp'}
SKIP_SUFFIX = ('.aux', '.log', '.out', '.pyc')
files = []
for root, dirs, fs in os.walk(pkg):
    dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(root, f), pkg)
        latex_aux = rel.startswith('manuscript' + os.sep) and f.endswith(SKIP_SUFFIX)
        if latex_aux or f.endswith('.pyc') or f == 'SHA256SUMS.txt':
            continue
        files.append(os.path.relpath(os.path.join(root, f), pkg))
lines = []
for f in files:
    lines.append('%s  %s' % (hashlib.sha256(open(os.path.join(pkg, f), 'rb').read()).hexdigest(), f))
open(os.path.join(pkg, 'SHA256SUMS.txt'), 'w').write('\n'.join(lines) + '\n')
top = os.path.basename(pkg)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in files + ['SHA256SUMS.txt']:
        z.write(os.path.join(pkg, f), os.path.join(top, f))
print(len(files) + 1, 'files ->', out, os.path.getsize(out), 'bytes')
