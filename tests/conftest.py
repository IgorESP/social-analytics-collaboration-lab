"""Fixtures compartidas por los tests."""

import pandas as pd
import pytest

from social_analytics.data_loader import Dataset, load_dataset


@pytest.fixture(scope="session")
def dataset() -> Dataset:
    """Conjunto de datos real del proyecto (carpeta data/), ya limpio."""
    return load_dataset()


@pytest.fixture
def mini_dataset() -> Dataset:
    """Conjunto de datos mínimo y controlado para comprobar cálculos exactos."""
    users = pd.DataFrame(
        {
            "user_id": [1, 2, 3],
            "username": ["ane", "jon", "sara"],
            "country": ["ES", "MX", "ES"],
            "signup_date": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-03-01"]),
            "followers": [100, 50, 10],
            "verified": [True, False, False],
        }
    )
    posts = pd.DataFrame(
        {
            "post_id": [10, 11, 12],
            "author_id": [1, 1, 2],
            "created_at": pd.to_datetime(["2026-09-07 10:00", "2026-09-08 11:00", "2026-09-08 12:00"]),
            "text": ["Hola #Python", "Más #python y #pandas", "Nada que decir"],
        }
    )
    interactions = pd.DataFrame(
        {
            "interaction_id": [1, 2, 3, 4, 5],
            "post_id": [10, 10, 11, 12, 12],
            "actor_id": [2, 3, 2, 1, 3],
            "kind": ["like", "comment", "share", "like", "like"],
            "created_at": pd.to_datetime(
                ["2026-09-07 12:00", "2026-09-07 13:00", "2026-09-09 09:00", "2026-09-09 10:00", "2026-09-10 10:00"]
            ),
        }
    )
    return Dataset(users=users, posts=posts, interactions=interactions)
