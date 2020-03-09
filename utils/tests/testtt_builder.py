import pytest

from package.builder import EXCLUDE_FILES, EXCLUDE_MODULES, ROOT_DIR, exclude


@pytest.mark.parametrize(
    "filename",
    [
        "test.py",
        "other.txt",
        "thing.md",
        "folder_name",
        "airflow.cfg",
        "airflow.file",
    ],
)
def test_exclude_returns_false(monkeypatch, filename):
    monkeypatch.setattr(
        "package.builder.Path.is_dir", lambda x: "." not in x.name
    )
    assert not exclude(filename)


@pytest.mark.parametrize(
    "filename",
    [".git", "__pycache__", ".pytest_cache", ".idea", "tests", "theirflow"],
)
def test_exclude_returns_true_for_directories(monkeypatch, filename):
    monkeypatch.setattr("package.builder.Path.is_dir", lambda x: True)
    assert exclude(filename)


@pytest.mark.parametrize("filepath", EXCLUDE_FILES)
def test_exclude_returns_true_for_files(monkeypatch, filepath):
    monkeypatch.setattr("package.builder.Path.is_dir", lambda x: False)
    assert exclude(filepath)


@pytest.mark.parametrize("filename", EXCLUDE_MODULES)
def test_exclude_returns_true_for_modules(monkeypatch, filename):
    monkeypatch.setattr(
        "package.builder.Path.is_dir", lambda x: filename in EXCLUDE_MODULES
    )
    assert exclude(filename)


@pytest.mark.parametrize(
    "filepath,excluded",
    [
        (".env", True),
        ("theirflow_template/env.activate", False),
        ("theirflow_template/env.deactivate", False),
        ("docker_deployment/.env", True),
        ("docker_deployment/template.env", False),
    ],
)
def test_exclude_for_env_files(monkeypatch, filepath, excluded):
    monkeypatch.setattr("package.builder.Path.is_dir", lambda x: False)
    filepath = ROOT_DIR / filepath
    assert exclude(filepath) is excluded
