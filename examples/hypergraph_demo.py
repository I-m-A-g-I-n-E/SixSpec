#!/usr/bin/env python3
"""
Demonstration of the SpecificationHypergraph auto-organization system.

This script shows how the hypergraph automatically organizes specifications
based on shared dimensions, implementing the "grocery store rule" example
from the specification.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sixspec.core.models import Chunk, Dimension
from sixspec.core.hypergraph import SpecificationHypergraph
import json


def demo_grocery_store_example():
    """Demonstrate the classic grocery store vs hardware store example."""
    print("=" * 60)
    print("HYPERGRAPH AUTO-ORGANIZATION DEMO")
    print("=" * 60)
    print()
    
    # Create hypergraph
    graph = SpecificationHypergraph()
    
    # Create specifications for today's errands
    print("Adding specifications for today's errands...")
    print()
    
    # Grocery shopping tasks
    grocery1 = Chunk(
        subject="User",
        predicate="buys",
        object="milk",
        dimensions={
            Dimension.WHERE: "grocery",
            Dimension.WHEN: "today"
        }
    )
    
    grocery2 = Chunk(
        subject="User",
        predicate="buys",
        object="bread",
        dimensions={
            Dimension.WHERE: "grocery",
            Dimension.WHEN: "today"
        }
    )
    
    # Hardware store task
    hardware = Chunk(
        subject="User",
        predicate="buys",
        object="hammer",
        dimensions={
            Dimension.WHERE: "hardware",
            Dimension.WHEN: "today"
        }
    )
    
    # Add objects to graph
    g1 = graph.add_object(grocery1)
    print(f"Added: {grocery1.predicate} {grocery1.object} (node: {g1})")
    print(f"  Dimensions: WHERE={grocery1.need(Dimension.WHERE)}, WHEN={grocery1.need(Dimension.WHEN)}")
    
    g2 = graph.add_object(grocery2)
    print(f"Added: {grocery2.predicate} {grocery2.object} (node: {g2})")
    print(f"  Dimensions: WHERE={grocery2.need(Dimension.WHERE)}, WHEN={grocery2.need(Dimension.WHEN)}")
    
    h = graph.add_object(hardware)
    print(f"Added: {hardware.predicate} {hardware.object} (node: {h})")
    print(f"  Dimensions: WHERE={hardware.need(Dimension.WHERE)}, WHEN={hardware.need(Dimension.WHEN)}")
    print()
    
    # Show connections
    print("Auto-generated connections:")
    print("-" * 40)
    for node1, node2, data in graph.graph.edges(data=True):
        obj1 = graph._object_map[node1]
        obj2 = graph._object_map[node2]
        shared_dims = [d.value for d in data['dimensions']]
        print(f"  {obj1.object} <-> {obj2.object}: weight={data['weight']} (shared: {', '.join(shared_dims)})")
    print()
    
    # Show clusters
    clusters = graph.find_clusters()
    print(f"Clusters found: {len(clusters)}")
    for i, cluster in enumerate(clusters):
        print(f"  Cluster {i+1}: {len(cluster)} objects")
        for node_id in cluster:
            obj = graph._object_map[node_id]
            print(f"    - {obj.predicate} {obj.object}")
    print()
    
    # Generate hierarchy
    print("Generated Hierarchy:")
    print("-" * 40)
    hierarchy = graph.organize_hierarchy()
    print_hierarchy(hierarchy, indent=0)
    print()
    
    return graph, hierarchy


def demo_complex_organization():
    """Demonstrate complex multi-epic organization."""
    print("=" * 60)
    print("COMPLEX MULTI-EPIC ORGANIZATION")
    print("=" * 60)
    print()
    
    graph = SpecificationHypergraph()
    
    # Monday grocery shopping
    monday_grocery1 = Chunk(
        subject="User",
        predicate="buys",
        object="milk",
        dimensions={
            Dimension.WHERE: "grocery",
            Dimension.WHEN: "monday",
            Dimension.WHO: "John"
        }
    )
    
    monday_grocery2 = Chunk(
        subject="User",
        predicate="buys",
        object="bread",
        dimensions={
            Dimension.WHERE: "grocery",
            Dimension.WHEN: "monday",
            Dimension.WHO: "John"
        }
    )
    
    # Tuesday grocery shopping (same person)
    tuesday_grocery = Chunk(
        subject="User",
        predicate="buys",
        object="eggs",
        dimensions={
            Dimension.WHERE: "grocery",
            Dimension.WHEN: "tuesday",
            Dimension.WHO: "John"
        }
    )
    
    # Different activity entirely
    coding_task = Chunk(
        subject="Developer",
        predicate="implements",
        object="feature",
        dimensions={
            Dimension.WHAT: "authentication",
            Dimension.HOW: "OAuth2",
            Dimension.WHY: "security"
        }
    )
    
    # Add all objects
    print("Adding specifications...")
    for obj in [monday_grocery1, monday_grocery2, tuesday_grocery, coding_task]:
        node_id = graph.add_object(obj)
        print(f"  Added: {obj.predicate} {obj.object}")
    print()
    
    # Show clusters
    clusters = graph.find_clusters()
    print(f"Clusters found: {len(clusters)}")
    for i, cluster in enumerate(clusters):
        print(f"  Cluster {i+1}:")
        common = graph._cluster_dimensions(cluster)
        if common:
            print(f"    Common dimensions: {', '.join(f'{d.value}={v}' for d, v in common.items())}")
        for node_id in cluster:
            obj = graph._object_map[node_id]
            print(f"    - {obj.predicate} {obj.object}")
    print()
    
    # Check epic grouping
    if len(clusters) >= 2:
        print("Epic grouping analysis:")
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                should_group = graph.should_be_epic(clusters[i], clusters[j])
                print(f"  Cluster {i+1} + Cluster {j+1}: {'Same epic' if should_group else 'Different epics'}")
    print()
    
    # Generate and show hierarchy
    hierarchy = graph.organize_hierarchy()
    print("Generated Hierarchy:")
    print("-" * 40)
    print_hierarchy(hierarchy, indent=0)
    print()
    
    return graph, hierarchy


def print_hierarchy(node, indent=0):
    """Pretty print a hierarchy node."""
    prefix = "  " * indent
    if node.level == "root":
        print(f"{prefix}{node.name}")
    elif node.level == "epic":
        print(f"{prefix}📚 {node.name}")
        if node.shared_dimensions:
            dims = ", ".join(f"{d.value}={v}" for d, v in node.shared_dimensions.items())
            print(f"{prefix}   (Shared: {dims})")
    elif node.level == "story":
        print(f"{prefix}📖 {node.name}")
        if node.shared_dimensions:
            dims = ", ".join(f"{d.value}={v}" for d, v in node.shared_dimensions.items())
            print(f"{prefix}   (Shared: {dims})")
    elif node.level == "task":
        print(f"{prefix}✓ {node.name}")
        if 'triple' in node.metadata:
            s, p, o = node.metadata['triple']
            print(f"{prefix}   ({s} {p} {o})")
    
    # Recurse for children
    for child in node.children:
        if hasattr(child, 'level'):  # It's a HierarchyNode
            print_hierarchy(child, indent + 1)


def export_hierarchy_json(hierarchy, filename="hierarchy.json"):
    """Export hierarchy to JSON file."""
    with open(filename, 'w') as f:
        json.dump(hierarchy.to_dict(), f, indent=2)
    print(f"Hierarchy exported to {filename}")


if __name__ == "__main__":
    print("SixSpec Hypergraph Auto-Organization System")
    print("=" * 60)
    print()
    
    # Run demos
    print("1. GROCERY STORE EXAMPLE")
    print("-" * 40)
    graph1, hierarchy1 = demo_grocery_store_example()
    
    print("\n")
    print("2. COMPLEX ORGANIZATION EXAMPLE")
    print("-" * 40)
    graph2, hierarchy2 = demo_complex_organization()
    
    print("\n")
    print("=" * 60)
    print("DEMO COMPLETE")
    print()
    print("The hypergraph has successfully:")
    print("✓ Auto-connected objects based on shared dimensions")
    print("✓ Detected clusters via connected components")
    print("✓ Identified epic groupings (2+ shared dimensions)")
    print("✓ Generated hierarchical organization (epic→story→task)")
    print()
    print("This implements the 'grocery store rule':")
    print("  Objects sharing ≥1 dimension belong to the same system")
    print("=" * 60)