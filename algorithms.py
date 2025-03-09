import heapq
from haversine import haversine

def dijkstra(graph, start, end):
    queue = [(0, start, [start])]
    visited = set()
    while queue:
        cost, node, path = heapq.heappop(queue)

        if node == end:
            return path, cost

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))

    return None, None


def astar(graph, coordinates, start, end):
    queue = [(0, start, [start], 0)]
    visited = set()
    while queue:
        f_cost, node, path, g_cost = heapq.heappop(queue)

        if node == end:
            return path, g_cost

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                if neighbor in coordinates and end in coordinates:
                    lat1, lon1 = coordinates[neighbor]
                    lat2, lon2 = coordinates[end]
                    h = haversine(lat1, lon1, lat2, lon2)
                else:
                    h = 0
                total_cost = g_cost + weight
                f = total_cost + h
                heapq.heappush(queue, (f, neighbor, path + [neighbor], total_cost))

    return None, None