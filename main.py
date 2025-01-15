import sys
import networkx as nx
import resource
import tracemalloc
import time
from multiprocessing import Process, Queue
from tsp import branch_bound, christofides, twice_around, utils

def execute_algorithm(func, graph, queue):
    """Executa o algoritmo e envia o resultado para a fila."""
    try:
        init = time.time()
        path, cost = func.solve(graph)
        end = time.time()
        queue.put((path, cost, end - init))  # Envia os resultados para a fila
    except Exception as e:
        queue.put(e)  # Envia exceções para a fila

def main(algorithm, path: str):
    # tracemalloc.start()
    graph, info = utils.create_graph_from_path(path)
    # current1, _ = tracemalloc.get_traced_memory()
    current1, _ = (0, 0)

    func = None

    if algorithm == "branch-bound":
        func = branch_bound
        graph = nx.to_numpy_array(graph)
    elif algorithm == "twice-around":
        func = twice_around
    elif algorithm == "christofides":
        func = christofides
    else:
        print(f"Failed to identify algorithm {algorithm}")
        return -1

    timeout = 1800  # 30 minutos
    queue = Queue()
    process = Process(target=execute_algorithm, args=(func, graph, queue))
    process.start()
    process.join()

    if process.is_alive():
        process.terminate()
        process.join()
        timed_out = True
    else:
        timed_out = False

    # current2, _ = tracemalloc.get_traced_memory()
    current2, _ = (0, 0)
    # tracemalloc.stop()

    if timed_out:
        print(f"Nome: {info['name']}")
        print(f"Número de cidades: {info['dimension']}")
        print(f"Custo: N/A")
        print(f"Tempo gasto: N/A")
        print(f"Memória usada: N/A")
    else:
        try:
            result = queue.get_nowait()
            if isinstance(result, Exception):
                path_result, cost, execution_time = result
                print(f"Nome: {info['name']}")
                print(f"Número de cidades: {info['dimension']}")
                print(f"Custo: N/A")
                print(f"Tempo gasto: N/A")
                print(f"Memória usada: N/A")
            else:
                path_result, cost, execution_time = result
                print(f"Nome: {info['name']}")
                print(f"Número de cidades: {info['dimension']}")
                print(f"Custo: {cost:2f}")
                print(f"Tempo gasto: {execution_time:.2f} segundos")
                print(f"Memória usada: {(current2 - current1) / 1024:.2f} KB")
        except Exception as e:
            print(f"Erro ao obter o resultado: {e}")


if __name__ == "__main__":
    # 1GB
    memory_limit = 4096 * 1024 * 1024

    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))

    if len(sys.argv) != 3:
        print("./main.py <branch-bound | twice-around | christofides> <input>")
        exit(1)

    try:
        main(sys.argv[1], sys.argv[2])
    except MemoryError:
        print("O programa atingiu o limite de memória.")
