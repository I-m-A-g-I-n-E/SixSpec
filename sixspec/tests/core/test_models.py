"""
Comprehensive tests for SixSpec core data structures.

Tests cover:
- Dimension enum
- DiltsLevel enum with properties
- W5H1 dataclass with all methods
- WHAT→WHY inheritance pattern
- Specialized subclasses (CommitW5H1, SpecW5H1)
- BaseActor abstract class
- Edge cases and error handling
"""

import pytest
from abc import ABC

from sixspec.core.models import (
    Dimension,
    DiltsLevel,
    W5H1,
    CommitW5H1,
    SpecW5H1,
    BaseActor,
)


# ============================================================================
# Dimension Enum Tests
# ============================================================================

def test_dimension_enum_values():
    """Test that all six dimensions are defined correctly."""
    assert Dimension.WHO.value == "who"
    assert Dimension.WHAT.value == "what"
    assert Dimension.WHEN.value == "when"
    assert Dimension.WHERE.value == "where"
    assert Dimension.HOW.value == "how"
    assert Dimension.WHY.value == "why"


def test_dimension_enum_count():
    """Test that exactly six dimensions exist."""
    assert len(list(Dimension)) == 6


# ============================================================================
# DiltsLevel Enum Tests
# ============================================================================

def test_dilts_level_values():
    """Test that all six levels are defined with correct values."""
    assert DiltsLevel.MISSION.value == 6
    assert DiltsLevel.IDENTITY.value == 5
    assert DiltsLevel.BELIEFS.value == 4
    assert DiltsLevel.CAPABILITY.value == 3
    assert DiltsLevel.BEHAVIOR.value == 2
    assert DiltsLevel.ENVIRONMENT.value == 1


def test_dilts_level_count():
    """Test that exactly six levels exist."""
    assert len(list(DiltsLevel)) == 6


def test_dilts_level_primary_dimensions():
    """Test that each level maps to correct primary dimensions."""
    assert DiltsLevel.MISSION.primary_dimensions == {Dimension.WHY}
    assert DiltsLevel.IDENTITY.primary_dimensions == {Dimension.WHO}
    assert DiltsLevel.BELIEFS.primary_dimensions == {Dimension.WHY}
    assert DiltsLevel.CAPABILITY.primary_dimensions == {Dimension.HOW}
    assert DiltsLevel.BEHAVIOR.primary_dimensions == {Dimension.WHAT}
    assert DiltsLevel.ENVIRONMENT.primary_dimensions == {Dimension.WHERE, Dimension.WHEN}


def test_dilts_level_autonomy():
    """Test that each level has correct autonomy string."""
    assert DiltsLevel.MISSION.autonomy == "extreme"
    assert DiltsLevel.IDENTITY.autonomy == "high"
    assert DiltsLevel.BELIEFS.autonomy == "moderate"
    assert DiltsLevel.CAPABILITY.autonomy == "low"
    assert DiltsLevel.BEHAVIOR.autonomy == "very_low"
    assert DiltsLevel.ENVIRONMENT.autonomy == "zero"


# ============================================================================
# W5H1 Basic Functionality Tests
# ============================================================================

def test_w5h1_creation_minimal():
    """Test creating a minimal W5H1 object."""
    spec = W5H1(
        subject="User",
        predicate="wants",
        object="feature"
    )
    assert spec.subject == "User"
    assert spec.predicate == "wants"
    assert spec.object == "feature"
    assert spec.dimensions == {}
    assert spec.confidence == {}
    assert spec.level is None


def test_w5h1_creation_with_dimensions():
    """Test creating W5H1 with initial dimensions."""
    dimensions = {
        Dimension.WHO: "Premium users",
        Dimension.WHAT: "Advanced reporting"
    }
    spec = W5H1(
        subject="System",
        predicate="provides",
        object="reports",
        dimensions=dimensions
    )
    assert spec.dimensions[Dimension.WHO] == "Premium users"
    assert spec.dimensions[Dimension.WHAT] == "Advanced reporting"


def test_w5h1_creation_with_level():
    """Test creating W5H1 with Dilts level."""
    spec = W5H1(
        subject="Team",
        predicate="builds",
        object="product",
        level=DiltsLevel.BEHAVIOR
    )
    assert spec.level == DiltsLevel.BEHAVIOR


# ============================================================================
# W5H1 Method Tests: has() and need()
# ============================================================================

def test_w5h1_has_dimension():
    """Test has() method for dimension presence."""
    spec = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHO: "user"}
    )
    assert spec.has(Dimension.WHO) is True
    assert spec.has(Dimension.WHAT) is False


def test_w5h1_need_existing_dimension():
    """Test need() returns value for existing dimension."""
    spec = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHO: "user"}
    )
    assert spec.need(Dimension.WHO) == "user"


def test_w5h1_need_missing_dimension():
    """Test need() returns None for missing dimension."""
    spec = W5H1(
        subject="A",
        predicate="B",
        object="C"
    )
    assert spec.need(Dimension.WHO) is None


# ============================================================================
# Critical Test: WHAT→WHY Inheritance Pattern
# ============================================================================

def test_what_becomes_why():
    """
    Test that parent's WHAT can become child's WHY.

    This is the fundamental pattern for purpose propagation:
    parent's WHAT → child's WHY creates semantic chain from
    mission to execution.
    """
    # Parent defines what needs to be built
    parent = W5H1(
        subject="System",
        predicate="needs",
        object="billing",
        dimensions={
            Dimension.WHAT: "Build billing system",
            Dimension.WHO: "Engineering team"
        }
    )

    # Child inherits parent's WHAT as their WHY
    child = W5H1(
        subject="Developer",
        predicate="integrates",
        object="Stripe",
        dimensions={
            Dimension.WHY: parent.need(Dimension.WHAT),  # Purpose inheritance
            Dimension.WHAT: "Integrate Stripe API"
        }
    )

    # Verify the inheritance chain
    assert child.need(Dimension.WHY) == "Build billing system"
    assert child.need(Dimension.WHAT) == "Integrate Stripe API"
    assert parent.need(Dimension.WHAT) == child.need(Dimension.WHY)


def test_multilevel_purpose_propagation():
    """Test purpose propagation through multiple levels."""
    # Level 1: Mission
    mission = W5H1(
        subject="Company",
        predicate="aims",
        object="goal",
        dimensions={Dimension.WHAT: "Dominate SaaS market"}
    )

    # Level 2: Identity (inherits mission's WHAT as WHY)
    identity = W5H1(
        subject="Product",
        predicate="embodies",
        object="values",
        dimensions={
            Dimension.WHY: mission.need(Dimension.WHAT),
            Dimension.WHAT: "Build best-in-class CRM"
        }
    )

    # Level 3: Capability (inherits identity's WHAT as WHY)
    capability = W5H1(
        subject="Team",
        predicate="develops",
        object="features",
        dimensions={
            Dimension.WHY: identity.need(Dimension.WHAT),
            Dimension.WHAT: "Implement contact management"
        }
    )

    # Verify the chain
    assert identity.need(Dimension.WHY) == "Dominate SaaS market"
    assert capability.need(Dimension.WHY) == "Build best-in-class CRM"

    # Chain is preserved: mission → identity → capability
    assert mission.need(Dimension.WHAT) == identity.need(Dimension.WHY)
    assert identity.need(Dimension.WHAT) == capability.need(Dimension.WHY)


# ============================================================================
# W5H1 Method Tests: set() and get_confidence()
# ============================================================================

def test_w5h1_set_with_default_confidence():
    """Test set() with default confidence of 1.0."""
    spec = W5H1(subject="A", predicate="B", object="C")
    spec.set(Dimension.WHO, "user")

    assert spec.need(Dimension.WHO) == "user"
    assert spec.get_confidence(Dimension.WHO) == 1.0


def test_w5h1_set_with_custom_confidence():
    """Test set() with custom confidence score."""
    spec = W5H1(subject="A", predicate="B", object="C")
    spec.set(Dimension.WHO, "Premium users", confidence=0.9)
    spec.set(Dimension.WHAT, "Advanced reporting", confidence=0.6)

    assert spec.get_confidence(Dimension.WHO) == 0.9
    assert spec.get_confidence(Dimension.WHAT) == 0.6


def test_w5h1_set_invalid_confidence():
    """Test set() raises error for invalid confidence."""
    spec = W5H1(subject="A", predicate="B", object="C")

    with pytest.raises(ValueError, match="Confidence must be in"):
        spec.set(Dimension.WHO, "user", confidence=1.5)

    with pytest.raises(ValueError, match="Confidence must be in"):
        spec.set(Dimension.WHO, "user", confidence=-0.1)


def test_w5h1_get_confidence_missing_dimension():
    """Test get_confidence() returns 0.0 for unset dimension."""
    spec = W5H1(subject="A", predicate="B", object="C")
    assert spec.get_confidence(Dimension.WHO) == 0.0


def test_confidence_scores():
    """Test comprehensive confidence tracking."""
    spec = W5H1(
        subject="User",
        predicate="wants",
        object="feature"
    )

    spec.set(Dimension.WHO, "Premium users", confidence=0.9)
    spec.set(Dimension.WHAT, "Advanced reporting", confidence=0.6)

    assert spec.get_confidence(Dimension.WHO) == 0.9
    assert spec.get_confidence(Dimension.WHAT) == 0.6
    assert spec.get_confidence(Dimension.WHY) == 0.0  # Not set


# ============================================================================
# W5H1 Relationship Tests: shared_dimensions() and is_same_system()
# ============================================================================

def test_shared_dimensions_with_overlap():
    """Test shared_dimensions() finds overlapping dimensions."""
    spec1 = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={
            Dimension.WHERE: "store",
            Dimension.WHEN: "today"
        }
    )
    spec2 = W5H1(
        subject="D",
        predicate="E",
        object="F",
        dimensions={
            Dimension.WHERE: "store",
            Dimension.WHO: "user"
        }
    )

    shared = spec1.shared_dimensions(spec2)
    assert shared == {Dimension.WHERE}


def test_shared_dimensions_no_overlap():
    """Test shared_dimensions() with no overlap."""
    spec1 = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHO: "user"}
    )
    spec2 = W5H1(
        subject="D",
        predicate="E",
        object="F",
        dimensions={Dimension.WHAT: "action"}
    )

    shared = spec1.shared_dimensions(spec2)
    assert shared == set()


def test_shared_dimensions_all_overlap():
    """Test shared_dimensions() with complete overlap."""
    dimensions = {
        Dimension.WHO: "user",
        Dimension.WHAT: "action"
    }
    spec1 = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions=dimensions.copy()
    )
    spec2 = W5H1(
        subject="D",
        predicate="E",
        object="F",
        dimensions=dimensions.copy()
    )

    shared = spec1.shared_dimensions(spec2)
    assert shared == {Dimension.WHO, Dimension.WHAT}


def test_same_system_rule():
    """
    Test the "grocery store rule": ≥1 shared dimension = same system.

    This test validates the fundamental grouping mechanism for
    organizing W5H1 objects into systems.
    """
    # Two purchases at the grocery store
    grocery1 = W5H1(
        subject="User",
        predicate="buys",
        object="milk",
        dimensions={
            Dimension.WHERE: "grocery store",
            Dimension.WHEN: "today"
        }
    )
    grocery2 = W5H1(
        subject="User",
        predicate="buys",
        object="bread",
        dimensions={
            Dimension.WHERE: "grocery store",
            Dimension.WHEN: "today"
        }
    )

    # Purchase at hardware store (shares WHERE and WHEN dimensions, different values)
    hardware = W5H1(
        subject="User",
        predicate="buys",
        object="hammer",
        dimensions={
            Dimension.WHERE: "hardware store",
            Dimension.WHEN: "today"
        }
    )

    # Purchase online (shares only WHEN dimension)
    online = W5H1(
        subject="User",
        predicate="buys",
        object="book",
        dimensions={
            Dimension.WHEN: "today",
            Dimension.HOW: "online"
        }
    )

    # Share WHERE + WHEN = same system
    assert grocery1.is_same_system(grocery2)

    # Share WHERE + WHEN dimensions (even with different values) = same system
    assert grocery1.is_same_system(hardware)

    # Share only WHEN = still same system (≥1 dimension)
    assert grocery1.is_same_system(online)

    # Verify shared dimensions
    assert Dimension.WHERE in grocery1.shared_dimensions(grocery2)
    assert Dimension.WHEN in grocery1.shared_dimensions(grocery2)
    assert grocery1.shared_dimensions(hardware) == {Dimension.WHERE, Dimension.WHEN}
    assert grocery1.shared_dimensions(online) == {Dimension.WHEN}


def test_is_same_system_no_overlap():
    """Test is_same_system() returns False when no dimensions shared."""
    spec1 = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHO: "user"}
    )
    spec2 = W5H1(
        subject="D",
        predicate="E",
        object="F",
        dimensions={Dimension.WHAT: "action"}
    )

    assert spec1.is_same_system(spec2) is False


# ============================================================================
# W5H1 Utility Method Tests
# ============================================================================

def test_copy_with_basic():
    """Test copy_with() creates new instance with updates."""
    original = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHO: "user"}
    )

    updated = original.copy_with(object="D")

    assert updated.object == "D"
    assert updated.subject == "A"
    assert updated.predicate == "B"
    assert updated.dimensions == {Dimension.WHO: "user"}

    # Original unchanged
    assert original.object == "C"


def test_copy_with_dimensions():
    """Test copy_with() can update dimensions."""
    original = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHO: "user"}
    )

    updated = original.copy_with(
        dimensions={Dimension.WHO: "admin", Dimension.WHAT: "action"}
    )

    assert updated.dimensions == {
        Dimension.WHO: "admin",
        Dimension.WHAT: "action"
    }
    # Original unchanged
    assert original.dimensions == {Dimension.WHO: "user"}


def test_copy_with_level():
    """Test copy_with() can update level."""
    original = W5H1(
        subject="A",
        predicate="B",
        object="C",
        level=DiltsLevel.BEHAVIOR
    )

    updated = original.copy_with(level=DiltsLevel.CAPABILITY)

    assert updated.level == DiltsLevel.CAPABILITY
    assert original.level == DiltsLevel.BEHAVIOR


def test_required_dimensions_base():
    """Test base W5H1 has no required dimensions."""
    spec = W5H1(subject="A", predicate="B", object="C")
    assert spec.required_dimensions() == set()


def test_is_complete_base():
    """Test base W5H1 is always complete (no requirements)."""
    spec = W5H1(subject="A", predicate="B", object="C")
    assert spec.is_complete() is True


# ============================================================================
# W5H1 Serialization Tests
# ============================================================================

def test_to_dict_minimal():
    """Test to_dict() with minimal W5H1."""
    spec = W5H1(subject="A", predicate="B", object="C")
    data = spec.to_dict()

    assert data['subject'] == "A"
    assert data['predicate'] == "B"
    assert data['object'] == "C"
    assert data['dimensions'] == {}
    assert data['confidence'] == {}
    assert data['level'] is None


def test_to_dict_full():
    """Test to_dict() with complete W5H1."""
    spec = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHO: "user"},
        confidence={Dimension.WHO: 0.9},
        level=DiltsLevel.BEHAVIOR
    )
    data = spec.to_dict()

    assert data['subject'] == "A"
    assert data['dimensions'] == {"who": "user"}
    assert data['confidence'] == {"who": 0.9}
    assert data['level'] == 2


def test_from_dict_minimal():
    """Test from_dict() with minimal data."""
    data = {
        'subject': 'A',
        'predicate': 'B',
        'object': 'C',
        'dimensions': {},
        'confidence': {},
        'level': None
    }
    spec = W5H1.from_dict(data)

    assert spec.subject == "A"
    assert spec.predicate == "B"
    assert spec.object == "C"
    assert spec.dimensions == {}
    assert spec.level is None


def test_from_dict_full():
    """Test from_dict() with complete data."""
    data = {
        'subject': 'A',
        'predicate': 'B',
        'object': 'C',
        'dimensions': {'who': 'user', 'what': 'action'},
        'confidence': {'who': 0.9},
        'level': 2
    }
    spec = W5H1.from_dict(data)

    assert spec.subject == "A"
    assert spec.need(Dimension.WHO) == "user"
    assert spec.need(Dimension.WHAT) == "action"
    assert spec.get_confidence(Dimension.WHO) == 0.9
    assert spec.level == DiltsLevel.BEHAVIOR


def test_serialization_round_trip():
    """Test that to_dict() → from_dict() preserves data."""
    original = W5H1(
        subject="User",
        predicate="wants",
        object="feature",
        dimensions={
            Dimension.WHO: "Premium users",
            Dimension.WHAT: "Advanced reporting"
        },
        confidence={
            Dimension.WHO: 0.9,
            Dimension.WHAT: 0.7
        },
        level=DiltsLevel.CAPABILITY
    )

    # Serialize and deserialize
    data = original.to_dict()
    restored = W5H1.from_dict(data)

    # Verify all data preserved
    assert restored.subject == original.subject
    assert restored.predicate == original.predicate
    assert restored.object == original.object
    assert restored.dimensions == original.dimensions
    assert restored.confidence == original.confidence
    assert restored.level == original.level


# ============================================================================
# CommitW5H1 Specialized Subclass Tests
# ============================================================================

def test_commit_w5h1_required_dimensions():
    """Test CommitW5H1 requires WHY and HOW."""
    commit = CommitW5H1(
        subject="Developer",
        predicate="implements",
        object="feature"
    )
    assert commit.required_dimensions() == {Dimension.WHY, Dimension.HOW}


def test_commit_w5h1_is_complete_false():
    """Test CommitW5H1 is incomplete without WHY and HOW."""
    commit = CommitW5H1(
        subject="Developer",
        predicate="implements",
        object="feature",
        dimensions={Dimension.WHY: "Add authentication"}
    )
    assert commit.is_complete() is False


def test_commit_w5h1_is_complete_true():
    """Test CommitW5H1 is complete with WHY and HOW."""
    commit = CommitW5H1(
        subject="Developer",
        predicate="implements",
        object="feature",
        dimensions={
            Dimension.WHY: "Add user authentication",
            Dimension.HOW: "Using OAuth2 with JWT tokens"
        }
    )
    assert commit.is_complete() is True


def test_commit_w5h1_inherits_w5h1_methods():
    """Test CommitW5H1 inherits all W5H1 methods."""
    commit = CommitW5H1(
        subject="Dev",
        predicate="codes",
        object="feature"
    )

    # Test need()
    commit.set(Dimension.WHY, "purpose")
    assert commit.need(Dimension.WHY) == "purpose"

    # Test has()
    assert commit.has(Dimension.WHY) is True
    assert commit.has(Dimension.WHAT) is False


# ============================================================================
# SpecW5H1 Specialized Subclass Tests
# ============================================================================

def test_spec_w5h1_required_dimensions():
    """Test SpecW5H1 requires WHO, WHAT, and WHY."""
    spec = SpecW5H1(
        subject="System",
        predicate="provides",
        object="feature"
    )
    assert spec.required_dimensions() == {
        Dimension.WHO,
        Dimension.WHAT,
        Dimension.WHY
    }


def test_spec_w5h1_is_complete_false():
    """Test SpecW5H1 is incomplete without all required dimensions."""
    spec = SpecW5H1(
        subject="System",
        predicate="provides",
        object="feature",
        dimensions={
            Dimension.WHO: "Users",
            Dimension.WHAT: "Login"
        }
    )
    assert spec.is_complete() is False


def test_spec_w5h1_is_complete_true():
    """Test SpecW5H1 is complete with WHO, WHAT, and WHY."""
    spec = SpecW5H1(
        subject="System",
        predicate="provides",
        object="authentication",
        dimensions={
            Dimension.WHO: "End users",
            Dimension.WHAT: "Secure login system",
            Dimension.WHY: "Protect user data"
        }
    )
    assert spec.is_complete() is True


def test_spec_w5h1_inherits_w5h1_methods():
    """Test SpecW5H1 inherits all W5H1 methods."""
    spec = SpecW5H1(
        subject="System",
        predicate="does",
        object="thing"
    )

    # Test serialization
    spec.set(Dimension.WHO, "user")
    data = spec.to_dict()
    assert data['dimensions'] == {"who": "user"}


# ============================================================================
# BaseActor Abstract Class Tests
# ============================================================================

def test_base_actor_is_abstract():
    """Test that BaseActor cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseActor("TestActor")


def test_base_actor_implementation():
    """Test concrete implementation of BaseActor."""
    class SimpleActor(BaseActor):
        def understand(self, spec: W5H1) -> bool:
            return spec.has(Dimension.WHAT)

        def execute(self, spec: W5H1) -> str:
            return f"Executing: {spec.need(Dimension.WHAT)}"

    actor = SimpleActor("TestActor")
    assert actor.name == "TestActor"
    assert actor.context == {}


def test_base_actor_understand():
    """Test understand() method in concrete implementation."""
    class SimpleActor(BaseActor):
        def understand(self, spec: W5H1) -> bool:
            return spec.has(Dimension.WHAT)

        def execute(self, spec: W5H1) -> str:
            return "executed"

    actor = SimpleActor("TestActor")

    spec_with_what = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHAT: "task"}
    )
    spec_without_what = W5H1(
        subject="A",
        predicate="B",
        object="C"
    )

    assert actor.understand(spec_with_what) is True
    assert actor.understand(spec_without_what) is False


def test_base_actor_execute():
    """Test execute() method in concrete implementation."""
    class SimpleActor(BaseActor):
        def understand(self, spec: W5H1) -> bool:
            return True

        def execute(self, spec: W5H1) -> str:
            return f"Executing: {spec.need(Dimension.WHAT)}"

    actor = SimpleActor("TestActor")
    spec = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHAT: "build feature"}
    )

    result = actor.execute(spec)
    assert result == "Executing: build feature"


def test_base_actor_context():
    """Test that actors can maintain dimensional context."""
    class ContextualActor(BaseActor):
        def understand(self, spec: W5H1) -> bool:
            return True

        def execute(self, spec: W5H1) -> None:
            # Store dimension in context
            if spec.has(Dimension.WHO):
                self.context[Dimension.WHO] = spec.need(Dimension.WHO)

    actor = ContextualActor("ContextActor")
    spec = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHO: "user"}
    )

    actor.execute(spec)
    assert actor.context[Dimension.WHO] == "user"


# ============================================================================
# Edge Cases and Error Handling Tests
# ============================================================================

def test_w5h1_empty_dimensions():
    """Test W5H1 handles empty dimensions gracefully."""
    spec = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={}
    )
    assert spec.need(Dimension.WHO) is None
    assert spec.has(Dimension.WHO) is False
    assert spec.required_dimensions() == set()
    assert spec.is_complete() is True


def test_w5h1_none_values():
    """Test W5H1 behavior with None dimension values."""
    spec = W5H1(subject="A", predicate="B", object="C")

    # Need returns None for unset dimension
    assert spec.need(Dimension.WHO) is None

    # Has returns False for unset dimension
    assert spec.has(Dimension.WHO) is False


def test_dimension_overwrite():
    """Test that setting a dimension twice overwrites the first value."""
    spec = W5H1(subject="A", predicate="B", object="C")

    spec.set(Dimension.WHO, "user1", confidence=0.5)
    assert spec.need(Dimension.WHO) == "user1"
    assert spec.get_confidence(Dimension.WHO) == 0.5

    spec.set(Dimension.WHO, "user2", confidence=0.9)
    assert spec.need(Dimension.WHO) == "user2"
    assert spec.get_confidence(Dimension.WHO) == 0.9


def test_confidence_boundary_values():
    """Test confidence accepts boundary values 0.0 and 1.0."""
    spec = W5H1(subject="A", predicate="B", object="C")

    spec.set(Dimension.WHO, "user1", confidence=0.0)
    assert spec.get_confidence(Dimension.WHO) == 0.0

    spec.set(Dimension.WHAT, "action", confidence=1.0)
    assert spec.get_confidence(Dimension.WHAT) == 1.0


def test_shared_dimensions_empty_specs():
    """Test shared_dimensions() with empty dimension dicts."""
    spec1 = W5H1(subject="A", predicate="B", object="C")
    spec2 = W5H1(subject="D", predicate="E", object="F")

    assert spec1.shared_dimensions(spec2) == set()
    assert spec1.is_same_system(spec2) is False


def test_copy_with_no_updates():
    """Test copy_with() with no updates creates identical copy."""
    original = W5H1(
        subject="A",
        predicate="B",
        object="C",
        dimensions={Dimension.WHO: "user"}
    )

    copy = original.copy_with()

    assert copy.subject == original.subject
    assert copy.predicate == original.predicate
    assert copy.object == original.object
    assert copy.dimensions == original.dimensions

    # But they're different objects
    assert copy is not original


def test_from_dict_missing_optional_fields():
    """Test from_dict() handles missing optional fields."""
    data = {
        'subject': 'A',
        'predicate': 'B',
        'object': 'C'
    }
    spec = W5H1.from_dict(data)

    assert spec.dimensions == {}
    assert spec.confidence == {}
    assert spec.level is None