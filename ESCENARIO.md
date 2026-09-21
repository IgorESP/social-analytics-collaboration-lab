# Escenario J02: Cambios innecesarios en outputs y metadatos

- **Aprendizaje:** Limpieza de notebooks
- **Herramientas:** nbstripout
- **Ramas:** `ejercicio/j02-alumno-a`, `ejercicio/j02-alumno-b` y `integracion/j02` (destino de las PR); punto de partida: etiqueta `lab/j02/base`

## Contexto

A y B han cambiado una celda distinta cada una de `notebooks/01_exploracion_usuarios.ipynb`. Antes de hacer commit ejecutaron el notebook completo y guardaron los resultados.

## Qué hay que investigar

¿Cuántas líneas cambia cada PR? ¿Cuántas corresponden a cambios de código? ¿Por qué hay conflictos si cada persona tocó una celda diferente?

## Tareas

1. Identificad el punto de partida: `uv run python scripts/lab.py info j02` y `git show lab/j02/base:ESCENARIO.md`.
2. Examinad el historial: `git log --oneline --graph lab/j02/base ejercicio/j02-alumno-a ejercicio/j02-alumno-b integracion/j02`.
3. Revisad las diferencias entre ramas: `git diff lab/j02/base ejercicio/j02-alumno-a` (y lo mismo con la rama B).
4. Mirad el tamaño de los diffs: `git diff --stat lab/j02/base ejercicio/j02-alumno-a` (y B).
5. Integrad A y después B en `integracion/j02`. Analizad los conflictos y cancelad el merge.
6. Activad nbstripout (`uv run python scripts/lab.py notebooks activar-nbstripout`). Cada persona, en su rama, guarda el notebook limpio (`git add --renormalize ...`), hace commit y publica (consultad docs/NOTEBOOKS.md si Git no os deja cambiar de rama).
7. Repetid la integración y comparad el resultado.

## Evidencias

- Líneas cambiadas antes y después de limpiar (`git diff --stat`).
- Número de conflictos antes y después de usar nbstripout.
- Explicación de qué elimina nbstripout y qué conserva.

## Restaurar el escenario

`uv run python scripts/lab.py restaurar j02` devuelve las ramas a su estado original y guarda vuestro trabajo en ramas `respaldo/...`.
