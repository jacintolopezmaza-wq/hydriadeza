def test_listar_valvulas_devuelve_geojson_inicial(client):
    r = client.get("/api/valvulas")
    assert r.status_code == 200
    geojson = r.json()
    assert geojson["type"] == "FeatureCollection"
    ids = {f["properties"]["id"] for f in geojson["features"]}
    assert ids == {"V1", "V2", "V3", "V4"}


def test_crear_valvula_ok(client):
    r = client.post("/api/valvulas", json={
        "nombre": "Nueva", "lat": 42.66, "lng": -8.12,
        "estado": "cerrada", "diametro": 63, "material": "fibrocemento",
    })
    assert r.status_code == 200
    assert r.json()["id"] == "V5"

    listado = client.get("/api/valvulas").json()
    nueva = next(f for f in listado["features"] if f["properties"]["id"] == "V5")
    assert nueva["properties"]["material"] == "fibrocemento"
    assert nueva["properties"]["diametro"] == 63
    assert nueva["geometry"]["coordinates"] == [-8.12, 42.66]


def test_crear_valvula_sin_tuberia_ni_nodo_no_falla(client):
    """Lo habitual en campo: se sabe el material pero no la topología."""
    r = client.post("/api/valvulas", json={"nombre": "Sin plano", "lat": 42.66, "lng": -8.12})
    assert r.status_code == 200


def test_crear_valvula_id_no_colisiona_tras_borrar_una_intermedia(client):
    """Regresión: con id = len(valvulas)+1, borrar una válvula que no es la
    última hacía que el siguiente alta reutilizara un id ya existente.
    Aquí: V1..V4 iniciales + V5 nueva = 5: al borrar V2 quedan 4, y
    len()+1 volvería a dar "V5", colisionando con la que ya existe."""
    v5 = client.post("/api/valvulas", json={"nombre": "A", "lat": 42.66, "lng": -8.12}).json()["id"]
    assert v5 == "V5"
    client.delete("/api/valvulas/V2")

    v6 = client.post("/api/valvulas", json={"nombre": "B", "lat": 42.66, "lng": -8.12}).json()["id"]
    assert v6 == "V6"

    ids = [f["properties"]["id"] for f in client.get("/api/valvulas").json()["features"]]
    assert len(ids) == len(set(ids)), "hay ids de válvula duplicados"


def test_crear_valvula_lat_fuera_de_rango_falla(client):
    r = client.post("/api/valvulas", json={"nombre": "x", "lat": 200, "lng": 0})
    assert r.status_code == 422


def test_crear_valvula_estado_invalido_falla(client):
    r = client.post("/api/valvulas", json={"nombre": "x", "lat": 1, "lng": 1, "estado": "rota"})
    assert r.status_code == 422


def test_crear_valvula_material_invalido_falla(client):
    r = client.post("/api/valvulas", json={"nombre": "x", "lat": 1, "lng": 1, "material": "acero"})
    assert r.status_code == 422


def test_crear_valvula_nombre_vacio_falla(client):
    r = client.post("/api/valvulas", json={"nombre": "", "lat": 1, "lng": 1})
    assert r.status_code == 422


def test_borrar_valvula_ok(client):
    r = client.delete("/api/valvulas/V1")
    assert r.status_code == 200
    ids = {f["properties"]["id"] for f in client.get("/api/valvulas").json()["features"]}
    assert "V1" not in ids


def test_borrar_valvula_inexistente_da_404(client):
    r = client.delete("/api/valvulas/V999")
    assert r.status_code == 404


def test_valvula_cercana_encuentra_la_mas_proxima(client):
    client.post("/api/valvulas", json={
        "nombre": "Chareda de Outeiros", "lat": 42.6605, "lng": -8.1205,
        "material": "fibrocemento", "diametro": 63,
    })
    r = client.get("/api/valvulas/cercana", params={"lat": 42.6606, "lng": -8.1206})
    assert r.status_code == 200
    body = r.json()
    assert body["material"] == "fibrocemento"
    assert body["pn_limite_bar"] == 5.0
    assert body["distancia_m"] < 50


def test_valvula_cercana_sin_ninguna_documentada_da_404(client):
    r = client.get("/api/valvulas/cercana", params={"lat": 42.66, "lng": -8.12})
    assert r.status_code == 404
