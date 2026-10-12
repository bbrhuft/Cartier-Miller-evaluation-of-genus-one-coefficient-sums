"""Explicit, portable dependency configuration for the pilot.

Three external inputs are required by default:
  --retained   (or env RETAINED_RESEARCH)   completed retained research tree
  --extension  (or env CM_EXTENSION_SOURCE) .../source/CM_Cartier_Extension_20261012
  --handover   (or env HANDOVER_ROOT)       .../Ordinary_K_Research_Handover_20261012
A missing or malformed dependency is an error (exit status 2), never a silent
skip.  The only way to run with less is the explicit flag
--allow-missing-dependencies, which is recorded in every summary as a reduced
scope and makes run_all.py report the run as REDUCED (nonzero exit).
"""
from pathlib import Path
import argparse
import os
import sys

EXIT_DEPENDENCY = 2

EXPECTED = {
    'retained': ['depth_three_recognition_20261007/core/depth_three_recognize.py',
                 'depth_three_recognition_20261007/core/depth_three_b0_recognize.py',
                 'depth_two_recognition_20261006/core/recognize.py',
                 'isogeny_closure_20261006/core/isogeny_closure.py',
                 'branch_point_20261006/branch_evaluator.py'],
    'extension': ['core/fixed_D_evaluator.py', 'results/cm_tables.json', 'SHA256SUMS.json'],
    'handover': ['validation/results/same_trace_different_slopes.json',
                 'validation/results/ordinary_targets.csv', 'knowledge/retained_CM_tables.json'],
}
ENV = {'retained': 'RETAINED_RESEARCH', 'extension': 'CM_EXTENSION_SOURCE', 'handover': 'HANDOVER_ROOT'}


class DependencyMissing(RuntimeError):
    pass


def add_arguments(parser):
    parser.add_argument('--retained', default=None)
    parser.add_argument('--extension', default=None)
    parser.add_argument('--handover', default=None)
    parser.add_argument('--allow-missing-dependencies', action='store_true')
    return parser


def resolve(args, needed=('retained', 'extension', 'handover')):
    """Return {'paths': {...}, 'missing': [...], 'allow_missing': bool}; raise if missing and not allowed."""
    paths, missing = {}, []
    for key in needed:
        raw = getattr(args, key, None) or os.environ.get(ENV[key])
        if not raw:
            missing.append(f'{key}: not configured (pass --{key} or set {ENV[key]})')
            continue
        root = Path(raw).resolve()
        absent = [rel for rel in EXPECTED[key] if not (root / rel).is_file()]
        if absent:
            missing.append(f'{key}: {root} lacks {absent}')
            continue
        paths[key] = str(root)
    if missing and not args.allow_missing_dependencies:
        raise DependencyMissing('; '.join(missing))
    return {'paths': paths, 'missing': missing, 'allow_missing': bool(args.allow_missing_dependencies)}


def parse(description, needed=('retained', 'extension', 'handover'), extra=None):
    parser = argparse.ArgumentParser(description=description)
    add_arguments(parser)
    if extra:
        extra(parser)
    args = parser.parse_args()
    try:
        deps = resolve(args, needed)
    except DependencyMissing as exc:
        print('DEPENDENCY_MISSING:', exc)
        sys.exit(EXIT_DEPENDENCY)
    return args, deps
