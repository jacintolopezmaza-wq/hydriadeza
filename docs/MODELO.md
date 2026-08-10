# Modelo de red y maniobra de corte

## Elementos

- **Nodos**: uniones/cruces de la red. Id + coordenadas.
- **Tuberías**: aristas que unen dos nodos. Id + nodo_a + nodo_b.
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

## Pendiente (v2)

- Aislamiento no intencionado (segundas válvulas que aíslan de rebote).
- Estado abierta/cerrada dinámico y su efecto en el cálculo.
