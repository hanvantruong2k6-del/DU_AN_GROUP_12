"""
BAI TOAN THUC TE (Phan 8): TOI UU LO TRINH XE QUET RAC (STREET SWEEPING)
- xu ly bang cach ket hop 3 thuat toan da cai dat: DIJKSTRA, GHEP CAP TRONG
SO NHO NHAT (tu cai bang backtracking), va HIERHOLZER.

MO TA BAI TOAN:
- Mot cong ty ve sinh, cu the do thi co 1 xe quet rac can di qua all cac con
  duong trong 1 khu pho de quet don / thu gom rac hai ben duong.
- Day la bai toan tren canh (edge) cua do thi: phai di qua het moi doan duong, khac voi bai toan tim duong ngan nhat o Phan 5 (Dijkstra,
  Bellman-Ford) la chi can den dung 1 dinh dich.
- Xe xuat phat va back dung bai do (garage) sau khi hoan thanh,
  sao cho ton it quang duong di thua (di lai / khong quet) it nhat co the.

MO HINH HOA THANH DO THI:
    + Moi giao lo (nga ba/nga tu) trong khu pho  = 1 DINH (node)
    + Moi doan duong can quet                    = 1 CANH (edge), VO HUONG
    + Do dai doan duong (m)                    = TRONG SO CUA CANH
    + Bai do xe (garage)                         = dinh xuat phat/ket thuc
    + Can tim: 1 chu trinh di qua mot canh dung 1 lan, bat dau/ket thuc tai
      garage, voi tong quang duong di thua (deadhead) la MIX
      => Day chinh la bai toan:: CHU TRINH EULER MO RONG.

Quan trọng - VI SAO KHONG THE CHAY EULER TRUC TIEP:
    Voi mang luoi duong pho " thuc te", hau nhu khong bao giotat ca giao lo
    deu co bac chan. Vi du trong file nay co toi 6/8 dinh bac le
    (Handshaking Lemma dam bao so dinh bac le luon la "SO CHAN"). Do vay khong the ap dung Fleury/Hierholzer truc tiep - day chinh la ly do can them 
    ham dieu phoi "route_orchestrator.py", ket hop 3 thuat toan:
      (1) DIJKSTRA tinh khoang cach ngan nhat giua cac dinh bac le
      (2) Ghep căp trong so nho nhat tren tap
          dinh bac le, dung khoang cach vua tinh lam trong so
      (3) X2 cac canh tren duong di ngan nhat cua tung cap da ghep,
          roi chay HIERHOLZER tren do thi da "tang cuong" (moi dinh gio
          deu bac chan) de tim chu trinh Euler)
"""
import os
from graph import Graph
from euler import has_eulerian
from route_orchestrator import optimize_route

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_SAMPLE = os.path.join(_THIS_DIR, "..", "samples", "street_network.txt")
_DEFAULT_OUT = os.path.join(_THIS_DIR, "..", "outputs")


def build_street_network(path=_DEFAULT_SAMPLE):
    return Graph.from_file(path)


def run_demo(save_dir=_DEFAULT_OUT):
    import visualize as viz
    os.makedirs(save_dir, exist_ok=True)

    g = build_street_network()
    garage = 0

    print(g)
    print("\n--- So do mang luoi duong pho (danh sach ke, trong so = met) ---")
    g.print_adjacency_list()

    deg = [len(g.adj[v]) for v in range(g.n)]
    odd = [g.labels[v] for v in range(g.n) if deg[v] % 2 == 1]
    print(f"\nBac cua tung giao lo: {[(g.labels[v], deg[v]) for v in range(g.n)]}")
    print(f"So giao lo bac le: {len(odd)} -> {odd}  (khong thoa dieu kien Euler, can xu ly nang cao)")

    status, _ = has_eulerian(g)
    print(f"Kiem tra dieu kien Euler truc tiep: {status} -> phai dung Dijkstra + Ghep cap trong so nho nhat + Hierholzer")

    print("\n--- Ap dung: Dijkstra + Ghep cap trong so nho nhat + Hierholzer ---")
    result = optimize_route(g, start=garage, verbose=True)

    circuit = result["circuit"]
    print("\nKET QUA LO TRINH TOI UU CHO XE QUET RAC:")
    print("  Lo trinh:", " -> ".join(g.labels[x] for x in circuit))
    print(f"  Tong do dai duong can quet (moi doan 1 lan) : {result['original_total']:.0f} m")
    print(f"  Quang duong phai di lai them (deadhead)     : {result['extra_distance']:.0f} m")
    print(f"  TONG QUANG DUONG XE PHAI DI                 : {result['total_distance']:.0f} m")

    # ve minh hoa
    viz.draw_graph(g, title="Mang luoi duong pho khu vuc (Garage = diem xuat phat)",
                    save_path=f"{save_dir}/real_world_street_network.png")

    viz.draw_matching_result(g, result["odd_vertices"], result["matching"], result["duplicated_edges"],
                           save_path=f"{save_dir}/real_world_matching_result.png")

    viz.draw_optimized_route(g, circuit, result["total_distance"],
                        save_path=f"{save_dir}/real_world_optimized_route.png")

    return g, result


if __name__ == "__main__":
    run_demo()
