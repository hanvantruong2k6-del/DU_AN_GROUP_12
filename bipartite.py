
"""
Kiem tra do thi hai phia (bipartite) bang thuat toan to mau 2 mau (BFS).
Ap dung chuan cho do thi vo huong; voi do thi co huong, ta xet do thi
nen vo huong tuong ung (bo qua chieu canh) vi tinh "hai phia" la khai
niem cua do thi vo huong.
"""


def is_bipartite(graph):
    color = [-1] * graph.n
    parts = ([], [])

    # xay dung ke vo huong (gop ca chieu nguoc neu do thi co huong)
    undirected_adj = {i: set() for i in range(graph.n)}
    for u in range(graph.n):
        for (v, w) in graph.adj[u]:
            undirected_adj[u].add(v)
            undirected_adj[v].add(u)

    for s in range(graph.n):
        if color[s] != -1:
            continue
        color[s] = 0
        parts[0].append(s)
        queue = [s]
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            for v in undirected_adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    parts[color[v]].append(v)
                    queue.append(v)
                elif color[v] == color[u]:
                    return False, None, None
    return True, parts[0], parts[1]
