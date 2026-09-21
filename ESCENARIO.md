# Escenario G02: Una rama renombra un módulo y otra lo modifica

- **Aprendizaje:** Conflicto de estructura
- **Herramientas:** git merge, git grep
- **Ramas:** `ejercicio/g02-alumno-a`, `ejercicio/g02-alumno-b` y `integracion/g02` (destino de las PR); punto de partida: etiqueta `lab/g02/base`

## Contexto

La persona A ha reorganizado el código: `helpers.py` pasa a llamarse `text_utils.py`. La persona B, que no lo sabía, ha añadido a `helpers.py` la extracción de menciones (@usuario) y un ranking de usuarios mencionados.

## Qué hay que investigar

¿Detecta Git el renombrado? ¿Qué cambios de B llegan al fichero nuevo y qué referencias al nombre antiguo quedan?

## Tareas

1. Identificad el punto de partida: `uv run python scripts/lab.py info g02` y `git show lab/g02/base:ESCENARIO.md`.
2. Examinad el historial: `git log --oneline --graph lab/g02/base ejercicio/g02-alumno-a ejercicio/g02-alumno-b integracion/g02`.
3. Revisad las diferencias entre ramas: `git diff lab/g02/base ejercicio/g02-alumno-a` (y lo mismo con la rama B).
4. Integrad primero la PR de A en `integracion/g02`.
5. Integrad después la rama de B en local y anotad qué ficheros indica Git en conflicto y por qué.
6. Resolved los conflictos y ejecutad `uv run pytest`. Si algo falla, buscad la causa con `git grep`.
7. Dejad el proyecto sin ninguna referencia al módulo antiguo y documentad la decisión en la PR.

## Evidencias

- Salida de `git status` durante el merge.
- Salida de `git log --follow --oneline -- src/social_analytics/text_utils.py`.
- Lista de referencias al módulo antiguo que encontrasteis y cómo las corregisteis.

## Restaurar el escenario

`uv run python scripts/lab.py restaurar g02` devuelve las ramas a su estado original y guarda vuestro trabajo en ramas `respaldo/...`.
