# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SixSpec is a dimensional specification framework that combines the 5W1H model (Who, What, When, Where, Why, How) with Dilts' Logical Levels to create self-documenting, traceable, and queryable systems. The framework's core principle: **Parent's WHAT becomes child's WHY** - creating full traceability from mission to implementation.

## Core Concepts

### Terminology (Updated 2025)
- **Chunk** (formerly W5H1): Universal container for dimensional specifications with subject-predicate-object structure
- **5W1H** (not W5H1): The proper term for the five W's + How framework
- **Dimension**: The six dimensions (WHO, WHAT, WHEN, WHERE, WHY, HOW)
- **DiltsLevel**: Hierarchical levels (MISSION=6, IDENTITY=5, BELIEFS=4, CAPABILITY=3, BEHAVIOR=2, ENVIRONMENT=1)

### Key Architecture Principles
1. **Purpose Propagation**: Parent's WHAT always becomes child's WHY
2. **Validation Over Prediction**: Portfolio execution validates actual results, not predicted confidence
3. **Lazy Evaluation**: Use `need()` for on-demand dimension access instead of requiring all dimensions upfront
4. **Confidence Tracking**: Track certainty per dimension, not per spec
5. **Hierarchical Autonomy**: Autonomy decreases as you descend from Mission (L6) to Environment (L1)

## Common Development Commands

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/git/test_parser.py
pytest tests/core/test_hypergraph.py

# Run with coverage
pytest --cov=sixspec tests/

# Run specific test class or function
pytest tests/git/test_parser.py::TestCommitMessageParser
pytest tests/git/test_parser.py::TestCommitMessageParser::test_parse_basic_commit
```

### Installation
```bash
# Install package in development mode
pip install -e .

# Install with dev dependencies (includes pytest)
pip install -e ".[dev]"

# Install git hook for dimensional commits
cp sixspec/git/hooks/commit-msg .git/hooks/
chmod +x .git/hooks/commit-msg

# Configure commit message template
git config commit.template templates/.gitmessage
```

### Git Workflow
```bash
# Make dimensional commit (WHY and HOW are mandatory)
git commit -m "fix: payment timeout

WHY: Users abandoning carts at 25% rate
HOW: Added retry logic with exponential backoff"

# Query dimensional history
python -c "from pathlib import Path; from sixspec.git.history import DimensionalGitHistory; h = DimensionalGitHistory(Path('.')); print([c.commit_hash[:7] for c in h.query(where='payment')])"
```

## Architecture Overview

### Layer Structure
```
Application Layer → Walker Layer → Agent Layer → Core Layer → Integration Layer
```

### Core Layer (`sixspec/core/`)
- **models.py**: Dimension enum, DiltsLevel enum, Chunk class, CommitChunk, SpecChunk
- **hypergraph.py**: Graph operations for dimensional specifications

**Important**: Recent refactor renamed W5H1 → Chunk. When editing core code:
- Use `Chunk` for the base class
- Use `CommitChunk` for Git commits (requires WHY + HOW)
- Use `SpecChunk` for full specifications (requires WHO + WHAT + WHY)

### Agent Layer (`sixspec/agents/`)
- **BaseActor**: Abstract interface for understanding and executing specs
- **NodeAgent**: Operates on isolated specs (e.g., TreeSitter, linters)
- **GraphAgent**: Traverses relationships and gathers context (e.g., dependency analysis)

### Walker Layer (`sixspec/walkers/`)
- **DiltsWalker**: Core hierarchical delegation with WHAT→WHY propagation
- **A2AWalker**: Adds Google A2A protocol for graceful pause/resume
- **Workspace**: Isolated execution environment per walker
- **Strategies**: Level-specific implementations (MissionWalker, CapabilityWalker)

### Git Integration (`sixspec/git/`)
- **parser.py**: `CommitMessageParser` - Parses dimensional commits into CommitChunk objects
- **history.py**: `DimensionalGitHistory` - Queryable commit history
- **hooks/commit-msg**: Git hook that validates WHY and HOW dimensions

### A2A Integration (`sixspec/a2a/`)
- **task.py**: `Task` class with lifecycle (PENDING → RUNNING → PAUSED/COMPLETED/FAILED)
- **status.py**: `TaskStatus` enum and `StatusUpdate` for real-time streaming

## Code Patterns

### Creating Dimensional Specifications
```python
from sixspec.core import Chunk, Dimension

# Basic Chunk
spec = Chunk(
    subject="System",
    predicate="needs",
    object="payment processing",
    dimensions={
        Dimension.WHY: "Enable premium subscriptions",
        Dimension.WHAT: "Stripe integration",
        Dimension.HOW: "Using Stripe Checkout API"
    }
)

# Access dimensions (lazy evaluation)
why = spec.need(Dimension.WHY)  # Returns value or None
if spec.has(Dimension.HOW):
    how = spec.need(Dimension.HOW)

# Set with confidence
spec.set(Dimension.WHERE, "payment service", confidence=0.9)
```

### Purpose Propagation (Critical Pattern)
```python
# Parent defines WHAT
parent = Chunk("System", "needs", "billing",
    dimensions={Dimension.WHAT: "Build billing system"})

# Child inherits parent's WHAT as WHY
child = Chunk("Dev", "integrates", "Stripe",
    dimensions={
        Dimension.WHY: parent.need(Dimension.WHAT),  # ← This is required
        Dimension.WHAT: "Integrate Stripe API"
    })
```

### Walker Delegation
```python
from sixspec.walkers import DiltsWalker
from sixspec.core import DiltsLevel

# Create walker at specific level
walker = DiltsWalker(level=DiltsLevel.CAPABILITY)

# Traverse down hierarchy (delegates to child levels)
result = walker.traverse(spec)

# Trace provenance back to root
provenance_chain = walker.trace_provenance()  # Returns list of WHY values
```

### Git Commit Parsing
```python
from pathlib import Path
from sixspec.git.parser import CommitMessageParser
from sixspec.git.history import DimensionalGitHistory

# Parse single commit
commit = CommitMessageParser.parse(commit_msg, commit_hash)
print(commit.need(Dimension.WHY))
print(commit.commit_type)  # feat, fix, refactor, etc.

# Query history
history = DimensionalGitHistory(Path("/path/to/repo"))
payment_fixes = history.query(where="payment", commit_type="fix")
timeout_issues = history.query(why="timeout")
file_history = history.trace_file_purpose("src/payment/stripe.py")
```

## File Organization

```
sixspec/
├── core/
│   ├── models.py          # Dimension, DiltsLevel, Chunk, CommitChunk
│   └── hypergraph.py      # Graph operations
├── agents/
│   ├── node_agent.py      # Isolated operations
│   ├── graph_agent.py     # Context-aware traversal
│   └── examples/          # Example implementations
├── walkers/
│   ├── dilts_walker.py    # Hierarchical delegation
│   ├── a2a_walker.py      # A2A protocol integration
│   ├── workspace.py       # Isolated execution environment
│   └── strategies/        # Level-specific walkers
├── git/
│   ├── parser.py          # Commit message parsing
│   ├── history.py         # Queryable history
│   └── hooks/
│       └── commit-msg     # Validation hook
└── a2a/
    ├── task.py            # Task lifecycle
    └── status.py          # Status updates

tests/
├── core/                  # Core model tests
├── agents/                # Agent tests
├── walkers/               # Walker tests
├── git/                   # Git integration tests
└── a2a/                   # A2A protocol tests
```

## Important Constraints

### Commit Message Format
All commits MUST include:
- Type: `feat`, `fix`, `refactor`, `docs`, `test`, or `chore`
- WHY dimension (purpose/business value)
- HOW dimension (technical approach)

Optional dimensions: WHAT, WHERE, WHEN, WHO

The git hook at `sixspec/git/hooks/commit-msg` enforces this.

### WHAT→WHY Chain
**Never break the purpose chain.** When creating child specifications or walkers:
```python
# ✓ Correct
child_dimensions = {
    Dimension.WHY: parent.need(Dimension.WHAT),
    Dimension.WHAT: "Child's action"
}

# ✗ Wrong - loses context
child_dimensions = {
    Dimension.WHAT: "Child's action"
}
```

### Validation Pattern
In portfolio execution, always validate results, never predict:
```python
# ✓ Correct - validate actual results
def validate(self, result: Any) -> ValidationResult:
    score = run_tests(result)
    return ValidationResult(score=score, passed=score > 0.8)

# ✗ Wrong - predicting before execution
def estimate_confidence(self, strategy: str) -> float:
    return 0.8  # Guessing
```

## Common Gotchas

1. **Import paths**: After W5H1→Chunk rename, use:
   ```python
   from sixspec.core import Chunk, CommitChunk, Dimension
   # NOT: from sixspec.core import W5H1
   ```

2. **Dimension access**: Use `need()` for lazy evaluation:
   ```python
   why = spec.need(Dimension.WHY)  # ✓ Returns None if missing
   why = spec.dimensions[Dimension.WHY]  # ✗ Raises KeyError
   ```

3. **Confidence defaults**: When not specified, confidence defaults to 1.0

4. **Dilts levels**: Remember the mapping:
   - MISSION (L6): FOR_WHAT dimension, extreme autonomy
   - IDENTITY (L5): WHO dimension, high autonomy
   - BELIEFS (L4): WHY dimension, moderate autonomy
   - CAPABILITY (L3): HOW dimension, low autonomy
   - BEHAVIOR (L2): WHAT dimension, very low autonomy
   - ENVIRONMENT (L1): WHERE/WHEN dimensions, zero autonomy

5. **Test fixtures**: Git tests use `tests/git/fixtures/sample_commits.txt` for test data

## Development Philosophy

From DESIGN_PHILOSOPHY.md:

- **Dimensional Completeness**: Capture all six dimensions when relevant
- **Purpose Propagation**: Parent's WHAT → Child's WHY
- **Validation Over Prediction**: Validate actual results, not predicted confidence
- **Lazy Evaluation**: Don't demand what you don't need
- **Confidence Tracking**: Per-dimension confidence, not per-spec
- **Hierarchical Autonomy**: Freedom decreases from Mission to Environment
- **Graceful Interruption**: A2A enables pause/resume without context loss
- **Self-Documentation**: Git history as queryable documentation

## Dependencies

- Python 3.9+
- pytest 7.0+ (dev dependency)
- No runtime dependencies (pure Python)

Future optional dependencies for A2A integration will include `agent2agent` and `grpcio` when Google's A2A library becomes available.
