"""Runtime-source manifest and retained-source verification, not a signature."""
import hashlib
import json
from pathlib import Path

from boundary_framework import __version__


def runtime_files(root):
    root = Path(root)
    files = list(root.glob('*.py')) + list(root.glob('*.bat'))
    files += list((root / 'retained_cm').rglob('*.py'))
    files += [root / 'SOURCE_PROVENANCE.json']
    return sorted(p for p in files if p.is_file())


def build_manifest(root):
    root = Path(root)
    return {'schema': 1, 'version': __version__,
            'scope': 'All root Python/batch launchers, retained Python modules and SOURCE_PROVENANCE.json; generated results and prose excluded.',
            'files': {p.relative_to(root).as_posix():
                      {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
                      for p in runtime_files(root)}}


def verify_manifest(root):
    root = Path(root)
    errors, checked = [], 0
    path = root / 'RUNTIME_MANIFEST.json'
    try:
        raw = path.read_bytes()
        if len(raw) > 4 * 1024 * 1024:
            raise ValueError('manifest exceeds size limit')
        manifest = json.loads(raw)
        if (type(manifest.get('schema')) is not int or manifest['schema'] != 1 or
                manifest.get('version') != __version__ or not isinstance(manifest.get('files'), dict)):
            raise ValueError('invalid manifest schema/version')
        names = set(manifest['files'])
        actual = {p.relative_to(root).as_posix() for p in runtime_files(root)}
        for name in sorted(actual - names):
            errors.append(f'unexpected runtime file: {name}')
        for name, entry in manifest['files'].items():
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts or name not in actual:
                errors.append(f'missing or invalid runtime path: {name}')
                continue
            data = (root / relative).read_bytes()
            checked += 1
            if (not isinstance(entry, dict) or entry.get('bytes') != len(data) or
                    entry.get('sha256') != hashlib.sha256(data).hexdigest()):
                errors.append(f'runtime hash mismatch: {name}')
        digest = hashlib.sha256(raw).hexdigest()
    except (OSError, ValueError, TypeError, AttributeError, RecursionError) as exc:
        errors.append(f'manifest unreadable/invalid: {exc}'); digest = None
    return {'passed': not errors, 'files_checked': checked,
            'manifest_sha256': digest, 'errors': errors}


def verify_provenance(root):
    root = Path(root)
    errors, checked = [], 0
    try:
        provenance = json.loads((root / 'SOURCE_PROVENANCE.json').read_text())
        entries = [(e['delivered_path'], e['sha256']) for e in provenance['copied_files']]
        forest = provenance['many_prime_forest']
        entries.append((forest['copied_path'], forest['sha256']))
        for name, expected in entries:
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('invalid provenance path')
            checked += 1
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                errors.append(f'retained source mismatch: {name}')
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        errors.append(f'provenance verification failed: {exc}')
    return {'passed': not errors, 'files_checked': checked, 'errors': errors}


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    print(json.dumps({'runtime': verify_manifest(root), 'retained': verify_provenance(root)}, indent=2))
