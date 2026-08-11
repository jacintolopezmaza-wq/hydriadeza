from app.core.geo import distancia_metros, tuberia_mas_cercana


def test_distancia_metros_punto_igual_es_cero():
    assert distancia_metros(42.66, -8.12, 42.66, -8.12) == 0


def test_distancia_metros_un_grado_de_latitud_son_unos_111km():
    d = distancia_metros(0.0, 0.0, 1.0, 0.0)
    assert 110_000 < d < 112_000


def test_tuberia_mas_cercana_elige_el_segmento_correcto():
    nodos = {"A": [42.665, -8.112], "B": [42.663, -8.118], "C": [42.615, -8.135]}
    tuberias = [
        {"id": "P1", "a": "A", "b": "B"},
        {"id": "P2", "a": "B", "b": "C"},
    ]
    tuberia, distancia = tuberia_mas_cercana(42.664, -8.115, nodos, tuberias)
    assert tuberia["id"] == "P1"
    assert distancia < 200


def test_tuberia_mas_cercana_ignora_tuberias_con_nodo_desconocido():
    nodos = {"A": [42.665, -8.112], "B": [42.663, -8.118]}
    tuberias = [{"id": "P1", "a": "A", "b": "NOEXISTE"}]
    tuberia, distancia = tuberia_mas_cercana(42.664, -8.115, nodos, tuberias)
    assert tuberia is None
