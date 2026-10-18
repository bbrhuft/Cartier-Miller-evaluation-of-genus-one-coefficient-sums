"""Release-maintainer tool; evidence capture never regenerates this manifest."""
import json
from pathlib import Path
from release_integrity import build_manifest

if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    path = root / 'RUNTIME_MANIFEST.json'
    path.write_text(json.dumps(build_manifest(root), indent=2) + '\n', encoding='utf-8')
    print(path)
