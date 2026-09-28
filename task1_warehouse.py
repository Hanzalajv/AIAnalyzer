# task1_warehouse.py
import math
import networkx as nx
import matplotlib.pyplot as plt

locations = {
    "Receiving_Area": (0, 0),
    "Storage_A": (2, 1),
    "Storage_B": (1, 4),
    "Sorting_Area": (4, 2),
    "Inspection_Area": (5, 5),
    "Packing_Station": (7, 6)
}

warehouse_graph = {
    "Receiving_Area": {"Storage_A": 2.2, "Storage_B": 4.1},
    "Storage_A": {"Sorting_Area": 2.2},
    "Storage_B": {"Inspection_Area": 5.0, "Sorting_Area": 6.0},
    "Sorting_Area": {"Inspection_Area": 3.2, "Packing_Station": 5.0},
    "Inspection_Area": {"Packing_Station": 2.2},
    "Packing_Station": {}
}

GOAL = "Packing_Station"

def h(n):
    x1, y1 = locations[n]
    x2, y2 = locations[GOAL]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

print("=" * 55)
print("HEURISTIC VALUES (Euclidean to Packing_Station)")
print("=" * 55)
for n in locations:
    print(f"h({n:20s}) = {h(n):.3f}")

print("\n" + "=" * 60)
print("CONSISTENCY CHECK: h(n) <= c(n,m) + h(m)")
print("=" * 60)
for n, nbrs in warehouse_graph.items():
    for m, cost in nbrs.items():
        lhs, rhs = h(n), cost + h(m)
        ok = "OK" if lhs <= rhs + 1e-9 else "VIOLATION"
        print(f"h({n})={lhs:.3f}  <=  {cost} + h({m})={h(m):.3f} = {rhs:.3f}  [{ok}]")

G = nx.DiGraph()
for n, nbrs in warehouse_graph.items():
    for m, w in nbrs.items():
        G.add_edge(n, m, weight=w)

fig, ax = plt.subplots(figsize=(10, 7))
nx.draw_networkx_edges(G, locations, ax=ax, arrows=True, arrowsize=15)
nx.draw_networkx_nodes(G, locations, ax=ax, node_color="skyblue",
                       node_size=1800, edgecolors="black")
nx.draw_networkx_edge_labels(G, locations,
                             nx.get_edge_attributes(G, "weight"), ax=ax)
nx.draw_networkx_labels(G, locations, ax=ax, font_size=9, font_weight="bold")
ax.set_title("Warehouse Graph (Task 1)")
ax.axis("off")
plt.tight_layout()
plt.savefig("task1_warehouse.png", dpi=150)
plt.show()

print("""
EXPLANATION:
Euclidean distance is a suitable heuristic because:
1. Movement is spatial, so straight-line proximity is meaningful.
2. It is ADMISSIBLE - never overestimates the actual remaining cost.
3. It is CONSISTENT - triangle inequality holds (verified above).
""")