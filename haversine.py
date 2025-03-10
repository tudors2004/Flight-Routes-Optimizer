import math
import json

# The routes are 6 or 7 years old so there might be missing routes between airports,
# and for some smaller airports there might be random routes that do not exist at all
# but in general the routes are correct

# The haversine formula is used to calculate the distance between two points on the surface of a sphere
def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # the earths radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # distance in km


# This script helps to create the graph.json file

coordinates = {}
with open("static/coordinates.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        iata = parts[0].strip()
        lat = float(parts[1])
        lon = float(parts[2])
        coordinates[iata] = (lat, lon)


graph = {}
with open("static/routes.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        src = parts[0].strip()
        dst = parts[1].strip()

        if src in coordinates and dst in coordinates:
            lat1, lon1 = coordinates[src]
            lat2, lon2 = coordinates[dst]
            distance = round(haversine(lat1, lon1, lat2, lon2))

            if src not in graph:
                graph[src] = {}

            graph[src][dst] = distance
        else:
            print(f" missing coord for {src} or {dst}")


with open("static/graph.json", "w") as f:
    json.dump(graph, f, indent=4)
