import heapq
from mock import AIRPORTS_DICT, ROUTES, get_adjacency


def dijkstra(origin: str, dest: str, criterion: str = "tempo"):
    graph = get_adjacency(criterion)
    dist  = {n: float("inf") for n in graph}
    prev  = {n: None for n in graph}
    dist[origin] = 0
    heap = [(0, origin)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    path, cur = [], dest
    while cur:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    if not path or path[0] != origin:
        return None, None, None

    edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    return path, dist[dest], edges


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