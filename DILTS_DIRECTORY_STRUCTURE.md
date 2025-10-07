# Dilts Directory Structure: Living Digital Representation

## Vision

Create a templated directory structure based on Dilts' Logical Levels that serves as a **living, version-controlled, queryable digital representation** of an individual or organization. This structure leverages SixSpec's dimensional framework to make organizational identity, strategy, and execution fully traceable and AI-queryable.

## Core Concept

**Every directory level = A Dilts Level**  
**Every file = A dimensional specification (W5H1)**  
**Every commit = A change with traceable purpose (WHY + HOW)**  
**Git history = The evolution of organizational consciousness**

---

## Directory Structure Schema

```
organization-name/
├── .sixspec/
│   ├── config.yaml              # SixSpec configuration
│   ├── templates/               # W5H1 templates per level
│   └── validators/              # Level-specific validators
│
├── L6-MISSION/                  # FOR WHAT - Why we exist
│   ├── README.md                # Overview of mission
│   ├── mission-statement.w5h1   # Core mission (W5H1 format)
│   ├── vision-2030.w5h1         # Long-term vision
│   ├── purpose-charter.w5h1     # Organizational purpose
│   └── impact-goals.w5h1        # Intended impact on world
│
├── L5-IDENTITY/                 # WHO - What defines us
│   ├── README.md
│   ├── brand/
│   │   ├── brand-identity.w5h1  # Core brand definition
│   │   ├── visual-assets/
│   │   │   ├── logo.svg
│   │   │   ├── colors.w5h1      # Color palette with reasoning
│   │   │   ├── typography.w5h1  # Font choices with WHY
│   │   │   └── wordmarks/
│   │   ├── voice-and-tone.w5h1  # Brand voice definition
│   │   └── brand-guidelines.pdf
│   ├── values/
│   │   ├── core-values.w5h1     # Non-negotiable values
│   │   ├── culture-code.w5h1    # How values manifest
│   │   └── ethics-framework.w5h1
│   └── positioning/
│       ├── market-position.w5h1 # Where we stand
│       ├── differentiation.w5h1 # What makes us unique
│       └── target-audience.w5h1 # Who we serve
│
├── L4-BELIEFS/                  # WHY - Our guiding principles
│   ├── README.md
│   ├── principles/
│   │   ├── decision-framework.w5h1    # How we make decisions
│   │   ├── quality-philosophy.w5h1    # What quality means
│   │   ├── innovation-approach.w5h1   # How we innovate
│   │   └── sustainability.w5h1        # Environmental stance
│   ├── assumptions/
│   │   ├── market-assumptions.w5h1    # What we believe about market
│   │   ├── customer-assumptions.w5h1  # What we believe about users
│   │   ├── technology-bets.w5h1       # Tech philosophy
│   │   └── validated/                 # Proven assumptions
│   │       └── .gitkeep
│   ├── mental-models/
│   │   ├── problem-solving.w5h1       # How we approach problems
│   │   ├── growth-mindset.w5h1        # How we view development
│   │   └── learning-culture.w5h1      # How we learn
│   └── relationships/
│       ├── belief-dependencies.graph  # Which beliefs depend on others
│       └── belief-conflicts.graph     # Contradictions to resolve
│
├── L3-CAPABILITIES/             # WHAT - What we can deliver
│   ├── README.md
│   ├── services/
│   │   ├── service-catalog.w5h1       # All offerings
│   │   ├── consulting/
│   │   │   ├── strategy-consulting.w5h1
│   │   │   ├── technical-advisory.w5h1
│   │   │   └── implementation-support.w5h1
│   │   ├── products/
│   │   │   ├── product-a.w5h1
│   │   │   ├── product-b.w5h1
│   │   │   └── roadmaps/
│   │   └── platforms/
│   │       └── internal-tools.w5h1
│   ├── competencies/
│   │   ├── core-competencies.w5h1     # What we're best at
│   │   ├── technical-stack.w5h1       # Technologies we master
│   │   ├── domain-expertise.w5h1      # Industries we understand
│   │   └── certifications/            # Validated capabilities
│   ├── resources/
│   │   ├── team-capabilities.w5h1     # Team skills matrix
│   │   ├── infrastructure.w5h1        # Technical resources
│   │   ├── partnerships.w5h1          # Strategic partners
│   │   └── ip-portfolio.w5h1          # Intellectual property
│   └── dependencies/
│       └── capability-graph.json      # How capabilities relate
│
├── L2-BEHAVIORS/                # HOW - How we operate
│   ├── README.md
│   ├── strategic/                     # APPROACH - Top-down initiatives
│   │   ├── planning-process.w5h1      # How we approach planning
│   │   ├── resource-allocation.w5h1   # How we allocate resources
│   │   ├── performance-management.w5h1
│   │   ├── risk-management.w5h1
│   │   └── governance-model.w5h1
│   ├── tactical/                      # RESPONSE - Bottom-up feedback
│   │   ├── market-response.w5h1       # How we respond to market feedback
│   │   ├── customer-feedback.w5h1     # How we respond to customer signals
│   │   ├── performance-metrics.w5h1   # What we observe and measure
│   │   ├── continuous-improvement.w5h1 # How observations inform refinement
│   │   ├── incident-response.w5h1     # How we respond to issues
│   │   └── adaptive-planning.w5h1     # How reality shapes strategy
│   ├── operational/
│   │   ├── daily-standups.w5h1
│   │   ├── weekly-retros.w5h1
│   │   ├── quarterly-reviews.w5h1
│   │   └── annual-strategy.w5h1
│   ├── communication/
│   │   ├── internal-comms.w5h1        # How we communicate internally
│   │   ├── stakeholder-communication.w5h1  # How we engage stakeholders
│   │   ├── public-relations.w5h1      # How we communicate publicly
│   │   └── crisis-communication.w5h1
│   └── flows/
│       ├── approach-flow.graph        # Strategy → Tactics (our approach)
│       ├── response-flow.graph        # Environment → Strategy (market response)
│       └── feedback-loops.w5h1        # How behaviors adapt bidirectionally
│
├── L1-ENVIRONMENT/              # WHERE/WHEN - Context we operate in
│   ├── README.md
│   ├── market/
│   │   ├── target-markets.w5h1        # Geographic/vertical markets
│   │   ├── market-analysis/
│   │   │   ├── competitive-landscape.w5h1
│   │   │   ├── market-trends.w5h1
│   │   │   ├── industry-analysis.w5h1
│   │   │   └── regulatory-environment.w5h1
│   │   └── customer-segments/
│   │       ├── segment-profiles.w5h1
│   │       ├── buyer-personas/
│   │       └── customer-journeys/
│   ├── timing/
│   │   ├── business-cycles.w5h1       # When we're busy/slow
│   │   ├── market-windows.w5h1        # When to enter markets
│   │   ├── seasonal-patterns.w5h1     # Seasonal behaviors
│   │   └── milestones.w5h1            # Key dates and events
│   ├── locations/
│   │   ├── physical-presence.w5h1     # Offices, facilities
│   │   ├── digital-presence.w5h1      # Online properties
│   │   ├── service-areas.w5h1         # Where we serve
│   │   └── supply-chain.w5h1          # Physical/digital supply chain
│   ├── stakeholders/
│   │   ├── customers.w5h1             # For whom we exist
│   │   ├── partners.w5h1              # Who we work with
│   │   ├── investors.w5h1             # Who funds us
│   │   ├── employees.w5h1             # Who we employ
│   │   └── community.w5h1             # Who we impact
│   └── constraints/
│       ├── legal-compliance.w5h1      # Legal boundaries
│       ├── resource-constraints.w5h1  # What we lack
│       ├── technical-constraints.w5h1 # Technical limits
│       └── market-constraints.w5h1    # Market realities
│
└── .git/                        # Version control (the evolution layer)
    └── hooks/
        └── commit-msg           # SixSpec commit validator
```

---

## The .w5h1 File Format

Every `.w5h1` file is a YAML-formatted dimensional specification:

```yaml
# L6-MISSION/mission-statement.w5h1
---
# SixSpec W5H1 Specification
level: MISSION
created: 2024-01-15
last_updated: 2024-01-15
status: active

# Core Triple (Subject-Predicate-Object)
subject: "Our Organization"
predicate: "exists to"
object: "democratize access to AI-powered research"

# Six Dimensions
dimensions:
  WHO:
    value: "Researchers, students, and knowledge workers globally"
    confidence: 1.0
    sources:
      - "Founding charter"
      - "Market research Q4 2023"

  WHAT:
    value: "Build tools that make AI-enhanced research accessible and affordable"
    confidence: 0.95
    sources:
      - "Product strategy 2024"

  WHEN:
    value: "Now through 2030, with focus on education sector first"
    confidence: 0.85
    sources:
      - "Strategic plan 2024-2030"

  WHERE:
    value: "Global, starting with English-speaking markets"
    confidence: 0.90
    sources:
      - "Market entry strategy"

  HOW:
    value: "By creating intuitive, AI-powered annotation and knowledge management platforms"
    confidence: 0.80
    sources:
      - "Technical roadmap"
      - "Product development plan"

  WHY:
    value: "Because knowledge work is bottlenecked by information overload and siloed insights"
    confidence: 1.0
    sources:
      - "Problem validation interviews (n=50)"
      - "Market analysis"

# Relationships (Purpose Propagation)
parent_spec: null  # Top level has no parent
child_specs:
  - "../L5-IDENTITY/brand/brand-identity.w5h1"
  - "../L5-IDENTITY/values/core-values.w5h1"

# Metadata
tags:
  - mission
  - purpose
  - vision
  - foundational

validators:
  - required: [WHY, WHAT]
  - confidence_threshold: 0.7

# Provenance
created_by: "Founding team"
approved_by: "Board of Directors"
review_cycle: "Annual"
next_review: "2025-01-15"
```

---

## Workshop: L4-BELIEFS Structure

This is the most complex level because beliefs:
1. **Flow bidirectionally** (inform strategy ↑ and guide execution ↓)
2. **Are interconnected** (changing one affects others)
3. **Have confidence levels** (some validated, some assumed)
4. **Evolve with evidence** (must track validation/invalidation)

### Proposed L4-BELIEFS Detailed Structure

```
L4-BELIEFS/
├── README.md                     # Philosophy: How beliefs guide us
│
├── principles/                   # Core operating principles
│   ├── _index.w5h1              # Overview with belief hierarchy
│   ├── decision-making/
│   │   ├── framework.w5h1       # How we decide
│   │   ├── values-based.w5h1    # When values conflict, how to choose
│   │   ├── data-driven.w5h1     # Role of data in decisions
│   │   └── intuition-vs-analysis.w5h1
│   ├── quality/
│   │   ├── definition.w5h1      # What quality means to us
│   │   ├── speed-vs-quality.w5h1
│   │   ├── technical-debt.w5h1  # Our philosophy on debt
│   │   └── testing-philosophy.w5h1
│   ├── innovation/
│   │   ├── risk-tolerance.w5h1  # How much risk we accept
│   │   ├── experimentation.w5h1 # How we test new ideas
│   │   ├── failure-handling.w5h1
│   │   └── idea-generation.w5h1
│   └── sustainability/
│       ├── environmental.w5h1
│       ├── financial.w5h1
│       └── social-impact.w5h1
│
├── assumptions/                  # What we believe to be true
│   ├── _index.w5h1              # Overview: managing assumptions
│   ├── market/
│   │   ├── customer-needs.w5h1  # What customers want (assumed)
│   │   ├── willingness-to-pay.w5h1
│   │   ├── market-size.w5h1
│   │   └── competitive-dynamics.w5h1
│   ├── product/
│   │   ├── value-proposition.w5h1
│   │   ├── feature-importance.w5h1
│   │   ├── usability-assumptions.w5h1
│   │   └── technical-feasibility.w5h1
│   ├── organizational/
│   │   ├── team-capacity.w5h1
│   │   ├── hiring-assumptions.w5h1
│   │   ├── remote-work.w5h1
│   │   └── culture-assumptions.w5h1
│   ├── validated/               # Assumptions we've proven
│   │   ├── _validation-log.md
│   │   └── [moved from parent when validated]
│   └── invalidated/             # Assumptions proven wrong
│       ├── _invalidation-log.md
│       └── [moved from parent when disproven]
│
├── mental-models/               # How we think about problems
│   ├── _index.w5h1
│   ├── problem-solving/
│   │   ├── root-cause-analysis.w5h1
│   │   ├── first-principles.w5h1
│   │   ├── systems-thinking.w5h1
│   │   └── design-thinking.w5h1
│   ├── growth/
│   │   ├── growth-mindset.w5h1
│   │   ├── learning-culture.w5h1
│   │   ├── continuous-improvement.w5h1
│   │   └── feedback-loops.w5h1
│   ├── customer-centric/
│   │   ├── user-first.w5h1
│   │   ├── jobs-to-be-done.w5h1
│   │   └── customer-development.w5h1
│   └── collaboration/
│       ├── team-dynamics.w5h1
│       ├── transparency.w5h1
│       └── psychological-safety.w5h1
│
├── relationships/                # How beliefs connect and conflict
│   ├── belief-graph.json        # Machine-readable graph
│   ├── dependencies/
│   │   ├── _index.md            # Overview of dependencies
│   │   └── [auto-generated from belief-graph.json]
│   ├── conflicts/
│   │   ├── _index.md            # Known contradictions
│   │   ├── quality-vs-speed.w5h1
│   │   ├── innovation-vs-stability.w5h1
│   │   └── customer-vs-business.w5h1
│   └── reinforcements/
│       ├── _index.md            # Mutually reinforcing beliefs
│       └── [auto-generated from belief-graph.json]
│
├── evolution/                    # How beliefs change
│   ├── changelog.md             # Belief evolution log
│   ├── validation-process.w5h1  # How we validate beliefs
│   ├── revision-policy.w5h1     # When/how we revise
│   └── archived/
│       └── [deprecated beliefs with context]
│
└── meta/
    ├── belief-confidence.json   # Confidence scores per belief
    ├── last-review-dates.json   # When each belief was last examined
    └── validation-status.json   # Which beliefs need validation
```

### Example: L4-BELIEFS/assumptions/market/customer-needs.w5h1

```yaml
---
level: BELIEFS
created: 2024-01-10
last_updated: 2024-03-15
status: validation_needed
confidence: 0.65

subject: "Target customers"
predicate: "need"
object: "faster research workflow tools"

dimensions:
  WHO:
    value: "Academic researchers and graduate students"
    confidence: 0.85
    sources:
      - "User interviews (n=30)"

  WHAT:
    value: "Tools that reduce time from research question to validated insight"
    confidence: 0.70
    sources:
      - "Problem validation interviews"
      - "Competitive analysis"

  WHEN:
    value: "During literature review and synthesis phases"
    confidence: 0.60
    sources:
      - "User observation studies (n=10)"
    notes: "Needs more validation"

  WHERE:
    value: "In their research workflow, between reading and writing"
    confidence: 0.75

  HOW:
    value: "By automating annotation, extraction, and knowledge graph building"
    confidence: 0.50
    sources:
      - "Feature prioritization survey"
    notes: "Multiple approaches possible - needs experimentation"

  WHY:
    value: "To publish more papers and advance their careers faster"
    confidence: 0.90
    sources:
      - "Motivational interviews (n=50)"
      - "Literature on academic incentives"

# Purpose Propagation
parent_spec: "../../L5-IDENTITY/positioning/target-audience.w5h1"
child_specs:
  - "../../L3-CAPABILITIES/services/products/research-tool.w5h1"

# Assumption-Specific Metadata
assumption_type: "customer_need"
validation_status: "partially_validated"
validation_method: "customer_interviews"
sample_size: 30
confidence_threshold: 0.80
requires_validation_by: "2024-06-01"

# Related Beliefs
depends_on:
  - "../product/value-proposition.w5h1"
  - "willingness-to-pay.w5h1"
conflicts_with: []
reinforces:
  - "../../principles/quality/speed-vs-quality.w5h1"

# Evidence Trail
evidence:
  supporting:
    - type: "interview"
      date: "2024-01-15"
      count: 30
      summary: "25/30 researchers cited speed as top pain point"
      confidence_boost: +0.15
    - type: "survey"
      date: "2024-02-10"
      count: 100
      summary: "78% would pay for 50% time reduction"
      confidence_boost: +0.10
  contradicting:
    - type: "usage_data"
      date: "2024-03-01"
      summary: "Beta users spending more time, not less"
      confidence_penalty: -0.20
      status: "investigating"

# Validation Plan
validation:
  next_steps:
    - "A/B test with beta users"
    - "Time-tracking study (n=20)"
    - "Competitor feature analysis"
  success_criteria:
    - "50% reduction in research workflow time"
    - "80% of users report time savings"
    - "Increased confidence to 0.85+"

tags:
  - assumption
  - customer-need
  - validation-needed
  - high-priority
```

---

## Purpose Propagation Examples

### Top-Down (Strategy → Execution)

```
L6-MISSION/mission-statement.w5h1
  WHAT: "Democratize AI-powered research"
  ↓ (becomes child's WHY)

L5-IDENTITY/positioning/market-position.w5h1
  WHY: "Democratize AI-powered research"
  WHAT: "Be the accessible alternative to expensive enterprise tools"
  ↓

L4-BELIEFS/assumptions/market/willingness-to-pay.w5h1
  WHY: "Be the accessible alternative"
  WHAT: "Customers will pay $10-20/month, not $100+/month"
  ↓

L3-CAPABILITIES/services/products/research-tool.w5h1
  WHY: "Price point of $10-20/month"
  WHAT: "SaaS product with freemium model"
  ↓

L2-BEHAVIORS/tactical/deployment-pipeline.w5h1
  WHY: "Support freemium SaaS model"
  WHAT: "Automated CI/CD with feature flagging for tier management"
  ↓

L1-ENVIRONMENT/locations/digital-presence.w5h1
  WHY: "Automated deployment pipeline"
  WHAT: "AWS infrastructure with CloudFront CDN"
```

### Bottom-Up (Market Reality → Strategy)

```
L1-ENVIRONMENT/market/competitive-landscape.w5h1
  WHAT: "Competitors raising prices 30% annually"
  ↑ (informs parent)

L2-BEHAVIORS/strategic/resource-allocation.w5h1
  WHY: "Competitive price increases create opportunity"
  WHAT: "Allocate 60% of budget to product development"
  ↑

L3-CAPABILITIES/competencies/technical-stack.w5h1
  WHY: "Need to outcompete on features AND price"
  WHAT: "Build with cost-efficient open-source stack"
  ↑

L4-BELIEFS/principles/quality/technical-debt.w5h1
  WHY: "Must balance cost efficiency with quality"
  WHAT: "Accept 10% technical debt for 2x faster shipping"
  ↑

L5-IDENTITY/values/core-values.w5h1
  WHY: "Speed and cost matter to market position"
  WHAT: "Value: Pragmatic excellence over perfect solutions"
  ↑

L6-MISSION/mission-statement.w5h1
  WHY: "Market demands accessible, practical solutions"
  WHAT: [potentially] "Pivot from 'best research tool' to 'most accessible research tool'"
```

---

## ## Git Integration: Version Control as Consciousness Evolution

### Commit Message Format for Organizational Changes

```bash
# Example: Adding new belief
git add L4-BELIEFS/principles/innovation/risk-tolerance.w5h1
git commit -m "feat: define risk tolerance principle

WHY: Team needs clarity on acceptable innovation risks
HOW: Created dimensional spec with confidence thresholds
WHAT: Risk tolerance framework (0.7 confidence)
WHERE: L4-BELIEFS/principles/innovation/
WHO: Product and engineering teams
WHEN: For all new feature decisions

Links to:
- Parent: L5-IDENTITY/values/core-values.w5h1
- Child: L3-CAPABILITIES/competencies/core-competencies.w5h1"
```

### Querying Organizational Evolution

```python
from sixspec.git.history import DimensionalGitHistory
from pathlib import Path

# Load org history
org = DimensionalGitHistory(Path("/path/to/org-repo"))

# Query: How has our mission evolved?
mission_changes = org.query(where="L6-MISSION")
for commit in mission_changes:
    print(f"{commit.commit_hash}: {commit.need(Dimension.WHY)}")

# Query: All changes to beliefs about customers
customer_beliefs = org.query(
    where="L4-BELIEFS/assumptions/market",
    why="customer"
)

# Query: What drove pricing strategy changes?
pricing_history = org.trace_file_purpose(
    "L4-BELIEFS/assumptions/market/willingness-to-pay.w5h1"
)

# Analysis: Belief validation over time
beliefs = org.query(where="L4-BELIEFS/assumptions")
validated = [b for b in beliefs if "validation" in b.need(Dimension.HOW)]
print(f"Validation rate: {len(validated)/len(beliefs):.1%}")
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Create directory structure template
- [ ] Define .w5h1 YAML schema
- [ ] Build validators for each Dilts level
- [ ] Implement SixSpec git hooks
- [ ] Create starter templates for each level

### Phase 2: Core Functionality (Weeks 3-4)
- [ ] Build W5H1 file parser/validator
- [ ] Create CLI tool for file creation
- [ ] Implement purpose propagation validator
- [ ] Build relationship graph generator
- [ ] Create confidence tracking system

### Phase 3: Beliefs Engine (Weeks 5-6)
- [ ] Implement assumption validation workflow
- [ ] Build belief dependency tracker
- [ ] Create conflict detection system
- [ ] Implement evolution/changelog automation
- [ ] Build belief confidence dashboard

### Phase 4: Query & Analysis (Weeks 7-8)
- [ ] Extend DimensionalGitHistory for org queries
- [ ] Build provenance tracing for any file
- [ ] Create impact analysis tool
- [ ] Implement change propagation detector
- [ ] Build organizational insights dashboard

### Phase 5: AI Integration (Weeks 9-10)
- [ ] Train LLM on W5H1 format
- [ ] Build AI-assisted file creation
- [ ] Implement automated relationship detection
- [ ] Create AI-powered belief validation suggestions
- [ ] Build natural language query interface

---

## Use Cases

### 1. Strategic Planning
**Scenario**: Board wants to update mission statement

```bash
# Current mission
cat L6-MISSION/mission-statement.w5h1

# What would change downstream?
sixspec impact-analysis L6-MISSION/mission-statement.w5h1

# Output:
# Would affect:
# - 3 identity specs in L5-IDENTITY/
# - 12 beliefs in L4-BELIEFS/
# - 8 capabilities in L3-CAPABILITIES/
# - 45 behaviors in L2-BEHAVIORS/
# Total downstream impact: 68 files

# Make change with full context
git add L6-MISSION/mission-statement.w5h1
git commit -m "feat: refocus mission on accessibility

WHY: Market research shows price is #1 barrier (n=500)
HOW: Shifted from 'powerful' to 'accessible' positioning
WHAT: Mission emphasizes democratization over sophistication
WHERE: L6-MISSION/mission-statement.w5h1
CONFIDENCE: 0.85

Impact Analysis:
- L5 Identity: Brand needs repositioning
- L4 Beliefs: Pricing assumptions validated
- L3 Capabilities: Feature prioritization changes"
```

### 2. Belief Validation
**Scenario**: Testing assumption about customer willingness to pay

```bash
# Check current assumption
sixspec belief check L4-BELIEFS/assumptions/market/willingness-to-pay.w5h1

# Output:
# Status: validation_needed
# Confidence: 0.65
# Last validated: Never
# Evidence: 2 supporting, 1 contradicting
# Next review: 2024-06-01 (overdue)

# Run experiment, gather data
# Update with results

sixspec belief update \
  L4-BELIEFS/assumptions/market/willingness-to-pay.w5h1 \
  --add-evidence "pricing_test" \
  --result "validation_failed" \
  --confidence 0.35 \
  --move-to "invalidated/"

# Automated git commit:
# "refactor: invalidate pricing assumption
# 
# WHY: A/B test showed 60% churn at $20/month
# HOW: Moved to invalidated/, updated confidence to 0.35
# WHAT: Pricing assumption now contradicted by data
# 
# Downstream impacts:
# - L3: Product pricing strategy needs revision
# - L2: Revenue projections need update"
```

### 3. Capability Development
**Scenario**: Adding new service offering

```bash
# Create new capability
sixspec create capability \
  --name "ai-consulting" \
  --parent "L6-MISSION/mission-statement.w5h1"

# Wizard prompts:
# WHY does this capability exist?
> "Democratize AI-powered research" [inherited from parent]
#
# WHAT is this capability?
> "AI-powered research workflow consulting"
#
# WHO is this for?
> "Research institutions with 50+ researchers"
#
# HOW will we deliver this?
> "8-week engagement: assessment, training, implementation"
#
# Confidence level (0.0-1.0)?
> 0.70

# Creates:
# - L3-CAPABILITIES/services/consulting/ai-consulting.w5h1
# - Updates parent's child_specs list
# - Suggests related behaviors to create
# - Flags beliefs that need validation
```

### 4. Organizational Audit
**Scenario**: New investor wants to understand company

```bash
# Generate full organizational map
sixspec audit --output investor-deck/

# Generates:
# 1. org-structure.pdf - Visual Dilts hierarchy
# 2. purpose-chain.pdf - Full WHAT→WHY propagation
# 3. belief-map.pdf - All assumptions with confidence
# 4. capability-matrix.pdf - Services with evidence
# 5. evolution-timeline.pdf - Major changes over time
# 6. confidence-dashboard.pdf - What we know vs. assume

# Query: Show me high-confidence validated beliefs
sixspec query "
  SELECT * FROM L4-BELIEFS/assumptions/validated/
  WHERE confidence > 0.85
  ORDER BY validation_date DESC
"

# Query: What are our biggest strategic bets?
sixspec query "
  SELECT * FROM L4-BELIEFS/assumptions/
  WHERE confidence < 0.60 
    AND impact = 'high'
  ORDER BY confidence ASC
"
```

### 5. Culture Documentation
**Scenario**: Onboarding new team member

```bash
# Generate personalized onboarding pack
sixspec onboarding-pack --role "senior-engineer"

# Creates reading list:
# 1. L6-MISSION/mission-statement.w5h1 - Why we exist
# 2. L5-IDENTITY/values/core-values.w5h1 - Who we are
# 3. L4-BELIEFS/mental-models/problem-solving.w5h1 - How we think
# 4. L3-CAPABILITIES/competencies/technical-stack.w5h1 - What you'll use
# 5. L2-BEHAVIORS/tactical/code-review-process.w5h1 - How we work
# 6. Recent changes (last 90 days) to understand current focus

# Interactive exploration
sixspec explore --level L4-BELIEFS

# > What principles guide technical decisions?
# > How do we balance quality vs. speed?
# > What are our current assumptions about customers?
# > Which beliefs have been validated vs. assumed?
```

---

## Advanced Features

### 1. Automated Relationship Detection

```python
# Walker that builds belief dependency graph
class BeliefGraphWalker(GraphAgent):
    def traverse(self, start: W5H1) -> Graph:
        """
        Build graph of belief relationships by:
        1. Parsing all belief W5H1 files
        2. Detecting dimensional overlaps
        3. Identifying logical dependencies
        4. Flagging potential conflicts
        """
        graph = Graph()
        beliefs = self.load_all_beliefs()
        
        for belief in beliefs:
            # Add node
            graph.add_node(belief)
            
            # Detect dependencies
            for other in beliefs:
                if belief.depends_on_logically(other):
                    graph.add_edge(belief, other, type="depends")
                elif belief.conflicts_with(other):
                    graph.add_edge(belief, other, type="conflicts")
                elif belief.reinforces(other):
                    graph.add_edge(belief, other, type="reinforces")
        
        return graph

# Usage
walker = BeliefGraphWalker("belief-mapper")
graph = walker.traverse(start_belief)
graph.export("L4-BELIEFS/relationships/belief-graph.json")
```

### 2. Change Impact Analysis

```python
class ImpactAnalyzer(DiltsWalker):
    def analyze_change(self, file_path: str, new_content: W5H1) -> ImpactReport:
        """
        Analyze downstream impact of changing a W5H1 file:
        1. Load current version
        2. Compare dimensions
        3. Trace all child_specs
        4. Identify affected files
        5. Estimate confidence impact
        """
        current = self.load_w5h1(file_path)
        
        # What changed?
        changes = self.diff_dimensions(current, new_content)
        
        # Who inherits this WHAT as their WHY?
        children = self.trace_children(file_path)
        
        # How does confidence propagate?
        confidence_impact = self.calculate_confidence_cascade(
            changes, children
        )
        
        return ImpactReport(
            files_affected=len(children),
            dimensions_changed=changes,
            confidence_delta=confidence_impact,
            suggested_updates=self.generate_update_suggestions(children, changes)
        )

# Usage
analyzer = ImpactAnalyzer(level=DiltsLevel.BELIEFS)
impact = analyzer.analyze_change(
    "L4-BELIEFS/assumptions/market/customer-needs.w5h1",
    new_version
)

if impact.files_affected > 10:
    print(f"WARNING: {impact.files_affected} files need review")
    for suggestion in impact.suggested_updates:
        print(f"  - {suggestion.file}: {suggestion.change}")
```

### 3. Confidence Tracking Over Time

```python
class ConfidenceTracker:
    def track_belief_evolution(self, belief_file: str) -> Timeline:
        """
        Track how belief confidence changes over time:
        1. Parse git history for this file
        2. Extract confidence scores from each version
        3. Correlate with evidence added/removed
        4. Identify validation events
        """
        history = DimensionalGitHistory(self.repo_path)
        commits = history.trace_file_purpose(belief_file)
        
        timeline = Timeline()
        for commit in commits:
            belief = self.parse_w5h1_at_commit(belief_file, commit.commit_hash)
            
            timeline.add_point(
                date=commit.date,
                confidence=belief.get_confidence_overall(),
                event_type=self.classify_change(commit),
                evidence_count=len(belief.evidence_supporting),
                notes=commit.need(Dimension.WHY)
            )
        
        return timeline

# Usage
tracker = ConfidenceTracker(Path("/path/to/org"))
timeline = tracker.track_belief_evolution(
    "L4-BELIEFS/assumptions/market/customer-needs.w5h1"
)

# Output:
# 2024-01-10: Confidence 0.30 (created, initial assumption)
# 2024-01-25: Confidence 0.50 (+0.20, interviews n=30)
# 2024-02-15: Confidence 0.65 (+0.15, survey n=100)
# 2024-03-01: Confidence 0.45 (-0.20, usage data contradicts)
# 2024-03-15: Confidence 0.35 (-0.10, A/B test failed)
# → Status: VALIDATION FAILED, needs strategy pivot
```

### 4. Natural Language Queries

```python
class OrgQueryAgent(GraphAgent):
    def answer_question(self, question: str) -> Answer:
        """
        Answer natural language questions about the org:
        - "Why are we building feature X?"
        - "What assumptions underlie our pricing?"
        - "Who approved the mission change?"
        - "How has our risk tolerance evolved?"
        """
        # Parse question into dimensional query
        query = self.nlp_to_dimensional_query(question)
        
        # Map to file paths
        relevant_files = self.find_relevant_files(query)
        
        # Gather context
        context = self.gather_context(relevant_files, depth=2)
        
        # Trace provenance if needed
        if query.needs_provenance:
            chain = self.trace_provenance_chain(relevant_files[0])
            context.add_provenance(chain)
        
        # Generate answer
        return self.synthesize_answer(question, context)

# Usage
agent = OrgQueryAgent("org-qa")

answer = agent.answer_question(
    "Why are we building the AI research tool?"
)

# Returns:
# Level 1 (Direct): To democratize AI-powered research [L6-MISSION]
# Level 2 (Strategic): To capture education market before competitors [L5-IDENTITY]
# Level 3 (Tactical): To validate customer willingness to pay $15/month [L4-BELIEFS]
# 
# Confidence: 0.85 (Mission), 0.75 (Strategy), 0.65 (Validation)
# 
# Evidence:
# - 50 problem validation interviews
# - Market analysis showing 30% annual growth
# - Competitor pricing analysis
#
# Related files:
# - L6-MISSION/mission-statement.w5h1
# - L5-IDENTITY/positioning/market-position.w5h1
# - L4-BELIEFS/assumptions/market/willingness-to-pay.w5h1
```

---

## CLI Tool Specification

### Core Commands

```bash
# Initialize org repo
sixspec init <org-name>
  --template [startup|enterprise|nonprofit|personal]
  --levels [1-6]  # Which Dilts levels to include

# Create new W5H1 file
sixspec create <level> <name>
  --parent <parent-file>
  --wizard  # Interactive mode
  --template <template-name>

# Validate file(s)
sixspec validate <file-or-directory>
  --fix  # Auto-fix common issues
  --strict  # Enforce all validators

# Query the org
sixspec query <query-string>
  --format [json|yaml|table|graph]
  --output <file>

# Analyze impact
sixspec impact <file>
  --what-if <new-value>  # Simulate change
  --depth [1-6]  # How deep to trace

# Belief operations
sixspec belief check <belief-file>
sixspec belief validate <belief-file> --evidence <evidence-file>
sixspec belief invalidate <belief-file> --reason <reason>
sixspec belief move <belief-file> --to [validated|invalidated]

# Relationship operations
sixspec graph build  # Build relationship graphs
sixspec graph show <file>  # Show file's relationships
sixspec graph find-conflicts  # Detect belief conflicts

# Reporting
sixspec report <report-type>
  # Types: audit, evolution, confidence, impact, beliefs
  --output <directory>
  --format [pdf|html|markdown]

# Exploration
sixspec explore
  --level <level>
  --interactive

# Git integration
sixspec log <file>  # Enhanced git log with dimensional info
sixspec trace <file>  # Full provenance chain
sixspec why <file>  # Why does this exist? (full chain)
```

### Example Workflow

```bash
# 1. Initialize new organization
sixspec init "AI Research Co" --template startup

# 2. Customize mission
cd "AI-Research-Co"
sixspec create mission primary-mission --wizard

# WHY does your organization exist?
> Because researchers waste 60% of time on manual tasks

# WHAT will you do about it?
> Build AI-powered research workflow automation

# WHO will benefit?
> Academic researchers and graduate students

# Confidence in this mission (0.0-1.0)?
> 0.85

# Created: L6-MISSION/primary-mission.w5h1

# 3. Define identity
sixspec create identity brand-identity \
  --parent L6-MISSION/primary-mission.w5h1

# 4. Document assumptions
sixspec create belief assumption/market/customer-pain \
  --parent L5-IDENTITY/brand-identity.w5h1 \
  --confidence 0.60 \
  --validation-needed

# 5. Add evidence over time
sixspec belief validate \
  L4-BELIEFS/assumptions/market/customer-pain.w5h1 \
  --evidence "interviews_jan_2024.json" \
  --confidence-boost 0.15

# 6. Query organizational knowledge
sixspec query "show all assumptions with confidence < 0.70"

# 7. Analyze proposed changes
sixspec impact L6-MISSION/primary-mission.w5h1 \
  --what-if "WHAT: Build collaborative research platforms"

# Output:
# Impact Analysis:
# - 23 files would need review
# - 5 beliefs would need revalidation
# - 3 capabilities would become misaligned
# - Estimated effort: 40 hours
#
# Proceed? [y/N]

# 8. Generate reports
sixspec report audit --output investor-deck/ --format pdf
```

---

## Integration with Your Research Tool

### Applying This to Your AI Research Tool Project

You can use this Dilts directory structure as **the organizational backbone** for your research tool development:

```
research-tool-org/
├── L6-MISSION/
│   └── mission.w5h1
│       # WHY: Bridge gap between AI research and structured knowledge
│       # WHAT: Build AI-powered annotation and research collaboration platform
│
├── L5-IDENTITY/
│   ├── brand/brand-identity.w5h1
│   │   # WHO: Researchers, students, knowledge workers
│   │   # WHAT: The accessible research companion
│   └── positioning/differentiation.w5h1
│       # WHY: Notion/Obsidian lack AI intelligence, ChatGPT lacks structure
│       # WHAT: Structured + AI-powered + Collaborative
│
├── L4-BELIEFS/
│   ├── assumptions/product/
│   │   ├── annotation-value.w5h1
│   │   │   # Assumption: Users need AI-assisted annotation
│   │   │   # Confidence: 0.75
│   │   │   # Evidence: User interviews n=30
│   │   ├── graph-database-value.w5h1
│   │   │   # Assumption: Graph > relational for research
│   │   │   # Confidence: 0.85
│   │   │   # Evidence: Literature + prototyping
│   │   └── collaboration-need.w5h1
│   │       # Assumption: Teams want shared research spaces
│   │       # Confidence: 0.60
│   │       # Status: needs_validation
│   └── principles/development/
│       ├── mvp-scope.w5h1
│       │   # Belief: Start with solo researcher, add collaboration later
│       │   # Confidence: 0.90
│       └── tech-stack.w5h1
│           # Belief: Cloud-native, API-first, LLM-integrated
│           # Confidence: 0.95
│
├── L3-CAPABILITIES/
│   ├── services/products/
│   │   └── research-annotation-tool.w5h1
│   │       # WHAT: Browser extension + web app + API
│   │       # HOW: React + FastAPI + Neo4j + OpenAI
│   │       # Features: annotation, extraction, graph building, querying
│   └── competencies/
│       ├── ai-integration.w5h1
│       ├── graph-databases.w5h1
│       └── research-workflows.w5h1
│
├── L2-BEHAVIORS/
│   ├── strategic/
│   │   ├── feature-prioritization.w5h1
│   │   │   # HOW: Value vs. Effort matrix + user feedback
│   │   └── mvp-iteration.w5h1
│   │       # HOW: 2-week sprints, user testing every sprint
│   └── tactical/
│       ├── development-workflow.w5h1
│       ├── ai-testing-strategy.w5h1
│       └── user-feedback-collection.w5h1
│
└── L1-ENVIRONMENT/
    ├── market/
    │   ├── target-users.w5h1
    │   │   # WHO: Academic researchers, consultants, analysts
    │   │   # WHERE: Global, English-speaking initially
    │   └── competitive-landscape.w5h1
    │       # WHEN: Market window open due to AI advances
    │       # WHERE: Competing with Notion, Obsidian, Zotero, ChatGPT
    └── constraints/
        ├── budget-constraints.w5h1
        └── technical-constraints.w5h1
```

### Linking to Your Development Workflow

```bash
# Every product decision traces to mission
sixspec why features/ai-annotation.py

# Output:
# L1 (Implementation): AI-powered annotation feature
#   WHY: Enable efficient research synthesis [L2-BEHAVIORS]
# L2 (Behavior): Efficient research synthesis workflow
#   WHY: Deliver core value proposition [L3-CAPABILITIES]
# L3 (Capability): Research annotation tool
#   WHY: Bridge AI and structured knowledge [L4-BELIEFS]
# L4 (Belief): Graph databases superior for research
#   WHY: Structured knowledge enables collaboration [L5-IDENTITY]
# L5 (Identity): The structured research companion
#   WHY: Democratize AI-powered research [L6-MISSION]
# L6 (Mission): Make AI research accessible to all

# Validate assumptions during development
sixspec belief check \
  L4-BELIEFS/assumptions/product/annotation-value.w5h1

# Move to validated after user testing
sixspec belief validate \
  L4-BELIEFS/assumptions/product/annotation-value.w5h1 \
  --evidence "beta-testing-results.json" \
  --confidence 0.90

# Track evolution of product thinking
sixspec report evolution \
  --filter L4-BELIEFS/assumptions/product/ \
  --since "2024-01-01"
```

This structure ensures:
1. **Every feature has traceable purpose** (WHAT→WHY chain)
2. **Assumptions are explicitly managed** (validated vs. assumed)
3. **Strategic decisions are documented** (not lost in Slack)
4. **Team alignment is visible** (everyone sees the same org graph)
5. **Pivots are evidence-based** (confidence scores drive decisions)

---

## Conclusion

This Dilts-based directory structure transforms organizational knowledge from **implicit and scattered** to **explicit and structured**:

- **Mission isn't a poster** → It's a `.w5h1` file with full dimensional context
- **Values aren't platitudes** → They're traceable to behaviors and validated assumptions
- **Strategy isn't a slide deck** → It's a living graph of beliefs and capabilities
- **Culture isn't vague** → It's documented behaviors with clear WHY chains
- **Evolution isn't forgotten** → Git history captures every change with purpose

The result is a **living digital twin of your organization** that:
- AI agents can query and understand
- Teams can navigate and contribute to
- Leaders can analyze and optimize
- New members can explore and internalize

**Your organization becomes as queryable as your codebase.**

