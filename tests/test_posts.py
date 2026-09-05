from social_analytics.posts import posts_by_weekday, posts_per_user, top_hashtags, top_posts


def test_posts_per_user(mini_dataset):
    assert posts_per_user(mini_dataset.posts).to_dict() == {1: 2, 2: 1}


def test_posts_by_weekday(mini_dataset):
    weekdays = posts_by_weekday(mini_dataset.posts)
    assert weekdays.index[0] == "Monday"
    assert weekdays["Monday"] == 1
    assert weekdays["Tuesday"] == 2
    assert weekdays.sum() == 3


def test_top_hashtags_agrupa_mayusculas(mini_dataset):
    assert top_hashtags(mini_dataset.posts).to_dict() == {"python": 2, "pandas": 1}


def test_top_hashtags_respeta_el_limite(dataset):
    assert len(top_hashtags(dataset.posts, limit=3)) == 3


def test_top_posts(mini_dataset):
    top = top_posts(mini_dataset.posts, mini_dataset.interactions, n=2)
    assert top["post_id"].tolist() == [10, 12]
    assert top["interactions"].tolist() == [2, 2]
