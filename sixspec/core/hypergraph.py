"""
Hypergraph auto-organization system for dimensional clustering.

This module implements a hypergraph structure that automatically organizes
Chunk specifications based on shared dimensions, following the "grocery store rule":
objects sharing at least one dimension belong to the same system.

Key Concepts:
    - Hypergraph: Graph where edges connect multiple nodes (specifications)
    - Dimensional edges: Edges weighted by number of shared dimensions
    - Clustering: Connected components form natural groupings
    - Epic detection: Clusters with 2+ shared dimensions suggest epic groupings
    - Hierarchy generation: Automatic organization into epic→story→task structure

Example:
    >>> from sixspec.core.models import Chunk, Dimension
    >>> from sixspec.core.hypergraph import SpecificationHypergraph
    >>> 
    >>> graph = SpecificationHypergraph()
    >>> 
    >>> # Add grocery shopping tasks
    >>> milk = Chunk("User", "buys", "milk",
    ...            dimensions={Dimension.WHERE: "grocery", Dimension.WHEN: "today"})
    >>> bread = Chunk("User", "buys", "bread",
    ...             dimensions={Dimension.WHERE: "grocery", Dimension.WHEN: "today"})
    >>> 
    >>> graph.add_object(milk)
    >>> graph.add_object(bread)
    >>> 
    >>> # They cluster together based on shared dimensions
    >>> clusters = graph.find_clusters()
    >>> hierarchy = graph.organize_hierarchy()
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
import networkx as nx

from sixspec.core.models import Chunk, Dimension


@dataclass
class HierarchyNode:
    """
    Node in the specification hierarchy.
    
    Attributes:
        level: Hierarchy level ('epic', 'story', 'task')
        name: Human-readable name generated from shared dimensions
        shared_dimensions: Dimensions common to all children
        children: Child nodes or Chunk objects
        metadata: Additional metadata for the node
    """
    level: str
    name: str
    shared_dimensions: Dict[Dimension, str] = field(default_factory=dict)
    children: List[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_child(self, child: Any) -> None:
        """Add a child node or Chunk object."""
        self.children.append(child)
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            'level': self.level,
            'name': self.name,
            'shared_dimensions': {
                dim.value: val for dim, val in self.shared_dimensions.items()
            },
            'children': [
                child.to_dict() if hasattr(child, 'to_dict') else str(child)
                for child in self.children
            ],
            'metadata': self.metadata
        }


class SpecificationHypergraph:
    """
    Hypergraph for auto-organizing Chunk specifications based on dimensions.
    
    This class implements the core hypergraph structure that automatically
    connects specifications based on shared dimensions and organizes them
    into a hierarchy of epics, stories, and tasks.
    
    The "grocery store rule": specifications sharing at least one dimension
    belong to the same system and will be connected in the graph.
    """
    
    def __init__(self):
        """Initialize empty hypergraph."""
        self.graph = nx.Graph()
        self._object_counter = 0
        self._object_map: Dict[str, Chunk] = {}
    
    def add_object(self, obj: Chunk) -> str:
        """
        Add a Chunk object to the hypergraph and auto-connect to related objects.
        
        This method adds the object as a node and creates weighted edges to
        all other nodes based on the number of shared dimensions.
        
        Args:
            obj: Chunk object to add
            
        Returns:
            Node ID assigned to the object
            
        Example:
            >>> graph = SpecificationHypergraph()
            >>> spec = Chunk("User", "does", "task",
            ...            dimensions={Dimension.WHERE: "home"})
            >>> node_id = graph.add_object(spec)
        """
        # Generate unique node ID
        node_id = f"node_{self._object_counter}"
        self._object_counter += 1
        
        # Store object reference
        self._object_map[node_id] = obj
        
        # Add node with object as data
        self.graph.add_node(node_id, object=obj)
        
        # Connect to all existing nodes based on shared dimensions
        for existing_id in list(self.graph.nodes()):
            if existing_id == node_id:
                continue
                
            existing_obj = self._object_map[existing_id]
            shared = obj.shared_dimensions(existing_obj)
            
            # Create edge if objects share at least one dimension
            if len(shared) > 0:
                # Edge weight = number of shared dimensions
                self.graph.add_edge(node_id, existing_id, weight=len(shared), dimensions=shared)
        
        return node_id
    
    def find_clusters(self) -> List[Set[str]]:
        """
        Identify connected components (clusters) in the hypergraph.
        
        Each connected component represents a group of specifications that
        share at least one dimension transitively.
        
        Returns:
            List of sets, each containing node IDs in a cluster
            
        Example:
            >>> graph = SpecificationHypergraph()
            >>> # Add connected specs
            >>> graph.add_object(milk)
            >>> graph.add_object(bread)
            >>> # Add disconnected spec
            >>> graph.add_object(hammer)
            >>> clusters = graph.find_clusters()
            >>> len(clusters)
            2
        """
        return [set(component) for component in nx.connected_components(self.graph)]
    
    def should_be_epic(self, cluster1: Set[str], cluster2: Set[str]) -> bool:
        """
        Determine if two clusters should be grouped under the same epic.
        
        Clusters belong to the same epic if their members share 2+ dimensions
        on average across cluster boundaries.
        
        Args:
            cluster1: First cluster of node IDs
            cluster2: Second cluster of node IDs
            
        Returns:
            True if clusters should be in same epic, False otherwise
            
        Example:
            >>> # Two grocery trips on different days
            >>> monday_cluster = {"node_0", "node_1"}  # WHERE: grocery, WHEN: monday
            >>> tuesday_cluster = {"node_2", "node_3"}  # WHERE: grocery, WHEN: tuesday
            >>> graph.should_be_epic(monday_cluster, tuesday_cluster)
            True  # Share WHERE dimension strongly
        """
        if not cluster1 or not cluster2:
            return False
        
        # Find dimensions shared between clusters
        shared_dimensions = self._cross_cluster_dimensions(cluster1, cluster2)
        
        # Epic threshold: 2+ shared dimensions on average
        return len(shared_dimensions) >= 2
    
    def _cross_cluster_dimensions(self, cluster1: Set[str], cluster2: Set[str]) -> Set[Dimension]:
        """
        Find dimensions commonly shared between two clusters.
        
        Args:
            cluster1: First cluster of node IDs
            cluster2: Second cluster of node IDs
            
        Returns:
            Set of dimensions that appear frequently across clusters
        """
        dimension_counts = defaultdict(int)
        total_pairs = 0
        
        for node1 in cluster1:
            obj1 = self._object_map[node1]
            for node2 in cluster2:
                obj2 = self._object_map[node2]
                shared = obj1.shared_dimensions(obj2)
                for dim in shared:
                    dimension_counts[dim] += 1
                total_pairs += 1
        
        if total_pairs == 0:
            return set()
        
        # Return dimensions that appear in >50% of cross-cluster pairs
        threshold = total_pairs * 0.5
        return {dim for dim, count in dimension_counts.items() if count >= threshold}
    
    def _cluster_dimensions(self, cluster: Set[str]) -> Dict[Dimension, str]:
        """
        Find dimensions and values common to all objects in a cluster.
        
        Args:
            cluster: Set of node IDs in the cluster
            
        Returns:
            Dictionary of dimensions and values shared by all objects
            
        Example:
            >>> cluster = {"node_0", "node_1"}  # Both have WHERE: "grocery"
            >>> graph._cluster_dimensions(cluster)
            {<Dimension.WHERE: 'where'>: 'grocery'}
        """
        if not cluster:
            return {}
        
        # Get first object's dimensions as starting point
        first_node = next(iter(cluster))
        first_obj = self._object_map[first_node]
        common_dims = dict(first_obj.dimensions)
        
        # Keep only dimensions that match across all objects
        for node_id in cluster:
            if node_id == first_node:
                continue
            
            obj = self._object_map[node_id]
            dims_to_remove = []
            
            for dim, value in common_dims.items():
                if not obj.has(dim) or obj.need(dim) != value:
                    dims_to_remove.append(dim)
            
            for dim in dims_to_remove:
                del common_dims[dim]
        
        return common_dims
    
    def organize_hierarchy(self) -> HierarchyNode:
        """
        Generate full epic→story→task hierarchy from the hypergraph.
        
        This method analyzes the graph structure and shared dimensions to
        create a three-level hierarchy:
        - Epic: Groups of clusters with 2+ shared dimensions
        - Story: Individual clusters sharing dimensions
        - Task: Individual Chunk objects
        
        Returns:
            Root HierarchyNode containing the full hierarchy
            
        Example:
            >>> graph = SpecificationHypergraph()
            >>> # Add various tasks
            >>> graph.add_object(grocery1)
            >>> graph.add_object(grocery2)
            >>> graph.add_object(hardware)
            >>> 
            >>> hierarchy = graph.organize_hierarchy()
            >>> print(hierarchy.name)
            "Root"
            >>> print(hierarchy.children[0].name)
            "Today's Errands"
        """
        root = HierarchyNode(level="root", name="Root")
        
        # Find all clusters
        clusters = self.find_clusters()
        
        if not clusters:
            return root
        
        # Group clusters into epics
        epic_groups = self._group_into_epics(clusters)
        
        for epic_clusters in epic_groups:
            # Find dimensions common across epic
            epic_dims = self._find_epic_dimensions(epic_clusters)
            epic_name = self._generate_name_from_dimensions(epic_dims, "Epic")
            
            epic = HierarchyNode(
                level="epic",
                name=epic_name,
                shared_dimensions=epic_dims
            )
            
            # Create stories from clusters
            for cluster in epic_clusters:
                story_dims = self._cluster_dimensions(cluster)
                story_name = self._generate_name_from_dimensions(story_dims, "Story")
                
                story = HierarchyNode(
                    level="story",
                    name=story_name,
                    shared_dimensions=story_dims
                )
                
                # Add tasks (individual objects)
                for node_id in cluster:
                    obj = self._object_map[node_id]
                    task_name = f"{obj.predicate} {obj.object}"
                    
                    task = HierarchyNode(
                        level="task",
                        name=task_name.capitalize(),
                        shared_dimensions=obj.dimensions.copy(),
                        metadata={'node_id': node_id, 'triple': (obj.subject, obj.predicate, obj.object)}
                    )
                    task.add_child(obj)
                    story.add_child(task)
                
                epic.add_child(story)
            
            root.add_child(epic)
        
        return root
    
    def _group_into_epics(self, clusters: List[Set[str]]) -> List[List[Set[str]]]:
        """
        Group clusters into epics based on dimensional overlap.
        
        Args:
            clusters: List of clusters to group
            
        Returns:
            List of epic groups, each containing related clusters
        """
        if not clusters:
            return []
        
        # Build graph of cluster relationships
        cluster_graph = nx.Graph()
        for i, cluster in enumerate(clusters):
            cluster_graph.add_node(i, cluster=cluster)
        
        # Connect clusters that should be in same epic
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                if self.should_be_epic(clusters[i], clusters[j]):
                    cluster_graph.add_edge(i, j)
        
        # Find connected components in cluster graph
        epic_groups = []
        for component in nx.connected_components(cluster_graph):
            epic_clusters = [clusters[i] for i in component]
            epic_groups.append(epic_clusters)
        
        return epic_groups
    
    def _find_epic_dimensions(self, clusters: List[Set[str]]) -> Dict[Dimension, str]:
        """
        Find dimensions common across all clusters in an epic.
        
        Args:
            clusters: List of clusters in the epic
            
        Returns:
            Dictionary of shared dimensions and values
        """
        if not clusters:
            return {}
        
        # Start with dimensions from first cluster
        epic_dims = self._cluster_dimensions(clusters[0])
        
        # Keep only dimensions shared by all clusters
        for cluster in clusters[1:]:
            cluster_dims = self._cluster_dimensions(cluster)
            dims_to_remove = []
            
            for dim, value in epic_dims.items():
                if dim not in cluster_dims or cluster_dims[dim] != value:
                    dims_to_remove.append(dim)
            
            for dim in dims_to_remove:
                del epic_dims[dim]
        
        return epic_dims
    
    def _generate_name_from_dimensions(self, dimensions: Dict[Dimension, str], 
                                      prefix: str = "") -> str:
        """
        Generate a human-readable name from shared dimensions.
        
        Args:
            dimensions: Dictionary of dimensions and values
            prefix: Optional prefix for the name
            
        Returns:
            Generated name string
            
        Example:
            >>> dims = {Dimension.WHERE: "grocery", Dimension.WHEN: "today"}
            >>> graph._generate_name_from_dimensions(dims, "Epic")
            "Epic: Today at Grocery"
        """
        if not dimensions:
            return f"{prefix}: Unnamed" if prefix else "Unnamed"
        
        # Priority order for name generation
        priority = [Dimension.WHEN, Dimension.WHERE, Dimension.WHO, 
                   Dimension.WHAT, Dimension.HOW, Dimension.WHY]
        
        name_parts = []
        for dim in priority:
            if dim in dimensions:
                value = dimensions[dim]
                if dim == Dimension.WHEN:
                    name_parts.append(value.capitalize())
                elif dim == Dimension.WHERE:
                    name_parts.append(f"at {value.capitalize()}")
                elif dim == Dimension.WHO:
                    name_parts.append(f"for {value}")
                elif dim == Dimension.WHAT:
                    name_parts.append(f"- {value}")
                elif dim == Dimension.HOW:
                    name_parts.append(f"via {value}")
                elif dim == Dimension.WHY:
                    name_parts.append(f"to {value}")
        
        name = " ".join(name_parts) if name_parts else "Unnamed"
        return f"{prefix}: {name}" if prefix else name
    
    def get_node_info(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific node.
        
        Args:
            node_id: Node identifier
            
        Returns:
            Dictionary with node information or None if not found
        """
        if node_id not in self._object_map:
            return None
        
        obj = self._object_map[node_id]
        neighbors = list(self.graph.neighbors(node_id))
        edges = []
        
        for neighbor in neighbors:
            edge_data = self.graph.edges[node_id, neighbor]
            edges.append({
                'neighbor': neighbor,
                'weight': edge_data['weight'],
                'shared_dimensions': [d.value for d in edge_data['dimensions']]
            })
        
        return {
            'node_id': node_id,
            'object': obj.to_dict(),
            'neighbors': neighbors,
            'edges': edges
        }
    
    def to_dict(self) -> dict:
        """
        Export hypergraph to dictionary representation.
        
        Returns:
            Dictionary containing graph structure and objects
        """
        nodes = []
        for node_id in self.graph.nodes():
            nodes.append(self.get_node_info(node_id))
        
        return {
            'nodes': nodes,
            'num_nodes': self.graph.number_of_nodes(),
            'num_edges': self.graph.number_of_edges(),
            'clusters': [list(cluster) for cluster in self.find_clusters()]
        }