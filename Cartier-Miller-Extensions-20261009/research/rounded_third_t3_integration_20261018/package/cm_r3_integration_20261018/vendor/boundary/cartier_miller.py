"""Consolidated public interface for the Cartier--Miller boundary release candidate.

Examples: python cartier_miller.py third --p 17
          python cartier_miller.py check --benchmarks smoke
See PUBLIC_INTERFACE.md for mathematical scope and stable exports.
"""
import argparse
import importlib
import sys

from boundary_framework import (
    __version__, BoundaryError, ResourceLimitError, UnsupportedPrefixError,
    BoundaryRequest, BoundaryEvaluator, BoundaryResult, PrefixProvider,
    DirectReferencePrefix, SuppliedPrefix, complete_sum,
    DirectFactorialBackend, ProductTreeFactorialBackend, BGSFactorialBackend,
)
from integrated_thirds import ThirdPointSession, ThirdPointPrefixProvider
from integrated_fifths import FifthPointSession, FifthBoundaryEvaluator
from shared_boundaries import BoundaryBatchSession
from many_primes import ManyPrimeEvaluator, PrimeQuery, range_queries
from calibrate_dispatch import calibrate

__all__ = [
    '__version__', 'BoundaryError', 'ResourceLimitError', 'UnsupportedPrefixError',
    'BoundaryRequest', 'BoundaryEvaluator', 'BoundaryResult', 'PrefixProvider',
    'DirectReferencePrefix', 'SuppliedPrefix', 'complete_sum',
    'DirectFactorialBackend', 'ProductTreeFactorialBackend', 'BGSFactorialBackend',
    'ThirdPointSession', 'ThirdPointPrefixProvider', 'FifthPointSession',
    'FifthBoundaryEvaluator', 'BoundaryBatchSession', 'ManyPrimeEvaluator',
    'PrimeQuery', 'range_queries', 'calibrate',
]

COMMANDS = {
    'boundary': 'boundary_framework',
    'boundaries': 'shared_boundaries',
    'third': 'integrated_thirds',
    'fifth': 'integrated_fifths',
    'many': 'many_primes',
    'calibrate': 'calibrate_dispatch',
    'validate': 'run_validation',
    'check': 'release_check',
}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', nargs='?', choices=tuple(COMMANDS))
    parser.add_argument('--version', action='version', version=__version__)
    if not argv or argv[0] in ('-h', '--help', '--version'):
        parser.parse_args(argv); parser.print_help() if not argv else None
        return 0
    if argv[0] not in COMMANDS:
        parser.error(f'unknown command: {argv[0]}')
    return importlib.import_module(COMMANDS[argv[0]]).main(argv[1:])


if __name__ == '__main__':
    raise SystemExit(main())
