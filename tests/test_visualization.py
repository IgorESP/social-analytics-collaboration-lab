from social_analytics.visualization import plot_interactions_by_kind, plot_users_by_country

PNG_SIGNATURE = b"\x89PNG"


def test_plot_users_by_country_genera_png(mini_dataset, tmp_path):
    path = plot_users_by_country(mini_dataset.users, tmp_path / "graficos" / "paises.png")
    assert path.read_bytes().startswith(PNG_SIGNATURE)


def test_plot_interactions_by_kind_genera_png(mini_dataset, tmp_path):
    path = plot_interactions_by_kind(mini_dataset.interactions, tmp_path / "tipos.png")
    assert path.read_bytes().startswith(PNG_SIGNATURE)
