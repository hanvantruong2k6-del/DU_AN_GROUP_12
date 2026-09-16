"""
BFS va DFS tu xay dung (tu cai queue/stack bang list).
"""


def bfs(graph, start):
    """Duyet do thi theo chieu rong tu dinh 'start'. Tra ve thu tu duyet va cay BFS (parent)."""
    visited = [False] * graph.n
    parent = [-1] * graph.n
    order = []

    queue = [start]
    visited[start] = True
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        order.append(u)
        # duyet cac dinh ke theo thu tu tang dan de ket qua on dinh, de doi chieu bang tay
        for (v, w) in sorted(graph.adj[u], key=lambda x: x[0]):
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.append(v)
    return order, parent


def dfs(graph, start):
    """Duyet do thi theo chieu sau tu dinh 'start' (dung stack tu cai, khong de quy)."""
    visited = [False] * graph.n
    parent = [-1] * graph.n
    order = []

    stack = [start]
    while stack:
        u = stack.pop()
        if visited[u]:
            continue
        visited[u] = True
        order.append(u)
        # day cac dinh ke theo thu tu giam dan vao stack de khi pop ra dung thu tu tang dan
        for (v, w) in sorted(graph.adj[u], key=lambda x: x[0], reverse=True):
            if not visited[v]:
                stack.append(v)
                if parent[v] == -1:
                    parent[v] = u
    return order, parent


def dfs_recursive(graph, start):
    """Ban de quy cua DFS, dung de doi chieu / giai thich them."""
    visited = [False] * graph.n
    parent = [-1] * graph.n
    order = []

    def visit(u):
        visited[u] = True
        order.append(u)
        for (v, w) in sorted(graph.adj[u], key=lambda x: x[0]):
            if not visited[v]:
                parent[v] = u
                visit(v)

    visit(start)
    return order, parent
