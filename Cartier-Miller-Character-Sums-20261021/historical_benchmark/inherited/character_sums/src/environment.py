"""Environment and provenance capture."""
import hashlib
import json
import os
import platform
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANDIDATE_FILES = [
    'src/cmcs.py',
    'src/reference.py',
    'src/harness.py',
    'src/environment.py',
    'src/develop.py',
    'src/confirm.py',
    'src/verify_character_identities_extended.py',
    'supplied/verify_character_identities.py',
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def vendor_files():
    out = []
    base = os.path.join(ROOT, 'vendor', 'cm_system')
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d != '__pycache__')
        for name in sorted(filenames):
            if name.endswith('.py'):
                out.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return out


def file_hashes(paths):
    return {p: sha256(os.path.join(ROOT, p)) for p in paths if os.path.exists(os.path.join(ROOT, p))}


def environment():
    import numpy
    info = {
        'python': sys.version.split()[0],
        'implementation': platform.python_implementation(),
        'platform': platform.platform(),
        'machine': platform.machine(),
        'numpy': numpy.__version__,
    }
    try:
        import flint
        info['python_flint'] = flint.__version__
    except Exception as exc:              # pragma: no cover
        info['python_flint'] = 'unavailable: %s' % exc
    try:
        import cypari2
        P = cypari2.Pari()
        info['cypari2'] = cypari2.__version__ if hasattr(cypari2, '__version__') else 'present'
        info['pari'] = '.'.join(str(x) for x in P.version()[:3])
    except Exception as exc:              # pragma: no cover
        info['pari'] = 'unavailable: %s' % exc
    try:
        with open('/proc/cpuinfo') as fh:
            for line in fh:
                if line.startswith('model name'):
                    info['cpu'] = line.split(':', 1)[1].strip()
                    break
    except OSError:
        pass
    info['cpu_count'] = os.cpu_count()
    return info


def provenance():
    with open(os.path.join(ROOT, 'PROVENANCE_INPUTS.json')) as fh:
        return json.load(fh)
