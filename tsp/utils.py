import networkx as nx
import numpy as np

def create_graph_from_path(path: str) -> tuple[nx.Graph, dict]:
    info = {
        "name": "",
        "comment": "",
        "type": "",
        "dimension": "",
        "edge_weight_type": "",
    }

    file = open(path)

    # Le as informacoes adicionais da entrada
    info["name"] = file.readline().split(':')[1].strip()
    info["comment"]  = file.readline().split(':')[1]
    info["type"]  = file.readline().split(':')[1]
    info["dimension"]  = int(file.readline().split(':')[1])
    info["edge_weight_type"]  = file.readline().split(':')[1]
    file.readline()

    
    graph = nx.Graph()

    while True:
        line = file.readline()
        if "EOF" in line:
            break
        id, x, y = line.split()
        graph.add_node(int(id) - 1, pos=(float(x), float(y)))

    for vi in graph.nodes:
        for vj in graph.nodes:
            xi, yi = graph.nodes[vi]['pos']
            xj, yj = graph.nodes[vj]['pos']

            distance = np.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
            graph.add_edge(vi, vj, weight=distance)
    
    return graph, info