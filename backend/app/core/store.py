"""Almacén de datos de la red.

Si están definidas SUPABASE_URL y SUPABASE_KEY usa Postgres (Supabase):
persiste entre despliegues, necesario en producción. Si no, cae a un
fichero JSON local — así el desarrollo y los tests no necesitan Supabase.
"""

import json
import os
from pathlib import Path

RED_PATH = Path(__file__).resolve().parent.parent / "data" / "red.json"

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

_cliente = None
if SUPABASE_URL and SUPABASE_KEY:
    from supabase import create_client
    _cliente = create_client(SUPABASE_URL, SUPABASE_KEY)


def cargar_red():
    if _cliente:
        r = _cliente.table("red_estado").select("datos").eq("id", 1).single().execute()
        return r.data["datos"]
    with open(RED_PATH, encoding="utf-8") as f:
        return json.load(f)


def guardar_red(red):
    if _cliente:
        _cliente.table("red_estado").update({"datos": red}).eq("id", 1).execute()
        return
    with open(RED_PATH, "w", encoding="utf-8") as f:
        json.dump(red, f, ensure_ascii=False, indent=2)
