"""Los notebooks deben ser JSON válido y ejecutarse de principio a fin.

Ejecutar solo la comprobación rápida (sin lanzar kernels):
    uv run pytest tests/test_notebooks.py -m "not notebook"
"""

from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "notebooks").glob("*.ipynb"))
CONFLICT_MARKERS = ("<<<<<<<", ">>>>>>>")


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_sin_marcas_de_conflicto(path):
    text = path.read_text(encoding="utf-8")
    assert not any(marker in text for marker in CONFLICT_MARKERS), "Hay marcas de conflicto sin resolver"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_es_json_valido(path):
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)


@pytest.mark.notebook
@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_se_ejecuta(path):
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=120, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()
