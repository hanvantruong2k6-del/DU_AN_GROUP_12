# -*- coding: utf-8 -*-
"""
real_world.py
BAI TOAN THUC TE (Phan 8): TOI UU LO TRINH XE QUET RAC (STREET SWEEPING)
bang bai toan NGUOI PHAT THU TRUNG QUOC (Chinese Postman Problem), su dung
thuat toan Euler (Hierholzer) lam nen tang.

MO TA BAI TOAN:
- Mot cong ty ve sinh do thi co 1 xe quet rac can di qua TAT CA cac con
  duong trong 1 khu pho de quet don / thu gom rac hai ben duong.
- Khac voi bai toan giao hang (chi can DEN TUNG DIEM), bai toan quet rac can
  DI QUA HET MOI DOAN DUONG - day la diem mau chot khien bai toan nay la
  bai toan tren CANH (edge) chu khong phai tren DINH (vertex) nhu Dijkstra.
- Xe xuat phat va PHAI QUAY VE dung bai do (garage) sau khi hoan thanh,
  sao cho TON IT QUANG DUONG DI THUA (di lai / khong quet) nhat co the.

MO HINH HOA THANH DO THI:
    + Moi giao lo (nga ba/nga tu) trong khu pho  = 1 DINH (node)
    + Moi doan duong can quet                    = 1 CANH (edge), VO HUONG
    + Do dai doan duong (met)                    = TRONG SO cua canh
    + Bai do xe (garage)                         = dinh xuat phat/ket thuc
    + Can tim: 1 CHU TRINH di qua MOI CANH DUNG 1 LAN, bat dau/ket thuc tai
      garage, voi TONG QUANG DUONG DI THUA (deadhead) la NHO NHAT.
    => Day chinh la bai toan CHU TRINH EULER mo rong (Chinese Postman).

DIEM MAU CHOT - VI SAO KHONG THE CHAY EULER TRUC TIEP:
    Voi mang luoi duong pho THUC TE, hau nhu KHONG BAO GIO tat ca giao lo
    deu co bac chan. Vi du minh hoa trong file nay co toi 6/8 dinh bac le
    (Handshaking Lemma dam bao so dinh bac le luon la SO CHAN). Do do KHONG
    THE ap dung Fleury/Hierholzer truc tiep - day chinh la ly do can them
    buoc "nang cao": GHEP CAP CAC DINH BAC LE + NHAN DOI DUONG DI NGAN NHAT
    (dung lai Dijkstra) DE BIEN DO THI THANH CO CHU TRINH EULER, roi moi
    chay Hierholzer (xem chi tiet trong module chinese_postman.py).
"""
import os
from graph import Graph
from euler import has_eulerian
from chinese_postman import chinese_postman

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_SAMPLE = os.path.join(_THIS_DIR, "..", "samples", "street_network_cpp.txt")
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
    print(f"So giao lo bac le: {len(odd)} -> {odd}  (KHONG thoa dieu kien Euler, can xu ly nang cao)")

    status, _ = has_eulerian(g)
    print(f"Kiem tra dieu kien Euler truc tiep: {status} -> phai dung Chinese Postman Problem")

    print("\n--- Ap dung Chinese Postman Problem ---")
    result = chinese_postman(g, start=garage, verbose=True)

    circuit = result["circuit"]
    print("\nKET QUA LO TRINH TOI UU CHO XE QUET RAC:")
    print("  Lo trinh:", " -> ".join(g.labels[x] for x in circuit))
    print(f"  Tong do dai duong can quet (moi doan 1 lan) : {result['original_total']:.0f} m")
    print(f"  Quang duong phai di lai them (deadhead)     : {result['extra_distance']:.0f} m")
    print(f"  TONG QUANG DUONG XE PHAI DI                 : {result['total_distance']:.0f} m")

    # ve minh hoa
    viz.draw_graph(g, title="Mang luoi duong pho khu vuc (Garage = diem xuat phat)",
                    save_path=f"{save_dir}/real_world_street_network.png")

    viz.draw_cpp_matching(g, result["odd_vertices"], result["matching"], result["duplicated_edges"],
                           save_path=f"{save_dir}/real_world_cpp_matching.png")

    viz.draw_cpp_route(g, circuit, result["total_distance"],
                        save_path=f"{save_dir}/real_world_cpp_route.png")

    return g, result


if __name__ == "__main__":
    run_demo()
