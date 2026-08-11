"""Presión nominal (PN) máxima admisible por material de tubería.

Valores de catálogo genéricos según norma UNE-EN, no específicos de una
instalación real:

  - PVC          (UNE-EN 1452):  clase mínima habitual PN6
  - Polietileno  (UNE-EN 12201): clase mínima habitual PN6
  - Fibrocemento (UNE 88201):    Clase A (~5 bar), la más débil de las
                                  clases históricas (A/B/C/D); material en
                                  desuso y a menudo el eslabón más frágil
                                  de una red mixta.

Cuando se conozca la PN real marcada en la tubería (a menudo indicada en
los planos de obra o en la propia tubería), regístrala en el tramo
correspondiente: prevalece siempre sobre el valor por defecto.
"""

from typing import Optional

PN_POR_DEFECTO_BAR = {
    "pvc": 6.0,
    "polietileno": 6.0,
    "fibrocemento": 5.0,
}

# Material sin documentar todavía: se asume el límite más restrictivo
# conocido (fibrocemento) para no dar una falsa sensación de seguridad.
PN_DESCONOCIDO_BAR = 5.0


def pn_limite(material: Optional[str], pn_conocido: Optional[float]) -> float:
    if pn_conocido:
        return pn_conocido
    if material in PN_POR_DEFECTO_BAR:
        return PN_POR_DEFECTO_BAR[material]
    return PN_DESCONOCIDO_BAR
