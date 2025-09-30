# SixSpec Design Philosophy

## Why SixSpec Exists

### The Problem

Traditional software development suffers from three fundamental gaps:

1. **Context Loss**: Code changes are made, but the reasoning behind them disappears over time
2. **Purpose Fragmentation**: Requirements, design, implementation, and documentation live in separate silos
3. **Agent Blindness**: AI agents can read code but cannot understand *why* it exists or *how* it should evolve

### The Solution

SixSpec makes **context**, **purpose**, and **reasoning** first-class citizens by:

1. Capturing the six dimensions of every specification (W5H1)
2. Creating traceable chains from mission to implementation
3. Making Git history queryable and self-documenting
4. Enabling AI agents to understand purpose, not just syntax

---

## Core Principles

### 1. Dimensional Completeness

**Principle**: Every specification should answer WHO, WHAT, WHEN, WHERE, HOW, and WHY.

**Rationale**: Incomplete specifications lead to incorrect implementations. Traditional specs focus on WHAT but rarely capture WHY or HOW with the same rigor.

**In Practice:**
```python
# ✗ Incomplete
"Add payment processing"

# ✓ Complete
W5H1(
    subject="System",
    predicate="provides",
    object="payment processing",
    dimensions={
        Dimension.WHO: "Premium subscribers",
        Dimension.WHAT: "Stripe integration with hosted checkout",
        Dimension.WHEN: "On subscription purchase",
        Dimension.WHERE: "Payment service module",
        Dimension.HOW: "Using Stripe Checkout Sessions API",
        Dimension.WHY: "Enable premium subscriptions per Q2 roadmap"
    }
)
```

### 2. Purpose Propagation

**Principle**: Parent's WHAT becomes child's WHY.

**Rationale**: This creates an unbreakable chain of purpose from strategic mission down to individual lines of code. Every implementation knows *why* it exists.

**In Practice:**
```
Mission (L6):    WHAT = "Achieve market leadership"
                          ↓ (becomes child's WHY)
Identity (L5):   WHY = "Achieve market leadership"
                 WHAT = "Launch premium tier"
                          ↓
Beliefs (L4):    WHY = "Launch premium tier"
                 WHAT = "Subscription model"
                          ↓
Capability (L3): WHY = "Subscription model"
                 WHAT = "Integrate payment processing"
                          ↓
Behavior (L2):   WHY = "Integrate payment processing"
                 WHAT = "Stripe webhook handlers"
                          ↓
Environment (L1): WHY = "Stripe webhook handlers"
                  WHAT = "POST /webhooks/stripe endpoint"
                  → EXECUTES
```

**Impact**: Ask "why does this endpoint exist?" at any level and get the complete chain back to business mission.

### 3. Validation Over Prediction

**Principle**: Choose strategies based on actual results, not predicted confidence.

**Rationale**: Predictions are guesses. Validation tests reality. Portfolio execution tries multiple approaches and picks the winner based on measurable outcomes.

**In Practice:**
```python
# ✗ Bad: Predict before execution
def estimate_success(strategy: str) -> float:
    return 0.8  # Guessing

# ✓ Good: Validate after execution
def validate(result: Any) -> ValidationResult:
    test_coverage = run_tests(result)
    return ValidationResult(
        score=test_coverage,
        passed=test_coverage > 0.8
    )
```

### 4. Lazy Evaluation

**Principle**: Don't demand what you don't need, but make it available when you do.

**Rationale**: Not every dimension is relevant at every level. Use `need()` for on-demand dimension access rather than requiring all dimensions upfront.

**In Practice:**
```python
# ✗ Eager: Forces all dimensions
def process(spec: W5H1):
    who = spec.dimensions[Dimension.WHO]      # KeyError if missing
    what = spec.dimensions[Dimension.WHAT]    # KeyError if missing
    why = spec.dimensions[Dimension.WHY]      # KeyError if missing

# ✓ Lazy: Fetch what you need
def process(spec: W5H1):
    who = spec.need(Dimension.WHO)   # None if missing, no error
    if who:
        personalize_for(who)
```

### 5. Confidence Tracking

**Principle**: Track certainty per dimension, not per spec.

**Rationale**: Different dimensions have different confidence levels. You might be certain about WHO (users) but uncertain about HOW (implementation approach).

**In Practice:**
```python
spec = W5H1("System", "needs", "feature")

# High confidence: Requirements are clear
spec.set(Dimension.WHO, "All users", confidence=1.0)

# Medium confidence: Approach chosen but not finalized
spec.set(Dimension.HOW, "OAuth2 with JWT", confidence=0.7)

# Low confidence: Still exploring
spec.set(Dimension.WHERE, "Auth service", confidence=0.4)

# Make decisions based on confidence
for dim in spec.dimensions:
    if spec.get_confidence(dim) < 0.5:
        research_alternatives(dim)
```

### 6. Hierarchical Autonomy

**Principle**: Autonomy decreases as you descend the Dilts hierarchy.

**Rationale**: Strategic levels (Mission, Identity) should have freedom to explore radically different approaches. Tactical levels (Behavior, Environment) should execute with precision.

| Level | Autonomy | Decision Scope |
|-------|----------|----------------|
| Mission (L6) | Extreme | Can redefine entire purpose |
| Identity (L5) | High | Can redefine product strategy |
| Beliefs (L4) | Moderate | Can choose principles |
| Capability (L3) | Low | Can select methods |
| Behavior (L2) | Very Low | Can execute defined behaviors |
| Environment (L1) | Zero | Must execute exactly as specified |

**In Practice:**
```python
# Mission Walker: Extreme freedom
class MissionWalker(DiltsWalker):
    def generate_strategies(self, spec, n):
        return [
            "Aggressive market expansion",
            "Sustainable growth focus",
            "Innovation-first approach"
        ]

# Environment Walker: No freedom
class EnvironmentWalker(DiltsWalker):
    def execute_ground_action(self, spec):
        # Execute exactly as specified
        return execute_precisely(spec.need(Dimension.WHAT))
```

### 7. Graceful Interruption

**Principle**: Systems should pause and resume without losing context.

**Rationale**: Real work gets interrupted. A2A protocol enables graceful pause/resume while preserving the full WHAT→WHY chain.

**In Practice:**
```python
walker = A2AWalker(level=DiltsLevel.CAPABILITY)
walker.task.start()

# Work happens...
# User interrupts

walker.task.pause()  # Cascade to all children
# All context preserved:
# - WHAT→WHY chain
# - Workspace data
# - Task hierarchy

# Later...
walker.task.resume()  # Bottom-up: children first
# Continues exactly where it left off
```

### 8. Self-Documentation

**Principle**: The version control history should be queryable documentation.

**Rationale**: Documentation rots. Commit messages with WHY and HOW create permanent, queryable documentation linked directly to code changes.

**In Practice:**
```bash
# Traditional commit
git commit -m "Added retry logic"
# → Vague, no context

# Dimensional commit
git commit -m "fix: payment API timeout

WHY: Users abandoning carts at 25% rate due to timeout
HOW: Added retry logic with exponential backoff (3 attempts)"
# → Clear purpose and approach, forever linked to code

# Query history
history.query(why="timeout")  # Find all timeout-related changes
history.trace_file_purpose("payment.py")  # See evolution with reasons
```

---

## Design Decisions

### Why W5H1?

**Decision**: Use six dimensions (WHO, WHAT, WHEN, WHERE, HOW, WHY) instead of custom fields.

**Rationale**:
- Universal: Applicable to any domain
- Complete: Captures all context
- Familiar: Questions everyone already asks
- Structured: Enables programmatic reasoning

**Alternative Considered**: Custom domain-specific fields
- Problem: Every domain needs different fields
- Problem: No standard interface for agents

### Why Dilts' Logical Levels?

**Decision**: Use Dilts hierarchy (Mission → Identity → Beliefs → Capability → Behavior → Environment).

**Rationale**:
- Proven: Used in NLP and organizational psychology
- Natural: Matches how humans think about goals
- Hierarchical: Clear delegation pattern
- Autonomy gradient: Natural autonomy levels

**Alternative Considered**: Flat structure
- Problem: No clear delegation pattern
- Problem: All decisions have equal weight

### Why Subject-Predicate-Object?

**Decision**: W5H1 uses RDF-style triples (subject-predicate-object).

**Rationale**:
- Graph-friendly: Natural for relationships
- Semantic: Clear meaning
- Standard: RDF is widely understood
- Flexible: Can represent any relationship

**Alternative Considered**: Key-value pairs
- Problem: Doesn't capture relationships
- Problem: Harder to reason about connections

### Why Immutable Copies?

**Decision**: Use `copy_with()` for updates instead of mutation.

**Rationale**:
- History: Preserve original specs
- Parallel execution: No race conditions
- Debugging: Can trace changes
- Portfolio: Each strategy gets clean copy

**Alternative Considered**: Mutable updates
- Problem: Lost history
- Problem: Concurrent modification bugs

### Why Portfolio Execution?

**Decision**: Try multiple strategies, validate results, pick winner.

**Rationale**:
- Reality beats prediction: Actual results > confidence scores
- Exploration: Don't commit to first idea
- Safety: Validation prevents bad strategies
- Learning: Compare approaches empirically

**Alternative Considered**: Single best-guess strategy
- Problem: First guess often wrong
- Problem: No comparison data

### Why A2A Protocol?

**Decision**: Implement Google's Agent-to-Agent protocol.

**Rationale**:
- Standard: Emerging industry standard
- Graceful: Pause/resume without context loss
- Hierarchical: Parent-child coordination
- Production-ready: Battle-tested pattern

**Alternative Considered**: Custom lifecycle
- Problem: Reinventing the wheel
- Problem: Less likely to integrate with other systems

---

## Philosophical Foundations

### The Grocery Store Rule

**Concept**: Two objects belong to the same system if they share ≥1 dimension.

**Example**:
```python
milk = W5H1("User", "buys", "milk", dimensions={
    Dimension.WHERE: "grocery store"
})
bread = W5H1("User", "buys", "bread", dimensions={
    Dimension.WHERE: "grocery store"
})
hammer = W5H1("User", "buys", "hammer", dimensions={
    Dimension.WHERE: "hardware store"
})

milk.is_same_system(bread)   # True (same WHERE)
milk.is_same_system(hammer)  # False (different WHERE)
```

**Rationale**: Systems emerge from shared context. Any dimensional overlap suggests relationship.

### The Provenance Chain

**Concept**: Every action can trace its purpose back to root mission.

**Example**:
```python
deepest_walker.trace_provenance()
# Returns:
# [
#     "Achieve market leadership",      # Mission
#     "Launch premium tier",            # Identity
#     "Subscription model",             # Beliefs
#     "Integrate payment",              # Capability
#     "Stripe webhooks",                # Behavior
#     "POST /webhooks/stripe"           # Environment
# ]
```

**Rationale**: "Why am I doing this?" should always have an answer that traces to business value.

### The Confidence Gradient

**Concept**: Requirements flow from high certainty to low certainty.

```
WHO: 1.0    (Business knows users)
WHY: 1.0    (Business knows goals)
WHAT: 0.9   (Features mostly clear)
WHERE: 0.7  (Architecture emerging)
HOW: 0.5    (Implementation uncertain)
WHEN: 0.3   (Timing exploratory)
```

**Rationale**: Make decisions when confidence is sufficient, not before.

### The Autonomy Gradient

**Concept**: Freedom decreases as abstraction decreases.

```
L6 (Mission):      Ask "Should we exist?"
L5 (Identity):     Ask "What should we be?"
L4 (Beliefs):      Ask "Why this approach?"
L3 (Capability):   Ask "How to implement?"
L2 (Behavior):     Ask "What to execute?"
L1 (Environment):  Execute precisely
```

**Rationale**: Strategic thinking at top, precise execution at bottom.

---

## Anti-Patterns

### 1. Dimension Overload

**Anti-pattern**: Requiring all six dimensions for every spec.

```python
# ✗ Bad: Forces irrelevant dimensions
spec = W5H1("System", "does", "thing")
spec.set(Dimension.WHO, "N/A")      # Meaningless
spec.set(Dimension.WHEN, "Always")  # Not helpful
spec.set(Dimension.WHERE, "System") # Too vague
```

**Correct approach**: Only require dimensions that add value.

```python
# ✓ Good: Only relevant dimensions
commit = CommitW5H1("fix", "resolves", "bug")
commit.set(Dimension.WHY, "Users experiencing crashes")
commit.set(Dimension.HOW, "Added null check")
# WHO, WHEN, WHERE optional - add if relevant
```

### 2. Ignoring Confidence

**Anti-pattern**: Making decisions without checking confidence.

```python
# ✗ Bad: Ignoring confidence
approach = spec.need(Dimension.HOW)
implement(approach)  # What if confidence was 0.2?
```

**Correct approach**: Check confidence before committing.

```python
# ✓ Good: Confidence-aware decisions
approach = spec.need(Dimension.HOW)
confidence = spec.get_confidence(Dimension.HOW)

if confidence > 0.7:
    implement(approach)
elif confidence > 0.4:
    prototype_and_validate(approach)
else:
    research_alternatives()
```

### 3. Breaking the WHAT→WHY Chain

**Anti-pattern**: Creating child specs without inheriting parent's WHAT as WHY.

```python
# ✗ Bad: Lost purpose
parent_spec = W5H1("System", "needs", "feature",
    dimensions={Dimension.WHAT: "User authentication"})

child_spec = W5H1("Dev", "implements", "OAuth")
# No WHY! Lost context.
```

**Correct approach**: Always propagate purpose.

```python
# ✓ Good: Purpose preserved
child_spec = W5H1("Dev", "implements", "OAuth",
    dimensions={
        Dimension.WHY: parent_spec.need(Dimension.WHAT),
        Dimension.WHAT: "OAuth2 with JWT tokens"
    })
```

### 4. Premature Execution

**Anti-pattern**: Executing at high levels instead of delegating.

```python
# ✗ Bad: Mission level doing implementation
class MissionWalker(DiltsWalker):
    def traverse(self, spec):
        # Don't do this!
        return implement_feature_directly(spec)
```

**Correct approach**: Delegate down the hierarchy.

```python
# ✓ Good: Mission delegates to Identity
class MissionWalker(DiltsWalker):
    def traverse(self, spec):
        child = self._create_child(DiltsLevel.IDENTITY)
        return child.execute(self._create_child_spec(spec))
```

### 5. Validation-Free Portfolio

**Anti-pattern**: Picking strategies based on arbitrary criteria.

```python
# ✗ Bad: No validation
def execute_portfolio(self, spec, n):
    children = self.spawn_children(n, spec)
    results = [child.execute(spec) for child, spec in children]
    return results[0]  # Why first? Arbitrary!
```

**Correct approach**: Validate and pick winner.

```python
# ✓ Good: Validation-driven selection
def execute_portfolio(self, spec, n):
    children = self.spawn_children(n, spec)
    results = []
    for child, child_spec in children:
        result = child.execute(child_spec)
        validation = self.validate(result)
        results.append((result, validation))

    # Pick best based on validation score
    return max(results, key=lambda r: r[1].score)[0]
```

---

## Future Philosophy

### AI Agents as First-Class Citizens

SixSpec is designed for a future where AI agents:
- Read dimensional commits to understand purpose
- Generate tests based on HOW dimension
- Update documentation from WHY dimension
- Trace requirements through provenance chains
- Make context-aware decisions

### Specifications as Living Graphs

Future enhancements will treat specs as graph nodes:
- Edges represent relationships (parent-child, similar-to, conflicts-with)
- Graph traversal reveals impact analysis
- Pattern matching discovers architectural styles
- Graph queries answer complex questions

### Time-Travel Specifications

Vision: Query specs at any point in time:
```python
# What was the purpose of this feature in January?
spec_jan = history.at(date="2024-01-01").get_spec("user-auth")

# How did our approach evolve?
evolution = history.trace_evolution("user-auth")
for snapshot in evolution:
    print(f"{snapshot.date}: {snapshot.need(Dimension.HOW)}")
```

---

## Conclusion

SixSpec's philosophy centers on three convictions:

1. **Context is Everything**: Code without context is noise
2. **Purpose Propagates**: Every implementation should know its "why"
3. **Validation Wins**: Reality beats prediction

These principles create a framework where:
- Git history becomes queryable documentation
- AI agents understand purpose, not just syntax
- Requirements trace to implementation
- Work can be interrupted and resumed gracefully
- Portfolio execution discovers better solutions

The goal is not perfection but **traceability**, **explainability**, and **evolution**.

---

## Further Reading

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and components
- [TUTORIAL.md](TUTORIAL.md) - Hands-on learning path
- [API_REFERENCE.md](API_REFERENCE.md) - Complete API documentation
- [README.md](README.md) - Quick start and overview

---

**"If you can't explain why you're doing something, maybe you shouldn't be doing it."**

— SixSpec Philosophy
