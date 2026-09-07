# -*- coding: utf-8 -*-
"""
shortest_path.py
Dijkstra va Bellman-Ford tu xay dung tu dau (khong dung heapq, khong dung
thu vien do thi co san). Dijkstra dung "min tuyen tinh" O(V^2), phu hop de
sinh vien doi chieu voi ket qua chay tay tung buoc (co in ra tung vong lap).
"""

INF = float("inf")


def dijkstra(graph, src, dst=None, verbose=False):
    """
    Yeu cau: trong so khong am.
    Tra ve: dist[], parent[]
    """
    dist = [INF] * graph.n
    parent = [-1] * graph.n
    visited = [False] * graph.n
    dist[src] = 0

    for step in range(graph.n):
        # tim dinh u chua tham voi dist nho nhat (O(V) - "min tuyen tinh")
        u, best = -1, INF
        for i in range(graph.n):
            if not visited[i] and dist[i] < best:
                best, u = dist[i], i
        if u == -1:
            break
        visited[u] = True
        if verbose:
            print(f"  Buoc {step+1}: chon dinh {graph.labels[u]} voi dist={dist[u]}")
        for (v, w) in graph.adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                if verbose:
                    print(f"      cap nhat dist[{graph.labels[v]}] = {dist[v]} (qua {graph.labels[u]})")
    return dist, parent


def bellman_ford(graph, src, dst=None, verbose=False):
    """
    Cho phep trong so am (khong co chu trinh am). Phat hien chu trinh am.
    Tra ve: dist[], parent[], has_negative_cycle(bool)
    """
    dist = [INF] * graph.n
    parent = [-1] * graph.n
    dist[src] = 0

    edges = graph.edge_list
    # neu do thi vo huong, moi canh (u,v,w) coi nhu 2 canh co huong u->v va v->u
    directed_edges = []
    for (u, v, w) in edges:
        directed_edges.append((u, v, w))
        if not graph.directed:
            directed_edges.append((v, u, w))

    for it in range(graph.n - 1):
        changed = False
        for (u, v, w) in directed_edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if verbose:
            print(f"  Vong lap {it+1}: dist = {dist}")
        if not changed:
            break

    has_negative_cycle = False
    for (u, v, w) in directed_edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, parent, has_negative_cycle


def reconstruct_path(parent, src, dst):
    if parent[dst] == -1 and src != dst:
        return []
    path = [dst]
    while path[-1] != src:
        p = parent[path[-1]]
        if p == -1:
            return []
        path.append(p)
    path.reverse()
    return path
