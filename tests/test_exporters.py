import pandas as pd

from social_analytics.exporters import export_to_excel


def test_export_to_excel_crea_tres_hojas(mini_dataset, tmp_path):
    path = export_to_excel(mini_dataset, tmp_path / "datos.xlsx")
    sheets = pd.read_excel(path, sheet_name=None)
    assert list(sheets) == ["usuarios", "publicaciones", "interacciones"]
    assert len(sheets["usuarios"]) == 3
