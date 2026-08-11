from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..core.geo import distancia_metros
from ..core.store import _cliente

router = APIRouter(prefix="/api", tags=["depositos"])


class DepositoNuevo(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    zona: str | None = Field(default=None, max_length=120)
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    cota: float  # metros sobre el nivel del mar


def _requiere_bd():
    if not _cliente:
        raise HTTPException(503, "Los depósitos requieren la base de datos (SUPABASE_URL/SUPABASE_KEY)")


@router.get("/depositos")
def listar_depositos():
    """Depósitos reales de la red, cada uno con su cota real."""
    _requiere_bd()
    r = _cliente.table("depositos").select("*").execute()
    return r.data


@router.post("/depositos")
def crear_deposito(d: DepositoNuevo):
    _requiere_bd()
    r = _cliente.table("depositos").insert(d.model_dump()).execute()
    return r.data[0]


@router.get("/depositos/cercana")
def deposito_cercano(lat: float = Query(...), lng: float = Query(...)):
    """Depósito real más próximo a un punto, para usar su cota en el
    cálculo de presión estática en vez de un valor fijo manual."""
    _requiere_bd()
    depositos = _cliente.table("depositos").select("*").execute().data
    if not depositos:
        raise HTTPException(404, "No hay depósitos registrados todavía")
    mejor = min(depositos, key=lambda d: distancia_metros(lat, lng, d["lat"], d["lng"]))
    mejor["distancia_m"] = round(distancia_metros(lat, lng, mejor["lat"], mejor["lng"]))
    return mejor
