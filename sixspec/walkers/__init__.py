"""
Walkers: Hierarchical execution with WHAT->WHY propagation.

This module provides the core walker implementation for SixSpec,
enabling hierarchical delegation through Dilts' Logical Levels.

Core Classes:
    - DiltsWalker: Base walker with WHAT->WHY propagation
    - Workspace: Isolated execution environment
    - ValidationResult: Result validation for portfolio execution

Strategy Implementations:
    - MissionWalker: Level 6 walker (extreme autonomy)
    - CapabilityWalker: Level 3 walker (low autonomy)

Example:
    >>> from sixspec.walkers import MissionWalker
    >>> from sixspec.core.models import W5H1, Dimension
    >>> walker = MissionWalker()
    >>> spec = W5H1(
    ...     subject="Company",
    ...     predicate="aims",
    ...     object="growth",
    ...     dimensions={Dimension.WHAT: "Achieve market leadership"}
    ... )
    >>> result = walker.execute(spec)
"""

from sixspec.walkers.dilts_walker import DiltsWalker, ValidationResult
from sixspec.walkers.workspace import Workspace
from sixspec.walkers.strategies.mission_strategy import MissionWalker
from sixspec.walkers.strategies.capability_strategy import CapabilityWalker

__all__ = [
    "DiltsWalker",
    "ValidationResult",
    "Workspace",
    "MissionWalker",
    "CapabilityWalker",
]