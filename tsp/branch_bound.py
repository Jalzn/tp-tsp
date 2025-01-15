import numpy as np
import time

def calcula_limite_inicial(matriz_dist):
    n = len(matriz_dist)
    limite = 0
    for i in range(n):
        arestas = sorted(matriz_dist[i])
        limite += arestas[1] if arestas[0] == 0 else arestas[0]
        limite += arestas[2] if arestas[1] == 0 else arestas[1]
    return limite // 2

def reduz_matriz(matriz):
    n = len(matriz)
    reducao = 0
    matriz_reduzida = matriz.copy()
    for i in range(n):
        min_linha = np.min(matriz_reduzida[i])
        if min_linha != float('inf') and min_linha > 0:
            matriz_reduzida[i] -= min_linha
            reducao += min_linha
    for j in range(n):
        min_coluna = np.min(matriz_reduzida[:, j])
        if min_coluna != float('inf') and min_coluna > 0:
            matriz_reduzida[:, j] -= min_coluna
            reducao += min_coluna
    return matriz_reduzida, reducao

def calcula_custo_insercao(matriz_dist, origem, destino, visitados):
    if len(visitados) == len(matriz_dist) - 1:
        return matriz_dist[origem][destino] + matriz_dist[destino][visitados[0]]
    return matriz_dist[origem][destino]

def limite_inferior(matriz_dist, caminho_atual, nao_visitados):
    n = len(matriz_dist)
    if len(nao_visitados) <= 2:
        custo = 0
        for i in range(len(caminho_atual) - 1):
            custo += matriz_dist[caminho_atual[i]][caminho_atual[i + 1]]
        if len(nao_visitados) == 1:
            ultimo = list(nao_visitados)[0]
            custo += matriz_dist[caminho_atual[-1]][ultimo]
            custo += matriz_dist[ultimo][caminho_atual[0]]
        return custo
    indices = list(nao_visitados)
    if caminho_atual:
        indices.append(caminho_atual[-1])
    submatriz = matriz_dist[np.ix_(indices, indices)]
    _, reducao = reduz_matriz(submatriz)
    custo_atual = 0
    for i in range(len(caminho_atual) - 1):
        custo_atual += matriz_dist[caminho_atual[i]][caminho_atual[i + 1]]
    return custo_atual + reducao

def solve(matriz_dist):
    n = len(matriz_dist)
    melhor_caminho = None
    melhor_custo = float('inf')
    inicio = time.time()
    ultimo_print = inicio
    limite_inicial = calcula_limite_inicial(matriz_dist)
    pilha = [(0, limite_inicial, [0], set(range(1, n)))]
    podas = 0
    iteracoes = 0
    
    while pilha:
        iteracoes += 1
        tempo_atual = time.time()
        if tempo_atual - ultimo_print >= 60:
            print(f"Tempo decorrido: {(tempo_atual - inicio) / 60:.2f} minutos")
            print(f"Melhor custo atual: {melhor_custo:.2f}")
            print(f"Número de podas: {podas}")
            print(f"Tamanho da pilha: {len(pilha)}")
            ultimo_print = tempo_atual
        
        custo_atual, limite, caminho_atual, nao_visitados = pilha.pop()
        if limite >= melhor_custo:
            podas += 1
            continue
        if not nao_visitados:
            custo_total = custo_atual + matriz_dist[caminho_atual[-1]][0]
            if custo_total < melhor_custo:
                melhor_custo = custo_total
                melhor_caminho = caminho_atual[:]
            continue
        ordenados = sorted(
            nao_visitados,
            key=lambda x: calcula_custo_insercao(matriz_dist, caminho_atual[-1], x, caminho_atual)
        )
        for prox in ordenados:
            novo_custo = custo_atual + matriz_dist[caminho_atual[-1]][prox]
            if novo_custo >= melhor_custo:
                podas += 1
                continue
            novos_nao_visitados = nao_visitados - {prox}
            novo_caminho = caminho_atual + [prox]
            novo_limite = limite_inferior(matriz_dist, novo_caminho, novos_nao_visitados)
            if novo_limite < melhor_custo:
                pilha.append((novo_custo, novo_limite, novo_caminho, novos_nao_visitados))
    
    return melhor_caminho, melhor_custo
