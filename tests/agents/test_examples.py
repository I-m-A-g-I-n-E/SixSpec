"""
Tests for example agent implementations.

These tests verify that:
- TreeSitterAgent correctly implements NodeAgent interface
- DependencyAnalyzer correctly implements GraphAgent interface
- Both examples work as documented in the ticket
"""

import pytest
from sixspec.agents.examples.treesitter_agent import TreeSitterAgent
from sixspec.agents.examples.dependency_analyzer import DependencyAnalyzer
from sixspec.core.models import W5H1, Dimension


class TestTreeSitterAgent:
    """Tests for TreeSitterAgent example implementation."""

    def test_treesitter_agent_init(self):
        """Test TreeSitterAgent initialization."""
        agent = TreeSitterAgent()
        assert agent.name == "TreeSitter"
        assert agent.scope == "code_file"

    def test_treesitter_agent_is_node_agent(self):
        """Test that TreeSitterAgent is a NodeAgent."""
        from sixspec.agents.node_agent import NodeAgent
        agent = TreeSitterAgent()
        assert isinstance(agent, NodeAgent)

    def test_treesitter_agent_requires_complete_spec(self):
        """Test that TreeSitterAgent requires complete specs."""
        agent = TreeSitterAgent()

        # Complete spec with WHERE dimension
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

        # Incomplete spec without dimensions
        incomplete = W5H1(
            subject="File",
            predicate="contains",
            object="code",
            dimensions={}
        )
        assert not agent.understand(incomplete)

    def test_treesitter_agent_process_node(self):
        """Test TreeSitterAgent processing a file spec."""
        agent = TreeSitterAgent()

        spec = W5H1(
            subject="Module",
            predicate="defines",
            object="functions",
            dimensions={
                Dimension.WHERE: "/src/utils.py",
                Dimension.WHAT: "utility functions"
            }
        )

        result = agent.process_node(spec)
        assert isinstance(result, str)
        assert "/src/utils.py" in result
        assert "Parsed AST" in result

    def test_treesitter_agent_execute(self):
        """Test TreeSitterAgent execute method."""
        agent = TreeSitterAgent()

        spec = W5H1(
            subject="File",
            predicate="contains",
            object="code",
            dimensions={
                Dimension.WHERE: "main.py",
                Dimension.WHAT: "application code"
            }
        )

        result = agent.execute(spec)
        assert "main.py" in result

    def test_treesitter_agent_missing_where_dimension(self):
        """Test TreeSitterAgent handles missing WHERE dimension."""
        agent = TreeSitterAgent()

        spec = W5H1(
            subject="File",
            predicate="contains",
            object="code",
            dimensions={}
        )

        with pytest.raises(ValueError):
            agent.execute(spec)


class TestDependencyAnalyzer:
    """Tests for DependencyAnalyzer example implementation."""

    def test_dependency_analyzer_init(self):
        """Test DependencyAnalyzer initialization."""
        analyzer = DependencyAnalyzer()
        assert analyzer.name == "DependencyAnalyzer"
        assert analyzer.neighbors == []
        assert analyzer.visited == set()

    def test_dependency_analyzer_is_graph_agent(self):
        """Test that DependencyAnalyzer is a GraphAgent."""
        from sixspec.agents.graph_agent import GraphAgent
        analyzer = DependencyAnalyzer()
        assert isinstance(analyzer, GraphAgent)

    def test_dependency_analyzer_accepts_partial_spec(self):
        """Test that DependencyAnalyzer accepts partial specs."""
        analyzer = DependencyAnalyzer()

        # Partial spec with just WHERE
        partial = W5H1(
            subject="Service",
            predicate="depends",
            object="library",
            dimensions={
                Dimension.WHERE: "payment_service"
            }
        )
        assert analyzer.understand(partial)

    def test_dependency_analyzer_find_dependencies_by_shared_where(self):
        """Test finding dependencies that share WHERE dimension."""
        analyzer = DependencyAnalyzer()

        service_spec = W5H1(
            subject="Payment",
            predicate="processes",
            object="transaction",
            dimensions={Dimension.WHERE: "payment_service"}
        )

        db_spec = W5H1(
            subject="Database",
            predicate="stores",
            object="data",
            dimensions={Dimension.WHERE: "payment_service"}
        )

        api_spec = W5H1(
            subject="API",
            predicate="exposes",
            object="endpoint",
            dimensions={Dimension.WHERE: "api_gateway"}
        )

        # Set neighbors for traversal
        analyzer.neighbors = [db_spec, api_spec]

        dependencies = analyzer.traverse(service_spec)

        assert db_spec in dependencies
        assert api_spec not in dependencies

    def test_dependency_analyzer_no_shared_dimensions(self):
        """Test DependencyAnalyzer with no shared dimensions."""
        analyzer = DependencyAnalyzer()

        spec = W5H1(
            subject="Service",
            predicate="runs",
            object="task",
            dimensions={Dimension.WHERE: "service_a"}
        )

        unrelated = W5H1(
            subject="Other",
            predicate="does",
            object="thing",
            dimensions={Dimension.WHERE: "service_b"}
        )

        analyzer.neighbors = [unrelated]
        dependencies = analyzer.traverse(spec)

        assert len(dependencies) == 0

    def test_dependency_analyzer_multiple_dependencies(self):
        """Test finding multiple dependencies."""
        analyzer = DependencyAnalyzer()

        main_spec = W5H1(
            subject="Service",
            predicate="coordinates",
            object="workflow",
            dimensions={Dimension.WHERE: "backend"}
        )

        dep1 = W5H1(
            subject="Auth",
            predicate="validates",
            object="token",
            dimensions={Dimension.WHERE: "backend"}
        )

        dep2 = W5H1(
            subject="Logger",
            predicate="records",
            object="events",
            dimensions={Dimension.WHERE: "backend"}
        )

        dep3 = W5H1(
            subject="Cache",
            predicate="stores",
            object="data",
            dimensions={Dimension.WHERE: "backend"}
        )

        analyzer.neighbors = [dep1, dep2, dep3]
        dependencies = analyzer.traverse(main_spec)

        assert len(dependencies) == 3
        assert dep1 in dependencies
        assert dep2 in dependencies
        assert dep3 in dependencies

    def test_dependency_analyzer_execute(self):
        """Test DependencyAnalyzer execute method."""
        analyzer = DependencyAnalyzer()

        spec = W5H1(
            subject="Service",
            predicate="uses",
            object="resource",
            dimensions={Dimension.WHERE: "app"}
        )

        neighbor = W5H1(
            subject="Database",
            predicate="provides",
            object="storage",
            dimensions={Dimension.WHERE: "app"}
        )

        analyzer.neighbors = [neighbor]
        result = analyzer.execute(spec)

        assert isinstance(result, list)
        assert neighbor in result


class TestExampleIntegration:
    """Integration tests showing both examples working together."""

    def test_node_and_graph_agents_both_implement_base_actor(self):
        """Test that both example agents implement BaseActor interface."""
        from sixspec.core.models import BaseActor

        tree_agent = TreeSitterAgent()
        dep_analyzer = DependencyAnalyzer()

        assert isinstance(tree_agent, BaseActor)
        assert isinstance(dep_analyzer, BaseActor)

    def test_different_understand_requirements(self):
        """Test that NodeAgent and GraphAgent have different understanding."""
        tree_agent = TreeSitterAgent()
        dep_analyzer = DependencyAnalyzer()

        # Partial spec
        partial = W5H1(
            subject="Code",
            predicate="exists",
            object="somewhere",
            dimensions={Dimension.WHERE: "file.py"}
        )

        # Complete spec
        complete = W5H1(
            subject="Code",
            predicate="exists",
            object="somewhere",
            dimensions={
                Dimension.WHERE: "file.py",
                Dimension.WHAT: "implementation"
            }
        )

        # GraphAgent accepts partial
        assert dep_analyzer.understand(partial)

        # Both accept complete
        assert tree_agent.understand(complete)
        assert dep_analyzer.understand(complete)

    def test_agents_can_be_used_interchangeably_with_base_actor(self):
        """Test that both agents can be used where BaseActor is expected."""
        from sixspec.core.models import BaseActor
        from typing import List

        def process_with_agents(agents: List[BaseActor], spec: W5H1):
            """Function that accepts BaseActor instances."""
            results = []
            for agent in agents:
                if agent.understand(spec):
                    results.append(agent.name)
            return results

        tree_agent = TreeSitterAgent()
        dep_analyzer = DependencyAnalyzer()

        spec = W5H1(
            subject="Test",
            predicate="runs",
            object="code",
            dimensions={
                Dimension.WHERE: "test.py",
                Dimension.WHAT: "unit tests"
            }
        )

        results = process_with_agents([tree_agent, dep_analyzer], spec)

        assert "TreeSitter" in results
        assert "DependencyAnalyzer" in results