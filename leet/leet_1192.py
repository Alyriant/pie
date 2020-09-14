class Solution:
    def criticalConnections(self, n, connections): # List[List[int]]) -> List[List[int]]:
        found_critical = []
        verts = [list() for _ in range(n)]

        # create adj list graph
        for c in connections:
            u = c[0]
            v = c[1]
            verts[u].append(v)
            verts[v].append(u)

        # process the graph
        order = [-1] * n
        low = [-1] * n
        self.count = 0

        def dfs(vert, parent):
            order[vert] = self.count
            low[vert] = self.count
            self.count += 1
            adj = verts[vert]
            for t in adj:
                if order[t] == -1:
                    dfs(t, vert)
                    if low[vert] > low[t]:
                        low[vert] = low[t]
                    if low[t] == order[t]:
                        found_critical.append([vert, t])
                elif t != parent:
                    if low[vert] > order[t]:
                        low[vert] = order[t]

        for vert in range(n):
            if order[vert] == -1:
                dfs(vert, vert)

        return found_critical


if __name__ == "__main__":
    edges = [[0, 1]]
    print(Solution().criticalConnections(2, edges))
    edges = [[0, 1], [1, 2]]
    print(Solution().criticalConnections(3, edges))
    edges = [[0, 1], [1, 2], [2, 0], [1, 3]]
    print(Solution().criticalConnections(4, edges))