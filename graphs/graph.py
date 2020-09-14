from collections import deque
import random


class Edge:

    def __init__(self, v, w):
        self.v = v
        self.w = w


class Graph:
    """ A base class for different graph implementations """

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

    def get_adj_iter(self, v):
        return []


class AdjListGraph(Graph):
    """ Adjacency-list multigraph based on Sedgewick, 17.1 """

    def __init__(self, num_verts, directed):
        super().__init__(num_verts, directed)
        self._verts = [list() for _ in range(num_verts)]

    def insert_edge(self, edge):
        self._verts[edge.v].append(edge.w)
        if not self.is_directed():
            self._verts[edge.w].append(edge.v)
        self._num_edges += 1

    def remove_edge(self, edge):
        self._verts[edge.v].remove(edge.w)
        if not self.is_directed():
            self._verts[edge.w].remove(edge.v)
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


def create_random_dense_graph(num_verts, approx_num_edges, directed):
    """ Sedgewick 17.13 """
    graph = AdjSetGraph(num_verts, directed)
    probability = approx_num_edges / (num_verts * (num_verts - 1))
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


def create_random_k_neighbor_graph(num_verts, approx_num_edges, directed, k):
    """  """
    graph = AdjSetGraph(num_verts, directed)
    probability = approx_num_edges / (num_verts * (2 * k))
    if not directed:
        probability *= 2
    for v in range(num_verts):
        for x in range(v - k, v + k):
            w = (x + num_verts) % num_verts
            p = random.random()
            if p < probability and w != v:
                if directed and random.randint(0, 1) == 1:
                    graph.insert_edge(Edge(v, w))
                else:
                    graph.insert_edge(Edge(w, v))
    return graph


def create_random_sparse_graph(num_verts, num_edges, directed):
    """ Sedgewick 17.12 """
    graph = AdjSetGraph(num_verts, directed)
    while graph.num_edges() < num_edges:
        v = random.randint(0, num_verts - 1)
        w = random.randint(0, num_verts - 1)
        if v != w:
            graph.insert_edge(Edge(v, w))
    return graph


def path_from_dfs(graph, v, w):
    """ Sedgewick 17.16 """
    visited = [False] * graph.num_verts()
    path = []

    def search(u):
        path.append(u)
        if u == w:
            return True
        visited[u] = True
        neighbors = graph.get_adj_iter(u)
        for vert in neighbors:
            if not visited[vert]:
                if search(vert):
                    return True
        path.pop()
        return False

    search(v)
    return path


def path_from_bfs(graph, a, b):
    visited = [False] * graph.num_verts()
    parent = [-1] * graph.num_verts()
    queue = deque()

    def search(edge):
        parent[edge.w] = edge.v
        if edge.w == b:
            return True
        visited[edge.w] = True
        neighbors = graph.get_adj_iter(edge.w)
        for vert in neighbors:
            if not visited[vert]:
                queue.appendleft(Edge(edge.w, vert))
        return False

    found = False
    queue.appendleft(Edge(-1, a))
    while queue and not found:
        found = search(queue.pop())

    path = deque()
    path_str = ""
    if found:
        p = b
        while p != -1:
            path.appendleft(p)
            p = parent[p]
        path_str = "-".join([str(node) for node in path])

    return path_str


def print_graph(graph):
    """ Sedgewick 17.3 """

    print(f"directed: { graph.is_directed() }")
    print(f"num verts: { graph.num_verts() }")
    print(f"num edges: { graph.num_edges() }")
    for v in range(graph.num_verts()):
        print(f"{ v }: { sorted(list(graph.get_adj_iter(v))) }")
