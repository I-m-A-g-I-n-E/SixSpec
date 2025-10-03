"""
Unit tests for the SpecificationHypergraph class.

Tests the auto-organization capabilities including:
- Object connection based on shared dimensions
- Cluster detection via connected components
- Epic grouping for 2+ dimension overlap
- Hierarchy generation (epic→story→task)
- The "grocery store rule" example
"""

import pytest
from sixspec.core.models import Chunk, Dimension
from sixspec.core.hypergraph import SpecificationHypergraph, HierarchyNode


class TestSpecificationHypergraph:
    """Test suite for SpecificationHypergraph."""
    
    def test_empty_graph(self):
        """Test empty hypergraph initialization."""
        graph = SpecificationHypergraph()
        assert graph.graph.number_of_nodes() == 0
        assert graph.graph.number_of_edges() == 0
        assert graph.find_clusters() == []
    
    def test_add_single_object(self):
        """Test adding a single object to the graph."""
        graph = SpecificationHypergraph()
        obj = Chunk("User", "does", "task",
                   dimensions={Dimension.WHERE: "home"})
        
        node_id = graph.add_object(obj)
        
        assert node_id == "node_0"
        assert graph.graph.number_of_nodes() == 1
        assert graph.graph.number_of_edges() == 0
        assert len(graph.find_clusters()) == 1
    
    def test_auto_connect_shared_dimension(self):
        """Test that objects sharing dimensions auto-connect."""
        graph = SpecificationHypergraph()
        
        obj1 = Chunk("User", "buys", "milk",
                    dimensions={Dimension.WHERE: "grocery"})
        obj2 = Chunk("User", "buys", "bread",
                    dimensions={Dimension.WHERE: "grocery"})
        
        node1 = graph.add_object(obj1)
        node2 = graph.add_object(obj2)
        
        # Should be connected with weight 1 (one shared dimension)
        assert graph.graph.has_edge(node1, node2)
        edge_data = graph.graph.edges[node1, node2]
        assert edge_data['weight'] == 1
        assert Dimension.WHERE in edge_data['dimensions']
        
        # Should be in same cluster
        clusters = graph.find_clusters()
        assert len(clusters) == 1
        assert {node1, node2} == clusters[0]
    
    def test_no_connection_without_shared_dimensions(self):
        """Test that objects with no shared dimensions don't connect."""
        graph = SpecificationHypergraph()
        
        obj1 = Chunk("User", "buys", "milk",
                    dimensions={Dimension.WHERE: "grocery"})
        obj2 = Chunk("User", "buys", "hammer",
                    dimensions={Dimension.WHAT: "tool"})
        
        node1 = graph.add_object(obj1)
        node2 = graph.add_object(obj2)
        
        # Should NOT be connected
        assert not graph.graph.has_edge(node1, node2)
        
        # Should be in different clusters
        clusters = graph.find_clusters()
        assert len(clusters) == 2
    
    def test_multiple_shared_dimensions(self):
        """Test edge weight increases with more shared dimensions."""
        graph = SpecificationHypergraph()
        
        obj1 = Chunk("User", "buys", "milk",
                    dimensions={
                        Dimension.WHERE: "grocery",
                        Dimension.WHEN: "today",
                        Dimension.WHO: "John"
                    })
        obj2 = Chunk("User", "buys", "bread",
                    dimensions={
                        Dimension.WHERE: "grocery",
                        Dimension.WHEN: "today",
                        Dimension.WHO: "John"
                    })
        
        node1 = graph.add_object(obj1)
        node2 = graph.add_object(obj2)
        
        # Should be connected with weight 3 (three shared dimensions)
        edge_data = graph.graph.edges[node1, node2]
        assert edge_data['weight'] == 3
        assert len(edge_data['dimensions']) == 3
    
    def test_grocery_store_example(self):
        """Test the classic grocery store vs hardware store example."""
        graph = SpecificationHypergraph()
        
        # Grocery shopping tasks
        grocery1 = Chunk("User", "buys", "milk",
                       dimensions={
                           Dimension.WHERE: "grocery",
                           Dimension.WHEN: "today"
                       })
        grocery2 = Chunk("User", "buys", "bread",
                       dimensions={
                           Dimension.WHERE: "grocery",
                           Dimension.WHEN: "today"
                       })
        
        # Hardware store task
        hardware = Chunk("User", "buys", "hammer",
                       dimensions={
                           Dimension.WHERE: "hardware",
                           Dimension.WHEN: "today"
                       })
        
        g1 = graph.add_object(grocery1)
        g2 = graph.add_object(grocery2)
        h = graph.add_object(hardware)
        
        # Grocery items should be connected to each other
        assert graph.graph.has_edge(g1, g2)
        
        # Hardware should connect to groceries (share WHEN)
        assert graph.graph.has_edge(g1, h)
        assert graph.graph.has_edge(g2, h)
        
        # But grocery connection should be stronger (2 dimensions vs 1)
        grocery_edge = graph.graph.edges[g1, g2]
        hardware_edge1 = graph.graph.edges[g1, h]
        assert grocery_edge['weight'] > hardware_edge1['weight']
        
        # All should be in same cluster (share WHEN)
        clusters = graph.find_clusters()
        assert len(clusters) == 1
    
    def test_cluster_dimensions(self):
        """Test finding common dimensions in a cluster."""
        graph = SpecificationHypergraph()
        
        obj1 = Chunk("User", "buys", "milk",
                    dimensions={
                        Dimension.WHERE: "grocery",
                        Dimension.WHEN: "today",
                        Dimension.WHO: "John"
                    })
        obj2 = Chunk("User", "buys", "bread",
                    dimensions={
                        Dimension.WHERE: "grocery",
                        Dimension.WHEN: "today",
                        Dimension.WHO: "Jane"  # Different WHO
                    })
        
        node1 = graph.add_object(obj1)
        node2 = graph.add_object(obj2)
        
        cluster = {node1, node2}
        common_dims = graph._cluster_dimensions(cluster)
        
        # Should have WHERE and WHEN but not WHO
        assert Dimension.WHERE in common_dims
        assert common_dims[Dimension.WHERE] == "grocery"
        assert Dimension.WHEN in common_dims
        assert common_dims[Dimension.WHEN] == "today"
        assert Dimension.WHO not in common_dims
    
    def test_should_be_epic(self):
        """Test epic detection based on 2+ shared dimensions."""
        graph = SpecificationHypergraph()
        
        # Monday grocery shopping
        monday1 = Chunk("User", "buys", "milk",
                      dimensions={
                          Dimension.WHERE: "grocery",
                          Dimension.WHEN: "monday",
                          Dimension.WHO: "John"
                      })
        monday2 = Chunk("User", "buys", "bread",
                      dimensions={
                          Dimension.WHERE: "grocery",
                          Dimension.WHEN: "monday",
                          Dimension.WHO: "John"
                      })
        
        # Tuesday grocery shopping (same person and store)
        tuesday1 = Chunk("User", "buys", "eggs",
                       dimensions={
                           Dimension.WHERE: "grocery",
                           Dimension.WHEN: "tuesday",
                           Dimension.WHO: "John"
                       })
        tuesday2 = Chunk("User", "buys", "butter",
                       dimensions={
                           Dimension.WHERE: "grocery",
                           Dimension.WHEN: "tuesday",
                           Dimension.WHO: "John"
                       })
        
        m1 = graph.add_object(monday1)
        m2 = graph.add_object(monday2)
        t1 = graph.add_object(tuesday1)
        t2 = graph.add_object(tuesday2)
        
        monday_cluster = {m1, m2}
        tuesday_cluster = {t1, t2}
        
        # Should be epic (share WHERE and WHO)
        assert graph.should_be_epic(monday_cluster, tuesday_cluster)
    
    def test_organize_hierarchy_simple(self):
        """Test hierarchy generation with simple example."""
        graph = SpecificationHypergraph()
        
        # Add related tasks
        obj1 = Chunk("User", "buys", "milk",
                    dimensions={
                        Dimension.WHERE: "grocery",
                        Dimension.WHEN: "today"
                    })
        obj2 = Chunk("User", "buys", "bread",
                    dimensions={
                        Dimension.WHERE: "grocery",
                        Dimension.WHEN: "today"
                    })
        
        graph.add_object(obj1)
        graph.add_object(obj2)
        
        hierarchy = graph.organize_hierarchy()
        
        # Should have root → epic → story → tasks
        assert hierarchy.level == "root"
        assert len(hierarchy.children) == 1  # One epic
        
        epic = hierarchy.children[0]
        assert epic.level == "epic"
        assert len(epic.children) == 1  # One story
        
        story = epic.children[0]
        assert story.level == "story"
        assert len(story.children) == 2  # Two tasks
        
        for task in story.children:
            assert task.level == "task"
    
    def test_organize_hierarchy_complex(self):
        """Test hierarchy with multiple epics and stories."""
        graph = SpecificationHypergraph()
        
        # Today's errands
        grocery1 = Chunk("User", "buys", "milk",
                       dimensions={
                           Dimension.WHERE: "grocery",
                           Dimension.WHEN: "today"
                       })
        grocery2 = Chunk("User", "buys", "bread",
                       dimensions={
                           Dimension.WHERE: "grocery",
                           Dimension.WHEN: "today"
                       })
        hardware = Chunk("User", "buys", "hammer",
                       dimensions={
                           Dimension.WHERE: "hardware",
                           Dimension.WHEN: "today"
                       })
        
        # Tomorrow's cooking (completely different)
        cooking1 = Chunk("User", "prepares", "ingredients",
                       dimensions={
                           Dimension.WHERE: "kitchen",
                           Dimension.WHEN: "tomorrow",
                           Dimension.WHAT: "dinner"
                       })
        cooking2 = Chunk("User", "cooks", "meal",
                       dimensions={
                           Dimension.WHERE: "kitchen",
                           Dimension.WHEN: "tomorrow",
                           Dimension.WHAT: "dinner"
                       })
        
        graph.add_object(grocery1)
        graph.add_object(grocery2)
        graph.add_object(hardware)
        graph.add_object(cooking1)
        graph.add_object(cooking2)
        
        hierarchy = graph.organize_hierarchy()
        
        # Should have two separate epics (different WHEN values)
        assert len(hierarchy.children) == 2
        
        for epic in hierarchy.children:
            assert epic.level == "epic"
            # Each epic should have stories
            assert len(epic.children) > 0
            
            for story in epic.children:
                assert story.level == "story"
                # Each story should have tasks
                assert len(story.children) > 0
    
    def test_name_generation(self):
        """Test human-readable name generation from dimensions."""
        graph = SpecificationHypergraph()
        
        # Test various dimension combinations
        dims1 = {
            Dimension.WHERE: "grocery",
            Dimension.WHEN: "today"
        }
        name1 = graph._generate_name_from_dimensions(dims1, "Epic")
        assert "Today" in name1
        assert "grocery" in name1.lower()
        
        dims2 = {
            Dimension.WHO: "John",
            Dimension.WHAT: "shopping"
        }
        name2 = graph._generate_name_from_dimensions(dims2, "Story")
        assert "John" in name2
        assert "shopping" in name2
        
        # Empty dimensions
        name3 = graph._generate_name_from_dimensions({}, "Task")
        assert "Unnamed" in name3
    
    def test_get_node_info(self):
        """Test retrieving node information."""
        graph = SpecificationHypergraph()
        
        obj = Chunk("User", "does", "task",
                   dimensions={Dimension.WHERE: "home"})
        node_id = graph.add_object(obj)
        
        info = graph.get_node_info(node_id)
        
        assert info is not None
        assert info['node_id'] == node_id
        assert info['object']['subject'] == "User"
        assert len(info['neighbors']) == 0  # No connections
        assert len(info['edges']) == 0
        
        # Non-existent node
        assert graph.get_node_info("fake_node") is None
    
    def test_to_dict_export(self):
        """Test exporting graph to dictionary."""
        graph = SpecificationHypergraph()
        
        obj1 = Chunk("User", "buys", "milk",
                    dimensions={Dimension.WHERE: "grocery"})
        obj2 = Chunk("User", "buys", "bread",
                    dimensions={Dimension.WHERE: "grocery"})
        
        graph.add_object(obj1)
        graph.add_object(obj2)
        
        export = graph.to_dict()
        
        assert export['num_nodes'] == 2
        assert export['num_edges'] == 1
        assert len(export['clusters']) == 1
        assert len(export['clusters'][0]) == 2
    
    def test_hierarchy_node_to_dict(self):
        """Test HierarchyNode serialization."""
        node = HierarchyNode(
            level="epic",
            name="Test Epic",
            shared_dimensions={Dimension.WHERE: "store"},
            metadata={'test': 'value'}
        )
        
        child = HierarchyNode(level="story", name="Test Story")
        node.add_child(child)
        
        result = node.to_dict()
        
        assert result['level'] == "epic"
        assert result['name'] == "Test Epic"
        assert 'where' in result['shared_dimensions']
        assert len(result['children']) == 1
        assert result['metadata']['test'] == 'value'
    
    def test_transitive_clustering(self):
        """Test that clustering is transitive through shared dimensions."""
        graph = SpecificationHypergraph()
        
        # A shares WHERE with B
        obj_a = Chunk("User", "does", "A",
                     dimensions={Dimension.WHERE: "place1"})
        
        # B shares WHERE with A and WHEN with C
        obj_b = Chunk("User", "does", "B",
                     dimensions={
                         Dimension.WHERE: "place1",
                         Dimension.WHEN: "time1"
                     })
        
        # C shares WHEN with B but nothing with A
        obj_c = Chunk("User", "does", "C",
                     dimensions={Dimension.WHEN: "time1"})
        
        graph.add_object(obj_a)
        graph.add_object(obj_b)
        graph.add_object(obj_c)
        
        # All should be in same cluster (transitive connection)
        clusters = graph.find_clusters()
        assert len(clusters) == 1
        assert len(clusters[0]) == 3
    
    def test_multiple_epic_detection(self):
        """Test that multiple cluster groups form separate epics."""
        graph = SpecificationHypergraph()
        
        # Group 1: Shopping tasks (WHERE + WHEN shared)
        shop1 = Chunk("User", "shops", "groceries",
                     dimensions={
                         Dimension.WHERE: "store",
                         Dimension.WHEN: "morning",
                         Dimension.WHO: "Alice"
                     })
        shop2 = Chunk("User", "shops", "supplies",
                     dimensions={
                         Dimension.WHERE: "store",
                         Dimension.WHEN: "morning",
                         Dimension.WHO: "Alice"
                     })
        
        # Group 2: Work tasks (WHO + HOW shared, different WHEN)
        work1 = Chunk("User", "codes", "feature",
                     dimensions={
                         Dimension.WHO: "Bob",
                         Dimension.HOW: "agile",
                         Dimension.WHEN: "afternoon"
                     })
        work2 = Chunk("User", "reviews", "code",
                     dimensions={
                         Dimension.WHO: "Bob",
                         Dimension.HOW: "agile",
                         Dimension.WHEN: "afternoon"
                     })
        
        graph.add_object(shop1)
        graph.add_object(shop2)
        graph.add_object(work1)
        graph.add_object(work2)
        
        clusters = graph.find_clusters()
        # Should have 2 separate clusters
        assert len(clusters) == 2
        
        # Clusters should not be in same epic (< 2 shared dimensions)
        cluster1 = next(c for c in clusters if "node_0" in c)
        cluster2 = next(c for c in clusters if "node_2" in c)
        assert not graph.should_be_epic(cluster1, cluster2)