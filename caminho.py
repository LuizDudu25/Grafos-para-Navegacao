import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def construir_adjacencia(arvore):
    adj = {}
    for (u, v, peso) in arvore:
        adj.setdefault(u, []).append((v, peso))
        adj.setdefault(v, []).append((u, peso))
    return adj

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

def estatisticas_caminho(caminho, distancia):
    if not caminho or len(caminho) < 2:
        return {
            'num_vertices': 0 if not caminho else len(caminho),
            'num_arestas': 0,
            'distancia_total': 0,
            'distancia_media_aresta': 0,
            'distancia_euclidiana_direta': 0,
            'razao_caminho': 0
        }
    
    num_vertices = len(caminho)
    num_arestas = num_vertices - 1
    distancia_media = distancia / num_arestas if num_arestas > 0 else 0
    
    # Distância euclidiana direta
    dist_direta = math.dist(caminho[0], caminho[-1])
    
    # Razão entre caminho na árvore e linha reta
    razao = distancia / dist_direta if dist_direta > 0 else float('inf')
    
    return {
        'num_vertices': num_vertices,
        'num_arestas': num_arestas,
        'distancia_total': distancia,
        'distancia_media_aresta': distancia_media,
        'distancia_euclidiana_direta': dist_direta,
        'razao_caminho': razao
    }
