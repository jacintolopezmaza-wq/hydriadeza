from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional


class ValvulaNueva(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    estado: Literal["abierta", "cerrada"] = "abierta"
    # Posición en la topología de red: puede no conocerse aún si la válvula
    # se capturó en campo sin el modelo de tuberías cargado (se enlaza después).
    tuberia: Optional[str] = None
    nodo: Optional[str] = None
    aisla: Optional[str] = Field(default=None, max_length=120)
    diametro: Optional[float] = Field(default=None, gt=0)

    @field_validator("nombre", "aisla", "tuberia", "nodo")
    @classmethod
    def sin_espacios_sobrantes(cls, v):
        return v.strip() if isinstance(v, str) else v


class AveriaRequest(BaseModel):
    tuberia_averiada: str = Field(min_length=1)


Material = Literal["pvc", "polietileno", "fibrocemento"]


class TuberiaMaterial(BaseModel):
    material: Material
    # PN real marcada en la tubería, en bar, si se conoce. Si no se indica,
    # se usa el valor por defecto de la clase mínima habitual del material.
    pn: Optional[float] = Field(default=None, gt=0, le=100)
