"""Base client for sa-openapi."""

from __future__ import annotations

from typing import Any

from typing_extensions import Self

from ._auth import AuthHandler
from ._config import ClientConfig, ConfigManager
from ._transport import Transport
from .services import ChannelService, DashboardService, DatasetService, ModelService


class BaseClient:
    """Base client for Sensors Analytics API."""

    def __init__(self, config: ClientConfig):
        self.config = config
        self._transport = Transport(config, AuthHandler(config.api_key, config.project))
        self._auth = AuthHandler(config.api_key, config.project)

        # Initialize services
        self.dashboard = DashboardService(self._transport, self._auth)
        self.channel = ChannelService(self._transport, self._auth)
        self.dataset = DatasetService(self._transport, self._auth)
        self.model = ModelService(self._transport, self._auth)

    def close(self) -> None:
        """Close the client and release resources."""
        self._transport.close()

    @property
    def is_closed(self) -> bool:
        """Check if client is closed."""
        return self._transport._client.is_closed


class SensorsAnalyticsClient(BaseClient):
    """Synchronous client for Sensors Analytics API."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        project: str = "default",
        *,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        config = ClientConfig(
            base_url=base_url,
            api_key=api_key,
            project=project,
            timeout=timeout,
            max_retries=max_retries,
        )
        super().__init__(config)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    @classmethod
    def from_config(cls, config: ClientConfig) -> Self:
        """Create client from config.

        Args:
            config: Client configuration

        Returns:
            Client instance
        """
        return cls(
            base_url=config.base_url,
            api_key=config.api_key,
            project=config.project,
            timeout=config.timeout,
            max_retries=config.max_retries,
        )

    @classmethod
    def from_profile(cls, profile: str = "default") -> Self:
        """Create client from config profile.

        Args:
            profile: Profile name

        Returns:
            Client instance

        Raises:
            ValueError: If profile not found
        """
        manager = ConfigManager()
        config = manager.get_profile(profile)
        if not config:
            raise ValueError(f"Profile '{profile}' not found")
        return cls.from_config(config)
