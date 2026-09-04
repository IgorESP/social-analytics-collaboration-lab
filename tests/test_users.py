from social_analytics.users import active_users, follower_stats, top_users_by_followers, users_by_country


def test_users_by_country(mini_dataset):
    assert users_by_country(mini_dataset.users).to_dict() == {"ES": 2, "MX": 1}


def test_users_by_country_datos_reales(dataset):
    counts = users_by_country(dataset.users)
    assert counts.index[0] == "ES"
    assert counts.sum() == len(dataset.users)


def test_top_users_by_followers(mini_dataset):
    top = top_users_by_followers(mini_dataset.users, n=2)
    assert top["username"].tolist() == ["ane", "jon"]


def test_follower_stats(mini_dataset):
    stats = follower_stats(mini_dataset.users)
    assert stats["max"] == 100
    assert stats["median"] == 50


def test_active_users_incluye_la_fecha_limite(mini_dataset):
    activos = active_users(mini_dataset.interactions, mini_dataset.users, since="2026-09-09 10:00")
    assert set(activos["user_id"]) == {1, 3}
