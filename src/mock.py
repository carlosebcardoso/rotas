# Aeroportos das capitais brasileiras
AIRPORTS = [
    ("RIO", "Rio Branco",       -9.97,  -67.80),   # AC - Rio Branco
    ("MCZ", "Maceió",           -9.66,  -35.70),   # AL - Maceió
    ("MCP", "Macapá",            0.03,  -51.07),   # AP - Macapá
    ("MAO", "Manaus",           -3.10,  -60.02),   # AM - Manaus
    ("SSA", "Salvador",        -12.97,  -38.50),   # BA - Salvador
    ("FOR", "Fortaleza",        -3.78,  -38.53),   # CE - Fortaleza
    ("BSB", "Brasília",        -15.87,  -47.92),   # DF - Brasília
    ("VIX", "Vitória",         -20.26,  -40.28),   # ES - Vitória
    ("GYN", "Goiânia",         -16.63,  -49.22),   # GO - Goiânia
    ("SLZ", "São Luís",         -2.53,  -44.30),   # MA - São Luís
    ("CGB", "Cuiabá",          -15.65,  -56.12),   # MT - Cuiabá
    ("CGR", "Campo Grande",    -20.47,  -54.67),   # MS - Campo Grande
    ("CNF", "Belo Horizonte",  -19.62,  -43.97),   # MG - Belo Horizonte
    ("BEL", "Belém",            -1.38,  -48.48),   # PA - Belém
    ("JPA", "João Pessoa",      -7.15,  -34.95),   # PB - João Pessoa
    ("CWB", "Curitiba",        -25.53,  -49.17),   # PR - Curitiba
    ("REC", "Recife",           -8.13,  -34.92),   # PE - Recife
    ("THE", "Teresina",         -5.09,  -42.80),   # PI - Teresina
    ("GIG", "Rio de Janeiro",  -22.81,  -43.25),   # RJ - Rio de Janeiro
    ("NAT", "Natal",            -5.77,  -35.20),   # RN - Natal
    ("POA", "Porto Alegre",    -29.99,  -51.17),   # RS - Porto Alegre
    ("PVH", "Porto Velho",      -8.77,  -63.90),   # RO - Porto Velho
    ("BVB", "Boa Vista",         2.82,  -60.67),   # RR - Boa Vista
    ("FLN", "Florianópolis",   -27.67,  -48.55),   # SC - Florianópolis
    ("GRU", "São Paulo",       -23.43,  -46.47),   # SP - São Paulo
    ("AJU", "Aracaju",         -11.00,  -37.07),   # SE - Aracaju
    ("PMW", "Palmas",          -10.29,  -48.36),   # TO - Palmas
]

# Rotas com preço (do seu grafo original) e tempo estimado (fictício)
# Formato: (origem, destino, preço, tempo_minutos)
ROUTES = [
    # === HUB NORTE: Manaus ===
    ("MAO", "BEL",  120, 490),    # Manaus - Belém
    ("MAO", "PVH",   90, 350),    # Manaus - Porto Velho
    ("MAO", "BVB",   95, 380),    # Manaus - Boa Vista
    ("MAO", "CGB",  140, 590),    # Manaus - Cuiabá
    ("MAO", "BSB",  180, 830),    # Manaus - Brasília
    
    # === HUB NORDESTE: Recife ===
    ("REC", "FOR",   75, 280),    # Recife - Fortaleza
    ("REC", "SSA",   85, 310),    # Recife - Salvador
    ("REC", "NAT",   50, 180),    # Recife - Natal
    ("REC", "JPA",   35, 120),    # Recife - João Pessoa
    ("REC", "MCZ",   45, 160),    # Recife - Maceió
    ("REC", "AJU",   55, 200),    # Recife - Aracaju
    ("REC", "THE",   90, 340),    # Recife - Teresina
    ("REC", "SLZ",  105, 410),    # Recife - São Luís
    
    # === HUB CENTRO-OESTE: Brasília ===
    ("BSB", "GYN",   55, 200),    # Brasília - Goiânia
    ("BSB", "CGB",   95, 350),    # Brasília - Cuiabá
    ("BSB", "CGR",  110, 420),    # Brasília - Campo Grande
    ("BSB", "CNF",   95, 360),    # Brasília - Belo Horizonte
    ("BSB", "SSA",  120, 460),    # Brasília - Salvador
    ("BSB", "FOR",  150, 620),    # Brasília - Fortaleza
    ("BSB", "BEL",  145, 580),    # Brasília - Belém
    ("BSB", "PMW",   90, 350),    # Brasília - Palmas
    ("BSB", "GIG",  115, 450),    # Brasília - Rio de Janeiro
    
    # === HUB SUDESTE: São Paulo ===
    ("GRU", "GIG",   60, 230),    # São Paulo - Rio de Janeiro
    ("GRU", "CNF",   75, 280),    # São Paulo - Belo Horizonte
    ("GRU", "CWB",   55, 210),    # São Paulo - Curitiba
    ("GRU", "FLN",   85, 310),    # São Paulo - Florianópolis
    ("GRU", "POA",  115, 430),    # São Paulo - Porto Alegre
    ("GRU", "CGR",  100, 390),    # São Paulo - Campo Grande
    ("GRU", "VIX",   90, 350),    # São Paulo - Vitória
    ("GRU", "BSB",  130, 520),    # São Paulo - Brasília
    ("GRU", "SSA",  165, 680),    # São Paulo - Salvador
    ("GRU", "REC",  180, 750),    # São Paulo - Recife
    
    # === ROTAS REGIONAIS NORTE ===
    ("BEL", "SLZ",   85, 320),    # Belém - São Luís
    ("BEL", "MCP",   65, 230),    # Belém - Macapá
    ("MCP", "BVB",   90, 350),    # Macapá - Boa Vista
    ("PVH", "RIO",   75, 280),    # Porto Velho - Rio Branco
    ("PVH", "CGB",  110, 420),    # Porto Velho - Cuiabá
    
    # === ROTAS REGIONAIS NORDESTE ===
    ("FOR", "THE",   70, 250),    # Fortaleza - Teresina
    ("FOR", "NAT",   60, 220),    # Fortaleza - Natal
    ("SSA", "AJU",   50, 180),    # Salvador - Aracaju
    ("SSA", "VIX",   90, 350),    # Salvador - Vitória
    ("SLZ", "THE",   55, 200),    # São Luís - Teresina
    
    # === ROTAS REGIONAIS CENTRO-OESTE ===
    ("GYN", "CGB",  100, 380),    # Goiânia - Cuiabá
    ("CGR", "CGB",   90, 350),    # Campo Grande - Cuiabá
    
    # === ROTAS REGIONAIS SUDESTE ===
    ("CNF", "VIX",   65, 240),    # Belo Horizonte - Vitória
    ("CNF", "GIG",   55, 210),    # Belo Horizonte - Rio de Janeiro
    ("GIG", "VIX",   70, 260),    # Rio de Janeiro - Vitória
    
    # === ROTAS REGIONAIS SUL ===
    ("CWB", "FLN",   50, 180),    # Curitiba - Florianópolis
    ("FLN", "POA",   60, 230),    # Florianópolis - Porto Alegre
    ("CWB", "POA",   80, 290),    # Curitiba - Porto Alegre
    
    # === CONEXÕES ESTRATÉGICAS ===
    ("PMW", "BEL",  110, 420),    # Palmas - Belém
    ("PMW", "SSA",  100, 380),    # Palmas - Salvador
    ("RIO", "MAO",   90, 350),    # Rio Branco - Manaus
    ("MCZ", "AJU",   40, 150),    # Maceió - Aracaju
    ("NAT", "JPA",   35, 120),    # Natal - João Pessoa
]

AIRPORTS_DICT = {
    iata: {"iata": iata, "cidade": cidade, "lat": lat, "lon": lon}
    for iata, cidade, lat, lon in AIRPORTS
}

def get_adjacency(criterion: str = "tempo") -> dict:
    idx = 2 if criterion == "tempo" else 3
    graph = {iata: [] for iata, *_ in AIRPORTS}
    for row in ROUTES:
        origem, destino, peso = row[0], row[1], row[idx]
        graph[origem].append((destino, peso))
        graph[destino].append((origem, peso))
    return graph