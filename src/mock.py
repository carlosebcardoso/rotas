from streamlit_agraph import Node, Edge

# Aeroportos: (id IATA, nome, x, y)
# Posições aproximadas geograficamente no canvas 700x500
AIRPORTS = [
    ("SSZ", "São Luís",    170,  90),
    ("BEL", "Belém",       210,  70),
    ("FOR", "Fortaleza",   310,  75),
    ("REC", "Recife",      420,  160),
    ("SSA", "Salvador",    380,  250),
    ("BSB", "Brasília",    280,  290),
    ("GRU", "São Paulo",   240,  390),
    ("GIG", "Rio de Jan.", 310,  420),
    ("CWB", "Curitiba",    230,  440),
    ("POA", "Porto Alegre",215,  480),
    ("CGR", "Campo Grande",185,  370),
    ("CGB", "Cuiabá",      140,  310),
    ("MAO", "Manaus",       80,  130),
]

AIRPORTS_DICT = {
    iata: {
        "iata": iata,
        "cidade": cidade,
        "x": x,
        "y": y,
    }
    for iata, cidade, x, y in AIRPORTS
}

# Rotas: (origem, destino, tempo em minutos)
# Pensadas para que vários pares importantes NÃO tenham rota direta:
# - São Luís <-> Rio: não há rota direta
# - Manaus <-> Salvador: não há rota direta
# - Porto Alegre <-> Fortaleza: não há rota direta
# - Cuiabá <-> Recife: não há rota direta
ROUTES = [
    ("SSZ", "BEL",  60),
    ("SSZ", "FOR",  90),
    ("SSZ", "BSB", 120),
    ("BEL", "MAO", 110),
    ("BEL", "FOR",  95),
    ("FOR", "REC",  75),
    ("FOR", "BSB", 150),
    ("REC", "SSA",  80),
    ("REC", "GIG", 175),
    ("SSA", "BSB", 105),
    ("SSA", "GRU", 170),
    ("BSB", "GRU", 115),
    ("BSB", "CGR", 130),
    ("BSB", "CGB", 140),
    ("GRU", "GIG",  55),
    ("GRU", "CWB",  55),
    ("GRU", "CGR", 100),
    ("GIG", "CWB",  80),
    ("CWB", "POA",  65),
    ("CGR", "CGB",  90),
    ("MAO", "CGB", 135),
    ("MAO", "BSB", 200),
]

def build_nodes(highlight: list[str] = []) -> list[Node]:
    return [
        Node(
            id=iata,
            label=f"{iata}\n{cidade}",
            size=30 if iata in highlight else 20,
            color="#1D9E75" if iata in highlight else "#378ADD",
            font={"color": "#fff", "size": 11},
            x=x * 1.0,
            y=y * 1.0,
        )
        for iata, cidade, x, y in AIRPORTS
    ]

def build_edges(path_edges: list[tuple] = []) -> list[Edge]:
    edges = []
    for origem, destino, tempo in ROUTES:
        on_path = (origem, destino) in path_edges or (destino, origem) in path_edges
        edges.append(Edge(
            source=origem,
            target=destino,
            label=f"{tempo}min",
            color="#D85A30" if on_path else "#B4B2A9",
            width=3 if on_path else 1,
            font={ "color": "#fff", "strokeWidth": 0 }
            
        ))
    return edges

def get_adjacency() -> dict:
    """Lista de adjacência para o Dijkstra: {origem: [(destino, tempo)]}"""
    graph = {iata: [] for iata, *_ in AIRPORTS}
    for origem, destino, tempo in ROUTES:
        graph[origem].append((destino, tempo))
        graph[destino].append((origem, tempo))
    return graph