import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import app.core.store as store
import main

RED_ORIGINAL = Path(__file__).resolve().parent.parent / "app" / "data" / "red.json"


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Cliente de pruebas con su propia copia de red.json: cada test parte
    de los mismos datos de ejemplo y nunca toca el fichero real del repo."""
    red_temporal = tmp_path / "red.json"
    shutil.copy(RED_ORIGINAL, red_temporal)
    monkeypatch.setattr(store, "RED_PATH", red_temporal)
    return TestClient(main.app)
