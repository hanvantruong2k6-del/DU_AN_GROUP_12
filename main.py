import os
from graph import Graph
from traversal import bfs, dfs
from bipartite import is_bipartite
from shortest_path import dijkstra, bellman_ford, reconstruct_path
from euler import has_eulerian, fleury, hierholzer
from mst import prim, kruskal
import visualize as viz
import real_world

SAMPLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "samples")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
os.makedirs(OUT, exist_ok=True)


def line(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# PHAN 1: Input + Ve + Luu hinh
def part1_input_and_draw():
    line("PHAN 1: INPUT DO THI, VE VA LUU HINH")
    g = Graph.from_file(os.path.join(SAMPLES, "basic_undirected.txt"))
    print(g)
    save_path = os.path.join(OUT, "part1_input_graph.png")
    viz.draw_graph(g, title="Do thi dau vao (vo huong)", save_path=save_path)
    return g


# PHAN 2: 3 cach bieu dien
def part2_representations(g):
    line("PHAN 2: CAC PHUONG PHAP BIEU DIEN DO THI")
    print("\n[1] Adjacency Matrix (Ma tran ke):")
    g.print_adjacency_matrix()

    print("\n[2] Adjacency List (Danh sach ke):")
    g.print_adjacency_list()

    print("\n[3] Edge List (Danh sach canh):")
    g.print_edge_list()

    print("\n--- Kiem tra chuyen doi qua lai (Adjacency Matrix -> Graph) ---")
    mat = g.to_adjacency_matrix()
    g2 = Graph.from_adjacency_matrix(mat, directed=g.directed, weighted=g.weighted, labels=g.labels)
    print("Do thi tai tao tu ma tran ke:", g2)
    print("Edge list sau tai tao:", g2.to_edge_list())

    print("\n--- Kiem tra chuyen doi qua lai (Edge List -> Graph) ---")
    el = g.to_edge_list()
    g3 = Graph.from_edge_list(g.n, el, directed=g.directed, weighted=g.weighted, labels=g.labels)
    print("Do thi tai tao tu danh sach canh:", g3)


# PHAN 3: BFS & DFS
def part3_traversal(g):
    line("PHAN 3: DUYET DO THI BFS & DFS (bat dau tu dinh A = 0)")
    start = 0

    order_bfs, parent_bfs = bfs(g, start)
    print("BFS order:", " -> ".join(g.labels[x] for x in order_bfs))
    print("BFS parent[]:", {g.labels[i]: (g.labels[p] if p != -1 else None) for i, p in enumerate(parent_bfs)})

    order_dfs, parent_dfs = dfs(g, start)
    print("\nDFS order:", " -> ".join(g.labels[x] for x in order_dfs))
    print("DFS parent[]:", {g.labels[i]: (g.labels[p] if p != -1 else None) for i, p in enumerate(parent_dfs)})

    print("\n>>> Ket qua BFS/DFS se duoc doi chieu chi tiet voi ket qua chay tay trong bao cao Word.")

    viz.draw_traversal_order(g, order_bfs, parent_bfs, "Do thi duyet BFS tu A",
                              os.path.join(OUT, "bfs.png"))
    viz.draw_traversal_order(g, order_dfs, parent_dfs, "Do thi duyet DFS tu A",
                              os.path.join(OUT, "dfs.png"))


# PHAN 4: Bipartite check

def part4_bipartite():
    line("PHAN 4: KIEM TRA DO THI HAI PHIA (BIPARTITE)")

    g_bi = Graph.from_file(os.path.join(SAMPLES, "bipartite_graph.txt"))
    ok, part0, part1 = is_bipartite(g_bi)
    print(f"\nDo thi 'bipartite_graph.txt': {g_bi}")
    print(f"  -> La do thi hai phia? {ok}")
    if ok:
        print(f"     Tap 1: {[g_bi.labels[x] for x in part0]}")
        print(f"     Tap 2: {[g_bi.labels[x] for x in part1]}")
        colors = {v: "#f4a261" for v in part0}
        colors.update({v: "#2a9d8f" for v in part1})
        viz.draw_graph(g_bi, node_colors=colors, title="Do thi hai phia (2 mau)",
                        save_path=os.path.join(OUT, "bipartite_yes.png"))

    g_nonbi = Graph.from_file(os.path.join(SAMPLES, "non_bipartite_graph.txt"))
    ok2, _, _ = is_bipartite(g_nonbi)
    print(f"\nDo thi 'non_bipartite_graph.txt': {g_nonbi}")
    print(f"  -> La do thi hai phia? {ok2}  (co chua chu trinh do dai le an trong do thi lon hon nen khong the hai phia)")
    viz.draw_graph(g_nonbi, title="Do thi khong hai phia (co chu trinh le)",
                    save_path=os.path.join(OUT, "bipartite_no.png"))


# PHAN 5: Dijkstra & Bellman-Ford

def part5_shortest_path():
    line("PHAN 5: DUONG DI NGAN NHAT - DIJKSTRA & BELLMAN-FORD")

    print("\n--- DIJKSTRA (trong so khong am) ---")
    g1 = Graph.from_file(os.path.join(SAMPLES, "weighted_directed_dijkstra.txt"))
    print(g1)
    src, dst = 0, g1.n - 1
    dist, parent = dijkstra(g1, src, verbose=True)
    path = reconstruct_path(parent, src, dst)
    print(f"\nDijkstra: duong ngan nhat {g1.labels[src]} -> {g1.labels[dst]} = {dist[dst]}")
    print("  Duong di:", " -> ".join(g1.labels[x] for x in path))
    print(">>> Doi chieu chay tay: ket qua trung khop")
    viz.draw_shortest_path(g1, path, dist[dst], "Dijkstra", src, dst,
                            os.path.join(OUT, "dijkstra.png"))

    print("\n--- BELLMAN-FORD (cho phep trong so am) ---")
    g2 = Graph.from_file(os.path.join(SAMPLES, "weighted_directed_bellmanford.txt"))
    print(g2)
    src2, dst2 = 0, g2.n - 1
    dist2, parent2, neg_cycle = bellman_ford(g2, src2, verbose=True)
    print(f"\nBellman-Ford: co chu trinh am? {neg_cycle}")
    path2 = reconstruct_path(parent2, src2, dst2)
    print(f"Duong ngan nhat {g2.labels[src2]} -> {g2.labels[dst2]} = {dist2[dst2]}")
    print("  Duong di:", " -> ".join(g2.labels[x] for x in path2))
    print(">>> Doi chieu chay tay ")
    viz.draw_shortest_path(g2, path2, dist2[dst2], "Bellman-Ford", src2, dst2,
                            os.path.join(OUT, "bellmanford.png"))


# PHAN Fleury & Hierholzer

def part7_euler():
    line("PHAN: FLEURY & HIERHOLZER (DUONG/CHU TRINH EULER)")

    for fname, desc in [("euler_circuit.txt", "co du kien chu trinh Euler"),
                         ("euler_path.txt", "co du kien duong di Euler")]:
        g = Graph.from_file(os.path.join(SAMPLES, fname))
        status, odd = has_eulerian(g)
        print(f"\nDo thi '{fname}' ({desc}): {g}")
        print(f"  Ket qua kiem tra dieu kien Euler: {status} (dinh bac le: {[g.labels[x] for x in odd]})")

        print("  --- Fleury ---")
        path_f = fleury(g, verbose=True)
        print("  Duong di Fleury:", " -> ".join(g.labels[x] for x in path_f) if path_f else "Khong ton tai")

        print("  --- Hierholzer ---")
        path_h = hierholzer(g, verbose=True)
        print("  Duong di Hierholzer:", " -> ".join(g.labels[x] for x in path_h) if path_h else "Khong ton tai")

        tag = fname.split(".")[0]
        if path_f:
            viz.draw_euler(g, path_f, "Fleury", os.path.join(OUT, f"fleury_{tag}.png"))
        if path_h:
            viz.draw_euler(g, path_h, "Hierholzer", os.path.join(OUT, f"hierholzer_{tag}.png"))


# PHAN: Prim & Kruskal

def part7_mst():
    line("PHAN 7.3 & 7.4: PRIM & KRUSKAL (CAY KHUNG NHO NHAT)")
    g = Graph.from_file(os.path.join(SAMPLES, "mst_graph.txt"))
    print(g)

    print("\n--- Prim (bat dau tu dinh A) ---")
    mst_p, total_p = prim(g, start=0, verbose=True)
    print(f"MST (Prim), tong trong so = {total_p}")
    for (u, v, w) in mst_p:
        print(f"   {g.labels[u]} - {g.labels[v]} (w={w})")
    viz.draw_mst(g, mst_p, total_p, "Prim", os.path.join(OUT, "prim_mst.png"))

    print("\n--- Kruskal ---")
    mst_k, total_k = kruskal(g, verbose=True)
    print(f"MST (Kruskal), tong trong so = {total_k}")
    for (u, v, w) in mst_k:
        print(f"   {g.labels[u]} - {g.labels[v]} (w={w})")
    viz.draw_mst(g, mst_k, total_k, "Kruskal", os.path.join(OUT, "kruskal_mst.png"))

    print(f"\n>>> Ca 2 thuat toan deu cho tong trong so MST bang nhau: Prim={total_p}, Kruskal={total_k}")


# PHAN 8: Bai toan thuc te

def part8_real_world():
    line("PHAN 8: UNG DUNG THUC TE - XE QUET RAC (KET HOP DIJKSTRA + GHEP CAP + HIERHOLZER)")
    real_world.run_demo(save_dir=OUT)


def main():
    g = part1_input_and_draw()
    part2_representations(g)
    part3_traversal(g)
    part4_bipartite()
    part5_shortest_path()
    part7_euler()
    part7_mst()
    part8_real_world()

    line("HOAN TAT DEMO. Tat ca hinh anh se luu vao trong thu muc outputs/")


if __name__ == "__main__":
    main()
