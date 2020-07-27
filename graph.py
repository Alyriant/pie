import queue

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
            
    def addEdgesFromLists(self, edges):
        for e in edges:
            weight = e[2] if self.weighted else None
            self.addEdge(Edge(e[0], e[1], weight))
            
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
    
    def breadthFirstTraversal(self, start):
        """Find the paths and distances of other nodes from the start node.
        Ignores path weights."""
        num = len(self.adjacency_map)
        KNOWN = False
        DIST = 1
        PATH = 2
        info = { v : list([False, -1, list()]) for v in self.adjacency_map.keys() }
        cur = info[start]
        cur[KNOWN] = True
        cur[DIST] = 0
        cur[PATH].append(start)
        
        q = queue.SimpleQueue()
        q.put(start)
        while not q.empty():
            cur = q.get()
            cur_info = info[cur]
            neighbors = self.adjacency_map[cur]
            for edge in neighbors:
                vert = edge.v2
                print(vert, info)
                i = info[vert]
                if not i[KNOWN]:
                    i[KNOWN] = True
                    i[DIST] = cur_info[DIST] + 1
                    i[PATH].extend(cur_info[PATH])
                    i[PATH].append(vert)
                    q.put(vert)
        
        for vert, val in info.items():
            print(f"To {vert} - path length: {val[DIST]}. Path: {val[PATH]}.")
        
        
    
if __name__ ==  "__main__":
    g = Graph()
    call = "g.addEdgesFromLists([[2,3], [3,4], [1,0], [1,2], [1,3]])"
    print(call)
    exec(call)
    print(g.findTopologicalOrdering())
    
    call = "g.addEdgesFromLists([[2,1]])"
    print(call)
    exec(call)
    print(g.findTopologicalOrdering())
    
    g = Graph()
    call = "g.addEdgesFromLists([[2,3], [3,4], [1,0], [1,2], [1,3]])"
    print(call)
    exec(call)
    call = 'g.breadthFirstTraversal(2)'
    print(call)
    exec(call)
    