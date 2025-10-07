# Dilts Organizational Structure Example

This example demonstrates how to use SixSpec's embedded framework to create a **living digital representation** of an individual or organization based on Dilts' Logical Levels of Change.

## Quick Start

```bash
# 1. Run the setup script
bash setup-example.sh "My-Organization"

# 2. Explore the created structure
cd My-Organization
tree -L 2

# 3. Query and analyze
python ../org_query_example.py .
```

## What Gets Created

The setup script creates a complete Dilts hierarchy:

```
My-Organization/
├── L6-MISSION/          # FOR WHAT - Why we exist
├── L5-IDENTITY/         # WHO - What defines us  
├── L4-BELIEFS/          # WHY - Guiding principles
├── L3-CAPABILITIES/     # WHAT - What we deliver
├── L2-BEHAVIORS/        # HOW - How we operate
└── L1-ENVIRONMENT/      # WHERE/WHEN - Context
```

Each level contains:
- Directory structure tailored to that level
- README explaining the level's purpose
- Example `.w5h1` files demonstrating the format
- Relationships defining parent-child connections

## The .w5h1 File Format

Every organizational specification uses the W5H1 (5W1H) dimensional format:

```yaml
---
level: BELIEFS
created: 2024-01-25
status: validation_needed
confidence: 0.65

subject: "Target customers"
predicate: "are willing to pay"
object: "$15-20/month for research tools"

dimensions:
  WHO:
    value: "Academic researchers with limited budgets"
    confidence: 0.85
    sources:
      - "User interviews (n=30)"
  
  WHAT:
    value: "Monthly subscription of $15-20"
    confidence: 0.65
    sources:
      - "Pricing survey (n=100)"
  
  WHY:
    value: "Build accessible research tools"  # Inherited from parent
    confidence: 0.95
  
  HOW:
    value: "Freemium model with paid AI features"
    confidence: 0.70

parent_spec: "../../L5-IDENTITY/positioning/market-position.w5h1"
child_specs:
  - "../../L3-CAPABILITIES/services/products/research-tool.w5h1"

tags: [assumption, pricing, validation-needed]
```

## Key Concepts

### 1. Purpose Propagation

**Parent's WHAT becomes child's WHY**

This creates an unbreakable chain from mission to execution:

```
L6 WHAT: "Democratize AI research tools"
    ↓
L5 WHY: "Democratize AI research tools"
L5 WHAT: "Be the accessible alternative to expensive tools"
    ↓
L4 WHY: "Be the accessible alternative"
L4 WHAT: "Customers will pay $15-20/month"
    ↓
L3 WHY: "Price point of $15-20/month"
L3 WHAT: "SaaS product with freemium model"
```

### 2. Confidence Tracking

Every dimension has a confidence score (0.0-1.0):

- **1.0**: Certain (validated, proven)
- **0.8-0.9**: High confidence (strong evidence)
- **0.6-0.7**: Moderate (some validation needed)
- **0.4-0.5**: Low (assumption, needs testing)
- **0.0-0.3**: Very uncertain (speculation)

### 3. Belief Validation

Beliefs in L4 can be:
- **Active**: Current assumptions
- **Validated**: Moved to `validated/` after proof
- **Invalidated**: Moved to `invalidated/` when disproven

This creates an evidence-based learning system.

### 4. Bidirectional Flow (L2)

Behaviors flow both ways:
- **Top-down**: Strategic plans → Tactical execution
- **Bottom-up**: Market feedback → Strategic adjustment

## Usage Examples

### Query Organizational Knowledge

```bash
python org_query_example.py ./My-Organization

# Output:
# 📊 Specifications by Level
# 🔗 Purpose Propagation Validation
# 💡 Belief Confidence Analysis
# 🎯 Most/Least Confident Specs
# 👻 Orphaned Specs
```

### Validate Purpose Chain

```python
from org_query_example import OrgLoader, PurposePropagationValidator

loader = OrgLoader("./My-Organization")
specs = loader.load_all()

validator = PurposePropagationValidator(specs)
issues = validator.validate_all()

if issues:
    print("Purpose propagation issues:")
    for issue in issues:
        print(f"  - {issue}")
```

### Analyze Beliefs

```python
from org_query_example import BeliefAnalyzer

analyzer = BeliefAnalyzer(specs)

# Get confidence summary
summary = analyzer.get_confidence_summary()
print(f"Average belief confidence: {summary['mean']:.2f}")

# Find beliefs needing validation
needs_val = analyzer.get_validation_needed(threshold=0.70)
print(f"\n{len(needs_val)} beliefs need validation:")
for path, confidence, spec in needs_val:
    print(f"  {confidence:.2f} - {path}")
```

### Trace Provenance

```python
from org_query_example import OrgInsights

insights = OrgInsights(specs)

# Trace any spec back to mission
chain = insights.get_provenance_chain("L3-CAPABILITIES/services/products/research-tool.w5h1")

print("Full purpose chain:")
for i, item in enumerate(chain, 1):
    print(f"{i}. {item}")

# Output:
# 1. L6 WHAT: Democratize AI research tools
# 2. L5 WHAT: Be the accessible alternative
# 3. L4 WHAT: Customers pay $15-20/month
# 4. L3 WHAT: SaaS freemium product
```

## Integration with Git

### Dimensional Commits

Every change to the organizational structure uses dimensional commits:

```bash
git add L4-BELIEFS/assumptions/market/pricing.w5h1
git commit

# Template prompts for:
# WHY: Why this change?
# HOW: How implemented?
# WHAT: What changed?
# WHERE: Which files?
# WHO: Who's affected?
# WHEN: When does it apply?
```

### Query History

```python
from sixspec.git.history import DimensionalGitHistory

history = DimensionalGitHistory(Path("./My-Organization"))

# Find all belief changes
belief_changes = history.query(where="L4-BELIEFS")

# Find all pricing-related changes
pricing = history.query(why="pricing")

# Trace evolution of a file
evolution = history.trace_file_purpose("L4-BELIEFS/assumptions/market/pricing.w5h1")
```

## Dilts Levels Explained

### L6 - MISSION (FOR WHAT)
**Extreme autonomy** - Can question existence itself

- Mission statements
- Vision documents
- Impact goals
- Ultimate purpose

**Questions**: Why do we exist? What's our impact?

### L5 - IDENTITY (WHO)
**High autonomy** - Can redefine what we are

- Brand identity
- Core values
- Culture code
- Market positioning

**Questions**: Who are we? What makes us unique?

### L4 - BELIEFS (WHY)
**Moderate autonomy** - Can choose principles

- Operating principles
- Assumptions (testable beliefs)
- Mental models
- Decision frameworks

**Questions**: Why this approach? What do we believe?

**Special**: Beliefs are validated or invalidated based on evidence.

### L3 - CAPABILITIES (WHAT)
**Low autonomy** - Can select methods

- Services and products
- Core competencies
- Resources and partnerships
- Technical capabilities

**Questions**: What can we deliver? How do we do it?

### L2 - BEHAVIORS (HOW)
**Very low autonomy** - Can execute defined behaviors

- **Strategic (APPROACH)**: Measured initiatives to serve market through identity
- **Tactical (RESPONSE)**: Measured responses to market feedback informing strategy
- Operational rituals
- Communication patterns

**Questions**: How do we approach the market? How does it respond? How do we adapt?

**Special**: Bidirectional flow
- **Strategy → Tactics**: Our approach (initiatives acting on environment)
- **Tactics → Strategy**: Market response (feedback informing refinement)

### L1 - ENVIRONMENT (WHERE/WHEN)
**Zero autonomy** - Cannot change context

- Target markets
- Competitive landscape
- Stakeholders
- Constraints (legal, resource, technical)

**Questions**: Where/when do we operate? For whom?

## Use Cases

### 1. Strategic Planning
- Update mission → See downstream impact
- Test assumptions → Update confidence
- Validate beliefs → Move to validated/

### 2. Onboarding
- New team member explores L6→L1
- Understands WHY behind every decision
- Sees full provenance chain

### 3. Decision Making
- Check relevant beliefs and confidence
- Trace decision back to mission
- Document decision as new spec

### 4. Investor Relations
- Generate organizational audit report
- Show validated vs. assumed beliefs
- Demonstrate evidence-based strategy

### 5. Culture Documentation
- Make implicit culture explicit
- Track value evolution over time
- Ensure behavior-values alignment

## Next Steps

1. **Customize the example** for your organization
2. **Add your actual content** to each level
3. **Install SixSpec git hooks** for validation
4. **Query and analyze** your organizational knowledge
5. **Evolve with evidence** - validate assumptions, update confidence

## Philosophy

> **"Every file answers WHO, WHAT, WHEN, WHERE, HOW, WHY"**  
> **"Parent's WHAT → Child's WHY (purpose propagation)"**  
> **"Your organization becomes as queryable as your codebase"**

## Related Documentation

- [DILTS_DIRECTORY_STRUCTURE.md](../../DILTS_DIRECTORY_STRUCTURE.md) - Full specification
- [ARCHITECTURE.md](../../ARCHITECTURE.md) - SixSpec architecture
- [DESIGN_PHILOSOPHY.md](../../DESIGN_PHILOSOPHY.md) - Core principles
- [README.md](../../README.md) - SixSpec overview

## License

MIT
