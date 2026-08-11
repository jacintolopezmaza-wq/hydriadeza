"""Utilidades geométricas mínimas sobre coordenadas lat/lng (WGS84)."""

import math


def _a_metros(lat, lng, lat_ref):
    """Proyección equirrectangular simple, válida para distancias cortas
    (escala de un municipio), tomando lat_ref como paralelo de referencia."""
    r = 6371000
    x = math.radians(lng) * r * math.cos(math.radians(lat_ref))
    y = math.radians(lat) * r
    return x, y


def _dist_punto_segmento(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def tuberia_mas_cercana(lat, lng, nodos, tuberias):
    """Devuelve (tuberia, distancia_m) del tramo cuyo trazado (segmento
    recto entre sus dos nodos) está más cerca del punto dado."""
    px, py = _a_metros(lat, lng, lat)
    mejor, mejor_d = None, float("inf")
    for t in tuberias:
        na, nb = nodos.get(t["a"]), nodos.get(t["b"])
        if not na or not nb:
            continue
        ax, ay = _a_metros(na[0], na[1], lat)
        bx, by = _a_metros(nb[0], nb[1], lat)
        d = _dist_punto_segmento(px, py, ax, ay, bx, by)
        if d < mejor_d:
            mejor_d, mejor = d, t
    return mejor, mejor_d
