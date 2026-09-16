# Notebooks en Git: nbstripout y nbdime

Un notebook (`.ipynb`) es un fichero JSON. Contiene el código, las salidas
(tablas, imágenes en base64), los contadores de ejecución y metadatos. Git lo
compara línea a línea como cualquier texto, y eso causa dos problemas:

1. **Ruido:** ejecutar un notebook cambia cientos de líneas aunque el código no cambie.
2. **Conflictos ilegibles:** si Git inserta marcas `<<<<<<<` dentro del JSON,
   el notebook deja de ser JSON válido y Jupyter no puede abrirlo.

Las dos herramientas están instaladas con `uv sync` (grupo `dev`):

| Herramienta | Para qué sirve |
|-------------|----------------|
| **nbstripout** | Elimina outputs, contadores y metadatos de ejecución **antes de guardar en Git** |
| **nbdime** | Compara y fusiona notebooks **celda a celda** (`nbdiff`, `nbmerge`, interfaz web) |

## Configuración: siempre local y en cada clon

Instalar los paquetes con uv **no basta**. La integración con Git son
filtros y *drivers* que se guardan en `.git/config` y `.git/info/attributes`.
Esos ficheros no se versionan, así que **cada persona debe activarlos en su
clon**.

```bash
uv run python scripts/lab.py notebooks estado               # qué hay configurado
uv run python scripts/lab.py notebooks activar-nbstripout   # filtro clean + textconv para git diff
uv run python scripts/lab.py notebooks activar-nbdime       # diff/merge driver y herramientas web
uv run python scripts/lab.py notebooks desactivar-nbdime
uv run python scripts/lab.py notebooks desactivar-nbstripout
```

El script ejecuta los comandos que se muestran a continuación y escribe en
la configuración la **ruta absoluta** al Python del entorno `.venv`. Así
Git encuentra las herramientas aunque el entorno no esté activado.

### Equivalencia con los comandos oficiales

```bash
uv run nbstripout --install          # escribe en .git/config y .git/info/attributes
git config filter.nbstripout.clean "\"$(uv run python -c 'import sys; print(sys.executable)')\" -m nbstripout --keep-id"
uv run nbstripout --status
uv run nbdime config-git --enable    # ¡OJO! añade líneas al .gitattributes versionado
```

`nbstripout --install` no permite indicar `--keep-id`. Por eso el script
ajusta después el filtro (ver «Detalles útiles»).

`nbdime config-git --enable` modifica el fichero `.gitattributes` del
proyecto, que está en Git. Aparecerá como cambio pendiente en cada rama.
Además, configura el comando `git-nbmergedriver` sin ruta: si el entorno no
está activado, Git no lo encuentra (`command not found`). Por eso en este
laboratorio usamos `scripts/lab.py`.

## nbstripout

Con el filtro activo:

- `git add` guarda el notebook **sin outputs** aunque en tu disco los tenga.
- `git diff` muestra solo cambios de código y markdown (usa `nbstripout -t` como *textconv*).
- `git status` puede mostrar como modificado un notebook que se guardó con
  outputs: el filtro detecta que la versión limpia no coincide con la del
  repositorio. Mientras no hagas commit, **Git no te dejará cambiar de rama**
  («Your local changes ... would be overwritten») y `lab.py restaurar` se negará
  a continuar. Solución: guarda la versión limpia con
  `git add --renormalize <notebook>` y `git commit`, o descarta con
  `git switch --discard-changes <rama>` si no quieres guardarla.
- `git diff` usa la versión limpia, pero `git diff --stat` **no**: sigue
  contando las líneas reales del JSON.

Limpiar un notebook a mano (sin filtro):

```bash
uv run nbstripout --keep-id notebooks/01_exploracion_usuarios.ipynb
git diff --stat
```

Detalles útiles:

- Por defecto, nbstripout **renumera los `id` de las celdas** ("0", "1", ...).
  nbdime usa esos ids para emparejar las celdas de dos versiones. Si se
  renumeran, una celda insertada o borrada desplaza los ids de las
  siguientes y nbdime compara celdas que no se corresponden (por ejemplo,
  un título con un gráfico). Por eso en este proyecto usamos siempre
  `--keep-id` y los notebooks tienen ids estables y descriptivos.
- No elimina `metadata.language_info.version`. Para quitarla también:
  `git config filter.nbstripout.extrakeys "metadata.language_info.version"`.
- En Windows, nbstripout escribe los ficheros con CRLF. No pasa nada: el
  `.gitattributes` del proyecto los normaliza a LF al hacer `git add`.

## nbdime

```bash
uv run nbdiff notebooks/02_analisis_publicaciones.ipynb                     # cambios sin commit
uv run nbdiff lab/j01/base ejercicio/j01-alumno-a -- notebooks/02_analisis_publicaciones.ipynb
uv run nbdiff-web lab/j01/base ejercicio/j01-alumno-a -- notebooks/02_analisis_publicaciones.ipynb
uv run nbshow --sources notebooks/02_analisis_publicaciones.ipynb           # lista de celdas
```

Con el driver de merge activado (`activar-nbdime`), `git merge` fusiona
los notebooks celda a celda:

- Si dos ramas cambian celdas distintas, el merge es automático.
- Si hay conflicto, el notebook **sigue siendo JSON válido** y nbdime deja
  marcas legibles: dentro de la celda (`<<<<<<< local`, `=======`,
  `>>>>>>> remote`), como celdas marcadoras alrededor de grupos de celdas
  insertadas, o como `<<<<<<< LOCAL CELL DELETED >>>>>>>` cuando una rama
  borra una celda que la otra modifica. Ábrelo en Jupyter, decide, y elimina
  las marcas (y las celdas marcadoras).
- Herramienta visual: `uv run git mergetool --tool nbdime` abre `nbmerge-web`
  en el navegador para elegir celda a celda.

**Comprueba siempre el resultado de un merge de notebooks**, celda a celda
(`nbshow`) y ejecutándolo de principio a fin:

```bash
uv run pytest tests/test_notebooks.py -v
```

Un merge driver puede fallar. Si ves un `Traceback` en la salida de
`git merge`, el fichero puede haberse quedado con una sola de las versiones.

## Buenas prácticas

- Ejecuta «Restart & Run All» antes de dar por bueno un notebook.
- No guardes outputs en Git; si un resultado es importante, genéralo con código (`salida/`).
- Mueve a `src/` la lógica reutilizable: el código de los módulos se revisa y se prueba mejor que el de los notebooks.
- Evita celdas gigantes: los conflictos son más fáciles de resolver en celdas pequeñas.
