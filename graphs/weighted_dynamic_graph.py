import functools
from collections import deque
from copy import copy, deepcopy
from typing import TypeVar, Dict, List, Iterable, Union, Optional
import random
from graphs.densegraph import DenseGraph

VertName = TypeVar('VertName', int, str)
Weight = TypeVar('Weight', int, float)


@functools.total_ordering
class Edge:
    v: VertName
    w: VertName
    weight: Weight

    def __init__(self, v: VertName, w: VertName, weight: Weight):
        self.v = v
        self.w = w
        self.weight = weight

    def __lt__(self, other):
        return self.v < other.v or self.w < other.w or self.weight < other.weight

    def __eq__(self, other):
        return self.v == other.v and self.w == other.w and self.weight == other.weight

    @classmethod
    def from_edge(cls, e: 'Edge'):
        return cls(e.v, e.w, e.weight)


class WeightedDynamicGraph:
    """ An adjacency list multigraph with named verts which can add verts. """

    _directed: bool
    _verts: Dict[VertName, List[Edge]]
    _num_edges: int

    def __init__(self, directed: bool) -> None:
        self._directed = directed
        self._verts = {}
        self._num_edges = 0

    def is_directed(self) -> bool:
        return self._directed

    def set_is_directed(self) -> None:
        if not self._directed:
            self._directed = True
            self._num_edges *= 2
            to_add = []
            for v in self._verts:
                for edge in self.get_adjacent(v):
                    if edge.w == v:
                        to_add.append(edge)
            for edge in to_add:
                self._verts[edge.v].append(Edge.from_edge(edge))

    def num_verts(self) -> int:
        return len(self._verts)

    def _assure_vert(self, v: VertName) -> None:
        if v not in self._verts:
            self._verts[v] = []

    def add_vert(self, v) -> None:
        self._assure_vert(v)

    def get_verts(self) -> Iterable[VertName]:
        return self._verts.keys()

    def num_edges(self) -> int:
        return self._num_edges

    def has_edge(self, e: Edge) -> bool:
        for edge in self.get_adjacent(e.v):
            if edge == e:
                return True
        return False

    def has_edge_ignoring_weight(self, v: VertName, w: VertName) -> bool:
        for edge in self.get_adjacent(v):
            if edge.w == w:
                return True
        return False

    def get_edge(self, v: VertName, w: VertName) -> Union[Edge, None]:
        for edge in self.get_adjacent(v):
            if edge.w == w:
                if not self.is_directed():
                    edge = Edge(min(v, w), max(v, w), edge.weight)
                return edge
        return None

    def get_edges(self) -> List[Edge]:
        edges = []
        for v in self._verts:
            for e in self.get_adjacent(v):
                if self.is_directed() or e.v <= e.w:
                    edges.append(Edge.from_edge(e))
        return edges

    def insert_edge(self, edge: Edge) -> None:
        self._assure_vert(edge.v)
        self._assure_vert(edge.w)
        self._verts[edge.v].append(Edge.from_edge(edge))
        if not self.is_directed() and edge.v != edge.w:
            self._verts[edge.w].append(Edge(edge.w, edge.v, edge.weight))
        self._num_edges += 1

    def add_edges_from_array(self, arr: List[List[Union[VertName, Weight]]]) -> None:
        for edge in arr:
            self.insert_edge(Edge(edge[0], edge[1], edge[2]))

    def add_edges_from_array_default_weight(self, arr: List[List[VertName]]):
        for edge in arr:
            self.insert_edge(Edge(edge[0], edge[1], 1.0))

    def remove_edge(self, edge: Edge) -> None:
        if edge in self.get_adjacent(edge.v):
            self._verts[edge.v].remove(edge)
            if not self.is_directed() and edge.v != edge.w:
                self._verts[edge.w].remove(Edge(edge.w, edge.v, edge.weight))
            self._num_edges -= 1

    def get_adjacent(self, v: VertName) -> List[Edge]:
        return self._verts[v]

    def get_adjacent_verts(self, v: VertName) -> List[VertName]:
        return [e.w for e in self.get_adjacent(v)]

    def has_self_loops(self) -> bool:
        for v in self.get_verts():
            for e in self.get_adjacent(v):
                if e.v == e.w:
                    return True
        return False


class DigraphTransitiveClosure:
    """
    Uses Warshall's algorithm to generate an adjacency matrix graph for the kernel dag
    of a digraph to answer reachability queries.
    """

    digraph: WeightedDynamicGraph
    kernel_dag: DenseGraph
    kernel_dag_closure: DenseGraph
    vert_to_component_map: Dict[VertName, int]

    def __init__(self, graph: WeightedDynamicGraph) -> None:
        self.digraph = graph
        self.kernel_dag, self.vert_to_component_map = find_kernel_dag_for_digraph(self.digraph)
        self.kernel_dag_closure = self._compute_transitive_closure()

    def _compute_transitive_closure(self) -> DenseGraph:
        graph = deepcopy(self.kernel_dag)
        for v in range(graph.num_verts()):
            graph.insert_edge((v, v))
        for i in range(graph.num_verts()):
            for s in range(graph.num_verts()):
                if graph.has_edge((s, i)):
                    for t in range(graph.num_verts()):
                        if graph.has_edge((i, t)):
                            graph.insert_edge((s, t))
        return graph

    def reachable(self, v: VertName, w: VertName) -> bool:
        cv = self.vert_to_component_map[v]
        cw = self.vert_to_component_map[w]
        if cv == cw:
            return True
        else:
            return self.kernel_dag_closure.has_edge((cv, cw))


def create_random_graph_helper(graph: WeightedDynamicGraph, multigraph: bool,
                               self_loops: bool, num_verts: int) -> None:
    # ensure at least one
    if self_loops:
        v = random.randint(0, num_verts - 1)
        weight = random.uniform(0, 1)
        graph.insert_edge(Edge(v, v, weight))

    if multigraph:
        v = w = 0
        while v == w:
            v = random.randint(0, num_verts - 1)
            w = random.randint(0, num_verts - 1)
        weight = random.uniform(0, 1)
        graph.insert_edge(Edge(v, w, weight))
        graph.insert_edge(Edge(v, w, weight))


def create_random_dense_graph(num_verts: int, num_edges: int,
                              directed: bool, multigraph: bool, self_loops: bool
                              ) -> WeightedDynamicGraph:
    graph = WeightedDynamicGraph(directed)
    for v in range(num_verts):
        graph.add_vert(v)

    create_random_graph_helper(graph, multigraph, self_loops, num_verts)

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
                    weight = random.uniform(0, 1)
                    if directed and random.randint(0, 1) == 1:
                        if multigraph or not graph.has_edge_ignoring_weight(v, w):
                            graph.insert_edge(Edge(v, w, weight))
                    else:
                        if multigraph or not graph.has_edge_ignoring_weight(w, v):
                            graph.insert_edge(Edge(w, v, weight))
                if graph.num_edges() == num_edges:
                    break
            if graph.num_edges() == num_edges:
                break
    return graph


def create_random_k_neighbor_graph(k: int, num_verts: int, num_edges: int,
                                   directed: bool, multigraph: bool, self_loops: bool
                                   ) -> WeightedDynamicGraph:
    graph = WeightedDynamicGraph(directed)
    for v in range(num_verts):
        graph.add_vert(v)

    # ensure at least one
    if self_loops:
        v = random.randint(0, num_verts - 1)
        weight = random.uniform(0, 1)
        graph.insert_edge(Edge(v, v, weight))
    if multigraph:
        v = random.randint(0, num_verts - 1)
        w = (v + k) % num_verts
        weight = random.uniform(0, 1)
        graph.insert_edge(Edge(v, w, weight))
        graph.insert_edge(Edge(v, w, weight))

    probability = num_edges / (num_verts * (2 * k))
    if not directed:
        probability *= 2
    while graph.num_edges() < num_edges:
        for v in range(num_verts):
            for x in range(v - k, v + k + 1):
                w = (x + num_verts) % num_verts
                p = random.random()
                if p < probability and (self_loops or w != v):
                    weight = random.uniform(0, 1)
                    if directed and random.randint(0, 1) == 1:
                        if multigraph or not graph.has_edge_ignoring_weight(v, w):
                            graph.insert_edge(Edge(v, w, weight))
                    else:
                        if multigraph or not graph.has_edge_ignoring_weight(w, v):
                            graph.insert_edge(Edge(w, v, weight))
                if graph.num_edges() == num_edges:
                    break
            if graph.num_edges() == num_edges:
                break
    return graph


def create_random_sparse_graph(num_verts: int, num_edges: int,
                               directed: bool, multigraph: bool, self_loops: bool
                               ) -> WeightedDynamicGraph:
    graph = WeightedDynamicGraph(directed)
    for v in range(num_verts):
        graph.add_vert(v)

    create_random_graph_helper(graph, multigraph, self_loops, num_verts)

    while graph.num_edges() < num_edges:
        v = random.randint(0, num_verts - 1)
        w = random.randint(0, num_verts - 1)
        if (self_loops or w != v) and (
                multigraph or not graph.has_edge_ignoring_weight(v, w)):
            weight = random.uniform(0, 1)
            graph.insert_edge(Edge(v, w, weight))
    return graph


def path_from_dfs(graph: WeightedDynamicGraph, a: VertName, b: VertName) -> str:
    visited = set()
    path = []

    def search(u: VertName) -> bool:
        path.append(u)
        visited.add(u)
        if u == b and len(path) > 1:
            return True
        else:
            neighbors = graph.get_adjacent_verts(u)
            for t in neighbors:
                if t not in visited or t == b:
                    if search(t):
                        return True
        path.pop()
        return False

    if a == b and a in graph.get_adjacent_verts(a):
        path.extend([b, b])
    else:
        search(a)

    path_str = ""
    if path:
        path_str = "-".join([str(vert) for vert in path])

    return path_str


def path_from_bfs(graph: WeightedDynamicGraph, a: VertName, b: VertName) -> str:
    visited = set()
    parent = {v: -1 for v in graph.get_verts()}
    unprocessed = deque()
    is_cycle = (a == b)

    def search(edge):
        parent[edge[1]] = edge[0]
        if edge[1] == b and edge[0] != -1:
            return True
        visited.add(edge[1])
        neighbors = graph.get_adjacent_verts(edge[1])
        for t in neighbors:
            if t not in visited or t == b:
                unprocessed.appendleft((edge[1], t))
        return False

    if is_cycle and a in graph.get_adjacent_verts(a):
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


def is_multigraph(graph: WeightedDynamicGraph) -> bool:
    for v in graph.get_verts():
        seen = set()
        for e in graph.get_adjacent(v):
            if (e.v, e.w) in seen:
                return True
            else:
                seen.add((e.v, e.w))
    return False


def print_weighted_graph(graph: WeightedDynamicGraph):
    print(f"directed: {graph.is_directed()}")
    print(f"is dag: {is_dag(graph)}")
    print(f"has self-loops: {graph.has_self_loops()}")
    print(f"is multigraph: {is_multigraph(graph)}")
    print(f"num verts: {graph.num_verts()}")
    print(f"num edges: {graph.num_edges()}")
    for v in sorted(graph.get_verts()):
        print(f"{v}: ", end="")
        for e in sorted(list(graph.get_adjacent(v))):
            print(f"({e.w} : {e.weight})", end=" ")
        print()


def classify_and_print_edges(graph: WeightedDynamicGraph):
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

            for t in sorted(graph.get_adjacent_verts(u)):
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

            for t in sorted(graph.get_adjacent_verts(v)):
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


def is_dag(graph: WeightedDynamicGraph) -> bool:
    if not graph.is_directed():
        return False

    pre = {v: False for v in graph.get_verts()}
    post = {v: False for v in graph.get_verts()}
    dag = True

    def directed_dfs(v: VertName) -> None:
        nonlocal dag

        pre[v] = True

        for t in graph.get_adjacent_verts(v):
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


def convert_to_dag(graph: WeightedDynamicGraph):
    graph.set_is_directed()

    pre = {v: False for v in graph.get_verts()}
    post = {v: False for v in graph.get_verts()}
    edges_to_remove = []

    def directed_dfs(v):

        pre[v] = True

        for e in graph.get_adjacent(v):
            t = e.w
            if not pre[t]:
                directed_dfs(t)
            elif t == v:
                edges_to_remove.append(e)  # self-loop
            elif not post[t]:
                edges_to_remove.append(e)  # back edge

        post[v] = True

    for v in graph.get_verts():
        if not pre[v]:
            directed_dfs(v)

    for edge in edges_to_remove:
        graph.remove_edge(edge)


def create_reversed_graph(graph: WeightedDynamicGraph) -> Union[WeightedDynamicGraph, None]:
    if not graph.is_directed():
        return None

    rev = WeightedDynamicGraph(directed=True)
    for edge in graph.get_edges():
        rev.insert_edge(Edge(edge.w, edge.v, edge.weight))
    return rev


def topological_sort_dag(graph: WeightedDynamicGraph) -> Union[List[VertName], None]:
    if not graph.is_directed():
        return None

    pre = {v: False for v in graph.get_verts()}
    post = {v: False for v in graph.get_verts()}
    reverse_topo = []
    is_a_dag = True

    def dfs(v):
        nonlocal is_a_dag

        pre[v] = True
        for t in graph.get_adjacent_verts(v):
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


def strong_components_kosaraju(graph: WeightedDynamicGraph):
    """
    Given a digraph, computes the strongly-connected components. Returns:
    component_count (num strong components)
    vert_to_component_map
    components (list of vertices belonging to each component)
    """
    if not graph.is_directed:
        return None, None, None

    rev = create_reversed_graph(graph)
    vert_to_component_map = {v: -1 for v in rev.get_verts()}
    component_count = 0
    post_id = {v: -1 for v in rev.get_verts()}
    post_count = 0

    def dfs(w, dfs_graph):
        nonlocal post_count

        vert_to_component_map[w] = component_count
        for t in dfs_graph.get_adjacent_verts(w):
            if vert_to_component_map[t] == -1:
                dfs(t, dfs_graph)
        post_id[post_count] = w
        post_count += 1

    for v in rev.get_verts():
        if vert_to_component_map[v] == -1:
            dfs(v, rev)
    rev_post_id = copy(post_id)

    vert_to_component_map = {v: -1 for v in rev.get_verts()}
    component_count = 0
    post_count = 0
    for n in range(graph.num_verts() - 1, -1, -1):
        v = rev_post_id[n]
        if vert_to_component_map[v] == -1:
            dfs(v, graph)
            component_count += 1

    components = [[] for _ in range(component_count)]
    for v, i in vert_to_component_map.items():
        components[i].append(v)
    for component in components:
        component.sort()
    components.sort()

    return component_count, vert_to_component_map, components


def find_kernel_dag_for_digraph(graph: WeightedDynamicGraph):
    num_components, vert_to_component_map, strong_components = \
        strong_components_kosaraju(graph)
    if not num_components:
        return None, None

    kernel_dag = DenseGraph(num_components, directed=True)
    for edge in graph.get_edges():
        v = vert_to_component_map[edge.v]
        w = vert_to_component_map[edge.w]
        if v != w:
            kernel_dag.insert_edge((v, w))
    return kernel_dag, vert_to_component_map


def prims_algorithm_for_minimal_spanning_tree(graph: WeightedDynamicGraph
                                              ) -> (Weight, List[Edge]):
    """
    Prim's algorithm for a minimal spanning tree.
    Requires graph vertices are numbers 0 to V-1.
    Inefficient for sparse graphs.
    """

    n = graph.num_verts()
    weights = [float("inf")] * n
    mst: List[Optional[Edge]] = [None] * n
    frontier: List[Optional[Edge]] = [None] * n
    min_vert = -1
    v = 0

    while min_vert != 0:
        min_vert = 0
        for w in range(1, n):
            if mst[w] is None:
                e = graph.get_edge(v, w)
                if e:
                    if e.weight < weights[w]:
                        weights[w] = e.weight
                        frontier[w] = e
                if weights[w] < weights[min_vert]:
                    min_vert = w

        if min_vert:
            mst[min_vert] = frontier[min_vert]
        v = min_vert

    return sum([mst[i].weight for i in range(1, n)]), mst[1:]
