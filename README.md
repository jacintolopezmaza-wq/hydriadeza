# HydriaDeza · Red de Agua

Gestión y maniobras de corte de la red de agua potable. Localiza las llaves de
corte por aldea/calle y calcula automáticamente qué válvulas cerrar ante una
avería para aislar el tramo.

## Estructura

```
hydriadeza/
├── backend/            API FastAPI + motor de maniobras de corte
│   ├── main.py
│   ├── requirements.txt      dependencias de producción
│   ├── requirements-dev.txt  + pytest/httpx, para desarrollo
│   ├── tests/                 suite de pruebas automáticas
│   └── app/
│       ├── api/        endpoints (valvulas, tuberias, maniobra)
│       ├── core/       algoritmo (red_corte), geometría (geo),
│       │               límites por material (materiales), almacén (store)
│       ├── models/     esquemas Pydantic
│       └── data/       red.json (datos de ejemplo)
├── campo/              app de campo (una página) para registrar válvulas
│   └── index.html      → desplegable en GitHub Pages
├── simulador/          demo interactivo del flujo (sin GPS ni servidor)
│   └── index.html
├── frontend/           componentes para la app Next.js
│   └── components/MapaValvulas.jsx
└── docs/               modelo de datos y algoritmo
```

## Arrancar el backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Documentación interactiva en `http://localhost:8000/docs`.

### Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Los tests usan su propia copia temporal de `red.json`: nunca modifican los
datos reales del repo. Corre `pytest` antes de subir cualquier cambio al
backend.

### Endpoints

- `GET    /api/valvulas` — válvulas en GeoJSON (para el mapa)
- `POST   /api/valvulas` — registrar una válvula (material/diámetro opcionales, sin necesitar plano)
- `DELETE /api/valvulas/{id}` — eliminar una válvula
- `GET    /api/valvulas/cercana?lat=&lng=` — válvula documentada más próxima a un punto
- `GET    /api/tuberias` — tramos con su material/PN (solo si hay topología cargada)
- `PATCH  /api/tuberias/{id}` — asignar material/PN real a un tramo
- `GET    /api/tuberias/cercana?lat=&lng=` — tramo del plano más próximo a un punto
- `POST   /api/maniobra` — `{"tuberia_averiada": "P3"}` → válvulas a cerrar + zona afectada

## App de campo

Sube `campo/index.html` y actívalo en **GitHub Pages**. Ábrelo en el móvil
(HTTPS) para capturar válvulas con GPS. En Ajustes puedes indicar la URL de
tu backend para sincronizar las válvulas entre operarios; sin ella funciona
igualmente en local (LocalStorage del navegador).

## Simulador

Abre `simulador/index.html` en cualquier navegador para ver el flujo completo.

## Modelo

Ver [`docs/MODELO.md`](docs/MODELO.md).
