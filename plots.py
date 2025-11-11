import matplotlib.pyplot as plt
from shapely.geometry import Polygon


# Gerais
def plotar_obstaculos(obstaculos, ax, color1, color2, alpha, lw, zorder1, zorder2):
    for obst in obstaculos:
        pol = Polygon(obst)
        x, y = pol.exterior.xy
        ax.fill(x, y, color=color1, alpha=alpha, zorder=zorder1)
        ax.plot(x, y, color=color2, linewidth=lw, zorder=zorder2, label="_contorno")

def exibicao(ax):
    # Legenda
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])  # espaço para legenda
    ax.legend(
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        frameon=True,
        shadow=True
    )

    # Aspecto e exibição
    ax.set_aspect('equal', 'box')
    plt.tight_layout()
    plt.show()


# Plotar grafo de visibilidade
def plotar_grafo(grafo, obstaculos, q_start=None, q_goal=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Obstáculos
    plotar_obstaculos(obstaculos, ax, "lightgray", "black", 0.8, 2.0, 1, 5)

    # Arestas
    for v in grafo:
        for viz, _ in grafo[v]:
            # garante que v e viz sejam iteráveis com 2 valores (x, y)
            if isinstance(v, (tuple, list)) and isinstance(viz, (tuple, list)) and len(v) == 2 and len(viz) == 2:
                ax.plot(
                    [v[0], viz[0]], [v[1], viz[1]],
                    color='steelblue', linewidth=1.8, alpha=0.7, zorder=1
                )

    # Vértices
    try:
        xs, ys = zip(*[v for v in grafo.keys() if isinstance(v, (tuple, list)) and len(v) == 2])
        ax.scatter(xs, ys, s=20, color='navy', label='Vértices do grafo', zorder=2)
    except ValueError:
        # Grafo pode estar vazio — apenas ignora
        pass

    # Ponto inicial e final
    if q_start and isinstance(q_start, (tuple, list)) and len(q_start) == 2:
        ax.scatter(*q_start, s=80, color='green', marker='o', edgecolors='black',
                   label='Ponto inicial (q_start)', zorder=3)
    if q_goal and isinstance(q_goal, (tuple, list)) and len(q_goal) == 2:
        ax.scatter(*q_goal, s=80, color='red', marker='X', edgecolors='black',
                   label='Ponto final (q_goal)', zorder=3)

    # Aparência geral
    ax.set_title("Grafo de Visibilidade", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, linestyle="--", alpha=0.3)

    exibicao(ax)


# Plotar MST
def plotar_mst(arestas, obstaculos, q_start=None, q_goal=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Obstáculos
    plotar_obstaculos(obstaculos, ax, "gainsboro", "gray", 0.6, 1.0, 1, 2)

    # Arestas da MST
    for u, v, _ in arestas:
        if isinstance(u, (tuple, list)) and isinstance(v, (tuple, list)) and len(u) == 2 and len(v) == 2:
            ax.plot(
                [u[0], v[0]], [u[1], v[1]],
                color='forestgreen', linewidth=2.5, alpha=0.9, zorder=4
            )

    # Vértices
    vertices = set()
    for u, v, _ in arestas:
        vertices.add(u)
        vertices.add(v)

    if vertices:
        xs, ys = zip(*vertices)
        ax.scatter(xs, ys, s=25, color='darkgreen', label='Vértices da MST', zorder=3)

    # Ponto inicial e final
    if q_start:
        ax.scatter(*q_start, s=100, color='green', marker='o', edgecolors='black',
                   label='Ponto inicial (q_start)', zorder=6)
    if q_goal:
        ax.scatter(*q_goal, s=100, color='red', marker='X', edgecolors='black',
                   label='Ponto final (q_goal)', zorder=6)

    # Aparência geral
    ax.set_title("Árvore Geradora Mínima (MST)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, linestyle="--", alpha=0.3)

    exibicao(ax)


# Plotar caminho final
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
