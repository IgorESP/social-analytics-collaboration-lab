from social_analytics.cli import main


def test_cli_resumen(capsys):
    assert main(["resumen"]) == 0
    assert "Usuarios: 40" in capsys.readouterr().out


def test_cli_informe(tmp_path):
    salida = tmp_path / "informe.md"
    assert main(["informe", "--salida", str(salida)]) == 0
    assert salida.read_text(encoding="utf-8").startswith("# Informe")


def test_cli_graficos(tmp_path):
    assert main(["graficos", "--carpeta", str(tmp_path)]) == 0
    assert sorted(p.name for p in tmp_path.glob("*.png")) == ["interacciones_por_tipo.png", "usuarios_por_pais.png"]


def test_cli_dashboard(capsys):
    assert main(["dashboard"]) == 0
    assert '"totales"' in capsys.readouterr().out
