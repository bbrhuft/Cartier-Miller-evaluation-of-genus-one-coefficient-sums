"""Check package integrity and imported-source provenance; no mathematics claim."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent


def main():
    items=json.loads((ROOT/'SHA256SUMS.json').read_text())
    failed=[]
    for name,digest in items.items():
        p=ROOT/name
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:failed.append(name)
    if failed:
        print(json.dumps({'status':'failed','changed_or_missing':failed},indent=2));return 1
    prov=json.loads((ROOT/'PROVENANCE.json').read_text())
    for x in prov:
        if x.get('redistributed') is False:continue  # identified by hash only; see RELEASE_NOTE.md
        p=ROOT/x['destination']
        if hashlib.sha256(p.read_bytes()).hexdigest()!=x['delivered_sha256']:
            raise AssertionError('copied source changed: '+x['destination'])
    print(json.dumps({'status':'passed','hashed_files':len(items),'provenance_entries':len(prov),
                      'scope':'integrity only; validate.py checks mathematics'},indent=2));return 0


if __name__=='__main__':sys.exit(main())
