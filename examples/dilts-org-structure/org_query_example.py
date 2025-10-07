"""
Example: Querying and analyzing Dilts organizational structure

This demonstrates how to:
1. Load W5H1 organizational files
2. Validate purpose propagation (parent WHAT → child WHY)
3. Track belief confidence over time
4. Detect relationship conflicts
5. Generate organizational insights
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class DiltsLevel(Enum):
    """Dilts Logical Levels"""
    MISSION = 6
    IDENTITY = 5
    BELIEFS = 4
    CAPABILITY = 3
    BEHAVIOR = 2
    ENVIRONMENT = 1


@dataclass
class Dimension:
    """A single dimension value with confidence and sources"""
    value: str
    confidence: float
    sources: List[str]
    notes: Optional[str] = None


@dataclass
class W5H1Org:
    """Organizational W5H1 specification"""
    level: DiltsLevel
    created: str
    status: str
    subject: str
    predicate: str
    object: str
    dimensions: Dict[str, Dimension]
    parent_spec: Optional[str]
    child_specs: List[str]
    tags: List[str]
    file_path: Path
    
    @property
    def why(self) -> Optional[Dimension]:
        return self.dimensions.get('WHY')
    
    @property
    def what(self) -> Optional[Dimension]:
        return self.dimensions.get('WHAT')
    
    @property
    def who(self) -> Optional[Dimension]:
        return self.dimensions.get('WHO')
    
    @property
    def how(self) -> Optional[Dimension]:
        return self.dimensions.get('HOW')
    
    @property
    def where(self) -> Optional[Dimension]:
        return self.dimensions.get('WHERE')
    
    @property
    def when(self) -> Optional[Dimension]:
        return self.dimensions.get('WHEN')


class OrgLoader:
    """Load and parse W5H1 organizational files"""
    
    def __init__(self, org_root: Path):
        self.org_root = Path(org_root)
        self.specs: Dict[str, W5H1Org] = {}
    
    def load_all(self) -> Dict[str, W5H1Org]:
        """Load all .w5h1 files in the organization"""
        for w5h1_file in self.org_root.rglob("*.w5h1"):
            spec = self.load_file(w5h1_file)
            if spec:
                # Use relative path as key
                rel_path = w5h1_file.relative_to(self.org_root)
                self.specs[str(rel_path)] = spec
        
        return self.specs
    
    def load_file(self, file_path: Path) -> Optional[W5H1Org]:
        """Load a single W5H1 file"""
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            
            # Parse dimensions
            dimensions = {}
            for dim_name, dim_data in data.get('dimensions', {}).items():
                if isinstance(dim_data, dict):
                    dimensions[dim_name] = Dimension(
                        value=dim_data.get('value', ''),
                        confidence=dim_data.get('confidence', 0.0),
                        sources=dim_data.get('sources', []),
                        notes=dim_data.get('notes')
                    )
            
            # Determine Dilts level
            level_str = data.get('level', '').upper()
            level = DiltsLevel[level_str] if level_str in DiltsLevel.__members__ else None
            
            if not level:
                print(f"Warning: {file_path} has invalid level: {level_str}")
                return None
            
            return W5H1Org(
                level=level,
                created=data.get('created', ''),
                status=data.get('status', 'unknown'),
                subject=data.get('subject', ''),
                predicate=data.get('predicate', ''),
                object=data.get('object', ''),
                dimensions=dimensions,
                parent_spec=data.get('parent_spec'),
                child_specs=data.get('child_specs', []),
                tags=data.get('tags', []),
                file_path=file_path
            )
        
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None


class PurposePropagationValidator:
    """Validate that parent WHAT becomes child WHY"""
    
    def __init__(self, specs: Dict[str, W5H1Org]):
        self.specs = specs
    
    def validate_all(self) -> List[str]:
        """Validate all parent-child relationships"""
        issues = []
        
        for path, spec in self.specs.items():
            if spec.parent_spec and spec.why:
                parent_path = self._resolve_parent_path(path, spec.parent_spec)
                parent = self.specs.get(parent_path)
                
                if not parent:
                    issues.append(
                        f"{path}: Parent not found: {spec.parent_spec}"
                    )
                elif not parent.what:
                    issues.append(
                        f"{path}: Parent has no WHAT dimension"
                    )
                elif not self._is_similar(parent.what.value, spec.why.value):
                    issues.append(
                        f"{path}: WHY does not match parent WHAT\n"
                        f"  Parent WHAT: {parent.what.value}\n"
                        f"  Child WHY: {spec.why.value}"
                    )
        
        return issues
    
    def _resolve_parent_path(self, child_path: str, parent_ref: str) -> str:
        """Resolve relative parent path"""
        child_dir = Path(child_path).parent
        parent_path = (child_dir / parent_ref).resolve()
        
        # Make relative to org root
        try:
            rel = parent_path.relative_to(self.specs[child_path].file_path.parent.parent)
            return str(rel)
        except:
            return parent_ref.lstrip('../')
    
    def _is_similar(self, text1: str, text2: str) -> bool:
        """Check if two texts are similar (simple version)"""
        # In production, use more sophisticated similarity
        t1 = text1.lower().strip()
        t2 = text2.lower().strip()
        return t1 in t2 or t2 in t1 or t1 == t2


class BeliefAnalyzer:
    """Analyze beliefs: confidence, validation status, evidence"""
    
    def __init__(self, specs: Dict[str, W5H1Org]):
        self.specs = specs
        self.beliefs = {
            path: spec for path, spec in specs.items()
            if spec.level == DiltsLevel.BELIEFS
        }
    
    def get_confidence_summary(self) -> Dict[str, any]:
        """Get confidence statistics for all beliefs"""
        confidences = []
        
        for spec in self.beliefs.values():
            for dim in spec.dimensions.values():
                confidences.append(dim.confidence)
        
        if not confidences:
            return {}
        
        return {
            'mean': sum(confidences) / len(confidences),
            'min': min(confidences),
            'max': max(confidences),
            'count': len(confidences),
            'below_threshold': sum(1 for c in confidences if c < 0.70)
        }
    
    def get_validation_needed(self, threshold: float = 0.70) -> List[tuple]:
        """Get beliefs that need validation (below threshold)"""
        need_validation = []
        
        for path, spec in self.beliefs.items():
            if 'validation' in spec.tags or 'validation_needed' in spec.tags:
                # Calculate overall confidence
                if spec.dimensions:
                    avg_conf = sum(d.confidence for d in spec.dimensions.values()) / len(spec.dimensions)
                    if avg_conf < threshold:
                        need_validation.append((path, avg_conf, spec))
        
        return sorted(need_validation, key=lambda x: x[1])
    
    def get_validated_vs_assumed(self) -> Dict[str, int]:
        """Count validated vs. assumed beliefs"""
        counts = {
            'validated': 0,
            'invalidated': 0,
            'needs_validation': 0,
            'total': len(self.beliefs)
        }
        
        for path, spec in self.beliefs.items():
            if 'validated' in path or spec.status == 'validated':
                counts['validated'] += 1
            elif 'invalidated' in path or spec.status == 'invalidated':
                counts['invalidated'] += 1
            elif 'validation' in spec.tags or spec.status == 'validation_needed':
                counts['needs_validation'] += 1
        
        return counts


class OrgInsights:
    """Generate organizational insights"""
    
    def __init__(self, specs: Dict[str, W5H1Org]):
        self.specs = specs
    
    def get_level_counts(self) -> Dict[str, int]:
        """Count specs by Dilts level"""
        counts = {level.name: 0 for level in DiltsLevel}
        
        for spec in self.specs.values():
            counts[spec.level.name] += 1
        
        return counts
    
    def get_provenance_chain(self, spec_path: str) -> List[str]:
        """Get full provenance chain from mission to spec"""
        chain = []
        current_path = spec_path
        visited = set()
        
        while current_path and current_path not in visited:
            spec = self.specs.get(current_path)
            if not spec:
                break
            
            visited.add(current_path)
            
            if spec.what:
                chain.append(f"L{spec.level.value} WHAT: {spec.what.value}")
            
            if not spec.parent_spec:
                break
            
            # Resolve parent
            parent_dir = Path(current_path).parent
            parent_path = (parent_dir / spec.parent_spec).resolve()
            
            # Find matching spec
            for path, candidate in self.specs.items():
                if candidate.file_path.resolve() == parent_path:
                    current_path = path
                    break
            else:
                break
        
        return list(reversed(chain))
    
    def find_orphans(self) -> List[str]:
        """Find specs with missing parents"""
        orphans = []
        
        for path, spec in self.specs.items():
            if spec.parent_spec and spec.level != DiltsLevel.MISSION:
                # Try to resolve parent
                parent_dir = Path(path).parent
                parent_path = (parent_dir / spec.parent_spec)
                
                found = False
                for candidate_path in self.specs.keys():
                    if spec.parent_spec in candidate_path:
                        found = True
                        break
                
                if not found:
                    orphans.append(path)
        
        return orphans
    
    def get_most_confident(self, n: int = 5) -> List[tuple]:
        """Get specs with highest average confidence"""
        scored = []
        
        for path, spec in self.specs.items():
            if spec.dimensions:
                avg = sum(d.confidence for d in spec.dimensions.values()) / len(spec.dimensions)
                scored.append((path, avg, spec))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:n]
    
    def get_least_confident(self, n: int = 5) -> List[tuple]:
        """Get specs with lowest average confidence"""
        scored = []
        
        for path, spec in self.specs.items():
            if spec.dimensions:
                avg = sum(d.confidence for d in spec.dimensions.values()) / len(spec.dimensions)
                scored.append((path, avg, spec))
        
        scored.sort(key=lambda x: x[1])
        return scored[:n]


def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python org_query_example.py <org-directory>")
        sys.exit(1)
    
    org_root = Path(sys.argv[1])
    
    if not org_root.exists():
        print(f"Error: {org_root} does not exist")
        sys.exit(1)
    
    print("🔍 Loading organizational structure...")
    loader = OrgLoader(org_root)
    specs = loader.load_all()
    print(f"✅ Loaded {len(specs)} specifications")
    print()
    
    # Level counts
    print("📊 Specifications by Level:")
    insights = OrgInsights(specs)
    for level, count in insights.get_level_counts().items():
        print(f"  L{DiltsLevel[level].value} {level:12s}: {count}")
    print()
    
    # Validate purpose propagation
    print("🔗 Validating Purpose Propagation (Parent WHAT → Child WHY):")
    validator = PurposePropagationValidator(specs)
    issues = validator.validate_all()
    if issues:
        print(f"  ⚠️  Found {len(issues)} issues:")
        for issue in issues[:5]:  # Show first 5
            print(f"    - {issue}")
    else:
        print("  ✅ All parent-child relationships valid")
    print()
    
    # Belief analysis
    print("💡 Belief Analysis:")
    belief_analyzer = BeliefAnalyzer(specs)
    
    conf_summary = belief_analyzer.get_confidence_summary()
    if conf_summary:
        print(f"  Average confidence: {conf_summary['mean']:.2f}")
        print(f"  Range: {conf_summary['min']:.2f} - {conf_summary['max']:.2f}")
        print(f"  Below threshold (0.70): {conf_summary['below_threshold']}")
    
    val_counts = belief_analyzer.get_validated_vs_assumed()
    print(f"  Validated: {val_counts['validated']}")
    print(f"  Invalidated: {val_counts['invalidated']}")
    print(f"  Needs validation: {val_counts['needs_validation']}")
    print(f"  Total beliefs: {val_counts['total']}")
    print()
    
    # Beliefs needing validation
    needs_val = belief_analyzer.get_validation_needed()
    if needs_val:
        print(f"⚠️  Top beliefs needing validation:")
        for path, conf, spec in needs_val[:3]:
            print(f"  {conf:.2f} - {path}")
            if spec.what:
                print(f"       WHAT: {spec.what.value[:60]}...")
    print()
    
    # Confidence extremes
    print("🎯 Most Confident Specs:")
    for path, conf, spec in insights.get_most_confident(3):
        print(f"  {conf:.2f} - {path}")
    print()
    
    print("🤔 Least Confident Specs:")
    for path, conf, spec in insights.get_least_confident(3):
        print(f"  {conf:.2f} - {path}")
    print()
    
    # Orphans
    orphans = insights.find_orphans()
    if orphans:
        print(f"👻 Orphaned Specs (missing parents): {len(orphans)}")
        for orphan in orphans[:3]:
            print(f"  - {orphan}")
    print()
    
    # Provenance example
    if specs:
        example_path = list(specs.keys())[0]
        print(f"🔍 Provenance Chain Example ({example_path}):")
        chain = insights.get_provenance_chain(example_path)
        for i, item in enumerate(chain, 1):
            print(f"  {i}. {item}")


if __name__ == "__main__":
    main()
