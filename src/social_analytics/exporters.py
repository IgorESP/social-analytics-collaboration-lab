"""Exportación de los datos limpios a otros formatos."""

from pathlib import Path

import pandas as pd

from social_analytics.data_loader import Dataset


def export_to_excel(ds: Dataset, path: Path | str) -> Path:
    """Guarda usuarios, publicaciones e interacciones en hojas de un mismo Excel."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        ds.users.to_excel(writer, sheet_name="usuarios", index=False)
        ds.posts.to_excel(writer, sheet_name="publicaciones", index=False)
        ds.interactions.to_excel(writer, sheet_name="interacciones", index=False)
    return path
