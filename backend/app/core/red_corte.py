"""Motor de cálculo de maniobras de corte (análisis de segmentos por válvulas)."""

import networkx as nx


def construir_segmentos(nodos, tuberias, valvulas):
    """Divide la red en segmentos (componentes conexos sin cruzar válvulas).

    Devuelve (segmentos, elem_seg):
      - segmentos: lista de sets de elementos ('nodo', id) / ('tuberia', id)
      - elem_seg:  dict elemento -> índice de segmento
    """
    # Ignora válvulas capturadas en campo aún sin vincular a la topología
    # (sin tuberia/nodo asignados): no participan en el cálculo de segmentos.
    hay_valvula = {
        (v["tuberia"], v["nodo"]) for v in valvulas if v.get("tuberia") and v.get("nodo")
    }

    G = nx.Graph()
    for n in nodos:
        G.add_node(("nodo", n))
    for t in tuberias:
        G.add_node(("tuberia", t["id"]))
        for extremo in (t["a"], t["b"]):
            if (t["id"], extremo) not in hay_valvula:
                G.add_edge(("tuberia", t["id"]), ("nodo", extremo))

    segmentos = [set(c) for c in nx.connected_components(G)]
    elem_seg = {e: i for i, comp in enumerate(segmentos) for e in comp}
    return segmentos, elem_seg


def maniobra_de_corte(tuberia_averiada, valvulas, elem_seg):
    """Ante una avería en 'tuberia_averiada' devuelve (cerrar, afectados).

      - cerrar:    lista de ids de válvula a cerrar (borde del segmento)
      - afectados: elementos que se quedan sin suministro
    """
    seg = elem_seg[("tuberia", tuberia_averiada)]

    cerrar = []
    for v in valvulas:
        tub_dentro = elem_seg.get(("tuberia", v["tuberia"])) == seg
        nodo_dentro = elem_seg.get(("nodo", v["nodo"])) == seg
        if tub_dentro != nodo_dentro:  # válvula de borde (XOR)
            cerrar.append(v["id"])

    afectados = [e for e, s in elem_seg.items() if s == seg]
    return cerrar, afectados
