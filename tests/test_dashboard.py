import json

from social_analytics.dashboard import build_dashboard


def test_build_dashboard_estructura(dataset):
    panel = build_dashboard(dataset)
    assert set(panel) == {"totales", "interacciones_por_tipo", "hashtags", "publicaciones_destacadas"}
    assert len(panel["publicaciones_destacadas"]) == 3


def test_build_dashboard_es_serializable(dataset):
    assert json.loads(json.dumps(build_dashboard(dataset)))["totales"]["usuarios"] == 40
