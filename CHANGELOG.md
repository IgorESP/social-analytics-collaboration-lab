# Registro de cambios

Todos los cambios relevantes del proyecto se documentan en este fichero.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [versionado semántico](https://semver.org/lang/es/).

## [Sin publicar]

## [1.0.0] - 2026-09-20

### Añadido

- Datos ficticios de usuarios, publicaciones e interacciones con errores intencionados.
- Carga y limpieza de datos con contrato de columnas (`schema.py`).
- Análisis de usuarios, publicaciones, hashtags e interacciones.
- Tasa de engagement por autor.
- Informe de actividad en Markdown y gráficos en PNG.
- Comando `social-analytics` con las órdenes `resumen`, `informe` y `graficos`.
- Notebooks de exploración de usuarios y de publicaciones.
- Herramientas de desarrollo: pytest, nbstripout y nbdime.
- Script `scripts/lab.py` y documentación del laboratorio.

### Corregido

- `load_dataset` ya no depende del directorio de trabajo.
