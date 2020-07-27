class Edge:
    def __init__(self, v1, v2, weight=None):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight
            
class Graph:
    """adjacency_map graph"""
        
    def __init__(self, directed=True, weighted=False):
        self.adjacency_map = {}
        self.directed = directed
        self.weighted = weighted
    
    def addVert(self, vert):
        if self.adjacency_map.get(vert) is None:
            self.adjacency_map[vert] = set()
                
    def addVerts(self, verts):
        for vert in verts:
            self.addVert(vert)
    
    def addEdge(self, edge):
        self.addVert(edge.v1)
        self.addVert(edge.v2)
        self.adjacency_map[edge.v1].add(edge)
        if not self.directed:
            reverse = Edge(edge.v2, edge.v1, edge.weight)
            self.adjacency_map[edge.v2].add(reverse)
            
    def addEdges(self, edges):
        for edge in edges:
            self.addEdge(edge)
            
    def findTopologicalOrdering(self):
        indegree = {}
        for vert in self.adjacency_map.keys():
            indegree[vert] = 0
        for edges in self.adjacency_map.values():
            for edge in edges:
                indegree[edge.v2] += 1
        order = []
        queue = []
        for v1 in indegree:
            if indegree[v1] == 0:
                queue.append(v1)
        while queue:
            v1 = queue.pop()
            order.append(v1)
            indegree.pop(v1)
            for edge in self.adjacency_map[v1]:
                indegree[edge.v2] -= 1
                if indegree[edge.v2] == 0:
                    queue.append(edge.v2)
        if indegree:
            return ["cyclic graph, no topological ordering"]
        else:
            return order
    
    
if __name__ ==  "__main__":
    g = Graph()
    g.addEdges([Edge(2,3), Edge(3,4), Edge(1,0), Edge(1,2), Edge(1,3)])
    print(g.findTopologicalOrdering())
    
    g.addEdges([Edge(2,1)])
    print(g.findTopologicalOrdering())
    