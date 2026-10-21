import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent
files={n:hashlib.sha256((root/n).read_bytes()).hexdigest()
       for n in ('cm_character_route.py','verify_repair.py','freeze.py')}
digest=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
(root/'FREEZE.json').write_text(json.dumps({'files':files,'digest':digest},indent=2)+'\n')
print(digest)
