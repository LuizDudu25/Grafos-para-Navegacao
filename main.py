from mapa import ler_mapa
from grafo import grafo_visibilidade, plotar_grafo

if __name__ == "__main__":
    arquivo_mapa = "mapa.txt"
    
    try:
        # Ler o mapa
        print("Lendo mapa...")
        q_start, q_goal, obstaculos = ler_mapa(arquivo_mapa)
        
        print(f"Ponto inicial: {q_start}")
        print(f"Ponto final: {q_goal}")
        print(f"Número de obstáculos: {len(obstaculos)}")
        
        # Criar grafo de visibilidade
        print("\nCriando grafo de visibilidade...")
        grafo = grafo_visibilidade(q_start, q_goal, obstaculos)
        
        # Estatísticas
        total_arestas = sum(len(vizinhos) for vizinhos in grafo.values()) // 2
        print(f"\nEstatísticas do grafo:")
        print(f"  - Vértices: {len(grafo)}")
        print(f"  - Arestas: {total_arestas}")
        
        # Visualizar
        print("\nVisualizando grafo...")
        plotar_grafo(q_start, q_goal, obstaculos, grafo)
        
    except Exception as e:
        print(f"\nErro na execução: {e}")