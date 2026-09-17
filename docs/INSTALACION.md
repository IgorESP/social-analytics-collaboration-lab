# Guía de instalación

Esta guía prepara el entorno de trabajo y recupera el repositorio del
laboratorio. Hay dos caminos según el papel de cada miembro de la pareja:

- **Alumno/a A** recupera el repositorio desde el fichero `.bundle` y lo publica en GitHub.
- **Alumno/a B** clona el repositorio de GitHub de la pareja.

## 1. Requisitos

| Herramienta | Versión mínima | Comprobación |
|-------------|----------------|--------------|
| Git | 2.38 | `git --version` |
| uv | 0.5 | `uv --version` |
| Cuenta de GitHub | — | acceso a <https://github.com> |
| Editor | VS Code (recomendado) o JupyterLab | — |

No hace falta instalar Python a mano: **uv descarga la versión indicada en
`.python-version` (3.12)** si no la encuentra en el equipo.

Instalar uv:

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Configuración de Git (una vez por equipo)

```bash
git config --global user.name "Nombre Apellido"
git config --global user.email "tu-correo@ejemplo.com"   # el mismo correo que en GitHub
git config --global init.defaultBranch main
git config --global pull.rebase false        # git pull hace merge (comportamiento explícito)
git config --global core.editor "code --wait"  # opcional: VS Code como editor de Git
```

> **Finales de línea:** el repositorio incluye un `.gitattributes` que fuerza
> LF. No necesitas cambiar `core.autocrlf`; los conflictos se verán igual en
> Windows, Linux y macOS.

## 2. Dónde guardar el repositorio

Usa una ruta **corta y fuera de carpetas sincronizadas** (OneDrive, Google
Drive, Dropbox). Por ejemplo `C:\dev\` en Windows o `~/dev/` en Linux/macOS.

- OneDrive bloquea ficheros de `.git` mientras sincroniza y puede corromper el repositorio.
- Windows limita las rutas a 260 caracteres y el entorno `.venv` tiene rutas profundas.

## 3. Alumno/a A: recuperar el repositorio desde el bundle

El profesorado os entrega `social-analytics-collaboration-lab.bundle`. Un
*bundle* es un repositorio Git completo empaquetado en un fichero: contiene
todas las ramas, las etiquetas y el historial.

```bash
cd ~/dev                                   # o C:\dev
git bundle list-heads ruta/al/social-analytics-collaboration-lab.bundle   # 59 referencias (ramas y etiquetas)
git clone ruta/al/social-analytics-collaboration-lab.bundle social-analytics-collaboration-lab
cd social-analytics-collaboration-lab
git bundle verify ruta/al/social-analytics-collaboration-lab.bundle       # "... is okay"
```

`git bundle verify` solo funciona dentro de un repositorio. Por eso se
ejecuta después de clonar. Si al clonar aparece el aviso
`hint: Using 'master' as the name for the initial branch`, ignóralo: la rama
que se obtiene es `main` (o configura `init.defaultBranch main`, apartado 1).
Para comprobar que el fichero no se ha dañado en la descarga, compara su suma
SHA-256 con la de `SHA256SUMS.txt`: `sha256sum` en Linux/macOS,
`Get-FileHash` en PowerShell.

`git clone` solo crea la rama local `main`; las demás quedan como
`origin/...`. Para crear **todas las ramas locales** de una vez:

```bash
git fetch origin "+refs/heads/*:refs/heads/*" --update-head-ok
git branch --list | wc -l                  # deben aparecer 25 ramas (en PowerShell: (git branch).Count)
git tag --list | wc -l                     # 33 etiquetas: v1.0.0 y lab/<id>/...
```

El remoto `origin` apunta todavía al fichero bundle. Cámbiale el nombre para
dejar `origin` libre para GitHub:

```bash
git remote rename origin bundle
```

Continúa en [TRABAJO_COLABORATIVO.md](TRABAJO_COLABORATIVO.md#1-publicar-el-repositorio-en-github-alumnoa-a)
para publicarlo en GitHub.

## 4. Alumno/a B: clonar el repositorio de la pareja

Cuando A haya publicado el repositorio y aceptes su invitación:

```bash
cd ~/dev
git clone https://github.com/<usuario-de-A>/social-analytics-collaboration-lab.git
cd social-analytics-collaboration-lab
git branch -r | wc -l          # todas las ramas aparecen como origin/...
git switch ejercicio/g01-alumno-b   # crea la rama local con seguimiento de origin
```

No hace falta crear todas las ramas locales: `git switch <rama>` las crea
según las vas necesitando.

## 5. Crear el entorno con uv (A y B)

```bash
uv sync                      # crea .venv con Python 3.12 y las dependencias exactas de uv.lock
uv run pytest                # en main deben pasar todos los tests (unos 40 s)
uv run social-analytics resumen
uv run python scripts/lab.py entorno
```

- `uv sync` instala también el grupo `dev` (pytest, nbstripout, nbdime, ipykernel).
- Para JupyterLab: `uv sync --group lab` y después `uv run jupyter lab`.
- En VS Code, selecciona el intérprete `.venv` del proyecto como kernel de los notebooks.
- Usa siempre `uv run ...`. Así se ejecuta con el entorno del proyecto sin activarlo.

Si cambias a una rama cuyo `uv.lock` es distinto (escenario G04), `uv run`
sincroniza el entorno automáticamente antes de ejecutar.

## 6. Problemas frecuentes del entorno

Estos problemas **no forman parte de los ejercicios**: son de configuración.

| Síntoma | Causa | Solución |
|---------|-------|----------|
| `failed to hardlink file ... (os error 396)` al hacer `uv sync` | Caché de uv y proyecto en sistemas de ficheros incompatibles (OneDrive) | `set UV_LINK_MODE=copy` (cmd), `$env:UV_LINK_MODE="copy"` (PowerShell) o `export UV_LINK_MODE=copy` |
| `Espacio en disco insuficiente` / `No space left on device` | Disco lleno | Libera espacio; `uv cache prune` elimina la caché que no se usa |
| `Filename too long` al clonar o en `.venv` | Ruta demasiado larga en Windows | Mueve el repositorio a `C:\dev\`; opcional: `git config --global core.longpaths true` |
| `Permission denied` / `unable to unlink` en `.git` | OneDrive o un antivirus bloquean ficheros | Trabaja fuera de OneDrive |
| `uv: command not found` tras instalar | El terminal no ha recargado el `PATH` | Abre un terminal nuevo |
| `git-nbmergedriver: command not found` | nbdime configurado con `nbdime config-git` fuera del entorno | Usa `uv run python scripts/lab.py notebooks activar-nbdime` (ver [NOTEBOOKS.md](NOTEBOOKS.md)) |
| `Author identity unknown` | Falta `user.name` / `user.email` | Ver la configuración de Git del apartado 1 |
| Muchas ramas no aparecen tras clonar el bundle | Solo se crea `main` al clonar | `git fetch origin "+refs/heads/*:refs/heads/*" --update-head-ok` |
| `RuntimeWarning: Proactor event loop` al ejecutar notebooks en Windows | Aviso de pyzmq | Inofensivo; pytest lo filtra |
