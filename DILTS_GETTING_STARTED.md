# Getting Started: Dilts Organizational Structure

## TL;DR - 5 Minutes to Working Example

```bash
# 1. Navigate to examples
cd /home/Projects/SixSpec/examples/dilts-org-structure

# 2. Create your org structure
bash setup-example.sh "My-Company"

# 3. Explore what was created
cd My-Company
tree -L 2

# 4. Query and analyze
cd ..
python org_query_example.py My-Company
```

**Result**: Complete organizational structure with 6 Dilts levels, example files, git integration, and analysis tools.

---

## What Problem Does This Solve?

### Before: The Organizational Knowledge Crisis

**Symptoms:**
- 💬 "Why are we doing this?" → "I don't know, ask Sarah"
- 📄 Mission statement is a poster nobody reads
- 🤷 Values are platitudes disconnected from behavior
- 📊 Strategy lives in slide decks that get outdated
- 🌫️ Culture is implicit, tribal knowledge
- 🔄 Same mistakes repeated because history is lost
- 🆕 Onboarding takes months to understand "how we work"

**Root Cause**: Organizational knowledge is **implicit, scattered, and unqueryable**.

### After: Structured, Queryable Organization

**Reality:**
- 🎯 "Why are we doing this?" → `sixspec why features/feature-x` → Full chain mission→execution
- 📜 Mission is a `.w5h1` file with full dimensional context and provenance
- ✅ Values trace to specific behaviors with measurable confidence
- 📊 Strategy is living graph of beliefs with validation status
- 📚 Culture is documented specifications anyone can explore
- 🔬 Learnings captured: assumptions → validated/invalidated
- 🚀 Onboarding is self-guided: explore L6→L1 with full "why" context

**Solution**: Make organizational knowledge **explicit, structured, and AI-queryable** using Dilts hierarchy + SixSpec framework.

---

## Core Concept in 60 Seconds

### The Dilts Hierarchy

Organizations operate at 6 levels of abstraction (Dilts' Logical Levels):

```
L6: MISSION      (FOR WHAT) - Why do we exist?
L5: IDENTITY     (WHO)      - What defines us?
L4: BELIEFS      (WHY)      - What do we believe?
L3: CAPABILITIES (WHAT)     - What can we deliver?
L2: BEHAVIORS    (HOW)      - How do we operate?
L1: ENVIRONMENT  (WHERE)    - What context do we face?
```

### Purpose Propagation

**Parent's WHAT becomes child's WHY** - creates unbreakable chain:

```
L6 WHAT: "Democratize AI research"
    ↓
L5 WHY:  "Democratize AI research"        (inherited)
L5 WHAT: "Be accessible alternative"
    ↓
L4 WHY:  "Be accessible alternative"      (inherited)
L4 WHAT: "Price at $15-20/month"
```

Ask "why?" at ANY level → get complete chain to mission.

### Six Dimensions (5W1H)

Every specification answers: **WHO, WHAT, WHEN, WHERE, HOW, WHY**

```yaml
dimensions:
  WHO:   "Target researchers"        confidence: 0.85
  WHAT:  "$15-20/month pricing"      confidence: 0.65
  WHEN:  "After free trial"          confidence: 0.60
  WHERE: "In subscription flow"      confidence: 0.75
  HOW:   "Freemium model"            confidence: 0.70
  WHY:   "Be accessible"             confidence: 0.80
```

Confidence scores track certainty → guide decisions.

---

## Quick Start: 3 Paths

### Path 1: Just Explore (5 min)

```bash
# Create example
cd /home/Projects/SixSpec/examples/dilts-org-structure
bash setup-example.sh "Example-Org"
cd Example-Org

# Explore structure
tree -L 2

# Read example mission
cat L6-MISSION/mission-statement.w5h1

# Read example belief (with validation)
cat L4-BELIEFS/assumptions/market/customer-willingness-to-pay.w5h1

# See git integration
git log --oneline
```

**Outcome**: Understand the structure, file format, and purpose propagation.

### Path 2: Customize for Your Org (30 min)

```bash
# Create your org
bash setup-example.sh "Your-Company-Name"
cd Your-Company-Name

# 1. Update mission
vim L6-MISSION/mission-statement.w5h1

# Replace with your actual:
# - WHY: Why does your org exist?
# - WHAT: What is your primary mission?
# - WHO: Who do you serve?

# 2. Define identity
vim L5-IDENTITY/brand/brand-identity.w5h1

# Your brand:
# - WHO: Your identity
# - WHAT: How it manifests
# - WHY: (inherited from mission)
# - HOW: Your approach

# 3. Document key beliefs
vim L4-BELIEFS/assumptions/market/customer-needs.w5h1

# Your assumptions:
# - What do you believe about customers?
# - Confidence level?
# - Evidence supporting/contradicting?

# 4. Commit changes
git add .
git commit
# (Uses dimensional commit template - fill in WHY and HOW)

# 5. Query your org
cd ..
python org_query_example.py Your-Company-Name
```

**Outcome**: Your organization as structured, queryable data.

### Path 3: Integrate with Real Project (2 hours)

For your AI research tool project:

```bash
# 1. Create org structure in project
cd /path/to/your/research-tool-project
mkdir org-knowledge
cd org-knowledge

bash /home/Projects/SixSpec/examples/dilts-org-structure/setup-example.sh "research-tool-org"
cd research-tool-org

# 2. Document your mission
# Why are you building this tool?
vim L6-MISSION/mission-statement.w5h1

# 3. Capture key assumptions
# Create file for each major assumption:
vim L4-BELIEFS/assumptions/product/annotation-value.w5h1
vim L4-BELIEFS/assumptions/product/graph-superiority.w5h1
vim L4-BELIEFS/assumptions/market/willingness-to-pay.w5h1

# 4. Define capabilities
vim L3-CAPABILITIES/services/products/annotation-tool.w5h1

# 5. Document development approach
vim L2-BEHAVIORS/tactical/development-workflow.w5h1
vim L2-BEHAVIORS/strategic/mvp-iteration.w5h1

# 6. Capture market context
vim L1-ENVIRONMENT/market/competitive-landscape.w5h1
vim L1-ENVIRONMENT/market/target-users.w5h1

# 7. Link product decisions to org knowledge
# In your codebase, add comments:
# WHY: See org-knowledge/research-tool-org/L4-BELIEFS/...
# This feature implements: L3-CAPABILITIES/services/...

# 8. Query for decision-making
cd ../..
python /home/Projects/SixSpec/examples/dilts-org-structure/org_query_example.py org-knowledge/research-tool-org

# Should we build feature X?
# → Check L4 beliefs confidence
# → Trace to L6 mission alignment
# → Review L1 market validation
```

**Outcome**: Product decisions traceable to organizational knowledge.

---

## The File Format: .w5h1 YAML

### Minimal Example

```yaml
---
level: CAPABILITIES
created: 2024-03-15
status: active

subject: "Our team"
predicate: "delivers"
object: "AI-powered research tools"

dimensions:
  WHAT:
    value: "Browser extension + web app for research annotation"
    confidence: 0.90
    sources:
      - "Product strategy 2024"
  
  WHY:
    value: "Democratize AI-powered research"  # From parent
    confidence: 0.95
  
  HOW:
    value: "React + FastAPI + Neo4j + OpenAI"
    confidence: 0.85

parent_spec: "../L5-IDENTITY/positioning/market-position.w5h1"
child_specs:
  - "../L2-BEHAVIORS/tactical/dev-workflow.w5h1"

tags: [capability, product, core]
```

### With Full Validation (Belief Example)

```yaml
---
level: BELIEFS
created: 2024-01-25
last_updated: 2024-03-15
status: validation_needed
confidence: 0.65

subject: "Target customers"
predicate: "will pay"
object: "$15-20/month for research automation"

dimensions:
  WHO:
    value: "Academic researchers with limited budgets"
    confidence: 0.85
    sources: ["User interviews (n=30)"]
  
  WHAT:
    value: "Monthly subscription $15-20"
    confidence: 0.65
    sources: ["Pricing survey (n=100)"]
    notes: "Needs A/B testing"
  
  WHY:
    value: "Be accessible alternative to enterprise tools"
    confidence: 0.80
    sources: ["Inherited from L5-IDENTITY"]
  
  HOW:
    value: "Freemium: free basic, paid for AI features"
    confidence: 0.70
    sources: ["Pricing strategy doc"]

parent_spec: "../../L5-IDENTITY/positioning/market-position.w5h1"
child_specs:
  - "../../L3-CAPABILITIES/services/products/research-tool.w5h1"

# Assumption-specific fields
assumption_type: "pricing"
validation_status: "partially_validated"
confidence_threshold: 0.80
requires_validation_by: "2024-06-01"

# Evidence trail
evidence:
  supporting:
    - type: "survey"
      date: "2024-02-10"
      sample_size: 100
      summary: "62% would pay $15-20/month"
      confidence_boost: 0.10
  
  contradicting:
    - type: "competitor_analysis"
      date: "2024-03-01"
      summary: "Competitors charge $50-100 successfully"
      confidence_penalty: -0.10
      notes: "But they target institutions, not individuals"

# Validation plan
validation:
  method: "A/B pricing test"
  success_criteria:
    - "≥40% conversion free→paid"
    - "≥70% retention after 3 months"
  timeline: "Q2 2024"
  next_steps:
    - "Set up A/B infrastructure (Apr 1)"
    - "Run test at $10/$15/$20 (Apr 15 - May 15)"
    - "Move to validated/ or invalidated/ (May 30)"

tags: [assumption, pricing, validation-needed, revenue-critical]
```

---

## Common Use Cases

### 1. Strategic Decision: "Should we pivot?"

**Scenario**: Considering major product pivot

```bash
# 1. Check current mission alignment
cat L6-MISSION/mission-statement.w5h1

# 2. Review beliefs confidence
python org_query_example.py . | grep "Least Confident"

# 3. Check which beliefs have been invalidated
find L4-BELIEFS/assumptions/invalidated -name "*.w5h1"

# 4. Analyze impact of pivot
sixspec impact L6-MISSION/mission-statement.w5h1 \
  --what-if "WHAT: Build collaborative research platforms"

# Decision criteria:
# - Multiple L4 beliefs invalidated? → Pivot may be needed
# - Mission still aligned? → Stay course
# - High confidence throughout? → Don't pivot on gut feel
```

### 2. Feature Decision: "Build feature X?"

**Scenario**: Engineering wants to add new feature

```bash
# 1. Trace proposed feature to mission
# Create draft spec:
vim L3-CAPABILITIES/proposed/feature-x.w5h1

# 2. Check purpose propagation
# Does parent WHAT align with our mission?

# 3. Review related beliefs
grep -r "feature-x" L4-BELIEFS/

# 4. Check confidence levels
# If confidence in related beliefs < 0.70 → validate first
# If confidence > 0.80 → build it

# 5. Document decision
git commit -m "feat: added feature-x capability spec

WHY: Validated user need (confidence 0.85)
HOW: Traces to L6 mission through L4 beliefs
WHAT: Added capability spec with full provenance"
```

### 3. Onboarding: "Help new hire understand culture"

**Scenario**: New developer joins team

```bash
# Generate personalized reading list
sixspec onboarding-pack --role "engineer" > onboarding.md

# Contents:
# 1. L6-MISSION - Why we exist
# 2. L5-IDENTITY/values - Who we are
# 3. L4-BELIEFS/mental-models - How we think
# 4. L3-CAPABILITIES/tech-stack - What you'll use
# 5. L2-BEHAVIORS/dev-workflow - How we work
# 6. Recent changes (last 90 days)

# Interactive exploration
sixspec explore --level L4-BELIEFS

# Natural language queries:
# > "Why do we use React?"
# > "What's our approach to technical debt?"
# > "How do we balance quality vs speed?"
# → Answers with full provenance and confidence
```

### 4. Belief Validation: "Test pricing assumption"

**Scenario**: Running A/B test on pricing

```bash
# Before test: Check current assumption
cat L4-BELIEFS/assumptions/market/pricing.w5h1
# Confidence: 0.65
# Status: validation_needed

# Run A/B test...

# After test: Update with results
sixspec belief update \
  L4-BELIEFS/assumptions/market/pricing.w5h1 \
  --add-evidence "a-b-test-q2-2024.json" \
  --result "validation_confirmed" \
  --confidence 0.85 \
  --move-to "validated/"

# Automatically:
# - Updates confidence score
# - Moves file to validated/
# - Commits with dimensional message
# - Analyzes downstream impact
# - Notifies affected specs
```

### 5. Quarterly Review: "How are we evolving?"

**Scenario**: Board meeting, need evolution summary

```bash
# Generate comprehensive report
sixspec report evolution \
  --since "2024-01-01" \
  --output "board-presentation/"

# Generated:
# 1. confidence-trend.pdf - Confidence over time
# 2. belief-validation.pdf - Validated vs invalidated
# 3. major-changes.pdf - Strategic shifts
# 4. impact-analysis.pdf - What changed and why
# 5. provenance-chains.pdf - Full traceability

# Query specific questions:
# "What beliefs did we validate this quarter?"
find L4-BELIEFS/assumptions/validated -name "*.w5h1" -mtime -90

# "What assumptions were disproven?"
find L4-BELIEFS/assumptions/invalidated -name "*.w5h1" -mtime -90

# "How has mission evolved?"
git log --all -- L6-MISSION/
```

---

## Advanced: Integrating with Development

### Link Code to Org Knowledge

```python
# features/annotation.py

"""
AI-powered research annotation feature.

WHY: See org-knowledge/L4-BELIEFS/assumptions/product/annotation-value.w5h1
     Validated user need (confidence 0.85) for faster research synthesis.

WHAT: See org-knowledge/L3-CAPABILITIES/services/products/annotation-tool.w5h1
      Core capability delivering on mission to democratize AI research.

PROVENANCE:
  L6: Democratize AI research
  L5: Be accessible alternative
  L4: Users need annotation assistance (validated)
  L3: Build annotation tool (this capability)
  L2: Implement via browser extension
  L1: Serve academic researchers
"""

def annotate_with_ai(text, context):
    # Implementation...
    pass
```

### Decision Log in Git

```bash
# Every major decision gets documented

git commit -m "decision: use React over Vue for frontend

WHY: See L4-BELIEFS/principles/tech-stack.w5h1
     Aligns with 'mature, widely-supported technologies' principle
     
HOW: Evaluated both frameworks against criteria:
     - Community size: React wins
     - Developer familiarity: Team knows React
     - Job market: More React developers available
     
WHAT: Updated L3-CAPABILITIES/competencies/tech-stack.w5h1
      
CONFIDENCE: 0.90 (high confidence in decision)

IMPACT:
  - L3: Added React to core tech stack
  - L2: Updated development workflow for React patterns
  - L1: Hiring requirements now specify React experience
  
Evidence:
  - Developer survey (n=15): 13/15 prefer React
  - Market analysis: 3x more React jobs than Vue
  - Community metrics: React GitHub stars 2x Vue"
```

---

## Troubleshooting

### "Purpose propagation validation failing"

**Issue**: `parent WHAT ≠ child WHY`

```bash
# Check parent's WHAT
cat L5-IDENTITY/brand/brand-identity.w5h1 | grep -A5 "WHAT:"

# Check child's WHY
cat L4-BELIEFS/assumptions/market/pricing.w5h1 | grep -A5 "WHY:"

# They should match (or be very similar)

# Fix: Update child's WHY to match parent's WHAT
vim L4-BELIEFS/assumptions/market/pricing.w5h1
# Change WHY value to match parent's WHAT value

# Validate
python org_query_example.py . | grep "Purpose Propagation"
```

### "Confidence too low to make decision"

**Issue**: Want to proceed but confidence < threshold

**Don't**: Proceed anyway  
**Do**: Run validation or prototype

```yaml
# If confidence < 0.70 for critical decision:

# Option 1: Gather more evidence
validation:
  method: "user interviews"
  sample_size: 30
  expected_confidence: 0.80
  
# Option 2: Run cheap experiment
validation:
  method: "landing page test"
  cost: "$500 ads"
  expected_confidence: 0.75
  
# Option 3: Build prototype
validation:
  method: "2-week prototype"
  success_criteria: "3/5 users find value"
  expected_confidence: 0.85
```

### "Too many files to maintain"

**Issue**: Structure becoming unwieldy

**Solution**: Focus on high-impact files

```bash
# Priority tiers:
# Tier 1 (Always maintain): L6, L5, core L4 beliefs
# Tier 2 (Quarterly review): L3, L2 processes
# Tier 3 (Annual review): L1 environment docs

# Set review cycles in files:
review_cycle: "Annual"    # L1
review_cycle: "Quarterly" # L2, L3
review_cycle: "Monthly"   # L4 assumptions
review_cycle: "As-needed" # L5 (rarely changes)
review_cycle: "Annual"    # L6 (very stable)

# Auto-flag stale files:
sixspec check-staleness --warn-after 90
```

---

## Next Steps

### Immediate (Today)

1. ✅ Run the setup script and explore example
2. ✅ Read example files to understand format
3. ✅ Run query tool to see analysis

### This Week

1. Create structure for your actual organization
2. Fill in L6 (Mission) with real content
3. Document 3-5 key beliefs in L4
4. Link one code decision to org knowledge

### This Month

1. Complete all 6 levels with real content
2. Train team on querying org knowledge
3. Integrate into decision-making process
4. Run first belief validation experiment

### This Quarter

1. Make org knowledge the source of truth
2. Reference in all major decisions
3. Validate/invalidate assumptions based on evidence
4. Generate quarterly evolution report

---

## Resources

**Documentation**:
- [DILTS_DIRECTORY_STRUCTURE.md](./DILTS_DIRECTORY_STRUCTURE.md) - Full specification
- [DILTS_IMPLEMENTATION_SUMMARY.md](./DILTS_IMPLEMENTATION_SUMMARY.md) - Implementation overview
- [examples/dilts-org-structure/README.md](./examples/dilts-org-structure/README.md) - Example walkthrough

**Code**:
- `setup-example.sh` - Automated setup
- `org_query_example.py` - Query and analysis tool

**SixSpec Framework**:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - SixSpec architecture
- [DESIGN_PHILOSOPHY.md](./DESIGN_PHILOSOPHY.md) - Core principles
- [README.md](./README.md) - SixSpec overview

---

## Philosophy

> **"If you can't explain why you're doing something,**  
> **maybe you shouldn't be doing it."**

This framework makes the "why" explicit, traceable, and queryable.

**Before**: Decisions based on gut feel, politics, or "we've always done it this way"  
**After**: Decisions based on evidence, aligned with mission, traceable to purpose

**Your organization becomes as rigorous as your codebase.**
