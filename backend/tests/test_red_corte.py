"""Tests del algoritmo puro de segmentación (sin pasar por la API)."""

from app.core.red_corte import construir_segmentos, maniobra_de_corte

NODOS = ["A", "B", "C"]
TUBERIAS = [{"id": "P1", "a": "A", "b": "B"}, {"id": "P2", "a": "B", "b": "C"}]


def test_sin_valvulas_todo_es_un_unico_segmento():
    segmentos, elem_seg = construir_segmentos(NODOS, TUBERIAS, [])
    assert len(segmentos) == 1
    assert elem_seg[("tuberia", "P1")] == elem_seg[("tuberia", "P2")]


def test_una_valvula_separa_la_red_en_dos_segmentos():
    valvulas = [{"id": "V1", "tuberia": "P2", "nodo": "B"}]
    segmentos, elem_seg = construir_segmentos(NODOS, TUBERIAS, valvulas)
    assert len(segmentos) == 2
    assert elem_seg[("tuberia", "P1")] != elem_seg[("tuberia", "P2")]


def test_valvulas_sin_tuberia_o_nodo_se_ignoran_en_la_topologia():
    """Válvula capturada en campo sin plano: no debe romper el cálculo."""
    valvulas = [{"id": "V1", "tuberia": None, "nodo": None}]
    segmentos, elem_seg = construir_segmentos(NODOS, TUBERIAS, valvulas)
    assert len(segmentos) == 1  # como si la válvula no existiera


def test_maniobra_de_corte_cierra_solo_las_valvulas_de_borde():
    # A -P1- B -P2- C -P3- D, con válvulas en (P1,B) y (P3,C): una avería
    # en P2 debe aislar el tramo B-P2-C cerrando ambas válvulas de borde,
    # sin tocar P1 ni P3, que quedan fuera del segmento afectado.
    nodos = ["A", "B", "C", "D"]
    tuberias = [
        {"id": "P1", "a": "A", "b": "B"},
        {"id": "P2", "a": "B", "b": "C"},
        {"id": "P3", "a": "C", "b": "D"},
    ]
    valvulas = [
        {"id": "V1", "tuberia": "P1", "nodo": "B"},
        {"id": "V2", "tuberia": "P3", "nodo": "C"},
    ]
    _, elem_seg = construir_segmentos(nodos, tuberias, valvulas)
    cerrar, afectados = maniobra_de_corte("P2", valvulas, elem_seg)
    assert set(cerrar) == {"V1", "V2"}
    assert ("tuberia", "P2") in afectados
    assert ("nodo", "B") in afectados
    assert ("nodo", "C") in afectados
    assert ("tuberia", "P1") not in afectados
    assert ("tuberia", "P3") not in afectados
