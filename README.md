# Grafos para Navegação

Este projeto explora o uso de estruturas de grafos e árvores aplicadas à navegação de robôs em ambientes com obstáculos.  
A partir de um mapa bidimensional definido por um arquivo de texto, o sistema é capaz de:

- Gerar o grafo de visibilidade com base na posição dos obstáculos;  
- Construir uma árvore geradora mínima (MST) utilizando algoritmos clássicos (Prim ou Kruskal);  
- Encontrar o caminho mais adequado entre dois pontos (inicial e final) dentro do espaço livre;  
- Visualizar graficamente todas as etapas do processo, mostrando o mapa, o grafo, a árvore e o caminho final.  

O objetivo é demonstrar, de forma prática, como conceitos fundamentais de teoria dos grafos e geometria computacional podem ser aplicados à navegação autônoma — simulando o planejamento de trajetória de um robô em um ambiente com múltiplos obstáculos.

---

##  Tecnologias utilizadas

-  Python 3
- Bibliotecas principais:
  - `matplotlib` → visualização dos grafos e caminhos  
  - `shapely` → operações geométricas (detecção de interseção e visibilidade)  
  - `math`, `itertools`, `heapq` → manipulação de coordenadas e algoritmos de busca  

---

## Objetivo do projeto

Este trabalho foi desenvolvido como uma atividade prática sobre o conceito de árvores e busca em grafos,  
explorando algoritmos clássicos de planejamento de movimento em robótica.  

O código foi construído de forma incremental, seguindo as etapas propostas em sala, com foco na clareza e visualização dos resultados.

---

## Estrutura do Projeto

O projeto foi construído de forma modular, dividindo cada etapa em um arquivo separado, o que facilita a leitura e o entendimento do fluxo.  
A primeira etapa corresponde à **leitura do mapa** e à preparação dos dados geométricos que servirão de base para todo o sistema.

---

### 1. Leitura do mapa (`mapa.py`)

O módulo `mapa.py` é responsável por **interpretar o arquivo de texto** que descreve o ambiente de navegação.  
Esse arquivo contém as informações do ponto inicial, ponto final e os vértices de cada obstáculo no plano 2D.

O formato esperado é o seguinte:

- ponto inicial (x_start, y_start)

- ponto final (x_goal, y_goal)

- número de obstáculos (N)

para cada obstáculo:

n_quinas
x1 y1
x2 y2
...
xn yn

---

### Implementação

O código a seguir faz a leitura do arquivo, valida o formato e retorna as estruturas necessárias:

```python
def ler_mapa(arquivo):
    try:
        with open(arquivo, 'r') as f:
            linhas = [linha.strip() for linha in f.readlines() 
                     if linha.strip() and not linha.strip().startswith('#')]
        
        if len(linhas) < 3:
            raise ValueError("Arquivo de mapa incompleto")
        
        q_start = tuple(map(float, linhas[0].split()))
        q_goal = tuple(map(float, linhas[1].split()))
        n_obstaculos = int(linhas[2])
        
        obstaculos = []
        i = 3
        for _ in range(n_obstaculos):
            if i >= len(linhas):
                raise ValueError("Número de obstáculos inconsistente")
            
            n_quinas = int(linhas[i])
            i += 1
            quinas = []
            
            for _ in range(n_quinas):
                if i >= len(linhas):
                    raise ValueError("Número de vértices inconsistente")
                x, y = map(float, linhas[i].split())
                quinas.append((x, y))
                i += 1
            
            obstaculos.append(quinas)
        
        return q_start, q_goal, obstaculos
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado")
        raise
    except ValueError as e:
        print(f"Erro ao ler mapa: {e}")
        raise
    except Exception as e:
        print(f"Erro inesperado: {e}")
        raise
```
---

## Explicação

- q_start e q_goal são tuplas representando as coordenadas inicial e final do robô.
- Cada obstáculo é armazenado como uma lista de vértices (x, y), o que permite usar bibliotecas como shapely para verificar interseções.
- A função retorna: `q_start`, `q_goal` e `obstaculos`, que são usados pelas próximas etapas para montar o grafo de visibilidade.
