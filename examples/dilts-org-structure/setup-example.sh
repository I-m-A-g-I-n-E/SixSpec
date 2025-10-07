#!/bin/bash
# Example: Setting up a Dilts-based organizational structure
# This demonstrates creating a living organizational representation

set -e

ORG_NAME="${1:-AI-Research-Co}"
echo "🚀 Creating Dilts organizational structure for: $ORG_NAME"

# Create root directory
mkdir -p "$ORG_NAME"
cd "$ORG_NAME"

# Initialize git
git init
echo "✅ Initialized git repository"

# Create .sixspec configuration
mkdir -p .sixspec/templates .sixspec/validators .sixspec/schemas

cat > .sixspec/config.yaml << 'EOF'
# SixSpec Configuration for Organizational Structure
version: "1.0"
framework: "dilts-org-structure"

# Dilts levels configuration
levels:
  6:
    name: "MISSION"
    label: "FOR WHAT - Why we exist"
    autonomy: "extreme"
    required_dimensions: ["WHY", "WHAT"]
    optional_dimensions: ["WHO", "WHEN"]
    
  5:
    name: "IDENTITY"
    label: "WHO - What defines us"
    autonomy: "high"
    required_dimensions: ["WHO", "WHAT", "WHY"]
    optional_dimensions: ["HOW"]
    
  4:
    name: "BELIEFS"
    label: "WHY - Our guiding principles"
    autonomy: "moderate"
    required_dimensions: ["WHY", "WHAT"]
    confidence_tracking: true
    validation_required: true
    
  3:
    name: "CAPABILITIES"
    label: "WHAT - What we can deliver"
    autonomy: "low"
    required_dimensions: ["WHAT", "WHY", "HOW"]
    
  2:
    name: "BEHAVIORS"
    label: "HOW - How we operate"
    autonomy: "very_low"
    required_dimensions: ["HOW", "WHAT", "WHY"]
    bidirectional: true  # Both top-down and bottom-up
    
  1:
    name: "ENVIRONMENT"
    label: "WHERE/WHEN - Context we operate in"
    autonomy: "zero"
    required_dimensions: ["WHERE", "WHEN", "WHO"]

# Validation rules
validation:
  purpose_propagation: true  # Parent WHAT must equal child WHY
  confidence_thresholds:
    mission: 0.70
    identity: 0.70
    beliefs: 0.60
    capabilities: 0.75
    behaviors: 0.80
    environment: 0.90
  
  belief_validation:
    require_evidence: true
    require_validation_plan: true
    confidence_decay: 0.05  # per month without revalidation

# Git integration
git:
  dimensional_commits: true
  commit_template: ".sixspec/templates/.gitmessage"
  hooks:
    - commit-msg
    - pre-commit

# Relationships
relationships:
  track_dependencies: true
  detect_conflicts: true
  build_graphs: true
EOF

echo "✅ Created .sixspec/config.yaml"

# Create git commit message template
cat > .sixspec/templates/.gitmessage << 'EOF'
# <type>: <summary>
#
# WHY: <purpose/business value>
# HOW: <technical approach>
# WHAT: <specific change>
# WHERE: <files/components>
# WHO: <users/systems affected>
# WHEN: <conditions/triggers>
#
# Type: feat, fix, refactor, docs, belief, strategy
# 
# Links to:
# - Parent: <parent-file.w5h1>
# - Child: <child-file.w5h1>
#
# Confidence: <0.0-1.0>
# Impact: [high|medium|low]
EOF

git config commit.template .sixspec/templates/.gitmessage
echo "✅ Configured git commit template"

echo "📁 Creating Dilts directory structure..."

# Create all directories with READMEs
for level_dir in "L6-MISSION" "L5-IDENTITY" "L4-BELIEFS" "L3-CAPABILITIES" "L2-BEHAVIORS" "L1-ENVIRONMENT"; do
    mkdir -p "$level_dir"
done

# L5 subdirectories
mkdir -p L5-IDENTITY/{brand,values,positioning}

# L4 subdirectories (most complex)
mkdir -p L4-BELIEFS/{principles,assumptions,mental-models,relationships,evolution,meta}
mkdir -p L4-BELIEFS/principles/{decision-making,quality,innovation,sustainability}
mkdir -p L4-BELIEFS/assumptions/{market,product,organizational,validated,invalidated}
mkdir -p L4-BELIEFS/mental-models/{problem-solving,growth,customer-centric,collaboration}
mkdir -p L4-BELIEFS/relationships/{dependencies,conflicts,reinforcements}

# L3 subdirectories
mkdir -p L3-CAPABILITIES/{services,competencies,resources,dependencies}
mkdir -p L3-CAPABILITIES/services/{consulting,products,platforms}

# L2 subdirectories
mkdir -p L2-BEHAVIORS/{strategic,tactical,operational,communication,flows}

# L1 subdirectories
mkdir -p L1-ENVIRONMENT/{market,timing,locations,stakeholders,constraints}
mkdir -p L1-ENVIRONMENT/market/{analysis,segments}

echo "✅ Created directory structure"

# Create example W5H1 file
cat > L6-MISSION/mission-statement.w5h1 << 'EOF'
---
level: MISSION
created: 2024-01-15
status: active

subject: "Our Organization"
predicate: "exists to"
object: "democratize access to AI-powered research tools"

dimensions:
  WHY:
    value: "Knowledge work is bottlenecked by information overload"
    confidence: 1.0
    sources:
      - "Problem validation interviews (n=50)"
    
  WHAT:
    value: "Build accessible AI-powered tools for research"
    confidence: 0.95
    sources:
      - "Product strategy 2024"

parent_spec: null
child_specs:
  - "../L5-IDENTITY/brand/brand-identity.w5h1"

tags: [mission, purpose, foundational]
created_by: "Founding team"
review_cycle: "Annual"
EOF

echo "✅ Created example mission statement"

# Create initial commit
git add .
git commit -m "feat: initialize Dilts organizational structure

WHY: Create living digital representation of organization
HOW: Set up SixSpec framework with Dilts levels 1-6
WHAT: Directory structure, templates, example files
CONFIDENCE: 0.90"

echo ""
echo "✅ Setup complete for: $ORG_NAME"
echo ""
echo "📚 Structure created:"
echo "  L6-MISSION/      - Why we exist"
echo "  L5-IDENTITY/     - Who we are"
echo "  L4-BELIEFS/      - Our principles & assumptions"
echo "  L3-CAPABILITIES/ - What we deliver"
echo "  L2-BEHAVIORS/    - How we operate"
echo "  L1-ENVIRONMENT/  - Where/when we work"
echo ""
