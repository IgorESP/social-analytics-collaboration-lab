# Escenarios del laboratorio

El laboratorio tiene 8 casos independientes: 4 de código y estructura del proyecto (G01–G04)
y 4 de notebooks (J01–J04). Todos parten de la versión estable `v1.0.0` de `main`.

## Mapa de ramas

```text
main ── v1.0.0
  ├── lab/g01/base (etiqueta) ── enunciado ESCENARIO.md
  │     ├── ejercicio/g01-alumno-a     commits de la persona A
  │     ├── ejercicio/g01-alumno-b     commits de la persona B
  │     └── integracion/g01            destino de las PR
  ├── lab/g02/base
  │     └── ...
  └── lab/j04/base
        └── ...
```

- Las ramas A y B de un escenario parten **del mismo commit** (`lab/<id>/base`).
- Las ramas de integración parten de la base.
- Los conflictos **no están resueltos**: aparecen cuando intentáis integrar las ramas.
- Cada rama tiene una etiqueta con su estado original: `lab/<id>/base`, `lab/<id>/a`,
  `lab/<id>/b` y `lab/<id>/integracion`.

## Lista de escenarios

| ID | Incidencia | Aprendizaje | Herramientas | Sesión corta |
|----|------------|-------------|--------------|:--------:|
| G01 | Dos ramas modifican las mismas líneas de una función | Conflicto de contenido | git merge, editor | ✔ |
| G02 | Una rama renombra un módulo y otra lo modifica | Conflicto de estructura | git merge, git grep |  |
| G03 | Dos ramas cambian de forma incompatible la interfaz de una función | Conflicto funcional | pytest | ✔ |
| G04 | Dos ramas modifican pyproject.toml y las dependencias | Integración de configuración | uv lock, uv sync |  |
| J01 | Dos personas modifican la misma celda de un notebook | Conflicto en notebooks | nbdime | ✔ |
| J02 | Cambios innecesarios en outputs y metadatos | Limpieza de notebooks | nbstripout | ✔ |
| J03 | Dos ramas añaden celdas en la misma zona del notebook | Inserciones concurrentes | nbdime |  |
| J04 | Una rama elimina una celda que otra modifica | Conflicto borrar/modificar | nbdime |  |

## Contexto de cada escenario

### G01 · Dos ramas modifican las mismas líneas de una función

Las dos personas de la pareja han mejorado `engagement_rate` (`src/social_analytics/interactions.py`) a la vez y sin coordinarse. La persona A pondera las interacciones por tipo. La persona B corrige un error con los autores que no tienen seguidores. Las dos mejoras son necesarias.

- Ramas: `ejercicio/g01-alumno-a`, `ejercicio/g01-alumno-b` (desde la etiqueta `lab/g01/base`) · PR hacia `integracion/g01`
- Enunciado completo: `git show lab/g01/base:ESCENARIO.md`

### G02 · Una rama renombra un módulo y otra lo modifica

La persona A ha reorganizado el código: `helpers.py` pasa a llamarse `text_utils.py`. La persona B, que no lo sabía, ha añadido a `helpers.py` la extracción de menciones (@usuario) y un ranking de usuarios mencionados.

- Ramas: `ejercicio/g02-alumno-a`, `ejercicio/g02-alumno-b` (desde la etiqueta `lab/g02/base`) · PR hacia `integracion/g02`
- Enunciado completo: `git show lab/g02/base:ESCENARIO.md`

### G03 · Dos ramas cambian de forma incompatible la interfaz de una función

La persona A ha cambiado la interfaz de `top_posts` para alinearla con `top_hashtags`. La persona B ha creado un módulo `dashboard.py` y un nuevo comando de la CLI que usan `top_posts`.

- Ramas: `ejercicio/g03-alumno-a`, `ejercicio/g03-alumno-b` (desde la etiqueta `lab/g03/base`) · PR hacia `integracion/g03`
- Enunciado completo: `git show lab/g03/base:ESCENARIO.md`

### G04 · Dos ramas modifican pyproject.toml y las dependencias

Cada persona ha añadido una funcionalidad que necesita una dependencia nueva: A exporta a Excel (`openpyxl`) y B genera tablas Markdown (`tabulate`). Las dos han actualizado `pyproject.toml`, `uv.lock` y la versión del proyecto.

- Ramas: `ejercicio/g04-alumno-a`, `ejercicio/g04-alumno-b` (desde la etiqueta `lab/g04/base`) · PR hacia `integracion/g04`
- Enunciado completo: `git show lab/g04/base:ESCENARIO.md`

### J01 · Dos personas modifican la misma celda de un notebook

En `notebooks/02_analisis_publicaciones.ipynb`, A y B han cambiado la celda que analiza las interacciones por tipo: A las muestra en porcentaje y B añade un gráfico.

- Ramas: `ejercicio/j01-alumno-a`, `ejercicio/j01-alumno-b` (desde la etiqueta `lab/j01/base`) · PR hacia `integracion/j01`
- Enunciado completo: `git show lab/j01/base:ESCENARIO.md`

### J02 · Cambios innecesarios en outputs y metadatos

A y B han cambiado una celda distinta cada una de `notebooks/01_exploracion_usuarios.ipynb`. Antes de hacer commit ejecutaron el notebook completo y guardaron los resultados.

- Ramas: `ejercicio/j02-alumno-a`, `ejercicio/j02-alumno-b` (desde la etiqueta `lab/j02/base`) · PR hacia `integracion/j02`
- Enunciado completo: `git show lab/j02/base:ESCENARIO.md`

### J03 · Dos ramas añaden celdas en la misma zona del notebook

A y B han añadido cada una un análisis nuevo (dos celdas) justo después de la sección «Actividad por autor» de `notebooks/02_analisis_publicaciones.ipynb`.

- Ramas: `ejercicio/j03-alumno-a`, `ejercicio/j03-alumno-b` (desde la etiqueta `lab/j03/base`) · PR hacia `integracion/j03`
- Enunciado completo: `git show lab/j03/base:ESCENARIO.md`

### J04 · Una rama elimina una celda que otra modifica

A ha eliminado el gráfico de hashtags de `notebooks/02_analisis_publicaciones.ipynb` porque lo consideraba redundante. B ha mejorado precisamente ese gráfico.

- Ramas: `ejercicio/j04-alumno-a`, `ejercicio/j04-alumno-b` (desde la etiqueta `lab/j04/base`) · PR hacia `integracion/j04`
- Enunciado completo: `git show lab/j04/base:ESCENARIO.md`

## Consultar y restaurar

```bash
uv run python scripts/lab.py escenarios        # estado de todas las ramas
uv run python scripts/lab.py info g04          # punto de partida, commits y ficheros de un escenario
uv run python scripts/lab.py restaurar g04     # vuelve al estado original (con copia respaldo/*)
```

La restauración nunca borra trabajo: guarda el estado anterior de cada rama en
`respaldo/<id>/<fecha>/<rama>`. Ver [TRABAJO_COLABORATIVO.md](TRABAJO_COLABORATIVO.md#9-restaurar-un-escenario).
