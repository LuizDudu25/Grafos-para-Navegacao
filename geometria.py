def intersecao(p1, p2, q1, q2):
    def orient(a, b, c):
        # Calcula a orientação do tripé ordenado (a, b, c)
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    
    def entre(a, b, c):
        # Verifica se o ponto b está no segmento ac (quando colineares)
        return (min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and 
                min(a[1], c[1]) <= b[1] <= max(a[1], c[1]))
    
    o1 = orient(p1, p2, q1)
    o2 = orient(p1, p2, q2)
    o3 = orient(q1, q2, p1)
    o4 = orient(q1, q2, p2)
    
    # Caso geral: os segmentos se cruzam
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    
    # Casos especiais: pontos colineares
    if o1 == 0 and entre(p1, q1, p2):
        return True
    if o2 == 0 and entre(p1, q2, p2):
        return True
    if o3 == 0 and entre(q1, p1, q2):
        return True
    if o4 == 0 and entre(q1, p2, q2):
        return True
    
    return False


def ponto_dentro_poligono(ponto, poligono):
    x, y = ponto
    n = len(poligono)
    dentro = False
    
    j = n - 1
    for i in range(n):
        xi, yi = poligono[i]
        xj, yj = poligono[j]
        
        # Verifica se o raio horizontal a partir do ponto cruza a aresta
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            dentro = not dentro
        j = i
    
    return dentro


def linha_livre(p1, p2, obstaculos):
    # Verificar se o ponto médio está dentro de algum obstáculo
    # (importante para detectar segmentos que atravessam completamente um obstáculo)
    meio = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    for obst in obstaculos:
        if ponto_dentro_poligono(meio, obst):
            return False
    
    # Verificar interseções com as arestas dos obstáculos
    for obst in obstaculos:
        n = len(obst)
        for i in range(n):
            a, b = obst[i], obst[(i + 1) % n]
            
            # Se a aresta testada é parte do próprio obstáculo, ignorar
            # (permite conexões entre vértices adjacentes do mesmo obstáculo)
            if (p1 == a and p2 == b) or (p1 == b and p2 == a):
                continue
            
            if intersecao(p1, p2, a, b):
                return False
    
    return True