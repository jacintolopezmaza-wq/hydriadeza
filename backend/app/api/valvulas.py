from fastapi import APIRouter
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
                    "estado": v["estado"], "tuberia": v["tuberia"], "nodo": v["nodo"],
                },
            }
            for v in red["valvulas"]
        ],
    }


@router.post("/valvulas")
def crear_valvula(v: ValvulaNueva):
    """Registra una válvula capturada en campo."""
    red = cargar_red()
    nuevo_id = f"V{len(red['valvulas']) + 1}"
    red["valvulas"].append({
        "id": nuevo_id, "tuberia": v.tuberia, "nodo": v.nodo,
        "estado": v.estado, "nombre": v.nombre, "lat": v.lat, "lng": v.lng,
    })
    guardar_red(red)
    return {"ok": True, "id": nuevo_id}
