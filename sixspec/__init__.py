"""
SixSpec: Six-Dimensional Specification Framework

A framework for building self-documenting, traceable specifications using
the W5H1 model (WHO, WHAT, WHEN, WHERE, HOW, WHY) combined with Dilts'
Logical Levels for hierarchical organization.

Core concepts:
- W5H1: Six-dimensional object representing specifications
- Dimension: The six dimensions (WHO/WHAT/WHEN/WHERE/HOW/WHY)
- DiltsLevel: Hierarchical levels from Environment to Mission
- BaseActor: Interface for entities that understand dimensions
- DiltsWalker: Hierarchical walker with WHAT→WHY propagation
- Workspace: Isolated execution environment for walkers
"""

from sixspec.core.models import (
    Dimension,
    DiltsLevel,
    W5H1,
    CommitW5H1,
    SpecW5H1,
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
    "W5H1",
    "CommitW5H1",
    "SpecW5H1",
    "BaseActor",
    "DiltsWalker",
    "ValidationResult",
    "Workspace",
    "MissionWalker",
    "CapabilityWalker",
]