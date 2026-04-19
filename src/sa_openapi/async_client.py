"""Async client for sa-openapi."""

from __future__ import annotations

from typing import Any

from typing_extensions import Self

from ._auth import AuthHandler
from ._config import ClientConfig, ConfigManager
from ._transport import AiohttpTransport
from .services import (
    ChannelServiceV1,
    DashboardServiceV1,
    DatasetServiceV1,
    EventMetaServiceV1,
    ModelServiceV1,
    PropertyMetaServiceV1,
    SmartAlarmServiceV1,
)


class AsyncSensorsAnalyticsClient:
    """Primary async client for Sensors Analytics API.

    All service methods are coroutines and must be awaited.

    Usage::

        async with AsyncSensorsAnalyticsClient(
            base_url="https://...",
            api_key="sk-xxx",
            project="default",
        ) as client:
            navs = await client.dashboard.list_navigation()
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        project: str = "default",
        *,
        timeout: float = 30.0,
        max_retries: int = 3,
        version: str = "v1",
    ):
        self.config = ClientConfig(
            base_url=base_url,
            api_key=api_key,
            project=project,
            timeout=timeout,
            max_retries=max_retries,
            version=version,
        )
        self._auth = AuthHandler(api_key, project)
        self._transport = AiohttpTransport(self.config, self._auth)

        self.dashboard = DashboardServiceV1(self._transport, self._auth)
        self.channel = ChannelServiceV1(self._transport, self._auth)
        self.dataset = DatasetServiceV1(self._transport, self._auth)
        self.model = ModelServiceV1(self._transport, self._auth)
        self.event_meta = EventMetaServiceV1(self._transport, self._auth)
        self.property_meta = PropertyMetaServiceV1(self._transport, self._auth)
        self.smart_alarm = SmartAlarmServiceV1(self._transport, self._auth)

    async def aclose(self) -> None:
        """Close the underlying aiohttp session."""
        await self._transport.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    @classmethod
    def from_config(cls, config: ClientConfig) -> Self:
        """Create client from ClientConfig."""
        return cls(
            base_url=config.base_url,
            api_key=config.api_key,
            project=config.project,
            timeout=config.timeout,
            max_retries=config.max_retries,
            version=config.version,
        )

    @classmethod
    def from_profile(cls, profile: str = "default") -> Self:
        """Create client from a named config profile.

        Raises:
            ValueError: If profile not found
        """
        manager = ConfigManager()
        config = manager.get_profile(profile)
        if not config:
            raise ValueError(f"Profile '{profile}' not found")
        return cls.from_config(config)
