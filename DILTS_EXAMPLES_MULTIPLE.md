# Dilts Levels: Multiple Examples Per Level

This document provides 2-3 diverse examples for each Dilts level to illustrate the framework's universality.

---

## L6 - MISSION (FOR WHAT)

**Extreme Autonomy** - Can question existence itself

### Example 1: Technology Company
```yaml
subject: "Our Organization"
predicate: "exists to"
object: "accelerate global innovation through accessible technology"

dimensions:
  WHY:
    value: "Innovation is bottlenecked by complexity and cost barriers"
    confidence: 0.95
  
  WHAT:
    value: "Build tools that make advanced technology accessible to everyone"
    confidence: 0.90
```

### Example 2: Educational Institution
```yaml
subject: "Our Institution"
predicate: "exists to"
object: "transform lives through equitable access to knowledge"

dimensions:
  WHY:
    value: "Education is the foundation of opportunity and economic mobility"
    confidence: 1.0
  
  WHAT:
    value: "Provide world-class education regardless of background or location"
    confidence: 0.95
```

### Example 3: Environmental Organization
```yaml
subject: "Our Organization"
predicate: "exists to"
object: "solve climate crisis through data-driven action"

dimensions:
  WHY:
    value: "Climate change threatens human civilization and requires urgent coordinated response"
    confidence: 1.0
  
  WHAT:
    value: "Provide actionable climate intelligence to decision-makers globally"
    confidence: 0.85
```

---

## L5 - IDENTITY (WHO)

**High Autonomy** - Can redefine what we are

### Example 1: Tech Startup Identity
```yaml
subject: "Our Brand"
predicate: "represents"
object: "the trusted partner for digital transformation"

dimensions:
  WHO:
    value: "Technical excellence meets human-centered design"
    confidence: 0.85
  
  WHAT:
    value: "Brand that balances innovation with reliability"
    confidence: 0.80
  
  WHY:
    value: "Accelerate global innovation through accessible technology"  # From L6
    confidence: 0.90
```

### Example 2: Nonprofit Identity
```yaml
subject: "Our Organization"
predicate: "embodies"
object: "radical transparency and community-first values"

dimensions:
  WHO:
    value: "Open, inclusive, impact-driven change agents"
    confidence: 0.95
  
  WHAT:
    value: "Culture of radical transparency with quarterly public reporting"
    confidence: 0.90
  
  WHY:
    value: "Transform lives through equitable access to knowledge"  # From L6
    confidence: 0.95
```

### Example 3: Enterprise Identity
```yaml
subject: "Our Corporation"
predicate: "stands for"
object: "sustainable growth with uncompromising quality"

dimensions:
  WHO:
    value: "Premium brand synonymous with reliability and innovation"
    confidence: 0.90
  
  WHAT:
    value: "Positioning: The quality leader, not the cheapest option"
    confidence: 0.85
  
  WHY:
    value: "Solve climate crisis through data-driven action"  # From L6
    confidence: 0.85
```

---

## L4 - BELIEFS (WHY)

**Moderate Autonomy** - Can choose principles

### Example 1: Product Assumption
```yaml
subject: "Target customers"
predicate: "need"
object: "self-service onboarding over white-glove support"

dimensions:
  WHO:
    value: "SMB customers with technical competency"
    confidence: 0.70
  
  WHAT:
    value: "Preference for DIY with documentation vs. live support"
    confidence: 0.60  # Needs validation
  
  WHY:
    value: "Be trusted partner for digital transformation"  # From L5
    confidence: 0.85

assumption_type: "customer_preference"
validation_status: "needs_validation"
evidence:
  supporting:
    - type: "survey"
      sample_size: 50
      summary: "60% prefer self-service"
```

### Example 2: Technical Principle
```yaml
subject: "Our Engineering Team"
predicate: "believes in"
object: "quality over speed for core infrastructure"

dimensions:
  WHY:
    value: "Sustainable growth with uncompromising quality"  # From L5
    confidence: 0.90
  
  WHAT:
    value: "Core systems: 90% test coverage, comprehensive reviews"
    confidence: 0.95
  
  HOW:
    value: "Trade slower initial delivery for long-term maintainability"
    confidence: 0.90

assumption_type: "engineering_principle"
validation_status: "validated"  # Proven over time
```

### Example 3: Market Belief
```yaml
subject: "The market"
predicate: "is shifting toward"
object: "privacy-first products with ethical AI"

dimensions:
  WHAT:
    value: "Customers increasingly value privacy and ethical AI practices"
    confidence: 0.75
  
  WHEN:
    value: "Tipping point: next 18-24 months"
    confidence: 0.55  # Uncertain timing
  
  WHY:
    value: "Provide actionable climate intelligence"  # From L6
    confidence: 0.85

assumption_type: "market_trend"
validation_status: "partially_validated"
evidence:
  supporting:
    - "Privacy regulations: GDPR, CCPA"
    - "Consumer surveys showing privacy concerns"
  contradicting:
    - "Slow adoption of privacy-focused products"
```

---

## L3 - CAPABILITIES (WHAT)

**Low Autonomy** - Can select methods

### Example 1: SaaS Product
```yaml
subject: "Our Platform"
predicate: "provides"
object: "enterprise DevSecOps automation"

dimensions:
  WHAT:
    value: "Cloud-native platform: CI/CD + security + compliance"
    confidence: 0.90
  
  WHY:
    value: "Self-service onboarding preference"  # From L4
    confidence: 0.70
  
  HOW:
    value: "Microservices architecture, API-first, multi-cloud"
    confidence: 0.85
  
  WHO:
    value: "Enterprise development teams (50-500 engineers)"
    confidence: 0.80
```

### Example 2: Consulting Service
```yaml
subject: "Our Consulting Practice"
predicate: "delivers"
object: "digital transformation strategy and execution"

dimensions:
  WHAT:
    value: "8-week engagement: assessment, roadmap, pilot implementation"
    confidence: 0.85
  
  WHY:
    value: "Organizations value speed + security + simplicity"  # From L4
    confidence: 0.80
  
  HOW:
    value: "Blended team: strategy consultants + engineers + change management"
    confidence: 0.90
  
  WHO:
    value: "Fortune 500 companies in regulated industries"
    confidence: 0.85
```

### Example 3: Technical Competency
```yaml
subject: "Our Engineering Team"
predicate: "masters"
object: "AI/ML infrastructure at scale"

dimensions:
  WHAT:
    value: "Competency: distributed ML training, model serving, MLOps"
    confidence: 0.95
  
  WHY:
    value: "Market shifting toward privacy-first ethical AI"  # From L4
    confidence: 0.75
  
  HOW:
    value: "Kubernetes + Ray + Kubeflow + custom orchestration"
    confidence: 0.90
  
  WHO:
    value: "15 ML engineers, 8 PhDs, 5+ years average experience"
    confidence: 1.0
```

---

## L2 - BEHAVIORS (HOW)

**Very Low Autonomy** - Can execute defined behaviors

### Strategic (APPROACH) - Top-down initiatives

#### Example 1: Market Entry Strategy
```yaml
subject: "Our Sales Team"
predicate: "approaches"
object: "enterprise market through channel partnerships"

dimensions:
  WHY:
    value: "Deliver enterprise DevSecOps automation"  # From L3
    confidence: 0.90
  
  WHAT:
    value: "Initiative: Partner with 3 major systems integrators for enterprise reach"
    confidence: 0.75
  
  HOW:
    value: "Strategic: Quarterly partnership reviews, joint go-to-market"
    confidence: 0.80
  
  WHEN:
    value: "Rollout: Q2-Q3 2024, full deployment by Q4"
    confidence: 0.70
```

#### Example 2: Product Development Approach
```yaml
subject: "Our Product Team"
predicate: "approaches development"
object: "through rapid experimentation and validation"

dimensions:
  WHY:
    value: "Customer preference for self-service"  # From L4
    confidence: 0.60  # Low confidence drives experimentation
  
  WHAT:
    value: "Strategy: 2-week sprint cycles, monthly user testing, quarterly pivots"
    confidence: 0.90
  
  HOW:
    value: "Build-Measure-Learn: Ship fast, measure rigorously, iterate"
    confidence: 0.95
```

### Tactical (RESPONSE) - Bottom-up feedback

#### Example 1: Market Feedback Response
```yaml
subject: "Our Product Team"
predicate: "observes"
object: "40% of enterprise trials cite onboarding complexity"

dimensions:
  WHERE:
    value: "Enterprise trial data, support tickets, churn surveys"  # From L1
    confidence: 1.0  # Direct observation
  
  WHAT:
    value: "Response: Added guided onboarding wizard, reduced config steps by 60%"
    confidence: 0.85
  
  HOW:
    value: "Tactical: Weekly metrics review, rapid prototyping, A/B testing"
    confidence: 0.90
  
  IMPACT:
    value: "Updated L4 belief: Simplicity equally important as speed and security"
    confidence: 0.95
```

#### Example 2: Performance Observation
```yaml
subject: "Our Operations Team"
predicate: "responds to"
object: "system latency spikes during peak hours"

dimensions:
  WHERE:
    value: "Production monitoring, customer complaints"  # From L1
    confidence: 1.0
  
  WHAT:
    value: "Response: Implemented auto-scaling, optimized queries, added caching"
    confidence: 0.95
  
  HOW:
    value: "Tactical: Incident response → root cause → fix → validate"
    confidence: 0.90
  
  IMPACT:
    value: "Updated L3 capability: Added performance engineering competency"
    confidence: 0.85
```

#### Example 3: Competitive Response
```yaml
subject: "Our Strategy Team"
predicate: "responds to"
object: "competitor launching AI-powered feature"

dimensions:
  WHERE:
    value: "Competitive intelligence, customer requests, sales feedback"  # From L1
    confidence: 0.90
  
  WHAT:
    value: "Response: Accelerated ML roadmap, added AI assistant to Q3 release"
    confidence: 0.75
  
  HOW:
    value: "Tactical: Emergency sprint planning, resource reallocation"
    confidence: 0.80
  
  IMPACT:
    value: "Validated L4 belief: Market ready for AI features (confidence: 0.55 → 0.80)"
    confidence: 0.85
```

---

## L1 - ENVIRONMENT (WHERE/WHEN)

**Zero Autonomy** - Cannot change context, only adapt

### Example 1: Market Context
```yaml
subject: "Our Target Market"
predicate: "consists of"
object: "enterprise B2B in North America"

dimensions:
  WHERE:
    value: "Geographic: USA, Canada | Vertical: Financial services, Healthcare, Tech"
    confidence: 0.95
  
  WHO:
    value: "Decision makers: VP Engineering, CTO, CISO"
    confidence: 0.90
  
  WHEN:
    value: "Buying cycle: 3-6 months | Budget cycles: Q4 heavy"
    confidence: 0.85
  
  WHAT:
    value: "Market size: $5B TAM, growing 30% YoY"
    confidence: 0.80
```

### Example 2: Regulatory Constraints
```yaml
subject: "Our Operating Environment"
predicate: "requires compliance with"
object: "GDPR, SOC2, HIPAA regulations"

dimensions:
  WHERE:
    value: "EU data residency, US healthcare, financial services"
    confidence: 1.0
  
  WHAT:
    value: "Constraints: Data encryption, audit trails, access controls"
    confidence: 1.0
  
  WHY:
    value: "Legal requirement, cannot be negotiated or bypassed"
    confidence: 1.0
  
  IMPACT:
    value: "Affects L3 capabilities: Must include compliance features"
    confidence: 1.0
```

### Example 3: Competitive Landscape
```yaml
subject: "Our Competitive Environment"
predicate: "includes"
object: "5 major established players plus 20+ startups"

dimensions:
  WHERE:
    value: "DevOps market: GitLab, CircleCI, Jenkins, plus cloud providers"
    confidence: 0.90
  
  WHAT:
    value: "Competitive dynamics: Price pressure, feature parity race, M&A activity"
    confidence: 0.85
  
  WHEN:
    value: "Market consolidation expected in 12-24 months"
    confidence: 0.60
  
  IMPACT:
    value: "Informs L4 beliefs about differentiation and L5 positioning"
    confidence: 0.80
```

### Example 4: Economic Constraints
```yaml
subject: "Our Economic Environment"
predicate: "faces"
object: "budget constraints and economic uncertainty"

dimensions:
  WHERE:
    value: "Global: Post-pandemic recovery, inflation, interest rates"
    confidence: 0.95
  
  WHAT:
    value: "Impact: Customers scrutinizing spend, longer sales cycles, deal shrinkage"
    confidence: 0.85
  
  WHEN:
    value: "Duration: 18-24 month period of adjustment"
    confidence: 0.70
  
  IMPACT:
    value: "Affects L4 pricing beliefs and L3 product positioning"
    confidence: 0.80
```

---

## Strategy/Tactics Flow Examples

### Example 1: SaaS Platform Evolution

**Strategic Approach (Top-down)**:
```
L6 MISSION: Accelerate innovation through accessible technology
↓
L5 IDENTITY: Be the trusted partner for digital transformation
↓
L4 BELIEF: Organizations value speed + security equally (conf: 0.85)
↓
L3 CAPABILITY: DevSecOps platform with compliance automation
↓
L2 BEHAVIOR (Strategy): Launch enterprise tier with SOC2 + HIPAA
↓
L1 ENVIRONMENT: Deploy to Fortune 500 market
```

**Tactical Response (Bottom-up)**:
```
L1 OBSERVATION: 40% of trials cite complexity, 60% adoption rate
↑
L2 BEHAVIOR (Tactics): Add onboarding wizard, reduce config 60%
↑
L3 CAPABILITY UPDATE: Add guided onboarding competency
↑
L4 BELIEF REVISION: Organizations value speed + security + SIMPLICITY (conf: 0.85 → 0.95)
↑
L5 IDENTITY REFINEMENT: Emphasize "simple yet powerful" in brand
↑
L6 MISSION VALIDATION: Confirms accessibility is key to innovation
```

### Example 2: Education Platform Pivot

**Strategic Approach**:
```
L6: Transform lives through equitable education
L5: Be the champion of accessible learning
L4: Online learning is as effective as in-person (conf: 0.65 - needs validation)
L3: Build synchronous video learning platform
L2 (Strategy): Launch live online classes with premium pricing
L1: Deploy to K-12 education market
```

**Tactical Response**:
```
L1 OBSERVATION: 70% drop-off rate, students prefer asynchronous content
L2 (Tactics): Pivot to recorded lectures + discussion boards
L3 UPDATE: Add asynchronous learning capabilities
L4 REVISION: Students need flexibility over live interaction (conf: 0.65 → 0.90 - validated)
L5 UPDATE: Rebrand as "learn at your pace" not "live learning"
L6 VALIDATION: Confirms flexibility is key to access
```

---

## Key Insights from Multiple Examples

### 1. Purpose Propagation is Universal
- **Tech company**: Accessibility → Innovation → DevSecOps
- **Education**: Equity → Access → Flexible learning
- **Environment**: Urgency → Action → Data intelligence

Same pattern, different domains.

### 2. Confidence Varies by Certainty
- **L6 Mission**: High confidence (0.90-1.0) - core purpose rarely changes
- **L5 Identity**: High confidence (0.80-0.95) - values are stable
- **L4 Beliefs**: Variable (0.55-0.95) - assumptions need validation
- **L3 Capabilities**: Moderate-high (0.75-0.95) - execution clarity
- **L2 Behaviors**: High for tactics (0.80-1.0), moderate for strategy (0.70-0.90)
- **L1 Environment**: Very high (0.85-1.0) - observable reality

### 3. Bidirectional Flow Creates Learning
**Strategy → Tactics**: We act on the world
**Tactics → Strategy**: The world teaches us

Every example shows:
- Strategy starts with high-level intent
- Environment provides feedback
- Tactics capture that feedback
- Strategy adapts based on learning

### 4. Validation Moves Beliefs
- **Needs validation**: Low confidence (< 0.70)
- **Partially validated**: Medium confidence (0.70-0.84)
- **Validated**: High confidence (0.85-0.95)
- **Proven**: Very high confidence (0.95-1.0)

Examples show beliefs moving through this lifecycle.

---

## Usage in Documentation

These examples should be used to:

1. **Illustrate universality**: Framework works for tech, education, nonprofits, enterprise
2. **Show confidence variance**: Different levels have different certainty
3. **Demonstrate flow**: Both top-down and bottom-up paths
4. **Prove adaptability**: Examples show pivots based on feedback

Replace single use-case examples with 2-3 diverse examples per concept to show generalizability.
