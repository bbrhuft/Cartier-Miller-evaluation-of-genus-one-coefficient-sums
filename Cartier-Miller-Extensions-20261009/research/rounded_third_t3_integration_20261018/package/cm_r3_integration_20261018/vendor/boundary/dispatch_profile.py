"""Local measured dispatch data. Profiles contain timings, never Python code."""
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
from statistics import median
import sys
import tempfile
from time import perf_counter

from boundary_framework import BoundaryError, ResourceLimitError, __version__

SCHEMA = 1
MAX_PROFILE_BYTES = 4 * 1024 * 1024
MAX_RECORDS = 256
TIE_MARGIN = 0.05


def environment():
    return {'python': platform.python_version(), 'implementation': platform.python_implementation(),
            'system': platform.system(), 'release': platform.release(),
            'machine': platform.machine(), 'processor': platform.processor(),
            'logical_cpus': os.cpu_count(), 'pointer_bits': 64 if sys.maxsize > 2**32 else 32,
            'optimized': sys.flags.optimize}


def implementation_hash():
    root = Path(__file__).resolve().parent
    names = ['boundary_framework.py', 'many_primes.py', 'shared_boundaries.py',
             'integrated_thirds.py', 'integrated_fifths.py', 'dispatch_profile.py',
             'calibrate_dispatch.py', 'benchmark_many_primes.py']
    names += [str(p.relative_to(root)) for p in sorted((root / 'retained_cm').rglob('*.py'))]
    digest = hashlib.sha256()
    for name in names:
        digest.update(name.encode()); digest.update(b'\0')
        digest.update((root / name).read_bytes())
    return digest.hexdigest()


def configuration(evaluator):
    return {**evaluator.kernel_options,
            **{name: getattr(evaluator, name) for name in
               ('max_queries', 'max_forest_index', 'max_modulus_bits', 'max_chunk_product_bits')}}


def workload_key(queries, output_mode, collection):
    digest = hashlib.sha256()
    digest.update(f'{output_mode}:{collection}\n'.encode())
    for query in queries:
        digest.update(f'{query.p}:{query.L}\n'.encode())
    return digest.hexdigest()


def load_profile(path):
    if not isinstance(path, (str, Path)):
        raise BoundaryError('profile path must be a string or Path')
    path = Path(path)
    if path.stat().st_size > MAX_PROFILE_BYTES:
        raise BoundaryError('dispatch profile exceeds size limit')
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise BoundaryError('invalid dispatch profile JSON') from exc
    if (not isinstance(data, dict) or type(data.get('schema')) is not int or data['schema'] != SCHEMA
            or not isinstance(data.get('records'), list) or len(data['records']) > MAX_RECORDS
            or any(not isinstance(r, dict) for r in data.get('records', []))):
        raise BoundaryError('invalid dispatch profile schema')
    return data


def _candidates(record):
    candidates = record.get('candidates')
    if not isinstance(candidates, list) or not 1 <= len(candidates) <= 64:
        raise BoundaryError('invalid candidate list')
    result, seen = [], set()
    for candidate in candidates:
        if not isinstance(candidate, dict) or candidate.get('verified') is not True:
            raise BoundaryError('unverified dispatch candidate')
        engine, backend, chunks = (candidate.get(k) for k in ('engine', 'backend', 'chunks'))
        if engine not in ('forest', 'independent') or backend not in ('auto', 'direct', 'product_tree', 'bgs'):
            raise BoundaryError('invalid candidate method')
        if type(chunks) is not int or not 1 <= chunks <= 100000:
            raise BoundaryError('invalid candidate chunk count')
        samples = candidate.get('samples_seconds')
        if (not isinstance(samples, list) or not 3 <= len(samples) <= 20 or
                any(type(v) not in (int, float) or not 0 < v <= 1_000_000_000 or not math.isfinite(v) for v in samples)):
            raise BoundaryError('invalid candidate timing samples')
        key = (engine, backend, chunks)
        if key in seen:
            raise BoundaryError('duplicate dispatch candidate')
        seen.add(key)
        result.append({**candidate, 'median_seconds': median(samples)})
    return result


def select(evaluator, wanted, unique, *, profile, backend, output_mode, collection, chunks):
    """Select exact local measurements or return a labeled independent default."""
    begin = perf_counter()
    decision = {'status': 'fallback_untrained', 'reason': 'profile_not_supplied',
                'selected_engine': 'independent', 'selected_backend': backend,
                'selected_chunks': chunks, 'measured_median_seconds': None,
                'eligible_measured_candidates': 0, 'tie_margin': TIE_MARGIN}

    def finish():
        decision['selection_seconds'] = perf_counter() - begin
        return decision

    if not wanted:
        decision['reason'] = 'empty_workload'
        return finish()
    if profile is None:
        return finish()
    try:
        data = load_profile(profile)
    except FileNotFoundError:
        decision['reason'] = 'profile_missing'
        return finish()
    except (BoundaryError, OSError):
        decision['reason'] = 'profile_invalid_or_unreadable'
        return finish()
    if data.get('environment') != environment():
        decision['reason'] = 'profile_environment_mismatch'
        return finish()
    try:
        current_implementation = implementation_hash()
    except OSError:
        decision['reason'] = 'profile_source_unavailable'
        return finish()
    if data.get('implementation_sha256') != current_implementation or data.get('version') != __version__:
        decision['reason'] = 'profile_implementation_mismatch'
        return finish()
    key = workload_key(wanted, output_mode, collection)
    records = [r for r in data['records'] if isinstance(r, dict) and r.get('workload_sha256') == key]
    if not records:
        decision['reason'] = 'workload_unmeasured'
        return finish()
    record = records[-1]
    if record.get('configuration') != configuration(evaluator):
        decision['reason'] = 'profile_configuration_mismatch'
        return finish()
    try:
        candidates = _candidates(record)
    except BoundaryError:
        decision['reason'] = 'profile_candidate_invalid'
        return finish()
    eligible, rejected = [], []
    for candidate in candidates:
        if candidate['engine'] == 'independent' and backend != 'auto' and candidate['backend'] != backend:
            continue
        if candidate['engine'] == 'forest':
            schedule = evaluator._schedule(unique, candidate['chunks'])
            try:
                evaluator._check_forest(schedule)
            except ResourceLimitError:
                rejected.append({'engine': 'forest', 'chunks': candidate['chunks']})
                continue
        eligible.append(candidate)
    decision['eligible_measured_candidates'] = len(eligible)
    decision['resource_rejections'] = rejected
    if not eligible:
        decision['reason'] = 'no_eligible_measurement'
        return finish()
    baseline = next((c for c in eligible if c['engine'] == 'independent' and c['backend'] == backend), None)
    best = min(eligible, key=lambda c: c['median_seconds'])
    near_tie = baseline is not None and best['median_seconds'] >= (1 - TIE_MARGIN) * baseline['median_seconds']
    selected = baseline if near_tie else best
    decision.update(status='measured_near_tie' if near_tie and best is not baseline else 'measured_exact',
                    reason='retained_baseline_within_tie_margin' if near_tie and best is not baseline
                    else 'lowest_eligible_measured_median',
                    selected_engine=selected['engine'],
                    selected_backend=selected['backend'] if selected['engine'] == 'independent' else backend,
                    selected_chunks=selected['chunks'],
                    measured_median_seconds=selected['median_seconds'], workload_sha256=key,
                    profile_samples=len(selected['samples_seconds']))
    return finish()


def validate_target(path):
    """Check compatibility before an expensive calibration; do not write."""
    if not isinstance(path, (str, Path)):
        raise BoundaryError('profile path must be a string or Path')
    path = Path(path)
    if not path.resolve().parent.is_dir():
        raise BoundaryError('profile parent directory must exist')
    stamp = {'schema': SCHEMA, 'version': __version__, 'environment': environment(),
             'implementation_sha256': implementation_hash()}
    if path.exists():
        data = load_profile(path)
        if any(data.get(k) != v for k, v in stamp.items()):
            raise BoundaryError('existing profile belongs to another implementation or environment; use a new path')
    else:
        data = {**stamp, 'records': []}
    return data


def write_record(path, record):
    """Upsert one calibrated workload, preserving compatible measured records."""
    data = validate_target(path)
    path = Path(path)
    _candidates(record)
    data['records'] = [r for r in data['records'] if r.get('workload_sha256') != record['workload_sha256']]
    data['records'].append(record)
    if len(data['records']) > MAX_RECORDS:
        raise BoundaryError('dispatch profile record limit exceeded')
    data['updated_utc'] = datetime.now(timezone.utc).isoformat()
    encoded = json.dumps(data, indent=2, allow_nan=False) + '\n'
    if len(encoded.encode('utf-8')) > MAX_PROFILE_BYTES:
        raise BoundaryError('dispatch profile size limit exceeded')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.resolve().parent, delete=False) as stream:
            temporary = Path(stream.name); stream.write(encoded)
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
