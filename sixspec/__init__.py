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
"""

from sixspec.core.models import (
    Dimension,
    DiltsLevel,
    W5H1,
    CommitW5H1,
    SpecW5H1,
    BaseActor,
)

__all__ = [
    "Dimension",
    "DiltsLevel",
    "W5H1",
    "CommitW5H1",
    "SpecW5H1",
    "BaseActor",
]