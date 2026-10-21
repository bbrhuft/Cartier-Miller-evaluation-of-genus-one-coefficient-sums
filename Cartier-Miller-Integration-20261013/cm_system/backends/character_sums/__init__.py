"""Adapted copies of the 21 October 2026 character-sum supplement sources.

Only import statements differ from the frozen copies in
Cartier-Miller-Character-Sums-20261021/src/; see PROVENANCE.json.
"""
from .weighted_sums import single_pole, prepare_weights, PreparedWeights, WeightedSums

__all__ = ['single_pole', 'prepare_weights', 'PreparedWeights', 'WeightedSums']
