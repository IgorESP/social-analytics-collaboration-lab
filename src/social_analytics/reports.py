"""Generación del informe de actividad en Markdown."""

from pathlib import Path

import pandas as pd

from social_analytics.data_loader import Dataset
from social_analytics.interactions import interactions_by_kind, most_active_actors
from social_analytics.posts import top_posts


def _bullet_list(series: pd.Series) -> str:
    return "\n".join(f"- {index}: {value}" for index, value in series.items())


def summary_section(ds: Dataset) -> str:
    """Totales generales del conjunto de datos."""
    totals = [
        f"- Usuarios: {len(ds.users)}",
        f"- Publicaciones: {len(ds.posts)}",
        f"- Interacciones: {len(ds.interactions)}",
    ]
    by_kind = _bullet_list(interactions_by_kind(ds.interactions))
    return "\n".join(totals) + "\n\nInteracciones por tipo:\n\n" + by_kind


def top_users_section(ds: Dataset) -> str:
    """Usuarios que más interactúan."""
    top = most_active_actors(ds.interactions, ds.users, n=5)
    lines = [f"{i}. @{row.username} ({row.country}): {row.interactions} interacciones" for i, row in enumerate(top.itertuples(), start=1)]
    return "\n".join(lines)


def top_posts_section(ds: Dataset) -> str:
    """Publicaciones con más interacciones."""
    top = top_posts(ds.posts, ds.interactions, limit=5)
    lines = [f"{i}. [{row.interactions}] {row.text}" for i, row in enumerate(top.itertuples(), start=1)]
    return "\n".join(lines)


def build_sections(ds: Dataset) -> list[tuple[str, str]]:
    """Secciones del informe en el orden en que se publican."""
    return [
        ("Resumen", summary_section(ds)),
        ("Usuarios más activos", top_users_section(ds)),
        ("Publicaciones destacadas", top_posts_section(ds)),
    ]


def generate_report(ds: Dataset) -> str:
    """Devuelve el informe completo en formato Markdown."""
    parts = ["# Informe de actividad de la red social", ""]
    for title, body in build_sections(ds):
        parts += [f"## {title}", "", body, ""]
    return "\n".join(parts)


def save_report(ds: Dataset, path: Path | str) -> Path:
    """Guarda el informe en ``path`` y crea la carpeta si no existe."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(generate_report(ds), encoding="utf-8")
    return path
