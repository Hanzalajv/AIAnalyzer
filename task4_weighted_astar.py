# task4_weighted_astar.py
from searchAlgos import a_star

drone_graph = {
    "Distribution_Center": {"Zone_A": 2.2, "Zone_B": 3.0},
    "Zone_A": {"Zone_C": 2.2},
    "Zone_B": {"Zone_D": 5.0},
    "Zone_C": {"Zone_D": 3.2, "Customer_Building": 6.0},
    "Zone_D": {"Customer_Building": 3.2},
    "Customer_Building": {}
}

drone_locs = {
    "Distribution_Center": (0, 0),
    "Zone_A": (2, 1),
    "Zone_B": (1, 4),
    "Zone_C": (4, 2),
    "Zone_D": (5, 5),
    "Customer_Building": (8, 6)
}

start, goal = "Distribution_Center", "Customer_Building"

print(f"{'Weight':<8}{'Path':<60}{'Cost':<10}{'Nodes Expanded':<15}")
print("-" * 95)
for w in [1.0, 1.5, 2.0, 3.0]:
    path, cost, order = a_star(start, goal, drone_graph, drone_locs, weight=w)
    path_str = " -> ".join(path) if path else "None"
    print(f"{w:<8}{path_str:<60}{cost:<10.2f}{len(order):<15}")

print("""
ANALYSIS:
- w = 1.0 -> Normal A*, optimal path.
- w > 1.0 -> Heuristic weighted more; search becomes greedier, expands
  fewer nodes, but may return a higher-cost (suboptimal) path.
- Optimality guarantee is lost when w > 1.
""")