# ui.py
import streamlit as st
from mock import build_nodes, build_edges, get_adjacency, ROUTES, AIRPORTS, AIRPORTS_DICT
from streamlit_agraph import agraph, Config, Node

# Inicializa session state para seleção de dois nós
if "selected_first" not in st.session_state:
    st.session_state.selected_first = None
if "selected_second" not in st.session_state:
    st.session_state.selected_second = None
if "selecting_mode" not in st.session_state:
    st.session_state.selecting_mode = "first"  # "first" ou "second"
if "last_clicked" not in st.session_state:
    st.session_state.last_clicked = None

# Título
st.title("🗺️ Planejador de Rotas Aéreas")
st.markdown("---")

# Layout com 3 colunas: UI de seleção, gráfico e informações
col1, col2 = st.columns([1, 2])

# ==================== COLUNA 1: CONTROLES ====================
col1.subheader("🎮 Controles de Seleção")
col1.markdown("### ✈️ Seleção Atual")

# Primeiro nó
col1.markdown("**1️⃣ Primeiro Nó (Origem)**")
if st.session_state.selected_first:
    airport = AIRPORTS_DICT[st.session_state.selected_first]
    col1.success(f"✅ {airport['iata']} - {airport['cidade']}")
    if col1.button("🔄 Trocar Primeiro Nó", key="change_first"):
        st.session_state.selecting_mode = "first"
        st.info("Modo: Selecione o PRIMEIRO nó")
        st.rerun()
else:
    col1.warning("⏳ Nenhum nó selecionado")
    if col1.button("🎯 Selecionar Primeiro Nó", key="select_first"):
        st.session_state.selecting_mode = "first"
        st.info("Modo: Selecione o PRIMEIRO nó")
        st.rerun()

col1.markdown("---")

# Segundo nó
col1.markdown("**2️⃣ Segundo Nó (Destino)**")
if st.session_state.selected_second:
    airport = AIRPORTS_DICT[st.session_state.selected_second]
    col1.success(f"✅ {airport['iata']} - {airport['cidade']}")
    if col1.button("🔄 Trocar Segundo Nó", key="change_second"):
        st.session_state.selecting_mode = "second"
        st.info("Modo: Selecione o SEGUNDO nó")
        st.rerun()
else:
    col1.warning("⏳ Nenhum nó selecionado")
    if col1.button("🎯 Selecionar Segundo Nó", key="select_second"):
        st.session_state.selecting_mode = "second"
        st.info("Modo: Selecione o SEGUNDO nó")
        st.rerun()

col1.markdown("---")

# Indicador do modo atual
col1.markdown("### 🎯 Modo de Seleção Atual")
if st.session_state.selecting_mode == "first":
    col1.info("🔴 **Modo: Primeiro Nó** (Clique no mapa para selecionar a origem)")
else:
    col1.info("🔵 **Modo: Segundo Nó** (Clique no mapa para selecionar o destino)")

col1.markdown("---")

# Função para planejar rota
def planejar_rota():
    """Função temporária para planejar rota"""
    first = st.session_state.selected_first
    second = st.session_state.selected_second
    print(f"🛫 Planejando rota de {first} ({AIRPORTS_DICT[first]['cidade']}) para {second} ({AIRPORTS_DICT[second]['cidade']})")
    col1.success(f"✅ Rota planejada de {first} para {second}! (Verifique o console)")
    # Aqui você vai adicionar a lógica do Dijkstra depois

# Botão Planejar Rota
rota_pronta = (st.session_state.selected_first is not None and 
               st.session_state.selected_second is not None)

if rota_pronta:
    col1.success("✅ **2 nós selecionados!** Pronto para planejar rota!")
    if col1.button("🛫 Planejar Rota", type="primary", use_container_width=True):
        planejar_rota()
else:
    faltam = 2 - sum([st.session_state.selected_first is not None, 
                      st.session_state.selected_second is not None])
    col1.error(f"❌ **Faltam {faltam} nó(s)** para planejar rota")
    col1.button("🛫 Planejar Rota", disabled=True, use_container_width=True)

col1.markdown("---")

# Botão para limpar tudo
if col1.button("🗑️ Limpar todas as seleções", use_container_width=True):
    st.session_state.selected_first = None
    st.session_state.selected_second = None
    st.session_state.selecting_mode = "first"
    st.rerun()

# ==================== COLUNA 2: MAPA ====================
col2.subheader("🗺️ Mapa de Aeroportos")
col2.caption("💡 Clique nos aeroportos para selecionar | 🔴 Vermelho = Primeiro nó | 🔵 Turquesa = Segundo nó")

# Função para construir nós com cores baseadas na seleção
def build_nodes_with_selection(selected_first=None, selected_second=None):
    """Constrói nós com cores diferentes baseado na seleção"""
    nodes = []
    for iata, cidade, x, y in AIRPORTS:
        # Define a cor baseado no estado de seleção
        if iata == selected_first:
            color = "#FF6B6B"  # Vermelho para primeiro nó
            size = 35
            border_width = 3
        elif iata == selected_second:
            color = "#4ECDC4"  # Turquesa para segundo nó
            size = 35
            border_width = 3
        else:
            color = "#378ADD"  # Azul padrão
            size = 20
            border_width = 1
        
        node = Node(
            id=iata,
            label=f"{iata}\n{cidade}",
            size=size,
            color=color,
            font={"color": "#fff", "size": 11},
            x=x * 1.0,
            y=y * 1.0,
            border_width=border_width,
        )
        nodes.append(node)
    return nodes

# Configuração do grafo
config = Config(
    width=650,
    height=550,
    directed=True,
    physics=False,  # Desligar physics para usar coordenadas fixas
    hierarchical=False,
    nodeHighlightBehavior=True,   # destaca vizinhos ao hover
    highlightColor="#EF9F27",
    collapsible=False,
    selectable=True
)

# Constrói nós com as seleções atuais
nodes = build_nodes_with_selection(st.session_state.selected_first, st.session_state.selected_second)
edges = build_edges()  # Suas arestas originais

# Renderiza o grafo - retorna o ID do nó clicado
clicked_node_id = agraph(
    nodes=nodes, 
    edges=edges, 
    config=config
)

# Processa o clique no nó
if clicked_node_id and clicked_node_id != st.session_state.last_clicked:
    st.session_state.last_clicked = clicked_node_id
    
    # Verifica se o nó já está selecionado em alguma posição
    if clicked_node_id == st.session_state.selected_first:
        col2.warning(f"⚠️ Aeroporto {clicked_node_id} já está selecionado como PRIMEIRO nó!")
    elif clicked_node_id == st.session_state.selected_second:
        col2.warning(f"⚠️ Aeroporto {clicked_node_id} já está selecionado como SEGUNDO nó!")
    else:
        # Seleciona baseado no modo atual
        if st.session_state.selecting_mode == "first":
            st.session_state.selected_first = clicked_node_id
            col2.success(f"✅ Primeiro nó selecionado: {clicked_node_id} - {AIRPORTS_DICT[clicked_node_id]['cidade']}")
            # Automaticamente muda para segundo modo após selecionar primeiro
            if st.session_state.selected_second is None:
                st.session_state.selecting_mode = "second"
                st.info("🔄 Modo alterado automaticamente para: SEGUNDO nó")
        else:
            st.session_state.selected_second = clicked_node_id
            col2.success(f"✅ Segundo nó selecionado: {clicked_node_id} - {AIRPORTS_DICT[clicked_node_id]['cidade']}")
            # Não muda o modo automaticamente para permitir trocas
        
        st.rerun()

# ==================== SEÇÃO DE INFORMAÇÕES ====================
st.markdown("---")
st.subheader("📊 Resumo da Seleção")

col_info1, col_info2, col_info3 = st.columns(3)

# Coluna 1 - Primeiro Nó
first_info = "Não selecionado"
if st.session_state.selected_first:
    airport = AIRPORTS_DICT[st.session_state.selected_first]
    first_info = f"{airport['iata']} - {airport['cidade']}"

col_info1.metric(
    "Primeiro Nó (Origem)",
    first_info,
    delta=None
)

# Coluna 2 - Segundo Nó
second_info = "Não selecionado"
if st.session_state.selected_second:
    airport = AIRPORTS_DICT[st.session_state.selected_second]
    second_info = f"{airport['iata']} - {airport['cidade']}"

col_info2.metric(
    "Segundo Nó (Destino)",
    second_info,
    delta=None
)

# Coluna 3 - Status
rota_pronta = (st.session_state.selected_first is not None and 
               st.session_state.selected_second is not None)
if rota_pronta:
    status = "Pronto 🟢"
else:
    faltam = 2 - sum([st.session_state.selected_first is not None, 
                      st.session_state.selected_second is not None])
    status = f"Faltam {faltam} 🔴"

col_info3.metric(
    "Status",
    status,
    delta=None
)

# Mostra informações detalhadas se ambos estiverem selecionados
if st.session_state.selected_first and st.session_state.selected_second:
    st.markdown("---")
    st.subheader("📍 Detalhes da Rota")
    
    airport1 = AIRPORTS_DICT[st.session_state.selected_first]
    airport2 = AIRPORTS_DICT[st.session_state.selected_second]
    
    col_det1, col_det2 = st.columns(2)
    
    col_det1.markdown(f"**Origem:** {airport1['iata']} - {airport1['cidade']}")
    col_det1.markdown(f"**Coordenadas:** ({airport1['x']}, {airport1['y']})")
    
    col_det2.markdown(f"**Destino:** {airport2['iata']} - {airport2['cidade']}")
    col_det2.markdown(f"**Coordenadas:** ({airport2['x']}, {airport2['y']})")