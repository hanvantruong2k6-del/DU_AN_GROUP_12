# -*- coding: utf-8 -*-
"""
 - Do thi vo huong / co huong
 - Do thi co trong so / khong trong so
 - Chuyen doi qua lai: Adjacency Matrix <-> Adjacency List <-> Edge List
 - Doc du lieu tu file text 
"""

INF = float("inf")


class Graph:
    def __init__(self, num_nodes, directed=False, weighted=False, labels=None):
        self.n = num_nodes
        self.directed = directed
        self.weighted = weighted
        # nhan (ten) cua tung dinh, mac dinh la 0..n-1
        self.labels = labels if labels else [str(i) for i in range(num_nodes)]
        # adjacency list: adj[u] = list of (v, w)
        self.adj = {i: [] for i in range(num_nodes)}
        # danh sach canh (u, v, w) - moi canh luu 1 lan (ke ca do thi vo huong)
        self.edge_list = []

    # Xay dung do thi

    def add_edge(self, u, v, w=1):
        if u < 0 or u >= self.n or v < 0 or v >= self.n:
            raise ValueError(f"Dinh khong hop le: ({u},{v})")
        self.adj[u].append((v, w))
        self.edge_list.append((u, v, w))
        if not self.directed and u != v:
            self.adj[v].append((u, w))

    @staticmethod
    def from_file(path):
        """
        Dinh dang file dau vao (khong co dong trong o giua, # de comment):
        n_dinh
        directed|undirected
        weighted|unweighted
        u1 v1 [w1]
        u2 v2 [w2]
        ...
        (co the co dong "labels: A B C D ..." de dat ten dinh, tuy chon)
        """
        with open(path, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

        idx = 0
        n = int(lines[idx]); idx += 1
        directed = lines[idx].lower().startswith("d"); idx += 1
        weighted = lines[idx].lower().startswith("w"); idx += 1

        labels = None
        if idx < len(lines) and lines[idx].lower().startswith("labels"):
            labels = lines[idx].split(":", 1)[1].split()
            idx += 1

        g = Graph(n, directed=directed, weighted=weighted, labels=labels)
        for ln in lines[idx:]:
            parts = ln.split()
            u, v = int(parts[0]), int(parts[1])
            w = float(parts[2]) if (weighted and len(parts) > 2) else 1
            g.add_edge(u, v, w)
        return g

    @staticmethod
    def from_manual_input():
        """Nhap do thi truc tiep tu ban phim (dung khi chay demo interactive)."""
        n = int(input("So dinh: "))
        directed = input("Do thi co huong? (y/n): ").strip().lower() == "y"
        weighted = input("Do thi co trong so? (y/n): ").strip().lower() == "y"
        m = int(input("So canh: "))
        g = Graph(n, directed=directed, weighted=weighted)
        print("Nhap tung canh theo dang: u v" + (" w" if weighted else "") + " (dinh danh so tu 0)")
        for _ in range(m):
            parts = input().split()
            u, v = int(parts[0]), int(parts[1])
            w = float(parts[2]) if (weighted and len(parts) > 2) else 1
            g.add_edge(u, v, w)
        return g


    # 3 cach bieu dien - chuyen doi qua lai
    def to_adjacency_matrix(self):
        mat = [[0 if self.weighted else 0 for _ in range(self.n)] for _ in range(self.n)]
        # dung 0 nghia la khong co canh; neu weighted va can phan biet, dung INF cho "khong co canh"
        mat = [[INF] * self.n for _ in range(self.n)] if self.weighted else [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            mat[i][i] = 0 if self.weighted else mat[i][i]
        for u in range(self.n):
            for (v, w) in self.adj[u]:
                mat[u][v] = w if self.weighted else 1
        return mat

    def to_adjacency_list(self):
        return {u: list(self.adj[u]) for u in range(self.n)}

    def to_edge_list(self):
        return list(self.edge_list)

    @staticmethod
    def from_adjacency_matrix(mat, directed=False, weighted=False, labels=None):
        n = len(mat)
        g = Graph(n, directed=directed, weighted=weighted, labels=labels)
        for i in range(n):
            jrange = range(n) if directed else range(i, n)
            for j in jrange:
                val = mat[i][j]
                has_edge = (val != 0) if not weighted else (val != INF and val is not None)
                if has_edge and not (i == j and val == 0):
                    if i == j and val == 0:
                        continue
                    g.add_edge(i, j, val if weighted else 1)
        return g

    @staticmethod
    def from_edge_list(n, edges, directed=False, weighted=False, labels=None):
        g = Graph(n, directed=directed, weighted=weighted, labels=labels)
        for e in edges:
            u, v = e[0], e[1]
            w = e[2] if (weighted and len(e) > 2) else 1
            g.add_edge(u, v, w)
        return g

    # In cac dang bieu dien ra man hinh

    def print_adjacency_matrix(self):
        mat = self.to_adjacency_matrix()
        header = "     " + " ".join(f"{self.labels[j]:>5}" for j in range(self.n))
        print(header)
        for i in range(self.n):
            row = []
            for j in range(self.n):
                val = mat[i][j]
                if self.weighted and val == INF:
                    row.append(f"{'INF':>5}")
                else:
                    row.append(f"{val:>5}")
            print(f"{self.labels[i]:>5}" + " ".join(row))

    def print_adjacency_list(self):
        for u in range(self.n):
            nbrs = ", ".join(
                f"{self.labels[v]}" + (f"(w={w})" if self.weighted else "")
                for v, w in self.adj[u]
            )
            print(f"{self.labels[u]}: [{nbrs}]")

    def print_edge_list(self):
        for (u, v, w) in self.edge_list:
            if self.weighted:
                print(f"({self.labels[u]} - {self.labels[v]}, w={w})")
            else:
                print(f"({self.labels[u]} - {self.labels[v]})")

    def __repr__(self):
        kind = "co huong" if self.directed else "vo huong"
        wk = "co trong so" if self.weighted else "khong trong so"
        return f"<Graph n={self.n}, {kind}, {wk}, |E|={len(self.edge_list)}>"
