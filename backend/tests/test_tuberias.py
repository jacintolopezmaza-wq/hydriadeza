def test_listar_tuberias_sin_material_usa_limite_por_defecto(client):
    r = client.get("/api/tuberias")
    assert r.status_code == 200
    tuberias = r.json()
    assert {t["id"] for t in tuberias} == {"P1", "P2", "P3", "P4"}
    assert all(t["pn_limite_bar"] == 5.0 for t in tuberias)


def test_patch_material_sin_pn_usa_clase_minima_del_material(client):
    r = client.patch("/api/tuberias/P1", json={"material": "pvc"})
    assert r.status_code == 200
    assert r.json()["pn_limite_bar"] == 6.0


def test_patch_material_con_pn_real_prevalece(client):
    r = client.patch("/api/tuberias/P1", json={"material": "pvc", "pn": 10})
    assert r.status_code == 200
    assert r.json()["pn_limite_bar"] == 10.0


def test_patch_tuberia_inexistente_da_404(client):
    r = client.patch("/api/tuberias/P999", json={"material": "pvc"})
    assert r.status_code == 404


def test_patch_material_invalido_falla(client):
    r = client.patch("/api/tuberias/P1", json={"material": "acero"})
    assert r.status_code == 422


def test_tuberia_cercana_localiza_el_tramo_correcto(client):
    # P1 va de A [42.665,-8.112] a B [42.663,-8.118]: un punto sobre ese
    # segmento debe encontrar P1, no los otros tramos.
    r = client.get("/api/tuberias/cercana", params={"lat": 42.664, "lng": -8.115})
    assert r.status_code == 200
    assert r.json()["id"] == "P1"


def test_tuberia_cercana_sin_topologia_da_404(client, monkeypatch):
    import app.api.tuberias as tuberias_router

    monkeypatch.setattr(
        tuberias_router, "cargar_red",
        lambda: {"nodos": {}, "tuberias": [], "valvulas": []},
    )

    r = client.get("/api/tuberias/cercana", params={"lat": 42.66, "lng": -8.12})
    assert r.status_code == 404
