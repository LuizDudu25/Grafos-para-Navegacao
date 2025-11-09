import os

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