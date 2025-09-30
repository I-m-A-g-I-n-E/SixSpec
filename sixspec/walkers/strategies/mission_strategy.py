"""
Mission Strategy: Level 6 walker with extreme autonomy.

Mission-level walkers operate at the highest level of abstraction with
extreme autonomy. They can:
- Redefine entire purpose
- Choose fundamentally different approaches
- Make strategic decisions
- Set organizational direction

Example:
    >>> walker = MissionWalker()
    >>> spec = W5H1(
    ...     subject="Company",
    ...     predicate="needs",
    ...     object="growth",
    ...     dimensions={Dimension.WHAT: "Increase market share"}
    ... )
    >>> strategies = walker.generate_strategies(spec, 3)
    >>> len(strategies)
    3
"""

from typing import Any, List

from sixspec.core.models import Dimension, DiltsLevel, W5H1
from sixspec.walkers.dilts_walker import DiltsWalker, ValidationResult


class MissionWalker(DiltsWalker):
    """
    Walker for Mission level (L6) - Extreme autonomy.

    Mission walkers operate at FOR WHAT level:
    - Can redefine entire purpose
    - Generate fundamentally different strategic approaches
    - No constraints except physical/legal reality
    - Focus on long-term vision and impact

    Autonomy: EXTREME
    Primary Dimension: WHY (purpose)

    Example:
        >>> walker = MissionWalker()
        >>> walker.level
        <DiltsLevel.MISSION: 6>
        >>> walker.level.autonomy
        'extreme'
    """

    def __init__(self, parent: DiltsWalker = None):
        """
        Initialize a Mission-level walker.

        Args:
            parent: Optional parent walker (should be None for Mission)
        """
        super().__init__(level=DiltsLevel.MISSION, parent=parent)

    def generate_strategies(self, spec: W5H1, n: int) -> List[str]:
        """
        Generate n radically different strategic approaches.

        Mission-level strategies are fundamentally different paths
        to achieving the same ultimate purpose. They represent
        different visions of what success looks like.

        Args:
            spec: Specification with mission goal
            n: Number of strategies to generate

        Returns:
            List of strategic approaches (WHAT values)

        Example:
            >>> walker = MissionWalker()
            >>> spec = W5H1(
            ...     subject="Company",
            ...     predicate="aims to",
            ...     object="growth",
            ...     dimensions={Dimension.WHAT: "Grow revenue"}
            ... )
            >>> strategies = walker.generate_strategies(spec, 3)
            >>> len(strategies)
            3
            >>> all(isinstance(s, str) for s in strategies)
            True
        """
        base_what = spec.need(Dimension.WHAT) or "achieve mission"

        # Mission-level strategies are radically different approaches
        # These are just examples - real implementation would use
        # sophisticated reasoning to generate strategic options
        templates = [
            f"{base_what} through organic growth",
            f"{base_what} through acquisition strategy",
            f"{base_what} through market expansion",
            f"{base_what} through product innovation",
            f"{base_what} through operational excellence",
            f"{base_what} through partnership ecosystem",
            f"{base_what} through vertical integration",
            f"{base_what} through platform approach",
        ]

        # Return first n strategies
        return templates[:n] if n <= len(templates) else templates + [
            f"{base_what} - Alternative strategy {i}"
            for i in range(len(templates), n)
        ]

    def validate(self, result: Any) -> ValidationResult:
        """
        Validate mission-level execution result.

        Mission validation checks:
        - Did execution complete?
        - Is there a concrete result?
        - Does result align with purpose?

        Args:
            result: Result from execution

        Returns:
            ValidationResult with score and details

        Example:
            >>> walker = MissionWalker()
            >>> result = "EXECUTED: Strategy implementation"
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

        # Simple validation: non-empty result passes
        # Real implementation would check against mission criteria
        result_str = str(result)
        if "EXECUTED" in result_str:
            return ValidationResult(
                score=0.9,
                passed=True,
                details="Mission strategy executed successfully"
            )
        elif result_str:
            return ValidationResult(
                score=0.7,
                passed=True,
                details="Strategy completed with result"
            )
        else:
            return ValidationResult(
                score=0.1,
                passed=False,
                details="Empty result"
            )