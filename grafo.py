import math
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from .geometria import linha_livre


def grafo_visibilidade(q_start, q_goal, obstaculos, max_distancia=None):
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
        if linha_livre(v1, v2, obstaculos):
            G[v1].append((v2, distancia))
            G[v2].append((v1, distancia))
            conexoes += 1
    
    print(f"Grafo criado: {len(vertices)} vértices, {conexoes} arestas")
    print(f"Testados {total_pares} pares de vértices")
    
    return G

def plotar_grafo(q_start, q_goal, obstaculos, grafo, caminho=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    
    # Plotar obstáculos
    for obst in obstaculos:
        ax.add_patch(patches.Polygon(obst, closed=True, 
                                    facecolor='gray', 
                                    edgecolor='black', 
                                    alpha=0.7,
                                    linewidth=2))
    
    # Plotar arestas do grafo
    for v in grafo:
        for (vizinho, _) in grafo[v]:
            plt.plot([v[0], vizinho[0]], [v[1], vizinho[1]], 
                    color='lightblue', linewidth=0.5, alpha=0.4, zorder=1)
    
    # Plotar caminho (se fornecido)
    if caminho:
        for i in range(len(caminho) - 1):
            plt.plot([caminho[i][0], caminho[i+1][0]], 
                    [caminho[i][1], caminho[i+1][1]], 
                    color='red', linewidth=3, alpha=0.8, zorder=3, 
                    label='Caminho' if i == 0 else '')
    
    # Plotar vértices dos obstáculos
    for obst in obstaculos:
        xs, ys = zip(*obst)
        plt.plot(xs, ys, 'ko', markersize=4, zorder=2)
    
    # Plotar pontos inicial e final
    ax.plot(q_start[0], q_start[1], 'go', markersize=12, 
            label='Início', zorder=4, markeredgecolor='darkgreen', markeredgewidth=2)
    ax.plot(q_goal[0], q_goal[1], 'ro', markersize=12, 
            label='Objetivo', zorder=4, markeredgecolor='darkred', markeredgewidth=2)
    
    plt.legend(loc='best', fontsize=10)
    plt.title("Grafo de Visibilidade", fontsize=14, fontweight='bold')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()