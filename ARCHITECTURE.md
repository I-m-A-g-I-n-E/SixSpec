# SixSpec Architecture

## Overview

SixSpec is a hierarchical specification framework that combines the 5W1H dimensional model with Dilts' Logical Levels to create self-documenting, traceable, and queryable systems. This document explains how all the pieces fit together.

## Core Architecture Principle

**Parent's WHAT becomes child's WHY**

This simple rule creates:
- Full traceability from mission to implementation
- Self-documenting execution chains
- Explainable AI reasoning
- Purpose preservation through delegation

## System Layers

```
┌─────────────────────────────────────────┐
│         Application Layer                │
│  (Your code using SixSpec)              │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Walker Layer                     │
│  - DiltsWalker (hierarchical execution) │
│  - A2AWalker (task lifecycle)           │
│  - Strategy implementations             │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Agent Layer                      │
│  - NodeAgent (isolated operations)      │
│  - GraphAgent (context-aware)           │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Core Layer                       │
│  - Chunk (dimensional specs)             │
│  - Dimension enum                       │
│  - DiltsLevel enum                      │
│  - BaseActor interface                  │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Integration Layer                │
│  - Git (commits, history, hooks)        │
│  - A2A (task lifecycle protocol)        │
└─────────────────────────────────────────┘
```

## Core Components

### 1. Core Models (`sixspec/core/models.py`)

#### Dimension Enum
```python
class Dimension(Enum):
    WHO = "who"      # Actors, stakeholders
    WHAT = "what"    # Actions, objects
    WHEN = "when"    # Temporal context
    WHERE = "where"  # Spatial context
    HOW = "how"      # Methods, processes
    WHY = "why"      # Purpose, motivation
```

The six dimensions provide a complete framework for describing any specification, action, or context.

#### DiltsLevel Enum
```python
class DiltsLevel(Enum):
    MISSION = 6      # FOR WHAT - Extreme autonomy
    IDENTITY = 5     # WHO we are - High autonomy
    BELIEFS = 4      # WHY we choose - Moderate autonomy
    CAPABILITY = 3   # HOW we operate - Low autonomy
    BEHAVIOR = 2     # WHAT we do - Very low autonomy
    ENVIRONMENT = 1  # WHERE/WHEN - Zero autonomy
```

Each level has:
- **Autonomy level**: How much freedom in decision-making
- **Primary dimensions**: Which dimensions it naturally emphasizes
- **Delegation pattern**: How it creates child specifications

#### Chunk Class

Universal container for dimensional specifications:

```python
@dataclass
class 5W1H:
    subject: str                              # Who/what is acting
    predicate: str                            # Relationship/action
    object: str                               # Target/result
    dimensions: Dict[Dimension, str]          # Six dimensions
    confidence: Dict[Dimension, float]        # Per-dimension confidence
    level: Optional[DiltsLevel]               # Dilts level assignment
```

**Key Methods:**
- `has(dim)`: Check if dimension is set
- `need(dim)`: Demand-driven dimension fetch (enables lazy evaluation)
- `set(dim, value, confidence)`: Set dimension with confidence score
- `shared_dimensions(other)`: Find overlap with another Chunk
- `is_same_system(other)`: Grocery store rule (≥1 shared dimension)
- `is_complete()`: Validate all required dimensions present
- `copy_with(**updates)`: Immutable-style updates

**Specialized Subclasses:**

- **CommitChunk**: Requires WHY + HOW (for Git commits)
- **SpecChunk**: Requires WHO + WHAT + WHY (for full specifications)

### 2. Agent Layer (`sixspec/agents/`)

Agents are entities that understand and execute dimensional specifications.

#### BaseActor (Abstract)
```python
class BaseActor(ABC):
    def understand(self, spec: Chunk) -> bool:
        """Can this actor process this spec?"""

    def execute(self, spec: Chunk) -> Any:
        """Execute based on specification"""
```

#### NodeAgent

Operates on isolated specifications without graph awareness.

**Use cases:**
- TreeSitter parsing a single file
- Linter checking one function
- Test generator for one commit
- Formatter that doesn't need relationships

**Architecture:**
```python
class NodeAgent(BaseActor):
    def __init__(self, name: str, scope: str):
        self.scope = scope  # What kind of node?

    def understand(self, spec: Chunk) -> bool:
        # Must have dimensions and be complete
        return len(spec.dimensions) > 0 and spec.is_complete()

    def process_node(self, spec: Chunk) -> Any:
        # Subclass implements specific logic
        pass
```

#### GraphAgent

Traverses relationships and gathers context from neighbors.

**Use cases:**
- Dependency analysis
- Impact analysis
- Context-aware code generation
- Relationship discovery

**Architecture:**
```python
class GraphAgent(BaseActor):
    def __init__(self, name: str):
        self.current_node: Optional[Chunk] = None
        self.visited: Set[str] = set()

    def traverse(self, start: Chunk) -> Any:
        """Navigate the graph starting from a node"""

    def gather_context(self, spec: Chunk, depth: int) -> List[Chunk]:
        """Collect neighboring nodes for context"""
```

### 3. Walker Layer (`sixspec/walkers/`)

Walkers implement hierarchical delegation with WHAT→WHY propagation.

#### DiltsWalker

The core execution model:

```python
class DiltsWalker(GraphAgent):
    def __init__(self, level: DiltsLevel, parent: Optional['DiltsWalker'] = None):
        self.level = level
        self.parent = parent
        self.children: List['DiltsWalker'] = []
        self.workspace: Optional[Workspace] = None

        # CRITICAL: Inherit parent's WHAT as my WHY
        if parent and parent.current_node:
            parent_what = parent.current_node.need(Dimension.WHAT)
            if parent_what:
                self.add_context(Dimension.WHY, parent_what)
```

**Execution Flow:**

```
Level 6 (MISSION)
    WHAT: "Increase revenue"
    ↓ (child's WHY)
Level 5 (IDENTITY)
    WHY: "Increase revenue"
    WHAT: "Launch premium tier"
    ↓ (child's WHY)
Level 4 (BELIEFS)
    WHY: "Launch premium tier"
    WHAT: "Build payment system"
    ↓ (child's WHY)
Level 3 (CAPABILITY)
    WHY: "Build payment system"
    WHAT: "Integrate Stripe"
    ↓ (child's WHY)
Level 2 (BEHAVIOR)
    WHY: "Integrate Stripe"
    WHAT: "Implement webhook handlers"
    ↓ (child's WHY)
Level 1 (ENVIRONMENT)
    WHY: "Implement webhook handlers"
    WHAT: "Write WebhookController.handle_payment()"
    → EXECUTE
```

**Key Methods:**

- `traverse(start)`: Walk down hierarchy with WHAT→WHY propagation
- `spawn_children(n, spec)`: Portfolio execution - try multiple strategies
- `execute_portfolio(spec, n)`: Execute strategies, validate, pick winner
- `trace_provenance()`: Return full WHY chain from root to current
- `generate_strategies(spec, n)`: Generate n different approaches (override by level)
- `validate(result)`: Validate execution result (override by level)

**Portfolio Execution Pattern:**

```python
# Level 3 walker generating multiple strategies
walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
spec = Chunk(
    subject="System",
    predicate="needs",
    object="payment",
    dimensions={
        Dimension.WHAT: "Integrate payment processing",
        Dimension.WHY: "Launch premium tier"
    }
)

# Spawns 3 children with different strategies:
# Child 1 WHAT: "Integrate Stripe"
# Child 2 WHAT: "Integrate PayPal"
# Child 3 WHAT: "Build custom payment processor"

# All execute, validate results, pick winner
result = walker.execute_portfolio(spec, n_strategies=3)
```

#### A2AWalker

DiltsWalker enhanced with Google A2A protocol for graceful interruption:

```python
class A2AWalker(DiltsWalker):
    def __init__(self, level: DiltsLevel, parent: Optional['DiltsWalker'] = None):
        super().__init__(level, parent)
        self.task = Task(task_id=self.name, parent=parent.task if parent else None)
```

**A2A Lifecycle:**

```
PENDING → start() → RUNNING → pause() → PAUSED
                        ↓                    ↓
                   complete()           resume()
                        ↓                    ↓
                   COMPLETED            RUNNING
```

**Key Features:**
- Graceful pause with full context preservation
- Parent-child coordination via status callbacks
- Resume from pause without losing WHAT→WHY chain
- Cascade operations (pause cascades to children)

#### Strategy Implementations

**MissionWalker** (Level 6):
- Extreme autonomy
- Generates radically different strategic approaches
- Validation focuses on business outcomes

**CapabilityWalker** (Level 3):
- Low autonomy
- Generates technical implementation variations
- Validation focuses on technical correctness

### 4. Workspace (`sixspec/walkers/workspace.py`)

Isolated execution environment per walker:

```python
class Workspace:
    def __init__(self, walker_id: str):
        self.walker_id = walker_id
        self.data: Dict[str, Any] = {}
        self.created_at = datetime.now()

    def store(self, key: str, value: Any):
        """Store data in workspace"""

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data from workspace"""

    def clear():
        """Clear workspace data"""
```

**Purpose:**
- Isolate walker state
- Prevent cross-contamination in portfolio execution
- Enable clean cleanup after completion

### 5. Git Integration (`sixspec/git/`)

#### CommitMessageParser

Parses dimensional commits into CommitChunk objects:

```python
class CommitMessageParser:
    @classmethod
    def parse(cls, commit_msg: str, commit_hash: str = "") -> Commit5W1H:
        """Parse commit message into CommitChunk"""

    @classmethod
    def parse_git_log(cls, repo_path: Path, n: Optional[int] = None,
                     skip_invalid: bool = True) -> List[CommitChunk]:
        """Parse recent commits from git log"""
```

**Format:**
```
<type>: <subject>

WHY: <purpose>
HOW: <approach>
[optional dimensions]
```

#### DimensionalGitHistory

Queryable commit history:

```python
class DimensionalGitHistory:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.commits: List[CommitChunk] = []
        self._load_commits()

    def query(self, where: str = None, why: str = None,
              commit_type: str = None, **kwargs) -> List[CommitChunk]:
        """Query commits by any dimension"""

    def trace_file_purpose(self, file_path: str) -> List[CommitChunk]:
        """Find all commits affecting a file"""

    def get_purposes(self) -> List[str]:
        """Get all unique WHY values"""
```

**Query Examples:**
```python
history = DimensionalGitHistory(Path("/repo"))

# Find payment-related fixes
payment_fixes = history.query(where="payment", commit_type="fix")

# Find all timeout issues
timeout_issues = history.query(why="timeout")

# Trace file evolution
file_history = history.trace_file_purpose("src/payment/stripe.py")
```

#### Git Hook (`sixspec/git/hooks/commit-msg`)

Validates commits before acceptance:

```python
#!/usr/bin/env python3
# Validates:
# - Commit type is valid (feat, fix, refactor, docs, test, chore)
# - WHY dimension present
# - HOW dimension present
# - Skips merge commits
# - Ignores comment lines
```

### 6. A2A Integration (`sixspec/a2a/`)

Implementation of Google's Agent-to-Agent (A2A) protocol for graceful task lifecycle management.

#### Task

A2A-compatible task with lifecycle:

```python
class Task:
    def __init__(self, task_id: Optional[str] = None, parent: Optional['Task'] = None):
        self.status = TaskStatus.PENDING
        self.result: Optional[Any] = None
        self.error: Optional[str] = None
        self.parent = parent
        self.children: List['Task'] = []

    def start() -> None:
        """PENDING → RUNNING"""

    def pause() -> None:
        """RUNNING → PAUSED (cascades to children)"""

    def resume() -> None:
        """PAUSED → RUNNING (bottom-up: children first)"""

    def complete(result: Any) -> None:
        """→ COMPLETED (terminal)"""

    def fail(error: str) -> None:
        """→ FAILED (terminal)"""
```

#### TaskStatus

```python
class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

    def can_pause(self) -> bool:
        return self == TaskStatus.RUNNING

    def can_resume(self) -> bool:
        return self == TaskStatus.PAUSED

    def is_terminal(self) -> bool:
        return self in {TaskStatus.COMPLETED, TaskStatus.FAILED}
```

#### StatusUpdate

Real-time status streaming:

```python
@dataclass
class StatusUpdate:
    task_id: str
    status: TaskStatus
    result: Optional[Any]
    error: Optional[str]
    metadata: dict
```

## Data Flow Patterns

### 1. Hierarchical Delegation

```
Mission Level (L6)
   ├─ Defines WHAT: "Increase revenue by 20%"
   │
   └─> Identity Level (L5)
       ├─ Inherits WHY: "Increase revenue by 20%"
       ├─ Defines WHAT: "Launch premium tier"
       │
       └─> Beliefs Level (L4)
           ├─ Inherits WHY: "Launch premium tier"
           ├─ Defines WHAT: "Subscription model"
           │
           └─> Capability Level (L3)
               ├─ Inherits WHY: "Subscription model"
               ├─ Defines WHAT: "Payment integration"
               │
               └─> Behavior Level (L2)
                   ├─ Inherits WHY: "Payment integration"
                   ├─ Defines WHAT: "Stripe webhook handler"
                   │
                   └─> Environment Level (L1)
                       ├─ Inherits WHY: "Stripe webhook handler"
                       ├─ Defines WHAT: "POST /webhooks/stripe"
                       └─ EXECUTES: Creates endpoint
```

### 2. Portfolio Execution

```
Parent Walker (L3)
    ├─ WHAT: "Integrate payment"
    │
    ├─> Child 1 (L2)
    │   └─ Strategy: "Stripe integration"
    │       └─ Result: Score 0.9 ✓
    │
    ├─> Child 2 (L2)
    │   └─ Strategy: "PayPal integration"
    │       └─ Result: Score 0.7
    │
    └─> Child 3 (L2)
        └─ Strategy: "Custom payment processor"
            └─ Result: Score 0.5

Winner: Child 1 (highest validation score)
```

### 3. Provenance Tracing

```python
# At any level, trace back to root
walker = current_walker
chain = walker.trace_provenance()

# Returns:
[
    "Increase revenue by 20%",      # Mission (L6)
    "Launch premium tier",          # Identity (L5)
    "Subscription model",           # Beliefs (L4)
    "Payment integration",          # Capability (L3)
    "Stripe webhook handler",       # Behavior (L2)
    "POST /webhooks/stripe"         # Environment (L1)
]

# Answer "Why am I doing this?" at any level
# → Full chain shows complete reasoning
```

### 4. A2A Pause/Resume

```
Walker hierarchy executing:
    L6 → L5 → L4 → L3 (RUNNING)
         ↓
    User interrupts
         ↓
    L3.pause() → cascades to all children
         ↓
    L6 → L5 → L4 → L3 (PAUSED)
         ↓
    All context preserved:
    - WHAT→WHY chain
    - Workspace data
    - Task state
         ↓
    Later: L3.resume()
         ↓
    Bottom-up resume: children first
         ↓
    L6 → L5 → L4 → L3 (RUNNING)
    Continues from exact state
```

## Design Patterns

### 1. Lazy Evaluation

Use `need()` instead of direct access:

```python
# ✓ Good: Lazy evaluation
why = spec.need(Dimension.WHY)
if why:
    child_spec.set(Dimension.WHY, why)

# ✗ Bad: Direct access
why = spec.dimensions[Dimension.WHY]  # KeyError if missing
```

### 2. Purpose Propagation

Always propagate WHAT→WHY:

```python
# ✓ Good: Purpose propagation
child_dimensions = {
    Dimension.WHY: parent.need(Dimension.WHAT),  # Parent's WHAT
    Dimension.WHAT: "Implement feature"           # Child's WHAT
}

# ✗ Bad: No propagation
child_dimensions = {
    Dimension.WHAT: "Implement feature"  # Lost context
}
```

### 3. Confidence Tracking

Track confidence per dimension:

```python
# ✓ Good: Explicit confidence
spec.set(Dimension.WHO, "Premium users", confidence=0.9)
spec.set(Dimension.WHAT, "Advanced reports", confidence=0.6)

# Later: Make decisions based on confidence
if spec.get_confidence(Dimension.WHO) > 0.8:
    proceed_with_implementation()
```

### 4. Validation Over Prediction

Portfolio execution validates results, not predictions:

```python
# ✓ Good: Validate actual results
def validate(self, result: Any) -> ValidationResult:
    if test_suite_passes(result):
        return ValidationResult(score=0.95, passed=True)
    return ValidationResult(score=0.0, passed=False)

# ✗ Bad: Predict before execution
def estimate_confidence(self, strategy: str) -> float:
    return 0.8  # Guessing, not validating
```

### 5. Workspace Isolation

Each walker gets isolated workspace:

```python
# ✓ Good: Isolated workspace
walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
walker.workspace.store("temp_data", analysis_result)
result = walker.execute(spec)
walker.workspace.clear()  # Clean up

# ✗ Bad: Shared state
global_cache["temp_data"] = analysis_result  # Pollution
```

## Integration Points

### 1. Git Integration

```python
# Install hook
cp sixspec/git/hooks/commit-msg .git/hooks/
chmod +x .git/hooks/commit-msg

# Configure template
git config commit.template templates/.gitmessage

# Make dimensional commit
git commit -m "fix: payment timeout

WHY: Users abandoning carts at 25% rate
HOW: Added retry logic with exponential backoff"

# Query history
history = DimensionalGitHistory(Path("."))
results = history.query(where="payment", commit_type="fix")
```

### 2. A2A Integration

```python
# Create A2A-enabled walker
walker = A2AWalker(level=DiltsLevel.CAPABILITY)

# Subscribe to status updates
def handle_status(update: StatusUpdate):
    print(f"Status: {update.status}")

walker.task.on_status_change(handle_status)

# Execute with pause capability
walker.task.start()
result = walker.execute(spec)

# Graceful interruption
walker.task.pause()  # Preserves all context
# ... later ...
walker.task.resume()  # Continues exactly where it left off
```

### 3. Custom Agents

```python
# Create custom NodeAgent
class LinterAgent(NodeAgent):
    def __init__(self):
        super().__init__("Linter", scope="code_file")

    def process_node(self, spec: Chunk) -> Any:
        file_path = spec.need(Dimension.WHERE)
        return run_linter(file_path)

# Create custom GraphAgent
class DependencyAgent(GraphAgent):
    def __init__(self):
        super().__init__("DependencyAnalyzer")

    def traverse(self, start: Chunk) -> Any:
        context = self.gather_context(start, depth=2)
        return analyze_dependencies(context)
```

### 4. Custom Walkers

```python
# Custom walker with specific validation
class TestingWalker(DiltsWalker):
    def __init__(self):
        super().__init__(level=DiltsLevel.CAPABILITY)

    def generate_strategies(self, spec: Chunk, n: int) -> List[str]:
        base = spec.need(Dimension.WHAT)
        return [
            f"{base} with unit tests",
            f"{base} with integration tests",
            f"{base} with E2E tests"
        ]

    def validate(self, result: Any) -> ValidationResult:
        test_coverage = calculate_coverage(result)
        return ValidationResult(
            score=test_coverage,
            passed=test_coverage > 0.8,
            details=f"Coverage: {test_coverage:.1%}"
        )
```

## Performance Considerations

### 1. Lazy Loading

Git history uses lazy loading with caching:

```python
class DimensionalGitHistory:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.commits: List[CommitChunk] = []
        self._loaded = False

    def _load_commits(self):
        if not self._loaded:
            self.commits = CommitMessageParser.parse_git_log(self.repo_path)
            self._loaded = True
```

### 2. Portfolio Parallelization

Portfolio execution can be parallelized:

```python
# Sequential (current)
for child, spec in children_and_specs:
    result = child.execute(spec)

# Parallel (future enhancement)
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(child.execute, spec)
               for child, spec in children_and_specs]
    results = [f.result() for f in futures]
```

### 3. Workspace Cleanup

Always clean up workspaces:

```python
try:
    result = walker.execute(spec)
finally:
    if walker.workspace:
        walker.workspace.clear()
```

## Testing Architecture

### Test Organization

```
tests/
├── core/
│   └── test_models.py          # Chunk, Dimension, DiltsLevel
├── agents/
│   ├── test_node_agent.py      # NodeAgent tests
│   ├── test_graph_agent.py     # GraphAgent tests
│   └── test_examples.py        # Example agent tests
├── walkers/
│   ├── test_dilts_walker.py    # DiltsWalker tests
│   ├── test_a2a_walker.py      # A2AWalker tests
│   └── test_workspace.py       # Workspace tests
├── a2a/
│   └── test_task.py            # Task lifecycle tests
└── git/
    ├── test_parser.py          # Commit parsing
    ├── test_history.py         # History queries
    └── test_hooks.py           # Hook validation
```

### Test Coverage

- **Core models**: 100% (all dimensional operations)
- **Agents**: 95% (NodeAgent, GraphAgent, examples)
- **Walkers**: 90% (DiltsWalker, A2AWalker, strategies)
- **Git integration**: 95% (parser, history, hooks)
- **A2A integration**: 100% (task lifecycle)

## Future Architecture

### Phase 2 Enhancements

1. **CLI Tool**
   ```
   sixspec/
   └── cli/
       ├── __init__.py
       ├── commands.py
       └── interactive.py
   ```

2. **Visualization**
   ```
   sixspec/
   └── viz/
       ├── __init__.py
       ├── graph.py
       └── timeline.py
   ```

3. **Migration Tool**
   ```
   sixspec/
   └── migration/
       ├── __init__.py
       └── convert.py
   ```

### Extensibility Points

1. **Custom Dimensions**: Extend Dimension enum for domain-specific needs
2. **Custom Levels**: Create domain-specific hierarchies
3. **Custom Validation**: Override validate() for domain-specific checks
4. **Custom Strategies**: Override generate_strategies() for domain-specific approaches

## Summary

SixSpec's architecture is built on three core principles:

1. **Dimensional Specifications**: Chunk provides complete context
2. **Hierarchical Delegation**: Dilts levels organize autonomy
3. **Purpose Propagation**: WHAT→WHY creates traceability

This creates a system where:
- Every action has traceable purpose
- Git history becomes queryable
- AI agents understand context
- Execution can be paused and resumed gracefully
- Validation trumps prediction

The architecture is designed for:
- **Simplicity**: Core patterns are easy to understand
- **Extensibility**: Easy to add custom agents, walkers, strategies
- **Integration**: Works with existing tools (Git, testing frameworks)
- **Production-ready**: Comprehensive testing and validation
