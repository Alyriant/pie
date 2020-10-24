from unittest import TestCase
from graphs.weighted_dynamic_graph import *
from parameterized import parameterized, parameterized_class


class TestWeightedWeightedDynamicGraph(TestCase):
    def test_get_edges(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1, 1], [1, 2, 1], [2, 1, 1], [3, 3, 1], [3, 3, 1]])
        self.assertEqual(5, graph.num_edges())
        self.assertEqual(5, len(graph.get_edges()))
        graph.set_is_directed()
        self.assertEqual(10, graph.num_edges())
        self.assertEqual(10, len(graph.get_edges()))

    @parameterized.expand([
        ("FFF", 10, 25, False, False, False),
        ("FFT", 10, 25, False, False, True),
        ("FTF", 10, 25, False, True, False),
        ("FTT", 10, 25, False, True, True),
        ("TFF", 10, 25, True, False, False),
        ("TFT", 10, 25, True, False, True),
        ("TTF", 10, 25, True, True, False),
        ("TTT", 10, 25, True, True, True),
    ])
    def test_create_random_dense_graph(self, name, num_verts, num_edges, directed, multigraph, self_loops):
        graph = create_random_dense_graph(num_verts, num_edges, directed, multigraph, self_loops)
        self.assertEqual(num_verts, graph.num_verts())
        self.assertEqual(num_edges, graph.num_edges())
        self.assertEqual(directed, graph.is_directed())
        self.assertEqual(multigraph, is_multigraph(graph))
        self.assertEqual(self_loops, graph.has_self_loops())

    @parameterized.expand([
        ("FFF", 3, 10, 10, False, False, False),
        ("FFT", 3, 10, 10, False, False, True),
        ("FTF", 3, 10, 10, False, True, False),
        ("FTT", 3, 10, 10, False, True, True),
        ("TFF", 3, 10, 10, True, False, False),
        ("TFT", 3, 10, 10, True, False, True),
        ("TTF", 3, 10, 10, True, True, False),
        ("TTT", 3, 10, 10, True, True, True),
    ])
    def test_create_random_k_neighbor_graph(self, name, k, num_verts, num_edges, directed, multigraph, self_loops):
        graph = create_random_k_neighbor_graph(k, num_verts, num_edges, directed, multigraph, self_loops)
        self.assertEqual(num_verts, graph.num_verts())
        self.assertEqual(num_edges, graph.num_edges())
        self.assertEqual(directed, graph.is_directed())
        self.assertEqual(multigraph, is_multigraph(graph))
        self.assertEqual(self_loops, graph.has_self_loops())

    @parameterized.expand([
        ("FFF", 10, 25, False, False, False),
        ("FFT", 10, 25, False, False, True),
        ("FTF", 10, 25, False, True, False),
        ("FTT", 10, 25, False, True, True),
        ("TFF", 10, 25, True, False, False),
        ("TFT", 10, 25, True, False, True),
        ("TTF", 10, 25, True, True, False),
        ("TTT", 10, 25, True, True, True),
    ])
    def test_create_random_sparse_graph(self, name, num_verts, num_edges, directed, multigraph,self_loops):
        graph = create_random_sparse_graph(num_verts, num_edges, directed, multigraph,self_loops)
        self.assertEqual(num_verts, graph.num_verts())
        self.assertEqual(num_edges, graph.num_edges())
        self.assertEqual(directed, graph.is_directed())
        self.assertEqual(multigraph, is_multigraph(graph))
        self.assertEqual(self_loops, graph.has_self_loops())

    def test_path_from_dfs(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 3], [2, 3], [3, 3], [3, 4]])
        self.assertEqual("1-2-3-4", path_from_dfs(graph, 1, 4))

    def test_path_from_dfs_self_loop(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 0], [1, 2]])
        self.assertEqual("0-0", path_from_dfs(graph, 0, 0))

    def test_path_from_dfs_cycle(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 0]])
        self.assertEqual("0-1-0", path_from_dfs(graph, 0, 0))

    def test_path_from_dfs_none(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 3]])
        self.assertEqual("", path_from_dfs(graph, 0, 3))

    def test_path_from_dfs_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 3], [2, 3], [3, 3], [3, 4]])
        self.assertEqual("1-2-3-4", path_from_dfs(graph, 1, 4))

    def test_path_from_dfs_self_loop_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 0], [1, 2]])
        self.assertEqual("0-0", path_from_dfs(graph, 0, 0))

    def test_path_from_dfs_cycle_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 0]])
        self.assertEqual("0-1-2-0", path_from_dfs(graph, 0, 0))

    def test_path_from_dfs_none_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 3]])
        self.assertEqual("", path_from_dfs(graph, 0, 3))

    def test_path_from_bfs(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 3], [2, 3], [3, 3], [3, 4]])
        self.assertEqual("1-2-3-4", path_from_bfs(graph, 1, 4))

    def test_path_from_bfs_self_loop(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 0], [1, 2]])
        self.assertEqual("0-0", path_from_bfs(graph, 0, 0))

    def test_path_from_bfs_cycle(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 0]])
        self.assertEqual("0-1-0", path_from_bfs(graph, 0, 0))

    def test_path_from_bfs_none(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 3]])
        self.assertEqual("", path_from_bfs(graph, 0, 3))

    def test_path_from_bfs_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 3], [2, 3], [3, 3], [3, 4]])
        self.assertEqual("1-2-3-4", path_from_bfs(graph, 1, 4))

    def test_path_from_bfs_self_loop_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 0], [1, 2]])
        self.assertEqual("0-0", path_from_bfs(graph, 0, 0))

    def test_path_from_bfs_cycle_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 0]])
        self.assertEqual("0-1-2-0", path_from_bfs(graph, 0, 0))

    def test_path_from_bfs_none_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 3]])
        self.assertEqual("", path_from_bfs(graph, 0, 3))

    def test_has_self_loops(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 2], [2, 3]])
        self.assertTrue(graph.has_self_loops())

        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 3]])
        self.assertFalse(graph.has_self_loops())

    def test_has_self_loops_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 2], [2, 3]])
        self.assertTrue(graph.has_self_loops())

        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 3]])
        self.assertFalse(graph.has_self_loops())

    def test_is_multigraph(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 3], [3, 2]])
        self.assertTrue(is_multigraph(graph))

        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 2], [2, 2]])
        self.assertTrue(is_multigraph(graph))

        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 3]])
        self.assertFalse(is_multigraph(graph))

    def test_is_multigraph_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 3], [2, 3]])
        self.assertTrue(is_multigraph(graph))

        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [2, 2], [2, 2]])
        self.assertTrue(is_multigraph(graph))

        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 3]])
        self.assertFalse(is_multigraph(graph))

    def test_print_weighted_graph(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 1], [2, 3], [2, 3], [3, 4]])
        print_weighted_graph(graph)

    def test_classify_and_print_edges(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 1], [1, 2], [2, 0], [3, 4]])
        classify_and_print_edges(graph)

    def test_classify_and_print_edges_directed(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [0, 2], [0, 2], [1, 1], [1, 2], [2, 0], [3, 2]])
        classify_and_print_edges(graph)

    def test_is_dag(self):
        graph = WeightedDynamicGraph(directed=False)
        self.assertFalse(is_dag(graph))

        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [0, 1], [1, 2]])
        self.assertTrue(is_dag(graph))

        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 1]])
        self.assertFalse(is_dag(graph))

        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 1]])
        self.assertFalse(is_dag(graph))

        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [2, 0]])
        self.assertFalse(is_dag(graph))

    def test_convert_to_dag(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [0, 1], [1, 1], [1, 1], [1, 2], [2, 0], [2, 1]])
        self.assertFalse(is_dag(graph))
        convert_to_dag(graph)
        self.assertTrue(is_dag(graph))

    def test_create_reversed_graph(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1, 0.5], [1, 2, 0.6]])
        graph2 = create_reversed_graph(graph)
        self.assertTrue(graph2.has_edge_ignoring_weight(1, 0))
        self.assertTrue(graph2.has_edge(Edge(2, 1, 0.6)))

    def test_topological_sort_dag(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [0, 2], [1, 2], [3, 2]])
        t = topological_sort_dag(graph)
        self.assertTrue(t.index(3) < t.index(2))
        self.assertTrue(t.index(1) < t.index(2))
        self.assertTrue(t.index(0) < t.index(2))
        self.assertTrue(t.index(0) < t.index(1))

    def test_topological_sort_not_dag(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [0, 2], [2, 0], [1, 2], [3, 2]])
        t = topological_sort_dag(graph)
        self.assertEqual(None, t)

    def test_strong_components_kosaraju(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 1], [1, 2], [1, 2], [2, 0], [2, 3], [3, 4], [4, 3], [5, 3]])
        component_count, ids, components = strong_components_kosaraju(graph)
        # print(components)
        self.assertEqual(3, component_count)
        self.assertEqual(3, len(components))
        self.assertTrue(ids[0] == ids[1] and ids[0] == ids[2])
        self.assertTrue(ids[3] == ids[4])
        self.assertFalse(ids[2] == ids[3])
        self.assertFalse(ids[3] == ids[5])

    def test_strong_components_kosaraju2(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 0], [0, 1], [1, 2], [2, 0], [2, 3], [2, 3], [3, 4],
                                    [4, 5], [5, 6], [6, 3], [6, 4]])
        component_count, ids, components = strong_components_kosaraju(graph)
        # print(components)
        self.assertEqual(2, component_count)
        self.assertEqual(2, len(components))
        self.assertTrue(ids[0] == ids[1] and ids[0] == ids[2])
        self.assertTrue(ids[3] == ids[4] and ids[3] == ids[5] and ids[3] == ids[6])

    def test_find_kernel_dag_for_digraph(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 0], [0, 1], [1, 2], [2, 0], [2, 3], [2, 3], [3, 4],
                                    [4, 5], [5, 6], [6, 3], [6, 4]])
        kernel_dag, vert_to_component_map = find_kernel_dag_for_digraph(graph)
        # print_graph(kernel_dag)
        self.assertEqual(1, kernel_dag.num_edges())
        self.assertEqual(2, kernel_dag.num_verts())
        edges = kernel_dag.get_edges()
        self.assertTrue(edges[0] in ((0, 1), (1, 0)))

    def test_digraph_transitive_closure(self):
        graph = WeightedDynamicGraph(directed=True)
        graph.add_edges_from_array_default_weight([[0, 0], [0, 1], [1, 2], [2, 0], [2, 3], [2, 3], [3, 4],
                                    [4, 5], [5, 6], [6, 3], [6, 4]])
        tc = DigraphTransitiveClosure(graph)
        for v in range(3):
            for w in range(7):
                self.assertTrue(tc.reachable(v, w))
        for v in range(3, 7):
            for w in range(3, 7):
                self.assertTrue(tc.reachable(v, w))
            for w in range(0, 3):
                self.assertFalse(tc.reachable(v, w))

    def test_prims_algorithm_for_minimal_spanning_tree(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1, 4], [0, 2, 5], [0, 3, 3], [1, 2, 1], [1, 3, 6], [2, 3, 2]])
        total_weight, mst_edges = prims_algorithm_for_minimal_spanning_tree(graph)
        self.assertEqual(6, total_weight)
        self.assertEqual(3, len(mst_edges))
        for e in (Edge(1, 2, 1), Edge(2, 3, 2), Edge(0, 3, 3)):
            self.assertTrue(e in mst_edges)

    def test_prims_algorithm_with_priority_queue(self):
        graph = WeightedDynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1, 4], [0, 2, 5], [0, 3, 3], [1, 2, 1], [1, 3, 6], [2, 3, 2]])
        total_weight, mst_edges = prims_algorithm_with_priority_queue(graph)
        self.assertEqual(6, total_weight)
        self.assertEqual(3, len(mst_edges))
        for e in (Edge(1, 2, 1), Edge(2, 3, 2), Edge(0, 3, 3)):
            f = Edge(e.w, e.v, e.weight)
            self.assertTrue(e in mst_edges or f in mst_edges)
