AIRPORTS = [
    ("SSZ", "São Luís",      -2.54,  -44.30),
    ("BEL", "Belém",         -1.38,  -48.48),
    ("FOR", "Fortaleza",     -3.72,  -38.54),
    ("REC", "Recife",        -8.06,  -34.87),
    ("SSA", "Salvador",     -12.90,  -38.35),
    ("BSB", "Brasília",     -15.78,  -47.93),
    ("GRU", "São Paulo",    -23.43,  -46.47),
    ("GIG", "Rio de Jan.",  -22.81,  -43.25),
    ("CWB", "Curitiba",     -25.53,  -49.17),
    ("POA", "Porto Alegre", -29.99,  -51.17),
    ("CGR", "Campo Grande", -20.47,  -54.67),
    ("CGB", "Cuiabá",       -15.65,  -56.10),
    ("MAO", "Manaus",        -3.04,  -60.05),
]

AIRPORTS_DICT = {
    iata: {"iata": iata, "cidade": cidade, "lat": lat, "lon": lon}
    for iata, cidade, lat, lon in AIRPORTS
}

ROUTES = [
    ("SSZ", "BEL",   60,  320),
    ("SSZ", "FOR",   90,  410),
    ("SSZ", "BSB",  120,  580),
    ("BEL", "MAO",  110,  490),
    ("BEL", "FOR",   95,  370),
    ("FOR", "REC",   75,  280),
    ("FOR", "BSB",  150,  620),
    ("REC", "SSA",   80,  310),
    ("REC", "GIG",  175,  750),
    ("SSA", "BSB",  105,  460),
    ("SSA", "GRU",  170,  680),
    ("BSB", "GRU",  115,  520),
    ("BSB", "CGR",  130,  540),
    ("BSB", "CGB",  140,  560),
    ("GRU", "GIG",   55,  230),
    ("GRU", "CWB",   55,  210),
    ("GRU", "CGR",  100,  390),
    ("GIG", "CWB",   80,  320),
    ("CWB", "POA",   65,  260),
    ("CGR", "CGB",   90,  350),
    ("MAO", "CGB",  135,  590),
    ("MAO", "BSB",  200,  830),
]


def get_adjacency(criterion: str = "tempo") -> dict:
    idx = 2 if criterion == "tempo" else 3
    graph = {iata: [] for iata, *_ in AIRPORTS}
    for row in ROUTES:
        origem, destino, peso = row[0], row[1], row[idx]
        graph[origem].append((destino, peso))
        graph[destino].append((origem, peso))
    return graph