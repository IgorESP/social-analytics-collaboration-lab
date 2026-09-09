from social_analytics.reports import build_sections, generate_report, save_report


def test_build_sections_orden(dataset):
    titles = [title for title, _ in build_sections(dataset)]
    assert titles == ["Resumen", "Usuarios más activos", "Publicaciones destacadas"]


def test_generate_report_es_markdown(dataset):
    report = generate_report(dataset)
    assert report.startswith("# Informe de actividad de la red social")
    assert "## Resumen" in report
    assert f"- Usuarios: {len(dataset.users)}" in report


def test_save_report_crea_la_carpeta(dataset, tmp_path):
    path = save_report(dataset, tmp_path / "salida" / "informe.md")
    assert path.exists()
    assert path.read_text(encoding="utf-8").startswith("# Informe")
