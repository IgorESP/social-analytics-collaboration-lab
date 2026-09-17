# social-analytics-collaboration-lab

Laboratorio práctico de **trabajo colaborativo con Git y GitHub** para el curso
de especialización en Inteligencia Artificial y Big Data (IABD).

El proyecto es una pequeña aplicación de análisis de una **red social ficticia**
escrita en Python con Pandas, matplotlib y Jupyter. Sobre ella se han preparado
**8 casos** (4 de código y estructura, 4 de notebooks) que trabajaréis por
parejas o en grupos de tres. En ellos tendréis que crear ramas, abrir pull requests, revisar el
código de la otra persona y resolver conflictos.

## Inicio rápido

```bash
uv sync                                   # crea .venv e instala dependencias
uv run pytest                             # todos los tests deben pasar en main
uv run social-analytics resumen           # Usuarios: 40 | Publicaciones: 119 | ...
uv run python scripts/lab.py entorno      # comprueba Git, uv y las ramas del laboratorio
```

La instalación completa, incluida la recuperación del repositorio desde el
fichero `.bundle`, está en [docs/INSTALACION.md](docs/INSTALACION.md).

## Guía de lectura: qué leer y en qué orden

Leed los documentos **en este orden**, en el momento indicado. El documento de trabajo principal es el
**cuaderno** (paso 4); el resto lo explica o sirve de consulta.

### Antes de empezar (todo el grupo)

| Orden | Fichero | Quién | Qué vais a encontrar |
|:-----:|---------|-------|----------------------|
| 1 | **Este README** | Todos | Qué es el proyecto, cómo está organizado y esta guía de lectura |
| 2 | [docs/INSTALACION.md](docs/INSTALACION.md) | Todos | Requisitos, configuración de Git y `uv sync`. **A:** apartado 3 (recuperar el bundle). **B y C:** apartado 4 (clonar de GitHub) |
| 3 | [docs/TRABAJO_COLABORATIVO.md](docs/TRABAJO_COLABORATIVO.md) | Todos | **A:** apartados 1 y 2 (publicar en GitHub e invitar al grupo). **Todos:** apartados 3 a 7 (ramas, flujo de trabajo, PR, revisión y conflictos) |
| 4 | [CUADERNO_ALUMNADO_GIT_COLABORATIVO.ipynb](CUADERNO_ALUMNADO_GIT_COLABORATIVO.ipynb) | Todos | **Documento de trabajo:** preparación, roles (A, B y C), enunciados de los 8 casos, parte libre y espacios para evidencias |
| 5 | [docs/ESCENARIOS.md](docs/ESCENARIOS.md) | Todos | Mapa de ramas y lista de los 8 casos, con su contexto |

### Al empezar cada caso

| Orden | Qué leer o ejecutar | Para qué |
|:-----:|---------------------|----------|
| 6 | El ejercicio correspondiente del **cuaderno** | Contexto, problema que hay que investigar, tareas y evidencias |
| 7 | `git show lab/<id>/base:ESCENARIO.md` | El mismo enunciado, guardado en el punto de partida del caso |
| 8 | `uv run python scripts/lab.py info <id>` | Commits de A y de B, ficheros que cambian y estado de la rama de integración |

### Antes de los casos de notebooks (J01–J04)

| Orden | Fichero | Para qué |
|:-----:|---------|----------|
| 9 | [docs/NOTEBOOKS.md](docs/NOTEBOOKS.md) | Por qué los notebooks dan problemas en Git; cómo activar nbstripout y nbdime en vuestro clon |

### Para consultar cuando lo necesitéis

| Fichero | Cuándo |
|---------|--------|
| [docs/INSTALACION.md](docs/INSTALACION.md), apartado 6 | Algo del entorno falla (uv, rutas largas, OneDrive, identidad de Git...) |
| [docs/TRABAJO_COLABORATIVO.md](docs/TRABAJO_COLABORATIVO.md), apartados 7 a 9 | Resolver conflictos, reescribir una rama publicada o restaurar un caso |
| [data/README.md](data/README.md) | Columnas de los CSV y contrato de datos (útil en la parte libre) |
| [CHANGELOG.md](CHANGELOG.md) | Cambios del proyecto; añadid aquí vuestras entradas si lo pide un reto |
| `uv run python scripts/lab.py --help` | Comprobar el entorno, ver el estado de los casos, restaurar, revisar una PR, activar nbstripout y nbdime |

## Estructura del proyecto

```text
.
├── data/                     # CSV ficticios (usuarios, publicaciones, interacciones)
├── docs/                     # documentación del laboratorio
├── notebooks/                # análisis exploratorio con Jupyter
├── scripts/lab.py            # comprobaciones, estado y restauración de escenarios
├── src/social_analytics/
│   ├── data_loader.py        # carga y limpieza
│   ├── schema.py             # contrato de datos (columnas obligatorias)
│   ├── helpers.py            # utilidades de texto (hashtags)
│   ├── users.py              # análisis de usuarios
│   ├── posts.py              # análisis de publicaciones
│   ├── interactions.py       # interacciones y engagement
│   ├── reports.py            # informe en Markdown
│   ├── visualization.py      # gráficos con matplotlib
│   └── cli.py                # comando social-analytics
├── tests/                    # pytest
├── CUADERNO_ALUMNADO_GIT_COLABORATIVO.ipynb
└── pyproject.toml / uv.lock  # proyecto y dependencias gestionados con uv
```

## Línea de comandos

```bash
uv run social-analytics resumen                      # totales
uv run social-analytics informe --salida salida/informe.md
uv run social-analytics graficos --carpeta salida    # PNG de usuarios por país e interacciones
```

La carpeta `salida/` está en `.gitignore`: los resultados generados no se versionan.

## Secciones del informe

`uv run social-analytics informe` genera un informe en Markdown con estas secciones:

1. **Resumen**: totales de usuarios, publicaciones e interacciones.
2. **Usuarios más activos**: quién interactúa más con las publicaciones.
3. **Publicaciones destacadas**: las publicaciones con más interacciones.

## Ramas del laboratorio

- `main`: versión estable 1.0.0 (etiqueta `v1.0.0`). **No se trabaja directamente en ella.**
- Etiqueta `lab/<id>/base`: punto de partida de cada caso, con su enunciado `ESCENARIO.md`.
- `ejercicio/<id>-alumno-a` y `ejercicio/<id>-alumno-b`: trabajo de cada miembro de la pareja.
- `integracion/<id>`: rama de destino de las pull requests de cada escenario.
- Etiquetas `lab/<id>/...`: estado original de cada rama, que se usa para restaurar.

Más detalles en [docs/ESCENARIOS.md](docs/ESCENARIOS.md).

## Tests

```bash
uv run pytest                      # todo (incluye ejecutar los notebooks)
uv run pytest -m "not notebook"    # rápido: sin ejecutar notebooks
uv run pytest tests/test_reports.py -v
```
