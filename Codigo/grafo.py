import math
import itertools

from geometria import linha_livre

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



