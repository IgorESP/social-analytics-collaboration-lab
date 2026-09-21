# Escenario J04: Una rama elimina una celda que otra modifica

- **Aprendizaje:** Conflicto borrar/modificar
- **Herramientas:** nbdime
- **Ramas:** `ejercicio/j04-alumno-a`, `ejercicio/j04-alumno-b` y `integracion/j04` (destino de las PR); punto de partida: etiqueta `lab/j04/base`

## Contexto

A ha eliminado el gráfico de hashtags de `notebooks/02_analisis_publicaciones.ipynb` porque lo consideraba redundante. B ha mejorado precisamente ese gráfico.

## Qué hay que investigar

¿Qué decisión debe tomar el equipo? ¿Cómo marca nbdime este tipo de conflicto?

## Tareas

1. Identificad el punto de partida: `uv run python scripts/lab.py info j04` y `git show lab/j04/base:ESCENARIO.md`.
2. Examinad el historial: `git log --oneline --graph lab/j04/base ejercicio/j04-alumno-a ejercicio/j04-alumno-b integracion/j04`.
3. Revisad las diferencias entre ramas: `git diff lab/j04/base ejercicio/j04-alumno-a` (y lo mismo con la rama B).
4. Integrad A y después B con nbdime activado.
5. Debatid en la PR si la celda se conserva o se elimina y dejad la decisión por escrito.
6. Aplicad la decisión, eliminad cualquier marca de conflicto y ejecutad los tests de notebooks.

## Evidencias

- Marca de conflicto que deja nbdime en la celda.
- Comentario de la PR con la decisión y su justificación.

## Restaurar el escenario

`uv run python scripts/lab.py restaurar j04` devuelve las ramas a su estado original y guarda vuestro trabajo en ramas `respaldo/...`.
