import math

from graphics import *
from graphs.graph import *


def print_title(title):
    print()
    print(title, '-' * 30)


def read_graph(filename, directed=False):
    with open(filename) as f:
        lines = f.readlines()
        num_verts = int(lines[0])
        graph = AdjListGraph(num_verts, directed)
        scan_verts(graph, lines[1:])
        print_graph(graph)
        return graph


def scan_verts(graph, lines):
    """ read lines of vert number pairs representing edges and add to the graph """
    for line in lines:
        v, w = line.split()
        v = int(v)
        w = int(w)
        graph.insert_edge(Edge(v, w))


def draw_graph(graph):
    win = GraphWin("Graph", 1024, 1024)
    win.setCoords(-1.1, -1.1, 1.1, 1.1)

    angle = 2 * math.pi / graph.num_verts()
    _id = list(range(graph.num_verts()))
    for vert in _id:
        a = angle * vert
        c = Circle(Point(math.cos(a), math.sin(a)), 0.01)
        c.draw(win)
        c = Text(Point(1.05 * math.cos(a), 1.05 * math.sin(a)), str(vert))
        c.draw(win)

    edges = graph.get_edges()
    for edge in edges:
        a1 = angle * edge.v
        a2 = angle * edge.w
        p1 = Point(math.cos(a1), math.sin(a1))
        p2 = Point(math.cos(a2), math.sin(a2))
        line = Line(p1, p2)
        if graph.is_directed():
            line.setArrow("last")
        line.draw(win)

    win.getMouse()  # Pause to view result
    win.close()  # Close window when done


def random_sparse_graph():
    print_title("random_sparse_graph")
    graph = create_random_sparse_graph(num_verts=30, num_edges=40, directed=True)
    print_graph(graph)
    draw_graph(graph)


def random_dense_graph():
    print_title("random_dense_graph")
    graph = create_random_dense_graph(num_verts=10, approx_num_edges=40, directed=True)
    print_graph(graph)
    draw_graph(graph)


def random_k_neighbor_graph():
    print_title("random_k_neighbor_graph")
    graph = create_random_k_neighbor_graph(num_verts=20, approx_num_edges=20, directed=False, k=3)
    print_graph(graph)
    draw_graph(graph)


class ConnectedComponentsFromEdges:
    """ Creates trees for each connected component, which are
    gradually made more shallow to give quicker answers the
    more they are queried. Sedgewick 17.5, 1.3, 1.4 """

    def __init__(self, graph):
        _id = list(range(graph.num_verts()))
        edges = graph.get_edges()
        for edge in edges:
            i = edge.v
            j = edge.w
            while i != _id[i]:
                _id[i] = _id[_id[i]]
                i = _id[i]
            while j != _id[j]:
                _id[j] = _id[_id[j]]
                j = _id[j]
            if i != j:
                _id[i] = j
        self._component_count = 0
        for i in range(graph.num_verts()):
            if i == _id[i]:
                self._component_count += 1
        self._id = _id

    def component_count(self):
        return self._component_count

    def are_connected(self, i, j):
        _id = self._id
        while i != _id[i]:
            _id[i] = _id[_id[i]]
            i = _id[i]
        while j != _id[j]:
            _id[j] = _id[_id[j]]
            j = _id[j]
        return i == j


class ConnectedComponentsFromDFS:
    """ Sedgewick 18.3 """

    def __init__(self, graph):
        self._graph = graph
        self._component_count = 0
        self._cc_id = [-1] * graph.num_verts()
        self._spanning_tree_roots = []
        self._examine_graph()

    def component_count(self):
        return self._component_count

    def are_connected(self, v, w):
        return self._cc_id[v] == self._cc_id[w]

    def dfs_spanning_tree_roots(self):
        return self._spanning_tree_roots

    def _examine_graph(self):
        for v in range(self._graph.num_verts()):
            if self._cc_id[v] == -1:
                self._component_count += 1
                self._spanning_tree_roots.append(v)
                self._traverse_component(v)

    def _traverse_component(self, v):
        self._cc_id[v] = self._component_count
        for w in self._graph.get_adj_iter(v):
            if self._cc_id[w] == -1:
                self._traverse_component(w)


def connected_component_example():
    print_title("main")
    graph = read_graph('DriverExample.txt')

    cc1 = ConnectedComponentsFromEdges(graph)
    cc2 = ConnectedComponentsFromDFS(graph)
    print(cc1.component_count(), "cc1 components")
    print("cc1 0 connected to 1:", cc1.are_connected(0, 1))
    print("cc1 1 connected to 5:", cc1.are_connected(1, 5))
    print(cc2.component_count(), "cc2 components")
    print("cc2 0 connected to 1:", cc2.are_connected(0, 1))
    print("cc2 1 connected to 5:", cc2.are_connected(1, 5))
    print("cc2 dfs spanning tree roots:", cc2.dfs_spanning_tree_roots())

    print("Path from 0 to 1:", path_from_dfs(graph, 0, 1))
    print("Path from 1 to 5:", path_from_dfs(graph, 1, 5))
    draw_graph(graph)


class ClassifyAndPrintEdgesInDFS:

    def __init__(self, graph):
        self._graph = graph
        self._depth = 0
        self._count = 0
        self._order = [-1] * graph.num_verts()
        self._examine_graph()

    def _print_level(self, v, w, _type):
        print(f"{' ' * self._depth}{v}-{w} {_type} ({self._order[v]}, {self._order[w]})")

    def _examine_graph(self):
        for v in range(self._graph.num_verts()):
            if self._order[v] == -1:
                self._traverse(Edge(v, v))

    def _traverse(self, edge):
        self._print_level(edge.v, edge.w, "tree")
        self._depth += 1
        self._order[edge.w] = self._count
        self._count += 1
        for t in sorted(self._graph.get_adj_iter(edge.w)):
            if self._order[t] == -1:
                self._traverse(Edge(edge.w, t))
            elif t == edge.v:
                self._print_level(edge.w, t, "parent")
            elif self._order[t] < self._order[edge.w]:
                self._print_level(edge.w, t, "back")
            else:
                self._print_level(edge.w, t, "down")
        self._depth -= 1


def classify_and_print_edges():
    print_title("classify_and_print_edges")
    graph = read_graph('ClassifyEdgeExample.txt')
    ClassifyAndPrintEdgesInDFS(graph)


class FindCriticalEdgesAndArticulationPoints:

    def __init__(self, graph):
        self._graph = graph
        self._order = [-1] * graph.num_verts()
        self._low = [-1] * graph.num_verts()
        self._count = -1
        self._critical_edges = []
        self._articulation_points = set()
        self._find_all()
        draw_graph(graph)

    def _find_all(self):
        for v in range(self._graph.num_verts()):
            if self._order[v] == -1:
                self._dfs(v, v)
        self._print_all()

    def _dfs(self, v, parent):
        self._count += 1
        self._order[v] = self._count
        self._low[v] = self._count
        adj = self._graph.get_adj_iter(v)
        children = 0
        for t in adj:
            if self._order[t] == -1:
                children += 1
                self._dfs(t, v)
                if self._order[t] == self._low[t]:
                    self._critical_edges.append((v, t))
                self._low[v] = min(self._low[v], self._low[t])
                if self._low[t] >= self._order[v] and v != parent:
                    self._articulation_points.add(v)
            elif t != parent:
                self._low[v] = min(self._low[v], self._order[t])
        if v == parent and children > 1:
            self._articulation_points.add(v)

    def _print_all(self):
        print(f"Critical edges: {sorted(self._critical_edges)}")
        print(f"Articulation points: {sorted(self._articulation_points)}")


def detect_critical_edges_and_articulation_points():
    print_title("detect_critical_edges_and_articulation_points")
    graph = read_graph('CriticalAndArticulation.txt')
    FindCriticalEdgesAndArticulationPoints(graph)


class DetectCycleWithDFS:

    def __init__(self, graph):
        self._graph = graph
        self._count = 0
        self._order = [-1] * graph.num_verts()
        self._examine_graph()
        draw_graph(graph)

    def _examine_graph(self):
        has_cycle = False
        v = 0
        while v < self._graph.num_verts() and has_cycle is False:
            if self._order[v] == -1:
                has_cycle = self._has_cycle(Edge(v, v))
            v += 1
        print(f"Has cycle: {has_cycle}")

    def _has_cycle(self, edge):
        self._order[edge.w] = self._count
        self._count += 1
        for t in self._graph.get_adj_iter(edge.w):
            if self._order[t] == -1:
                has = self._has_cycle(Edge(edge.w, t))
                if has:
                    return True
            elif t == edge.v:
                pass  # parent
            else:
                return True
        return False


def detect_cycle():
    print_title("detect_cycle")
    graph = read_graph('ClassifyEdgeExample.txt')
    DetectCycleWithDFS(graph)


class PrintTwoWayEulerTour:

    def __init__(self, graph):
        self._graph = graph
        self._count = 0
        self._order = [-1] * graph.num_verts()
        self._parent = [-1] * graph.num_verts()
        self._examine_graph()
        draw_graph(graph)

    def _examine_graph(self):
        for v in range(self._graph.num_verts()):
            if self._order[v] == -1:
                self._traverse(Edge(v, v))

    def _traverse(self, edge):
        if edge.v != edge.w:
            print('-', end="")
        print(edge.w, end="")
        self._order[edge.w] = self._count
        self._count += 1
        self._parent[edge.w] = edge.v
        for t in sorted(self._graph.get_adj_iter(edge.w)):
            if self._order[t] == -1:
                self._traverse(Edge(edge.w, t))
            elif t == edge.v:
                pass
            elif self._order[t] < self._order[edge.w]:
                print(f"-{t}-{edge.w}", end="")
            else:
                pass
        if edge.v == edge.w:
            print()
        else:
            print(f"-{edge.v}", end="")


def euler_tour():
    print_title("euler_tour")
    graph = read_graph('ClassifyEdgeExample.txt')
    PrintTwoWayEulerTour(graph)


def bfs_test():
    print_title("bfs_test")
    graph = AdjListGraph(6, directed=False)
    graph.add_edges_from_array([[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 4]])
    print(f"Path from 0 to 4: {path_from_bfs(graph, 0, 4)}")
    draw_graph(graph)


if __name__ == "__main__":
    connected_component_example()
    random_sparse_graph()
    random_dense_graph()
    random_k_neighbor_graph()
    classify_and_print_edges()
    detect_cycle()
    euler_tour()
    detect_critical_edges_and_articulation_points()
    bfs_test()
