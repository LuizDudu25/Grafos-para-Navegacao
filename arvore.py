import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def prim(grafo, inicio):
    """
    Implementa o algoritmo de Prim para encontrar a MST.
    Ideal para grafos densos como grafos de visibilidade.
    
    Args:
        grafo: Dicionário {vértice: [(vizinho, peso), ...]}
        inicio: Vértice inicial (normalmente q_start)
    
    Returns:
        tuple: (mst, total_peso, vertices_alcancados)
        - mst: lista de arestas (u, v, peso)
        - total_peso: soma dos pesos da MST
        - vertices_alcancados: conjunto de vértices na MST
    
    Complexidade: O(E log V) onde E = arestas, V = vértices
    """
    visitado = set()
    mst = []
    pq = []  # fila de prioridade (peso, origem, destino)
    total_peso = 0.0

    def adicionar_arestas(v):
        """Adiciona todas as arestas do vértice v à fila de prioridade."""
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


def validar_mst(grafo, mst, vertices_alcancados):
    """
    Valida se a MST gerada está correta e se o grafo é conexo.
    
    Args:
        grafo: Grafo original
        mst: MST gerada
        vertices_alcancados: Vértices incluídos na MST
    
    Returns:
        dict: Informações sobre a validação
    """
    total_vertices = len(grafo)
    vertices_na_mst = len(vertices_alcancados)
    arestas_esperadas = vertices_na_mst - 1 if vertices_na_mst > 0 else 0
    
    resultado = {
        'valida': len(mst) == arestas_esperadas and vertices_na_mst > 0,
        'total_vertices': total_vertices,
        'vertices_alcancados': vertices_na_mst,
        'arestas_na_mst': len(mst),
        'arestas_esperadas': arestas_esperadas,
        'grafo_conexo': vertices_na_mst == total_vertices,
        'componentes_desconexos': total_vertices - vertices_na_mst
    }
    
    return resultado


def estatisticas_mst(mst):
    """
    Calcula estatísticas detalhadas da MST.
    
    Returns:
        dict: Estatísticas da MST
    """
    if not mst:
        return {
            'peso_total': 0,
            'peso_medio': 0,
            'peso_min': 0,
            'peso_max': 0,
            'num_arestas': 0
        }
    
    pesos = [peso for (_, _, peso) in mst]
    
    return {
        'peso_total': sum(pesos),
        'peso_medio': sum(pesos) / len(pesos),
        'peso_min': min(pesos),
        'peso_max': max(pesos),
        'num_arestas': len(mst)
    }


def plotar_mst(q_start, q_goal, obstaculos, mst, mostrar_pesos=False):
    """
    Visualiza a MST com cores baseadas no peso das arestas.
    
    Args:
        q_start: Ponto inicial
        q_goal: Ponto objetivo
        obstaculos: Lista de obstáculos (polígonos)
        mst: MST gerada pelo algoritmo de Prim
        mostrar_pesos: Se True, exibe o peso de cada aresta
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_aspect('equal')

    # Plotar obstáculos
    for obst in obstaculos:
        ax.add_patch(patches.Polygon(obst, closed=True, 
                                    facecolor='gray', 
                                    edgecolor='black',
                                    alpha=0.7,
                                    linewidth=2))

    # Plotar arestas da MST com gradiente de cores
    if mst:
        pesos = [peso for (_, _, peso) in mst]
        peso_min, peso_max = min(pesos), max(pesos)
        
        for (u, v, peso) in mst:
            # Gradiente: azul (leve) -> vermelho (pesado)
            if peso_max > peso_min:
                intensidade = (peso - peso_min) / (peso_max - peso_min)
            else:
                intensidade = 0.5
            
            # RGB: azul escuro -> roxo -> vermelho
            cor = (0.8 * intensidade, 0.2, 1 - 0.8 * intensidade)
            
            plt.plot([u[0], v[0]], [u[1], v[1]], 
                    color=cor, linewidth=2.5, alpha=0.9, zorder=2)
            
            # Opcional: mostrar peso da aresta
            if mostrar_pesos:
                meio_x = (u[0] + v[0]) / 2
                meio_y = (u[1] + v[1]) / 2
                ax.text(meio_x, meio_y, f'{peso:.1f}', 
                       fontsize=7, ha='center', 
                       bbox=dict(boxstyle='round,pad=0.3', 
                                facecolor='white', alpha=0.7))

    # Plotar vértices dos obstáculos
    for obst in obstaculos:
        xs, ys = zip(*obst)
        plt.plot(xs, ys, 'ko', markersize=6, zorder=3, alpha=0.6)

    # Plotar pontos inicial e final (destaque)
    ax.plot(q_start[0], q_start[1], 'go', markersize=16, 
            label='Início (q_start)', zorder=5, 
            markeredgecolor='darkgreen', markeredgewidth=2.5)
    ax.plot(q_goal[0], q_goal[1], 'ro', markersize=16, 
            label='Objetivo (q_goal)', zorder=5, 
            markeredgecolor='darkred', markeredgewidth=2.5)

    # Informações da MST
    stats = estatisticas_mst(mst)
    info_text = f"Arestas: {stats['num_arestas']} | Peso Total: {stats['peso_total']:.2f}"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.legend(loc='upper right', fontsize=11, framealpha=0.9)
    plt.title("Árvore Geradora Mínima (MST) - Algoritmo de Prim", 
             fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("X", fontsize=11)
    plt.ylabel("Y", fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()