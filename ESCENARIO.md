# Escenario G01: Dos ramas modifican las mismas líneas de una función

- **Aprendizaje:** Conflicto de contenido
- **Herramientas:** git merge, editor
- **Ramas:** `ejercicio/g01-alumno-a`, `ejercicio/g01-alumno-b` y `integracion/g01` (destino de las PR); punto de partida: etiqueta `lab/g01/base`

## Contexto

Las dos personas de la pareja han mejorado `engagement_rate` (`src/social_analytics/interactions.py`) a la vez y sin coordinarse. La persona A pondera las interacciones por tipo. La persona B corrige un error con los autores que no tienen seguidores. Las dos mejoras son necesarias.

## Qué hay que investigar

¿Qué líneas han tocado las dos ramas? ¿Se puede quedar solo una versión o hay que combinarlas?

## Tareas

1. Identificad el punto de partida: `uv run python scripts/lab.py info g01` y `git show lab/g01/base:ESCENARIO.md`.
2. Examinad el historial: `git log --oneline --graph lab/g01/base ejercicio/g01-alumno-a ejercicio/g01-alumno-b integracion/g01`.
3. Revisad las diferencias entre ramas: `git diff lab/g01/base ejercicio/g01-alumno-a` (y lo mismo con la rama B).
4. A abre una PR de `ejercicio/g01-alumno-a` hacia `integracion/g01`. B la revisa, comenta al menos una línea y la aprueba.
5. Integrad la PR de A en GitHub.
6. B abre su PR hacia `integracion/g01` y observa el aviso de conflictos.
7. Resolved el conflicto en local: actualizad la rama de B con `integracion/g01`, combinad las dos mejoras y ejecutad `uv run pytest`.
8. Publicad la rama resuelta, comprobad que la PR ya no tiene conflictos e integradla.

## Evidencias

- Captura o enlace de las dos PR y del comentario de revisión.
- Fragmento con las marcas de conflicto antes de resolver (`<<<<<<<`, `=======`, `>>>>>>>`).
- Versión final de `engagement_rate` y salida de `uv run pytest`.

## Restaurar el escenario

`uv run python scripts/lab.py restaurar g01` devuelve las ramas a su estado original y guarda vuestro trabajo en ramas `respaldo/...`.
