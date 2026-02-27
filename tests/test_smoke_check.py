from gallstone_showcase.paths import data_csv_path, notebook_path, project_root


def test_project_root_exists() -> None:
    assert project_root().exists()


def test_data_path_is_resolvable() -> None:
    path = data_csv_path()
    assert path.exists()
    assert path.name == "gallstone.csv"


def test_notebook_path_exists() -> None:
    assert notebook_path().exists()
