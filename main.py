import sys
import argparse
import networkx as nx
import tracemalloc
import time
from multiprocessing import Process, Queue
from tsp import branch_bound, christofides, twice_around, utils

def execute_algorithm(func, graph, queue):
    """Executa o algoritmo e envia o resultado para a fila."""
    try:
        start_time = time.time()
        path, cost = func.solve(graph)
        end_time = time.time()
        queue.put((path, cost, end_time - start_time))
    except Exception as e:
        queue.put(e)

def main():
    parser = argparse.ArgumentParser(description="Resolução do TSP utilizando diferentes algoritmos.")
    parser.add_argument("algorithm", choices=["branch-bound", "twice-around", "christofides"],
                        help="Escolha o algoritmo a ser utilizado.")
    parser.add_argument("input", type=str, help="Caminho para o arquivo de entrada do grafo.")
    parser.add_argument("--memory", action="store_true", help="Rastrear uso de memória durante a execução.")
    
    args = parser.parse_args()

    if args.algorithm == "branch-bound":
        func = branch_bound
    elif args.algorithm == "twice-around":
        func = twice_around
    elif args.algorithm == "christofides":
        func = christofides
    else:
        print(f"Algoritmo {args.algorithm} não identificado.")
        sys.exit(1)

    if args.memory:
        tracemalloc.start()

    graph, info = utils.create_graph_from_path(args.input)

    if args.algorithm == "branch-bound":
        graph = nx.to_numpy_array(graph)

    if args.memory:
        mem_start, _ = tracemalloc.get_traced_memory()
    else:
        mem_start = 0

    timeout = 1800  # 30 minutos
    queue = Queue()
    process = Process(target=execute_algorithm, args=(func, graph, queue))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        timed_out = True
    else:
        timed_out = False

    if args.memory:
        mem_end, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    else:
        mem_end = 0

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
                raise result

            path_result, cost, execution_time = result
            print(f"Nome: {info['name']}")
            print(f"Número de cidades: {info['dimension']}")
            print(f"Custo: {cost:.2f}")
            print(f"Tempo gasto: {execution_time:.2f} segundos")
            if args.memory:
                print(f"Memória usada: {(mem_end - mem_start) / 1024:.2f} KB")
        except Exception as e:
            print(f"Erro ao obter o resultado: {e}")

if __name__ == "__main__":
    main()
