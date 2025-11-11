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

---

### 2. Criação do Grafo de Visibilidade (`grafo.py`)

Após a leitura do mapa, a próxima etapa é a geração do grafo de visibilidade.  
Essa fase consiste em identificar quais vértices do ambiente podem “se ver” sem que uma linha entre eles atravesse nenhum obstáculo.  
O resultado é um grafo onde cada vértice representa um ponto do mapa e cada aresta representa uma conexão direta possível.

---

### Lógica geral

1. Cada vértice de todos os obstáculos é adicionado a uma lista de pontos.  
2. Para cada par de vértices distintos `(v1, v2)`, o algoritmo testa se o segmento entre eles é visível, ou seja:  
   - Não cruza nenhum obstáculo;  
   - Está completamente dentro da área livre.  
3. Se a linha for visível, adiciona-se uma aresta ponderada entre `v1` e `v2`, cujo peso é a distância euclidiana entre os pontos.

O grafo resultante é representado como um dicionário de adjacência:  
```python
grafo[v1] = [(v2, distancia), (v3, distancia), ...]
```

---

### Implementação

A função `grafo_visibilidade()` recebe os pontos inicial e final e a lista de obstáculos e retorna o grafo de visibilidade completo:

```python
def grafo_visibilidade(q_start, q_goal, obstaculos, max_distancia=None, debug=False):
    # Coletar todos os vértices
    vertices = [q_start, q_goal]
    for obst in obstaculos:
        vertices.extend(obst)
    
    # Inicializar o grafo
    G = {v: [] for v in vertices}
    
    # Testar visibilidade entre todos os pares de vértices
    total_pares = 0
    conexoes = 0
    
    for v1, v2 in itertools.combinations(vertices, 2):
        total_pares += 1
        distancia = math.dist(v1, v2)
        
        # Otimização: ignorar conexões muito distantes (se especificado)
        if max_distancia and distancia > max_distancia:
            continue
        
        # Verificar se a linha entre v1 e v2 está livre
        livre = linha_livre(v1, v2, obstaculos)
        
        if livre:
            G[v1].append((v2, distancia))
            G[v2].append((v1, distancia))
            conexoes += 1
        else:
            if debug:
                # Log leve para entender porque nenhuma aresta existe
                print(f"bloqueado: {v1} <-> {v2} (dist={distancia:.2f})")
    
    if debug:
        print(f"Grafo criado: {len(vertices)} vértices, {conexoes} arestas")
        print(f"Testados {total_pares} pares de vértices")
        # graus
        graus = {v: len(adj) for v, adj in G.items()}
        degs = sorted(graus.items(), key=lambda x: -x[1])
        print("Top graus (vértice: grau):", degs[:6])
    
    return G
```

O módulo `geometria.py` define funções utilitárias para as operações geométricas:

```python
def dist(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])
```
```python
def ponto_dentro_poligono(p, poligono):
    return Polygon(poligono).covers(Point(p))
```
```python
def intersecao(p1, q1, p2, q2):
    return LineString([p1, q1]).intersects(LineString([p2, q2]))
```
```python
def linha_livre(p1, p2, obstaculos):
    linha = LineString([p1, p2])
    for obst in obstaculos:
        pol = Polygon(obst)
        if pol.is_empty:
            continue

        # Se a linha cruza o polígono (intersects) e não apenas toca (touches)
        if linha.intersects(pol) and not linha.touches(pol):
            return False

    return True
```

---

### Visualização

A função `plotar_grafo()` (no módulo `plots.py`) permite visualizar o grafo sobre o mapa, mostrando os vértices, arestas visíveis e os obstáculos.
Com o exemplo de mapa de `mapa.txt` temos a seguinte visualização:

<p align="center">
  <img src="Prints/Grafo_visibilidade.png" alt="Grafo de Visibilidade" width="600"/>
</p>

Essa visualização é fundamental para validar o comportamento do grafo de visibilidade antes das etapas seguintes (geração da árvore e busca de caminho).

---

### 3. Geração da Árvore Geradora Mínima (`arvore.py`)

Com o grafo de visibilidade construído, o próximo passo é reduzi-lo a uma estrutura mínima de conexões.  
Isso é feito aplicando um algoritmo de Árvore Geradora Mínima (MST), que conecta todos os vértices do grafo com o menor custo total possível.

Essa árvore representa a estrutura mínima de navegação do robô, preservando a conectividade entre os vértices relevantes sem criar ciclos desnecessários.

---

### Lógica geral

O algoritmo percorre o grafo escolhendo arestas de menor peso que não formam ciclos, até conectar todos os vértices.

---

### Implementação

O projeto implementa o algoritmo de Prim, por ser eficiente e fácil de adaptar para grafos representados por dicionários de adjacência.

```python
def prim(grafo, inicio):
    visitado = set()
    mst = []
    pq = []  # fila de prioridade (peso, origem, destino)
    total_peso = 0.0

    def adicionar_arestas(v):
        visitado.add(v)
        for (viz, peso) in grafo.get(v, []):
            if viz not in visitado:
                heapq.heappush(pq, (peso, v, viz))

    # Iniciar do vértice fornecido
    adicionar_arestas(inicio)

    # Construir a MST
    while pq:
        peso, u, v = heapq.heappop(pq)
        if v not in visitado:
            mst.append((u, v, peso))
            total_peso += peso
            adicionar_arestas(v)

    return mst, total_peso, visitado
```

### Visualização
A função `plotar_mst()` (em `plots.py`) exibe a árvore gerada, destacando as arestas que conectam os vértices escolhidos pelo algoritmo.
Com o exemplo de mapa de `mapa.txt` temos a seguinte visualização:

<p align="center">
  <img src="Prints/Grafo_MST.png" alt="Árvore Geradora Mínima" width="600"/>
</p>

Essa visualização ajuda a confirmar que a árvore cobre todas as regiões navegáveis do mapa, conectando os vértices visíveis sem redundância.

---

### 4. Identificação do Vértice Mais Próximo (`verticeMaisProximo()`)

Com a árvore geradora mínima construída, o próximo passo é ligar o robô ao grafo,  
encontrando o vértice mais próximo de sua posição inicial (`q_start`) e final (`q_goal`).

Essa função é fundamental para permitir que o algoritmo de busca (etapa seguinte) saiba onde começar e onde terminar dentro da estrutura da árvore.

---

### Lógica geral

1. A função percorre todos os vértices da árvore;  
2. Calcula a distância euclidiana entre cada vértice e o ponto dado;  
3. Retorna o vértice cuja distância é a menor encontrada.

Esse processo é feito tanto para o ponto inicial (`q_start`) quanto para o ponto final (`q_goal`).

---

### Implementação

O projeto implementa a função `verticeMaisProximo()` no módulo `arvore.py`

```python
def verticeMaisProximo(ponto, arvore):
    # validar ponto
    if not (isinstance(ponto, (tuple, list)) and len(ponto) == 2):
        raise ValueError("Ponto deve ser tupla/lista de 2 floats")

    # extrair vértices
    if isinstance(arvore, dict):
        vertices = list(arvore.keys())
    else:
        vertices = set()
        for u, v, _ in arvore:
            vertices.add(u)
            vertices.add(v)
        vertices = list(vertices)

    if len(vertices) == 0:
        raise ValueError("Árvore está vazia — nenhum vértice para examinar")

    # calcular mais próximo
    menor_dist = float('inf')
    mais_prox = None
    for v in vertices:
        d = math.dist(ponto, v)
        if d < menor_dist:
            menor_dist = d
            mais_prox = v

    return mais_prox
```

---

### 5. Algoritmo de Busca na Árvore (`caminho.py`)

Com os vértices inicial e final identificados, o sistema agora precisa encontrar o caminho que conecta esses dois pontos na árvore geradora mínima.

---

### Lógica geral

1. O algoritmo começa no vértice inicial (`v_inicio`);  
2. Explora recursivamente cada vizinho até encontrar o vértice final (`v_final`);  
3. Mantém um registro do caminho percorrido para retornar a sequência completa de vértices.

---

### Implementação

Por se tratar de uma árvore, não há necessidade de heurísticas ou filas de prioridade, basta uma busca recursiva ou iterativa. Como a MST é uma estrutura sem ciclos e com caminho único entre quaisquer dois vértices, um algoritmo simples de busca em profundidade (DFS) é suficiente para encontrar o trajeto entre os nós desejados.

```python
def buscarCaminho(v_inicio, v_fim, arvore):
    # Validações
    if not arvore:
        print("Árvore vazia fornecida")
        return None, 0
    
    # Construir adjacência com pesos
    adj = construir_adjacencia(arvore)
    
    # Verificar se os vértices existem
    if v_inicio not in adj:
        print(f"Vértice inicial {v_inicio} não está na árvore")
        return None, 0
    if v_fim not in adj:
        print(f"Vértice final {v_fim} não está na árvore")
        return None, 0
    
    # DFS com backtracking para encontrar o caminho
    visitados = set()
    caminho = []
    distancia_total = [0]  # Lista para poder modificar em função aninhada
    
    def dfs(atual, dist_acumulada):
        """Busca em profundidade recursiva."""
        visitados.add(atual)
        caminho.append(atual)
        
        # Se encontrou o destino
        if atual == v_fim:
            distancia_total[0] = dist_acumulada
            return True
        
        # Explorar vizinhos
        for (viz, peso) in adj.get(atual, []):
            if viz not in visitados:
                if dfs(viz, dist_acumulada + peso):
                    return True
        
        # Backtracking: remover vértice se não levou ao destino
        caminho.pop()
        return False
    
    # Executar busca
    if dfs(v_inicio, 0):
        return caminho, distancia_total[0]
    else:
        return None, 0
```

---

### 6. Plotagem do Caminho Final (`plots.py`)

A etapa final do projeto é a visualização do caminho encontrado sobre o mapa. Essa parte é fundamental para validar visualmente os resultados de todas as etapas anteriores: do grafo de visibilidade à árvore geradora mínima, até o trajeto final do robô.

O módulo `plots.py` centraliza todas as funções de plotagem, garantindo consistência estética entre os gráficos.

---

### Lógica geral

Assim como as demais plotagens, a visualização do caminho ocorre com a mesma lógica, com algumas pequenas diferenças entre cada plotagem.

1. Desenha todos os obstáculos no mapa, com contornos visíveis e preenchimento leve;  
2. Exibe todas as arestas do grafo de visibilidade, em cinza claro e pouca opacidade;  
3. Destaca o caminho final entre o ponto inicial e final em vermelho;  
4. Mostra marcadores distintos para o ponto inicial (`q_start`) e final (`q_goal`).

---

### Implementação

```python
def plotar_caminho(caminho, obstaculos, q_start, q_goal, grafo=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Obstáculos
    plotar_obstaculos(obstaculos, ax, "gainsboro", "gray", 0.7, 2.0, 1, 2)

    # Grafo de visibilidade
    if grafo:
        for u in grafo:
            for v, _ in grafo[u]:
                ax.plot(
                    [u[0], v[0]], [u[1], v[1]],
                    color='lightgray', linewidth=1, alpha=0.8, zorder=1
                )

    # Caminho final
    if caminho and len(caminho) > 1:
        for i in range(len(caminho) - 1):
            x0, y0 = caminho[i]
            x1, y1 = caminho[i + 1]
            ax.plot(
                [x0, x1], [y0, y1],
                color='red', linewidth=3.5, alpha=0.95, zorder=5
            )

    # Vértices do caminho
    if caminho:
        xs, ys = zip(*caminho)
        ax.scatter(xs, ys, s=30, color='darkred', zorder=6, label="Caminho")

    # Ponto inicial e final
    ax.scatter(*q_start, s=120, color='limegreen', marker='o', edgecolors='black',
               label='Ponto inicial (q_start)', zorder=7)
    ax.scatter(*q_goal, s=120, color='red', marker='X', edgecolors='black',
               label='Ponto final (q_goal)', zorder=7)

    # Aparência geral
    ax.set_title("Caminho Final", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, linestyle="--", alpha=0.25)

    exibicao(ax)
```

---

### Visualização

<p align="center">
  <img src="Prints/Caminho_final.png" alt="Caminho Final" width="600"/>
</p>

A figura acima mostra o resultado final do processo: o caminho encontrado pelo robô a partir do grafo de visibilidade e da árvore geradora mínima, contornando os obstáculos até alcançar o ponto de destino.

---

## Conclusão e Aprendizados

Este projeto integrou, de forma prática e visual, diversos conceitos fundamentais de teoria dos grafos, geometria computacional e planejamento de movimento.  
Ao longo das seis etapas de desenvolvimento, foi possível construir um sistema completo de navegação autônoma em ambiente bidimensional, com detecção de obstáculos, geração de caminhos e visualização do resultado. O projeto possibilitou uma série de aprendizados como:

- Aplicação de grafos de visibilidade para representar regiões navegáveis no plano;  
- Uso de estruturas de árvore (MST) para reduzir o grafo e manter conectividade mínima;  
- Implementação de busca recursiva para encontrar trajetos entre vértices;  
- Utilização de bibliotecas como Shapely e Matplotlib para manipulação geométrica e exibição gráfica;  
- Importância de integrar algoritmos clássicos de grafos com ferramentas de visualização, tornando os resultados mais intuitivos e verificáveis.

A metodologia apresentada serve de base para problemas reais de:

- Navegação de robôs autônomos em ambientes conhecidos;  
- Planejamento de rotas em mapas bidimensionais;  
- Simulação de trajetórias em sistemas de visão computacional e jogos.

Além de reforçar o entendimento dos algoritmos estudados, o projeto proporciona uma visão mais clara de como a teoria se transforma em prática dentro da engenharia de software e da robótica.
