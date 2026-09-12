"""Gráficos del análisis.

Se usa la API orientada a objetos de matplotlib (``Figure``) para no depender
de ninguna interfaz gráfica: funciona igual en scripts, tests y notebooks.
"""

from pathlib import Path

import pandas as pd
from matplotlib.figure import Figure

from social_analytics.interactions import interactions_by_kind
from social_analytics.users import users_by_country


def _save(fig: Figure, path: Path | str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=100, bbox_inches="tight")
    return path


def plot_users_by_country(users: pd.DataFrame, path: Path | str) -> Path:
    """Gráfico de barras con el número de usuarios por país."""
    counts = users_by_country(users)
    fig = Figure(figsize=(6, 4))
    ax = fig.subplots()
    ax.bar(counts.index.astype(str), counts.values, color="#4C72B0")
    ax.set_title("Usuarios por país")
    ax.set_ylabel("Usuarios")
    return _save(fig, path)


def plot_interactions_by_kind(interactions: pd.DataFrame, path: Path | str) -> Path:
    """Gráfico de barras con las interacciones de cada tipo."""
    counts = interactions_by_kind(interactions)
    fig = Figure(figsize=(5, 4))
    ax = fig.subplots()
    ax.bar(counts.index.astype(str), counts.values, color="#55A868")
    ax.set_title("Interacciones por tipo")
    ax.set_ylabel("Interacciones")
    return _save(fig, path)
