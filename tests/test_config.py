"""Tests for config."""

import os
import tempfile
from pathlib import Path

import pytest

from sa_openapi._config import ClientConfig, ConfigManager


def test_client_config():
    """Test client configuration."""
    config = ClientConfig(
        base_url="https://example.sensorsdata.cn",
        api_key="sk-test",
        project="default",
    )

    assert config.base_url == "https://example.sensorsdata.cn"
    assert config.api_key == "sk-test"
    assert config.project == "default"
    assert config.timeout == 30.0
    assert config.max_retries == 3


def test_client_config_base_urls():
    """Test base URL properties."""
    config = ClientConfig(
        base_url="https://example.sensorsdata.cn",
        api_key="sk-test",
        project="default",
    )

    assert config.dashboard_base_url == "https://example.sensorsdata.cn/api/v3/analytics/v1"
    assert config.model_base_url == "https://example.sensorsdata.cn/api/v3/analytics/v2"


def test_config_manager_default_path():
    """Test default config path."""
    manager = ConfigManager()
    assert manager.DEFAULT_CONFIG_PATH == Path.home() / ".sa-openapi.toml"


def test_config_manager_with_custom_path():
    """Test custom config path."""
    with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
        manager = ConfigManager(config_path=Path(f.name))
        assert manager.config_path == Path(f.name)


def test_client_config_from_env():
    """Test environment variable overrides."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.toml"

        # Create config file
        config_path.write_text('[default]\nbase_url = "https://file.sensorsdata.cn"\n')

        # Set env vars
        with patch_env("SA_BASE_URL", "https://env.sensorsdata.cn"):
            manager = ConfigManager(config_path=config_path)
            # Env should override file
            assert manager.get_default_profile().base_url == "https://env.sensorsdata.cn"


def patch_env(key, value):
    """Context manager to patch environment variable."""
    old = os.environ.get(key)
    os.environ[key] = value
    yield
    if old is None:
        del os.environ[key]
    else:
        os.environ[key] = old
