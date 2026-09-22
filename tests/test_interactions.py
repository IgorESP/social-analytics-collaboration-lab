import pytest

from social_analytics.interactions import (
    engagement_rate,
    interactions_by_kind,
    interactions_per_post,
    most_active_actors,
)


def test_interactions_by_kind(mini_dataset):
    assert interactions_by_kind(mini_dataset.interactions).to_dict() == {"like": 3, "comment": 1, "share": 1}


def test_interactions_per_post(mini_dataset):
    assert interactions_per_post(mini_dataset.interactions).to_dict() == {10: 2, 11: 1, 12: 2}


def test_engagement_rate(mini_dataset):
    rate = engagement_rate(mini_dataset.posts, mini_dataset.interactions, mini_dataset.users)
    assert rate.to_dict() == pytest.approx({1: 0.03, 2: 0.04, 3: 0.0})


def test_most_active_actors(mini_dataset):
    top = most_active_actors(mini_dataset.interactions, mini_dataset.users, n=1)
    assert top["user_id"].tolist() == [2]
    assert top["interactions"].tolist() == [2]


def test_engagement_rate_autor_sin_seguidores(mini_dataset):
    """Un autor con 0 seguidores no debe tener engagement infinito."""
    users = mini_dataset.users.assign(followers=[100, 0, 10])
    rate = engagement_rate(mini_dataset.posts, mini_dataset.interactions, users)
    assert rate[2] == 0


def test_engagement_rate_datos_reales_sin_infinitos(dataset):
    rate = engagement_rate(dataset.posts, dataset.interactions, dataset.users)
    assert rate.notna().all()
    assert rate.max() < float("inf")
