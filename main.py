from mapa import ler_mapa
from grafo import grafo_visibilidade, plotar_grafo
from arvore import prim, validar_mst, estatisticas_mst, plotar_mst

if __name__ == "__main__":
    arquivo_mapa = "mapa.txt"
    try:
        # ==================== ETAPA 1: LEITURA DO MAPA ====================
        q_start, q_goal, obstaculos = ler_mapa(arquivo_mapa)
        print(f"\nConfiguração do mapa carregada com sucesso")
        print(f"\nPonto inicial (q_start): {q_start}")
        print(f"Ponto objetivo (q_goal):   {q_goal}")
        print(f"Número de obstáculos:      {len(obstaculos)}")
        # Estatísticas dos obstáculos
        total_vertices_obs = sum(len(obst) for obst in obstaculos)
        vertices_por_obst = [len(obst) for obst in obstaculos]
        print(f"\nDetalhes dos obstáculos:")
        print(f"Total de vértices: {total_vertices_obs}")
        print(f"Média de vértices por obstáculo: {total_vertices_obs/len(obstaculos):.1f}")
        print(f"Min/Max vértices: {min(vertices_por_obst)} / {max(vertices_por_obst)}")
        # ==================== ETAPA 2: GRAFO DE VISIBILIDADE ====================
        print("\nConstruindo grafo de visibilidade...")
        grafo = grafo_visibilidade(q_start, q_goal, obstaculos)
        # Estatísticas do grafo
        total_vertices = len(grafo)
        total_arestas = sum(len(vizinhos) for vizinhos in grafo.values()) // 2
        print(f"\nGrafo construído com sucesso")
        print(f"\nInformações do grafo:")
        print(f"Vértices:  {total_vertices}")
        print(f"Arestas:   {total_arestas}")
        if total_vertices > 1:
            max_arestas = total_vertices * (total_vertices - 1) // 2
            densidade = total_arestas / max_arestas
            grau_medio = (2 * total_arestas) / total_vertices
            print(f"Densidade:  {densidade:.2%} ({total_arestas}/{max_arestas})")
            print(f"Grau médio: {grau_medio:.2f}")
        # Verificar se existe caminho entre start e goal
        vertices_alcancaveis_start = set()
        fila = [q_start]
        visitados = {q_start}
        while fila:
            v = fila.pop(0)
            vertices_alcancaveis_start.add(v)
            for (viz, _) in grafo.get(v, []):
                if viz not in visitados:
                    visitados.add(viz)
                    fila.append(viz)
        if q_goal in vertices_alcancaveis_start:
            print(f"\nExiste caminho entre q_start e q_goal")
        else:
            print(f"\nNão existe caminho entre q_start e q_goal")
            print(f"O grafo possui componentes desconexas.")
        # Visualizar grafo
        print(f"\nGerando visualização do grafo de visibilidade...")
        plotar_grafo(q_start, q_goal, obstaculos, grafo)
        # ==================== ETAPA 3: ÁRVORE GERADORA MÍNIMA ====================
        print(f"\nCalculando MST usando o algoritmo de Prim...")
        mst, total_peso, vertices_alcancados = prim(grafo, q_start)
        print(f"\nMST calculada com sucesso!")
        # Estatísticas da MST
        stats = estatisticas_mst(mst)
        validacao = validar_mst(grafo, mst, vertices_alcancados)
        print(f"\nInformações da MST:")
        print(f"Número de arestas:  {stats['num_arestas']}")
        print(f"Peso total:         {stats['peso_total']:.2f}")
        print(f"Peso médio/aresta:  {stats['peso_medio']:.2f}")
        print(f"Aresta mais leve:   {stats['peso_min']:.2f}")
        print(f"Aresta mais pesada: {stats['peso_max']:.2f}")
        print(f"\nCobertura:")
        print(f"Vértices na MST: {validacao['vertices_alcancados']}/{validacao['total_vertices']}")
        print(f"Cobertura:       {(validacao['vertices_alcancados']/validacao['total_vertices']*100):.1f}%")
        # Validação
        if validacao['grafo_conexo']:
            print(f"\nGrafo é totalmente conexo, MST completa")
        else:
            print(f"\nGrafo não é totalmente conexo")
            print(f"Vértices desconexos: {validacao['componentes_desconexos']}")
            print(f"A MST cobre apenas a componente conexa contendo q_start")
        # Verificar se q_goal está na MST
        if q_goal in vertices_alcancados:
            print(f"q_goal está incluído na MST")
        else:
            print(f"q_goal NÃO está na MST (está em componente desconexo)")
        # Visualizar MST
        print(f"\nGerando visualização da MST...")
        plotar_mst(q_start, q_goal, obstaculos, mst, mostrar_pesos=False)

    except FileNotFoundError:
        print(f"\nArquivo '{arquivo_mapa}' não encontrado")
        print(f"Verifique se o arquivo existe no diretório atual")
        
    except ValueError as e:
        print(f"\nERRO no formato do mapa: {e}")
        print(f"Verifique a estrutura do arquivo de mapa")
        
    except Exception as e:
        print(f"\nERRO inesperado durante a execução:")
        print(f"{e}")
        print(f"\nTrace completo do erro:")
        import traceback
        traceback.print_exc()
