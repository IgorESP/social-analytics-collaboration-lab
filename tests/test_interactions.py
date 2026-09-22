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
    assert rate.to_dict() == pytest.approx({1: 0.06, 2: 0.04, 3: 0.0})


def test_most_active_actors(mini_dataset):
    top = most_active_actors(mini_dataset.interactions, mini_dataset.users, n=1)
    assert top["user_id"].tolist() == [2]
    assert top["interactions"].tolist() == [2]


def test_engagement_rate_pondera_por_tipo(mini_dataset):
    """Un share (3) vale más que un comment (2) y este más que un like (1)."""
    solo_post_11 = mini_dataset.interactions[mini_dataset.interactions["post_id"] == 11]
    rate = engagement_rate(mini_dataset.posts, solo_post_11, mini_dataset.users)
    assert rate[1] == pytest.approx(3 / 100)
