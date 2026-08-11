def test_maniobra_p3_cierra_las_valvulas_del_borde(client):
    """Con los datos de ejemplo (docs/MODELO.md): avería en P3 (C-D) debe
    cerrar V2, V3 y V4, y dejar sin agua el nodo C y las tuberías P2 y P3."""
    r = client.post("/api/maniobra", json={"tuberia_averiada": "P3"})
    assert r.status_code == 200
    body = r.json()
    assert set(body["cerrar"]) == {"V2", "V3", "V4"}
    assert body["nodos_sin_agua"] == ["C"]
    assert set(body["tuberias_afectadas"]) == {"P2", "P3"}
    assert {c["id"] for c in body["coordenadas"]} == {"V2", "V3", "V4"}


def test_maniobra_tuberia_inexistente_da_404(client):
    r = client.post("/api/maniobra", json={"tuberia_averiada": "P999"})
    assert r.status_code == 404


def test_maniobra_tuberia_averiada_vacia_falla(client):
    r = client.post("/api/maniobra", json={"tuberia_averiada": ""})
    assert r.status_code == 422
