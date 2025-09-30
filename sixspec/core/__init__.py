"""
Core data structures for SixSpec framework.

This module contains the fundamental building blocks:
- Dimension enum
- DiltsLevel enum with autonomy properties
- W5H1 dataclass for six-dimensional specifications
- Specialized W5H1 subclasses (CommitW5H1, SpecW5H1)
- BaseActor abstract class for dimensional awareness
- SpecificationHypergraph for auto-organization
- HierarchyNode for hierarchical structure representation
"""

from sixspec.core.models import (
    Dimension,
    DiltsLevel,
    W5H1,
    CommitW5H1,
    SpecW5H1,
    BaseActor,
)
from sixspec.core.hypergraph import (
    SpecificationHypergraph,
    HierarchyNode,
)

__all__ = [
    "Dimension",
    "DiltsLevel",
    "W5H1",
    "CommitW5H1",
    "SpecW5H1",
    "BaseActor",
    "SpecificationHypergraph",
    "HierarchyNode",
]