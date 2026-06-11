import streamlit as st
from mock import AIRPORTS_DICT
from chart import build_figure
from components import inject_css, render_criterion_toggle, render_airport_selector, render_actions, render_result

st.set_page_config(
    page_title="Planejador de Rotas Aéreas",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

for key, default in [
    ("selected_first",  None),
    ("selected_second", None),
    ("selecting_mode",  "first"),
    ("route_result",    None),
    ("criterion",       "tempo"),
]:
    if key not in st.session_state:
        st.session_state[key] = default

panel, _spacer, canvas, resultado = st.columns([1, 0.04, 2.8, 1])

with panel:
    st.markdown("## Rotas Aéreas")
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
    render_criterion_toggle()
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
    render_airport_selector("first")
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
    render_airport_selector("second")
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
    render_actions()

with canvas:
    path_edges = []
    if st.session_state.route_result:
        _, _, path_edges = st.session_state.route_result

    fig = build_figure(
        first=st.session_state.selected_first,
        second=st.session_state.selected_second,
        path_edges=path_edges or [],
        criterion=st.session_state.criterion,
    )

    event = st.plotly_chart(
        fig,
        width='stretch',
        height=720,
        config={
            "scrollZoom": True,
            "displayModeBar": True,
            "modeBarButtonsToRemove": [
                "select2d", "lasso2d", "autoScale2d",
                "hoverClosestGeo", "hoverCompareCartesian",
                "toImage", "sendDataToCloud", "toggleSpikelines",
            ],
            "displaylogo": False,
        },
        on_select="rerun",
        selection_mode="points",
        key="map",
    )

    if event and event.selection and event.selection.get("points"):
        clicked_iata = event.selection["points"][0].get("customdata")
        if clicked_iata and clicked_iata in AIRPORTS_DICT:
            first  = st.session_state.selected_first
            second = st.session_state.selected_second

            if clicked_iata not in (first, second):
                if st.session_state.selecting_mode == "first":
                    st.session_state.selected_first = clicked_iata
                    if not second:
                        st.session_state.selecting_mode = "second"
                else:
                    st.session_state.selected_second = clicked_iata

                st.session_state.route_result = None
                st.rerun()

    criterion = st.session_state.criterion
    caption = (
        "Amarelo = rota mais rápida  ·  Labels = minutos por trecho"
        if criterion == "tempo"
        else "Amarelo = rota mais barata  ·  Labels = preço por trecho"
    )
    st.caption(f"Vermelho = origem  ·  Azul = destino  ·  {caption}")

with resultado:
    render_result()