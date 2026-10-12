"""Shared harness for the repaired independent-check drivers.

Every driver records each mathematical comparison through Run.check().  Exit status:
    0  at least one check executed and none failed
    1  at least one mathematical disagreement (or an invariant violation, CheckFailure)
    2  a required dependency is missing (e.g. the target CSV), never silently skipped
    4  no check executed (vacuous run), treated as a failure
Informational items (explicitly outside a claim, e.g. p = 5) are recorded separately
and never counted as passes.  Results go to <out>/<driver>.json; nothing is appended
to files in the current directory.
"""
from pathlib import Path
import argparse
import json
import os
import platform
import sys
import time

EXIT_FAIL, EXIT_DEPENDENCY, EXIT_VACUOUS = 1, 2, 4


class CheckFailure(AssertionError):
    pass


def require(cond, msg='invariant failed'):
    if not cond:
        raise CheckFailure(msg if isinstance(msg, str) else repr(msg))


def base_parser(description, needs_targets=False):
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument('--out', default=str(Path(__file__).resolve().parent / 'results'),
                    help='directory for the JSON result (created if absent)')
    if needs_targets:
        ap.add_argument('--targets', default=os.environ.get('ORDK_TARGETS'),
                        help='path to ordinary_targets.csv (or set ORDK_TARGETS); required')
    return ap


def require_targets(path):
    if not path or not Path(path).is_file():
        print(f'DEPENDENCY_MISSING: ordinary_targets.csv not found ({path!r}); pass --targets or set ORDK_TARGETS')
        sys.exit(EXIT_DEPENDENCY)
    return str(Path(path).resolve())


class Run:
    def __init__(self, name, scope, out):
        self.name, self.scope, self.out = name, scope, Path(out)
        self.checks = 0
        self.failures = []
        self.groups = {}
        self.info = {}
        self.t0 = time.time()

    def check(self, ok, detail=None, group='main'):
        g = self.groups.setdefault(group, {'checks': 0, 'failures': 0})
        g['checks'] += 1
        self.checks += 1
        if not ok:
            g['failures'] += 1
            self.failures.append({'group': group, 'detail': detail})
        return ok

    def note(self, key, value):
        self.info[key] = value

    def finish(self, error=None):
        status = 'PASS'
        code = 0
        if error is not None:
            status, code = 'FAIL', EXIT_FAIL
        elif self.failures:
            status, code = 'FAIL', EXIT_FAIL
        elif self.checks == 0:
            status, code = 'VACUOUS', EXIT_VACUOUS
        rec = {'driver': self.name, 'status': status, 'exit_code': code, 'scope': self.scope,
               'checks': self.checks, 'failures': len(self.failures), 'groups': self.groups,
               'failure_examples': self.failures[:10], 'error': error, 'informational': self.info,
               'seconds': round(time.time() - self.t0, 2), 'python': sys.version, 'platform': platform.platform()}
        self.out.mkdir(parents=True, exist_ok=True)
        (self.out / f'{self.name}.json').write_text(json.dumps(rec, indent=2, default=str))
        print(f'INDEPENDENT_CHECK {self.name} status={status} checks={self.checks} failures={len(self.failures)}')
        sys.exit(code)


def run_main(run_factory, body):
    """Execute body(run); convert invariant violations into a FAIL record and exit 1."""
    run = run_factory()
    try:
        body(run)
    except CheckFailure as exc:
        print('FAIL:', exc)
        run.finish(error=f'CheckFailure: {exc}')
    run.finish()
