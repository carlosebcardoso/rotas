def acha_menores(g, v_origem):
  menores_custos = {v: float('inf') for v in g}
  menores_custos[v_origem] = 0
  verificados = set()

  while len(verificados) < len(g):
    v_atual = None
    menor_custo = float('inf')

    for v in g:
      if v not in verificados and menores_custos[v] < menor_custo:
        menor_custo = menores_custos[v]
        v_atual = v
    
    if v_atual is None:
      break

    verificados.add(v_atual)

    for v_destino, custo in g[v_atual]:
      novo_custo = menores_custos[v_atual] + custo

      if novo_custo < menores_custos[v_destino]:
        menores_custos[v_destino] = novo_custo

  return menores_custos
