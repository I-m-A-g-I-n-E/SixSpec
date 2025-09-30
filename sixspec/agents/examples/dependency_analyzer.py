"""
DependencyAnalyzer: Example GraphAgent implementation for analyzing dependencies.

This module demonstrates how to create a concrete GraphAgent that traverses
relationships between specifications to find dependencies.

Example:
    >>> from sixspec.agents.examples import DependencyAnalyzer
    >>> analyzer = DependencyAnalyzer()
    >>> spec = W5H1("Service", "depends", "library",
    ...     dimensions={Dimension.WHERE: "payment_service"})
    >>> analyzer.neighbors = [other_spec1, other_spec2]
    >>> dependencies = analyzer.traverse(spec)
"""

from typing import List
from sixspec.agents.graph_agent import GraphAgent
from sixspec.core.models import W5H1, Dimension


class DependencyAnalyzer(GraphAgent):
    """
    Analyzes dependencies between specifications using graph traversal.

    This is an example GraphAgent that demonstrates how to:
    - Work with partial specifications
    - Traverse relationships between nodes
    - Find specs that share dimensions
    - Analyze dependency chains

    The analyzer identifies dependencies by finding specs that share
    the WHERE dimension, indicating they operate in the same context
    and may have dependencies.

    Attributes:
        name: "DependencyAnalyzer" - identifier for this agent
        current_node: Currently analyzing node
        visited: Set of visited node IDs
        neighbors: List of neighboring specs to consider

    Example:
        >>> analyzer = DependencyAnalyzer()
        >>> analyzer.name
        'DependencyAnalyzer'
        >>> spec1 = W5H1("Service", "calls", "API",
        ...     dimensions={Dimension.WHERE: "service_a"})
        >>> spec2 = W5H1("Service", "uses", "Database",
        ...     dimensions={Dimension.WHERE: "service_a"})
        >>> analyzer.neighbors = [spec2]
        >>> deps = analyzer.traverse(spec1)
        >>> len(deps)
        1
    """

    def __init__(self):
        """
        Initialize the DependencyAnalyzer.

        Sets up the agent with name "DependencyAnalyzer" for tracking
        and identifying this specific agent instance.
        """
        super().__init__("DependencyAnalyzer")

    def traverse(self, start: W5H1) -> List[W5H1]:
        """
        Find all specs that depend on or are depended upon by this spec.

        Traverses the graph to find specifications that share the WHERE
        dimension with the starting spec, indicating they operate in the
        same context and may have dependencies.

        The algorithm:
        1. Start from the given spec
        2. Look at all neighbors (set via self.neighbors)
        3. Find specs that share WHERE dimension
        4. Return list of dependency specs

        Args:
            start: W5H1 specification to start dependency analysis from

        Returns:
            List of W5H1 specs that have dependencies with the start spec

        Example:
            >>> analyzer = DependencyAnalyzer()
            >>> service_spec = W5H1("Payment", "processes", "transaction",
            ...     dimensions={Dimension.WHERE: "payment_service"})
            >>> db_spec = W5H1("Database", "stores", "data",
            ...     dimensions={Dimension.WHERE: "payment_service"})
            >>> api_spec = W5H1("API", "exposes", "endpoint",
            ...     dimensions={Dimension.WHERE: "api_gateway"})
            >>> analyzer.neighbors = [db_spec, api_spec]
            >>> deps = analyzer.traverse(service_spec)
            >>> db_spec in deps
            True
            >>> api_spec in deps
            False
        """
        dependencies = []

        # Find specs that share WHERE dimension with same value
        for neighbor in self.neighbors:
            if (Dimension.WHERE in start.shared_dimensions(neighbor) and
                start.need(Dimension.WHERE) == neighbor.need(Dimension.WHERE)):
                dependencies.append(neighbor)

        return dependencies