# Escenario G03: Dos ramas cambian de forma incompatible la interfaz de una función

- **Aprendizaje:** Conflicto funcional
- **Herramientas:** pytest
- **Ramas:** `ejercicio/g03-alumno-a`, `ejercicio/g03-alumno-b` y `integracion/g03` (destino de las PR); punto de partida: etiqueta `lab/g03/base`

## Contexto

La persona A ha cambiado la interfaz de `top_posts` para alinearla con `top_hashtags`. La persona B ha creado un módulo `dashboard.py` y un nuevo comando de la CLI que usan `top_posts`.

## Qué hay que investigar

¿El merge da algún aviso? ¿Funciona el proyecto después de integrar las dos ramas? ¿Por qué Git no puede detectarlo?

## Tareas

1. Identificad el punto de partida: `uv run python scripts/lab.py info g03` y `git show lab/g03/base:ESCENARIO.md`.
2. Examinad el historial: `git log --oneline --graph lab/g03/base ejercicio/g03-alumno-a ejercicio/g03-alumno-b integracion/g03`.
3. Revisad las diferencias entre ramas: `git diff lab/g03/base ejercicio/g03-alumno-a` (y lo mismo con la rama B).
4. Revisad las dos PR por separado: ¿pasan los tests en cada rama?
5. Integrad A y después B en `integracion/g03`.
6. Ejecutad `uv run pytest` en la rama de integración y analizad el error.
7. Corregid el problema en una rama nueva (`fix/g03-...`) y abrid una PR con la corrección.

## Evidencias

- Salida del merge (¿hubo conflictos?).
- Salida de pytest con el fallo y explicación de la causa.
- PR de corrección con una descripción que explique el cambio de interfaz.

## Restaurar el escenario

`uv run python scripts/lab.py restaurar g03` devuelve las ramas a su estado original y guarda vuestro trabajo en ramas `respaldo/...`.
