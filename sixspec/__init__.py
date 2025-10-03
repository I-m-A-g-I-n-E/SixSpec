"""
SixSpec: Six-Dimensional Specification Framework

A framework for building self-documenting, traceable specifications using
the Chunk model (WHO, WHAT, WHEN, WHERE, HOW, WHY) combined with Dilts'
Logical Levels for hierarchical organization.

Core concepts:
- Chunk: Six-dimensional object representing specifications
- Dimension: The six dimensions (WHO/WHAT/WHEN/WHERE/HOW/WHY)
- DiltsLevel: Hierarchical levels from Environment to Mission
- BaseActor: Interface for entities that understand dimensions
- DiltsWalker: Hierarchical walker with WHAT→WHY propagation
- Workspace: Isolated execution environment for walkers
"""

from sixspec.core.models import (
    Dimension,
    DiltsLevel,
    Chunk,
    CommitChunk,
    SpecChunk,
    BaseActor,
)
from sixspec.walkers import (
    DiltsWalker,
    ValidationResult,
    Workspace,
    MissionWalker,
    CapabilityWalker,
)

__all__ = [
    "Dimension",
    "DiltsLevel",
    "Chunk",
    "CommitChunk",
    "SpecChunk",
    "BaseActor",
    "DiltsWalker",
    "ValidationResult",
    "Workspace",
    "MissionWalker",
    "CapabilityWalker",
]