"""
Agent implementations for the SixSpec framework.

This module provides concrete actor implementations that extend BaseActor:
- NodeAgent: Operates on individual W5H1 nodes without graph awareness
- GraphAgent: Operates on graph structures with relationship traversal

Example:
    >>> from sixspec.agents import NodeAgent, GraphAgent
"""

from sixspec.agents.node_agent import NodeAgent
from sixspec.agents.graph_agent import GraphAgent

__all__ = ['NodeAgent', 'GraphAgent']