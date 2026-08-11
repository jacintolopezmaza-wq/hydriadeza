# Modelo de red y maniobra de corte

## Elementos

- **Nodos**: uniones/cruces de la red. Id + coordenadas.
- **Tuberías**: aristas que unen dos nodos. Id + nodo_a + nodo_b. Opcionalmente
  llevan `material` (`pvc` | `polietileno` | `fibrocemento`) y `pn` (presión
  nominal real en bar, si se conoce). Ver [Presión máxima por material](#presión-máxima-por-material).
- **Válvulas**: cada una situada en un extremo de una tubería, junto a un nodo
  (`tuberia` + `nodo`). Es lo que define dónde se puede cortar. `tuberia`/`nodo`
  son opcionales: la mayoría de averías se capturan sin plano de red, así que
  la válvula también puede llevar directamente su propio `material` y
  `diametro`, tal como se observan en el punto de la avería.

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

El límite de presión que se compara contra la presión estática calculada en
un punto (`app/core/materiales.py`) es, en orden de preferencia:

1. La `pn` real documentada, si se conoce.
2. Si no, la clase mínima habitual del material (norma UNE-EN, valores de
   catálogo genéricos, no específicos de esta instalación):
   - PVC (UNE-EN 1452): PN6
   - Polietileno (UNE-EN 12201): PN6
   - Fibrocemento (UNE 88201): Clase A ≈ 5 bar
3. Si no hay ningún material documentado cerca: 5 bar (el límite más
   restrictivo conocido), para no dar una falsa sensación de seguridad.

Hay dos fuentes posibles de material, y "Presión aquí" usa **la más cercana
de las dos, priorizando siempre la válvula sobre el tramo del plano** (la
válvula es el dato real que se captura en campo; el plano de tuberías rara
vez existe):

- **Por válvula** (caso normal, sin plano): cada válvula puede llevar su
  propio `material`/`diametro`, capturados directamente al registrarla.
  Consultar la más cercana a un punto: `GET /api/valvulas/cercana?lat=..&lng=..`.
- **Por tramo del plano** (solo si existe topología real, p. ej. importada
  de EPANET): `PATCH /api/tuberias/{id}` con `{"material": "...", "pn": <bar o null>}`,
  y `GET /api/tuberias/cercana?lat=..&lng=..` para consultar el tramo más
  cercano. Editor en Ajustes → *Materiales de tuberías*.

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
