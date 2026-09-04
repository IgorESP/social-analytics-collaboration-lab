"""Análisis de usuarios."""

import pandas as pd


def users_by_country(users: pd.DataFrame) -> pd.Series:
    """Número de usuarios por país, de mayor a menor."""
    return users["country"].value_counts().rename("users")


def top_users_by_followers(users: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Los ``n`` usuarios con más seguidores."""
    columns = ["user_id", "username", "country", "followers"]
    return users.nlargest(n, "followers")[columns].reset_index(drop=True)


def follower_stats(users: pd.DataFrame) -> pd.Series:
    """Estadísticos básicos del número de seguidores."""
    return users["followers"].agg(["count", "mean", "median", "max"]).round(1)


def active_users(interactions: pd.DataFrame, users: pd.DataFrame, since: str) -> pd.DataFrame:
    """Usuarios con al menos una interacción desde la fecha ``since`` (incluida)."""
    recent = interactions[interactions["created_at"] >= pd.Timestamp(since)]
    counts = recent.groupby("actor_id").size().rename("interactions")
    result = users.set_index("user_id").join(counts, how="inner").rename_axis("user_id")
    return result.sort_values("interactions", ascending=False).reset_index()
