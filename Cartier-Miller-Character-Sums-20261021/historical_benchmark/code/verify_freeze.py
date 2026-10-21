import hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
rec = json.load(open(os.path.join(HERE, 'FREEZE.json')))
bad = [f for f, d in rec['files'].items() if hashlib.sha256(open(os.path.join(HERE, f), 'rb').read()).hexdigest() != d]
lines = ''.join('%s  %s\n' % (rec['files'][k], k) for k in sorted(rec['files']))
ok = not bad and hashlib.sha256(lines.encode()).hexdigest() == rec['digest']
print('FREEZE', 'OK' if ok else 'MISMATCH', rec['digest'], bad)
sys.exit(0 if ok else 1)
