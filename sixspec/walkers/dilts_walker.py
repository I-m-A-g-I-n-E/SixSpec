"""
DiltsWalker: Hierarchical walker with WHAT→WHY purpose propagation.

This module implements the core SixSpec execution model using Dilts'
Logical Levels for hierarchical delegation with purpose propagation.

Core Pattern:
    Parent's WHAT becomes child's WHY

This enables:
- Self-documenting execution (every walker knows its purpose)
- Full traceability (trace_provenance() returns full WHY chain)
- Explainable AI (why did system do X? follow WHAT→WHY chain)
- Graceful interruption with context (pause preserves meaning)
- Dynamic re-planning (same WHY, different WHAT)

Example:
    >>> mission = DiltsWalker(level=DiltsLevel.MISSION)
    >>> spec = W5H1(
    ...     subject="Company",
    ...     predicate="needs",
    ...     object="revenue",
    ...     dimensions={Dimension.WHAT: "Increase revenue"}
    ... )
    >>> result = mission.execute(spec)
    >>> len(mission.children) > 0  # Spawned children
    True
"""

import uuid
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from sixspec.agents.graph_agent import GraphAgent
from sixspec.core.models import Dimension, DiltsLevel, W5H1
from sixspec.walkers.workspace import Workspace


@dataclass
class ValidationResult:
    """
    Result of validating an execution outcome.

    Used by portfolio execution to select the best strategy
    based on actual results, not predicted confidence.

    Attributes:
        score: Validation score (higher is better)
        passed: Whether validation passed minimum threshold
        details: Additional validation details

    Example:
        >>> result = ValidationResult(score=0.9, passed=True, details="All tests passed")
        >>> result.score
        0.9
    """
    score: float
    passed: bool
    details: str = ""


class DiltsWalker(GraphAgent):
    """
    Walker that traverses Dilts hierarchy with WHAT→WHY propagation.

    This is the core SixSpec execution model. DiltsWalker extends
    GraphAgent because walkers need to:
    - Traverse relationships between specs
    - Gather context from neighbors
    - Understand dimensional connections

    Key Features:
    - Hierarchical delegation from Mission (L6) to Environment (L1)
    - Automatic WHAT→WHY propagation from parent to child
    - Portfolio execution (spawn multiple strategies, pick winner)
    - Full provenance tracing
    - Workspace isolation per walker

    The Six Levels:
        Level 6 (MISSION):       FOR WHAT - Extreme autonomy, strategic
        Level 5 (IDENTITY):      WHO we are - High autonomy, product definition
        Level 4 (BELIEFS):       WHY we choose - Moderate autonomy, choices
        Level 3 (CAPABILITY):    HOW we operate - Low autonomy, most start here
        Level 2 (BEHAVIOR):      WHAT we do - Very low autonomy, specific features
        Level 1 (ENVIRONMENT):   WHERE/WHEN - Zero autonomy, ground truth

    Attributes:
        name: Identifier for this walker
        level: Dilts level this walker operates at
        parent: Optional parent walker (one level higher)
        children: List of child walkers spawned by this walker
        workspace: Isolated workspace for execution
        context: Dimensional context (includes inherited WHY)

    Example:
        >>> parent = DiltsWalker(level=DiltsLevel.IDENTITY)
        >>> parent_spec = W5H1(
        ...     subject="Company",
        ...     predicate="launches",
        ...     object="product",
        ...     dimensions={Dimension.WHAT: "Launch premium tier"}
        ... )
        >>> parent.execute(parent_spec)
        >>> child = DiltsWalker(level=DiltsLevel.BELIEFS, parent=parent)
        >>> child.context[Dimension.WHY] == "Launch premium tier"
        True
    """

    def __init__(self, level: DiltsLevel, parent: Optional['DiltsWalker'] = None):
        """
        Initialize a DiltsWalker.

        CRITICAL: If parent exists, inherits parent's WHAT as my WHY.
        This is the core purpose propagation pattern.

        Args:
            level: Dilts level this walker operates at
            parent: Optional parent walker (one level higher)

        Example:
            >>> walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
            >>> walker.level
            <DiltsLevel.CAPABILITY: 3>
        """
        # Generate unique walker ID
        walker_id = f"Walker-L{level.value}-{uuid.uuid4().hex[:8]}"
        super().__init__(walker_id)
        self.level = level
        self.parent = parent
        self.children: List['DiltsWalker'] = []
        self.workspace: Optional[Workspace] = None

        # CRITICAL: Inherit parent's WHAT as my WHY
        if parent and parent.current_node:
            parent_what = parent.current_node.need(Dimension.WHAT)
            if parent_what:
                self.add_context(Dimension.WHY, parent_what)

    def add_context(self, dim: Dimension, value: str) -> None:
        """
        Add dimensional context to this walker.

        Args:
            dim: Dimension to add
            value: Value for dimension

        Example:
            >>> walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
            >>> walker.add_context(Dimension.WHY, "Build feature")
            >>> walker.context[Dimension.WHY]
            'Build feature'
        """
        self.context[dim] = value

    def traverse(self, start: W5H1) -> Any:
        """
        Traverse down the Dilts hierarchy.

        At each level:
        1. Set my WHAT from the spec
        2. If at Level 1 (ENVIRONMENT), execute ground action
        3. Otherwise, spawn child at lower level with WHAT→WHY propagation

        Args:
            start: W5H1 specification to execute

        Returns:
            Result from ground action or child execution

        Example:
            >>> walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
            >>> spec = W5H1(
            ...     subject="System",
            ...     predicate="needs",
            ...     object="feature",
            ...     dimensions={Dimension.WHAT: "Integrate payment"}
            ... )
            >>> result = walker.traverse(spec)
            >>> isinstance(result, str)
            True
        """
        self.current_node = start

        # Set my WHAT
        my_what = start.need(Dimension.WHAT)
        if my_what:
            self.add_context(Dimension.WHAT, my_what)

        # Create workspace for this walker
        self.workspace = Workspace(self.name)

        if self.level == DiltsLevel.ENVIRONMENT:
            # Level 1: Execute ground truth
            return self.execute_ground_action(start)
        else:
            # Spawn child at lower level
            child_level = DiltsLevel(self.level.value - 1)
            child = self._create_child(child_level)
            self.children.append(child)

            # Child's spec inherits my WHAT as their WHY
            child_spec = self._create_child_spec(start, my_what)

            return child.execute(child_spec)

    def _create_child(self, child_level: DiltsLevel) -> 'DiltsWalker':
        """
        Create a child walker. Can be overridden for custom walker types.

        Args:
            child_level: Dilts level for child

        Returns:
            New DiltsWalker instance
        """
        return DiltsWalker(level=child_level, parent=self)

    def _create_child_spec(self, base_spec: W5H1, parent_what: Optional[str]) -> W5H1:
        """
        Create child spec with WHAT→WHY propagation.

        Args:
            base_spec: Base specification
            parent_what: Parent's WHAT value

        Returns:
            New W5H1 with parent's WHAT as WHY
        """
        # Create new dimensions dict with parent's WHAT as child's WHY
        child_dimensions = base_spec.dimensions.copy()
        if parent_what:
            child_dimensions[Dimension.WHY] = parent_what

        return base_spec.copy_with(dimensions=child_dimensions)

    def spawn_children(self, n_strategies: int, base_spec: W5H1) -> List[Tuple['DiltsWalker', W5H1]]:
        """
        Spawn multiple children exploring different approaches.

        Portfolio strategy: try several approaches, pick what works.
        Each child gets:
        - Parent's WHAT as their WHY (purpose propagation)
        - Different WHAT (strategy variation)

        Args:
            n_strategies: Number of different strategies to try
            base_spec: Base specification for children

        Returns:
            List of (child_walker, child_spec) tuples

        Example:
            >>> walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
            >>> spec = W5H1(
            ...     subject="System",
            ...     predicate="needs",
            ...     object="payment",
            ...     dimensions={Dimension.WHAT: "Integrate payment"}
            ... )
            >>> children = walker.spawn_children(3, spec)
            >>> len(children)
            3
        """
        children = []
        my_what = self.current_node.need(Dimension.WHAT) if self.current_node else None

        # Generate n different strategies
        strategies = self.generate_strategies(base_spec, n_strategies)

        for strategy in strategies:
            child_level = DiltsLevel(self.level.value - 1)
            child = self._create_child(child_level)

            # Create child spec with:
            # - Parent's WHAT as child's WHY
            # - Strategy as child's WHAT
            child_dimensions = base_spec.dimensions.copy()
            if my_what:
                child_dimensions[Dimension.WHY] = my_what
            child_dimensions[Dimension.WHAT] = strategy

            child_spec = base_spec.copy_with(dimensions=child_dimensions)
            children.append((child, child_spec))

        return children

    def execute_portfolio(self, spec: W5H1, n_strategies: int = 3) -> Any:
        """
        Execute multiple strategies in parallel.

        Portfolio approach:
        1. Generate n different strategies
        2. Execute all strategies
        3. Validate results
        4. Select winner based on validation score (not confidence)

        Args:
            spec: Specification to execute
            n_strategies: Number of strategies to try (default: 3)

        Returns:
            Best result from portfolio

        Example:
            >>> walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
            >>> spec = W5H1(
            ...     subject="System",
            ...     predicate="needs",
            ...     object="payment",
            ...     dimensions={
            ...         Dimension.WHAT: "Integrate payment",
            ...         Dimension.WHY: "Launch premium"
            ...     }
            ... )
            >>> result = walker.execute_portfolio(spec, n_strategies=3)
            >>> len(walker.children)
            3
        """
        self.current_node = spec

        # Spawn children with different strategies
        children_and_specs = self.spawn_children(n_strategies, spec)

        results = []
        for child, child_spec in children_and_specs:
            try:
                result = child.execute(child_spec)
                validation = self.validate(result)
                results.append({
                    'child': child,
                    'spec': child_spec,
                    'result': result,
                    'validation': validation
                })
                self.children.append(child)
            except Exception as e:
                # Strategy failed, skip it
                results.append({
                    'child': child,
                    'spec': child_spec,
                    'result': None,
                    'validation': ValidationResult(score=0.0, passed=False, details=str(e))
                })

        # Pick best based on validation score, not confidence
        if not results:
            raise RuntimeError("All strategies failed")

        best = max(results, key=lambda r: r['validation'].score)

        if not best['validation'].passed:
            raise RuntimeError(f"No strategy passed validation. Best score: {best['validation'].score}")

        return best['result']

    def trace_provenance(self) -> List[str]:
        """
        Trace WHY chain from here to root.

        Returns the full WHAT→WHY chain from Mission (L6) down to
        current level. This enables full explainability: "Why am I
        doing this? Because parent wanted X, which is because..."

        Returns:
            List of WHAT values from root to current, showing full chain

        Example:
            >>> L6 = DiltsWalker(level=DiltsLevel.MISSION)
            >>> spec = W5H1(
            ...     subject="Company",
            ...     predicate="needs",
            ...     object="revenue",
            ...     dimensions={Dimension.WHAT: "Increase revenue"}
            ... )
            >>> L6.execute(spec)
            >>> # Get deepest walker
            >>> walker = L6
            >>> while walker.children:
            ...     walker = walker.children[0]
            >>> chain = walker.trace_provenance()
            >>> "Increase revenue" in chain
            True
        """
        chain = []
        walker = self

        # Walk up to root, collecting WHAT values
        while walker:
            what = walker.context.get(Dimension.WHAT)
            if what:
                chain.append(what)
            walker = walker.parent

        # Reverse so root (Mission) is first
        return list(reversed(chain))

    def execute_ground_action(self, spec: W5H1) -> str:
        """
        Level 1: Actually do the thing.

        This is where actual execution happens. At Environment level
        (L1), we have zero autonomy - just execute the specified action.

        Args:
            spec: Specification with ground-level action

        Returns:
            Result string describing execution

        Example:
            >>> walker = DiltsWalker(level=DiltsLevel.ENVIRONMENT)
            >>> spec = W5H1(
            ...     subject="System",
            ...     predicate="executes",
            ...     object="action",
            ...     dimensions={
            ...         Dimension.WHAT: "Run tests",
            ...         Dimension.WHY: "Verify implementation"
            ...     }
            ... )
            >>> result = walker.execute_ground_action(spec)
            >>> "EXECUTED" in result
            True
        """
        what = spec.need(Dimension.WHAT)
        why = spec.need(Dimension.WHY)
        return f"EXECUTED: {what} (because: {why})"

    def generate_strategies(self, spec: W5H1, n: int) -> List[str]:
        """
        Generate n different strategies for achieving the goal.

        Subclasses should override this based on their level's autonomy.
        Higher levels (Mission, Identity) have extreme autonomy and can
        generate radically different strategies. Lower levels (Behavior,
        Environment) have limited autonomy and generate minor variations.

        Default implementation provides generic strategies.

        Args:
            spec: Specification describing goal
            n: Number of strategies to generate

        Returns:
            List of strategy descriptions (WHAT values)

        Example:
            >>> class ConcreteWalker(DiltsWalker):
            ...     def generate_strategies(self, spec, n):
            ...         base = spec.need(Dimension.WHAT) or "action"
            ...         return [f"{base} - Strategy {i+1}" for i in range(n)]
            ...     def validate(self, result):
            ...         return ValidationResult(score=0.8, passed=True)
            >>> walker = ConcreteWalker(level=DiltsLevel.CAPABILITY)
            >>> strategies = walker.generate_strategies(
            ...     W5H1("A", "B", "C", dimensions={Dimension.WHAT: "Build"}),
            ...     3
            ... )
            >>> len(strategies)
            3
        """
        # Default implementation: generate generic strategies
        base_what = spec.need(Dimension.WHAT) or "achieve goal"
        return [f"{base_what} - Approach {i+1}" for i in range(n)]

    def validate(self, result: Any) -> ValidationResult:
        """
        Validate the result of execution.

        Portfolio selection uses this to pick the best strategy based
        on actual results, not predicted confidence. Subclasses should
        override this to define level-appropriate validation criteria.

        Default implementation provides basic validation.

        Args:
            result: Result from execution

        Returns:
            ValidationResult with score and pass/fail status

        Example:
            >>> class ConcreteWalker(DiltsWalker):
            ...     def generate_strategies(self, spec, n):
            ...         return [f"Strategy {i}" for i in range(n)]
            ...     def validate(self, result):
            ...         # Simple validation: non-empty result passes
            ...         score = 0.8 if result else 0.0
            ...         return ValidationResult(
            ...             score=score,
            ...             passed=bool(result),
            ...             details="Result validation"
            ...         )
            >>> walker = ConcreteWalker(level=DiltsLevel.CAPABILITY)
            >>> validation = walker.validate("success")
            >>> validation.passed
            True
        """
        # Default implementation: basic validation
        if result is None:
            return ValidationResult(
                score=0.0,
                passed=False,
                details="No result returned"
            )

        result_str = str(result)
        if "EXECUTED" in result_str:
            return ValidationResult(
                score=0.85,
                passed=True,
                details="Execution completed successfully"
            )
        elif result_str:
            return ValidationResult(
                score=0.7,
                passed=True,
                details="Result returned"
            )
        else:
            return ValidationResult(
                score=0.1,
                passed=False,
                details="Empty result"
            )