"""
Walkers: Hierarchical execution with WHAT->WHY propagation.

This module provides the core walker implementation for SixSpec,
enabling hierarchical delegation through Dilts' Logical Levels.

Core Classes:
    - DiltsWalker: Base walker with WHAT->WHY propagation
    - ClaudeWalker: DiltsWalker enhanced with Claude Agent SDK integration
    - A2AWalker: DiltsWalker enhanced with A2A task lifecycle (DEPRECATED - use ClaudeWalker)
    - Workspace: Isolated execution environment
    - ValidationResult: Result validation for portfolio execution

Strategy Implementations:
    - MissionWalker: Level 6 walker (extreme autonomy)
    - CapabilityWalker: Level 3 walker (low autonomy)

Example:
    >>> from sixspec.walkers import MissionWalker
    >>> from sixspec.core.models import Chunk, Dimension
    >>> walker = MissionWalker()
    >>> spec = Chunk(
    ...     subject="Company",
    ...     predicate="aims",
    ...     object="growth",
    ...     dimensions={Dimension.WHAT: "Achieve market leadership"}
    ... )
    >>> result = walker.execute(spec)
"""

from sixspec.walkers.dilts_walker import DiltsWalker, ValidationResult
from sixspec.walkers.workspace import Workspace
from sixspec.walkers.claude_walker import ClaudeWalker
from sixspec.walkers.a2a_walker import A2AWalker  # DEPRECATED
from sixspec.walkers.strategies.mission_strategy import MissionWalker
from sixspec.walkers.strategies.capability_strategy import CapabilityWalker

__all__ = [
    "DiltsWalker",
    "ClaudeWalker",
    "A2AWalker",  # DEPRECATED - use ClaudeWalker
    "ValidationResult",
    "Workspace",
    "MissionWalker",
    "CapabilityWalker",
]