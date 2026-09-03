"""Contrato de datos: columnas obligatorias de cada tabla.

Cualquier cambio en estas listas es un cambio de contrato: afecta a los CSV
de ``data/``, al código que los usa y a los notebooks. Revísalo en equipo.
"""

import pandas as pd

SCHEMAS: dict[str, list[str]] = {
    "users": ["user_id", "username", "country", "signup_date", "followers", "verified"],
    "posts": ["post_id", "author_id", "created_at", "text"],
    "interactions": ["interaction_id", "post_id", "actor_id", "kind", "created_at"],
}


class SchemaError(ValueError):
    """La tabla no cumple el contrato de datos."""


def validate_columns(df: pd.DataFrame, table: str) -> None:
    """Comprueba que ``df`` tiene todas las columnas obligatorias de ``table``."""
    missing = [column for column in SCHEMAS[table] if column not in df.columns]
    if missing:
        raise SchemaError(f"La tabla '{table}' no tiene las columnas obligatorias: {missing}")
