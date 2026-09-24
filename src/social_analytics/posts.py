"""Análisis de publicaciones y hashtags."""

import pandas as pd

from social_analytics.helpers import extract_hashtags

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def posts_per_user(posts: pd.DataFrame) -> pd.Series:
    """Número de publicaciones de cada autor, de mayor a menor."""
    return posts["author_id"].value_counts().rename("posts")


def posts_by_weekday(posts: pd.DataFrame) -> pd.Series:
    """Número de publicaciones por día de la semana (de lunes a domingo)."""
    weekdays = posts["created_at"].dt.day_name()
    return weekdays.value_counts().reindex(WEEKDAYS, fill_value=0).rename("posts")


def top_hashtags(posts: pd.DataFrame, limit: int = 10) -> pd.Series:
    """Hashtags más utilizados. Cada publicación cuenta una sola vez por hashtag."""
    tags = posts["text"].map(lambda text: sorted(set(extract_hashtags(text)))).explode().dropna()
    counts = tags.value_counts().sort_index().sort_values(ascending=False, kind="stable")
    return counts.head(limit).rename("posts")


def top_posts(
    posts: pd.DataFrame,
    interactions: pd.DataFrame,
    *,
    limit: int = 10,
    min_interactions: int = 0,
) -> pd.DataFrame:
    """Las ``limit`` publicaciones con más interacciones.

    Solo se tienen en cuenta las publicaciones con al menos ``min_interactions``.
    Los argumentos con nombre siguen la misma convención que ``top_hashtags``.
    """
    counts = interactions.groupby("post_id").size().rename("interactions")
    ranked = posts.set_index("post_id").join(counts).fillna({"interactions": 0})
    ranked["interactions"] = ranked["interactions"].astype(int)
    ranked = ranked[ranked["interactions"] >= min_interactions]
    ranked = ranked.sort_values(["interactions", "created_at"], ascending=[False, True])
    return ranked.head(limit).reset_index()[["post_id", "author_id", "text", "interactions"]]
