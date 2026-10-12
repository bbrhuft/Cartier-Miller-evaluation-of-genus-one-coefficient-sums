#!/usr/bin/env python3
"""Extract the retained input and rerun the review without network access."""
from pathlib import Path
import subprocess, sys, zipfile

root=Path(__file__).resolve().parent
dest=root/'inherited'
with zipfile.ZipFile(root/'inputs/Depth_Three_Recognition_Handover_20261012.zip') as z:
    for name in z.namelist():
        if not (dest/name).resolve().is_relative_to(dest.resolve()):
            raise ValueError('unsafe archive path')
    z.extractall(dest)
for relative in ['verify_handover.py',
                 'research/depth_three_recognition_20261007/theory/b0/derive_b0_family.py',
                 'research/depth_three_recognition_20261007/core/validate_depth_three_b0.py']:
    subprocess.run([sys.executable,str(dest/relative)],cwd=dest,check=True)
subprocess.run([sys.executable,str(root/'independent_audit.py')],cwd=root,check=True)
