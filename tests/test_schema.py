import pandas as pd
import pytest

from social_analytics.data_loader import DATA_DIR
from social_analytics.schema import SCHEMAS, SchemaError, validate_columns


@pytest.mark.parametrize("table", sorted(SCHEMAS))
def test_cabecera_csv_cumple_el_contrato(table):
    header = (DATA_DIR / f"{table}.csv").read_text(encoding="utf-8").splitlines()[0]
    assert header.split(",") == SCHEMAS[table]


def test_validate_columns_detecta_columnas_ausentes():
    incompleta = pd.DataFrame(columns=["post_id", "author_id", "text"])
    with pytest.raises(SchemaError, match="created_at"):
        validate_columns(incompleta, "posts")
