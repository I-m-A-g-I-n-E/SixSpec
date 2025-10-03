"""
Capability Strategy: Level 3 walker with low autonomy.

Capability-level walkers operate at the HOW level with low autonomy.
They can:
- Select methods within constraints
- Choose implementation approaches
- Combine existing capabilities
- Optimize processes

Most walkers start at Capability level (L3).

Example:
    >>> walker = CapabilityWalker()
    >>> spec = Chunk(
    ...     subject="System",
    ...     predicate="needs",
    ...     object="payment",
    ...     dimensions={
    ...         Dimension.WHAT: "Integrate payment processing",
    ...         Dimension.WHY: "Enable premium tier"
    ...     }
    ... )
    >>> strategies = walker.generate_strategies(spec, 3)
    >>> len(strategies)
    3
"""

from typing import Any, List, Optional

from sixspec.core.models import Dimension, DiltsLevel, Chunk
from sixspec.walkers.dilts_walker import DiltsWalker, ValidationResult


class CapabilityWalker(DiltsWalker):
    """
    Walker for Capability level (L3) - Low autonomy.

    Capability walkers operate at HOW level:
    - Can select methods within constraints
    - Choose from known implementation patterns
    - Combine existing capabilities
    - Focus on technical implementation

    This is where most walkers start execution, as it represents
    the typical starting point for technical work.

    Autonomy: LOW
    Primary Dimension: HOW (methods)

    Example:
        >>> walker = CapabilityWalker()
        >>> walker.level
        <DiltsLevel.CAPABILITY: 3>
        >>> walker.level.autonomy
        'low'
    """

    def __init__(self, parent: Optional[DiltsWalker] = None):
        """
        Initialize a Capability-level walker.

        Args:
            parent: Optional parent walker (typically Beliefs level)
        """
        super().__init__(level=DiltsLevel.CAPABILITY, parent=parent)

    def generate_strategies(self, spec: Chunk, n: int) -> List[str]:
        """
        Generate n different implementation approaches.

        Capability-level strategies are different technical approaches
        to implementing the same goal. They represent different HOW
        methods within established constraints.

        Args:
            spec: Specification with capability goal
            n: Number of strategies to generate

        Returns:
            List of implementation approaches (WHAT values)

        Example:
            >>> walker = CapabilityWalker()
            >>> spec = Chunk(
            ...     subject="System",
            ...     predicate="needs",
            ...     object="auth",
            ...     dimensions={
            ...         Dimension.WHAT: "Implement authentication",
            ...         Dimension.WHY: "Secure user access"
            ...     }
            ... )
            >>> strategies = walker.generate_strategies(spec, 3)
            >>> len(strategies)
            3
            >>> all(isinstance(s, str) for s in strategies)
            True
        """
        base_what = spec.need(Dimension.WHAT) or "implement capability"

        # Capability-level strategies are different technical approaches
        # These examples show common patterns at the HOW level
        templates = [
            f"{base_what} using standard library",
            f"{base_what} using third-party service",
            f"{base_what} using custom implementation",
            f"{base_what} using existing framework",
            f"{base_what} using microservice pattern",
            f"{base_what} using monolithic approach",
            f"{base_what} using serverless functions",
            f"{base_what} using event-driven architecture",
        ]

        # Return first n strategies
        return templates[:n] if n <= len(templates) else templates + [
            f"{base_what} - Alternative approach {i}"
            for i in range(len(templates), n)
        ]

    def validate(self, result: Any) -> ValidationResult:
        """
        Validate capability-level execution result.

        Capability validation checks:
        - Did implementation complete?
        - Is there a concrete result?
        - Does approach work?

        Args:
            result: Result from execution

        Returns:
            ValidationResult with score and details

        Example:
            >>> walker = CapabilityWalker()
            >>> result = "EXECUTED: Implementation approach"
            >>> validation = walker.validate(result)
            >>> validation.passed
            True
            >>> validation.score > 0
            True
        """
        if result is None:
            return ValidationResult(
                score=0.0,
                passed=False,
                details="No result returned"
            )

        # Capability validation checks if implementation worked
        result_str = str(result)
        if "EXECUTED" in result_str:
            # Check if there's a reason (WHY) in the result
            if "because:" in result_str:
                return ValidationResult(
                    score=1.0,
                    passed=True,
                    details="Implementation executed with full context"
                )
            else:
                return ValidationResult(
                    score=0.8,
                    passed=True,
                    details="Implementation executed"
                )
        elif result_str:
            return ValidationResult(
                score=0.6,
                passed=True,
                details="Implementation completed with result"
            )
        else:
            return ValidationResult(
                score=0.1,
                passed=False,
                details="Empty result"
            )