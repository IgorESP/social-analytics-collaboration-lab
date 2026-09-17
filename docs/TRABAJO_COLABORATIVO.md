# Guía de trabajo colaborativo

Cada pareja trabaja en **su propio repositorio de GitHub**. Lo publica la
persona A y la persona B entra como colaboradora. No se usan forks: todas
las ramas y todas las pull requests (PR) viven en el mismo repositorio.

## 1. Publicar el repositorio en GitHub (alumno/a A)

Requisito: haber recuperado el bundle y creado todas las ramas locales
([INSTALACION.md](INSTALACION.md#3-alumnoa-a-recuperar-el-repositorio-desde-el-bundle)).

### Opción A: desde la web de GitHub

1. En GitHub: **New repository**.
2. Nombre: `social-analytics-collaboration-lab`. Visibilidad: la que indique el profesorado (por defecto, **Private**).
3. **No** marques «Add a README», «.gitignore» ni «license»: el repositorio debe crearse **vacío**.
4. Copia la URL HTTPS o SSH que muestra GitHub y, en el repositorio local:

```bash
git remote add origin https://github.com/<tu-usuario>/social-analytics-collaboration-lab.git
git push -u origin main          # primero main: será la rama por defecto
git push origin --all            # el resto de ramas (escenarios, ejercicios, integración)
git push origin --tags           # etiquetas v1.0.0 y lab/<id>/* (necesarias para restaurar)
```

### Opción B: con GitHub CLI

```bash
gh auth login
gh repo create social-analytics-collaboration-lab --private --source=. --remote=origin
git push -u origin main
git push origin --all
git push origin --tags
```

### Comprobación

```bash
git ls-remote --heads origin | wc -l     # 25 ramas
git ls-remote --tags origin | grep -c lab/   # 32 etiquetas lab/*
```

En GitHub, comprueba que la rama por defecto es `main` (**Settings → General
→ Default branch**).

## 2. Incorporar a la pareja como colaboradora

1. A: **Settings → Collaborators → Add people**, busca el usuario de B y envía la invitación.
2. B: acepta la invitación (correo o <https://github.com/notifications>).
3. B: clona el repositorio ([INSTALACION.md](INSTALACION.md#4-alumnob-b-clonar-el-repositorio-de-la-pareja)).
4. Si el profesorado lo pide, invitadle también para que pueda revisar las PR.

> Las normas de protección de ramas no están disponibles en repositorios
> privados de cuentas gratuitas. En este laboratorio la norma «solo se integra
> mediante PR revisada» es un **acuerdo de la pareja**.

## 3. Modelo de ramas

```text
main (v1.0.0)                     estable: no se trabaja en ella
 └── lab/g01/base (etiqueta)      punto de partida del caso: ESCENARIO.md
      ├── ejercicio/g01-alumno-a  trabajo de A
      ├── ejercicio/g01-alumno-b  trabajo de B
      └── integracion/g01         destino de las PR del caso
```

- **Las PR de un escenario siempre van a `integracion/<id>`, nunca a `main`.**
  Así un escenario no contamina a los demás y cada uno puede repetirse.
- Si necesitas una corrección adicional, crea una rama nueva desde la de
  integración, por ejemplo `fix/g03-dashboard`, y abre otra PR.
- Las etiquetas `lab/<id>/base|a|b|integracion` guardan el estado original
  y son las que usa la restauración.
- **En grupos de tres**, la persona C no tiene rama propia en los casos: revisa
  las dos PR, integra y ejecuta los tests en la rama de integración.

## 4. Flujo de trabajo de cada escenario

| Paso | Qué hacer | Comandos de referencia |
|------|-----------|------------------------|
| 1. Punto de partida | Lee el enunciado y localiza la base | `uv run python scripts/lab.py info g01` · `git show lab/g01/base:ESCENARIO.md` |
| 2. Historial | Mira qué ha hecho cada rama | `git log --oneline --graph lab/g01/base ejercicio/g01-alumno-a ejercicio/g01-alumno-b` |
| 3. Diferencias | Compara las ramas con la base y entre sí | `git diff lab/g01/base ejercicio/g01-alumno-a` · `git diff ejercicio/g01-alumno-a ejercicio/g01-alumno-b --stat` |
| 4. Trabajo | Cada persona en su rama | `git switch ejercicio/g01-alumno-a` |
| 5. Commits | Pequeños y con mensajes descriptivos | `git add -p` · `git commit` |
| 6. Publicar | Sube la rama | `git push` (la primera vez: `git push -u origin <rama>`) |
| 7. Pull request | Base: `integracion/g01`; compare: tu rama | Web o `gh pr create --base integracion/g01` |
| 8. Revisión | La otra persona revisa | Pestaña **Files changed** |
| 9. Comentarios | Comentarios en línea, sugerencias, «Request changes» | **Review changes** |
| 10. Conflictos | Resuélvelos en local en la rama de la PR | `git merge origin/integracion/g01` |
| 11. Tests | Antes de pedir otra revisión | `uv run pytest` |
| 12. Integrar | «Create a merge commit» | botón **Merge pull request** |
| 13. Documentar | Descripción de la PR y evidencias en el cuaderno | — |

Turnaos: en cada escenario, una persona abre la primera PR y la otra revisa;
en el siguiente escenario, al revés.

## 5. Abrir una pull request

**Atención:** GitHub propone `main` como rama base. Cámbiala siempre a
`integracion/<id>`.

Web: **Pull requests → New pull request → base: `integracion/g01` ← compare:
`ejercicio/g01-alumno-a`**.

Con GitHub CLI:

```bash
gh pr create --base integracion/g01 --head ejercicio/g01-alumno-a \
  --title "G01: pondera las interacciones por tipo" \
  --body "Qué cambia, por qué y cómo se ha probado (uv run pytest)."
```

Una buena descripción de PR responde a: **qué** cambia, **por qué**, **cómo
se ha probado** y **qué debe mirar quien revisa**.

## 6. Revisar una pull request

1. Lee la descripción y la lista de commits.
2. En **Files changed**, comenta líneas concretas (botón `+`). Puedes proponer
   cambios con un bloque *suggestion*.
3. Descarga la rama y ejecuta los tests: `git fetch && git switch <rama> && uv run pytest`.
4. Termina la revisión con **Review changes**:
   - **Comment**: observaciones sin bloquear.
   - **Request changes**: hay que corregir algo antes de integrar.
   - **Approve**: lista para integrar.
5. Quien abrió la PR corrige con commits nuevos en la misma rama. La PR se actualiza sola al hacer `git push`.

Al revisar, buscad: cambios ajenos al objetivo, código de depuración, datos
modificados, tests eliminados, ficheros generados, notebooks con outputs y
mensajes de commit poco descriptivos. Ayuda automática:

```bash
uv run python scripts/lab.py revisar integracion/g01 ejercicio/g01-alumno-a
```

## 7. Resolver conflictos de una PR

GitHub avisa con «This branch has conflicts that must be resolved». El botón
**Resolve conflicts** solo sirve para conflictos sencillos de texto. Para
renombrados, borrados, `uv.lock` o notebooks, resuelve **en local**:

```bash
git switch ejercicio/g01-alumno-b
git pull                                  # trae lo último de tu rama
git fetch origin
git merge origin/integracion/g01          # trae lo ya integrado
git status                                # ficheros en conflicto
# ... edita, elimina las marcas <<<<<<< ======= >>>>>>> y combina los cambios ...
uv run pytest
git add <ficheros resueltos>
git commit                                # completa el merge
git push                                  # la PR se actualiza y deja de tener conflictos
```

Otros comandos útiles durante un conflicto:

```bash
git diff                     # qué queda por resolver
git log --merge --oneline    # commits implicados en el conflicto
git checkout --ours <f>      # quedarse con la versión de tu rama
git checkout --theirs <f>    # quedarse con la versión que se fusiona
git merge --abort            # cancelar y volver al estado anterior
```

Un merge sin conflictos **no garantiza** que el proyecto funcione: ejecuta
siempre los tests después de integrar.

## 8. Reescribir una rama ya publicada

A veces una PR debe rehacerse (por ejemplo, tras una revisión con «Request changes»). Si cambias commits que ya
estaban en GitHub, Git rechazará el `push` normal. Usa:

```bash
git push --force-with-lease
```

`--force-with-lease` solo sobrescribe si nadie ha subido commits nuevos a esa
rama. **Avisa antes a tu pareja.** Nunca reescribas `main`
ni una rama de integración compartida.

## 9. Restaurar un escenario

Para repetir un escenario desde el principio sin perder lo que habéis hecho:

```bash
uv run python scripts/lab.py restaurar g01             # ramas A, B e integración
uv run python scripts/lab.py restaurar g01 --rama b    # solo una rama
```

El script:

1. Se niega a continuar si hay un merge en curso o cambios sin commit.
2. Guarda el estado actual de cada rama en `respaldo/g01/<fecha>/<rama>`.
3. Devuelve cada rama a su etiqueta `lab/g01/...`.
4. Muestra los `git push --force-with-lease` necesarios para actualizar GitHub
   (o los ejecuta con `--publicar`).

Las PR ya integradas en GitHub no se deshacen; ciérralas o abre otras nuevas
tras restaurar. Para ver soluciones anteriores: `git branch --list "respaldo/*"`.

## 10. Documentar la solución

- En la **descripción de la PR**: problema, decisión tomada y cómo se ha comprobado.
- En el **cuaderno del alumnado**: rellenad las celdas de evidencias de cada
  ejercicio en una rama propia, por ejemplo `evidencias/pareja-07`, y abrid
  una PR hacia `main` al final del laboratorio si el profesorado lo pide.

## 11. Mensajes de commit

```text
tipo(ámbito): resumen en imperativo de menos de 72 caracteres

Cuerpo opcional: por qué se hace el cambio y qué consecuencias tiene.
```

Tipos habituales: `feat`, `fix`, `refactor`, `test`, `docs`, `build`,
`chore`, `perf`. Un `!` tras el tipo (`feat!:`) o una línea
`BREAKING CHANGE:` avisan de un cambio incompatible. Ejemplos en
`git log --oneline main`.
