from social_analytics.helpers import extract_mentions
from social_analytics.posts import top_mentions


def test_extract_mentions():
    assert extract_mentions("Gracias @Ane_Data y @jon_py") == ["ane_data", "jon_py"]


def test_extract_mentions_sin_menciones():
    assert extract_mentions("sin menciones") == []


def test_top_mentions(mini_dataset):
    posts = mini_dataset.posts.assign(text=["Hola @ane", "Gracias @ane y @jon", "Nada"])
    assert top_mentions(posts).to_dict() == {"ane": 2, "jon": 1}
