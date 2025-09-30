"""
Tests for strategy implementations.

Tests cover:
- MissionWalker strategy generation and validation
- CapabilityWalker strategy generation and validation
- Autonomy differences between levels
- Portfolio execution at different levels
"""

import pytest
from sixspec.core.models import Dimension, DiltsLevel, W5H1
from sixspec.walkers.strategies.mission_strategy import MissionWalker
from sixspec.walkers.strategies.capability_strategy import CapabilityWalker
from sixspec.walkers.dilts_walker import ValidationResult


class TestMissionWalker:
    """Tests for Mission-level walker (L6)."""

    def test_initialization(self):
        """Test MissionWalker initialization."""
        walker = MissionWalker()
        assert walker.level == DiltsLevel.MISSION
        assert walker.level.value == 6
        assert walker.level.autonomy == "extreme"

    def test_generate_strategies(self):
        """Test strategic option generation at Mission level."""
        walker = MissionWalker()
        spec = W5H1(
            subject="Company",
            predicate="aims to",
            object="growth",
            dimensions={Dimension.WHAT: "Grow market share"}
        )

        strategies = walker.generate_strategies(spec, 3)

        assert len(strategies) == 3
        assert all(isinstance(s, str) for s in strategies)
        # Should include base WHAT in strategies
        assert all("Grow market share" in s for s in strategies)
        # Should have different approaches
        assert len(set(strategies)) == 3

    def test_generate_many_strategies(self):
        """Test generating large number of strategies."""
        walker = MissionWalker()
        spec = W5H1(
            subject="Company",
            predicate="aims",
            object="goal",
            dimensions={Dimension.WHAT: "Achieve goal"}
        )

        strategies = walker.generate_strategies(spec, 10)

        assert len(strategies) == 10
        assert all(isinstance(s, str) for s in strategies)

    def test_validate_success(self):
        """Test validation of successful execution."""
        walker = MissionWalker()
        result = "EXECUTED: Strategy implementation (because: Purpose)"

        validation = walker.validate(result)

        assert isinstance(validation, ValidationResult)
        assert validation.passed is True
        assert validation.score > 0.8

    def test_validate_failure(self):
        """Test validation of failed execution."""
        walker = MissionWalker()

        # None result
        validation = walker.validate(None)
        assert validation.passed is False
        assert validation.score == 0.0

        # Empty result
        validation = walker.validate("")
        assert validation.passed is False

    def test_full_execution(self):
        """Test full Mission-level execution."""
        walker = MissionWalker()
        spec = W5H1(
            subject="Company",
            predicate="aims",
            object="success",
            dimensions={Dimension.WHAT: "Achieve market leadership"}
        )

        result = walker.execute(spec)

        assert result is not None
        assert walker.workspace is not None
        # Should spawn children
        assert len(walker.children) > 0


class TestCapabilityWalker:
    """Tests for Capability-level walker (L3)."""

    def test_initialization(self):
        """Test CapabilityWalker initialization."""
        walker = CapabilityWalker()
        assert walker.level == DiltsLevel.CAPABILITY
        assert walker.level.value == 3
        assert walker.level.autonomy == "low"

    def test_generate_strategies(self):
        """Test implementation approach generation at Capability level."""
        walker = CapabilityWalker()
        spec = W5H1(
            subject="System",
            predicate="needs",
            object="feature",
            dimensions={Dimension.WHAT: "Implement authentication"}
        )

        strategies = walker.generate_strategies(spec, 3)

        assert len(strategies) == 3
        assert all(isinstance(s, str) for s in strategies)
        # Should include base WHAT in strategies
        assert all("Implement authentication" in s for s in strategies)
        # Should have different approaches
        assert len(set(strategies)) == 3

    def test_generate_strategies_with_why(self):
        """Test strategy generation with WHY context."""
        walker = CapabilityWalker()
        spec = W5H1(
            subject="System",
            predicate="builds",
            object="component",
            dimensions={
                Dimension.WHAT: "Build payment integration",
                Dimension.WHY: "Enable premium tier"
            }
        )

        strategies = walker.generate_strategies(spec, 3)

        assert len(strategies) == 3
        assert all("Build payment integration" in s for s in strategies)

    def test_validate_with_context(self):
        """Test validation of execution with full context."""
        walker = CapabilityWalker()
        result = "EXECUTED: Build feature (because: User need)"

        validation = walker.validate(result)

        assert validation.passed is True
        assert validation.score == 1.0
        assert "full context" in validation.details

    def test_validate_without_context(self):
        """Test validation of execution without context."""
        walker = CapabilityWalker()
        result = "EXECUTED: Build feature"

        validation = walker.validate(result)

        assert validation.passed is True
        assert validation.score == 0.8

    def test_validate_failure(self):
        """Test validation of failed execution."""
        walker = CapabilityWalker()

        # None result
        validation = walker.validate(None)
        assert validation.passed is False
        assert validation.score == 0.0

        # Empty result
        validation = walker.validate("")
        assert validation.passed is False

    def test_full_execution(self):
        """Test full Capability-level execution."""
        walker = CapabilityWalker()
        spec = W5H1(
            subject="System",
            predicate="implements",
            object="feature",
            dimensions={
                Dimension.WHAT: "Integrate payment system",
                Dimension.WHY: "Support subscriptions"
            }
        )

        result = walker.execute(spec)

        assert result is not None
        assert walker.workspace is not None


class TestStrategyDifferences:
    """Tests comparing different strategy levels."""

    def test_autonomy_levels(self):
        """Test that different levels have different autonomy."""
        mission = MissionWalker()
        capability = CapabilityWalker()

        # Mission should have extreme autonomy
        assert mission.level.autonomy == "extreme"
        # Capability should have low autonomy
        assert capability.level.autonomy == "low"

    def test_strategy_variation(self):
        """Test that strategies vary by level."""
        mission_spec = W5H1(
            subject="Company",
            predicate="aims",
            object="growth",
            dimensions={Dimension.WHAT: "Achieve goal"}
        )
        capability_spec = W5H1(
            subject="System",
            predicate="needs",
            object="feature",
            dimensions={Dimension.WHAT: "Achieve goal"}
        )

        mission = MissionWalker()
        mission_strategies = mission.generate_strategies(mission_spec, 3)

        capability = CapabilityWalker()
        capability_strategies = capability.generate_strategies(capability_spec, 3)

        # Both generate same number
        assert len(mission_strategies) == len(capability_strategies)

        # But strategies should be different (different templates)
        # Mission uses strategic templates, Capability uses implementation templates
        assert mission_strategies != capability_strategies

    def test_validation_criteria(self):
        """Test that validation criteria differ by level."""
        mission = MissionWalker()
        capability = CapabilityWalker()

        result_with_context = "EXECUTED: Action (because: Reason)"
        result_without = "EXECUTED: Action"

        mission_val = mission.validate(result_with_context)
        capability_val = capability.validate(result_with_context)

        # Capability gives higher score for full context
        assert capability_val.score == 1.0
        # Mission gives good score but not perfect for execution
        assert mission_val.score == 0.9


class TestPortfolioExecution:
    """Tests for portfolio execution at different levels."""

    def test_mission_portfolio(self):
        """Test portfolio execution at Mission level."""
        walker = MissionWalker()
        spec = W5H1(
            subject="Company",
            predicate="needs",
            object="success",
            dimensions={Dimension.WHAT: "Achieve dominance"}
        )

        result = walker.execute_portfolio(spec, n_strategies=3)

        assert result is not None
        assert len(walker.children) == 3

    def test_capability_portfolio(self):
        """Test portfolio execution at Capability level."""
        walker = CapabilityWalker()
        spec = W5H1(
            subject="System",
            predicate="needs",
            object="payment",
            dimensions={
                Dimension.WHAT: "Integrate payment",
                Dimension.WHY: "Enable premium"
            }
        )

        result = walker.execute_portfolio(spec, n_strategies=3)

        assert result is not None
        assert len(walker.children) == 3

    def test_portfolio_picks_best(self):
        """Test that portfolio picks best result."""
        walker = CapabilityWalker()
        spec = W5H1(
            subject="System",
            predicate="does",
            object="task",
            dimensions={Dimension.WHAT: "Complete task"}
        )

        result = walker.execute_portfolio(spec, n_strategies=3)

        # Should pick a result
        assert result is not None
        # All children should have been tried
        assert len(walker.children) == 3


class TestWalkerInheritance:
    """Tests for parent-child relationships in walkers."""

    def test_child_inherits_why(self):
        """Test that child inherits parent's WHAT as WHY."""
        parent = CapabilityWalker()
        parent_spec = W5H1(
            subject="System",
            predicate="builds",
            object="feature",
            dimensions={Dimension.WHAT: "Build billing"}
        )
        parent.execute(parent_spec)

        # Check child got parent's WHAT as WHY
        if parent.children:
            child = parent.children[0]
            assert child.context[Dimension.WHY] == "Build billing"

    def test_mission_spawns_identity(self):
        """Test that Mission spawns Identity-level children."""
        mission = MissionWalker()
        spec = W5H1(
            subject="Company",
            predicate="aims",
            object="goal",
            dimensions={Dimension.WHAT: "Lead market"}
        )

        mission.execute(spec)

        assert len(mission.children) > 0
        child = mission.children[0]
        assert child.level.value == 5  # Identity level