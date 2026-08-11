from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import valvulas, maniobra, tuberias

app = FastAPI(title="HydriaDeza · Red de Agua", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ajusta en producción
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(valvulas.router)
app.include_router(maniobra.router)
app.include_router(tuberias.router)


@app.get("/")
def raiz():
    return {"app": "HydriaDeza · Red de Agua", "docs": "/docs"}
