"""
route_orchestrator.py
HAM DIEU PHOI (orchestrator): KET NOI 3 thuat toan lai voi nhau de xu ly
truong hop do thi KHONG THOA dieu kien Euler - day khong phai la 1 thuat
toan rieng biet cai dat tu dau, ma la ham "nhac truong" goi lai 2 thuat
toan da co (Dijkstra, Hierholzer) va chen them 1 buoc logic moi (ghep cap
trong so nho nhat) de noi chung lai thanh 1 quy trinh hoan chinh:
  (1) DIJKSTRA          - TAI SU DUNG ham dijkstra() da cai o shortest_path.py,
                          tinh khoang cach duong di ngan nhat giua cac dinh bac le
  (2) GHEP CAP TRONG SO NHO NHAT (backtracking do nhom tu thiet ke - phan
                          MOI duy nhat trong file nay, chua co o dau khac)
                        - ghep cac dinh bac le thanh cap sao cho tong khoang
                          cach nho nhat
  (3) HIERHOLZER        - TAI SU DUNG ham hierholzer() da cai o euler.py,
                          tim chu trinh Euler tren do thi da duoc "tang cuong"
                          (sau khi nhan doi cac canh theo ket qua ghep cap)
Day la phan "nang cao thuc su" cua Phan 8: xu ly truong hop do thi KHONG
thoa dieu kien Euler (co nhieu hon 2 dinh bac le).

Y TUONG THUAT TOAN:
 1. Tim tat ca dinh bac le trong do thi (so luong dinh bac le luon la SO CHAN,
    theo Bo de bat tay - Handshaking Lemma).
 2. Neu khong co dinh bac le nao -> do thi da co san chu trinh Euler, chi can
    chay Hierholzer (khong can xu ly gi them).
 3. Neu co dinh bac le -> tinh KHOANG CACH DUONG DI NGAN NHAT (bang Dijkstra,
    da cai dat san o shortest_path.py) giua MOI CAP dinh bac le.
 4. Tim PHEP GHEP CAP HOAN HAO TRONG SO NHO NHAT (Minimum Weight Perfect
    Matching) tren tap dinh bac le, dung khoang cach ngan nhat vua tinh lam
    trong so. Vi so luong dinh bac le trong thuc te thuong nho (< 10), ta
    dung QUY HOACH DE QUY (backtracking) de duyet tat ca cach ghep cap va
    chon phuong an tong trong so nho nhat - day chinh la phan "nang cao" xu
    ly khi khong co san Euler.
 5. Voi moi cap da ghep, NHAN DOI (them canh "ao") cac canh nam tren duong di
    ngan nhat giua 2 dinh do vao do thi goc. Sau buoc nay, MOI dinh cua do
    thi (da tang cuong) deu co bac chan.
 6. Chay HIERHOLZER tren do thi da tang cuong de tim chu trinh Euler - day
    chinh la lo trinh toi uu ma xe quet rac can di, bat dau va ket thuc tai
    diem xuat phat (garage), quay lai it duong nhat co the.

Tong quang duong di = tong do dai tat ca canh goc (moi canh phai duoc quet 1
lan) + tong khoang cach cac doan duong phai di LAI (deadhead / non-productive
travel) do ghep cap sinh ra.
"""
from graph import Graph
from shortest_path import dijkstra, reconstruct_path
from euler import hierholzer


def find_odd_vertices(graph):
    return [v for v in range(graph.n) if len(graph.adj[v]) % 2 == 1]


def min_weight_perfect_matching(odd_vertices, dist_matrix):
    """
    Quy hoach de quy (backtracking co cat nhanh) tim phep ghep cap hoan hao
    voi tong trong so nho nhat tren tap dinh bac le.
    Tra ve: (tong_chi_phi_nho_nhat, danh_sach_cap_da_ghep)
    """
    best = [float("inf"), None]

    def backtrack(remaining, pairs, cost):
        if cost >= best[0]:
            return  # cat nhanh: da vuot phuong an tot nhat hien tai
        if not remaining:
            best[0] = cost
            best[1] = list(pairs)
            return
        u = remaining[0]
        rest = remaining[1:]
        for i, v in enumerate(rest):
            new_remaining = rest[:i] + rest[i + 1:]
            pairs.append((u, v))
            backtrack(new_remaining, pairs, cost + dist_matrix[(u, v)])
            pairs.pop()

    backtrack(odd_vertices, [], 0)
    return best[0], best[1]


def optimize_route(graph, start=0, verbose=False):
    """
    graph: do thi VO HUONG, co trong so (trong so = do dai doan duong).
    Tra ve dict ket qua gom:
      circuit          : danh sach dinh theo lo trinh toi uu (chu trinh)
      original_total   : tong do dai tat ca doan duong (moi doan tinh 1 lan)
      extra_distance   : tong quang duong phai di LAI them (deadhead)
      total_distance   : original_total + extra_distance
      odd_vertices     : danh sach dinh bac le ban dau
      matching         : danh sach cac cap da ghep
      duplicated_edges : danh sach canh da bi nhan doi (de truc quan hoa)
    """
    odd = find_odd_vertices(graph)
    original_total = sum(w for (u, v, w) in graph.edge_list)

    if verbose:
        print(f"  Buoc 1: So dinh bac le = {len(odd)} -> {[graph.labels[v] for v in odd]}")

    if not odd:
        if verbose:
            print("  Do thi da thoa dieu kien Euler (0 dinh bac le) -> khong can ghep cap.")
        circuit = hierholzer(graph, start=start)
        return {
            "circuit": circuit, "original_total": original_total, "extra_distance": 0,
            "total_distance": original_total, "odd_vertices": [], "matching": [],
            "duplicated_edges": [],
        }

    # Buoc 2: Dijkstra tu moi dinh bac le -> khoang cach + duong di ngan nhat
    # den cac dinh bac le con lai
    dist_matrix, path_matrix = {}, {}
    for u in odd:
        dist, parent = dijkstra(graph, u)
        for v in odd:
            if u != v:
                dist_matrix[(u, v)] = dist[v]
                path_matrix[(u, v)] = reconstruct_path(parent, u, v)

    if verbose:
        print("  Buoc 2: Khoang cach duong di ngan nhat giua tung cap dinh bac le:")
        for u in odd:
            for v in odd:
                if u < v:
                    print(f"      {graph.labels[u]} <-> {graph.labels[v]} : {dist_matrix[(u, v)]:.0f} m")

    # Buoc 3: tim ghep cap hoan hao trong so nho nhat
    best_cost, pairs = min_weight_perfect_matching(odd, dist_matrix)
    if verbose:
        pair_str = ", ".join(f"({graph.labels[u]}-{graph.labels[v]}={dist_matrix[(u,v)]:.0f}m)" for u, v in pairs)
        print(f"  Buoc 3: Phuong an ghep cap toi uu (tong quang duong di lai = {best_cost:.0f} m): {pair_str}")

    # Buoc 4: tao do thi tang cuong - nhan doi cac canh tren duong ngan nhat cua tung cap
    aug = Graph(graph.n, directed=False, weighted=True, labels=graph.labels)
    for (u, v, w) in graph.edge_list:
        aug.add_edge(u, v, w)

    duplicated_edges = []
    for (u, v) in pairs:
        path = path_matrix[(u, v)]
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            w = next(w for (x, y, w) in graph.edge_list if (x == a and y == b) or (x == b and y == a))
            aug.add_edge(a, b, w)
            duplicated_edges.append((a, b, w))
            if verbose:
                print(f"    + Nhan doi canh ({graph.labels[a]}-{graph.labels[b]}, {w:.0f}m) "
                      f"vi thuoc duong noi cap ({graph.labels[u]}-{graph.labels[v]})")

    # Buoc 5: chay Hierholzer tren do thi da tang cuong (moi dinh gio deu bac chan)
    circuit = hierholzer(aug, start=start)
    total_distance = original_total + best_cost

    if verbose:
        print(f"  Buoc 4: Chay Hierholzer tren do thi da tang cuong -> tim duoc chu trinh du {len(circuit)-1} canh")
        print(f"  KET QUA: Tong quang duong xe phai di = {original_total:.0f} + {best_cost:.0f} (di lai) = {total_distance:.0f} m")

    return {
        "circuit": circuit, "original_total": original_total, "extra_distance": best_cost,
        "total_distance": total_distance, "odd_vertices": odd, "matching": pairs,
        "duplicated_edges": duplicated_edges,
    }
