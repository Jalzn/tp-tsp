import networkx as nx
from itertools import combinations

def solve(G):
    agm = nx.minimum_spanning_tree(G)
    
    nos_impares = []
    for no, grau in agm.degree():
        if grau % 2 == 1:
            nos_impares.append(no)
    
    subgrafo_impares = nx.Graph()
    for u, v in combinations(nos_impares, 2):
        peso = G[u][v]['weight']
        subgrafo_impares.add_edge(u, v, weight=-peso)
    
    emparelhamento_max = nx.max_weight_matching(subgrafo_impares, maxcardinality=True)
    
    multigrafo = nx.MultiGraph()
    multigrafo.add_edges_from(agm.edges(data=True))
    for u, v in emparelhamento_max:
        multigrafo.add_edge(u, v, weight=G[u][v]['weight'])
    
    circuito_euler = list(nx.eulerian_circuit(multigrafo))
    
    caminho = []
    for u, v in circuito_euler:
        if u not in caminho:
            caminho.append(u)
    caminho.append(caminho[0])
    
    custo_total = 0
    for i in range(len(caminho) - 1):
        custo_total += G[caminho[i]][caminho[i + 1]]['weight']
    
    return caminho, custo_total
