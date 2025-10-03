# SixSpec

Dimensional specification framework for making Git history queryable and self-documenting.

## Overview

SixSpec implements dimensional commit messages based on the 5W1H framework (Who, What, When, Where, How, Why). This makes your Git history a queryable dimensional graph that both humans and AI agents can reason about.

## Key Features

- **Dimensional Commit Format**: Commits include mandatory WHY (purpose) and HOW (approach) dimensions
- **Git Hook Validation**: Automatic validation ensures dimensional format compliance
- **Queryable History**: Search commits by purpose, affected files, technical approach, and more
- **Self-Documenting**: Git history becomes documentation that explains both what changed and why
- **Agent-Friendly**: AI agents can understand context and trace purpose through commit history

## Installation

```bash
# Install the package
pip install -e .

# Install git hook in your repository
cp sixspec/git/hooks/commit-msg .git/hooks/
chmod +x .git/hooks/commit-msg

# Configure commit template
git config commit.template templates/.gitmessage
```

## Commit Message Format

### Required Structure

```
<type>: <subject>

WHY: <purpose/business value>
HOW: <technical approach>

[optional dimensions]
WHAT: <specific change>
WHERE: <files/components>
WHEN: <conditions/triggers>
WHO: <users/systems affected>
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `docs`: Documentation
- `test`: Tests
- `chore`: Maintenance

### Examples

#### Bug Fix

```
fix: payment API timeout

WHY: Users abandoning carts at 25% rate due to timeout
HOW: Added retry logic with exponential backoff (3 attempts)
WHAT: Payment intent creation flow
WHERE: src/payment/stripe_integration.py
```

#### Feature

```
feat: add search filters

WHY: Users cannot find products efficiently
HOW: Implemented faceted search with Elasticsearch
WHAT: Product search endpoint
WHERE: src/search/api.py
WHO: All users
```

#### Refactor

```
refactor: extract payment validation

WHY: Code duplication across payment methods
HOW: Created shared validation module
WHERE: src/payment/validation.py, src/payment/stripe.py
```

## Usage

### Basic Parsing

```python
from sixspec.git.parser import CommitMessageParser

# Parse a single commit message
commit_msg = """fix: payment timeout

WHY: Users abandoning carts
HOW: Added retry logic"""

commit = CommitMessageParser.parse(commit_msg, "abc123")

print(commit.need(Dimension.WHY))  # "Users abandoning carts"
print(commit.need(Dimension.HOW))  # "Added retry logic"
print(commit.commit_type)  # "fix"
```

### Querying Git History

```python
from pathlib import Path
from sixspec.git.history import DimensionalGitHistory

# Load dimensional commits from a repo
history = DimensionalGitHistory(Path("/path/to/repo"))

# Find commits by purpose
user_experience_commits = history.query(why="user experience")

# Find commits affecting payment code
payment_commits = history.query(where="payment")

# Find all bug fixes related to payment
payment_fixes = history.query(where="payment", commit_type="fix")

# Trace purpose of a file
commits = history.trace_file_purpose("src/payment/stripe.py")
for commit in commits:
    print(f"{commit.commit_hash}: {commit.need(Dimension.WHY)}")

# Get all unique purposes
purposes = history.get_purposes()

# Get all affected files
files = history.get_affected_files()
```

### Advanced Queries

```python
# Multiple dimension filters
results = history.query(
    where="payment",
    why="timeout",
    commit_type="fix"
)

# Case-insensitive matching
results = history.query(where="PayMent")  # matches "payment", "PAYMENT", etc.

# Get all commits (empty query)
all_commits = history.query()
```

## Core Data Structures

### Dimension Enum

```python
from sixspec.core import Dimension

# The six dimensions
Dimension.WHO   # Users, systems affected
Dimension.WHAT  # Specific changes
Dimension.WHEN  # Conditions, triggers
Dimension.WHERE # Files, components
Dimension.HOW   # Technical approach
Dimension.WHY   # Purpose, business value
```

### Chunk

Base class for dimensional objects with subject-predicate-object structure.

```python
from sixspec.core import Chunk, Dimension

obj = Chunk(
    subject="developer",
    predicate="implements",
    object="feature",
    dimensions={
        Dimension.WHY: "improve user experience",
        Dimension.HOW: "using React components"
    }
)

# Check and access dimensions
if obj.has(Dimension.WHY):
    print(obj.need(Dimension.WHY))  # Raises KeyError if missing

optional = obj.get(Dimension.WHO, default="unknown")  # Safe with default
```

### CommitChunk

Specialized Chunk for Git commits. Requires WHY and HOW dimensions.

```python
from sixspec.core import CommitChunk, Dimension

commit = CommitChunk(
    subject="fix",
    predicate="changes",
    object="payment timeout",
    dimensions={
        Dimension.WHY: "Users abandoning carts",
        Dimension.HOW: "Added retry logic"
    },
    metadata={
        'commit_hash': 'abc123',
        'commit_type': 'fix'
    }
)

print(commit.commit_hash)  # "abc123"
print(commit.commit_type)  # "fix"
```

## Git Hook

The `commit-msg` hook validates commits before they're accepted:

```python
# sixspec/git/hooks/commit-msg

# Validates:
✓ Commit type (feat, fix, refactor, docs, test, chore)
✓ WHY dimension present
✓ HOW dimension present
✓ Skips merge commits
✓ Ignores comment lines
```

## Running Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run specific test file
pytest tests/git/test_parser.py

# Run with coverage
pytest --cov=sixspec tests/
```

## Project Structure

```
sixspec/
  __init__.py
  core.py              # Chunk, Dimension, CommitChunk
  git/
    __init__.py
    parser.py          # CommitMessageParser
    history.py         # DimensionalGitHistory
    hooks/
      commit-msg       # Git hook validation script

templates/
  .gitmessage          # Commit message template

tests/
  git/
    test_parser.py     # Parser tests
    test_history.py    # History query tests
    test_hooks.py      # Hook validation tests
    fixtures/
      sample_commits.txt
```

## Benefits

### Immediate Value

- **Better commit messages**: Developers must explain WHY and HOW
- **Searchable history**: Find commits by purpose, not just text
- **Self-documenting**: Git history explains the evolution of the codebase
- **Code review context**: Reviewers understand the reasoning behind changes

### Future Value (With Full Framework)

- **Test generation**: Test agents know what to test from WHY/HOW
- **Documentation automation**: Docs agents update from commits
- **Purpose tracing**: Agents trace requirements through to implementation
- **Full provenance**: Track from mission → objectives → features → commits

## Philosophy

Traditional commit messages answer "what changed?" Dimensional commits answer:

- **WHY** did we make this change? (purpose, business value)
- **HOW** did we implement it? (technical approach)
- **WHERE** did we change it? (files, components)
- **WHAT** specifically changed? (detailed changes)
- **WHO** is affected? (users, systems)
- **WHEN** does it apply? (conditions, triggers)

This makes Git history a dimensional graph that captures not just changes, but context and reasoning.

## Development Status

**Phase 1**: ✅ Complete
- Core data structures (Chunk, Dimension, CommitChunk)
- Commit message parser
- Git hook validation
- Dimensional history queries
- Comprehensive test suite

**Phase 2**: Planned
- CLI tool for installation and migration
- Interactive commit message builder
- Git log visualization
- Integration with other SixSpec components

## Dependencies

- Python 3.9+
- Git
- pytest (for testing)

## License

MIT

## Contributing

This is part of the SixSpec framework. See the main SixSpec documentation for contribution guidelines.

## Related

- Linear Issue: [IMA-84](https://linear.app/imajn/issue/IMA-84/implement-dimensional-commit-message-format-and-git-hooks)
- Depends on: [IMA-75](https://linear.app/imajn/issue/IMA-75/implement-core-w5h1object-data-structures) (CommitChunk class)