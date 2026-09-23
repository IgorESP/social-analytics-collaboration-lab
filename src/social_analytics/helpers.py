"""Utilidades de texto para las publicaciones de la red social."""

import re

HASHTAG_PATTERN = re.compile(r"#(\w+)")
MENTION_PATTERN = re.compile(r"@(\w+)")


def normalize_text(text: str) -> str:
    """Elimina espacios repetidos y recorta los extremos del texto."""
    return " ".join(str(text).split())


def _find_tokens(pattern: re.Pattern, text: str) -> list[str]:
    return [token.lower() for token in pattern.findall(str(text))]


def extract_hashtags(text: str) -> list[str]:
    """Devuelve los hashtags de un texto en minúsculas y sin el símbolo #."""
    return _find_tokens(HASHTAG_PATTERN, text)


def extract_mentions(text: str) -> list[str]:
    """Devuelve los usuarios mencionados (@usuario) en minúsculas y sin la @."""
    return _find_tokens(MENTION_PATTERN, text)
