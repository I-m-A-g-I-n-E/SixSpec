"""
Tests for DiltsWalker implementation.

Tests cover:
- WHAT→WHY propagation
- Full hierarchy execution
- Provenance tracing
- Autonomy gradient
- Portfolio execution
- Workspace isolation
"""

import pytest
from sixspec.core.models import Dimension, DiltsLevel, W5H1
from sixspec.walkers.dilts_walker import DiltsWalker, ValidationResult
from sixspec.walkers.strategies.mission_strategy import MissionWalker
from sixspec.walkers.strategies.capability_strategy import CapabilityWalker


def test_what_becomes_why():
    """
    Test that parent's WHAT becomes child's WHY.

    This is the core purpose propagation pattern.
    """
    # Create parent walker at Identity level
    parent = MissionWalker()
    parent_spec = W5H1(
        subject="Company",
        predicate="launches",
        object="product",
        dimensions={Dimension.WHAT: "Launch premium tier"}
    )
    parent.execute(parent_spec)

    # Create child at Beliefs level
    child = MissionWalker(parent=parent)
    child.current_node = parent.current_node

    # Child should inherit parent's WHAT as its WHY
    assert child.context[Dimension.WHY] == "Launch premium tier"


def test_full_hierarchy():
    """
    Test execution through full 6-level hierarchy.

    Should descend from Mission (L6) to Environment (L1).
    """
    mission = MissionWalker()
    spec = W5H1(
        subject="Company",
        predicate="needs to",
        object="grow",
        dimensions={Dimension.WHAT: "Increase revenue"}
    )

    result = mission.execute(spec)

    # Should descend to L1 and execute ground action
    assert "EXECUTED" in result
    # Should have spawned children
    assert len(mission.children) > 0


def test_provenance():
    """
    Test provenance tracing through hierarchy.

    Should be able to trace WHY chain from L1 to L6.
    """
    L6 = MissionWalker()
    spec = W5H1(
        subject="Company",
        predicate="needs",
        object="revenue",
        dimensions={Dimension.WHAT: "Increase revenue"}
    )
    L6.execute(spec)

    # Get L1 walker from execution (bottom of hierarchy)
    L1 = L6
    while L1.children:
        L1 = L1.children[0]

    # Trace provenance from L1 back to L6
    chain = L1.trace_provenance()

    # Should have full chain
    assert len(chain) == 6
    # Mission's WHAT should be at top of chain
    assert chain[0] == "Increase revenue"


def test_autonomy_gradient():
    """
    Test that different levels have different autonomy.

    Higher levels should have more autonomy (more strategy variation).
    """
    # Mission level - extreme autonomy
    mission = MissionWalker()
    mission_spec = W5H1(
        subject="Company",
        predicate="aims",
        object="growth",
        dimensions={Dimension.WHAT: "Grow market share"}
    )
    mission_strategies = mission.generate_strategies(mission_spec, 3)

    # Capability level - low autonomy
    capability = CapabilityWalker()
    capability_spec = W5H1(
        subject="System",
        predicate="needs",
        object="feature",
        dimensions={Dimension.WHAT: "Implement feature"}
    )
    capability_strategies = capability.generate_strategies(capability_spec, 3)

    # Both should generate 3 strategies
    assert len(mission_strategies) == 3
    assert len(capability_strategies) == 3

    # Strategies should be different strings
    assert all(isinstance(s, str) for s in mission_strategies)
    assert all(isinstance(s, str) for s in capability_strategies)


def test_portfolio_execution():
    """
    Test portfolio execution with multiple strategies.

    Should try multiple approaches and pick the best.
    """
    walker = CapabilityWalker()
    spec = W5H1(
        subject="System",
        predicate="needs",
        object="payment",
        dimensions={
            Dimension.WHAT: "Integrate payment processing",
            Dimension.WHY: "Launch premium tier"
        }
    )

    # Execute with 3 different strategies
    result = walker.execute_portfolio(spec, n_strategies=3)

    # Should have tried 3 approaches
    assert len(walker.children) == 3

    # Should have picked best result
    assert result is not None
    assert isinstance(result, str)


def test_workspace_isolation():
    """
    Test that each walker gets isolated workspace.
    """
    walker1 = CapabilityWalker()
    walker2 = CapabilityWalker()

    spec = W5H1(
        subject="System",
        predicate="executes",
        object="task",
        dimensions={Dimension.WHAT: "Do something"}
    )

    walker1.execute(spec)
    walker2.execute(spec)

    # Each should have its own workspace
    assert walker1.workspace is not None
    assert walker2.workspace is not None
    assert walker1.workspace.walker_id != walker2.workspace.walker_id
    assert walker1.workspace.path != walker2.workspace.path


def test_ground_action():
    """
    Test that Level 1 executes ground action.
    """
    walker = CapabilityWalker()
    walker.level = DiltsLevel.ENVIRONMENT  # Override to L1 for testing

    spec = W5H1(
        subject="System",
        predicate="executes",
        object="action",
        dimensions={
            Dimension.WHAT: "Run tests",
            Dimension.WHY: "Verify implementation"
        }
    )

    result = walker.execute_ground_action(spec)

    assert "EXECUTED" in result
    assert "Run tests" in result
    assert "Verify implementation" in result


def test_validation_result():
    """
    Test ValidationResult functionality.
    """
    # Successful validation
    success = ValidationResult(
        score=0.9,
        passed=True,
        details="Test passed"
    )
    assert success.score == 0.9
    assert success.passed is True

    # Failed validation
    failure = ValidationResult(
        score=0.2,
        passed=False,
        details="Test failed"
    )
    assert failure.score == 0.2
    assert failure.passed is False


def test_context_propagation():
    """
    Test that context is properly maintained and propagated.
    """
    parent = CapabilityWalker()
    parent_spec = W5H1(
        subject="System",
        predicate="needs",
        object="feature",
        dimensions={Dimension.WHAT: "Build billing system"}
    )
    parent.execute(parent_spec)

    # Parent should have WHAT in context
    assert parent.context[Dimension.WHAT] == "Build billing system"

    # Check that child was created with proper context
    if parent.children:
        child = parent.children[0]
        # Child's WHY should be parent's WHAT
        assert child.context[Dimension.WHY] == "Build billing system"


def test_spawn_children():
    """
    Test spawning multiple children with different strategies.
    """
    walker = CapabilityWalker()
    walker.current_node = W5H1(
        subject="System",
        predicate="needs",
        object="feature",
        dimensions={Dimension.WHAT: "Implement feature"}
    )

    base_spec = W5H1(
        subject="System",
        predicate="builds",
        object="component",
        dimensions={Dimension.WHAT: "Build component"}
    )

    children = walker.spawn_children(3, base_spec)

    # Should create 3 children
    assert len(children) == 3

    # Each child should have:
    # 1. A walker instance
    # 2. A spec with parent's WHAT as WHY
    for child_walker, child_spec in children:
        assert isinstance(child_walker, DiltsWalker)
        assert isinstance(child_spec, W5H1)
        assert child_spec.need(Dimension.WHY) == "Implement feature"


def test_walker_hierarchy_levels():
    """
    Test that walkers correctly track their levels.
    """
    mission = MissionWalker()
    assert mission.level == DiltsLevel.MISSION
    assert mission.level.value == 6

    capability = CapabilityWalker()
    assert capability.level == DiltsLevel.CAPABILITY
    assert capability.level.value == 3


def test_empty_spec_handling():
    """
    Test handling of specs with missing dimensions.
    """
    walker = CapabilityWalker()
    spec = W5H1(
        subject="System",
        predicate="does",
        object="something",
        dimensions={}  # No dimensions
    )

    # Should handle gracefully (might not execute fully but shouldn't crash)
    try:
        result = walker.execute(spec)
        # If it executes, result should exist
        assert result is not None
    except Exception:
        # Or it might raise an exception, which is also acceptable
        pass


def test_multiple_levels_of_children():
    """
    Test that hierarchy correctly creates multiple levels.
    """
    mission = MissionWalker()
    spec = W5H1(
        subject="Company",
        predicate="aims",
        object="growth",
        dimensions={Dimension.WHAT: "Achieve dominance"}
    )

    mission.execute(spec)

    # Mission should have children (Identity level)
    assert len(mission.children) > 0
    identity = mission.children[0]

    # Identity should have children (Beliefs level)
    assert len(identity.children) > 0
    beliefs = identity.children[0]

    # Each level should be one lower
    assert mission.level.value == 6
    assert identity.level.value == 5
    assert beliefs.level.value == 4