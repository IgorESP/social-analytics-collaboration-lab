"""Utilidades de texto (normalización y hashtags) para las publicaciones."""

import re

HASHTAG_PATTERN = re.compile(r"#(\w+)")


def normalize_text(text: str) -> str:
    """Elimina espacios repetidos y recorta los extremos del texto."""
    return " ".join(str(text).split())


def extract_hashtags(text: str) -> list[str]:
    """Devuelve los hashtags de un texto en minúsculas y sin el símbolo #."""
    return [tag.lower() for tag in HASHTAG_PATTERN.findall(str(text))]
