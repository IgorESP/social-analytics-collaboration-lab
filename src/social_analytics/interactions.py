"""Métricas de interacción y engagement."""

import pandas as pd

INTERACTION_WEIGHTS = {"like": 1, "comment": 2, "share": 3}


def interactions_by_kind(interactions: pd.DataFrame) -> pd.Series:
    """Número de interacciones de cada tipo (like, comment, share)."""
    return interactions["kind"].value_counts().rename("interactions")


def interactions_per_post(interactions: pd.DataFrame) -> pd.Series:
    """Número de interacciones recibidas por cada publicación."""
    return interactions.groupby("post_id").size().rename("interactions")


def engagement_rate(posts: pd.DataFrame, interactions: pd.DataFrame, users: pd.DataFrame) -> pd.Series:
    """Tasa de engagement de cada autor.

    engagement = interacciones ponderadas / seguidores
    (pesos: like=1, comment=2, share=3)
    """
    received = interactions.merge(posts[["post_id", "author_id"]], on="post_id")
    totals = received["kind"].map(INTERACTION_WEIGHTS).groupby(received["author_id"]).sum()
    followers = users.set_index("user_id")["followers"]
    rate = totals / followers
    return rate.fillna(0).sort_values(ascending=False).rename("engagement_rate")


def most_active_actors(interactions: pd.DataFrame, users: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Los ``n`` usuarios que más interactúan con las publicaciones."""
    counts = interactions.groupby("actor_id").size().rename("interactions")
    result = users.set_index("user_id")[["username", "country"]].join(counts, how="inner").rename_axis("user_id")
    return result.nlargest(n, "interactions").reset_index()
