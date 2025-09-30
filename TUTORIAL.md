# SixSpec Tutorial

Welcome to SixSpec! This tutorial will teach you the framework from the ground up through hands-on examples.

## Learning Path

1. **Basics**: Understanding W5H1 and dimensions
2. **Git Integration**: Dimensional commits
3. **Agents**: Building dimensional-aware agents
4. **Walkers**: Hierarchical execution
5. **Advanced**: Portfolio execution and A2A integration

---

## Part 1: Understanding W5H1

### What is W5H1?

W5H1 is a dimensional specification model that captures complete context using six dimensions:
- **WHO**: Actors, stakeholders
- **WHAT**: Actions, objects
- **WHEN**: Temporal context
- **WHERE**: Spatial context
- **HOW**: Methods, processes
- **WHY**: Purpose, motivation

### Exercise 1.1: Your First W5H1 Spec

```python
from sixspec.core import W5H1, Dimension

# Create a simple specification
spec = W5H1(
    subject="User",
    predicate="wants",
    object="feature"
)

# Add dimensions
spec.set(Dimension.WHO, "Premium users")
spec.set(Dimension.WHAT, "Advanced reporting dashboard")
spec.set(Dimension.WHY, "Better insights into business metrics")
spec.set(Dimension.WHERE, "Dashboard section")
spec.set(Dimension.HOW, "React components with Chart.js")

# Access dimensions
print(spec.need(Dimension.WHY))
# Output: Better insights into business metrics

# Check if dimension exists
if spec.has(Dimension.WHO):
    print(f"Target: {spec.need(Dimension.WHO)}")
# Output: Target: Premium users
```

**Key Concepts:**
- Use `set()` to add dimensions with confidence scores
- Use `need()` to retrieve dimensions (returns None if missing)
- Use `has()` to check if dimension exists

### Exercise 1.2: Confidence Tracking

```python
# Add dimensions with confidence scores
spec = W5H1("System", "needs", "authentication")

# High confidence: Requirements are clear
spec.set(Dimension.WHO, "All users", confidence=1.0)

# Medium confidence: Approach is chosen but not finalized
spec.set(Dimension.HOW, "OAuth2 with JWT tokens", confidence=0.7)

# Low confidence: Still exploring options
spec.set(Dimension.WHERE, "Frontend and backend", confidence=0.4)

# Make decisions based on confidence
for dim in [Dimension.WHO, Dimension.HOW, Dimension.WHERE]:
    confidence = spec.get_confidence(dim)
    if confidence < 0.5:
        print(f"⚠️  {dim.value} needs more research (confidence: {confidence})")
# Output: ⚠️  where needs more research (confidence: 0.4)
```

**When to use confidence scores:**
- 1.0: Certain, based on hard requirements
- 0.7-0.9: Probable, based on analysis
- 0.4-0.6: Possible, needs validation
- 0.0-0.3: Speculative, placeholder

### Exercise 1.3: Specialized W5H1 Types

```python
from sixspec.core import CommitW5H1, SpecW5H1

# CommitW5H1: Requires WHY + HOW
commit = CommitW5H1(
    subject="fix",
    predicate="resolves",
    object="timeout issue",
    dimensions={
        Dimension.WHY: "Users experiencing cart abandonment",
        Dimension.HOW: "Added retry logic with exponential backoff"
    }
)

print(commit.is_complete())  # True

# SpecW5H1: Requires WHO + WHAT + WHY
full_spec = SpecW5H1(
    subject="System",
    predicate="provides",
    object="authentication",
    dimensions={
        Dimension.WHO: "All users",
        Dimension.WHAT: "Secure login system",
        Dimension.WHY: "Protect user data and comply with regulations"
    }
)

print(full_spec.is_complete())  # True

# Check required dimensions
print(f"Commit requires: {commit.required_dimensions()}")
# Output: {<Dimension.WHY: 'why'>, <Dimension.HOW: 'how'>}
```

---

## Part 2: Git Integration

### Exercise 2.1: Your First Dimensional Commit

```bash
# 1. Install the git hook
cp sixspec/git/hooks/commit-msg .git/hooks/
chmod +x .git/hooks/commit-msg

# 2. Configure commit template (optional but recommended)
git config commit.template templates/.gitmessage

# 3. Make a change
echo "def hello(): return 'world'" > example.py
git add example.py

# 4. Commit with dimensional format
git commit -m "feat: add hello function

WHY: Need simple example for tutorial
HOW: Created basic function returning string"
```

**The hook validates:**
- ✅ Commit type is valid (feat, fix, refactor, docs, test, chore)
- ✅ WHY dimension is present
- ✅ HOW dimension is present

### Exercise 2.2: Commit Format Deep Dive

```bash
# Minimal valid commit
git commit -m "fix: payment timeout

WHY: Users abandoning carts due to API timeouts
HOW: Added retry logic with exponential backoff"

# Full commit with all dimensions
git commit -m "feat: add search filters

WHY: Users cannot efficiently find products in large catalog
HOW: Implemented faceted search using Elasticsearch
WHAT: Search filtering system with category, price, and rating filters
WHERE: src/search/api.py, src/search/filters.py
WHO: All users accessing product catalog
WHEN: On search query submission"

# Refactor example
git commit -m "refactor: extract validation logic

WHY: Duplicated validation code across 3 payment providers
HOW: Created shared PaymentValidator class with common methods
WHERE: src/payment/validation.py, src/payment/stripe.py, src/payment/paypal.py"
```

### Exercise 2.3: Querying Git History

```python
from pathlib import Path
from sixspec.git.history import DimensionalGitHistory
from sixspec.core import Dimension

# Load repository
history = DimensionalGitHistory(Path("."))

print(f"Total commits: {len(history.commits)}")

# Query by WHERE (files)
payment_commits = history.query(where="payment")
print(f"\n{len(payment_commits)} commits affecting payment code:")
for commit in payment_commits[:3]:  # First 3
    print(f"  - {commit.object}: {commit.need(Dimension.WHY)}")

# Query by WHY (purpose)
user_experience = history.query(why="user")
print(f"\n{len(user_experience)} commits related to users:")
for commit in user_experience[:3]:
    print(f"  - {commit.object}")

# Query by type
bug_fixes = history.query(commit_type="fix")
print(f"\n{len(bug_fixes)} bug fixes:")
for commit in bug_fixes[:3]:
    print(f"  - {commit.object}: {commit.need(Dimension.HOW)}")

# Combined query
payment_bugs = history.query(where="payment", commit_type="fix")
print(f"\n{len(payment_bugs)} payment-related bug fixes")

# Trace file history
file_commits = history.trace_file_purpose("src/payment/stripe.py")
print(f"\nEvolution of stripe.py:")
for commit in file_commits:
    print(f"  - {commit.object}")
    print(f"    WHY: {commit.need(Dimension.WHY)}")
```

**Query capabilities:**
- Query by any dimension (case-insensitive substring matching)
- Filter by commit type
- Combine multiple filters
- Trace individual file evolution
- Get unique purposes, files, commit types

---

## Part 3: Building Agents

Agents are entities that understand and execute dimensional specifications.

### Exercise 3.1: Your First NodeAgent

NodeAgents operate on isolated specifications without needing graph context.

```python
from sixspec.agents import NodeAgent
from sixspec.core import W5H1, Dimension

class GreetingAgent(NodeAgent):
    """Agent that generates greetings based on WHO dimension"""

    def __init__(self):
        super().__init__("GreetingAgent", scope="greeting")

    def process_node(self, spec: W5H1) -> str:
        who = spec.need(Dimension.WHO) or "friend"
        what = spec.need(Dimension.WHAT) or "hello"
        return f"{what.capitalize()}, {who}!"

# Use the agent
agent = GreetingAgent()

spec = W5H1(
    subject="Agent",
    predicate="greets",
    object="user",
    dimensions={
        Dimension.WHO: "Alice",
        Dimension.WHAT: "welcome"
    }
)

result = agent.execute(spec)
print(result)  # Output: Welcome, Alice!
```

### Exercise 3.2: Validation Agent

```python
class ValidationAgent(NodeAgent):
    """Validates that a spec has required information"""

    def __init__(self):
        super().__init__("ValidationAgent", scope="spec")

    def process_node(self, spec: W5H1) -> dict:
        """Returns validation report"""
        report = {
            "complete": spec.is_complete(),
            "dimensions": len(spec.dimensions),
            "low_confidence": []
        }

        # Check for low confidence dimensions
        for dim, value in spec.dimensions.items():
            confidence = spec.get_confidence(dim)
            if confidence < 0.5:
                report["low_confidence"].append({
                    "dimension": dim.value,
                    "confidence": confidence,
                    "value": value
                })

        return report

# Use the agent
validator = ValidationAgent()

spec = SpecW5H1(
    subject="System",
    predicate="needs",
    object="feature",
    dimensions={
        Dimension.WHO: "Users",
        Dimension.WHAT: "Export functionality",
        Dimension.WHY: "Data portability"
    }
)

# Add low confidence dimension
spec.set(Dimension.HOW, "Maybe CSV export?", confidence=0.3)

report = validator.execute(spec)
print(f"Complete: {report['complete']}")
print(f"Dimensions: {report['dimensions']}")
print(f"Low confidence: {len(report['low_confidence'])} dimension(s)")
for item in report['low_confidence']:
    print(f"  - {item['dimension']}: {item['value']} (confidence: {item['confidence']})")
```

### Exercise 3.3: GraphAgent for Context

GraphAgents traverse relationships and gather context.

```python
from sixspec.agents import GraphAgent

class ContextGatherer(GraphAgent):
    """Gathers context from neighboring specs"""

    def __init__(self):
        super().__init__("ContextGatherer")

    def traverse(self, start: W5H1) -> dict:
        """Gather context and return analysis"""
        self.current_node = start

        # In a real implementation, this would traverse a graph
        # For this example, we'll analyze the single node
        context = {
            "node": f"{start.subject} {start.predicate} {start.object}",
            "dimensions": list(start.dimensions.keys()),
            "shared_dimensions": {}
        }

        return context

# Use the agent
gatherer = ContextGatherer()

spec = W5H1(
    subject="Developer",
    predicate="implements",
    object="feature",
    dimensions={
        Dimension.WHY: "User request",
        Dimension.WHAT: "Export to PDF",
        Dimension.HOW: "Using ReportLab library"
    }
)

context = gatherer.traverse(spec)
print(f"Analyzing: {context['node']}")
print(f"Dimensions present: {[d.value for d in context['dimensions']]}")
```

---

## Part 4: Hierarchical Walkers

Walkers implement the core SixSpec pattern: hierarchical delegation with WHAT→WHY propagation.

### Exercise 4.1: Understanding WHAT→WHY Propagation

```python
from sixspec.walkers import DiltsWalker
from sixspec.core import DiltsLevel, W5H1, Dimension

# Create parent walker at Level 3 (Capability)
parent = DiltsWalker(level=DiltsLevel.CAPABILITY)

# Execute parent spec
parent_spec = W5H1(
    subject="Team",
    predicate="builds",
    object="payment system",
    dimensions={
        Dimension.WHAT: "Integrate payment processing"
    }
)

print("Parent Walker:")
print(f"  Level: {parent.level.name}")
print(f"  WHAT: {parent_spec.need(Dimension.WHAT)}")

# Create child walker - it inherits parent's WHAT as its WHY
child = DiltsWalker(level=DiltsLevel.BEHAVIOR, parent=parent)
parent.current_node = parent_spec  # Set parent's current node

# Re-create child to see inheritance
child = DiltsWalker(level=DiltsLevel.BEHAVIOR, parent=parent)

print("\nChild Walker:")
print(f"  Level: {child.level.name}")
print(f"  WHY (inherited from parent's WHAT): {child.context.get(Dimension.WHY)}")
```

**The Pattern:**
```
Parent: WHAT = "Integrate payment processing"
            ↓
Child:  WHY = "Integrate payment processing"
        WHAT = "Implement Stripe webhooks"
            ↓
Grandchild: WHY = "Implement Stripe webhooks"
            WHAT = "Create POST /webhooks/stripe endpoint"
```

### Exercise 4.2: Complete Hierarchical Execution

```python
from sixspec.walkers import DiltsWalker
from sixspec.core import DiltsLevel, W5H1, Dimension

# Start at Capability level (L3)
walker = DiltsWalker(level=DiltsLevel.CAPABILITY)

spec = W5H1(
    subject="System",
    predicate="needs",
    object="authentication",
    dimensions={
        Dimension.WHAT: "Implement user authentication",
        Dimension.WHY: "Secure user data"  # This comes from higher level
    }
)

# Execute - walker will delegate down to Environment (L1)
result = walker.traverse(spec)

print(f"Result: {result}")
print(f"\nChildren spawned: {len(walker.children)}")

# Trace the complete execution chain
def print_walker_tree(w, indent=0):
    prefix = "  " * indent
    what = w.context.get(Dimension.WHAT, "N/A")
    why = w.context.get(Dimension.WHY, "N/A")
    print(f"{prefix}L{w.level.value}: {w.level.name}")
    print(f"{prefix}  WHAT: {what}")
    print(f"{prefix}  WHY: {why}")
    for child in w.children:
        print_walker_tree(child, indent + 1)

print("\nExecution Tree:")
print_walker_tree(walker)
```

### Exercise 4.3: Provenance Tracing

```python
# After execution, trace back the WHY chain
walker = DiltsWalker(level=DiltsLevel.CAPABILITY)
spec = W5H1(
    subject="Team",
    predicate="builds",
    object="feature",
    dimensions={
        Dimension.WHAT: "Add search functionality",
        Dimension.WHY: "Improve user experience"
    }
)

result = walker.traverse(spec)

# Get to the deepest walker
deepest = walker
while deepest.children:
    deepest = deepest.children[0]

# Trace provenance
chain = deepest.trace_provenance()

print("Full provenance chain (root to current):")
for i, what in enumerate(chain):
    print(f"  L{6-i}: {what}")

print(f"\n'Why am I doing this?' answer at L{deepest.level.value}:")
print(f"Because my parent wanted: {deepest.context.get(Dimension.WHY)}")
```

---

## Part 5: Advanced Patterns

### Exercise 5.1: Portfolio Execution

Portfolio execution tries multiple strategies and picks the winner based on validation.

```python
from sixspec.walkers import DiltsWalker, ValidationResult
from sixspec.core import DiltsLevel, W5H1, Dimension

class PaymentWalker(DiltsWalker):
    """Custom walker that tries multiple payment integrations"""

    def __init__(self):
        super().__init__(level=DiltsLevel.CAPABILITY)

    def generate_strategies(self, spec: W5H1, n: int) -> list:
        """Generate different payment integration strategies"""
        return [
            "Integrate Stripe with hosted checkout",
            "Integrate Stripe with custom UI",
            "Integrate PayPal"
        ][:n]

    def validate(self, result: Any) -> ValidationResult:
        """Validate payment integration result"""
        # In real implementation, would check actual integration
        # For demo, simulate validation
        result_str = str(result)

        if "Stripe with custom UI" in result_str:
            return ValidationResult(
                score=0.95,
                passed=True,
                details="Best user experience and conversion rate"
            )
        elif "Stripe with hosted" in result_str:
            return ValidationResult(
                score=0.85,
                passed=True,
                details="Good security but less customization"
            )
        elif "PayPal" in result_str:
            return ValidationResult(
                score=0.70,
                passed=True,
                details="Works but lower conversion rate"
            )
        else:
            return ValidationResult(
                score=0.0,
                passed=False,
                details="Integration failed"
            )

# Use portfolio execution
walker = PaymentWalker()

spec = W5H1(
    subject="System",
    predicate="needs",
    object="payment",
    dimensions={
        Dimension.WHAT: "Integrate payment processing",
        Dimension.WHY: "Enable premium subscriptions"
    }
)

print("Trying 3 different strategies...")
result = walker.execute_portfolio(spec, n_strategies=3)

print(f"\nResult: {result}")
print(f"Strategies tried: {len(walker.children)}")

print("\nValidation scores:")
for i, child in enumerate(walker.children):
    print(f"  Strategy {i+1}: {child.context.get(Dimension.WHAT, 'N/A')}")
```

### Exercise 5.2: A2A Task Lifecycle

A2A (Agent-to-Agent) protocol enables graceful interruption and resume.

```python
from sixspec.walkers import A2AWalker
from sixspec.core import DiltsLevel, W5H1, Dimension
from sixspec.a2a import TaskStatus
import time

# Create A2A-enabled walker
walker = A2AWalker(level=DiltsLevel.CAPABILITY)

# Subscribe to status updates
def handle_status_update(update):
    print(f"Status: {update.status.value}")
    if update.result:
        print(f"Result: {update.result}")

walker.task.on_status_change(handle_status_update)

# Create spec
spec = W5H1(
    subject="System",
    predicate="processes",
    object="data",
    dimensions={
        Dimension.WHAT: "Process user data export",
        Dimension.WHY: "GDPR compliance request"
    }
)

# Start execution
print("Starting task...")
walker.task.start()

# Simulate work
print("Task running...")
time.sleep(0.1)

# Pause gracefully
print("\nPausing task (user interrupt)...")
walker.task.pause()
print(f"Task status: {walker.task.status.value}")
print(f"Context preserved: WHY = {walker.context.get(Dimension.WHY)}")

# Resume later
print("\nResuming task...")
walker.task.resume()
print(f"Task status: {walker.task.status.value}")
print(f"Context restored: WHY = {walker.context.get(Dimension.WHY)}")

# Complete
result = walker.traverse(spec)
walker.task.complete(result)
print(f"\nTask status: {walker.task.status.value}")
print(f"Result: {walker.task.result}")
```

### Exercise 5.3: Custom Strategy Walker

```python
from sixspec.walkers import DiltsWalker
from sixspec.core import DiltsLevel, W5H1, Dimension, CommitW5H1

class TestGenerationWalker(DiltsWalker):
    """Walker that generates tests based on commit dimensions"""

    def __init__(self):
        super().__init__(level=DiltsLevel.BEHAVIOR)

    def generate_strategies(self, spec: W5H1, n: int) -> list:
        """Generate different test strategies based on HOW dimension"""
        how = spec.need(Dimension.HOW) or "implementation"

        strategies = []

        # Strategy 1: Unit tests
        strategies.append(f"Write unit tests for {how}")

        # Strategy 2: Integration tests
        if n > 1:
            strategies.append(f"Write integration tests covering {how}")

        # Strategy 3: E2E tests
        if n > 2:
            strategies.append(f"Write E2E tests validating {how}")

        return strategies[:n]

    def validate(self, result: Any) -> ValidationResult:
        """Validate test quality"""
        result_str = str(result).lower()

        # Check for test coverage
        has_unit = "unit test" in result_str
        has_integration = "integration test" in result_str
        has_e2e = "e2e test" in result_str

        score = (has_unit * 0.4 + has_integration * 0.3 + has_e2e * 0.3)

        return ValidationResult(
            score=score,
            passed=score > 0.5,
            details=f"Unit: {has_unit}, Integration: {has_integration}, E2E: {has_e2e}"
        )

# Use for test generation
walker = TestGenerationWalker()

# Create spec from a commit
commit_spec = CommitW5H1(
    subject="feat",
    predicate="adds",
    object="search feature",
    dimensions={
        Dimension.WHY: "Users need to find products",
        Dimension.HOW: "Elasticsearch with faceted search",
        Dimension.WHERE: "src/search/api.py"
    }
)

print("Generating tests for commit...")
print(f"HOW: {commit_spec.need(Dimension.HOW)}")

result = walker.execute_portfolio(commit_spec, n_strategies=3)
print(f"\nGenerated: {result}")
```

---

## Part 6: Real-World Scenario

Let's build a complete example: A documentation generator that reads commits and generates docs.

### Exercise 6.1: Documentation Agent

```python
from sixspec.agents import NodeAgent
from sixspec.core import W5H1, Dimension, CommitW5H1
from sixspec.git.history import DimensionalGitHistory
from pathlib import Path

class DocGeneratorAgent(NodeAgent):
    """Generates documentation from dimensional commits"""

    def __init__(self):
        super().__init__("DocGenerator", scope="commit")

    def process_node(self, spec: W5H1) -> str:
        """Generate documentation from a commit spec"""
        if not isinstance(spec, CommitW5H1):
            raise ValueError("DocGenerator only works with commits")

        # Extract information
        what = spec.object  # commit subject
        why = spec.need(Dimension.WHY)
        how = spec.need(Dimension.HOW)
        where = spec.need(Dimension.WHERE)

        # Generate documentation section
        doc = f"### {what.title()}\n\n"
        doc += f"**Purpose**: {why}\n\n"
        doc += f"**Implementation**: {how}\n\n"

        if where:
            doc += f"**Files Modified**: {where}\n\n"

        return doc

# Use the agent
agent = DocGeneratorAgent()

# Load recent commits
history = DimensionalGitHistory(Path("."))

# Filter for features
features = history.query(commit_type="feat")

print("# Feature Documentation\n")
print("Auto-generated from dimensional commits\n")

for commit in features[:5]:  # First 5 features
    try:
        doc_section = agent.execute(commit)
        print(doc_section)
    except ValueError:
        continue
```

### Exercise 6.2: Complete Documentation Pipeline

```python
from sixspec.walkers import DiltsWalker
from sixspec.core import DiltsLevel, W5H1, Dimension
from sixspec.git.history import DimensionalGitHistory
from pathlib import Path

class DocumentationWalker(DiltsWalker):
    """Walker that orchestrates documentation generation"""

    def __init__(self):
        super().__init__(level=DiltsLevel.CAPABILITY)

    def generate_strategies(self, spec: W5H1, n: int) -> list:
        """Different documentation strategies"""
        return [
            "Generate API reference from commits",
            "Generate feature docs from commits",
            "Generate changelog from commits"
        ][:n]

    def validate(self, result: Any) -> ValidationResult:
        """Validate generated documentation"""
        result_str = str(result)

        # Check completeness
        has_purpose = "Purpose" in result_str
        has_impl = "Implementation" in result_str
        has_files = "Files" in result_str

        score = (has_purpose * 0.4 + has_impl * 0.4 + has_files * 0.2)

        return ValidationResult(
            score=score,
            passed=score > 0.6,
            details=f"Completeness: {score:.1%}"
        )

# Create walker
walker = DocumentationWalker()

# Create spec
spec = W5H1(
    subject="Team",
    predicate="generates",
    object="documentation",
    dimensions={
        Dimension.WHAT: "Generate documentation from commits",
        Dimension.WHY: "Keep docs synchronized with code changes"
    }
)

# Execute with portfolio
print("Generating documentation using multiple strategies...\n")
result = walker.execute_portfolio(spec, n_strategies=3)

print(f"Best strategy selected:")
print(f"Result: {result}")
```

---

## Next Steps

Congratulations! You've learned:

1. ✅ W5H1 dimensional specifications
2. ✅ Git integration with dimensional commits
3. ✅ Building NodeAgents and GraphAgents
4. ✅ Hierarchical walkers with WHAT→WHY propagation
5. ✅ Portfolio execution and validation
6. ✅ A2A task lifecycle management

### Further Learning

- **ARCHITECTURE.md**: Deep dive into system design
- **API_REFERENCE.md**: Complete API documentation
- **DESIGN_PHILOSOPHY.md**: Core principles and concepts
- **examples/**: More example implementations

### Build Your Own

Try creating:
1. A custom agent for your domain
2. A walker with domain-specific validation
3. A git history analyzer for your repository
4. An automated documentation generator

### Common Patterns

**Pattern 1: Validation-Driven Development**
```python
# Write validation first
def validate(self, result):
    return ValidationResult(
        score=calculate_quality(result),
        passed=meets_requirements(result)
    )

# Then generate strategies
def generate_strategies(self, spec, n):
    return create_n_approaches(spec)
```

**Pattern 2: Context Inheritance**
```python
# Always propagate purpose
child_spec = parent_spec.copy_with(
    dimensions={
        Dimension.WHY: parent_spec.need(Dimension.WHAT),
        Dimension.WHAT: "Child's specific action"
    }
)
```

**Pattern 3: Confidence-Based Decisions**
```python
# Check confidence before proceeding
if spec.get_confidence(Dimension.HOW) < 0.7:
    # Need more research
    return research_alternatives(spec)
else:
    # Confidence is high enough
    return implement(spec)
```

### Troubleshooting

**Problem**: Git hook not running
```bash
# Solution: Check permissions
ls -l .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

**Problem**: Import errors
```bash
# Solution: Reinstall in development mode
pip install -e .
```

**Problem**: Validation always fails
```python
# Solution: Debug validation logic
result = walker.validate(test_result)
print(f"Score: {result.score}, Passed: {result.passed}")
print(f"Details: {result.details}")
```

### Community

- Report issues on GitHub
- Read the existing test suite for more examples
- Check out `examples/` directory

Happy coding with SixSpec! 🎉
