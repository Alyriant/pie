class Graph:
    """ Graph based on Sedgewick, 17.1 """

    def __init__(self, num_verts, directed):
        self.num_verts = num_verts
        self.directed = directed
        self.num_edges = 0
        self.verts = [list() for _ in range(num_verts)]
    
    def num_verts(self):
        return self.num_verts
        
    def num_edges(self):
        return self.num_edges
    
    def insert_edge(self, edge):
        self.verts[edge.v].append(edge.w)
        self.num_edges += 1
    
    def remove_edge(self, edge):
        self.verts[v].remove(w)
        self.num_edges -= 1
        
    def get_adj_iter(self, v):
        return self.verts[v]
        
    def is_directed(self):
        return self.directed
        
#class AdjacencyIterator:
#
#    def __init__(self):
#        pass
#    
#    def __iter__(self):
#        return self
#    
#    def __next__(self):
#        pass
        
class Edge:

    def __init__(self, v, w):
        self.v = v
        self.w = w

class GraphUtilities:    

    def get_edges(graph):
        """ Sedgewick 17.2 """

        edges = []
        for v in range(graph.num_verts):
            for w in graph.get_adj_iter(v):
                if graph.is_directed() or v < w:
                    edges.append(Edge(v, w))
        return edges

class GraphIO:
    """ Sedgewick 17.4 """

    def print_graph(self, graph):
        """ Sedgewick 17.3 """

        for v in range(graph.num_verts):
            print(v, ":", end=" ")
            w = list(graph.get_adj_iter(v))
            print(w)

    def scan_verts(self, graph, lines):
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
        
class GraphConnectedComponents:
    """ Sedgewick 17.5 """

    def __init__(self, graph):
        pass
    
    def component_count(self):
        pass
    
    def are_connected(self, v, w):
        pass
        
class DriverExample:
    """ Sedgewick 17.6 """

    def main(self):
        with open('DriverExample.txt') as f: 
            lines = f.readlines()
            num_verts = int(lines[0])
            print(num_verts, "vertices")
            graph = Graph(num_verts, directed=False)
            io = GraphIO()
            io.scan_verts(graph, lines[1:])
            if num_verts < 20:
                io.print_graph(graph)
            print(graph.num_edges, "edges")
            cc = GraphConnectedComponents(graph)
            print(cc.component_count(), "components")
    
if __name__ == "__main__":
    DriverExample().main()