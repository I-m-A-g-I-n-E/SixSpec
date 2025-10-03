# SixSpec API Reference

Complete API documentation for the SixSpec framework.

## Table of Contents

- [Core Module](#core-module)
  - [Dimension](#dimension)
  - [DiltsLevel](#diltslevel)
  - [Chunk](#w5h1)
  - [CommitChunk](#commitw5h1)
  - [SpecChunk](#specw5h1)
  - [BaseActor](#baseactor)
- [Agents Module](#agents-module)
  - [NodeAgent](#nodeagent)
  - [GraphAgent](#graphagent)
- [Walkers Module](#walkers-module)
  - [DiltsWalker](#diltswalker)
  - [A2AWalker](#a2awalker)
  - [Workspace](#workspace)
  - [ValidationResult](#validationresult)
  - [MissionWalker](#missionwalker)
  - [CapabilityWalker](#capabilitywalker)
- [Git Module](#git-module)
  - [CommitMessageParser](#commitmessageparser)
  - [DimensionalGitHistory](#dimensionalgithistory)
- [A2A Module](#a2a-module)
  - [Task](#task)
  - [TaskStatus](#taskstatus)
  - [StatusUpdate](#statusupdate)

---

## Core Module

### Dimension

```python
from sixspec.core import Dimension
```

Enumeration of the six dimensions in the 5W1H model.

#### Values

```python
Dimension.WHO = "who"      # Actors, stakeholders, agents
Dimension.WHAT = "what"    # Actions, objects, results
Dimension.WHEN = "when"    # Temporal context, timing
Dimension.WHERE = "where"  # Spatial context, location
Dimension.HOW = "how"      # Methods, processes, implementation
Dimension.WHY = "why"      # Purpose, motivation, goals
```

#### Example

```python
from sixspec.core import Dimension

# Access dimension values
print(Dimension.WHY.value)  # "why"

# Iterate over all dimensions
for dim in Dimension:
    print(dim.name, dim.value)
```

---

### DiltsLevel

```python
from sixspec.core import DiltsLevel
```

Enumeration of Dilts' Logical Levels for hierarchical organization.

#### Values

```python
DiltsLevel.MISSION = 6      # FOR WHAT - Extreme autonomy
DiltsLevel.IDENTITY = 5     # WHO we are - High autonomy
DiltsLevel.BELIEFS = 4      # WHY we choose - Moderate autonomy
DiltsLevel.CAPABILITY = 3   # HOW we operate - Low autonomy
DiltsLevel.BEHAVIOR = 2     # WHAT we do - Very low autonomy
DiltsLevel.ENVIRONMENT = 1  # WHERE/WHEN - Zero autonomy
```

#### Properties

##### `primary_dimensions`

```python
@property
def primary_dimensions(self) -> Set[Dimension]
```

Returns the primary dimensions emphasized at this level.

**Returns:**
- `Set[Dimension]`: Set of dimensions naturally emphasized at this level

**Example:**
```python
level = DiltsLevel.CAPABILITY
print(level.primary_dimensions)  # {<Dimension.HOW: 'how'>}
```

##### `autonomy`

```python
@property
def autonomy(self) -> str
```

Returns the autonomy level as a string.

**Returns:**
- `str`: One of "extreme", "high", "moderate", "low", "very_low", "zero"

**Example:**
```python
level = DiltsLevel.MISSION
print(level.autonomy)  # "extreme"
```

---

### Chunk

```python
from sixspec.core import Chunk
```

Universal container for six-dimensional specifications.

#### Constructor

```python
Chunk(
    subject: str,
    predicate: str,
    object: str,
    dimensions: Dict[Dimension, str] = {},
    confidence: Dict[Dimension, float] = {},
    level: Optional[DiltsLevel] = None
)
```

**Parameters:**
- `subject`: The subject of the specification
- `predicate`: The relationship or action
- `object`: The object or result
- `dimensions`: Dictionary mapping Dimension to string values
- `confidence`: Dictionary mapping Dimension to confidence scores (0.0-1.0)
- `level`: Optional Dilts level assignment

**Example:**
```python
spec = Chunk(
    subject="User",
    predicate="wants",
    object="feature",
    dimensions={
        Dimension.WHO: "Premium users",
        Dimension.WHAT: "Advanced reporting"
    }
)
```

#### Methods

##### `has(dim: Dimension) -> bool`

Check if a dimension is set.

**Parameters:**
- `dim`: The dimension to check

**Returns:**
- `bool`: True if dimension is set, False otherwise

**Example:**
```python
if spec.has(Dimension.WHY):
    print("Purpose is defined")
```

##### `need(dim: Dimension) -> Optional[str]`

Demand-driven dimension fetch (lazy evaluation).

**Parameters:**
- `dim`: The dimension to fetch

**Returns:**
- `Optional[str]`: The dimension value if set, None otherwise

**Example:**
```python
why = spec.need(Dimension.WHY)
if why:
    print(f"Purpose: {why}")
```

##### `set(dim: Dimension, value: str, confidence: float = 1.0) -> None`

Set a dimension value with optional confidence score.

**Parameters:**
- `dim`: The dimension to set
- `value`: The dimension value
- `confidence`: Confidence score (0.0-1.0), defaults to 1.0

**Raises:**
- `ValueError`: If confidence is not in range [0.0, 1.0]

**Example:**
```python
spec.set(Dimension.WHO, "Premium users", confidence=0.9)
spec.set(Dimension.WHAT, "Advanced reporting", confidence=0.7)
```

##### `get_confidence(dim: Dimension) -> float`

Get the confidence score for a dimension.

**Parameters:**
- `dim`: The dimension to query

**Returns:**
- `float`: Confidence score (0.0-1.0), or 0.0 if dimension not set

**Example:**
```python
confidence = spec.get_confidence(Dimension.WHO)
if confidence < 0.5:
    print("Low confidence, needs validation")
```

##### `shared_dimensions(other: Chunk) -> Set[Dimension]`

Find dimensions shared with another Chunk object.

**Parameters:**
- `other`: Another Chunk object to compare with

**Returns:**
- `Set[Dimension]`: Set of dimensions present in both objects

**Example:**
```python
spec1 = Chunk("A", "B", "C", dimensions={Dimension.WHERE: "store"})
spec2 = Chunk("D", "E", "F", dimensions={Dimension.WHERE: "store"})
shared = spec1.shared_dimensions(spec2)
print(shared)  # {<Dimension.WHERE: 'where'>}
```

##### `is_same_system(other: Chunk) -> bool`

Check if two objects belong to the same system (grocery store rule).

**Parameters:**
- `other`: Another Chunk object to compare with

**Returns:**
- `bool`: True if objects share ≥1 dimension, False otherwise

**Example:**
```python
milk = Chunk("User", "buys", "milk", dimensions={Dimension.WHERE: "store"})
bread = Chunk("User", "buys", "bread", dimensions={Dimension.WHERE: "store"})
print(milk.is_same_system(bread))  # True
```

##### `copy_with(**updates) -> Chunk`

Create a copy with specified updates (immutable-style).

**Parameters:**
- `**updates`: Keyword arguments for attributes to update

**Returns:**
- `Chunk`: New Chunk instance with updates applied

**Example:**
```python
original = Chunk("A", "B", "C", dimensions={Dimension.WHO: "user"})
variant = original.copy_with(
    object="D",
    dimensions={Dimension.WHO: "admin"}
)
```

##### `required_dimensions() -> Set[Dimension]`

Get the set of required dimensions for this object.

**Returns:**
- `Set[Dimension]`: Set of required Dimension enums (empty for base class)

**Example:**
```python
spec = Chunk("A", "B", "C")
print(spec.required_dimensions())  # set()
```

##### `is_complete() -> bool`

Check if all required dimensions are set.

**Returns:**
- `bool`: True if all required dimensions are present, False otherwise

**Example:**
```python
spec = SpecChunk("A", "B", "C")
print(spec.is_complete())  # False (missing WHO, WHAT, WHY)

spec.set(Dimension.WHO, "user")
spec.set(Dimension.WHAT, "action")
spec.set(Dimension.WHY, "purpose")
print(spec.is_complete())  # True
```

##### `to_dict() -> dict`

Serialize to dictionary format.

**Returns:**
- `dict`: Dictionary representation suitable for JSON serialization

**Example:**
```python
spec = Chunk("A", "B", "C", dimensions={Dimension.WHO: "user"})
data = spec.to_dict()
```

##### `from_dict(data: dict) -> Chunk`

Deserialize from dictionary format (class method).

**Parameters:**
- `data`: Dictionary representation (from to_dict())

**Returns:**
- `Chunk`: New Chunk instance reconstructed from dictionary

**Example:**
```python
data = {
    'subject': 'A', 'predicate': 'B', 'object': 'C',
    'dimensions': {'who': 'user'},
    'confidence': {'who': 0.9},
    'level': None
}
spec = Chunk.from_dict(data)
```

---

### CommitChunk

```python
from sixspec.core import CommitChunk
```

Specialized Chunk for Git commits (requires WHY + HOW).

Inherits all methods from [Chunk](#w5h1).

#### Required Dimensions

```python
def required_dimensions(self) -> Set[Dimension]:
    return {Dimension.WHY, Dimension.HOW}
```

#### Example

```python
commit = CommitChunk(
    subject="fix",
    predicate="resolves",
    object="timeout issue",
    dimensions={
        Dimension.WHY: "Users experiencing cart abandonment",
        Dimension.HOW: "Added retry logic with exponential backoff"
    }
)
print(commit.is_complete())  # True
```

---

### SpecChunk

```python
from sixspec.core import SpecChunk
```

Specialized Chunk for full specifications (requires WHO + WHAT + WHY).

Inherits all methods from [Chunk](#w5h1).

#### Required Dimensions

```python
def required_dimensions(self) -> Set[Dimension]:
    return {Dimension.WHO, Dimension.WHAT, Dimension.WHY}
```

#### Example

```python
spec = SpecChunk(
    subject="System",
    predicate="provides",
    object="authentication",
    dimensions={
        Dimension.WHO: "All users",
        Dimension.WHAT: "Secure login system",
        Dimension.WHY: "Protect user data"
    }
)
print(spec.is_complete())  # True
```

---

### BaseActor

```python
from sixspec.core import BaseActor
```

Abstract base class for entities that understand dimensions.

#### Constructor

```python
BaseActor(name: str)
```

**Parameters:**
- `name`: Identifier for this actor

#### Attributes

- `name` (str): Identifier for this actor
- `context` (Dict[Dimension, Any]): Dimensional context maintained by this actor

#### Abstract Methods

##### `understand(spec: Chunk) -> bool`

Check if this actor can process the given specification.

**Parameters:**
- `spec`: Chunk specification to evaluate

**Returns:**
- `bool`: True if actor can process this spec, False otherwise

**Must be implemented by subclasses.**

##### `execute(spec: Chunk) -> Any`

Execute based on specification.

**Parameters:**
- `spec`: Chunk specification to execute

**Returns:**
- `Any`: Result of execution (type varies by actor and spec)

**Must be implemented by subclasses.**

#### Example

```python
class SimpleActor(BaseActor):
    def understand(self, spec: Chunk) -> bool:
        return spec.has(Dimension.WHAT)

    def execute(self, spec: Chunk) -> str:
        return f"Executing: {spec.need(Dimension.WHAT)}"

actor = SimpleActor("TestActor")
```

---

## Agents Module

### NodeAgent

```python
from sixspec.agents import NodeAgent
```

Agent that operates on individual nodes without graph awareness.

Extends [BaseActor](#baseactor).

#### Constructor

```python
NodeAgent(name: str, scope: str)
```

**Parameters:**
- `name`: Identifier for this agent
- `scope`: What kind of node does this operate on? (e.g., "file", "function", "commit")

#### Attributes

- `name` (str): Identifier for this agent
- `scope` (str): Type of node this agent operates on
- `context` (Dict[Dimension, Any]): Dimensional context

#### Methods

##### `understand(spec: Chunk) -> bool`

Check if this agent can process the given specification.

**Parameters:**
- `spec`: Chunk specification to evaluate

**Returns:**
- `bool`: True if spec is complete with dimensions, False otherwise

**Example:**
```python
agent = NodeAgent("TestAgent", "test")
complete = Chunk("A", "B", "C", dimensions={Dimension.WHO: "user"})
print(agent.understand(complete))  # True
```

##### `execute(spec: Chunk) -> Any`

Execute operation on this single node.

**Parameters:**
- `spec`: Chunk specification to execute

**Returns:**
- `Any`: Result from process_node() method

**Raises:**
- `ValueError`: If spec is missing required dimensions

**Example:**
```python
class EchoAgent(NodeAgent):
    def process_node(self, spec):
        return spec.subject

agent = EchoAgent("Echo", "test")
spec = Chunk("Hello", "says", "world")
result = agent.execute(spec)  # Returns "Hello"
```

##### `process_node(spec: Chunk) -> Any`

Process a single node specification (abstract method).

**Parameters:**
- `spec`: Complete Chunk specification to process

**Returns:**
- `Any`: Result of processing (type varies by implementation)

**Must be implemented by subclasses.**

**Example:**
```python
class CounterAgent(NodeAgent):
    def process_node(self, spec):
        return len(spec.dimensions)
```

---

### GraphAgent

```python
from sixspec.agents import GraphAgent
```

Agent that traverses relationships and gathers context from neighbors.

Extends [BaseActor](#baseactor).

#### Constructor

```python
GraphAgent(name: str)
```

**Parameters:**
- `name`: Identifier for this agent

#### Attributes

- `name` (str): Identifier for this agent
- `current_node` (Optional[Chunk]): Current node being processed
- `visited` (Set[str]): Set of visited node identifiers
- `context` (Dict[Dimension, Any]): Dimensional context

#### Methods

##### `understand(spec: Chunk) -> bool`

Check if this agent can process the given specification.

**Parameters:**
- `spec`: Chunk specification to evaluate

**Returns:**
- `bool`: True if spec has any dimensions, False otherwise

##### `execute(spec: Chunk) -> Any`

Execute operation with graph traversal.

**Parameters:**
- `spec`: Chunk specification to execute

**Returns:**
- `Any`: Result from traverse() method

##### `traverse(start: Chunk) -> Any`

Navigate the graph starting from a node (abstract method).

**Parameters:**
- `start`: Starting Chunk node

**Returns:**
- `Any`: Result of traversal

**Must be implemented by subclasses.**

##### `gather_context(spec: Chunk, depth: int = 1) -> List[Chunk]`

Collect neighboring nodes for context.

**Parameters:**
- `spec`: Starting Chunk node
- `depth`: How many hops to traverse (default: 1)

**Returns:**
- `List[Chunk]`: List of neighboring nodes

**Example:**
```python
class ContextAgent(GraphAgent):
    def traverse(self, start):
        context = self.gather_context(start, depth=2)
        return analyze(context)
```

---

## Walkers Module

### DiltsWalker

```python
from sixspec.walkers import DiltsWalker
```

Walker that traverses Dilts hierarchy with WHAT→WHY propagation.

Extends [GraphAgent](#graphagent).

#### Constructor

```python
DiltsWalker(level: DiltsLevel, parent: Optional['DiltsWalker'] = None)
```

**Parameters:**
- `level`: Dilts level this walker operates at
- `parent`: Optional parent walker (one level higher)

**Note:** If parent exists, automatically inherits parent's WHAT as WHY.

#### Attributes

- `name` (str): Unique identifier for this walker
- `level` (DiltsLevel): Dilts level this walker operates at
- `parent` (Optional[DiltsWalker]): Parent walker
- `children` (List[DiltsWalker]): List of child walkers spawned
- `workspace` (Optional[Workspace]): Isolated workspace for execution
- `current_node` (Optional[Chunk]): Current node being processed
- `context` (Dict[Dimension, Any]): Dimensional context (includes inherited WHY)

#### Methods

##### `add_context(dim: Dimension, value: str) -> None`

Add dimensional context to this walker.

**Parameters:**
- `dim`: Dimension to add
- `value`: Value for dimension

**Example:**
```python
walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
walker.add_context(Dimension.WHY, "Build feature")
```

##### `traverse(start: Chunk) -> Any`

Traverse down the Dilts hierarchy with WHAT→WHY propagation.

**Parameters:**
- `start`: Chunk specification to execute

**Returns:**
- `Any`: Result from ground action or child execution

**Example:**
```python
walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
spec = Chunk("System", "needs", "feature",
           dimensions={Dimension.WHAT: "Integrate payment"})
result = walker.traverse(spec)
```

##### `spawn_children(n_strategies: int, base_spec: Chunk) -> List[Tuple[DiltsWalker, Chunk]]`

Spawn multiple children exploring different approaches.

**Parameters:**
- `n_strategies`: Number of different strategies to try
- `base_spec`: Base specification for children

**Returns:**
- `List[Tuple[DiltsWalker, Chunk]]`: List of (child_walker, child_spec) tuples

**Example:**
```python
walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
spec = Chunk("System", "needs", "payment",
           dimensions={Dimension.WHAT: "Integrate payment"})
children = walker.spawn_children(3, spec)  # 3 different strategies
```

##### `execute_portfolio(spec: Chunk, n_strategies: int = 3) -> Any`

Execute multiple strategies in parallel and pick winner.

**Parameters:**
- `spec`: Specification to execute
- `n_strategies`: Number of strategies to try (default: 3)

**Returns:**
- `Any`: Best result from portfolio based on validation scores

**Raises:**
- `RuntimeError`: If all strategies fail validation

**Example:**
```python
walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
spec = Chunk("System", "needs", "payment",
           dimensions={
               Dimension.WHAT: "Integrate payment",
               Dimension.WHY: "Launch premium"
           })
result = walker.execute_portfolio(spec, n_strategies=3)
```

##### `trace_provenance() -> List[str]`

Trace WHY chain from here to root.

**Returns:**
- `List[str]`: List of WHAT values from root to current

**Example:**
```python
chain = walker.trace_provenance()
# Returns: ["Increase revenue", "Launch premium", "Build payment", ...]
```

##### `execute_ground_action(spec: Chunk) -> str`

Level 1: Actually execute the specified action.

**Parameters:**
- `spec`: Specification with ground-level action

**Returns:**
- `str`: Result string describing execution

**Example:**
```python
walker = DiltsWalker(level=DiltsLevel.ENVIRONMENT)
spec = Chunk("System", "executes", "action",
           dimensions={
               Dimension.WHAT: "Run tests",
               Dimension.WHY: "Verify implementation"
           })
result = walker.execute_ground_action(spec)
# Returns: "EXECUTED: Run tests (because: Verify implementation)"
```

##### `generate_strategies(spec: Chunk, n: int) -> List[str]`

Generate n different strategies for achieving the goal.

**Parameters:**
- `spec`: Specification describing goal
- `n`: Number of strategies to generate

**Returns:**
- `List[str]`: List of strategy descriptions (WHAT values)

**Override this method in subclasses for domain-specific strategies.**

**Example:**
```python
class CustomWalker(DiltsWalker):
    def generate_strategies(self, spec, n):
        base = spec.need(Dimension.WHAT) or "action"
        return [f"{base} - Strategy {i+1}" for i in range(n)]
```

##### `validate(result: Any) -> ValidationResult`

Validate the result of execution.

**Parameters:**
- `result`: Result from execution

**Returns:**
- `ValidationResult`: Validation result with score and pass/fail status

**Override this method in subclasses for domain-specific validation.**

**Example:**
```python
class CustomWalker(DiltsWalker):
    def validate(self, result):
        score = 0.8 if result else 0.0
        return ValidationResult(
            score=score,
            passed=bool(result),
            details="Validation details"
        )
```

---

### A2AWalker

```python
from sixspec.walkers import A2AWalker
```

DiltsWalker enhanced with Google A2A protocol for graceful interruption.

Extends [DiltsWalker](#diltswalker).

#### Constructor

```python
A2AWalker(level: DiltsLevel, parent: Optional['DiltsWalker'] = None)
```

**Parameters:**
- `level`: Dilts level this walker operates at
- `parent`: Optional parent walker

#### Additional Attributes

- `task` (Task): A2A task instance for lifecycle management

#### Methods

Inherits all methods from [DiltsWalker](#diltswalker), plus:

##### Access to Task Lifecycle

```python
# Start task
walker.task.start()

# Pause gracefully
walker.task.pause()

# Resume from pause
walker.task.resume()

# Complete successfully
walker.task.complete(result)

# Fail with error
walker.task.fail(error_message)
```

**Example:**
```python
walker = A2AWalker(level=DiltsLevel.CAPABILITY)

# Subscribe to status updates
def handle_status(update):
    print(f"Status: {update.status}")

walker.task.on_status_change(handle_status)

# Execute with pause capability
walker.task.start()
result = walker.execute(spec)

# Can pause and resume gracefully
walker.task.pause()  # Preserves all context
walker.task.resume()  # Continues exactly where it left off
```

---

### Workspace

```python
from sixspec.walkers import Workspace
```

Isolated execution environment per walker.

#### Constructor

```python
Workspace(walker_id: str)
```

**Parameters:**
- `walker_id`: Identifier for the walker owning this workspace

#### Attributes

- `walker_id` (str): Identifier for the walker
- `data` (Dict[str, Any]): Storage for workspace data
- `created_at` (datetime): Timestamp of creation

#### Methods

##### `store(key: str, value: Any) -> None`

Store data in workspace.

**Parameters:**
- `key`: Storage key
- `value`: Value to store

**Example:**
```python
workspace = Workspace("walker-123")
workspace.store("temp_data", {"result": 42})
```

##### `retrieve(key: str) -> Optional[Any]`

Retrieve data from workspace.

**Parameters:**
- `key`: Storage key

**Returns:**
- `Optional[Any]`: Stored value, or None if key not found

**Example:**
```python
data = workspace.retrieve("temp_data")
if data:
    print(data["result"])
```

##### `clear() -> None`

Clear all workspace data.

**Example:**
```python
workspace.clear()
```

---

### ValidationResult

```python
from sixspec.walkers import ValidationResult
```

Result of validating an execution outcome.

#### Constructor

```python
ValidationResult(score: float, passed: bool, details: str = "")
```

**Parameters:**
- `score`: Validation score (higher is better)
- `passed`: Whether validation passed minimum threshold
- `details`: Additional validation details (default: "")

#### Attributes

- `score` (float): Validation score
- `passed` (bool): Pass/fail status
- `details` (str): Validation details

#### Example

```python
result = ValidationResult(
    score=0.9,
    passed=True,
    details="All tests passed with 95% coverage"
)
```

---

### MissionWalker

```python
from sixspec.walkers import MissionWalker
```

Level 6 walker (Mission level) with extreme autonomy.

Extends [DiltsWalker](#diltswalker) with Mission-specific strategies.

#### Constructor

```python
MissionWalker()
```

Automatically sets level to `DiltsLevel.MISSION`.

#### Example

```python
walker = MissionWalker()
spec = Chunk(
    subject="Company",
    predicate="aims",
    object="growth",
    dimensions={Dimension.WHAT: "Achieve market leadership"}
)
result = walker.execute(spec)
```

---

### CapabilityWalker

```python
from sixspec.walkers import CapabilityWalker
```

Level 3 walker (Capability level) with low autonomy.

Extends [DiltsWalker](#diltswalker) with Capability-specific strategies.

#### Constructor

```python
CapabilityWalker()
```

Automatically sets level to `DiltsLevel.CAPABILITY`.

#### Example

```python
walker = CapabilityWalker()
spec = Chunk(
    subject="Team",
    predicate="implements",
    object="feature",
    dimensions={Dimension.WHAT: "Integrate payment processing"}
)
result = walker.execute(spec)
```

---

## Git Module

### CommitMessageParser

```python
from sixspec.git.parser import CommitMessageParser
```

Parse dimensional commit messages into CommitChunk objects.

#### Class Methods

##### `parse(commit_msg: str, commit_hash: str = "") -> CommitChunk`

Parse commit message into CommitChunk object.

**Parameters:**
- `commit_msg`: The commit message text
- `commit_hash`: The git commit hash (optional)

**Returns:**
- `CommitChunk`: Parsed commit object

**Raises:**
- `ValueError`: If message format is invalid

**Example:**
```python
msg = """fix: payment timeout

WHY: Users abandoning carts
HOW: Added retry logic"""

commit = CommitMessageParser.parse(msg, "abc123")
print(commit.need(Dimension.WHY))  # "Users abandoning carts"
```

##### `parse_git_log(repo_path: Path, n: Optional[int] = None, skip_invalid: bool = True) -> List[CommitChunk]`

Parse recent commits from git log.

**Parameters:**
- `repo_path`: Path to git repository
- `n`: Number of commits to fetch (None for all)
- `skip_invalid`: If True, skip invalid commits; if False, raise ValueError

**Returns:**
- `List[CommitChunk]`: List of parsed commit objects

**Raises:**
- `ValueError`: If git command fails or if skip_invalid=False and invalid commit found

**Example:**
```python
from pathlib import Path

commits = CommitMessageParser.parse_git_log(
    Path("/repo"),
    n=10,
    skip_invalid=True
)
```

---

### DimensionalGitHistory

```python
from sixspec.git.history import DimensionalGitHistory
```

Queryable commit history with dimensional filtering.

#### Constructor

```python
DimensionalGitHistory(repo_path: Path)
```

**Parameters:**
- `repo_path`: Path to git repository

**Example:**
```python
from pathlib import Path

history = DimensionalGitHistory(Path("."))
```

#### Attributes

- `repo_path` (Path): Path to git repository
- `commits` (List[CommitChunk]): List of dimensional commits

#### Methods

##### `query(where: str = None, why: str = None, what: str = None, who: str = None, when: str = None, how: str = None, commit_type: str = None) -> List[CommitChunk]`

Query commits by any dimension.

**Parameters:**
- `where`: Filter by WHERE dimension (case-insensitive substring)
- `why`: Filter by WHY dimension
- `what`: Filter by WHAT dimension
- `who`: Filter by WHO dimension
- `when`: Filter by WHEN dimension
- `how`: Filter by HOW dimension
- `commit_type`: Filter by commit type (feat, fix, etc.)

**Returns:**
- `List[CommitChunk]`: List of matching commits

**Example:**
```python
# Find payment-related fixes
payment_fixes = history.query(where="payment", commit_type="fix")

# Find timeout issues
timeout_issues = history.query(why="timeout")

# Combined query
results = history.query(
    where="payment",
    why="timeout",
    commit_type="fix"
)
```

##### `trace_file_purpose(file_path: str) -> List[CommitChunk]`

Find all commits affecting a specific file.

**Parameters:**
- `file_path`: Path to file (substring match in WHERE dimension)

**Returns:**
- `List[CommitChunk]`: List of commits affecting the file

**Example:**
```python
file_commits = history.trace_file_purpose("src/payment/stripe.py")
for commit in file_commits:
    print(f"{commit.object}: {commit.need(Dimension.WHY)}")
```

##### `get_purposes() -> List[str]`

Get all unique WHY values.

**Returns:**
- `List[str]`: List of unique purposes

**Example:**
```python
purposes = history.get_purposes()
print(f"Found {len(purposes)} unique purposes")
```

##### `get_affected_files() -> List[str]`

Get all unique WHERE values.

**Returns:**
- `List[str]`: List of unique file paths

**Example:**
```python
files = history.get_affected_files()
print(f"Commits affected {len(files)} files")
```

##### `get_commit_types() -> List[str]`

Get all unique commit types used.

**Returns:**
- `List[str]`: List of unique commit types

**Example:**
```python
types = history.get_commit_types()
print(f"Commit types: {', '.join(types)}")
```

##### `reload() -> None`

Force refresh from git.

**Example:**
```python
history.reload()  # Re-parse git log
```

---

## A2A Module

### Task

```python
from sixspec.a2a import Task
```

A2A-compatible task with lifecycle management.

#### Constructor

```python
Task(task_id: Optional[str] = None, parent: Optional['Task'] = None)
```

**Parameters:**
- `task_id`: Optional task identifier (generated if not provided)
- `parent`: Optional parent task for hierarchical coordination

#### Attributes

- `task_id` (str): Unique identifier
- `status` (TaskStatus): Current task status
- `result` (Optional[Any]): Result data (when completed)
- `error` (Optional[str]): Error message (when failed)
- `parent` (Optional[Task]): Parent task
- `children` (List[Task]): List of child tasks
- `status_callbacks` (List[Callable]): Callbacks invoked on status change

#### Methods

##### `start() -> None`

Start task execution (PENDING → RUNNING).

**Raises:**
- `RuntimeError`: If task is not in PENDING state

**Example:**
```python
task = Task()
task.start()
```

##### `pause() -> None`

Pause task execution gracefully (RUNNING → PAUSED).

Cascades pause to all children.

**Raises:**
- `RuntimeError`: If task is not RUNNING

**Example:**
```python
task.pause()
```

##### `resume() -> None`

Resume task execution (PAUSED → RUNNING).

Resumes children first (bottom-up).

**Raises:**
- `RuntimeError`: If task is not PAUSED

**Example:**
```python
task.resume()
```

##### `complete(result: Any = None) -> None`

Mark task as completed successfully.

**Parameters:**
- `result`: Optional result data

**Raises:**
- `RuntimeError`: If task is already in terminal state

**Example:**
```python
task.complete("Success!")
```

##### `fail(error: str) -> None`

Mark task as failed.

**Parameters:**
- `error`: Error message describing failure

**Raises:**
- `RuntimeError`: If task is already in terminal state

**Example:**
```python
task.fail("Connection timeout")
```

##### `add_child(child: Task) -> None`

Add a child task.

**Parameters:**
- `child`: Child task to add

##### `on_status_change(callback: Callable[[StatusUpdate], None]) -> None`

Register a callback for status changes.

**Parameters:**
- `callback`: Function called with StatusUpdate on status change

**Example:**
```python
def handle_update(update):
    print(f"Status: {update.status}")

task.on_status_change(handle_update)
```

##### `to_dict() -> dict`

Serialize task to dictionary.

**Returns:**
- `dict`: Dictionary representation of task state

---

### TaskStatus

```python
from sixspec.a2a import TaskStatus
```

Enumeration of task states.

#### Values

```python
TaskStatus.PENDING = "pending"
TaskStatus.RUNNING = "running"
TaskStatus.PAUSED = "paused"
TaskStatus.COMPLETED = "completed"
TaskStatus.FAILED = "failed"
```

#### Methods

##### `can_pause() -> bool`

Check if task can be paused from current state.

**Returns:**
- `bool`: True if status is RUNNING

##### `can_resume() -> bool`

Check if task can be resumed from current state.

**Returns:**
- `bool`: True if status is PAUSED

##### `is_terminal() -> bool`

Check if this is a terminal state.

**Returns:**
- `bool`: True if status is COMPLETED or FAILED

---

### StatusUpdate

```python
from sixspec.a2a import StatusUpdate
```

Real-time status update for task lifecycle.

#### Constructor

```python
StatusUpdate(
    task_id: str,
    status: TaskStatus,
    result: Optional[Any],
    error: Optional[str],
    metadata: dict
)
```

#### Attributes

- `task_id` (str): Task identifier
- `status` (TaskStatus): Current status
- `result` (Optional[Any]): Result if completed
- `error` (Optional[str]): Error if failed
- `metadata` (dict): Additional metadata

---

## Usage Patterns

### Pattern 1: Basic Dimensional Spec

```python
from sixspec.core import Chunk, Dimension

spec = Chunk("User", "wants", "feature")
spec.set(Dimension.WHO, "Premium users", confidence=0.9)
spec.set(Dimension.WHAT, "Export to PDF", confidence=0.7)
spec.set(Dimension.WHY, "Data portability requirements")

if spec.get_confidence(Dimension.WHAT) < 0.8:
    # Low confidence, need validation
    validate_approach(spec)
```

### Pattern 2: Custom Agent

```python
from sixspec.agents import NodeAgent
from sixspec.core import Chunk, Dimension

class MyAgent(NodeAgent):
    def __init__(self):
        super().__init__("MyAgent", scope="custom")

    def process_node(self, spec: Chunk) -> Any:
        # Your processing logic
        return process(spec)

agent = MyAgent()
result = agent.execute(spec)
```

### Pattern 3: Hierarchical Execution

```python
from sixspec.walkers import DiltsWalker
from sixspec.core import DiltsLevel, Chunk, Dimension

walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
spec = Chunk(
    subject="Team",
    predicate="builds",
    object="feature",
    dimensions={Dimension.WHAT: "Integrate payment"}
)

result = walker.traverse(spec)
provenance = walker.trace_provenance()
```

### Pattern 4: Portfolio Execution

```python
class CustomWalker(DiltsWalker):
    def generate_strategies(self, spec, n):
        # Generate n strategies
        return [f"Strategy {i}" for i in range(n)]

    def validate(self, result):
        # Validate result
        return ValidationResult(score=0.8, passed=True)

walker = CustomWalker(level=DiltsLevel.CAPABILITY)
result = walker.execute_portfolio(spec, n_strategies=3)
```

### Pattern 5: Git History Query

```python
from sixspec.git.history import DimensionalGitHistory
from pathlib import Path

history = DimensionalGitHistory(Path("."))
results = history.query(where="payment", commit_type="fix")

for commit in results:
    print(f"{commit.object}")
    print(f"  WHY: {commit.need(Dimension.WHY)}")
    print(f"  HOW: {commit.need(Dimension.HOW)}")
```

---

## Error Handling

### Common Exceptions

```python
# ValueError: Invalid confidence score
spec.set(Dimension.WHO, "user", confidence=1.5)  # Raises ValueError

# ValueError: Missing required dimensions
commit = CommitChunk("fix", "resolves", "bug")
commit.is_complete()  # False, missing WHY and HOW

# RuntimeError: Invalid state transition
task = Task()
task.pause()  # Raises RuntimeError (not running)

# ValueError: Invalid commit message
CommitMessageParser.parse("Invalid message")  # Raises ValueError
```

---

This API reference covers all public interfaces in SixSpec. For usage examples, see [TUTORIAL.md](TUTORIAL.md). For architectural details, see [ARCHITECTURE.md](ARCHITECTURE.md).
