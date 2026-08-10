# hydriadeza· Red de Agua

Gestión y maniobras de corte de la red de agua potable. Localiza las llaves de
corte por aldea/calle y calcula automáticamente qué válvulas cerrar ante una
avería para aislar el tramo.

## Estructura

```
flownodo-red/
├── backend/            API FastAPI + motor de maniobras de corte
│   ├── main.py
│   ├── requirements.txt
│   └── app/
│       ├── api/        endpoints (valvulas, maniobra)
│       ├── core/       algoritmo de segmentación (red_corte) + almacén
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

### Endpoints

- `GET  /api/valvulas` — válvulas en GeoJSON (para el mapa)
- `POST /api/valvulas` — registrar una válvula capturada en campo
- `POST /api/maniobra` — `{"tuberia_averiada": "P3"}` → válvulas a cerrar + zona afectada

## App de campo

Sube `campo/index.html` y actívalo en **GitHub Pages**. Ábrelo en el móvil
(HTTPS) para capturar válvulas con GPS.

## Simulador

Abre `simulador/index.html` en cualquier navegador para ver el flujo completo.

## Modelo

Ver [`docs/MODELO.md`](docs/MODELO.md).
