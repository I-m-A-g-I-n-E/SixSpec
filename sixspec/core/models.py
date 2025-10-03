"""
Core data structures for the SixSpec framework.

This module implements the fundamental building blocks for six-dimensional
specifications using the W5H1 model (WHO, WHAT, WHEN, WHERE, HOW, WHY)
combined with Dilts' Logical Levels.

Key Concepts:
    - Dimension: The six dimensions of specification
    - DiltsLevel: Hierarchical levels from Environment to Mission
    - W5H1: Universal container for dimensional specifications
    - Purpose Propagation: Parent's WHAT becomes child's WHY

Example:
    >>> from sixspec.core.models import W5H1, Dimension
    >>> parent = W5H1(
    ...     subject="System",
    ...     predicate="needs",
    ...     object="billing",
    ...     dimensions={Dimension.WHAT: "Build billing system"}
    ... )
    >>> child = W5H1(
    ...     subject="Developer",
    ...     predicate="integrates",
    ...     object="Stripe",
    ...     dimensions={
    ...         Dimension.WHY: parent.need(Dimension.WHAT),
    ...         Dimension.WHAT: "Integrate Stripe API"
    ...     }
    ... )
    >>> child.need(Dimension.WHY)
    'Build billing system'
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Set


class Dimension(Enum):
    """
    The six dimensions of specification (W5H1 model).

    These dimensions provide a complete framework for describing any
    specification, action, or context:
    - WHO: Actors, stakeholders, agents
    - WHAT: Actions, objects, results
    - WHEN: Temporal context, timing
    - WHERE: Spatial context, location
    - HOW: Methods, processes, implementation
    - WHY: Purpose, motivation, goals
    """
    WHO = "who"
    WHAT = "what"
    WHEN = "when"
    WHERE = "where"
    HOW = "how"
    WHY = "why"

class DiltsLevel(Enum): 
    """
    Dilts' Logical Levels for hierarchical organization.

    Each level represents a different scope of autonomy and abstraction,
    from concrete environment to abstract mission. Higher levels have
    greater autonomy and influence over lower levels.

    Levels (from highest to lowest):
    - MISSION (6): FOR WHAT - Extreme autonomy, purpose and vision
    - IDENTITY (5): WHO we are - High autonomy, core values
    - BELIEFS (4): WHY we choose - Moderate autonomy, principles
    - CAPABILITY (3): HOW we operate - Low autonomy, skills
    - BEHAVIOR (2): WHAT we do - Very low autonomy, actions
    - ENVIRONMENT (1): WHERE/WHEN - Zero autonomy, context
    """
    MISSION = 6
    IDENTITY = 5
    BELIEFS = 4
    CAPABILITY = 3
    BEHAVIOR = 2
    ENVIRONMENT = 1

    @property
    def primary_dimensions(self) -> Set[Dimension]:
        """
        Returns the primary dimensions emphasized at this level.

        Each Dilts level naturally emphasizes certain dimensions:
        - MISSION: FOR WHAT (purpose)
        - IDENTITY: WHO (self-concept)
        - BELIEFS: WHY (values and principles)
        - CAPABILITY: HOW (skills and methods)
        - BEHAVIOR: WHAT (actions and results)
        - ENVIRONMENT: WHERE, WHEN (context)

        Returns:
            Set of Dimension enums representing primary dimensions
        """
        mapping = {
            DiltsLevel.MISSION: {Dimension.WHY},
            DiltsLevel.IDENTITY: {Dimension.WHO},
            DiltsLevel.BELIEFS: {Dimension.WHY},
            DiltsLevel.CAPABILITY: {Dimension.HOW},
            DiltsLevel.BEHAVIOR: {Dimension.WHAT},
            DiltsLevel.ENVIRONMENT: {Dimension.WHERE, Dimension.WHEN},
        }
        return mapping[self]

    @property
    def autonomy(self) -> str:
        """
        Returns the autonomy level as a string.

        Higher levels have more autonomy in decision-making and influence:
        - extreme: Can redefine entire purpose
        - high: Can redefine identity and values
        - moderate: Can choose approaches based on beliefs
        - low: Can select methods within constraints
        - very_low: Can only execute defined behaviors
        - zero: Cannot change environmental constraints

        Returns:
            String describing autonomy level
        """
        mapping = {
            DiltsLevel.MISSION: "extreme",
            DiltsLevel.IDENTITY: "high",
            DiltsLevel.BELIEFS: "moderate",
            DiltsLevel.CAPABILITY: "low",
            DiltsLevel.BEHAVIOR: "very_low",
            DiltsLevel.ENVIRONMENT: "zero",
        }
        return mapping[self]

L = DiltsLevel # convenience alias
D = Dimension # convenience alias


@dataclass
class W5H1:
    """
    Six-dimensional specification object (W5H1 model).

    W5H1 is the universal container for specifications, combining:
    - Subject-predicate-object triple (RDF-style)
    - Six dimensions (WHO/WHAT/WHEN/WHERE/HOW/WHY)
    - Per-dimension confidence scores
    - Optional Dilts level assignment

    Key Design Principles:
    1. Lazy evaluation: Use need() to fetch dimensions on-demand
    2. Purpose propagation: Parent's WHAT becomes child's WHY
    3. Confidence tracking: Per-dimension confidence scores
    4. Context specialization: Subclasses for specific contexts

    Attributes:
        subject: The subject of the specification
        predicate: The relationship or action
        object: The object or result
        dimensions: Dictionary mapping Dimension to string values
        confidence: Dictionary mapping Dimension to confidence scores (0.0-1.0)
        level: Optional Dilts level assignment

    Example:
        >>> spec = W5H1(
        ...     subject="User",
        ...     predicate="wants",
        ...     object="feature"
        ... )
        >>> spec.set(Dimension.WHO, "Premium users", confidence=0.9)
        >>> spec.set(Dimension.WHAT, "Advanced reporting", confidence=0.6)
        >>> spec.need(Dimension.WHO)
        'Premium users'
        >>> spec.get_confidence(Dimension.WHO)
        0.9
    """
    subject: str
    predicate: str
    object: str
    dimensions: Dict[Dimension, str] = field(default_factory=dict)
    confidence: Dict[Dimension, float] = field(default_factory=dict)
    level: Optional[DiltsLevel] = None

    def has(self, dim: Dimension) -> bool:
        """
        Check if a dimension is set.

        Args:
            dim: The dimension to check

        Returns:
            True if dimension is set, False otherwise
        """
        return dim in self.dimensions

    def need(self, dim: Dimension) -> Optional[str]:
        """
        Demand-driven dimension fetch.

        This method enables lazy evaluation and purpose propagation.
        Returns None if the dimension is not set, allowing callers
        to handle missing dimensions gracefully.

        Args:
            dim: The dimension to fetch

        Returns:
            The dimension value if set, None otherwise

        Example:
            >>> parent = W5H1(
            ...     subject="System", predicate="needs", object="billing",
            ...     dimensions={Dimension.WHAT: "Build billing system"}
            ... )
            >>> child = W5H1(
            ...     subject="Dev", predicate="codes", object="integration",
            ...     dimensions={Dimension.WHY: parent.need(Dimension.WHAT)}
            ... )
            >>> child.need(Dimension.WHY)
            'Build billing system'
        """
        return self.dimensions.get(dim)

    def set(self, dim: Dimension, value: str, confidence: float = 1.0) -> None:
        """
        Set a dimension value with optional confidence score.

        Args:
            dim: The dimension to set
            value: The dimension value
            confidence: Confidence score (0.0-1.0), defaults to 1.0

        Raises:
            ValueError: If confidence is not in range [0.0, 1.0]

        Example:
            >>> spec = W5H1(subject="A", predicate="B", object="C")
            >>> spec.set(Dimension.WHO, "Users", confidence=0.8)
        """
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"Confidence must be in [0.0, 1.0], got {confidence}")
        self.dimensions[dim] = value
        self.confidence[dim] = confidence

    def get_confidence(self, dim: Dimension) -> float:
        """
        Get the confidence score for a dimension.

        Args:
            dim: The dimension to query

        Returns:
            Confidence score (0.0-1.0), or 0.0 if dimension not set
        """
        return self.confidence.get(dim, 0.0)

    def shared_dimensions(self, other: 'W5H1') -> Set[Dimension]:
        """
        Find dimensions shared with another W5H1 object.

        Two dimensions are "shared" if both objects have them set,
        regardless of whether the values are identical.

        Args:
            other: Another W5H1 object to compare with

        Returns:
            Set of dimensions present in both objects

        Example:
            >>> spec1 = W5H1("A", "B", "C", dimensions={
            ...     Dimension.WHERE: "store",
            ...     Dimension.WHEN: "today"
            ... })
            >>> spec2 = W5H1("D", "E", "F", dimensions={
            ...     Dimension.WHERE: "store",
            ...     Dimension.WHO: "user"
            ... })
            >>> spec1.shared_dimensions(spec2)
            {<Dimension.WHERE: 'where'>}
        """
        return set(self.dimensions.keys()) & set(other.dimensions.keys())

    def is_same_system(self, other: 'W5H1') -> bool:
        """
        Check if two objects belong to the same system.

        The "grocery store rule": Two objects belong to the same system
        if they share at least one dimension (≥1 shared dimension).

        This enables grouping and organization based on any dimensional
        overlap, not requiring complete alignment.

        Args:
            other: Another W5H1 object to compare with

        Returns:
            True if objects share ≥1 dimension, False otherwise

        Example:
            >>> milk = W5H1("User", "buys", "milk", dimensions={
            ...     Dimension.WHERE: "grocery store"
            ... })
            >>> bread = W5H1("User", "buys", "bread", dimensions={
            ...     Dimension.WHERE: "grocery store"
            ... })
            >>> hammer = W5H1("User", "buys", "hammer", dimensions={
            ...     Dimension.WHERE: "hardware store"
            ... })
            >>> milk.is_same_system(bread)  # Same store
            True
            >>> milk.is_same_system(hammer)  # Different store
            False
        """
        return len(self.shared_dimensions(other)) >= 1

    def copy_with(self, **updates) -> 'W5H1':
        """
        Create a copy with specified updates.

        This method enables immutable-style updates while preserving
        all other attributes. Useful for creating variants of a spec.

        Args:
            **updates: Keyword arguments for attributes to update

        Returns:
            New W5H1 instance with updates applied

        Example:
            >>> original = W5H1("A", "B", "C", dimensions={
            ...     Dimension.WHO: "user"
            ... })
            >>> variant = original.copy_with(
            ...     object="D",
            ...     dimensions={Dimension.WHO: "admin"}
            ... )
            >>> variant.object
            'D'
        """
        # Create copies of mutable defaults
        new_dimensions = self.dimensions.copy()
        new_confidence = self.confidence.copy()

        # Apply updates
        if 'dimensions' in updates:
            new_dimensions = updates.pop('dimensions')
        if 'confidence' in updates:
            new_confidence = updates.pop('confidence')

        return W5H1(
            subject=updates.get('subject', self.subject),
            predicate=updates.get('predicate', self.predicate),
            object=updates.get('object', self.object),
            dimensions=new_dimensions,
            confidence=new_confidence,
            level=updates.get('level', self.level),
        )

    def required_dimensions(self) -> Set[Dimension]:
        """
        Get the set of required dimensions for this object.

        Base W5H1 has no strict requirements - subclasses can override
        to enforce specific dimensional requirements.

        Returns:
            Set of required Dimension enums (empty for base class)
        """
        return set()

    def is_complete(self) -> bool:
        """
        Check if all required dimensions are set.

        Returns:
            True if all required dimensions are present, False otherwise

        Example:
            >>> spec = SpecW5H1("A", "B", "C")
            >>> spec.is_complete()
            False
            >>> spec.set(Dimension.WHO, "user")
            >>> spec.set(Dimension.WHAT, "action")
            >>> spec.set(Dimension.WHY, "purpose")
            >>> spec.is_complete()
            True
        """
        required = self.required_dimensions()
        return required.issubset(self.dimensions.keys())

    def to_dict(self) -> dict:
        """
        Serialize to dictionary format.

        Returns:
            Dictionary representation suitable for JSON serialization

        Example:
            >>> spec = W5H1("A", "B", "C", dimensions={
            ...     Dimension.WHO: "user"
            ... })
            >>> spec.to_dict()
            {'subject': 'A', 'predicate': 'B', 'object': 'C', ...}
        """
        return {
            'subject': self.subject,
            'predicate': self.predicate,
            'object': self.object,
            'dimensions': {dim.value: val for dim, val in self.dimensions.items()},
            'confidence': {dim.value: conf for dim, conf in self.confidence.items()},
            'level': self.level.value if self.level else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'W5H1':
        """
        Deserialize from dictionary format.

        Args:
            data: Dictionary representation (from to_dict())

        Returns:
            New W5H1 instance reconstructed from dictionary

        Example:
            >>> data = {
            ...     'subject': 'A', 'predicate': 'B', 'object': 'C',
            ...     'dimensions': {'who': 'user'},
            ...     'confidence': {'who': 0.9},
            ...     'level': None
            ... }
            >>> spec = W5H1.from_dict(data)
            >>> spec.need(Dimension.WHO)
            'user'
        """
        dimensions = {
            Dimension(k): v for k, v in data.get('dimensions', {}).items()
        }
        confidence = {
            Dimension(k): v for k, v in data.get('confidence', {}).items()
        }
        level = DiltsLevel(data['level']) if data.get('level') else None

        return cls(
            subject=data['subject'],
            predicate=data['predicate'],
            object=data['object'],
            dimensions=dimensions,
            confidence=confidence,
            level=level,
        )


class CommitW5H1(W5H1):
    """
    Specialized W5H1 for git commits.

    Git commits require dimensional documentation to create
    self-documenting version history:
    - WHY: Purpose of the change (inherits from parent's WHAT)
    - HOW: Implementation approach

    Example:
        >>> commit = CommitW5H1(
        ...     subject="Developer",
        ...     predicate="implements",
        ...     object="feature",
        ...     dimensions={
        ...         Dimension.WHY: "Add user authentication",
        ...         Dimension.HOW: "Using OAuth2 with JWT tokens"
        ...     }
        ... )
        >>> commit.is_complete()
        True
    """

    def required_dimensions(self) -> Set[Dimension]:
        """Git commits require WHY and HOW dimensions."""
        return {Dimension.WHY, Dimension.HOW}


class SpecW5H1(W5H1):
    """
    Specialized W5H1 for full specifications.

    Full specifications should identify the actors, actions, and
    purpose at minimum:
    - WHO: Stakeholders and actors
    - WHAT: The specification or requirement
    - WHY: Purpose and motivation

    Example:
        >>> spec = SpecW5H1(
        ...     subject="System",
        ...     predicate="provides",
        ...     object="authentication",
        ...     dimensions={
        ...         Dimension.WHO: "End users",
        ...         Dimension.WHAT: "Secure login system",
        ...         Dimension.WHY: "Protect user data"
        ...     }
        ... )
        >>> spec.is_complete()
        True
    """

    def required_dimensions(self) -> Set[Dimension]:
        """Full specs require WHO, WHAT, and WHY dimensions."""
        return {Dimension.WHO, Dimension.WHAT, Dimension.WHY}


class BaseActor(ABC):
    """
    Abstract base class for entities that understand dimensions.

    Actors are entities that can process and execute specifications.
    They maintain dimensional context and can understand and execute
    W5H1 specifications.

    Three types of actors will implement this interface:
    - Human actors: Manual execution with dimensional awareness
    - AI agents: Autonomous execution with dimensional reasoning
    - System actors: Automated execution with dimensional logging

    Attributes:
        name: Identifier for this actor
        context: Dimensional context maintained by this actor

    Example:
        >>> class SimpleActor(BaseActor):
        ...     def understand(self, spec):
        ...         return spec.has(Dimension.WHAT)
        ...     def execute(self, spec):
        ...         return f"Executing: {spec.need(Dimension.WHAT)}"
        >>> actor = SimpleActor("TestActor")
        >>> spec = W5H1("A", "B", "C", dimensions={
        ...     Dimension.WHAT: "task"
        ... })
        >>> actor.understand(spec)
        True
        >>> actor.execute(spec)
        'Executing: task'
    """

    def __init__(self, name: str):
        """
        Initialize an actor.

        Args:
            name: Identifier for this actor
        """
        self.name = name
        self.context: Dict[Dimension, Any] = {}

    @abstractmethod
    def understand(self, spec: W5H1) -> bool:
        """
        Check if this actor can process the given specification.

        Actors should examine the spec's dimensions and determine
        if they have the capability to execute it.

        Args:
            spec: W5H1 specification to evaluate

        Returns:
            True if actor can process this spec, False otherwise
        """
        pass

    @abstractmethod
    def execute(self, spec: W5H1) -> Any:
        """
        Execute based on specification.

        Actors implement this to perform actions defined in the spec.
        The return value depends on the actor type and specification.

        Args:
            spec: W5H1 specification to execute

        Returns:
            Result of execution (type varies by actor and spec)
        """
        pass