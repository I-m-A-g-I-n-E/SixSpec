"""
TreeSitterAgent: Example NodeAgent implementation for parsing code structure.

This module demonstrates how to create a concrete NodeAgent that operates
on individual code files without needing graph context.

Example:
    >>> from sixspec.agents.examples import TreeSitterAgent
    >>> agent = TreeSitterAgent()
    >>> spec = W5H1("File", "contains", "code",
    ...     dimensions={Dimension.WHERE: "/path/to/file.py"})
    >>> result = agent.process_node(spec)
    >>> print(result)
    Parsed AST from /path/to/file.py
"""

from typing import Any
from sixspec.agents.node_agent import NodeAgent
from sixspec.core.models import W5H1, Dimension


class TreeSitterAgent(NodeAgent):
    """
    Parses code structure using TreeSitter (mock implementation).

    This is an example NodeAgent that demonstrates how to:
    - Operate on complete file specifications
    - Extract dimensional information (WHERE for file path)
    - Process a single node without graph context
    - Return structured results

    In a real implementation, this would use the tree-sitter library
    to parse the actual code into an AST. This mock version demonstrates
    the interface and dimensional requirements.

    Attributes:
        name: "TreeSitter" - identifier for this agent
        scope: "code_file" - indicates this operates on file-level specs

    Example:
        >>> agent = TreeSitterAgent()
        >>> agent.name
        'TreeSitter'
        >>> agent.scope
        'code_file'
        >>> spec = W5H1("File", "contains", "code",
        ...     dimensions={Dimension.WHERE: "main.py"})
        >>> agent.understand(spec)
        True
        >>> result = agent.process_node(spec)
        >>> "main.py" in result
        True
    """

    def __init__(self):
        """
        Initialize the TreeSitterAgent.

        Sets up the agent with name "TreeSitter" and scope "code_file",
        indicating it operates on file-level code specifications.
        """
        super().__init__("TreeSitter", scope="code_file")

    def process_node(self, spec: W5H1) -> Any:
        """
        Parse the code file into AST (mock implementation).

        Extracts the file path from the WHERE dimension and returns
        a string representing the parsed AST. In a real implementation,
        this would:
        1. Read the file from the path
        2. Use tree-sitter to parse the code
        3. Return a structured AST object

        Args:
            spec: W5H1 specification with WHERE dimension set to file path

        Returns:
            String describing the parsing result

        Example:
            >>> agent = TreeSitterAgent()
            >>> spec = W5H1("Module", "defines", "functions",
            ...     dimensions={Dimension.WHERE: "/src/utils.py"})
            >>> result = agent.process_node(spec)
            >>> result
            'Parsed AST from /src/utils.py'
        """
        file_path = spec.need(Dimension.WHERE)
        # In a real implementation, would use TreeSitter to parse
        # For now, return a mock result
        return f"Parsed AST from {file_path}"