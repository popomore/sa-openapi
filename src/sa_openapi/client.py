"""Synchronous client — wraps AsyncSensorsAnalyticsClient via a background event loop."""

from __future__ import annotations

import asyncio
import threading
from contextlib import suppress
from typing import Any

from typing_extensions import Self

from ._config import ClientConfig, ConfigManager
from .async_client import AsyncSensorsAnalyticsClient


class _SyncServiceProxy:
    """Proxy that exposes async service methods as blocking sync calls."""

    def __init__(self, async_service: Any, run_sync: Any) -> None:
        self._service = async_service
        self._run_sync = run_sync

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._service, name)
        if asyncio.iscoroutinefunction(attr):

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return self._run_sync(attr(*args, **kwargs))

            wrapper.__name__ = name
            wrapper.__doc__ = attr.__doc__
            return wrapper
        return attr


class SensorsAnalyticsClient:
    """Synchronous client for Sensors Analytics API.

    Internally runs an :class:`AsyncSensorsAnalyticsClient` on a dedicated
    background thread so that a single aiohttp session is reused across calls.

    Usage::

        with SensorsAnalyticsClient(
            base_url="https://...",
            api_key="sk-xxx",
            project="default",
        ) as client:
            navs = client.dashboard.list_navigation()
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        project: str = "default",
        *,
        timeout: float = 30.0,
        max_retries: int = 3,
        sync_timeout: float = 30.0,
    ):
        self._closed = False
        self._sync_timeout = sync_timeout
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._loop.run_forever, daemon=True, name="sa-openapi-eventloop"
        )
        self._thread.start()

        self._async_client = AsyncSensorsAnalyticsClient(
            base_url=base_url,
            api_key=api_key,
            project=project,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.dashboard = _SyncServiceProxy(self._async_client.dashboard, self._run_sync)
        self.channel = _SyncServiceProxy(self._async_client.channel, self._run_sync)
        self.dataset = _SyncServiceProxy(self._async_client.dataset, self._run_sync)
        self.event_meta = _SyncServiceProxy(self._async_client.event_meta, self._run_sync)
        self.property_meta = _SyncServiceProxy(self._async_client.property_meta, self._run_sync)
        self.smart_alarm = _SyncServiceProxy(self._async_client.smart_alarm, self._run_sync)
        self.model = _SyncServiceProxy(self._async_client.model, self._run_sync)

    def _run_sync(self, coro: Any, timeout: float | None = None) -> Any:
        """Submit *coro* to the background event loop and block until done."""
        if self._closed:
            raise RuntimeError("Client is closed")
        fut = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return fut.result(timeout=self._sync_timeout if timeout is None else timeout)

    def close(self) -> None:
        """Close the aiohttp session and stop the background event loop."""
        if self._closed:
            return
        try:
            self._run_sync(self._async_client.aclose())
        finally:
            with suppress(RuntimeError):
                self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join(timeout=5)
            if not self._loop.is_closed():
                self._loop.close()
            self._closed = True

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    @classmethod
    def from_config(cls, config: ClientConfig) -> Self:
        """Create client from ClientConfig."""
        return cls(
            base_url=config.base_url,
            api_key=config.api_key,
            project=config.project,
            timeout=config.timeout,
            max_retries=config.max_retries,
            sync_timeout=max(config.timeout * 2, 30.0),
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
