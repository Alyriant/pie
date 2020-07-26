
class ALGraph:
    """adjacency_list graph"""

    def __init__(self):
        self.adjacency_list = {}
        
    def addEdges(self, edges):
        for edge in edges:
            self.addVerts(edge)
            v1, v2 = edge
            self.adjacency_list[v1].add(v2)
            
    def addVerts(self, verts):
        for vert in verts:
            if self.adjacency_list.get(vert) is None:
                self.adjacency_list[vert] = set()
    
    def findTopologicalOrdering(self):
        indegree = {}
        for vert in self.adjacency_list.keys():
            indegree[vert] = 0
        for verts in self.adjacency_list.values():
            for vert in verts:
                indegree[vert] += 1
        order = []
        while indegree:
            for v1 in indegree:
                #print(v1, indegree)
                if indegree[v1] == 0:
                    order.append(v1)
                    indegree.pop(v1)
                    for v2 in self.adjacency_list[v1]:
                        indegree[v2] -= 1
                    break
        return order
    
    
if __name__ ==  "__main__":
    g = ALGraph()
    g.addEdges([[2,3], [3,4], [1,0], [1,2], [1,3]])
    print(g.adjacency_list)
    print(g.findTopologicalOrdering())