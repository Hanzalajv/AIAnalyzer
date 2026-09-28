# task2_gbfs_airport.py
import math, heapq
import networkx as nx
import matplotlib.pyplot as plt

locations = {
    "Baggage_Area": (0, 0),
    "Security": (2, 1),
    "Checkpoint": (1, 4),
    "Food_Court": (4, 2),
    "Terminal_Hall": (5, 5),
    "Departure_Gate": (8, 6)
}

airport_graph = {
    "Baggage_Area": {"Security": 2.2, "Checkpoint": 4.1},
    "Security": {"Food_Court": 2.2},
    "Checkpoint": {"Terminal_Hall": 5.0},
    "Food_Court": {"Terminal_Hall": 3.2, "Departure_Gate": 6.0},
    "Terminal_Hall": {"Departure_Gate": 3.2},
    "Departure_Gate": {}
}

def h(n, goal="Departure_Gate"):
    x1, y1 = locations[n]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def gbfs(start, goal):
    counter = 0
    pq = [(h(start, goal), counter, start)]
    came_from = {start: None}
    visited = set()
    order = []
    while pq:
        _, _, cur = heapq.heappop(pq)
        if cur in visited:
            continue
        visited.add(cur)
        order.append(cur)
        if cur == goal:
            path = [cur]
            while came_from[cur]:
                cur = came_from[cur]
                path.append(cur)
            path.reverse()
            return path, order
        for nb in airport_graph.get(cur, {}):
            if nb not in visited and nb not in came_from:
                came_from[nb] = cur
                counter += 1
                heapq.heappush(pq, (h(nb, goal), counter, nb))
    return None, order

start, goal = "Baggage_Area", "Departure_Gate"
path, order = gbfs(start, goal)

print("GBFS Expansion Order:", " -> ".join(order))
print("Solution Path:", " -> ".join(path))
cost = sum(airport_graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
print(f"Total Path Cost: {cost:.2f}")

G = nx.DiGraph()
for n, nbrs in airport_graph.items():
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
ax.set_title("GBFS Solution - Airport Baggage Handling")
ax.axis("off")
plt.tight_layout()
plt.savefig("task2_gbfs.png", dpi=150)
plt.show()

print("""
EXPLANATION:
GBFS expands nodes purely by h(n) - the Euclidean distance to Departure_Gate.
It ignores g(n) (distance already travelled), so it prefers whichever
neighbor looks geometrically closest to the goal. Fast but not optimal.
""")