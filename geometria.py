import math
from shapely.geometry import Point, Polygon, LineString

def dist(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def ponto_dentro_poligono(p, poligono):
    return Polygon(poligono).covers(Point(p))

def intersecao(p1, q1, p2, q2):
    return LineString([p1, q1]).intersects(LineString([p2, q2]))

def linha_livre(p1, p2, obstaculos):
    linha = LineString([p1, p2])
    for obst in obstaculos:
        pol = Polygon(obst)
        if pol.is_empty:
            continue

        # Se a linha cruza o polígono (intersects) e não apenas toca (touches)
        if linha.intersects(pol) and not linha.touches(pol):
            return False

    return True
