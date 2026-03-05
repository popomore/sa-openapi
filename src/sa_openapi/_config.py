"""Configuration management for sa-openapi."""

from __future__ import annotations

import os
from contextlib import suppress
from pathlib import Path
from typing import Any

try:
    import tomllib as tomli  # Python 3.11+
except ImportError:  # pragma: no cover
    import tomli  # type: ignore[no-redef]

import toml


class ClientConfig:
    """Client configuration."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        project: str,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.project = project
        self.timeout = timeout
        self.max_retries = max_retries

    @property
    def dashboard_base_url(self) -> str:
        """Dashboard/Channel/Dataset base path."""
        return f"{self.base_url}/api/v3/analytics/v1"

    @property
    def model_base_url(self) -> str:
        """Model service base path."""
        return f"{self.base_url}/api/v3/analytics/v2"


class ConfigManager:
    """Manage configuration from file and environment variables."""

    DEFAULT_CONFIG_PATH = Path.home() / ".sa-openapi.toml"

    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config: dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file and environment variables."""
        # Load from file
        if self.config_path.exists():
            with self.config_path.open("rb") as f:
                self._config = tomli.load(f)

        # Override with environment variables
        if base_url := os.environ.get("SA_BASE_URL"):
            self._config.setdefault("default", {})["base_url"] = base_url
        if api_key := os.environ.get("SA_API_KEY"):
            self._config.setdefault("default", {})["api_key"] = api_key
        if project := os.environ.get("SA_PROJECT"):
            self._config.setdefault("default", {})["project"] = project

    def get_profile(self, profile: str = "default") -> ClientConfig | None:
        """Get configuration for a specific profile."""
        section = self._config.get(profile)
        if not section:
            return None

        return ClientConfig(
            base_url=section.get("base_url", ""),
            api_key=section.get("api_key", ""),
            project=section.get("project", "default"),
            timeout=section.get("timeout", 30.0),
            max_retries=section.get("max_retries", 3),
        )

    def get_default_profile(self) -> ClientConfig | None:
        """Get default profile configuration."""
        return self.get_profile("default")

    def list_profiles(self) -> list[str]:
        """List all available profiles."""
        return list(self._config.keys())

    def save_profile(self, profile: str, config: ClientConfig) -> None:
        """Save profile configuration to file."""
        self._config[profile] = {
            "base_url": config.base_url,
            "api_key": config.api_key,
            "project": config.project,
            "timeout": config.timeout,
            "max_retries": config.max_retries,
        }
        self._save_to_file()

    def _save_to_file(self) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with self.config_path.open("w", encoding="utf-8") as f:
            toml.dump(self._config, f)
        with suppress(OSError):
            self.config_path.chmod(0o600)

    def set_default_profile(self, profile: str) -> None:
        """Set default profile."""
        if profile == "default":
            if "default" not in self._config:
                raise ValueError("Default profile does not exist")
            return

        default_section = self._config.get(profile)
        if default_section is None:
            raise ValueError(f"Profile '{profile}' not found")

        self._config["default"] = default_section
        del self._config[profile]
        self._save_to_file()

