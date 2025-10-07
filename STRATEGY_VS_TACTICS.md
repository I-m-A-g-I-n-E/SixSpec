# Strategy vs. Tactics in the Dilts Framework

## Core Distinction

**STRATEGY = APPROACH** (How we initiate)  
**TACTICS = RESPONSE** (How we adapt)

---

## Definitions

### Strategy (Approach)

> **Measured initiatives designed to serve the market through our identity, with beliefs formed by capabilities enacted through behaviors upon the environment.**

**Direction**: Top-down (L6 → L1)  
**Nature**: Proactive, planned, intentional  
**Origin**: Internal (derived from mission, identity, beliefs)  
**Purpose**: Act upon the environment according to our intent

**Flow**:
```
MISSION (FOR WHAT we exist)
  ↓
IDENTITY (WHO we are)
  ↓
BELIEFS (WHY we choose this approach)
  ↓
CAPABILITIES (WHAT we can deliver)
  ↓
BEHAVIORS - STRATEGIC (HOW we approach)
  ↓
ENVIRONMENT (WHERE/WHEN we act)
```

### Tactics (Response)

> **Measured responses to the market we serve, giving us feedback that serves to evaluate our behaviors, inform our capabilities, revise our beliefs, possibly update our identity, and further refine our mission.**

**Direction**: Bottom-up (L1 → L6)  
**Nature**: Reactive, adaptive, learning-driven  
**Origin**: External (market feedback, observations, reality)  
**Purpose**: Learn from the environment to refine our approach

**Flow**:
```
ENVIRONMENT (WHAT we observe)
  ↑
BEHAVIORS - TACTICAL (HOW we respond)
  ↑
CAPABILITIES (WHAT we update/add)
  ↑
BELIEFS (WHY we revise assumptions)
  ↑
IDENTITY (WHO we may need to become)
  ↑
MISSION (FOR WHAT we truly exist)
```

---

## The Bidirectional Cycle

### Complete Cycle

```
     STRATEGY (Approach)
          ↓
    ┌─────────────┐
    │   MISSION   │  6
    └─────────────┘
          ↓
    ┌─────────────┐
    │  IDENTITY   │  5
    └─────────────┘
          ↓
    ┌─────────────┐
    │   BELIEFS   │  4  ← Tactics inform here
    └─────────────┘
          ↓
    ┌─────────────┐
    │ CAPABILITIES│  3  ← Tactics inform here
    └─────────────┘
          ↓
    ┌─────────────┐
    │  BEHAVIORS  │  2  ← Strategy meets Tactics
    │  Strategic  │     → Approach (top-down)
    │  Tactical   │     ← Response (bottom-up)
    └─────────────┘
          ↓ ↑
    ┌─────────────┐
    │ ENVIRONMENT │  1  ← We act here
    └─────────────┘     → It responds
          
     TACTICS (Response)
```

### L2 as the Pivot Point

**L2-BEHAVIORS is unique**: It's where strategy becomes action AND where feedback becomes learning.

```
L2-BEHAVIORS/
├── strategic/       APPROACH - "What we're going to do"
│   ├── planning-process.w5h1
│   ├── resource-allocation.w5h1
│   └── market-entry-strategy.w5h1
│
└── tactical/        RESPONSE - "What we learned"
    ├── market-response.w5h1
    ├── customer-feedback.w5h1
    └── performance-observations.w5h1
```

---

## Examples

### Example 1: Product Launch

**STRATEGIC APPROACH** (Top-down):

```yaml
# L6: MISSION
WHY: "Accelerate innovation through accessible technology"

# L5: IDENTITY
WHO: "The trusted partner for digital transformation"

# L4: BELIEFS
WHAT: "Enterprises value speed + security equally"
confidence: 0.75  # Assumption, needs validation

# L3: CAPABILITIES
WHAT: "DevSecOps platform with compliance automation"

# L2: BEHAVIORS (Strategic)
APPROACH: "Launch enterprise tier with SOC2 + HIPAA in Q2"
HOW: "Quarterly rollout to Fortune 500 through channel partners"

# L1: ENVIRONMENT
ACTION: "Deploy to 50 enterprise prospects"
```

**TACTICAL RESPONSE** (Bottom-up):

```yaml
# L1: ENVIRONMENT
OBSERVATION: "60% adoption, but 40% cite complexity as barrier"
WHERE: "Trial data, support tickets, churn surveys"
confidence: 1.0  # Direct observation

# L2: BEHAVIORS (Tactical)
RESPONSE: "Add onboarding wizard, reduce config steps by 60%"
HOW: "Weekly metrics review → rapid prototyping → A/B testing"

# L3: CAPABILITIES (Updated)
ADD: "Guided onboarding capability"
UPDATE: "Self-service platform now includes wizard"

# L4: BELIEFS (Revised)
ORIGINAL: "Enterprises value speed + security" (conf: 0.75)
REVISED: "Enterprises value speed + security + SIMPLICITY" (conf: 0.95)
EVIDENCE: "40% drop-off reduced to 10% after wizard added"

# L5: IDENTITY (Refined)
UPDATE: "Emphasize 'powerful yet simple' in brand messaging"

# L6: MISSION (Validated)
CONFIRMATION: "Accessible technology" means simple, not just fast
```

### Example 2: Market Expansion

**STRATEGIC APPROACH**:

```yaml
# L6-L5-L4 Chain
MISSION: "Transform lives through equitable education"
IDENTITY: "Champion of accessible learning"
BELIEF: "International markets ready for English-language content" (conf: 0.65)

# L3: CAPABILITY
WHAT: "Multi-language course platform"

# L2: STRATEGIC
APPROACH: "Launch in 5 non-English markets simultaneously"
TIMELINE: "Q3 2024"

# L1: ENVIRONMENT
ACTION: "Deploy to India, Brazil, Germany, Japan, France"
```

**TACTICAL RESPONSE**:

```yaml
# L1: OBSERVATION
RESULT: "India: 200% growth | Brazil: 150% | Germany: 80% | Japan: 30% | France: 20%"

# L2: TACTICAL
RESPONSE: 
  - "Double-down on India and Brazil"
  - "Pause Germany expansion"
  - "Cancel Japan and France (low ROI)"
  - "Investigate: Why India/Brazil succeeded vs. Germany/Japan/France?"

# L3: UPDATE
ADD: "Regional localization capability (not just translation)"
INSIGHT: "Success requires cultural adaptation, not just language"

# L4: REVISION
ORIGINAL: "International markets ready for English content" (conf: 0.65)
REVISED: "Emerging markets adopt faster than developed markets" (conf: 0.85)
REVISED: "Translation insufficient; cultural adaptation required" (conf: 0.90)

# L5: REFINEMENT
UPDATE: "Global champion of accessible learning, culturally adapted"

# L6: VALIDATION
INSIGHT: "Equity means meeting people where they are culturally, not just linguistically"
```

### Example 3: Pricing Strategy

**STRATEGIC APPROACH**:

```yaml
# L4: BELIEF
ASSUMPTION: "Market will pay $50/month for premium features" (conf: 0.60)

# L3: CAPABILITY
WHAT: "Three-tier pricing: Free, Pro ($50/mo), Enterprise ($custom)"

# L2: STRATEGIC
APPROACH: "Launch with $50 Pro tier, promote heavily"

# L1: ACTION
EXECUTE: "Launch pricing page, email campaign, sales push"
```

**TACTICAL RESPONSE**:

```yaml
# L1: OBSERVATION
RESULT: "5% conversion to Pro, 60% churn after first month"
FEEDBACK: "Too expensive" (85% of surveys)

# L2: TACTICAL
RESPONSE: "A/B test pricing: $20, $35, $50"
RESULT: "$20: 15% conversion, 30% churn | $35: 12% conversion, 25% churn"

# L3: UPDATE
REVISE: "Pro tier at $35/month"
ADD: "Annual discount option (20% off)"

# L4: REVISION
ORIGINAL: "Market will pay $50/month" (conf: 0.60) → INVALIDATED
VALIDATED: "Market will pay $35/month" (conf: 0.90)
LEARNED: "Annual discounts increase LTV and retention"

# L5: REFINEMENT (if needed)
NO CHANGE: Identity still aligned ("accessible" confirmed by pricing sensitivity)

# L6: VALIDATION
CONFIRMED: Mission of accessibility requires price consciousness
```

---

## Strategic vs. Tactical Behaviors

### Strategic Behaviors (APPROACH)

**Characteristics**:
- Planned in advance
- Based on beliefs and assumptions
- Confidence: 0.60-0.90 (assumptions)
- Directional: Top-down
- Question: "What should we do?"

**Examples**:
- Market entry plans
- Product roadmaps
- Resource allocation
- Partnership strategies
- Brand campaigns
- Pricing strategies
- Expansion plans

**File naming**:
- `strategic-planning-process.w5h1`
- `q2-market-entry-strategy.w5h1`
- `annual-resource-allocation.w5h1`

### Tactical Behaviors (RESPONSE)

**Characteristics**:
- Reactive to observations
- Based on data and feedback
- Confidence: 0.85-1.0 (observations)
- Directional: Bottom-up
- Question: "What did we learn?"

**Examples**:
- Customer feedback analysis
- Market response measurement
- Performance metrics review
- Competitive intelligence
- Incident learnings
- Churn analysis
- A/B test results

**File naming**:
- `customer-feedback-response.w5h1`
- `q2-market-response-analysis.w5h1`
- `performance-metrics-review.w5h1`

---

## When to Use Which

### Use STRATEGIC (Approach) when:

✅ Planning future initiatives  
✅ Allocating resources  
✅ Making product decisions  
✅ Entering new markets  
✅ Launching campaigns  
✅ Setting policies  

**Confidence**: Typically 0.60-0.85 (based on assumptions)  
**Direction**: "We believe X, so we'll do Y"  
**Files**: Go in `L2-BEHAVIORS/strategic/`

### Use TACTICAL (Response) when:

✅ Analyzing market feedback  
✅ Reviewing performance data  
✅ Responding to competitive moves  
✅ Learning from experiments  
✅ Adapting to observations  
✅ Revising assumptions  

**Confidence**: Typically 0.85-1.0 (based on data)  
**Direction**: "We observed X, so we'll adapt Y"  
**Files**: Go in `L2-BEHAVIORS/tactical/`

---

## The Learning Loop

### Healthy Organization

```
STRATEGY → ACTION → OBSERVATION → LEARNING → UPDATED STRATEGY
   ↓          ↓           ↓            ↓              ↓
  Plan    Execute    Measure      Analyze        Improve
  (0.70)   (L1)      (1.0)        (0.90)         (0.85)
```

**Signs of health**:
- Strategies tested through tactics
- Beliefs updated based on evidence
- Confidence increases with validation
- Failed strategies moved to `invalidated/`
- Successful patterns formalized

### Unhealthy Organization

```
STRATEGY → ACTION → ??? → REPEAT STRATEGY
   ↓          ↓      (no feedback loop)
  Plan    Execute      
  (0.70)   (L1)        

Result: Same confidence, no learning, repeated mistakes
```

**Signs of dysfunction**:
- No tactical response files
- Beliefs never updated
- Confidence remains low
- No files in `validated/` or `invalidated/`
- Same strategies repeated despite failure

---

## Implementation Guidelines

### 1. Create Both Directories

```
L2-BEHAVIORS/
├── strategic/     # Your plans
└── tactical/      # What you learned
```

### 2. Link Strategic to Beliefs

```yaml
# strategic/market-entry-strategy.w5h1
WHY: 
  value: "From L4: Market ready for our solution"
  confidence: 0.70  # Assumption
```

### 3. Link Tactical to Environment

```yaml
# tactical/market-response.w5h1
WHERE:
  value: "From L1: Trial data, customer surveys"
  confidence: 1.0  # Observation
```

### 4. Show the Update

```yaml
# tactical/market-response.w5h1
IMPACT:
  belief_updated: "L4: Market ready (0.70 → 0.85)"
  evidence: "60% conversion rate, 40% say 'exactly what we needed'"
```

### 5. Cycle Continues

Updated belief (now 0.85) informs next strategic decision with higher confidence.

---

## Key Insights

### 1. Strategy Without Tactics = Guessing

If you only have `strategic/` directory:
- No learning loop
- Confidence doesn't improve
- Mistakes repeated
- Beliefs never validated

**Fix**: Create `tactical/` and document what you observe.

### 2. Tactics Without Strategy = Reactive

If you only have `tactical/` directory:
- No clear intent
- Random walk
- No alignment to mission
- Opportunistic, not strategic

**Fix**: Create `strategic/` and document your approach.

### 3. Both Together = Learning Organization

When you have both:
- Clear intent (strategy)
- Reality check (tactics)
- Continuous improvement
- Evidence-based decisions
- Confidence increases over time

**Result**: Organizational intelligence.

---

## Validation Workflow

### Step 1: Strategic Hypothesis

```yaml
# strategic/pricing-hypothesis.w5h1
BELIEF: "Market will pay $50/month"
CONFIDENCE: 0.60
APPROACH: "Launch at $50, measure conversion"
```

### Step 2: Execute

Deploy pricing, measure results.

### Step 3: Tactical Observation

```yaml
# tactical/pricing-results.w5h1
OBSERVATION: "5% conversion, 60% churn, 'too expensive'"
CONFIDENCE: 1.0  # Direct measurement
```

### Step 4: Update Belief

```yaml
# L4-BELIEFS/assumptions/invalidated/pricing-50.w5h1
ORIGINAL: "Market will pay $50/month" (conf: 0.60)
STATUS: "INVALIDATED"
EVIDENCE: "5% conversion, well below 15% target"
MOVED: 2024-03-15
```

### Step 5: New Strategy

```yaml
# strategic/revised-pricing-strategy.w5h1
BELIEF: "Market will pay $35/month"
CONFIDENCE: 0.70  # Educated guess based on feedback
APPROACH: "A/B test $35, measure again"
```

### Step 6: Cycle Repeats

Eventually, find validated price point, move to `validated/`, use with high confidence.

---

## Summary

**Strategy (Approach)**:
- Top-down
- Intent-driven
- Based on beliefs
- Lower confidence (0.60-0.85)
- Question: "What should we do?"
- Files: `strategic/`

**Tactics (Response)**:
- Bottom-up
- Feedback-driven
- Based on observations
- Higher confidence (0.85-1.0)
- Question: "What did we learn?"
- Files: `tactical/`

**Together**: Learning loop that increases organizational intelligence.

**The Goal**: Strategy increasingly informed by validated tactics, reducing guesswork, increasing confidence, improving outcomes.

---

## Usage in Framework

1. **Document strategies** in `L2-BEHAVIORS/strategic/`
2. **Measure outcomes** in `L1-ENVIRONMENT/`
3. **Analyze feedback** in `L2-BEHAVIORS/tactical/`
4. **Update beliefs** in `L4-BELIEFS/`
5. **Refine identity** in `L5-IDENTITY/` (if needed)
6. **Validate mission** in `L6-MISSION/` (rarely changes)

**Result**: Every strategy is eventually tested, every belief is eventually validated or invalidated, and organizational confidence increases over time.

Your organization learns.
