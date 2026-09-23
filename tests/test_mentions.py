from social_analytics.helpers import extract_mentions


def test_extract_mentions():
    assert extract_mentions("Gracias @Ane_Data y @jon_py") == ["ane_data", "jon_py"]


def test_extract_mentions_sin_menciones():
    assert extract_mentions("sin menciones") == []
