"""Indicadores agregados para el panel de control (dashboard) del equipo."""

import pandas as pd

from social_analytics.data_loader import Dataset
from social_analytics.interactions import interactions_by_kind
from social_analytics.posts import top_hashtags, top_posts


def _as_dict(series: pd.Series) -> dict[str, int]:
    return {str(key): int(value) for key, value in series.items()}


def build_dashboard(ds: Dataset) -> dict:
    """Indicadores principales del panel, listos para convertir a JSON."""
    destacadas = top_posts(ds.posts, ds.interactions, n=3)
    return {
        "totales": {"usuarios": len(ds.users), "publicaciones": len(ds.posts), "interacciones": len(ds.interactions)},
        "interacciones_por_tipo": _as_dict(interactions_by_kind(ds.interactions)),
        "hashtags": _as_dict(top_hashtags(ds.posts, limit=5)),
        "publicaciones_destacadas": [
            {"post_id": int(row.post_id), "interacciones": int(row.interactions)} for row in destacadas.itertuples()
        ],
    }
