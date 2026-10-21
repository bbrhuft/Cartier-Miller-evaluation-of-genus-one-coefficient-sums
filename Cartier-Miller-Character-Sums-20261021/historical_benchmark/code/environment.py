"""Record the software/hardware environment (no timing)."""
import json, os, platform, subprocess, sys
def sh(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:
        return repr(e)
env = {
  'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
  'cpu_model': sh("grep -m1 'model name' /proc/cpuinfo | cut -d: -f2"), 'nproc': sh('nproc'),
  'cpu_flags_excerpt': sh("grep -m1 flags /proc/cpuinfo | tr ' ' '\\n' | grep -E '^(avx|avx2|avx512f|bmi2|adx)$' | tr '\\n' ' '"),
  'mem': sh('free -m | head -2'), 'kernel': sh('uname -a'), 'gcc': sh('gcc --version | head -1'),
  'native_build': 'gcc -O2 -fPIC -shared -o libcmnative.so cmnative.c (single-threaded, uint64 + __int128)',
  'pip_system': sh(sys.executable + ' -m pip list 2>/dev/null | grep -i -E "flint|cypari|numpy|cysignals|matplotlib"'),
  'pari_version': sh(sys.executable + " -c 'import cypari2;print(cypari2.Pari().version())'"),
  'flint_version': sh(sys.executable + " -c 'import flint;print(flint.__version__, flint.__FLINT_VERSION__)'"),
  'sage_venv_python': sh(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'venv_sage', 'bin', 'python') + ' --version'),
  'sage_venv_packages': sh(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'venv_sage', 'bin', 'pip') + ' list 2>/dev/null | grep -i passagemath'),
  'threading': 'all workers single-threaded; benchmark jobs run sequentially; OMP/BLAS not used',
  'host_caveat': 'uncontrolled 2-vCPU cloud VM; see REPORT section 12 for concurrent-activity windows',
}
print(json.dumps(env, indent=1))
