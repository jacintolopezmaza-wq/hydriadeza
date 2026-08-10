"""Almacén de datos de la red. De momento un JSON; sustituible por BD (SQLAlchemy)."""

import json
from pathlib import Path

RED_PATH = Path(__file__).resolve().parent.parent / "data" / "red.json"


def cargar_red():
    with open(RED_PATH, encoding="utf-8") as f:
        return json.load(f)


def guardar_red(red):
    with open(RED_PATH, "w", encoding="utf-8") as f:
        json.dump(red, f, ensure_ascii=False, indent=2)
