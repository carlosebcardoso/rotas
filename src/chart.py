import plotly.graph_objects as go
from mock import AIRPORTS, AIRPORTS_DICT, ROUTES
from algorithms import get_route_weight, airport_label


def _edge_label(origem: str, destino: str, criterion: str) -> str:
    w = get_route_weight(origem, destino, criterion)
    return f"{w}min" if criterion == "tempo" else f"R${w}"


def _edge_label_color(criterion: str) -> str:
    return "#92400e" if criterion == "tempo" else "#14532d"


def build_figure(
    first: str | None = None,
    second: str | None = None,
    path_edges: list | None = None,
    criterion: str = "tempo",
) -> go.Figure:
    path_edges = path_edges or []
    path_edge_set = {(a, b) for a, b in path_edges} | {(b, a) for a, b in path_edges}

    fig = go.Figure()

    for row in ROUTES:
        origem, destino = row[0], row[1]
        on_path = (origem, destino) in path_edge_set
        o, d = AIRPORTS_DICT[origem], AIRPORTS_DICT[destino]

        fig.add_trace(go.Scattergeo(
            lat=[o["lat"], d["lat"], None],
            lon=[o["lon"], d["lon"], None],
            mode="lines",
            line=dict(width=3 if on_path else 1.2, color="#f59e0b" if on_path else "#94a3b8"),
            hoverinfo="skip",
            showlegend=False,
        ))

        if on_path:
            fig.add_trace(go.Scattergeo(
                lat=[(o["lat"] + d["lat"]) / 2],
                lon=[(o["lon"] + d["lon"]) / 2],
                mode="text",
                text=[_edge_label(origem, destino, criterion)],
                textfont=dict(size=10, color=_edge_label_color(criterion)),
                hoverinfo="skip",
                showlegend=False,
            ))

    lats, lons, hover_labels, colors, sizes, borders, texts, customdata = [], [], [], [], [], [], [], []

    for iata, cidade, lat, lon in AIRPORTS:
        lats.append(lat)
        lons.append(lon)
        customdata.append(iata)
        texts.append(f"  {iata}")
        hover_labels.append(f"<b>{iata}</b> — {cidade}")

        if iata == first:
            colors.append("#ef4444"); sizes.append(14); borders.append(3)
        elif iata == second:
            colors.append("#3b82f6"); sizes.append(14); borders.append(3)
        else:
            colors.append("#1e40af"); sizes.append(9);  borders.append(1.5)

    fig.add_trace(go.Scattergeo(
        lat=lats, lon=lons,
        mode="markers+text",
        marker=dict(size=sizes, color=colors, line=dict(width=borders, color="#ffffff"), opacity=1.0),
        text=texts,
        textposition="middle right",
        textfont=dict(size=11, color="#1e293b", family="monospace"),
        hovertext=hover_labels,
        hoverinfo="text",
        customdata=customdata,
        showlegend=False,
    ))

    fig.update_geos(
        scope="south america",
        center=dict(lat=-15, lon=-53),
        projection_scale=3.2,
        showland=True,    landcolor="#e2e8f0",
        showocean=True,   oceancolor="#dbeafe",
        showlakes=True,   lakecolor="#bfdbfe",
        showrivers=True,  rivercolor="#93c5fd",
        showcountries=True, countrycolor="#94a3b8", countrywidth=1.2,
        showsubunits=True,  subunitcolor="#cbd5e1",  subunitwidth=0.6,
        bgcolor="rgba(0,0,0,0)",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(bgcolor="rgba(0,0,0,0)"),
        dragmode="pan",
    )

    return fig