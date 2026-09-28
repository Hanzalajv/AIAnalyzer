# searchAlgos.py
import math
import heapq

# ============ HOSPITAL GRAPH (Task 3) ============
locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },
    "Main_Corridor": {
        "Nursing_Station": 2.2
    },
    "Patient_Wing": {
        "Laboratory": 5.0
    },
    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },
    "Laboratory": {
        "Emergency_Ward": 3.2
    },
    "Emergency_Ward": {}
}

# ============ HEURISTIC FUNCTION ============
def heuristic(current, goal, loc_dict=None):
    """Euclidean distance heuristic."""
    if loc_dict is None:
        loc_dict = locations
    x1, y1 = loc_dict[current]
    x2, y2 = loc_dict[goal]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# ============ PATH RECONSTRUCTION ============
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from and came_from[current] is not None:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# ============ GREEDY BEST-FIRST SEARCH ============
def gbfs(start, goal, graph=None, loc_dict=None):
    """Greedy Best-First Search. Returns (path, cost, expanded_order)."""
    if graph is None:
        graph = hospital_graph
    if loc_dict is None:
        loc_dict = locations

    if start not in graph or goal not in graph:
        return None, float('inf'), []

    counter = 0
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal, loc_dict), counter, start))

    came_from = {start: None}
    visited = set()
    expanded_order = []

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        expanded_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            total = 0
            for i in range(len(path) - 1):
                total += graph[path[i]][path[i + 1]]
            return path, total, expanded_order

        for neighbor in graph.get(current, {}):
            if neighbor not in visited and neighbor not in came_from:
                came_from[neighbor] = current
                counter += 1
                h = heuristic(neighbor, goal, loc_dict)
                heapq.heappush(open_set, (h, counter, neighbor))

    return None, float('inf'), expanded_order

# ============ A* SEARCH ============
def a_star(start, goal, graph=None, loc_dict=None, weight=1.0):
    """A* Search. weight=1.0 normal A*, >1.0 Weighted A*."""
    if graph is None:
        graph = hospital_graph
    if loc_dict is None:
        loc_dict = locations

    if start not in graph or goal not in graph:
        return None, float('inf'), []

    counter = 0
    open_set = []
    h_start = heuristic(start, goal, loc_dict)
    heapq.heappush(open_set, (weight * h_start, counter, start))

    g_score = {start: 0}
    came_from = {start: None}
    visited = set()
    expanded_order = []

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        expanded_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, g_score[current], expanded_order

        for neighbor, edge_cost in graph.get(current, {}).items():
            tentative_g = g_score[current] + edge_cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                f_score = tentative_g + weight * heuristic(neighbor, goal, loc_dict)
                counter += 1
                heapq.heappush(open_set, (f_score, counter, neighbor))

    return None, float('inf'), expanded_order