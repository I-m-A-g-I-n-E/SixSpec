"""
Tests for GraphAgent base class.

These tests verify that GraphAgent correctly:
- Accepts partial specs
- Maintains traversal state (current_node, visited, neighbors)
- Finds neighbors by shared dimensions
- Gathers context from neighbors
- Generates unique node IDs
"""

import pytest
from sixspec.agents.graph_agent import GraphAgent
from sixspec.core.models import Chunk, Dimension


class TestGraphAgent(GraphAgent):
    """Test implementation of GraphAgent for testing."""

    def traverse(self, start: Chunk) -> list:
        """Simple implementation that returns visited nodes."""
        return list(self.visited)


def test_graph_agent_init():
    """Test GraphAgent initialization."""
    agent = TestGraphAgent("TestAgent")
    assert agent.name == "TestAgent"
    assert agent.current_node is None
    assert agent.visited == set()
    assert agent.neighbors == []
    assert isinstance(agent.context, dict)


def test_graph_agent_understands_partial_spec():
    """Test that GraphAgent can understand partial specs."""
    agent = TestGraphAgent("TestAgent")

    # Partial spec with just one dimension
    partial = Chunk(
        subject="Payment",
        predicate="processes",
        object="transaction",
        dimensions={
            Dimension.WHERE: "payment_service"
        }
    )
    assert agent.understand(partial)


def test_graph_agent_rejects_empty_spec():
    """Test that GraphAgent rejects specs with no dimensions."""
    agent = TestGraphAgent("TestAgent")

    # Empty spec without any dimensions
    empty = Chunk(
        subject="Empty",
        predicate="has",
        object="nothing",
        dimensions={}
    )
    assert not agent.understand(empty)


def test_graph_agent_execute_sets_state():
    """Test that execute() properly sets traversal state."""
    agent = TestGraphAgent("TestAgent")

    spec = Chunk(
        subject="Test",
        predicate="does",
        object="thing",
        dimensions={Dimension.WHAT: "something"}
    )

    agent.execute(spec)

    assert agent.current_node == spec
    assert len(agent.visited) == 1
    assert "Test:does:thing" in agent.visited


def test_graph_agent_node_id_generation():
    """Test node_id() generates unique identifiers."""
    node1 = Chunk("A", "does", "X")
    node2 = Chunk("A", "does", "Y")
    node3 = Chunk("B", "does", "X")

    id1 = GraphAgent.node_id(node1)
    id2 = GraphAgent.node_id(node2)
    id3 = GraphAgent.node_id(node3)

    assert id1 == "A:does:X"
    assert id2 == "A:does:Y"
    assert id3 == "B:does:X"
    assert id1 != id2
    assert id1 != id3


def test_graph_agent_find_neighbors_by_shared_dimensions():
    """Test finding neighbors that share dimensions."""
    agent = TestGraphAgent("TestAgent")

    node = Chunk(
        subject="A",
        predicate="does",
        object="X",
        dimensions={Dimension.WHERE: "service_a"}
    )

    neighbor1 = Chunk(
        subject="B",
        predicate="does",
        object="Y",
        dimensions={Dimension.WHERE: "service_a"}  # Shares WHERE
    )

    neighbor2 = Chunk(
        subject="C",
        predicate="does",
        object="Z",
        dimensions={Dimension.WHERE: "service_a"}  # Shares WHERE
    )

    unrelated = Chunk(
        subject="D",
        predicate="does",
        object="W",
        dimensions={Dimension.WHERE: "service_b"}  # Different WHERE
    )

    graph = [node, neighbor1, neighbor2, unrelated]
    neighbors = agent.find_neighbors(node, graph)

    assert neighbor1 in neighbors
    assert neighbor2 in neighbors
    assert unrelated not in neighbors
    assert node not in neighbors  # Node itself is not a neighbor


def test_graph_agent_gather_context_from_neighbors():
    """Test gathering dimensional context from neighbors."""
    agent = TestGraphAgent("TestAgent")

    # Partial spec missing WHO dimension
    partial = Chunk(
        subject="Payment",
        predicate="processes",
        object="transaction",
        dimensions={
            Dimension.WHERE: "payment_service"
        }
    )

    # Neighbor with WHO dimension
    neighbor = Chunk(
        subject="User",
        predicate="initiates",
        object="payment",
        dimensions={
            Dimension.WHERE: "payment_service",
            Dimension.WHO: "authenticated_user"
        }
    )

    graph = [partial, neighbor]
    context = agent.gather_context(partial, graph)

    assert Dimension.WHO in context
    assert context[Dimension.WHO] == "authenticated_user"


def test_graph_agent_gather_context_doesnt_override():
    """Test that gather_context doesn't override existing dimensions."""
    agent = TestGraphAgent("TestAgent")

    # Node with WHO already set
    node = Chunk(
        subject="Payment",
        predicate="processes",
        object="transaction",
        dimensions={
            Dimension.WHERE: "payment_service",
            Dimension.WHO: "original_user"
        }
    )

    # Neighbor with different WHO
    neighbor = Chunk(
        subject="User",
        predicate="initiates",
        object="payment",
        dimensions={
            Dimension.WHERE: "payment_service",
            Dimension.WHO: "different_user"
        }
    )

    graph = [node, neighbor]
    context = agent.gather_context(node, graph)

    # WHO should not be in context since node already has it
    assert Dimension.WHO not in context


def test_graph_agent_gather_context_multiple_dimensions():
    """Test gathering multiple dimensions from different neighbors."""
    agent = TestGraphAgent("TestAgent")

    # Node with only WHERE
    node = Chunk(
        subject="Payment",
        predicate="processes",
        object="transaction",
        dimensions={
            Dimension.WHERE: "payment_service"
        }
    )

    # Neighbor with WHO
    neighbor1 = Chunk(
        subject="User",
        predicate="initiates",
        object="payment",
        dimensions={
            Dimension.WHERE: "payment_service",
            Dimension.WHO: "user123"
        }
    )

    # Neighbor with WHEN
    neighbor2 = Chunk(
        subject="System",
        predicate="logs",
        object="event",
        dimensions={
            Dimension.WHERE: "payment_service",
            Dimension.WHEN: "2025-01-15"
        }
    )

    graph = [node, neighbor1, neighbor2]
    context = agent.gather_context(node, graph)

    assert Dimension.WHO in context
    assert context[Dimension.WHO] == "user123"
    assert Dimension.WHEN in context
    assert context[Dimension.WHEN] == "2025-01-15"


def test_graph_agent_visited_tracking():
    """Test that visited nodes are tracked correctly."""
    agent = TestGraphAgent("TestAgent")

    spec1 = Chunk("A", "does", "X", dimensions={Dimension.WHAT: "a"})
    spec2 = Chunk("B", "does", "Y", dimensions={Dimension.WHAT: "b"})

    # Execute first spec
    agent.execute(spec1)
    assert len(agent.visited) == 1

    # Execute second spec (simulating continued traversal)
    agent.visited.add(GraphAgent.node_id(spec2))
    assert len(agent.visited) == 2


def test_graph_agent_requires_traverse_implementation():
    """Test that GraphAgent requires subclasses to implement traverse."""
    # Cannot instantiate without implementing traverse
    with pytest.raises(TypeError):
        GraphAgent("Abstract")  # type: ignore


def test_graph_agent_neighbors_list():
    """Test that neighbors list can be populated and used."""
    agent = TestGraphAgent("TestAgent")

    spec1 = Chunk("A", "does", "X", dimensions={Dimension.WHERE: "place"})
    spec2 = Chunk("B", "does", "Y", dimensions={Dimension.WHERE: "place"})

    # Set neighbors
    agent.neighbors = [spec1, spec2]

    assert len(agent.neighbors) == 2
    assert spec1 in agent.neighbors
    assert spec2 in agent.neighbors


def test_graph_agent_find_neighbors_no_match():
    """Test find_neighbors returns empty list when no neighbors match."""
    agent = TestGraphAgent("TestAgent")

    node = Chunk(
        subject="Isolated",
        predicate="has",
        object="nothing",
        dimensions={Dimension.WHERE: "nowhere"}
    )

    other = Chunk(
        subject="Other",
        predicate="is",
        object="elsewhere",
        dimensions={Dimension.WHERE: "somewhere"}
    )

    graph = [node, other]
    neighbors = agent.find_neighbors(node, graph)

    assert len(neighbors) == 0


def test_graph_agent_is_same_system_relationship():
    """Test that neighbors are found based on is_same_system."""
    agent = TestGraphAgent("TestAgent")

    # Two nodes that share a dimension are in same system
    node1 = Chunk(
        subject="Service",
        predicate="processes",
        object="data",
        dimensions={Dimension.WHERE: "backend"}
    )

    node2 = Chunk(
        subject="API",
        predicate="exposes",
        object="endpoint",
        dimensions={Dimension.WHERE: "backend"}
    )

    assert node1.is_same_system(node2)

    graph = [node1, node2]
    neighbors = agent.find_neighbors(node1, graph)

    assert node2 in neighbors