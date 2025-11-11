import heapq
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

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


def validar_mst(grafo, mst, vertices_alcancados):
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

def extrair_vertices_arvore(arvore):
    vertices = set()
    for (u, v, _) in arvore:
        vertices.add(u)
        vertices.add(v)
    return vertices

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
