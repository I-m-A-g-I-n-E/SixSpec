"""
NodeAgent: Agent that operates on individual nodes without graph awareness.

This module provides the NodeAgent base class for agents that process
individual W5H1 specifications without needing graph context.

Key Characteristics:
- Operates on complete, well-formed specs
- No graph traversal capability
- Ideal for isolated operations like parsing, linting, formatting

Example:
    >>> class SimpleNodeAgent(NodeAgent):
    ...     def process_node(self, spec):
    ...         return f"Processed: {spec.subject}"
    >>> agent = SimpleNodeAgent("SimpleAgent", "file")
    >>> spec = W5H1("File", "contains", "code",
    ...             dimensions={Dimension.WHERE: "/path/to/file.py"})
    >>> agent.execute(spec)
    'Processed: File'
"""

from abc import abstractmethod
from typing import Any
from sixspec.core.models import BaseActor, W5H1


class NodeAgent(BaseActor):
    """
    Agent that operates on individual nodes without graph awareness.

    NodeAgent is designed for operations that:
    - Don't need relationship context
    - Work on isolated specifications
    - Require complete information upfront
    - Process independently

    Use cases:
    - TreeSitter parsing a single file
    - Linter checking one function
    - Test generator for one commit
    - Formatter that doesn't care about relationships

    Attributes:
        name: Identifier for this agent
        scope: What kind of node does this operate on?
        context: Dimensional context maintained by this agent

    Example:
        >>> class FileParserAgent(NodeAgent):
        ...     def process_node(self, spec):
        ...         file_path = spec.need(Dimension.WHERE)
        ...         return f"Parsing {file_path}"
        >>> agent = FileParserAgent("Parser", scope="code_file")
        >>> agent.scope
        'code_file'
    """

    def __init__(self, name: str, scope: str):
        """
        Initialize a NodeAgent.

        Args:
            name: Identifier for this agent
            scope: What kind of node does this operate on?
                  (e.g., "file", "function", "commit")
        """
        super().__init__(name)
        self.scope = scope

    def understand(self, spec: W5H1) -> bool:
        """
        Check if this agent can process the given specification.

        Node agents need clear, complete specs to operate effectively.
        This method checks if all required dimensions are present AND
        that the spec has at least one dimension set.

        Args:
            spec: W5H1 specification to evaluate

        Returns:
            True if spec is complete with dimensions, False otherwise

        Example:
            >>> agent = NodeAgent("TestAgent", "test")
            >>> complete = W5H1("A", "B", "C", dimensions={
            ...     Dimension.WHO: "user",
            ...     Dimension.WHAT: "action"
            ... })
            >>> incomplete = W5H1("A", "B", "C")
            >>> agent.understand(complete)
            True  # Has dimensions
            >>> agent.understand(incomplete)
            False  # No dimensions
        """
        # Must have at least one dimension and satisfy required dimensions
        return len(spec.dimensions) > 0 and spec.is_complete()

    def execute(self, spec: W5H1) -> Any:
        """
        Execute operation on this single node.

        This method validates that the spec is complete before
        delegating to the subclass-specific process_node() method.

        Args:
            spec: W5H1 specification to execute

        Returns:
            Result from process_node() method

        Raises:
            ValueError: If spec is missing required dimensions

        Example:
            >>> class EchoAgent(NodeAgent):
            ...     def process_node(self, spec):
            ...         return spec.subject
            >>> agent = EchoAgent("Echo", "test")
            >>> spec = W5H1("Hello", "says", "world")
            >>> agent.execute(spec)
            'Hello'
        """
        if not self.understand(spec):
            missing = [d for d in spec.required_dimensions() if not spec.has(d)]
            raise ValueError(
                f"{self.name} cannot process incomplete spec. "
                f"Missing required dimensions: {missing}"
            )

        return self.process_node(spec)

    @abstractmethod
    def process_node(self, spec: W5H1) -> Any:
        """
        Process a single node specification.

        Subclasses must implement this to define specific node
        processing logic. This method is only called after the
        spec has been validated as complete.

        Args:
            spec: Complete W5H1 specification to process

        Returns:
            Result of processing (type varies by implementation)

        Example:
            >>> class CounterAgent(NodeAgent):
            ...     def process_node(self, spec):
            ...         return len(spec.dimensions)
            >>> agent = CounterAgent("Counter", "test")
            >>> spec = W5H1("A", "B", "C", dimensions={
            ...     Dimension.WHO: "user"
            ... })
            >>> agent.process_node(spec)
            1
        """
        pass