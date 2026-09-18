"""Herramienta de apoyo del laboratorio de Git colaborativo.

Ejecútala siempre desde la raíz del repositorio:

    uv run python scripts/lab.py entorno            # comprueba la instalación
    uv run python scripts/lab.py escenarios         # estado de los 8 casos
    uv run python scripts/lab.py info g01           # punto de partida de un escenario
    uv run python scripts/lab.py restaurar g01      # vuelve al estado inicial (con copia de seguridad)
    uv run python scripts/lab.py revisar integracion/g01 ejercicio/g01-alumno-a
    uv run python scripts/lab.py notebooks estado   # nbstripout y nbdime en este repositorio
    uv run python scripts/lab.py notebooks activar-nbdime
    uv run python scripts/lab.py notebooks activar-nbstripout

Solo usa la biblioteca estándar de Python y comandos de Git. Ninguna orden
modifica GitHub salvo ``restaurar --publicar``, que lo indica antes de hacerlo.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = {"a": "ejercicio/{id}-alumno-a", "b": "ejercicio/{id}-alumno-b", "integracion": "integracion/{id}"}
BASE = "lab/{id}/base"  # punto de partida de cada caso (etiqueta, no rama)
OK, FAIL, WARN = "[ OK ]", "[FALLO]", "[AVISO]"


# --------------------------------------------------------------------------- utilidades


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if check and result.returncode != 0:
        raise SystemExit(f"Error al ejecutar: git {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout.strip()


def rev(ref: str) -> str | None:
    out = subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref + "^{commit}"], cwd=ROOT, capture_output=True, text=True)
    return out.stdout.strip() or None


def scenario_ids() -> list[str]:
    tags = git("tag", "--list", "lab/*/base").splitlines()
    return sorted(tag.split("/")[1] for tag in tags)


def branch_name(scenario: str, role: str) -> str:
    return ROLES[role].format(id=scenario)


def normalize_id(raw: str) -> str:
    scenario = raw.lower().strip()
    if scenario not in scenario_ids():
        raise SystemExit(f"Escenario desconocido: {raw}. Disponibles: {', '.join(scenario_ids())}")
    return scenario


def operation_in_progress() -> str | None:
    git_dir = Path(git("rev-parse", "--absolute-git-dir"))
    for marker, name in (("MERGE_HEAD", "merge"), ("rebase-merge", "rebase"), ("rebase-apply", "rebase"), ("CHERRY_PICK_HEAD", "cherry-pick"), ("REVERT_HEAD", "revert")):
        if (git_dir / marker).exists():
            return name
    return None


def run_tool(*cmd: str) -> str | None:
    if shutil.which(cmd[0]) is None:
        return None
    result = subprocess.run(cmd, capture_output=True, text=True)
    return (result.stdout or result.stderr).strip().splitlines()[0] if result.returncode == 0 else None


# --------------------------------------------------------------------------- entorno


def cmd_entorno(_: argparse.Namespace) -> int:
    problems = 0

    def report(ok: bool, message: str, hint: str = "", warning: bool = False) -> None:
        nonlocal problems
        if ok:
            print(f"{OK} {message}")
        else:
            print(f"{WARN if warning else FAIL} {message}" + (f"\n        -> {hint}" if hint else ""))
            problems += 0 if warning else 1

    git_version = run_tool("git", "--version") or ""
    match = re.search(r"(\d+)\.(\d+)", git_version)
    report(bool(match) and (int(match[1]), int(match[2])) >= (2, 38), f"Git: {git_version or 'no encontrado'}", "Instala Git 2.38 o superior")
    report(run_tool("uv", "--version") is not None, f"uv: {run_tool('uv', '--version') or 'no encontrado'}", "https://docs.astral.sh/uv/getting-started/installation/")
    report(sys.version_info >= (3, 11), f"Python: {sys.version.split()[0]} ({sys.executable})", "Ejecuta el script con 'uv run python scripts/lab.py ...'")
    in_venv = Path(sys.prefix).resolve() == (ROOT / ".venv").resolve()
    report(in_venv, "Python del entorno del proyecto (.venv)", "Usa 'uv run python scripts/lab.py ...'", warning=True)

    for module in ("pandas", "matplotlib", "pytest", "nbformat", "nbclient", "nbstripout", "nbdime"):
        try:
            __import__(module)
            report(True, f"Paquete {module} disponible")
        except ImportError:
            report(False, f"Paquete {module} no disponible", "Ejecuta 'uv sync'")

    name, email = git("config", "user.name", check=False), git("config", "user.email", check=False)
    report(bool(name and email), f"Identidad de Git: {name or '?'} <{email or '?'}>", 'git config --global user.name "Nombre Apellido"; git config --global user.email "correo@ejemplo.com"')
    autocrlf = git("config", "core.autocrlf", check=False) or "(sin definir)"
    report(True, f"core.autocrlf = {autocrlf} (el repositorio fuerza LF con .gitattributes)")

    missing = [s for s in scenario_ids() for role in ROLES if rev(branch_name(s, role)) is None]
    report(len(scenario_ids()) == 8, f"Casos encontrados: {len(scenario_ids())} de 8", "¿Has recuperado las etiquetas? git fetch origin --tags")
    report(not missing, "Todas las ramas locales de los escenarios existen" if not missing else f"Faltan {len(missing)} ramas locales (p. ej. {missing[0]})", "Consulta docs/TRABAJO_COLABORATIVO.md, apartado 'Recuperar todas las ramas'")
    remote = git("remote", "get-url", "origin", check=False)
    report(bool(remote), f"Remoto origin: {remote or 'no configurado'}", "Normal antes de publicar en GitHub", warning=True)
    print()
    print("Entorno correcto." if problems == 0 else f"Hay {problems} problema(s) que conviene resolver antes de empezar.")
    return 0 if problems == 0 else 1


# --------------------------------------------------------------------------- escenarios


def state_of(scenario: str, role: str) -> str:
    current, original = rev(branch_name(scenario, role)), rev(f"lab/{scenario}/{role}")
    if current is None:
        return "no existe"
    if current == original:
        return "original"
    if original and subprocess.run(["git", "merge-base", "--is-ancestor", original, current], cwd=ROOT).returncode == 0:
        return "avanzada"
    return "reescrita"


def cmd_escenarios(_: argparse.Namespace) -> int:
    print(f"{'ID':<5} {'alumno-a':<10} {'alumno-b':<10} {'integracion':<12} {'en origin':<9}")
    remote_branches = set(git("branch", "-r", "--format=%(refname:short)", check=False).splitlines())
    for scenario in scenario_ids():
        published = all(f"origin/{branch_name(scenario, role)}" in remote_branches for role in ROLES)
        states = [state_of(scenario, role) for role in ROLES]
        print(f"{scenario:<5} {states[0]:<10} {states[1]:<10} {states[2]:<12} {'sí' if published else 'no':<9}")
    print("\noriginal = igual que al empezar | avanzada = con commits nuevos | reescrita = historial distinto")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    scenario = normalize_id(args.escenario)
    base = BASE.format(id=scenario)
    a, b, integ = (branch_name(scenario, role) for role in ROLES)
    print(f"Escenario {scenario.upper()}\n")
    print(git("show", "--no-patch", "--format=Punto de partida (" + base + "): %h %s (%an, %ad)", "--date=short", base + "^{commit}"))
    for role, branch in (("a", a), ("b", b)):
        mb = git("merge-base", base, branch, check=False)
        same = mb == rev(base)
        print(f"\n{branch}  [{state_of(scenario, role)}]  {'parte de la base' if same else 'NO parte de la base: revisa el historial'}")
        print(git("log", "--format=  %h %s (%an)", f"{base}..{branch}") or "  (sin commits propios)")
        print(git("diff", "--stat=100", base, branch) or "  (sin cambios)")
    print(f"\n{integ}  [{state_of(scenario, 'integracion')}]")
    print(git("log", "--format=  %h %s (%an)", f"{base}..{integ}") or "  (igual que la base)")
    print(f"\nEnunciado: git show {base}:ESCENARIO.md")
    return 0


# --------------------------------------------------------------------------- restaurar


def cmd_restaurar(args: argparse.Namespace) -> int:
    scenario = normalize_id(args.escenario)
    roles = ["a", "b", "integracion"] if args.rama == "todas" else [args.rama]
    if (op := operation_in_progress()) is not None:
        raise SystemExit(f"Hay un {op} en curso. Termínalo o cancélalo antes (git {op} --abort).")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise SystemExit("Tienes cambios sin confirmar. Haz commit o 'git stash' antes de restaurar.")

    current = git("branch", "--show-current", check=False)
    targets = {branch_name(scenario, role): f"lab/{scenario}/{role}" for role in roles}
    if current in targets:
        print(f"Cambiando a main porque {current} se va a restaurar...")
        git("switch", "main")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backups: list[str] = []
    for branch, tag in targets.items():
        current_sha, original_sha = rev(branch), rev(tag)
        if original_sha is None:
            raise SystemExit(f"No existe la etiqueta {tag}. Recupérala con: git fetch origin --tags")
        if current_sha == original_sha:
            print(f"{OK} {branch} ya está en su estado original")
            continue
        if current_sha is not None:
            backup = f"respaldo/{scenario}/{stamp}/{branch.split('/')[-1]}"
            git("branch", backup, current_sha)
            backups.append(backup)
            print(f"{OK} Copia de seguridad: {backup} -> {current_sha[:8]}")
        git("branch", "--force", branch, original_sha)
        print(f"{OK} {branch} restaurada a {tag} ({original_sha[:8]})")

    if args.publicar:
        print("\nPublicando en origin (las ramas restauradas se sobrescriben con --force-with-lease)...")
        for backup in backups:
            git("push", "origin", backup)
        for branch in targets:
            subprocess.run(["git", "push", "--force-with-lease", "origin", f"{branch}:{branch}"], cwd=ROOT, check=False)
    elif backups or targets:
        print("\nLos cambios son solo locales. Para actualizar GitHub (avisa antes a tu pareja):")
        for branch in targets:
            print(f"  git push --force-with-lease origin {branch}")
        for backup in backups:
            print(f"  git push origin {backup}      # opcional: publica la copia de seguridad")
    print("\nTus soluciones anteriores siguen disponibles en las ramas respaldo/* (git branch --list 'respaldo/*').")
    return 0


# --------------------------------------------------------------------------- revisar


CATEGORIES = [
    ("código", re.compile(r"^src/")),
    ("tests", re.compile(r"^tests/")),
    ("datos", re.compile(r"^data/")),
    ("notebooks", re.compile(r"\.ipynb$")),
    ("configuración", re.compile(r"^(pyproject\.toml|uv\.lock|\.python-version|\.git\w+)$")),
    ("documentación", re.compile(r"(^docs/|\.md$)")),
]


def category(path: str) -> str:
    return next((name for name, pattern in CATEGORIES if pattern.search(path)), "otros")


def cmd_revisar(args: argparse.Namespace) -> int:
    base, head = args.base, args.rama
    for ref in (base, head):
        if rev(ref) is None:
            raise SystemExit(f"No existe la referencia {ref}")
    merge_base = git("merge-base", base, head)
    print(f"Revisión de {head} respecto a {base} (desde {merge_base[:8]})\n")
    print("Commits:")
    print(git("log", "--format=  %h %s (%an)", f"{merge_base}..{head}") or "  (ninguno)")
    changes = [line.split("\t") for line in git("diff", "--name-status", merge_base, head).splitlines()]
    print("\nFicheros modificados por categoría:")
    for name in [c for c, _ in CATEGORIES] + ["otros"]:
        files = [f"{status} {paths[-1]}" for status, *paths in changes if category(paths[-1]) == name]
        if files:
            print(f"  {name}:")
            print("\n".join(f"    {f}" for f in files))

    warnings: list[str] = []
    diff = git("diff", "--unified=0", merge_base, head)
    current_file = ""
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
        elif line.startswith("+") and not line.startswith("+++") and current_file.startswith("src/") and re.search(r"\bprint\(", line):
            warnings.append(f"print() añadido en {current_file}: {line[1:].strip()}")
        elif line.startswith("-") and not line.startswith("---") and re.match(r"-\s*def test_", line):
            warnings.append(f"Test eliminado o renombrado en {current_file}: {line[1:].strip()}")
    for status, *paths in changes:
        path = paths[-1]
        if category(path) == "datos":
            warnings.append(f"Se modifican datos de entrada: {path}")
        if path.endswith(".ipynb") and status != "D" and '"output_type"' in git("show", f"{head}:{path}", check=False):
            warnings.append(f"Notebook con outputs guardados: {path}")
        if status == "A" and "/" not in path and category(path) in ("otros", "documentación"):
            warnings.append(f"Fichero nuevo en la raíz del proyecto: {path}")
    commits = git("log", "--format=%s", f"{merge_base}..{head}").splitlines()
    for subject in commits:
        if len(subject.split()) < 3:
            warnings.append(f"Mensaje de commit poco descriptivo: '{subject}'")

    print("\nAvisos para la revisión:" if warnings else "\nSin avisos automáticos (revisa igualmente el código).")
    for warning in warnings:
        print(f"  {WARN} {warning}")
    print("\nEsta herramienta solo ayuda: la revisión de código la haces tú (git diff, comentarios en la PR).")
    return 0


# --------------------------------------------------------------------------- notebooks


def local_attributes() -> Path:
    """Fichero de atributos local del clon (.git/info/attributes): no se versiona."""
    path = Path(git("rev-parse", "--git-path", "info/attributes"))
    return path if path.is_absolute() else ROOT / path


def add_attribute(line: str) -> None:
    path = local_attributes()
    path.parent.mkdir(parents=True, exist_ok=True)
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    if line not in content.splitlines():
        path.write_text(content + ("" if content.endswith("\n") or not content else "\n") + line + "\n", encoding="utf-8")


def remove_attribute(fragment: str) -> None:
    path = local_attributes()
    if path.exists():
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if fragment not in line]
        path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def cmd_notebooks(args: argparse.Namespace) -> int:
    python = Path(sys.executable).as_posix()
    if args.accion == "activar-nbdime":
        commands = [
            ("diff.jupyternotebook.command", f'"{python}" -m nbdime.vcs.git.diffdriver diff'),
            ("merge.jupyternotebook.driver", f'"{python}" -m nbdime.vcs.git.mergedriver merge %O %A %B %L %P'),
            ("merge.jupyternotebook.name", "jupyter notebook merge driver"),
            ("difftool.nbdime.cmd", f'"{python}" -m nbdime.vcs.git.difftool diff "$LOCAL" "$REMOTE" "$BASE"'),
            ("mergetool.nbdime.cmd", f'"{python}" -m nbdime.vcs.git.mergetool merge "$BASE" "$LOCAL" "$REMOTE" "$MERGED"'),
            ("mergetool.nbdime.trustExitCode", "true"),
        ]
        for key, value in commands:
            git("config", "--local", key, value)
            print(f"git config --local {key} '{value}'")
        add_attribute("*.ipynb diff=jupyternotebook merge=jupyternotebook")
        print(f"Atributo añadido en {local_attributes()}: *.ipynb diff=jupyternotebook merge=jupyternotebook")
        print("\nnbdime activado SOLO en este clon (no se modifica .gitattributes).")
    elif args.accion == "desactivar-nbdime":
        for section in ("diff.jupyternotebook", "merge.jupyternotebook", "difftool.nbdime", "mergetool.nbdime"):
            git("config", "--local", "--remove-section", section, check=False)
        remove_attribute("jupyternotebook")
        print("nbdime desactivado en este clon.")
    elif args.accion == "activar-nbstripout":
        result = subprocess.run([sys.executable, "-m", "nbstripout", "--install"], cwd=ROOT)
        if result.returncode != 0:
            return result.returncode
        # nbstripout --install no admite --keep-id: sin él renumera los ids de celda
        # ("0", "1", ...) y nbdime deja de emparejar bien las celdas insertadas o borradas.
        for key, value in (
            ("filter.nbstripout.clean", f'"{python}" -m nbstripout --keep-id'),
            ("diff.ipynb.textconv", f'"{python}" -m nbstripout --keep-id -t'),
        ):
            git("config", "--local", key, value)
            print(f"git config --local {key} '{value}'")
        print("nbstripout instalado como filtro en este clon (.git/config y .git/info/attributes), conservando los ids de celda.")
    elif args.accion == "desactivar-nbstripout":
        return subprocess.run([sys.executable, "-m", "nbstripout", "--uninstall"], cwd=ROOT).returncode
    print("\nConfiguración actual de notebooks en este clon:")
    for key in ("filter.nbstripout.clean", "diff.ipynb.textconv", "diff.jupyternotebook.command", "merge.jupyternotebook.driver"):
        print(f"  {key} = {git('config', '--get', key, check=False) or '(sin configurar)'}")
    attrs = git("check-attr", "filter", "diff", "merge", "--", "notebooks/01_exploracion_usuarios.ipynb", check=False)
    print("  Atributos efectivos para notebooks/*.ipynb:")
    print("\n".join(f"    {line}" for line in attrs.splitlines()))
    return 0


# --------------------------------------------------------------------------- main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lab.py", description="Herramienta de apoyo del laboratorio de Git colaborativo")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("entorno", help="comprueba Git, uv, Python y las ramas del laboratorio").set_defaults(func=cmd_entorno)
    commands.add_parser("escenarios", help="estado de las ramas de cada escenario").set_defaults(func=cmd_escenarios)
    info = commands.add_parser("info", help="punto de partida y commits de un escenario")
    info.add_argument("escenario", help="identificador, por ejemplo g01 o j03")
    info.set_defaults(func=cmd_info)
    restore = commands.add_parser("restaurar", help="devuelve las ramas de un escenario a su estado inicial")
    restore.add_argument("escenario")
    restore.add_argument("--rama", choices=["a", "b", "integracion", "todas"], default="todas")
    restore.add_argument("--publicar", action="store_true", help="actualiza también origin con --force-with-lease")
    restore.set_defaults(func=cmd_restaurar)
    review = commands.add_parser("revisar", help="ayuda para revisar una pull request")
    review.add_argument("base", help="rama de destino de la PR")
    review.add_argument("rama", help="rama de la PR")
    review.set_defaults(func=cmd_revisar)
    notebooks = commands.add_parser("notebooks", help="configuración local de nbstripout y nbdime")
    notebooks.add_argument(
        "accion",
        choices=["estado", "activar-nbdime", "desactivar-nbdime", "activar-nbstripout", "desactivar-nbstripout"],
        nargs="?",
        default="estado",
    )
    notebooks.set_defaults(func=cmd_notebooks)
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
