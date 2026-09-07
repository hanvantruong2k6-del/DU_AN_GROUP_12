# -*- coding: utf-8 -*-
"""
euler.py
Thuat toan Fleury va Hierholzer tim chu trinh / duong di Euler.
Tu cai dat, khong dung thu vien do thi co san.
"""


def _degree_check_undirected(graph):
    """Dem so dinh bac le, kiem tra dieu kien ton tai duong/chu trinh Euler (vo huong)."""
    deg = [len(graph.adj[u]) for u in range(graph.n)]
    odd = [u for u in range(graph.n) if deg[u] % 2 == 1]
    return deg, odd


def has_eulerian(graph):
    """
    Tra ve ('circuit'|'path'|'none', danh sach dinh bac le)
    Chi ho tro day du cho do thi vo huong (pho bien trong bai tap).
    """
    # kiem tra do thi lien thong tren cac dinh co bac > 0
    nonzero = [u for u in range(graph.n) if len(graph.adj[u]) > 0]
    if nonzero:
        seen = set()
        stack = [nonzero[0]]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            for (v, w) in graph.adj[u]:
                if v not in seen:
                    stack.append(v)
        if any(u not in seen for u in nonzero):
            return "none", []

    deg, odd = _degree_check_undirected(graph)
    if len(odd) == 0:
        return "circuit", odd
    elif len(odd) == 2:
        return "path", odd
    else:
        return "none", odd


# ---------------------------------------------------------------------
# FLEURY'S ALGORITHM
# ---------------------------------------------------------------------
def _count_reachable(adj_copy, u, n):
    visited = [False] * n
    stack = [u]
    cnt = 0
    while stack:
        x = stack.pop()
        if visited[x]:
            continue
        visited[x] = True
        cnt += 1
        for (v, w, eid) in adj_copy[x]:
            if not visited[v]:
                stack.append(v)
    return cnt


def _is_bridge(adj_copy, u, v, eid, n):
    """Canh (u,v,eid) co phai la cau khong: so dinh reachable truoc/sau khi xoa canh."""
    before = _count_reachable(adj_copy, u, n)
    # xoa canh (ca 2 chieu, vi ta luon luu vo huong o day)
    removed = []
    for lst, x, other in [(adj_copy[u], u, v), (adj_copy[v], v, u)]:
        for item in lst:
            if item[0] == other and item[2] == eid:
                lst.remove(item)
                removed.append((x, item))
                break
    after = _count_reachable(adj_copy, u, n)
    # phuc hoi
    for x, item in removed:
        adj_copy[x].append(item)
    return after < before


def fleury(graph, start=None, verbose=False):
    """
    Thuat toan Fleury tim chu trinh/duong di Euler tren do thi vo huong.
    Nguyen tac: tai moi buoc, chi di qua canh la cau (bridge) khi khong con
    lua chon nao khac.
    Tra ve: danh sach dinh theo duong di Euler (hoac [] neu khong ton tai).
    """
    status, odd = has_eulerian(graph)
    if status == "none":
        return []

    if start is None:
        start = odd[0] if status == "path" else 0

    # adjacency co danh so id cho tung canh de xu ly multi-edge / xoa dung canh
    adj_copy = {u: [] for u in range(graph.n)}
    for eid, (u, v, w) in enumerate(graph.edge_list):
        adj_copy[u].append((v, w, eid))
        adj_copy[v].append((u, w, eid))

    total_edges = len(graph.edge_list)
    path = [start]
    u = start
    for step in range(total_edges):
        if not adj_copy[u]:
            break
        # chon canh khong phai cau, neu chi con 1 lua chon thi bat buoc di
        chosen = None
        if len(adj_copy[u]) == 1:
            chosen = adj_copy[u][0]
        else:
            for cand in adj_copy[u]:
                v, w, eid = cand
                if not _is_bridge(adj_copy, u, v, eid, graph.n):
                    chosen = cand
                    break
            if chosen is None:
                chosen = adj_copy[u][0]  # bat dac di qua cau

        v, w, eid = chosen
        if verbose:
            print(f"  Buoc {step+1}: di tu {graph.labels[u]} -> {graph.labels[v]} (canh #{eid})")
        # xoa canh khoi ca 2 phia
        adj_copy[u] = [it for it in adj_copy[u] if it[2] != eid]
        adj_copy[v] = [it for it in adj_copy[v] if it[2] != eid]
        path.append(v)
        u = v

    return path


# ---------------------------------------------------------------------
# HIERHOLZER'S ALGORITHM
# ---------------------------------------------------------------------
def hierholzer(graph, start=None, verbose=False):
    """
    Thuat toan Hierholzer tim chu trinh/duong di Euler - hieu qua O(E).
    Dung stack, ghep cac chu trinh con lai voi nhau.
    """
    status, odd = has_eulerian(graph)
    if status == "none":
        return []

    if start is None:
        start = odd[0] if status == "path" else 0

    adj_copy = {u: [] for u in range(graph.n)}
    for eid, (u, v, w) in enumerate(graph.edge_list):
        adj_copy[u].append([v, eid])
        adj_copy[v].append([u, eid])

    used = [False] * len(graph.edge_list)
    stack = [start]
    circuit = []

    while stack:
        u = stack[-1]
        # tim canh chua dung tu u
        found = False
        while adj_copy[u]:
            v, eid = adj_copy[u][-1]
            adj_copy[u].pop()
            if used[eid]:
                continue
            used[eid] = True
            stack.append(v)
            found = True
            if verbose:
                print(f"  Day vao stack: {graph.labels[v]} (qua canh #{eid})")
            break
        if not found:
            circuit.append(stack.pop())

    circuit.reverse()
    return circuit
