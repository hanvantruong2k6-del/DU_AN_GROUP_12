"""
PHAN TRUC QUAN HOA - phan nay cai thu vien
(matplotlib va networkx co san de tinh toa do bo tri dinh - layout).
Tat ca thuat toan (BFS/DFS/Dijkstra/Bellman-Ford/Prim/Kruskal/Fleury/
Hierholzer); lop nay chi nhan "KET QUA" da tinh san va ve minh hoa.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx


def _build_nx_layout(graph, seed=42):
    """Chi dung networkx de tinh toa do (spring layout) cho dep, khong dung de chay thuat toan."""
    G = nx.DiGraph() if graph.directed else nx.Graph()
    G.add_nodes_from(range(graph.n))
    for (u, v, w) in graph.edge_list:
        G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G, seed=seed, k=1.3 / (graph.n ** 0.3))
    return G, pos


def draw_graph(graph, path=None, title="Do thi", save_path=None,
                highlight_edges=None, node_colors=None, edge_labels=True):
    """
    Ve do thi co ban, co the highlight 1 duong di (path = list dinh) hoac
    1 tap canh (highlight_edges = list (u,v)).
    node_colors: dict {node: color} de to mau rieng (vd bipartite 2 mau).
    """
    G, pos = _build_nx_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = []
    for i in range(graph.n):
        if node_colors and i in node_colors:
            colors.append(node_colors[i])
        else:
            colors.append("#a7c7e7")

    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=650,
                            edgecolors="#333333", linewidths=1.2, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={i: graph.labels[i] for i in range(graph.n)},
                             font_size=11, font_weight="bold", ax=ax)

    highlight_set = set()
    if path:
        highlight_set = {(path[i], path[i + 1]) for i in range(len(path) - 1)}
        if not graph.directed:
            highlight_set |= {(b, a) for (a, b) in highlight_set}
    if highlight_edges:
        he = set(highlight_edges)
        highlight_set |= he
        if not graph.directed:
            highlight_set |= {(b, a) for (a, b) in he}

    normal_edges = [(u, v) for (u, v) in G.edges() if (u, v) not in highlight_set and (v, u) not in highlight_set]
    hl_edges = [(u, v) for (u, v) in G.edges() if (u, v) in highlight_set or (v, u) in highlight_set]

    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, ax=ax, width=1.4,
                            edge_color="#888888",
                            arrows=True, arrowstyle="-|>" if graph.directed else "-",
                            arrowsize=16 if graph.directed else 1,
                            connectionstyle="arc3,rad=0.05")
    if hl_edges:
        nx.draw_networkx_edges(G, pos, edgelist=hl_edges, ax=ax, width=3.0,
                                edge_color="#e63946",
                                arrows=True, arrowstyle="-|>" if graph.directed else "-",
                                arrowsize=18 if graph.directed else 1,
                                connectionstyle="arc3,rad=0.05")

    if edge_labels and graph.weighted:
        ed_labels = {(u, v): f"{w:g}" for (u, v, w) in graph.edge_list}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=ed_labels, font_size=9, ax=ax)

    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.axis("off")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"  [Da luu hinh] {save_path}")
    plt.close(fig)
    return save_path


def draw_traversal_order(graph, order, parent, title, save_path):
    """Ve cay BFS/DFS: to mau dinh theo thu tu tham, ve canh cua cay parent[]."""
    tree_edges = [(parent[v], v) for v in range(graph.n) if parent[v] != -1]
    rank = {node: i for i, node in enumerate(order)}
    cmap = plt.cm.viridis
    node_colors = {}
    for v in range(graph.n):
        if v in rank:
            node_colors[v] = cmap(rank[v] / max(1, len(order) - 1))
        else:
            node_colors[v] = "#dddddd"
    draw_graph(graph, highlight_edges=tree_edges, node_colors=node_colors,
               title=title, save_path=save_path)


def draw_mst(graph, mst_edges, total, algo_name, save_path):
    edges_uv = [(u, v) for (u, v, w) in mst_edges]
    draw_graph(graph, highlight_edges=edges_uv,
               title=f"{algo_name} - Cay khung nho nhat (tong = {total:g})",
               save_path=save_path)


def draw_euler(graph, path_nodes, algo_name, save_path):
    draw_graph(graph, path=path_nodes,
               title=f"{algo_name} - Duong/Chu trinh Euler",
               save_path=save_path)


def draw_shortest_path(graph, path, dist_target, algo_name, src, dst, save_path):
    draw_graph(graph, path=path,
               title=f"{algo_name}: duong ngan nhat {graph.labels[src]}->{graph.labels[dst]} (do dai={dist_target:g})",
               save_path=save_path)


def draw_matching_result(graph, odd_vertices, matching, duplicated_edges, save_path):
    """Ve do thi goc, danh dau cac dinh bac le va cac canh bi nhan doi do ghep cap (CPP)."""
    node_colors = {v: "#e63946" for v in odd_vertices}
    dup_edges_uv = [(u, v) for (u, v, w) in duplicated_edges]
    title = "Ghep cap dinh bac le (do) va canh nhan doi do ghep cap (do dam)"
    draw_graph(graph, highlight_edges=dup_edges_uv, node_colors=node_colors,
               title=title, save_path=save_path)


def draw_optimized_route(graph, circuit, total_distance, save_path):
    """Ve lo trinh toi uu hoan chinh (co the lap lai canh do di lai)."""
    G, pos = _build_nx_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 6))

    nx.draw_networkx_nodes(G, pos, node_color="#a7c7e7", node_size=650,
                            edgecolors="#333333", linewidths=1.2, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={i: graph.labels[i] for i in range(graph.n)},
                             font_size=11, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=list(G.edges()), ax=ax, width=1.2,
                            edge_color="#cccccc")

    # ve lo trinh nhu mot chuoi mui ten danh so thu tu, dung do cong (curvature)
    # tang dan khi cung 1 cap dinh duoc di qua nhieu lan (canh bi x2)
    pair_count = {}
    cmap = plt.cm.plasma
    n_steps = len(circuit) - 1
    for i in range(n_steps):
        u, v = circuit[i], circuit[i + 1]
        key = (min(u, v), max(u, v))
        pair_count[key] = pair_count.get(key, 0) + 1
        rad = 0.15 * (pair_count[key] - 1) * (1 if u < v else -1) + 0.08
        color = cmap(i / max(1, n_steps - 1))
        ax.annotate("", xy=pos[v], xytext=pos[u],
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2,
                                    connectionstyle=f"arc3,rad={rad}",
                                    shrinkA=14, shrinkB=14))

    ax.set_title(f"Lo trinh toi uu (Dijkstra + Ghep cap + Hierholzer), tong = {total_distance:g} m", fontsize=13, fontweight="bold")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"  [Da luu hinh] {save_path}")
    plt.close(fig)
    return save_path
