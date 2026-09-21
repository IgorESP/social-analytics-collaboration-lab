# Escenario J01: Dos personas modifican la misma celda de un notebook

- **Aprendizaje:** Conflicto en notebooks
- **Herramientas:** nbdime
- **Ramas:** `ejercicio/j01-alumno-a`, `ejercicio/j01-alumno-b` y `integracion/j01` (destino de las PR); punto de partida: etiqueta `lab/j01/base`

## Contexto

En `notebooks/02_analisis_publicaciones.ipynb`, A y B han cambiado la celda que analiza las interacciones por tipo: A las muestra en porcentaje y B añade un gráfico.

## Qué hay que investigar

¿Qué ocurre al fusionar con Git sin ayuda? ¿Se puede abrir el notebook? ¿Qué cambia al usar nbdime?

## Tareas

1. Identificad el punto de partida: `uv run python scripts/lab.py info j01` y `git show lab/j01/base:ESCENARIO.md`.
2. Examinad el historial: `git log --oneline --graph lab/j01/base ejercicio/j01-alumno-a ejercicio/j01-alumno-b integracion/j01`.
3. Revisad las diferencias entre ramas: `git diff lab/j01/base ejercicio/j01-alumno-a` (y lo mismo con la rama B).
4. Comparad las ramas con `git diff` y con `uv run nbdiff` (o `uv run nbdiff-web`).
5. Integrad A en `integracion/j01`. Fusionad B sin nbdime, intentad abrir el notebook y cancelad (`git merge --abort`).
6. Activad nbdime (`uv run python scripts/lab.py notebooks activar-nbdime`) y repetid el merge.
7. Combinad las dos ideas en la celda, comprobad que el notebook se ejecuta (`uv run pytest tests/test_notebooks.py`) y completad la integración.

## Evidencias

- Comparación de la salida de `git diff` y de `nbdiff` para la misma celda.
- Estado del notebook tras el merge con y sin nbdime.
- Celda final y resultado de los tests de notebooks.

## Restaurar el escenario

`uv run python scripts/lab.py restaurar j01` devuelve las ramas a su estado original y guarda vuestro trabajo en ramas `respaldo/...`.
