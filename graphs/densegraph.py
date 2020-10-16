from collections import deque
from copy import copy
import random


class DenseGraph:
    """ A fixed-size adjacency matrix non-multigraph with indexed verts """

    def __init__(self, num_verts, directed):
        self._directed = directed
        self._verts = [[False for j in range(num_verts)] for i in range(num_verts)]
        self._num_edges = 0
        self._num_verts = num_verts

    def is_directed(self):
        return self._directed

    def set_is_directed(self):
        if not self._directed:
            self._directed = True
            self._num_edges *= 2

    def num_verts(self):
        return self._num_verts

    def get_verts(self):
        return [i for i in range(self._num_verts)]

    def num_edges(self):
        return self._num_edges

    def has_edge(self, e):
        return self._verts[e[0]][e[1]]

    def get_edges(self):
        edges = []
        for v in range(self._num_verts):
            for w in range(self._num_verts):
                if self._verts[v][w]:
                    if self.is_directed() or v <= w:
                        edges.append((v, w))
        return edges

    def insert_edge(self, edge):
        if not self._verts[edge[0]][edge[1]]:
            self._verts[edge[0]][edge[1]] = True
            if not self.is_directed():
                self._verts[edge[1]][edge[0]] = True
            self._num_edges += 1

    def add_edges_from_array(self, arr):
        for edge in arr:
            self.insert_edge(edge)

    def remove_edge(self, edge):
        if self._verts[edge[0]][edge[1]]:
            self._verts[edge[0]][edge[1]] = False
            if not self.is_directed():
                self._verts[edge[1]][edge[0]] = False
            self._num_edges -= 1

    def get_adjacent(self, v):
        return [i for i in range(self._num_verts) if self._verts[v][i]]

    def has_self_loops(self):
        for i in range(self._num_verts):
            if self._verts[i][i]:
                return True
        return False


def create_random_dense_graph(num_verts, num_edges, directed, multigraph, self_loops):
    graph = DenseGraph(num_verts, directed)

    # ensure at least one
    if self_loops:
        v = random.randint(0, num_verts - 1)
        graph.insert_edge((v, v))

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
                        graph.insert_edge((v, w))
                    else:
                        graph.insert_edge((w, v))
                if graph.num_edges() == num_edges:
                    break
            if graph.num_edges() == num_edges:
                break
    return graph


def path_from_dfs(graph, a, b):
    visited = set()
    path = []

    def search(u):
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

    def search(edge):
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
                if is_cycle and p == a:
                    times_seen += 1
                    if times_seen == 2:
                        break
                p = parent[p]

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
    print(f"is dag: {is_dag(graph)}")
    print(f"has self-loops: {has_self_loops(graph)}")
    print(f"is multigraph: {is_multigraph(graph)}")
    print(f"num verts: {graph.num_verts()}")
    print(f"num edges: {graph.num_edges()}")
    for v in sorted(graph.get_verts()):
        print(f"{v}: {sorted(list(graph.get_adjacent(v)))}")


def classify_and_print_edges(graph):
    depth = 0
    pre_count = 0
    pre = {v: -1 for v in graph.get_verts()}

    def classify_and_print_undirected_graph_edges():

        def undirected_dfs(u, parent):
            nonlocal pre_count
            nonlocal depth

            pre[u] = pre_count
            pre_count += 1
            if parent == -1:
                print(f"{u} : root")
            else:
                print(f"{' ' * depth}{parent}-{u} : tree")
            depth += 1

            for t in sorted(graph.get_adjacent(u)):
                if pre[t] == -1:
                    undirected_dfs(t, parent=u)
                elif u == t:
                    print(f"{' ' * depth}{u}-{t} : self-loop")
                elif t == parent:
                    print(f"{' ' * depth}{u}-{t} : parent")
                elif pre[t] < pre[u]:
                    print(f"{' ' * depth}{u}-{t} : back")
                else:
                    print(f"{' ' * depth}{u}-{t} : down")

            depth -= 1

        for v in sorted(graph.get_verts()):
            if pre[v] == -1:
                undirected_dfs(v, parent=-1)

    def classify_and_print_digraph_edges():

        post = {v: False for v in graph.get_verts()}

        def directed_dfs(v, parent):
            nonlocal pre_count
            nonlocal depth

            pre[v] = pre_count
            pre_count += 1
            if parent == -1:
                print(f"{v} : root")
            else:
                print(f"{' ' * depth}{parent}->{v} : tree")
            depth += 1

            for t in sorted(graph.get_adjacent(v)):
                if pre[t] == -1:
                    directed_dfs(t, parent=v)
                elif t == v:
                    print(f"{' ' * depth}{v}->{t} : self-loop")
                elif not post[t]:
                    print(f"{' ' * depth}{v}->{t} : back")
                elif pre[t] > pre[v]:
                    print(f"{' ' * depth}{v}->{t} : down")
                else:
                    print(f"{' ' * depth}{v}->{t} : cross")

            depth -= 1
            post[v] = True

        for v in sorted(graph.get_verts()):
            if pre[v] == -1:
                directed_dfs(v, parent=-1)

    if graph.is_directed():
        classify_and_print_digraph_edges()
    else:
        classify_and_print_undirected_graph_edges()


def is_dag(graph):
    if not graph.is_directed():
        return False

    pre = {v: False for v in graph.get_verts()}
    post = {v: False for v in graph.get_verts()}
    dag = True

    def directed_dfs(v):
        nonlocal dag

        pre[v] = True

        for t in graph.get_adjacent(v):
            if not pre[t]:
                directed_dfs(t)
            elif t == v:
                dag = False  # self-loop
                break
            elif not post[t]:
                dag = False  # back edge
                break

        post[v] = True

    for v in graph.get_verts():

        if dag and not pre[v]:
            directed_dfs(v)

    return dag


def convert_to_dag(graph):

    graph.set_is_directed()

    pre = {v: False for v in graph.get_verts()}
    post = {v: False for v in graph.get_verts()}
    edges_to_remove = []

    def directed_dfs(v):

        pre[v] = True

        for t in graph.get_adjacent(v):
            if not pre[t]:
                directed_dfs(t)
            elif t == v:
                edges_to_remove.append((v, t))  # self-loop
            elif not post[t]:
                edges_to_remove.append((v, t))  # back edge

        post[v] = True

    for v in graph.get_verts():
        if not pre[v]:
            directed_dfs(v)

    for edge in edges_to_remove:
        graph.remove_edge(edge)


def create_reversed_graph(graph):
    if not graph.is_directed():
        return None

    rev = DynamicGraph(directed=True)
    for edge in graph.get_edges():
        rev.insert_edge((edge[1], edge[0]))
    return rev


def topological_sort_dag(graph):
    if not graph.is_directed():
        return None

    pre = {v: False for v in graph.get_verts()}
    post = {v: False for v in graph.get_verts()}
    reverse_topo = []
    is_a_dag = True

    def dfs(v):
        nonlocal is_a_dag

        pre[v] = True
        for t in graph.get_adjacent(v):
            if not pre[t]:
                dfs(t)
            elif not post[t] or v == t:
                is_a_dag = False
                break
        post[v] = True
        reverse_topo.append(v)

    for v in graph.get_verts():
        if not pre[v]:
            dfs(v)

    if not is_a_dag:
        return None

    return reverse_topo[::-1]


def strong_components_kosaraju(graph):
    if not graph.is_directed:
        return None

    rev = create_reversed_graph(graph)
    component_id = {v: -1 for v in rev.get_verts()}
    component_count = 0
    post_id = {v: -1 for v in rev.get_verts()}
    post_count = 0

    def dfs(w, dfs_graph):
        nonlocal post_count

        component_id[w] = component_count
        for t in dfs_graph.get_adjacent(w):
            if component_id[t] == -1:
                dfs(t, dfs_graph)
        post_id[post_count] = w
        post_count += 1

    for v in rev.get_verts():
        dfs(v, rev)
    rev_post_id = copy(post_id)

    component_id = {v: -1 for v in rev.get_verts()}
    component_count = 0
    post_count = 0
    for n in range(graph.num_verts()-1, -1, -1):
        v = rev_post_id[n]
        if component_id[v] == -1:
            dfs(v, graph)
            component_count += 1

    components = [[] for _ in range(component_count+1)]
    for v, i in component_id.items():
        components[i].append(v)
    for component in components:
        component.sort()
    components.sort()

    return component_count + 1, component_id, components

