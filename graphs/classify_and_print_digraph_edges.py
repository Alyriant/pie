from graphs.graph import *


class ClassifyAndPrintDigraphEdges:

    def __init__(self, graph):
        self._graph = graph
        self._depth = 0
        self._pre = [-1] * graph.num_verts()
        self._post = [-1] * graph.num_verts()
        self._pre_count = 0
        self._post_count = 0
        self._top_level()

    def _top_level(self):
        for v in range(self._graph.num_verts()):
            if self._pre[v] == -1:
                self._dfs(v, v)

    def _dfs(self, w, parent):
        self._pre[w] = self._pre_count
        self._pre_count += 1
        self._print_level(parent, w, "tree")
        self._depth += 1
        adj = self._graph.get_adj_iter(w)
        for t in adj:
            if self._pre[t] == -1:
                self._dfs(t, w)
            elif self._post[t] == -1:
                self._print_level(w, t, "back")
            elif self._pre[t] > self._pre[w]:
                self._print_level(w, t, "down")
            else:
                self._print_level(w, t, "cross")
        self._depth -= 1
        self._post[w] = self._post_count
        self._post_count += 1

    def _print_level(self, v, w, type_):
        print(' ' * self._depth, end='')
        print(f"{v}-{w}: {type_}   (pre {self._pre[v]}/{self._pre[w]}, post {self._post[v]}/{self._post[w]})")


def classify_and_print_digraph_edges():
    graph = AdjSetGraph(13, directed=True)
    graph.add_edges_from_array(
        [[0, 1], [0, 5], [0, 6], [2, 0], [2, 3], [3, 2], [3, 5], [4, 2], [4, 3], [4, 11], [5, 4], [6, 4], [6, 9],
         [7, 6], [7, 8], [8, 7], [8, 9], [9, 10], [9, 11], [10, 12], [11, 12], [12, 9]])
    print_graph(graph)
    ClassifyAndPrintDigraphEdges(graph)


if __name__=="__main__":
    classify_and_print_digraph_edges()
