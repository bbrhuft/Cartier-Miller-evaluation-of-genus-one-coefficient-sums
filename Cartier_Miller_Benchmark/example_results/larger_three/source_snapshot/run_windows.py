# SPDX-License-Identifier: GPL-2.0-or-later
"""Build a native Windows executable with MSYS2 UCRT64, then open the benchmark GUI (or run headless)."""
import argparse
import datetime
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__,add_help=False)
    ap.add_argument('--skip-build',action='store_true')
    args,remaining=ap.parse_known_args()
    if '--help' in remaining:
        print('Windows launcher option: --skip-build. Benchmark options:')
        return subprocess.call([sys.executable,str(ROOT/'app.py'),'--help'])
    if os.name!='nt':
        print('Use this launcher on Windows; on Linux/WSL use bash build.sh and python3 app.py.',file=sys.stderr)
        return 2
    prefix=Path(sys.executable).resolve().parent.parent
    compiler=prefix/'bin/g++.exe'
    if not compiler.is_file() or not (prefix/'include/NTL/ZZ.h').is_file():
        print('Please run with MSYS2 UCRT64 Python and install the GCC/NTL packages in README.md.',file=sys.stderr)
        return 2
    os.environ['PATH']=str(prefix/'bin')+os.pathsep+os.environ.get('PATH','')
    os.environ['OMP_NUM_THREADS']='1'
    os.environ['NTL_NUM_THREADS']='1'
    exe=ROOT/'bin/harvey_adapter.exe'
    exe.parent.mkdir(exist_ok=True)
    if not args.skip_build:
        cmd=[str(compiler),'-O3','-std=c++17','-pthread','-I'+str(prefix/'include'),'-L'+str(prefix/'lib'),
            str(ROOT/'harvey_adapter.cpp'),str(ROOT/'upstream/recurrences_ntl.cpp'),
            str(ROOT/'upstream/hypellfrob.cpp'),'-lntl','-lgmp','-o',str(exe)]
        print('Building native Windows Harvey adapter...',flush=True)
        subprocess.run(cmd,cwd=ROOT,check=True)
        build={'compiler_command':cmd,'compiler_version':subprocess.check_output([str(compiler),'--version'],text=True),
               'utc_built':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        import json
        (ROOT/'bin/build_metadata.json').write_text(json.dumps(build,indent=2),encoding='utf-8')
    if not exe.is_file():
        raise FileNotFoundError('No adapter executable exists. Run without --skip-build first.')
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    output=ROOT/'results'/stamp
    return subprocess.call([sys.executable,str(ROOT/'app.py'),'--executable',str(exe),
        '--output',str(output),*remaining],cwd=ROOT)

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (OSError,subprocess.CalledProcessError) as e:
        print('Benchmark failed: '+str(e),file=sys.stderr)
        raise SystemExit(1)
