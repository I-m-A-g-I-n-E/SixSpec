"""
Core data structures for SixSpec framework.

This module contains the fundamental building blocks:
- Dimension enum
- DiltsLevel enum with autonomy properties
- Chunk dataclass for six-dimensional specifications (5W1H model)
- Specialized Chunk subclasses (CommitChunk, SpecChunk)
- BaseActor abstract class for dimensional awareness
- SpecificationHypergraph for auto-organization
- HierarchyNode for hierarchical structure representation
"""

from sixspec.core.models import (
    Dimension,
    DiltsLevel,
    Chunk,
    CommitChunk,
    SpecChunk,
    BaseActor,
)
from sixspec.core.hypergraph import (
    SpecificationHypergraph,
    HierarchyNode,
)

__all__ = [
    "Dimension",
    "DiltsLevel",
    "Chunk",
    "CommitChunk",
    "SpecChunk",
    "BaseActor",
    "SpecificationHypergraph",
    "HierarchyNode",
]