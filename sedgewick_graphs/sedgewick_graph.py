from graphics import *
import math
import random


class Edge:

    def __init__(self, v, w):
        self.v = v
        self.w = w


class Graph:

    def __init__(self, num_verts, directed):
        self._num_verts = num_verts
        self._directed = directed
        self._num_edges = 0

    def num_verts(self):
        return self._num_verts

    def num_edges(self):
        return self._num_edges

    def is_directed(self):
        return self._directed

    def get_edges(self):
        """ Sedgewick 17.2 """

        edges = []
        for v in range(self.num_verts()):
            for w in self.get_adj_iter(v):
                if self.is_directed() or v < w:
                    edges.append(Edge(v, w))
        return edges

    def depth_first_search_path(self, v, w):
        """ Sedgewick 17.16 """
        visited = [False] * self.num_verts()
        path = []

        def search(u):
            path.append(u)
            if u == w:
                return True
            visited[u] = True
            neighbors = self.get_adj_iter(u)
            for vert in neighbors:
                if not visited[vert]:
                    if search(vert):
                        return True
            path.pop()
            return False

        search(v)
        return path


class AdjListGraph(Graph):
    """ Adjacency-list multigraph based on Sedgewick, 17.1 """

    def __init__(self, num_verts, directed):
        super().__init__(num_verts, directed)
        self._verts = [list() for _ in range(num_verts)]

    def insert_edge(self, edge):
        self._verts[edge.v].append(edge.w)
        self._num_edges += 1

    def remove_edge(self, edge):
        self._verts[edge.v].remove(edge.w)
        self._num_edges -= 1

    def get_adj_iter(self, v):
        return self._verts[v]


class AdjSetGraph(Graph):
    """ Adjacency-set graph based on Sedgewick, 17.1 """

    def __init__(self, num_verts, directed):
        super().__init__(num_verts, directed)
        self._verts = [set() for _ in range(num_verts)]

    def insert_edge(self, edge):
        if edge.w not in self._verts[edge.v]:
            self._verts[edge.v].add(edge.w)
            self._num_edges += 1
            if not self._directed:
                self._verts[edge.w].add(edge.v)

    def remove_edge(self, edge):
        if edge.w in self._verts[edge.v]:
            self._verts[edge.v].remove(edge.w)
            self._num_edges -= 1
            if not self._directed:
                self._verts[edge.w].remove(edge.v)

    def get_adj_iter(self, v):
        return list(self._verts[v])


def print_title(title):
    print()
    print(title, '-' * 30)


def print_graph(graph):
    """ Sedgewick 17.3 """

    print(f"directed: {graph.is_directed()}")
    print(f"num verts: {graph.num_verts()}")
    print(f"num edges: {graph.num_edges()}")
    for v in range(graph.num_verts()):
        print(v, ":", end=" ")
        w = sorted(list(graph.get_adj_iter(v)))
        print(w)


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
        if not graph.is_directed():
            graph.insert_edge(Edge(w, v))


def draw_graph(graph):
    win = GraphWin("Graph", 1024, 1024)
    win.setCoords(-1.1, -1.1, 1.1, 1.1)

    angle = 2 * math.pi / graph.num_verts()
    id = list(range(graph.num_verts()))
    for vert in id:
        a = angle * vert
        c = Circle(Point(math.cos(a), math.sin(a)), 0.01)
        c.draw(win)
        c = Text(Point(1.05*math.cos(a), 1.05*math.sin(a)), str(vert))
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


def create_random_sparse_graph(num_verts, num_edges, directed):
    """ Sedgewick 17.12 """
    graph = AdjSetGraph(num_verts, directed)
    while graph.num_edges() < num_edges:
        v = random.randint(0, num_verts-1)
        w = random.randint(0, num_verts-1)
        if v != w:
            graph.insert_edge(Edge(v, w))
    return graph


def random_sparse_graph():
    print_title("random_sparse_graph")
    graph = create_random_sparse_graph(num_verts=30, num_edges=40, directed=True)
    print_graph(graph)
    draw_graph(graph)


def create_random_dense_graph(num_verts, approx_num_edges, directed):
    """ Sedgewick 17.13 """
    graph = AdjSetGraph(num_verts, directed)
    probability = approx_num_edges/(num_verts*(num_verts-1))
    if not directed:
        probability *= 2
    for v in range(num_verts):
        if directed:
            next_range = num_verts
        else:
            next_range = v
        for w in range(next_range):
            if random.random() < probability and w != v:
                if directed and random.randint(0, 1) == 1:
                    graph.insert_edge(Edge(v, w))
                else:
                    graph.insert_edge(Edge(w, v))
    return graph


def random_dense_graph():
    print_title("random_dense_graph")
    graph = create_random_dense_graph(num_verts=10, approx_num_edges=40, directed=True)
    print_graph(graph)
    draw_graph(graph)


def create_random_k_neighbor_graph(num_verts, approx_num_edges, directed, k):
    """  """
    graph = AdjSetGraph(num_verts, directed)
    probability = approx_num_edges/(num_verts*(2*k))
    if not directed:
        probability *= 2
    for v in range(num_verts):
        if directed:
            next_range = num_verts
        else:
            next_range = v
        for x in range(v-k, v+k):
            w = (x+num_verts) % num_verts
            p = random.random()
            if p < probability and w != v:
                if directed and random.randint(0, 1) == 1:
                    graph.insert_edge(Edge(v, w))
                else:
                    graph.insert_edge(Edge(w, v))
    return graph


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

    print("Path from 0 to 1:", graph.depth_first_search_path(0, 1))
    print("Path from 1 to 5:", graph.depth_first_search_path(1, 5))
    draw_graph(graph)


class ClassifyAndPrintEdgesInDFS:

    def __init__(self, graph):
        self._graph = graph
        self._depth = 0
        self._count = 0
        self._order = [-1] * graph.num_verts()
        self._parent = [-1] * graph.num_verts()
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
        self._parent[edge.w] = edge.v
        for t in sorted(self._graph.get_adj_iter(edge.w)):
            if self._order[t] == -1:
                self._traverse(Edge(edge.w, t))
            elif t == edge.v:
                self._print_level(edge.w, t,  "parent")
            elif self._order[t] < self._order[edge.w]:
                self._print_level(edge.w, t, "back")
            else:
                self._print_level(edge.w, t, "down")
        self._depth -= 1


def classify_and_print_edges():
    print_title("classify_and_print_edges")
    graph = read_graph('ClassifyEdgeExample.txt')
    ClassifyAndPrintEdgesInDFS(graph)


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
                self._has_cycle(Edge(edge.w, t))
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


if __name__ == "__main__":
    connected_component_example()
    random_sparse_graph()
    random_dense_graph()
    random_k_neighbor_graph()
    classify_and_print_edges()
    detect_cycle()
    euler_tour()
