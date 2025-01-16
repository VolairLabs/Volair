import os
from volairframework.storage.configuration import ConfigManager


def test_initialize(monkeypatch):
    # Mock environment variable
    monkeypatch.setenv("TEST_KEY", "test_value")
    config = ConfigManager(db_name="test_config.db")
    config.initialize("TEST_KEY")
    assert config.get("TEST_KEY") == "test_value"


def test_set_and_get():
    config = ConfigManager(db_name="test_config.db")
    config.set("key1", "value1")
    assert config.get("key1") == "value1"


def test_get_with_default():
    config = ConfigManager(db_name="test_config.db")
    assert config.get("non_existent_key", "default_value") == "default_value"


def teardown_module(module):
    # Clean up the test database file
    if os.path.exists("test_config.db"):
        os.remove("test_config.db")
