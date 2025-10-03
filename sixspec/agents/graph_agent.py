"""
GraphAgent: Agent that operates on graph structures with relationship awareness.

This module provides the GraphAgent base class for agents that need to
understand and traverse relationships between Chunk specifications.

Key Characteristics:
- Can work with partial specs
- Traverses relationships between nodes
- Gathers context from neighbors
- Maintains visited state during traversal

Example:
    >>> class SimpleGraphAgent(GraphAgent):
    ...     def traverse(self, start):
    ...         return [start] + self.neighbors
    >>> agent = SimpleGraphAgent("GraphWalker")
    >>> spec = Chunk("A", "relates", "B")
    >>> agent.execute(spec)
    [<Chunk object>, ...]
"""

from abc import abstractmethod
from typing import Any, Dict, List, Optional, Set
from sixspec.core.models import BaseActor, Chunk, Dimension


class GraphAgent(BaseActor):
    """
    Agent that operates on graph structures.

    GraphAgent is designed for operations that:
    - Need to understand relationships
    - Can infer missing information
    - Follow chains of dependencies
    - Coordinate across multiple specs

    Use cases:
    - Walkers traversing dimensional hypergraph
    - Dependency analyzers finding related specs
    - Impact analyzers following change propagation
    - Conflict detectors checking dimensional overlaps

    Understanding:
    - Relationships between nodes
    - Shared dimensions (edges)
    - Traversal paths
    - Context inheritance

    Attributes:
        name: Identifier for this agent
        context: Dimensional context maintained by this agent
        current_node: Currently processing node
        visited: Set of visited node IDs
        neighbors: List of neighboring nodes

    Example:
        >>> class WalkerAgent(GraphAgent):
        ...     def traverse(self, start):
        ...         return [self.node_id(n) for n in self.neighbors]
        >>> agent = WalkerAgent("Walker")
        >>> agent.visited
        set()
    """

    def __init__(self, name: str):
        """
        Initialize a GraphAgent.

        Args:
            name: Identifier for this agent
        """
        super().__init__(name)
        self.current_node: Optional[Chunk] = None
        self.visited: Set[str] = set()
        self.neighbors: List[Chunk] = []

    def understand(self, spec: Chunk) -> bool:
        """
        Check if this agent can process the given specification.

        Graph agents can work with partial specs - they just need
        at least one dimension to start traversing from.

        Args:
            spec: Chunk specification to evaluate

        Returns:
            True if spec has at least one dimension, False otherwise

        Example:
            >>> agent = GraphAgent("TestAgent")
            >>> partial = Chunk("A", "B", "C", dimensions={
            ...     Dimension.WHERE: "store"
            ... })
            >>> empty = Chunk("A", "B", "C")
            >>> agent.understand(partial)
            True  # Has one dimension
            >>> agent.understand(empty)
            False  # No dimensions
        """
        return len(spec.dimensions) > 0

    def execute(self, spec: Chunk) -> Any:
        """
        Execute by traversing graph from this node.

        This method sets up the traversal state (current node, visited set)
        and delegates to the subclass-specific traverse() method.

        Args:
            spec: Chunk specification to start traversal from

        Returns:
            Result from traverse() method

        Example:
            >>> class CountingAgent(GraphAgent):
            ...     def traverse(self, start):
            ...         return len(self.visited)
            >>> agent = CountingAgent("Counter")
            >>> spec = Chunk("A", "B", "C", dimensions={
            ...     Dimension.WHO: "user"
            ... })
            >>> agent.execute(spec)
            1  # One node visited
        """
        self.current_node = spec
        self.visited.add(self.node_id(spec))

        return self.traverse(spec)

    @abstractmethod
    def traverse(self, start: Chunk) -> Any:
        """
        Traverse graph from starting node.

        Subclasses must implement this to define specific traversal
        strategy (breadth-first, depth-first, dependency-following, etc.).

        Args:
            start: Chunk node to start traversal from

        Returns:
            Result of traversal (type varies by implementation)

        Example:
            >>> class DepthFirstAgent(GraphAgent):
            ...     def traverse(self, start):
            ...         result = [start]
            ...         for neighbor in self.neighbors:
            ...             node_id = self.node_id(neighbor)
            ...             if node_id not in self.visited:
            ...                 self.visited.add(node_id)
            ...                 result.extend(self.traverse(neighbor))
            ...         return result
        """
        pass

    def find_neighbors(self, node: Chunk, graph: List[Chunk]) -> List[Chunk]:
        """
        Find nodes that share dimensions (connected by edges).

        Two nodes are neighbors if they share at least one dimension
        with the same value (not just the same dimension key).

        Args:
            node: The node to find neighbors for
            graph: List of all nodes in the graph

        Returns:
            List of neighboring Chunk nodes

        Example:
            >>> agent = GraphAgent("Finder")
            >>> node1 = Chunk("A", "B", "C", dimensions={
            ...     Dimension.WHERE: "service_a"
            ... })
            >>> node2 = Chunk("D", "E", "F", dimensions={
            ...     Dimension.WHERE: "service_a"
            ... })
            >>> node3 = Chunk("G", "H", "I", dimensions={
            ...     Dimension.WHERE: "service_b"
            ... })
            >>> graph = [node1, node2, node3]
            >>> neighbors = agent.find_neighbors(node1, graph)
            >>> node2 in neighbors
            True
            >>> node3 in neighbors
            False
        """
        neighbors = []
        for other in graph:
            if other == node:
                continue
            # Check if they share any dimension with the same value
            for dim in node.shared_dimensions(other):
                if node.need(dim) == other.need(dim):
                    neighbors.append(other)
                    break
        return neighbors

    def gather_context(self, node: Chunk, graph: List[Chunk]) -> Dict[Dimension, str]:
        """
        Gather dimensional context from neighbors.

        This method allows partial specs to inherit missing dimensions
        from their neighbors in the graph. Only dimensions that the
        node doesn't already have are inherited.

        Args:
            node: The node to gather context for
            graph: List of all nodes in the graph

        Returns:
            Dictionary mapping Dimensions to inherited values

        Example:
            >>> agent = GraphAgent("Gatherer")
            >>> partial = Chunk("Payment", "processes", "transaction",
            ...     dimensions={Dimension.WHERE: "payment_service"})
            >>> neighbor = Chunk("User", "initiates", "payment",
            ...     dimensions={
            ...         Dimension.WHERE: "payment_service",
            ...         Dimension.WHO: "authenticated_user"
            ...     })
            >>> graph = [partial, neighbor]
            >>> context = agent.gather_context(partial, graph)
            >>> context[Dimension.WHO]
            'authenticated_user'
        """
        context = {}
        neighbors = self.find_neighbors(node, graph)

        for neighbor in neighbors:
            for dim in Dimension:
                if not node.has(dim) and neighbor.has(dim):
                    # Inherit missing dimension from neighbor
                    context[dim] = neighbor.need(dim)

        return context

    @staticmethod
    def node_id(node: Chunk) -> str:
        """
        Generate unique ID for node.

        Creates a unique identifier based on the subject-predicate-object
        triple, which uniquely identifies a node in the graph.

        Args:
            node: Chunk node to generate ID for

        Returns:
            String ID in format "subject:predicate:object"

        Example:
            >>> node = Chunk("User", "wants", "feature")
            >>> GraphAgent.node_id(node)
            'User:wants:feature'
        """
        return f"{node.subject}:{node.predicate}:{node.object}"