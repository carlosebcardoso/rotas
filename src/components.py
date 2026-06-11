import streamlit as st
from algorithms import airport_label, dijkstra, calc_secondary_total, format_total, get_route_weight


CSS = """
<style>
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }

.panel-title {
    font-size: 0.70rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.25rem;
}
.node-badge {
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: #111827;
    margin-bottom: 0.5rem;
}
.node-badge.origin { border-left: 3px solid #ef4444; }
.node-badge.dest   { border-left: 3px solid #3b82f6; }
.node-badge.empty  { color: #9ca3af; font-weight: 400; }
.thin-divider { border: none; border-top: 1px solid #e5e7eb; margin: 1rem 0; }
.route-step {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.85rem;
    color: #374151;
    padding: 0.15rem 0;
}
.route-step .arrow { color: #f59e0b; font-weight: 700; }
</style>
"""

_DIVIDER = '<hr class="thin-divider">'


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def render_criterion_toggle():
    st.markdown('<p class="panel-title">Otimizar por</p>', unsafe_allow_html=True)

    col_t, col_p = st.columns(2)
    with col_t:
        active = st.session_state.criterion == "tempo"
        if st.button("⏱ Tempo", key="btn_tempo", width='stretch',
                     type="primary" if active else "secondary"):
            if not active:
                st.session_state.criterion = "tempo"
                st.session_state.route_result = None
                st.rerun()

    with col_p:
        active = st.session_state.criterion == "preco"
        if st.button("💰 Preço", key="btn_preco", width='stretch',
                     type="primary" if active else "secondary"):
            if not active:
                st.session_state.criterion = "preco"
                st.session_state.route_result = None
                st.rerun()

    hint = "Menor tempo de voo total" if st.session_state.criterion == "tempo" else "Menor custo total de passagens"
    st.caption(hint)


def render_airport_selector(role: str):
    is_origin = role == "first"
    title     = "Origem" if is_origin else "Destino"
    css_class = "origin" if is_origin else "dest"
    key_btn   = f"btn_{role}"
    selected  = st.session_state.selected_first if is_origin else st.session_state.selected_second
    selecting = st.session_state.selecting_mode == role

    st.markdown(f'<p class="panel-title">{title}</p>', unsafe_allow_html=True)

    if selected:
        st.markdown(
            f'<div class="node-badge {css_class}">{airport_label(selected)}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="node-badge empty">Clique em um aeroporto no mapa</div>',
            unsafe_allow_html=True,
        )

    label = f"Selecionando {title.lower()}..." if selecting else f"Selecionar {title.lower()}"
    if st.button(label, key=key_btn, width='stretch',
                 type="primary" if selecting else "secondary"):
        st.session_state.selecting_mode = role
        st.rerun()


def render_actions():
    rota_pronta = bool(st.session_state.selected_first and st.session_state.selected_second)

    if rota_pronta:
        if st.button("Calcular rota", type="primary", width='stretch'):
            path, total, edges = dijkstra(
                st.session_state.selected_first,
                st.session_state.selected_second,
                st.session_state.criterion,
            )
            st.session_state.route_result = (path, total, edges)
    else:
        st.button("Calcular rota", disabled=True, width='stretch')

    if st.button("Limpar seleção", width='stretch'):
        st.session_state.selected_first  = None
        st.session_state.selected_second = None
        st.session_state.selecting_mode  = "first"
        st.session_state.route_result    = None
        st.rerun()


def render_result():
    if not st.session_state.route_result:
        return

    path, total, _ = st.session_state.route_result
    criterion       = st.session_state.criterion
    secondary       = "preco" if criterion == "tempo" else "tempo"

    st.markdown("## Resultado")
    st.markdown(_DIVIDER, unsafe_allow_html=True)

    if path is None:
        st.error("Nenhuma rota encontrada.")
        return

    secondary_total = calc_secondary_total(path, secondary)
    primary_label   = "Tempo total" if criterion == "tempo" else "Custo total"
    secondary_label = "Custo total" if criterion == "tempo" else "Tempo total"

    st.metric(primary_label,   format_total(total,           criterion))
    st.metric(secondary_label, format_total(secondary_total, secondary))

    st.markdown(_DIVIDER, unsafe_allow_html=True)
    st.markdown('<p class="panel-title">Escalas</p>', unsafe_allow_html=True)

    for i, stop in enumerate(path):
        if i == 0:
            st.markdown(
                f'<div class="route-step">🛫 {airport_label(stop)}</div>',
                unsafe_allow_html=True,
            )
        else:
            w     = get_route_weight(path[i - 1], stop, criterion)
            label = f"{w} min" if criterion == "tempo" else f"R$ {w:,}".replace(",", ".")
            st.markdown(
                f'<div class="route-step">'
                f'<span class="arrow">→</span> {airport_label(stop)}'
                f'<span style="margin-left:auto;font-size:0.75rem;color:#6b7280;">{label}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )