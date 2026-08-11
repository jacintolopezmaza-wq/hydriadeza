# Modelo de red y maniobra de corte

## Elementos

- **Nodos**: uniones/cruces de la red. Id + coordenadas.
- **Tuberías**: aristas que unen dos nodos. Id + nodo_a + nodo_b. Opcionalmente
  llevan `material` (`pvc` | `polietileno` | `fibrocemento`) y `pn` (presión
  nominal real en bar, si se conoce). Ver [Presión máxima por material](#presión-máxima-por-material).
- **Válvulas**: cada una situada en un extremo de una tubería, junto a un nodo
  (`tuberia` + `nodo`). Es lo que define dónde se puede cortar.

## Segmentos

Un **segmento** es el conjunto de elementos que quedan conectados sin cruzar
ninguna válvula. Se calcula construyendo un grafo donde una tubería se conecta
con un nodo solo si **no** hay válvula en ese extremo, y hallando los
componentes conexos.

## Maniobra de corte

Ante una avería en una tubería:
1. Se localiza su segmento.
2. Las **válvulas a cerrar** son las del borde del segmento: aquellas donde
   exactamente uno de sus dos lados (tubería o nodo) está dentro del segmento.
3. Los nodos y tuberías del segmento son los que **quedan sin agua**.

## De dónde sale la topología

- **Modelo EPANET (`.inp`)**: usar la librería `wntr` para importar nodos,
  tuberías y válvulas directamente.
- **Digitalización manual**: capturar válvulas en campo (app `campo/`) y dibujar
  las tuberías como líneas entre nodos.

## Presión máxima por material

Cada tramo puede tener asignado un `material` y, si se conoce, su `pn` real
(presión nominal en bar marcada en la tubería). El límite de presión que se
compara contra la presión estática calculada en un punto (`app/core/materiales.py`)
es:

1. La `pn` real del tramo, si está documentada.
2. Si no, la clase mínima habitual del material (norma UNE-EN, valores de
   catálogo genéricos, no específicos de esta instalación):
   - PVC (UNE-EN 1452): PN6
   - Polietileno (UNE-EN 12201): PN6
   - Fibrocemento (UNE 88201): Clase A ≈ 5 bar
3. Si el tramo no tiene material asignado: 5 bar (el límite más restrictivo
   conocido), para no dar una falsa sensación de seguridad.

Editar el material de un tramo: `PATCH /api/tuberias/{id}` con
`{"material": "...", "pn": <bar o null>}`. Consultar el tramo más cercano a un
punto (para comparar su límite contra la presión estática ahí calculada):
`GET /api/tuberias/cercana?lat=..&lng=..`. La app de campo usa este segundo
endpoint automáticamente dentro de "Presión aquí" cuando hay backend
configurado, y expone el editor en Ajustes → *Materiales de tuberías*.

## Presión mínima/máxima para vivienda (CTE DB-HS4)

Además de la banda de servicio operativa (`pmin`/`pmax` en Ajustes, criterio
propio del operario) y del límite por material del tramo, "Presión aquí"
comprueba la presión estática calculada contra el **Código Técnico de la
Edificación, DB-HS4** (salubridad, suministro de agua): entre 100 y 500 kPa
(1–5 bar) en el punto de consumo de una vivienda. Es un valor normativo fijo,
no configurable, calculado en el cliente (`campo/index.html`, función
`mostrarPresion`).

Ten en cuenta que la CTE exige esa presión **en el grifo**, no en el suelo: el
cálculo actual no descuenta la altura de la vivienda ni las pérdidas de su
instalación interior, así que en edificios de varias plantas el valor real en
los pisos altos será menor que el mostrado.

## Pendiente (v2)

- Aislamiento no intencionado (segundas válvulas que aíslan de rebote).
- Estado abierta/cerrada dinámico y su efecto en el cálculo.
