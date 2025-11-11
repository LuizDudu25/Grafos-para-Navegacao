from mapa import ler_mapa
from grafo import grafo_visibilidade
from arvore import prim, validar_mst, estatisticas_mst, verticeMaisProximo
from caminho import buscarCaminho, estatisticas_caminho
from plots import plotar_grafo, plotar_mst, plotar_caminho

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
        plotar_grafo(grafo, obstaculos, q_start, q_goal)
        
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
        plotar_mst(mst, obstaculos, q_start, q_goal)

        # ==================== ETAPA 4: VÉRTICE MAIS PRÓXIMO ====================
        print(f"\nEncontrando os vértices mais próximo...")
        
        v_inicio = verticeMaisProximo(q_start, mst)
        v_fim = verticeMaisProximo(q_goal, mst)
        
        # ==================== ETAPA 5: BUSCA DE CAMINHO ====================
        # Só procurar caminho se q_goal estiver na MST
        if q_goal in vertices_alcancados:
            print(f"\nBuscando caminho de {q_start} até {q_goal}...")
            print(f"   Usando algoritmo: DFS (Depth-First Search)")
            
            # Buscar caminho
            caminho, distancia_caminho = buscarCaminho(v_inicio, v_fim, mst)
            
            if caminho:
                print(f"\nCaminho encontrado com sucesso")
                
                # Estatísticas do caminho
                stats_caminho = estatisticas_caminho(caminho, distancia_caminho)
                
                print(f"\nEstatísticas do caminho:")
                print(f"Vértices no caminho: {stats_caminho['num_vertices']}")
                print(f"Arestas percorridas: {stats_caminho['num_arestas']}")
                print(f"Distância total:     {stats_caminho['distancia_total']:.2f}")
                print(f"Distância média/aresta: {stats_caminho['distancia_media_aresta']:.2f}")
                
                print(f"\nComparação com linha direta:")
                print(f"Distância euclidiana: {stats_caminho['distancia_euclidiana_direta']:.2f}")
                print(f"Razão caminho/direto: {stats_caminho['razao_caminho']:.2f}x")
                
                if stats_caminho['razao_caminho'] < 1.5:
                    print(f"Caminho eficiente (razão < 1.5)")
                elif stats_caminho['razao_caminho'] < 2.5:
                    print(f"Caminho razoável (1.5 ≤ razão < 2.5)")
                else:
                    print(f"Caminho longo (razão ≥ 2.5)")
                
                # Mostrar primeiros e últimos vértices
                print(f"\nSequência do caminho:")
                if len(caminho) <= 6:
                    for i, v in enumerate(caminho):
                        print(f"    {i+1}. {v}")
                else:
                    for i in range(3):
                        print(f"    {i+1}. {caminho[i]}")
                    print(f"    ...")
                    for i in range(len(caminho) - 3, len(caminho)):
                        print(f"    {i+1}. {caminho[i]}")
                
            else:
                print(f"\nNenhum caminho encontrado!")
                print(f"Isso não deveria acontecer se q_goal está na MST.")
        
        else:
            print(f"\nBusca de caminho não realizada:")
            print(f"q_goal não está na MST (componente desconexo)")
            print(f"Não é possível encontrar caminho na árvore.")
            caminho = None
            distancia_caminho = 0
        
        # ==================== ETAPA 6: PLOTAR CAMINHO ====================
        if caminho:
            print(f"\nGerando visualização do caminho encontrado...")
            print(f"Caminho: {len(caminho)} vértices, distância {distancia_caminho:.2f}")
            
            # Plotar com grafo completo
            print(f"\nCaminho destacado sobre o grafo completo")
            plotar_caminho(caminho, obstaculos, q_start, q_goal, grafo)
        else:
            print(f"\nVisualização não realizada, nenhum caminho disponível")
        
    except FileNotFoundError:
        print(f"\nArquivo '{arquivo_mapa}' não encontrado")
        print(f"Verifique se o arquivo existe no diretório atual")
        
    except ValueError as e:
        print(f"\nErro no formato do mapa: {e}")
        print(f"Verifique a estrutura do arquivo de mapa")
        
    except Exception as e:
        print(f"\nErro inesperado durante a execução:")
        print(f"{e}")
        print(f"\nTrace completo do erro:")
        import traceback
        traceback.print_exc()
