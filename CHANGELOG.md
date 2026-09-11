# Registro de cambios

Todos los cambios relevantes del proyecto se documentan en este fichero.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [versionado semántico](https://semver.org/lang/es/).

## [Sin publicar]

### Añadido

- Datos ficticios de usuarios, publicaciones e interacciones con errores intencionados.
- Carga y limpieza de datos con contrato de columnas (`schema.py`).
- Análisis de usuarios, publicaciones, hashtags e interacciones.
- Tasa de engagement por autor.
- Informe de actividad en Markdown.

### Corregido

- `load_dataset` ya no depende del directorio de trabajo.
