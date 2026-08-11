from fastapi import APIRouter, HTTPException, Query
from ..core.store import cargar_red, guardar_red
from ..core.materiales import pn_limite
from ..core.geo import tuberia_mas_cercana
from ..models.schemas import TuberiaMaterial

router = APIRouter(prefix="/api", tags=["tuberias"])


@router.get("/tuberias")
def listar_tuberias():
    """Tuberías con su material/PN (si se conocen) y las coordenadas de
    sus dos extremos, para poder editarlas o dibujarlas en el mapa."""
    red = cargar_red()
    nodos = red["nodos"]
    return [
        {
            "id": t["id"], "a": t["a"], "b": t["b"],
            "material": t.get("material"), "pn": t.get("pn"),
            "pn_limite_bar": pn_limite(t.get("material"), t.get("pn")),
            "coords": [nodos.get(t["a"]), nodos.get(t["b"])],
        }
        for t in red["tuberias"]
    ]


@router.patch("/tuberias/{tuberia_id}")
def actualizar_material(tuberia_id: str, datos: TuberiaMaterial):
    """Registra el material (y opcionalmente la PN real) de un tramo ya
    existente en la red. No crea tramos nuevos."""
    red = cargar_red()
    for t in red["tuberias"]:
        if t["id"] == tuberia_id:
            t["material"] = datos.material
            t["pn"] = datos.pn
            guardar_red(red)
            return {"ok": True, "pn_limite_bar": pn_limite(datos.material, datos.pn)}
    raise HTTPException(404, f"Tubería {tuberia_id} no existe")


@router.get("/tuberias/cercana")
def tuberia_cercana(lat: float = Query(...), lng: float = Query(...)):
    """Tramo más próximo a un punto (lat, lng) y su límite de presión,
    para comparar contra la presión estática calculada en ese punto."""
    red = cargar_red()
    t, distancia_m = tuberia_mas_cercana(lat, lng, red["nodos"], red["tuberias"])
    if not t:
        raise HTTPException(404, "La red no tiene tuberías cargadas")
    return {
        "id": t["id"], "material": t.get("material"), "pn": t.get("pn"),
        "pn_limite_bar": pn_limite(t.get("material"), t.get("pn")),
        "distancia_m": round(distancia_m),
    }
