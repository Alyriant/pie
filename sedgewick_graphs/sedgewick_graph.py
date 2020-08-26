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


class GraphIO:
    """ Sedgewick 17.4 """

    @staticmethod
    def print_graph(graph):
        """ Sedgewick 17.3 """

        print(f"directed: {graph.is_directed()}")
        print(f"num verts: {graph.num_verts()}")
        print(f"num edges: {graph.num_edges()}")
        for v in range(graph.num_verts()):
            print(v, ":", end=" ")
            w = sorted(list(graph.get_adj_iter(v)))
            print(w)

    @staticmethod
    def scan_verts(graph, lines):
        """ read lines of vert number pairs representing edges and add to the graph """
        for line in lines:
            v, w = line.split()
            v = int(v)
            w = int(w)
            graph.insert_edge(Edge(v, w))
            if not graph.is_directed():
                graph.insert_edge(Edge(w, v))
    
    def scan_symbols(self):
        pass

    @staticmethod
    def draw_graph(graph):
        win = GraphWin("My Circle", 1024, 1024)
        win.setCoords(-1.1, -1.1, 1.1, 1.1)

        angle = 2 * math.pi / graph.num_verts()
        id = list(range(graph.num_verts()))
        for vert in id:
            a = angle * vert
            c = Circle(Point(math.cos(a), math.sin(a)), 0.01)
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

    @staticmethod
    def create_random_sparse_graph(num_verts, num_edges, directed):
        """ Sedgewick 17.12 """
        graph = AdjSetGraph(num_verts, directed)
        while graph.num_edges() < num_edges:
            v = random.randint(0, num_verts-1)
            w = random.randint(0, num_verts-1)
            if v != w:
                graph.insert_edge(Edge(v, w))
        return graph

    @staticmethod
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


class GraphConnectedComponents:
    """ Sedgewick 17.5, 1.3, 1.4 """
    
    def __init__(self, graph):
        id = list(range(graph.num_verts()))
        edges = graph.get_edges()
        for edge in edges:
            i = edge.v
            j = edge.w
            while i != id[i]:
                id[i] = id[id[i]]
                i = id[i]
            while j != id[j]:
                id[j] = id[id[j]]
                j = id[j]
            if i != j:
                id[i] = j
        self.count = 0
        for i in range(graph.num_verts()):
            if i == id[i]:
                self.count += 1
        self.id = id
        
    def component_count(self):
        return self.count
        
    def are_connected(self, i, j):
        id = self.id
        while i != id[i]:
            id[i] = id[id[i]]
            i = id[i]
        while j != id[j]:
            id[j] = id[id[j]]
            j = id[j]
        return i == j


class DriverExample:
    """ Sedgewick 17.6 """

    @staticmethod
    def main():
        with open('DriverExample.txt') as f: 
            lines = f.readlines()
            num_verts = int(lines[0])
            print(num_verts, "vertices")
            graph = AdjListGraph(num_verts, directed=False)
            io = GraphIO()
            io.scan_verts(graph, lines[1:])
            if num_verts < 20:
                io.print_graph(graph)
            print(graph.num_edges(), "edges")
            cc = GraphConnectedComponents(graph)
            print(cc.component_count(), "components")
            print("0 connected to 1:", cc.are_connected(0, 1))
            print("1 connected to 5:", cc.are_connected(1, 5))

            io.draw_graph(graph)

    @staticmethod
    def random_sparse_graph():
        io = GraphIO()
        graph = io.create_random_sparse_graph(num_verts=30, num_edges=40, directed=True)
        io.draw_graph(graph)

    @staticmethod
    def random_dense_graph():
        io = GraphIO()
        graph = io.create_random_dense_graph(num_verts=10, approx_num_edges=40, directed=True)
        io.draw_graph(graph)
        io.print_graph(graph)


if __name__ == "__main__":
    ex = DriverExample()
    ex.main()
    ex.random_sparse_graph()
    ex.random_dense_graph()