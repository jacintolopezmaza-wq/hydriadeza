from fastapi import APIRouter, HTTPException
from ..core.store import cargar_red
from ..core.red_corte import construir_segmentos, maniobra_de_corte
from ..models.schemas import AveriaRequest

router = APIRouter(prefix="/api", tags=["maniobra"])


@router.post("/maniobra")
def calcular_maniobra(req: AveriaRequest):
    """Dada una avería en una tubería, devuelve las válvulas a cerrar,
    sus coordenadas (para rutar) y la zona que queda sin agua."""
    red = cargar_red()
    _, elem_seg = construir_segmentos(red["nodos"], red["tuberias"], red["valvulas"])

    if ("tuberia", req.tuberia_averiada) not in elem_seg:
        raise HTTPException(404, f"Tubería {req.tuberia_averiada} no existe")

    cerrar, afectados = maniobra_de_corte(req.tuberia_averiada, red["valvulas"], elem_seg)

    por_id = {v["id"]: v for v in red["valvulas"]}
    coords = [
        {"id": vid, "nombre": por_id[vid].get("nombre", vid),
         "lat": por_id[vid]["lat"], "lng": por_id[vid]["lng"]}
        for vid in cerrar
    ]
    return {
        "cerrar": cerrar,
        "coordenadas": coords,
        "nodos_sin_agua": [n for tipo, n in afectados if tipo == "nodo"],
        "tuberias_afectadas": [n for tipo, n in afectados if tipo == "tuberia"],
    }
