"""Interfaz de línea de comandos: ``uv run social-analytics --help``."""

import argparse
from pathlib import Path

from social_analytics.data_loader import load_dataset
from social_analytics.reports import save_report
from social_analytics.visualization import plot_interactions_by_kind, plot_users_by_country


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="social-analytics", description="Análisis de la red social ficticia.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("resumen", help="muestra los totales del conjunto de datos")
    report = commands.add_parser("informe", help="genera el informe en Markdown")
    report.add_argument("--salida", type=Path, default=Path("salida/informe.md"))
    plots = commands.add_parser("graficos", help="genera los gráficos en PNG")
    plots.add_argument("--carpeta", type=Path, default=Path("salida"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ds = load_dataset()
    if args.command == "resumen":
        print(f"Usuarios: {len(ds.users)} | Publicaciones: {len(ds.posts)} | Interacciones: {len(ds.interactions)}")
    elif args.command == "informe":
        print(f"Informe guardado en {save_report(ds, args.salida)}")
    elif args.command == "graficos":
        for path in (
            plot_users_by_country(ds.users, args.carpeta / "usuarios_por_pais.png"),
            plot_interactions_by_kind(ds.interactions, args.carpeta / "interacciones_por_tipo.png"),
        ):
            print(f"Gráfico guardado en {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
