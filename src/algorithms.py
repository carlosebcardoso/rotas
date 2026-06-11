from mock import AIRPORTS_DICT, ROUTES, get_adjacency

def dijkstra(origin: str, dest: str, criterion: str = "tempo"):
    graph = get_adjacency(criterion)

    dist = {v: float("inf") for v in graph}
    path = {v: [] for v in graph}

    dist[origin] = 0
    path[origin] = [origin]

    visited = set()

    while len(visited) < len(graph):
        u = None
        min_dist = float("inf")

        for v in graph:
            if v not in visited and dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        if u is None:
            break

        if u == dest:
            break

        visited.add(u)

        for v, w in graph[u]:
            new_dist = dist[u] + w

            if new_dist < dist[v]:
                dist[v] = new_dist
                path[v] = path[u] + [v]

    if not path[dest]:
        return None, None, None

    edges = [
        (path[dest][i], path[dest][i + 1])
        for i in range(len(path[dest]) - 1)
    ]

    return path[dest], dist[dest], edges

def get_route_weight(origem: str, destino: str, criterion: str) -> int:
    idx = 2 if criterion == "tempo" else 3
    for row in ROUTES:
        if (row[0] == origem and row[1] == destino) or \
           (row[0] == destino and row[1] == origem):
            return row[idx]
    return 0


def calc_secondary_total(path: list, secondary: str) -> int:
    return sum(
        get_route_weight(path[i], path[i + 1], secondary)
        for i in range(len(path) - 1)
    )


def format_total(value: int, criterion: str) -> str:
    if criterion == "tempo":
        h, m = divmod(value, 60)
        return f"{h}h {m:02d}min" if h else f"{value} min"
    return f"R$ {value:,.0f}".replace(",", ".")


def airport_label(iata: str) -> str:
    a = AIRPORTS_DICT[iata]
    return f"{a['iata']} — {a['cidade']}"