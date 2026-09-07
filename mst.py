# -*- coding: utf-8 -*-
"""
mst.py
Thuat toan Prim va Kruskal tim cay khung nho nhat (Minimum Spanning Tree).
Tu cai dat: Union-Find (Kruskal) va chon min tuyen tinh (Prim), khong dung
thu vien do thi/heapq co san.
"""

INF = float("inf")


class DisjointSet:
    """Cau truc Union-Find tu xay dung, co path compression + union by rank."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def prim(graph, start=0, verbose=False):
    """
    Prim: chi ap dung cho do thi vo huong, lien thong.
    Tra ve: danh sach canh (u, v, w) cua MST, va tong trong so.
    """
    in_mst = [False] * graph.n
    key = [INF] * graph.n
    parent = [-1] * graph.n
    key[start] = 0

    mst_edges = []
    total = 0

    for step in range(graph.n):
        u, best = -1, INF
        for i in range(graph.n):
            if not in_mst[i] and key[i] < best:
                best, u = key[i], i
        if u == -1:
            break  # do thi khong lien thong
        in_mst[u] = True
        if parent[u] != -1:
            mst_edges.append((parent[u], u, key[u]))
            total += key[u]
            if verbose:
                print(f"  Buoc {step}: them canh ({graph.labels[parent[u]]}-{graph.labels[u]}), w={key[u]}")
        for (v, w) in graph.adj[u]:
            if not in_mst[v] and w < key[v]:
                key[v] = w
                parent[v] = u

    return mst_edges, total


def kruskal(graph, verbose=False):
    """
    Kruskal: sap xep canh tang dan theo trong so, dung Union-Find de tranh chu trinh.
    Tra ve: danh sach canh (u, v, w) cua MST, va tong trong so.
    """
    edges = sorted(graph.edge_list, key=lambda e: e[2])
    ds = DisjointSet(graph.n)
    mst_edges = []
    total = 0

    for (u, v, w) in edges:
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            mst_edges.append((u, v, w))
            total += w
            if verbose:
                print(f"  Chon canh ({graph.labels[u]}-{graph.labels[v]}), w={w}")
        else:
            if verbose:
                print(f"  Bo qua canh ({graph.labels[u]}-{graph.labels[v]}), w={w} -> tao chu trinh")
        if len(mst_edges) == graph.n - 1:
            break

    return mst_edges, total
