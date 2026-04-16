"""Tests for config."""

import os
import tempfile
from contextlib import contextmanager
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

    assert config.dashboard_v1_base_url == "https://example.sensorsdata.cn/api/v3/analytics/v1"
    assert config.model_v1_base_url == "https://example.sensorsdata.cn/api/v3/analytics/v1"


def test_config_manager_default_path():
    """Test default config path."""
    manager = ConfigManager()
    assert Path.home() / ".sa-openapi.toml" == manager.DEFAULT_CONFIG_PATH


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


def test_client_config_from_env_all_fields():
    """Test environment overrides for every default profile field."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.toml"
        config_path.write_text("", encoding="utf-8")

        with (
            patch_env("SA_BASE_URL", "https://env.sensorsdata.cn"),
            patch_env("SA_API_KEY", "sk-env"),
            patch_env("SA_PROJECT", "env-project"),
        ):
            manager = ConfigManager(config_path=config_path)
            profile = manager.get_default_profile()

        assert profile is not None
        assert profile.base_url == "https://env.sensorsdata.cn"
        assert profile.api_key == "sk-env"
        assert profile.project == "env-project"


def test_config_manager_missing_profile_and_list_profiles():
    """Test listing profiles and handling missing profiles."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.toml"
        config_path.write_text(
            '[default]\nbase_url = "https://default.sensorsdata.cn"\n'
            '\n[prod]\nbase_url = "https://prod.sensorsdata.cn"\n',
            encoding="utf-8",
        )

        manager = ConfigManager(config_path=config_path)

        assert manager.get_profile("missing") is None
        assert set(manager.list_profiles()) == {"default", "prod"}


def test_config_manager_save_profile_and_set_default_profile():
    """Test saving a profile and promoting it to default."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "nested" / "config.toml"
        manager = ConfigManager(config_path=config_path)
        prod = ClientConfig(
            base_url="https://prod.sensorsdata.cn/",
            api_key="sk-prod",
            project="prod-project",
            timeout=15.0,
            max_retries=5,
        )

        manager.save_profile("prod", prod)

        reloaded = ConfigManager(config_path=config_path)
        saved = reloaded.get_profile("prod")
        assert saved is not None
        assert saved.base_url == "https://prod.sensorsdata.cn"
        assert saved.api_key == "sk-prod"
        assert saved.project == "prod-project"
        assert saved.timeout == 15.0
        assert saved.max_retries == 5

        manager.set_default_profile("prod")

        default_profile = manager.get_default_profile()
        assert default_profile is not None
        assert default_profile.base_url == "https://prod.sensorsdata.cn"
        assert "prod" not in manager.list_profiles()


def test_config_manager_set_default_profile_validation():
    """Test validating default profile selection."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.toml"
        manager = ConfigManager(config_path=config_path)

        with pytest.raises(ValueError, match="Default profile does not exist"):
            manager.set_default_profile("default")

        with pytest.raises(ValueError, match="Profile 'missing' not found"):
            manager.set_default_profile("missing")

        manager.save_profile(
            "default",
            ClientConfig(
                base_url="https://default.sensorsdata.cn",
                api_key="sk-default",
                project="default-project",
            ),
        )

        manager.set_default_profile("default")

        default_profile = manager.get_default_profile()
        assert default_profile is not None
        assert default_profile.project == "default-project"


@contextmanager
def patch_env(key, value):
    """Context manager to patch environment variable."""
    old = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old
