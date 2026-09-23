"""Carga y limpieza de los datos de la red social."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from social_analytics.text_utils import normalize_text
from social_analytics.schema import validate_columns

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
VALID_INTERACTIONS = ("like", "comment", "share")


@dataclass
class Dataset:
    """Las tres tablas del proyecto, ya limpias."""

    users: pd.DataFrame
    posts: pd.DataFrame
    interactions: pd.DataFrame


def load_csv(path: Path) -> pd.DataFrame:
    """Lee un CSV en UTF-8 y avisa con claridad si el fichero no existe."""
    if not path.exists():
        raise FileNotFoundError(f"No se encuentra el fichero de datos: {path}")
    return pd.read_csv(path, encoding="utf-8")


def clean_users(users: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres y países, y elimina usuarios duplicados."""
    validate_columns(users, "users")
    users = users.copy()
    users["username"] = users["username"].str.strip().str.lower()
    users["country"] = users["country"].str.strip().str.upper().replace("", pd.NA).fillna("DESCONOCIDO")
    users["signup_date"] = pd.to_datetime(users["signup_date"], errors="coerce")
    users["followers"] = users["followers"].fillna(0).astype(int)
    users["verified"] = users["verified"].astype(bool)
    return users.drop_duplicates(subset="user_id", keep="first").reset_index(drop=True)


def clean_posts(posts: pd.DataFrame) -> pd.DataFrame:
    """Descarta publicaciones vacías o duplicadas y normaliza el texto."""
    validate_columns(posts, "posts")
    posts = posts.dropna(subset=["text"]).copy()
    posts["text"] = posts["text"].map(normalize_text)
    posts = posts[posts["text"] != ""].copy()
    posts["created_at"] = pd.to_datetime(posts["created_at"], errors="coerce")
    return posts.drop_duplicates(subset="post_id", keep="first").reset_index(drop=True)


def clean_interactions(interactions: pd.DataFrame) -> pd.DataFrame:
    """Normaliza el tipo de interacción y descarta los tipos desconocidos."""
    validate_columns(interactions, "interactions")
    interactions = interactions.copy()
    interactions["kind"] = interactions["kind"].str.strip().str.lower()
    interactions = interactions[interactions["kind"].isin(VALID_INTERACTIONS)].copy()
    interactions["created_at"] = pd.to_datetime(interactions["created_at"], errors="coerce")
    return interactions.reset_index(drop=True)


def load_dataset(data_dir: Path = DATA_DIR) -> Dataset:
    """Carga y limpia las tres tablas del proyecto."""
    users = clean_users(load_csv(data_dir / "users.csv"))
    posts = clean_posts(load_csv(data_dir / "posts.csv"))
    interactions = clean_interactions(load_csv(data_dir / "interactions.csv"))
    return Dataset(users=users, posts=posts, interactions=interactions)
