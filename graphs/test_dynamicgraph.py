from unittest import TestCase
from graphs.dynamicgraph import *


class Test(TestCase):
    def test_create_random_dense_graph(self):
        graph = create_random_dense_graph(num_verts=10, num_edges=25, directed=False, multigraph=False,
                                          self_loops=False)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 25)
        self.assertFalse(graph.is_directed())
        self.assertFalse(is_multigraph(graph))
        self.assertFalse(has_self_loops(graph))

    def test_create_random_dense_graph_2(self):
        graph = create_random_dense_graph(num_verts=10, num_edges=25, directed=False, multigraph=True, self_loops=True)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 25)
        self.assertFalse(graph.is_directed())
        self.assertTrue(is_multigraph(graph))
        self.assertTrue(has_self_loops(graph))

    def test_create_random_dense_graph_directed(self):
        graph = create_random_dense_graph(num_verts=10, num_edges=25, directed=True, multigraph=False, self_loops=False)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 25)
        self.assertTrue(graph.is_directed())
        self.assertFalse(is_multigraph(graph))
        self.assertFalse(has_self_loops(graph))

    def test_create_random_dense_graph_directed_2(self):
        graph = create_random_dense_graph(num_verts=10, num_edges=25, directed=True, multigraph=True, self_loops=True)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 25)
        self.assertTrue(graph.is_directed())
        self.assertTrue(is_multigraph(graph))
        self.assertTrue(has_self_loops(graph))

    def test_create_random_k_neighbor_graph(self):
        graph = create_random_k_neighbor_graph(k=3, num_verts=10, num_edges=10, directed=False, multigraph=False,
                                               self_loops=False)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 10)
        self.assertFalse(graph.is_directed())
        self.assertFalse(is_multigraph(graph))
        self.assertFalse(has_self_loops(graph))

    def test_create_random_k_neighbor_graph_2(self):
        graph = create_random_k_neighbor_graph(k=3, num_verts=10, num_edges=10, directed=False, multigraph=True,
                                               self_loops=True)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 10)
        self.assertFalse(graph.is_directed())
        self.assertTrue(is_multigraph(graph))
        self.assertTrue(has_self_loops(graph))

    def test_create_random_k_neighbor_graph_directed(self):
        graph = create_random_k_neighbor_graph(k=3, num_verts=10, num_edges=10, directed=True, multigraph=False,
                                               self_loops=False)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 10)
        self.assertTrue(graph.is_directed())
        self.assertFalse(is_multigraph(graph))
        self.assertFalse(has_self_loops(graph))

    def test_create_random_k_neighbor_graph_directed_2(self):
        graph = create_random_k_neighbor_graph(k=3, num_verts=10, num_edges=10, directed=True, multigraph=True,
                                               self_loops=True)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 10)
        self.assertTrue(graph.is_directed())
        self.assertTrue(is_multigraph(graph))
        self.assertTrue(has_self_loops(graph))

    def test_create_random_sparse_graph(self):
        graph = create_random_sparse_graph(num_verts=10, num_edges=25, directed=False, multigraph=False,
                                           self_loops=False)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 25)
        self.assertFalse(graph.is_directed())
        self.assertFalse(is_multigraph(graph))
        self.assertFalse(has_self_loops(graph))

    def test_create_random_sparse_graph_2(self):
        graph = create_random_sparse_graph(num_verts=10, num_edges=25, directed=False, multigraph=True, self_loops=True)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 25)
        self.assertFalse(graph.is_directed())
        self.assertTrue(is_multigraph(graph))
        self.assertTrue(has_self_loops(graph))

    def test_create_random_sparse_graph_directed(self):
        graph = create_random_sparse_graph(num_verts=10, num_edges=25, directed=True, multigraph=False,
                                           self_loops=False)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 25)
        self.assertTrue(graph.is_directed())
        self.assertFalse(is_multigraph(graph))
        self.assertFalse(has_self_loops(graph))

    def test_create_random_sparse_graph_directed_2(self):
        graph = create_random_sparse_graph(num_verts=10, num_edges=25, directed=True, multigraph=True, self_loops=True)
        self.assertEqual(graph.num_verts(), 10)
        self.assertEqual(graph.num_edges(), 25)
        self.assertTrue(graph.is_directed())
        self.assertTrue(is_multigraph(graph))
        self.assertTrue(has_self_loops(graph))

    def test_path_from_dfs(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 3], [2, 3], [3, 3], [3, 4]])
        self.assertEqual("1-2-3-4", path_from_dfs(graph, 1, 4))

    def test_path_from_dfs_self_loop(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 0], [1, 2]])
        self.assertEqual("0-0", path_from_dfs(graph, 0, 0))

    def test_path_from_dfs_cycle(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 0]])
        self.assertEqual("0-1-0", path_from_dfs(graph, 0, 0))

    def test_path_from_dfs_none(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [2, 3]])
        self.assertEqual("", path_from_dfs(graph, 0, 3))

    def test_path_from_dfs_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 3], [2, 3], [3, 3], [3, 4]])
        self.assertEqual("1-2-3-4", path_from_dfs(graph, 1, 4))

    def test_path_from_dfs_self_loop_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 0], [1, 2]])
        self.assertEqual("0-0", path_from_dfs(graph, 0, 0))

    def test_path_from_dfs_cycle_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 0]])
        self.assertEqual("0-1-2-0", path_from_dfs(graph, 0, 0))

    def test_path_from_dfs_none_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [2, 3]])
        self.assertEqual("", path_from_dfs(graph, 0, 3))

    def test_path_from_bfs(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 3], [2, 3], [3, 3], [3, 4]])
        self.assertEqual("1-2-3-4", path_from_bfs(graph, 1, 4))

    def test_path_from_bfs_self_loop(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 0], [1, 2]])
        self.assertEqual("0-0", path_from_bfs(graph, 0, 0))

    def test_path_from_bfs_cycle(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 0]])
        self.assertEqual("0-1-0", path_from_bfs(graph, 0, 0))

    def test_path_from_bfs_none(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [2, 3]])
        self.assertEqual("", path_from_bfs(graph, 0, 3))

    def test_path_from_bfs_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 3], [2, 3], [3, 3], [3, 4]])
        self.assertEqual("1-2-3-4", path_from_bfs(graph, 1, 4))

    def test_path_from_bfs_self_loop_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 0], [1, 2]])
        self.assertEqual("0-0", path_from_bfs(graph, 0, 0))

    def test_path_from_bfs_cycle_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 0]])
        self.assertEqual("0-1-2-0", path_from_bfs(graph, 0, 0))

    def test_path_from_bfs_none_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [2, 3]])
        self.assertEqual("", path_from_bfs(graph, 0, 3))

    def test_has_self_loops(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [2, 2], [2, 3]])
        self.assertTrue(has_self_loops(graph))

        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 3]])
        self.assertFalse(has_self_loops(graph))

    def test_has_self_loops_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [2, 2], [2, 3]])
        self.assertTrue(has_self_loops(graph))

        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 3]])
        self.assertFalse(has_self_loops(graph))

    def test_is_multigraph(self):
        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [2, 3], [3, 2]])
        self.assertTrue(is_multigraph(graph))

        graph = DynamicGraph(directed=False)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 3]])
        self.assertFalse(is_multigraph(graph))

    def test_is_multigraph_directed(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [2, 3], [2, 3]])
        self.assertTrue(is_multigraph(graph))

        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [2, 2], [2, 2]])
        self.assertTrue(is_multigraph(graph))

        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [1, 2], [2, 3]])
        self.assertFalse(is_multigraph(graph))

    def test_print_graph(self):
        graph = DynamicGraph(directed=True)
        graph.add_edges_from_array([[0, 1], [1, 1], [2, 3], [2, 3], [3, 4]])
        print_graph(graph)
