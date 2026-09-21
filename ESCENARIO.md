# Escenario G04: Dos ramas modifican pyproject.toml y las dependencias

- **Aprendizaje:** Integración de configuración
- **Herramientas:** uv lock, uv sync
- **Ramas:** `ejercicio/g04-alumno-a`, `ejercicio/g04-alumno-b` y `integracion/g04` (destino de las PR); punto de partida: etiqueta `lab/g04/base`

## Contexto

Cada persona ha añadido una funcionalidad que necesita una dependencia nueva: A exporta a Excel (`openpyxl`) y B genera tablas Markdown (`tabulate`). Las dos han actualizado `pyproject.toml`, `uv.lock` y la versión del proyecto.

## Qué hay que investigar

¿Qué ficheros de configuración entran en conflicto? ¿Conviene resolver `uv.lock` a mano? ¿Qué versión debe tener el proyecto?

## Tareas

1. Identificad el punto de partida: `uv run python scripts/lab.py info g04` y `git show lab/g04/base:ESCENARIO.md`.
2. Examinad el historial: `git log --oneline --graph lab/g04/base ejercicio/g04-alumno-a ejercicio/g04-alumno-b integracion/g04`.
3. Revisad las diferencias entre ramas: `git diff lab/g04/base ejercicio/g04-alumno-a` (y lo mismo con la rama B).
4. Integrad la PR de A y después intentad integrar la de B.
5. Resolved `pyproject.toml` a mano y regenerad `uv.lock` con uv, sin editarlo a mano.
6. Comprobad con `uv sync` y `uv run pytest` que funcionan las dos funcionalidades.
7. Justificad en la PR el número de versión elegido (versionado semántico).

## Evidencias

- Bloque `dependencies` y `version` final de `pyproject.toml`.
- Comandos usados para regenerar el lock y salida de `uv run pytest`.

## Restaurar el escenario

`uv run python scripts/lab.py restaurar g04` devuelve las ramas a su estado original y guarda vuestro trabajo en ramas `respaldo/...`.
