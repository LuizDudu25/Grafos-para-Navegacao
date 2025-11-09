O código é dividido em diferentes etapas:

Etapa 1: Leitura do mapa (configuração inicial, final e obstáculos).

ler_mapa(arquivo) 
Lê o arquivo de mapa e retorna as configurações inicial e final, além dos obstáculos.
Args: arquivo: caminho do arquivo de mapa
Returns: q_start: tupla com coordenadas do ponto inicial; q_goal: tupla com coordenadas do ponto final; obstaculos: lista de obstáculos (cada obstáculo é uma lista de vértices)


Etapa 2: Funções auxiliares de geometria (interseção de segmentos, ponto dentro de polígono, linha livre).

intersecao(p1, p2, q1, q2)
Retorna True se os segmentos p1-p2 e q1-q2 se cruzam.
Args: p1, p2: pontos que definem o primeiro segmento; q1, q2: pontos que definem o segundo segmento
Returns: True se os segmentos se cruzam, False caso contrário

ponto_dentro_poligono(ponto, poligono)
Verifica se um ponto está dentro de um polígono usando o algoritmo de ray casting.
Args: ponto: tupla (x, y) com as coordenadas do ponto; poligono: lista de vértices do polígono
Returns: True se o ponto está dentro do polígono, False caso contrário

linha_livre(p1, p2, obstaculos)
Verifica se o segmento p1-p2 está livre de colisão com obstáculos.
Args: p1, p2: pontos que definem o segmento; obstaculos: lista de obstáculos (polígonos)
Returns: True se o segmento está livre, False caso contrário


Etapa 3: Criação do grafo de visibilidade.

grafo_visibilidade(q_start, q_goal, obstaculos, max_distancia=None)
Cria o grafo de visibilidade a partir dos pontos inicial, final e obstáculos.
Args: q_start: ponto inicial; q_goal: ponto final; obstaculos: lista de obstáculos; max_distancia: distância máxima para considerar conexões (opcional)
Returns: Dicionário representando o grafo, onde cada chave é um vértice e o valor é uma lista de tuplas (vizinho, distância)


Etapa 4: Visualização do grafo (plotagem).

plotar_grafo(q_start, q_goal, obstaculos, grafo, caminho=None):
Plota o grafo de visibilidade com obstáculos.
Args: q_start: ponto inicial; q_goal: ponto final; obstaculos: lista de obstáculos; grafo: grafo de visibilidade; caminho: caminho a ser destacado (opcional)
