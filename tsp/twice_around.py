import networkx as nx

def solve(G):
    agm = nx.minimum_spanning_tree(G)
    ordem_dfs = list(nx.dfs_preorder_nodes(agm, 0))
    ordem_dfs.append(ordem_dfs[0])
    custo_total = sum(G[ordem_dfs[i]][ordem_dfs[i + 1]]['weight'] for i in range(len(ordem_dfs) - 1))
    return ordem_dfs, custo_total
