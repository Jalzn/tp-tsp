# Projeto TSP - Comparação de Algoritmos

Este projeto implementa três algoritmos para resolver o Problema do Caixeiro Viajante (TSP):

- Branch and Bound
- Twice Around
- Christofides

Agora é possível rastrear o uso de memória com a flag `--memory`, que ativa o módulo `tracemalloc` para os algoritmos, permitindo avaliar o consumo de memória durante a execução. Vale notar que essa funcionalidade pode impactar o tempo de execução.

## Requisitos

- Python 3.8 ou superior
- Biblioteca numpy
- Biblioteca networkx

## Instalação

Clone o repositório:

```
git clone https://github.com/Jalzn/tp-tsp  
cd tp-tsp  
```

Instale as dependências, se necessário:
```
pip install numpy networkx  
```

## Uso

Execute o programa com o comando:

```
python main.py <algoritmo> <arquivo-de-entrada> [--memory]
```

### Parâmetros

- `<algoritmo>`: Escolha entre "branch-bound", "twice-around" ou "christofides".
- `<arquivo-de-entrada>`: Caminho para o arquivo de entrada contendo a matriz de distâncias em formato do TSPLIB.
- `--memory`: (Opcional) Ativa o rastreamento de memória.

### Exemplo

```
python main.py branch-bound input.tsp
python main.py christofides input.tsp --memory
```

## Formato do Arquivo de Entrada

O arquivo de entrada deve seguir o formato TSPLIB:

```
NAME: Nome do conjunto de dados.
COMMENT: Breve descrição do problema ou mapa.
TYPE: Tipo do problema (deve ser TSP).
DIMENSION: Número de cidades ou nós.
EDGE_WEIGHT_TYPE: Tipo de cálculo de distância entre as cidades (ex.: EUC_2D para distância euclidiana bidimensional).
NODE_COORD_SECTION:
    Cada linha contém o identificador do nó seguido pelas coordenadas (ex.: x y).
EOF: Indica o final do arquivo.
```

## Saída

Ao executar o programa, ele retornará informações detalhadas sobre a execução do algoritmo, incluindo:

- **Nome do problema**: O nome definido no arquivo de entrada (campo NAME).
- **Número de cidades**: O número de nós ou cidades especificados no arquivo de entrada (campo DIMENSION).
- **Custo**: O custo total do caminho encontrado pelo algoritmo (ex.: soma das distâncias percorridas).
- **Tempo gasto**: O tempo total de execução do algoritmo em segundos.
- **Memória usada**: (Se `--memory` for ativado) A quantidade de memória utilizada durante a execução, em kilobytes (KB).

### Exemplo de Saída
```
Nome: alemanha  
Numero de cidades: 6  
Custo: 123.45  
Tempo gasto: 0.42  
Memoria usada: 8.25 KB  
```
Essas informações ajudam a avaliar o desempenho dos algoritmos em diferentes instâncias do problema.

Desenvolvido para fins de pesquisa e comparação de algoritmos de TSP.
