# Dilts Organizational Structure - File Index

## Quick Navigation

### 🚀 Start Here
- **README.md** - Overview, quick start, and examples
- **[Root] DILTS_GETTING_STARTED.md** - Step-by-step guide with 3 paths

### 📚 Documentation
- **[Root] DILTS_DIRECTORY_STRUCTURE.md** - Complete specification (701 lines)
- **[Root] DILTS_IMPLEMENTATION_SUMMARY.md** - Implementation overview (512 lines)
- **[Root] DILTS_COMPLETE_PACKAGE.md** - Package overview and reference (522 lines)

### 💻 Code
- **setup-example.sh** - Automated org structure creation (211 lines)
- **org_query_example.py** - Query and analysis tool (446 lines)

## File Descriptions

### Documentation Files

#### DILTS_DIRECTORY_STRUCTURE.md
**What**: Complete specification of the framework  
**Length**: 701 lines  
**Contains**:
- Full directory structure schema
- .w5h1 file format specification
- Detailed L4-BELIEFS workshop
- Purpose propagation examples
- Use cases and scenarios
- CLI tool design
- Integration with research tools

**Read when**: You want complete understanding of the concept

#### DILTS_IMPLEMENTATION_SUMMARY.md
**What**: Implementation overview and architecture  
**Length**: 512 lines  
**Contains**:
- Executive summary
- Implementation components
- Use cases with code
- Advanced features (relationship detection, impact analysis)
- CLI tool specification
- Next steps and roadmap

**Read when**: You want to understand how to build/extend this

#### DILTS_GETTING_STARTED.md
**What**: Practical getting started guide  
**Length**: 677 lines  
**Contains**:
- 3 learning paths (explore, customize, integrate)
- File format examples
- Common use cases with bash examples
- Troubleshooting
- Step-by-step onboarding

**Read when**: You want to start using this TODAY

#### DILTS_COMPLETE_PACKAGE.md
**What**: Overview of entire package  
**Length**: 522 lines  
**Contains**:
- Package contents summary
- Quick reference guide
- Decision guide (should you use this?)
- Integration patterns
- FAQ
- Success metrics

**Read when**: You want to see the big picture

#### README.md (this directory)
**What**: Example walkthrough  
**Length**: 352 lines  
**Contains**:
- Quick start instructions
- Core concepts explained
- .w5h1 format examples
- Usage examples (Python code)
- Dilts levels explained
- Integration guide

**Read when**: You want hands-on examples

### Code Files

#### setup-example.sh
**What**: Automated organization structure creation  
**Length**: 211 lines  
**Language**: Bash  
**Does**:
- Creates full Dilts directory structure (L6-L1)
- Generates .sixspec configuration
- Sets up git integration
- Creates git commit template
- Generates example .w5h1 files
- Initializes repository

**Usage**:
```bash
bash setup-example.sh "Your-Org-Name"
```

#### org_query_example.py
**What**: Query and analysis tool  
**Length**: 446 lines  
**Language**: Python  
**Features**:
- W5H1 file parser (YAML)
- Purpose propagation validator
- Belief confidence analyzer
- Relationship graph builder
- Organizational insights generator
- Command-line interface

**Usage**:
```bash
python org_query_example.py path/to/org
```

**Output**:
- Level counts
- Purpose propagation validation
- Belief confidence summary
- Validation status
- Confidence extremes
- Orphaned specs

## Reading Paths

### Path 1: Quick Exploration (30 min)
1. Read: [README.md](./README.md) - "Quick Start" section
2. Run: `bash setup-example.sh Test-Org`
3. Explore: `tree Test-Org -L 2`
4. Read: Example .w5h1 files
5. Run: `python org_query_example.py Test-Org`

**Outcome**: Understand structure, see it working

### Path 2: Deep Understanding (2 hours)
1. Read: [DILTS_GETTING_STARTED.md](../../DILTS_GETTING_STARTED.md) - Full
2. Read: [DILTS_DIRECTORY_STRUCTURE.md](../../DILTS_DIRECTORY_STRUCTURE.md) - Core sections
3. Study: Example .w5h1 files in detail
4. Review: `org_query_example.py` code

**Outcome**: Can explain framework to others

### Path 3: Implementation (1 day)
1. Read: [DILTS_IMPLEMENTATION_SUMMARY.md](../../DILTS_IMPLEMENTATION_SUMMARY.md) - Full
2. Study: Both code files in detail
3. Create: Your own org structure
4. Customize: Mission, beliefs, capabilities
5. Query: Validate your structure

**Outcome**: Working implementation for your org

### Path 4: Integration (1 week)
1. Read: All documentation
2. Review: All code
3. Integrate: With your existing project
4. Link: Code decisions to org knowledge
5. Train: Team on usage

**Outcome**: Org knowledge as source of truth

## File Relationships

```
Root Level (SixSpec repo):
├── DILTS_DIRECTORY_STRUCTURE.md       [Spec]
├── DILTS_IMPLEMENTATION_SUMMARY.md    [Implementation]
├── DILTS_GETTING_STARTED.md           [Tutorial]
├── DILTS_COMPLETE_PACKAGE.md          [Overview]
│
└── examples/dilts-org-structure/
    ├── INDEX.md (this file)           [Navigation]
    ├── README.md                      [Examples]
    ├── setup-example.sh               [Automation]
    └── org_query_example.py           [Analysis]
```

**Flow**:
1. **Concept** → DILTS_DIRECTORY_STRUCTURE.md
2. **Tutorial** → DILTS_GETTING_STARTED.md
3. **Examples** → examples/dilts-org-structure/README.md
4. **Create** → setup-example.sh
5. **Query** → org_query_example.py
6. **Implement** → DILTS_IMPLEMENTATION_SUMMARY.md
7. **Reference** → DILTS_COMPLETE_PACKAGE.md

## Key Concepts

### Purpose Propagation
**Parent WHAT → Child WHY**

Explained in:
- DILTS_DIRECTORY_STRUCTURE.md - Section "Purpose Propagation Examples"
- DILTS_GETTING_STARTED.md - Section "Core Concept in 60 Seconds"
- README.md - Section "Purpose Propagation"

Code: `org_query_example.py` - Class `PurposePropagationValidator`

### Belief Validation
**Assumptions → Validated/Invalidated**

Explained in:
- DILTS_DIRECTORY_STRUCTURE.md - Section "Workshop: L4-BELIEFS Structure"
- DILTS_GETTING_STARTED.md - Use case "Belief Validation"
- DILTS_IMPLEMENTATION_SUMMARY.md - Section "L4-BELIEFS: The Innovation Hub"

Code: `org_query_example.py` - Class `BeliefAnalyzer`

### Confidence Tracking
**Every dimension has confidence 0.0-1.0**

Explained in:
- DILTS_DIRECTORY_STRUCTURE.md - Example .w5h1 files
- DILTS_GETTING_STARTED.md - Section "The File Format"
- README.md - Section "Confidence Tracking"

Code: `org_query_example.py` - Method `get_confidence_summary()`

### Dilts Hierarchy
**6 levels: Mission → Identity → Beliefs → Capabilities → Behaviors → Environment**

Explained in:
- All documentation files
- Interactive visualization (HTML canvas)
- README.md - Section "Dilts Levels Explained"

Code: `setup-example.sh` - Creates all 6 levels

## Statistics

### Total Package
- **Documentation**: 5 files, ~3,270 lines
- **Code**: 2 files, ~660 lines
- **Total**: ~3,930 lines
- **Completion**: 100% (production-ready)

### Documentation Breakdown
- DILTS_DIRECTORY_STRUCTURE.md: 701 lines (spec)
- DILTS_IMPLEMENTATION_SUMMARY.md: 512 lines (implementation)
- DILTS_GETTING_STARTED.md: 677 lines (tutorial)
- DILTS_COMPLETE_PACKAGE.md: 522 lines (overview)
- README.md: 352 lines (examples)
- INDEX.md: ~250 lines (this file)

### Code Breakdown
- setup-example.sh: 211 lines (automation)
- org_query_example.py: 446 lines (analysis)

## Next Steps

### Immediate (Today)
1. Run setup script
2. Explore generated structure
3. Read example .w5h1 files
4. Run query tool

### This Week
1. Read DILTS_GETTING_STARTED.md fully
2. Create structure for your org
3. Fill in mission and beliefs
4. Validate purpose propagation

### This Month
1. Complete all 6 levels
2. Link to your codebase
3. Train team on usage
4. Run first belief validation

## Support

**Issues?** Check DILTS_GETTING_STARTED.md - "Troubleshooting" section

**Questions?** Review:
- DILTS_COMPLETE_PACKAGE.md - "FAQ" section
- DILTS_GETTING_STARTED.md - "Common Use Cases"

**Want to extend?** Study:
- DILTS_IMPLEMENTATION_SUMMARY.md - "Advanced Features"
- org_query_example.py - Working code

---

**Last Updated**: 2024 (creation date)  
**Status**: Production-ready  
**License**: MIT
