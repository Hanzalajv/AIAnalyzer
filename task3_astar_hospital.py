# task3_astar_hospital.py
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from searchAlgos import hospital_graph, locations, heuristic

def a_star(start, goal):
    counter = 0
    pq = [(heuristic(start, goal), counter, start)]
    g = {start: 0}
    came_from = {start: None}
    visited = set()
    order, trace = [], []

    while pq:
        _, _, cur = heapq.heappop(pq)
        if cur in visited:
            continue
        visited.add(cur)
        order.append(cur)
        trace.append({
            "Node": cur,
            "g(n)": round(g[cur], 3),
            "h(n)": round(heuristic(cur, goal), 3),
            "f(n)": round(g[cur] + heuristic(cur, goal), 3)
        })
        if cur == goal:
            path = [cur]
            while came_from[cur]:
                cur = came_from[cur]
                path.append(cur)
            path.reverse()
            return path, g[goal], order, trace

        for nb, w in hospital_graph.get(cur, {}).items():
            ng = g[cur] + w
            if nb not in g or ng < g[nb]:
                g[nb] = ng
                came_from[nb] = cur
                counter += 1
                heapq.heappush(pq, (ng + heuristic(nb, goal), counter, nb))
    return None, float('inf'), order, trace

start, goal = "Pharmacy", "Emergency_Ward"
path, cost, order, trace = a_star(start, goal)

print("A* Expansion Order:", " -> ".join(order))
print("Solution Path:", " -> ".join(path))
print(f"Total Cost: {cost:.2f}\n")
print(f"{'Node':<20}{'g(n)':<10}{'h(n)':<10}{'f(n)':<10}")
print("-" * 50)
for row in trace:
    print(f"{row['Node']:<20}{row['g(n)']:<10}{row['h(n)']:<10}{row['f(n)']:<10}")

G = nx.DiGraph()
for n, nbrs in hospital_graph.items():
    for m, w in nbrs.items():
        G.add_edge(n, m, weight=w)

fig, ax = plt.subplots(figsize=(11, 7))
nx.draw_networkx_edges(G, locations, ax=ax, edge_color="lightgray",
                       arrows=True, arrowsize=15, width=2)
nx.draw_networkx_nodes(G, locations, ax=ax, node_color="lightblue",
                       node_size=1800, edgecolors="black")
nx.draw_networkx_edge_labels(G, locations,
                             nx.get_edge_attributes(G, "weight"), ax=ax)
pe = list(zip(path[:-1], path[1:]))
nx.draw_networkx_edges(G, locations, edgelist=pe, ax=ax,
                       edge_color="red", width=4, arrows=True, arrowsize=20)
nx.draw_networkx_nodes(G, locations, nodelist=path, ax=ax,
                       node_color="salmon", node_size=1800, edgecolors="black")
nx.draw_networkx_labels(G, locations, ax=ax, font_size=9, font_weight="bold")
ax.set_title("A* Solution - Hospital Emergency Supply")
ax.axis("off")
plt.tight_layout()
plt.savefig("task3_astar.png", dpi=150)
plt.show()

print("""
COMPARISON A* vs GBFS:
A* uses f(n) = g(n) + h(n), balancing cost so far with remaining estimate.
GBFS uses only h(n). A* explores fewer nodes and guarantees optimality
when h is admissible; GBFS is faster but may take a longer route.
""")