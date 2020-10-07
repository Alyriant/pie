from collections import deque
import random


class DynamicGraph:
    """ An adjacency list multigraph with named verts which can add verts. """

    def __init__(self, directed):
        self._directed = directed
        self._verts = {}
        self._num_edges = 0

    def is_directed(self):
        return self._directed

    def num_verts(self):
        return len(self._verts)

    def _assure_vert(self, v):
        if v not in self._verts:
            self._verts[v] = []

    def add_vert(self, v):
        self._assure_vert(v)

    def get_verts(self):
        return self._verts.keys()

    def num_edges(self):
        return self._num_edges

    def has_edge(self, e):
        return e[1] in self.get_adjacent(e[0])

    def get_edges(self):
        edges = []
        for v, ws in self._verts:
            for w in ws:
                if self.is_directed() or v <= w:
                    edges.append((v, w))
        return edges

    def insert_edge(self, edge):
        self._assure_vert(edge[0])
        self._assure_vert(edge[1])
        self._verts[edge[0]].append(edge[1])
        if not self.is_directed() and edge[0] != edge[1]:
            self._verts[edge[1]].append(edge[0])
        self._num_edges += 1

    def add_edges_from_array(self, arr):
        for edge in arr:
            self.insert_edge(edge)

    def remove_edge(self, edge):
        self._verts[edge[0]].remove(edge[1])
        if not self.is_directed() and edge[0] != edge[1]:
            self._verts[edge[1]].remove(edge[0])
        self._num_edges -= 1

    def get_adjacent(self, v):
        return self._verts[v]


def create_random_dense_graph(num_verts, num_edges, directed, multigraph, self_loops):
    graph = DynamicGraph(directed)
    for v in range(num_verts):
        graph.add_vert(v)

    # ensure at least one
    if self_loops:
        v = random.randint(0, num_verts - 1)
        graph.insert_edge((v, v))
    if multigraph:
        v = random.randint(0, num_verts - 1)
        w = random.randint(0, num_verts - 1)
        graph.insert_edge((v, w))
        graph.insert_edge((v, w))

    probability = num_edges / (num_verts * (num_verts - 1))
    if not directed:
        probability *= 2
    while graph.num_edges() < num_edges:
        for v in range(num_verts):
            if directed:
                next_range = num_verts
            else:
                next_range = v + 1
            for w in range(next_range):
                if random.random() < probability and (self_loops or w != v):
                    if directed and random.randint(0, 1) == 1:
                        if multigraph or not graph.has_edge((v, w)):
                            graph.insert_edge((v, w))
                    else:
                        if multigraph or not graph.has_edge((w, v)):
                            graph.insert_edge((w, v))
                if graph.num_edges() == num_edges:
                    break
            if graph.num_edges() == num_edges:
                break
    return graph


def create_random_k_neighbor_graph(k, num_verts, num_edges, directed, multigraph, self_loops):
    graph = DynamicGraph(directed)
    for v in range(num_verts):
        graph.add_vert(v)

    # ensure at least one
    if self_loops:
        v = random.randint(0, num_verts - 1)
        graph.insert_edge((v, v))
    if multigraph:
        v = random.randint(0, num_verts - 1)
        w = (v+k) % num_verts
        graph.insert_edge((v, w))
        graph.insert_edge((v, w))

    probability = num_edges / (num_verts * (2 * k))
    if not directed:
        probability *= 2
    while graph.num_edges() < num_edges:
        for v in range(num_verts):
            for x in range(v - k, v + k + 1):
                w = (x + num_verts) % num_verts
                p = random.random()
                if p < probability and (self_loops or w != v):
                    if directed and random.randint(0, 1) == 1:
                        if multigraph or not graph.has_edge((v, w)):
                            graph.insert_edge((v, w))
                    else:
                        if multigraph or not graph.has_edge((w, v)):
                            graph.insert_edge((w, v))
                if graph.num_edges() == num_edges:
                    break
            if graph.num_edges() == num_edges:
                break
    return graph


def create_random_sparse_graph(num_verts, num_edges, directed, multigraph, self_loops):
    graph = DynamicGraph(directed)
    for v in range(num_verts):
        graph.add_vert(v)

    # ensure at least one
    if self_loops:
        v = random.randint(0, num_verts - 1)
        graph.insert_edge((v, v))
    if multigraph:
        v = random.randint(0, num_verts - 1)
        w = random.randint(0, num_verts - 1)
        graph.insert_edge((v, w))
        graph.insert_edge((v, w))

    while graph.num_edges() < num_edges:
        v = random.randint(0, num_verts - 1)
        w = random.randint(0, num_verts - 1)
        if (self_loops or w != v) and (multigraph or not graph.has_edge((v, w))):
            graph.insert_edge((v, w))
    return graph


def path_from_dfs(graph, a, b):
    visited = set()
    path = []

    def search(u):
        print("search {u}")
        path.append(u)
        visited.add(u)
        if u == b and len(path) > 1:
            return True
        else:
            neighbors = graph.get_adjacent(u)
            for vert in neighbors:
                if vert not in visited or vert == b:
                    if search(vert):
                        return True
        path.pop()
        return False

    if a == b and a in graph.get_adjacent(a):
        path.extend([b, b])
    else:
        search(a)

    path_str = ""
    if path:
        path_str = "-".join([str(vert) for vert in path])

    return path_str


def path_from_bfs(graph, a, b):
    visited = set()
    parent = {v: -1 for v in graph.get_verts()}
    unprocessed = deque()
    is_cycle = (a == b)
    path = None

    def search(edge):
        print(f"search {edge}")
        parent[edge[1]] = edge[0]
        if edge[1] == b and edge[0] != -1:
            return True
        visited.add(edge[1])
        neighbors = graph.get_adjacent(edge[1])
        for vert in neighbors:
            if vert not in visited or vert == b:
                unprocessed.appendleft((edge[1], vert))
        return False

    if is_cycle and a in graph.get_adjacent(a):
        path = [a, a]
    else:
        found = False
        unprocessed.appendleft((-1, a))
        while unprocessed and not found:
            found = search(unprocessed.pop())

        times_seen = 0
        path = deque()
        if found:
            p = b
            while p != -1:
                path.appendleft(p)
                print("appending", p)
                if is_cycle and p == a:
                    times_seen += 1
                    if times_seen == 2:
                        break
                p = parent[p]
        else: print("not found")

    path_str = ""
    if path:
        path_str = "-".join([str(vert) for vert in path])

    return path_str


def has_self_loops(graph):
    for v in graph.get_verts():
        if v in graph.get_adjacent(v):
            return True
    return False


def is_multigraph(graph):
    for v in graph.get_verts():
        seen = set()
        for w in graph.get_adjacent(v):
            if w in seen:
                return True
            else:
                seen.add(w)
    return False


def print_graph(graph):
    print(f"directed: {graph.is_directed()}")
    print(f"has self-loops: {has_self_loops(graph)}")
    print(f"is multigraph: {is_multigraph(graph)}")
    print(f"num verts: {graph.num_verts()}")
    print(f"num edges: {graph.num_edges()}")
    for v in sorted(graph.get_verts()):
        print(f"{v}: {sorted(list(graph.get_adjacent(v)))}")
