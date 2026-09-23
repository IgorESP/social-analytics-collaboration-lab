from social_analytics.text_utils import extract_hashtags, normalize_text


def test_normalize_text_elimina_espacios_repetidos():
    assert normalize_text("  hola    mundo  ") == "hola mundo"


def test_extract_hashtags_en_minusculas():
    assert extract_hashtags("Aprendo #Python y #pandas") == ["python", "pandas"]


def test_extract_hashtags_texto_sin_hashtags():
    assert extract_hashtags("sin etiquetas") == []
