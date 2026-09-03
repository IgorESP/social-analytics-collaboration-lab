import pytest

from social_analytics.data_loader import VALID_INTERACTIONS, load_csv, load_dataset


def test_load_dataset_conteos(dataset):
    assert len(dataset.users) == 40
    assert len(dataset.posts) == 119
    assert len(dataset.interactions) == 637


def test_clean_users_normaliza_nombres_y_paises(dataset):
    users = dataset.users
    assert users["user_id"].is_unique
    assert (users["username"] == users["username"].str.strip()).all()
    assert users["country"].str.fullmatch(r"[A-Z]{2}|DESCONOCIDO").all()


def test_clean_posts_descarta_vacias_y_duplicadas(dataset):
    posts = dataset.posts
    assert posts["post_id"].is_unique
    assert (posts["text"].str.len() > 0).all()
    assert "   " not in " ".join(posts["text"])


def test_clean_interactions_solo_tipos_validos(dataset):
    assert set(dataset.interactions["kind"]) <= set(VALID_INTERACTIONS)


def test_load_csv_fichero_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError, match="No se encuentra"):
        load_csv(tmp_path / "no_existe.csv")

