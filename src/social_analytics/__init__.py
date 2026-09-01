"""Social Analytics: análisis de una red social ficticia con Pandas."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("social-analytics")
except PackageNotFoundError:  # código usado sin instalar el paquete
    __version__ = "0.0.0"
