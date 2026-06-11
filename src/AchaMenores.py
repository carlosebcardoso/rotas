def AchaMenores(g, vOrigem):
  menoresCustos = {v: float('inf') for v in g}
  menoresCustos[vOrigem] = 0
  verificados = set()

  while len(verificados) < len(g):
    vAtual = None
    menorCusto = float('inf')

    for v in g:
      if v not in verificados and menoresCustos[v] < menorCusto:
        menorCusto = menoresCustos[v]
        vAtual = v
    
    if vAtual is None:
      break

    verificados.add(vAtual)

    for vDestino, custo in g[vAtual]:
      novoCusto = menoresCustos[vAtual] + custo

      if novoCusto < menoresCustos[vDestino]:
        menoresCustos[vDestino] = novoCusto

  return menoresCustos
