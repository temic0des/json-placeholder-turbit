from pydantic_core import ValidationError
import os, pytest

from app.utils.settings import Settings

def test_settings_loaded_from_env():
    os.environ["MONGO_INITDB_ROOT_USERNAME"] = "test_username"
    os.environ["MONGO_INITDB_ROOT_PASSWORD"] = "test_password"
    os.environ["MONGO_INITDB_ROOT_HOST"] = "localhost"
    os.environ["MONGO_INITDB_ROOT_PORT"] = "37017"
    os.environ["MONGO_INITDB_ROOT_DBNAME"] = "test_database"

    settings = Settings()

    mongo_uri = f"mongodb://{settings.mongo_initdb_root_username}:{settings.mongo_initdb_root_password}@{settings.mongo_initdb_root_host}:{settings.mongo_initdb_root_port}"

    assert settings.mongo_initdb_root_username == "test_username"
    assert settings.mongo_initdb_root_password == "test_password"
    assert settings.mongo_initdb_root_port == 37017
    assert settings.mongo_initdb_root_dbname == "test_database"
    assert settings.mongo_initdb_root_host == "localhost"
    assert str(settings.mongo_url) == mongo_uri

def test_settings_from_env_file(monkeypatch):

    monkeypatch.setenv("MONGO_INITDB_ROOT_USERNAME", "monkey_patch_test_username")
    monkeypatch.setenv("MONGO_INITDB_ROOT_PASSWORD", "monkey_patch_test_password")
    monkeypatch.setenv("MONGO_INITDB_ROOT_PORT", "37017")
    monkeypatch.setenv("MONGO_INITDB_ROOT_DBNAME", "monkey_patch_test_database")
    monkeypatch.setenv("MONGO_INITDB_ROOT_HOST", "monkey_patch_test_localhost")

    settings = Settings()

    mongo_uri = f"mongodb://{settings.mongo_initdb_root_username}:{settings.mongo_initdb_root_password}@{settings.mongo_initdb_root_host}:{settings.mongo_initdb_root_port}"

    assert settings.mongo_initdb_root_username == "monkey_patch_test_username"
    assert settings.mongo_initdb_root_password == "monkey_patch_test_password"
    assert settings.mongo_initdb_root_port == 37017
    assert settings.mongo_initdb_root_dbname == "monkey_patch_test_database"
    assert settings.mongo_initdb_root_host == "monkey_patch_test_localhost"
    assert str(settings.mongo_url) == mongo_uri

    assert settings.mongo_url.hosts()[0]['username'] == "monkey_patch_test_username"

def test_settings_without_values(monkeypatch):

    monkeypatch.setenv("MONGO_INITDB_ROOT_USERNAME", "")
    monkeypatch.setenv("MONGO_INITDB_ROOT_PASSWORD", "")
    monkeypatch.setenv("MONGO_INITDB_ROOT_PORT", "")
    monkeypatch.setenv("MONGO_INITDB_ROOT_DBNAME", "")
    monkeypatch.setenv("MONGO_INITDB_ROOT_HOST", "")

    with pytest.raises(ValidationError):
        Settings()