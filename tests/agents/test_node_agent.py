"""
Tests for NodeAgent base class.

These tests verify that NodeAgent correctly:
- Requires complete specs for operation
- Validates specs before processing
- Delegates to subclass process_node() method
- Raises appropriate errors for incomplete specs
"""

import pytest
from sixspec.agents.node_agent import NodeAgent
from sixspec.core.models import W5H1, Dimension


class TestNodeAgent(NodeAgent):
    """Test implementation of NodeAgent for testing."""

    def process_node(self, spec: W5H1) -> str:
        """Simple implementation that returns the subject."""
        return f"Processed: {spec.subject}"


def test_node_agent_init():
    """Test NodeAgent initialization."""
    agent = TestNodeAgent("TestAgent", "test_scope")
    assert agent.name == "TestAgent"
    assert agent.scope == "test_scope"
    assert isinstance(agent.context, dict)


def test_node_agent_understands_complete_spec():
    """Test that NodeAgent can understand complete specs."""
    agent = TestNodeAgent("TestAgent", "test")

    # Complete spec with dimensions
    complete = W5H1(
        subject="File",
        predicate="contains",
        object="code",
        dimensions={
            Dimension.WHERE: "/path/to/file.py",
            Dimension.WHAT: "Python code"
        }
    )
    assert agent.understand(complete)


def test_node_agent_rejects_incomplete_spec():
    """Test that NodeAgent rejects incomplete specs."""
    agent = TestNodeAgent("TestAgent", "test")

    # Incomplete spec without required dimensions
    incomplete = W5H1(
        subject="File",
        predicate="contains",
        object="code",
        dimensions={}
    )
    assert not agent.understand(incomplete)


def test_node_agent_execute_with_complete_spec():
    """Test NodeAgent execution with a complete spec."""
    agent = TestNodeAgent("TestAgent", "test")

    complete = W5H1(
        subject="TestSubject",
        predicate="does",
        object="thing",
        dimensions={
            Dimension.WHAT: "something"
        }
    )

    result = agent.execute(complete)
    assert result == "Processed: TestSubject"


def test_node_agent_execute_raises_on_incomplete_spec():
    """Test that NodeAgent raises ValueError for incomplete specs."""
    agent = TestNodeAgent("TestAgent", "test")

    incomplete = W5H1(
        subject="Incomplete",
        predicate="lacks",
        object="dimensions",
        dimensions={}
    )

    with pytest.raises(ValueError) as exc_info:
        agent.execute(incomplete)

    assert "cannot process incomplete spec" in str(exc_info.value).lower()


def test_node_agent_requires_process_node_implementation():
    """Test that NodeAgent requires subclasses to implement process_node."""
    # Cannot instantiate without implementing process_node
    with pytest.raises(TypeError):
        NodeAgent("Abstract", "scope")  # type: ignore


def test_node_agent_with_spec_subclass():
    """Test NodeAgent with SpecW5H1 that has required dimensions."""
    from sixspec.core.models import SpecW5H1

    agent = TestNodeAgent("TestAgent", "spec")

    # SpecW5H1 requires WHO, WHAT, WHY
    incomplete_spec = SpecW5H1(
        subject="System",
        predicate="provides",
        object="feature",
        dimensions={
            Dimension.WHO: "Users"
        }
    )
    assert not agent.understand(incomplete_spec)

    complete_spec = SpecW5H1(
        subject="System",
        predicate="provides",
        object="feature",
        dimensions={
            Dimension.WHO: "Users",
            Dimension.WHAT: "Authentication",
            Dimension.WHY: "Security"
        }
    )
    assert agent.understand(complete_spec)
    result = agent.execute(complete_spec)
    assert "System" in result


def test_node_agent_scope_attribute():
    """Test that scope attribute is accessible and meaningful."""
    file_agent = TestNodeAgent("FileAgent", "file")
    function_agent = TestNodeAgent("FunctionAgent", "function")
    commit_agent = TestNodeAgent("CommitAgent", "commit")

    assert file_agent.scope == "file"
    assert function_agent.scope == "function"
    assert commit_agent.scope == "commit"


def test_node_agent_context_management():
    """Test that NodeAgent maintains context properly."""
    agent = TestNodeAgent("ContextAgent", "test")

    # Context should be an empty dict initially
    assert agent.context == {}

    # Agent can store context
    agent.context[Dimension.WHO] = "test_user"
    assert agent.context[Dimension.WHO] == "test_user"


def test_node_agent_multiple_executions():
    """Test that NodeAgent can execute multiple times."""
    agent = TestNodeAgent("MultiAgent", "test")

    spec1 = W5H1("First", "does", "thing", dimensions={Dimension.WHAT: "a"})
    spec2 = W5H1("Second", "does", "thing", dimensions={Dimension.WHAT: "b"})

    result1 = agent.execute(spec1)
    result2 = agent.execute(spec2)

    assert result1 == "Processed: First"
    assert result2 == "Processed: Second"
    assert result1 != result2