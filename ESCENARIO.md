# Escenario J03: Dos ramas añaden celdas en la misma zona del notebook

- **Aprendizaje:** Inserciones concurrentes
- **Herramientas:** nbdime
- **Ramas:** `ejercicio/j03-alumno-a`, `ejercicio/j03-alumno-b` y `integracion/j03` (destino de las PR); punto de partida: etiqueta `lab/j03/base`

## Contexto

A y B han añadido cada una un análisis nuevo (dos celdas) justo después de la sección «Actividad por autor» de `notebooks/02_analisis_publicaciones.ipynb`.

## Qué hay que investigar

¿Cómo representa Git dos inserciones en el mismo punto del JSON? ¿Cómo lo trata nbdime? ¿Se ha conservado el trabajo de las dos personas?

## Tareas

1. Identificad el punto de partida: `uv run python scripts/lab.py info j03` y `git show lab/j03/base:ESCENARIO.md`.
2. Examinad el historial: `git log --oneline --graph lab/j03/base ejercicio/j03-alumno-a ejercicio/j03-alumno-b integracion/j03`.
3. Revisad las diferencias entre ramas: `git diff lab/j03/base ejercicio/j03-alumno-a` (y lo mismo con la rama B).
4. Integrad A y después B sin nbdime. Observad el resultado y cancelad.
5. Repetid con nbdime activado y comprobad celda por celda qué contiene el notebook resultante.
6. Conservad los dos análisis en un orden lógico y comprobad que el notebook se ejecuta.

## Evidencias

- Lista de celdas del notebook tras cada intento (`uv run nbshow --sources notebooks/02_analisis_publicaciones.ipynb`).
- Notebook final y resultado de `uv run pytest tests/test_notebooks.py`.

## Restaurar el escenario

`uv run python scripts/lab.py restaurar j03` devuelve las ramas a su estado original y guarda vuestro trabajo en ramas `respaldo/...`.
