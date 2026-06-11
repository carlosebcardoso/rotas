from mock import AIRPORTS_DICT, ROUTES, get_adjacency

def dijkstra(origin: str, dest: str, criterion: str = "tempo"):
    graph = get_adjacency(criterion)

    menores_custos = {v: float("inf") for v in graph}
    melhor_rota = {v: [] for v in graph}

    menores_custos[origin] = 0
    melhor_rota[origin] = [origin]

    verificados = set()

    while len(verificados) < len(graph):
        v_atual = None
        menor_custo = float("inf")

        for v in graph:
            if v not in verificados and menores_custos[v] < menor_custo:
                menor_custo = menores_custos[v]
                v_atual = v

        if v_atual is None:
            break

        if v_atual == dest:
            break

        verificados.add(v_atual)

        for v_destino, custo in graph[v_atual]:
            novo_custo = menores_custos[v_atual] + custo

            if novo_custo < menores_custos[v_destino]:
                menores_custos[v_destino] = novo_custo
                melhor_rota[v_destino] = (
                    melhor_rota[v_atual] + [v_destino]
                )

    if not melhor_rota[dest]:
        return None, None, None

    edges = [
        (melhor_rota[dest][i], melhor_rota[dest][i + 1])
        for i in range(len(melhor_rota[dest]) - 1)
    ]

    return (
        melhor_rota[dest],
        menores_custos[dest],
        edges,
    )

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