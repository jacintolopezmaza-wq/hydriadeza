from fastapi import APIRouter, HTTPException
from ..core.store import cargar_red, guardar_red
from ..models.schemas import ValvulaNueva

router = APIRouter(prefix="/api", tags=["valvulas"])


@router.get("/valvulas")
def listar_valvulas():
    """Devuelve las válvulas en formato GeoJSON para el mapa (Leaflet)."""
    red = cargar_red()
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [v["lng"], v["lat"]]},
                "properties": {
                    "id": v["id"], "nombre": v.get("nombre", v["id"]),
                    "estado": v["estado"], "tuberia": v.get("tuberia"), "nodo": v.get("nodo"),
                    "aisla": v.get("aisla"), "diametro": v.get("diametro"),
                },
            }
            for v in red["valvulas"]
        ],
    }


def _siguiente_id(valvulas):
    numeros = [
        int(v["id"][1:])
        for v in valvulas
        if v["id"].startswith("V") and v["id"][1:].isdigit()
    ]
    return f"V{(max(numeros) + 1) if numeros else 1}"


@router.post("/valvulas")
def crear_valvula(v: ValvulaNueva):
    """Registra una válvula capturada en campo."""
    red = cargar_red()
    nuevo_id = _siguiente_id(red["valvulas"])
    red["valvulas"].append({
        "id": nuevo_id, "tuberia": v.tuberia, "nodo": v.nodo,
        "estado": v.estado, "nombre": v.nombre, "lat": v.lat, "lng": v.lng,
        "aisla": v.aisla, "diametro": v.diametro,
    })
    guardar_red(red)
    return {"ok": True, "id": nuevo_id}


@router.delete("/valvulas/{valvula_id}")
def borrar_valvula(valvula_id: str):
    """Elimina una válvula del almacén (sincronización desde la app de campo)."""
    red = cargar_red()
    antes = len(red["valvulas"])
    red["valvulas"] = [v for v in red["valvulas"] if v["id"] != valvula_id]
    if len(red["valvulas"]) == antes:
        raise HTTPException(404, f"Válvula {valvula_id} no existe")
    guardar_red(red)
    return {"ok": True}
