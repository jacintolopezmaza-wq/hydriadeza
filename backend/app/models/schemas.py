from pydantic import BaseModel
from typing import Optional


class ValvulaNueva(BaseModel):
    nombre: str
    lat: float
    lng: float
    tuberia: str
    nodo: str
    estado: str = "abierta"


class AveriaRequest(BaseModel):
    tuberia_averiada: str
