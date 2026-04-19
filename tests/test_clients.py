"""Tests for async and sync clients."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import sa_openapi.client as client_module
from sa_openapi._config import ClientConfig
from sa_openapi.async_client import AsyncSensorsAnalyticsClient
from sa_openapi.client import SensorsAnalyticsClient, _SyncServiceProxy


class DummyAsyncService:
    """Small async service used for sync proxy tests."""

    def __init__(self, name: str):
        self.label = name

    async def ping(self, value: str) -> str:
        return f"{self.label}:{value}"


class FakeAsyncClient:
    """Fake async client used to isolate sync wrapper tests."""

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
        self.init_args = {
            "base_url": base_url,
            "api_key": api_key,
            "project": project,
            "timeout": timeout,
            "max_retries": max_retries,
        }
        self.dashboard = DummyAsyncService("dashboard")
        self.channel = DummyAsyncService("channel")
        self.dataset = DummyAsyncService("dataset")
        self.event_meta = DummyAsyncService("event_meta")
        self.property_meta = DummyAsyncService("property_meta")
        self.smart_alarm = DummyAsyncService("smart_alarm")
        self.model = DummyAsyncService("model")
        self.aclose = AsyncMock()


@pytest.mark.asyncio
async def test_async_client_initializes_services_and_delegates_close():
    """Test async client service wiring and close delegation."""
    client = AsyncSensorsAnalyticsClient(
        base_url="https://example.sensorsdata.cn",
        api_key="sk-test",
        project="analytics",
        timeout=12.0,
        max_retries=4,
    )
    client._transport.close = AsyncMock()

    assert client.config.base_url == "https://example.sensorsdata.cn"
    assert client.config.project == "analytics"
    assert client.dashboard._transport is client._transport
    assert client.model._transport is client._transport

    await client.aclose()

    client._transport.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_async_client_context_manager_uses_aclose():
    """Test async context management."""
    client = AsyncSensorsAnalyticsClient(
        base_url="https://example.sensorsdata.cn",
        api_key="sk-test",
    )
    client.aclose = AsyncMock()

    async with client as active:
        assert active is client

    client.aclose.assert_awaited_once()


def test_async_client_factories(monkeypatch):
    """Test async client factories from config and profile."""
    config = ClientConfig(
        base_url="https://example.sensorsdata.cn",
        api_key="sk-config",
        project="config-project",
        timeout=18.0,
        max_retries=6,
    )

    from_config = AsyncSensorsAnalyticsClient.from_config(config)
    assert from_config.config.api_key == "sk-config"
    assert from_config.config.timeout == 18.0

    monkeypatch.setattr(
        "sa_openapi.async_client.ConfigManager.get_profile",
        lambda self, profile="default": config if profile == "prod" else None,
    )

    from_profile = AsyncSensorsAnalyticsClient.from_profile("prod")
    assert from_profile.config.project == "config-project"

    with pytest.raises(ValueError, match="Profile 'missing' not found"):
        AsyncSensorsAnalyticsClient.from_profile("missing")


def test_sync_service_proxy_wraps_coroutines():
    """Test sync proxy turns async methods into blocking calls."""
    service = DummyAsyncService("proxy")

    def run_sync(coro):
        coro.close()
        return "wrapped"

    proxy = _SyncServiceProxy(service, run_sync)

    assert proxy.ping("value") == "wrapped"
    assert proxy.ping.__name__ == "ping"
    assert proxy.label == "proxy"


def test_sync_client_context_manager_proxies_services(monkeypatch):
    """Test sync client service proxies and context manager cleanup."""
    monkeypatch.setattr(client_module, "AsyncSensorsAnalyticsClient", FakeAsyncClient)

    with SensorsAnalyticsClient(
        base_url="https://example.sensorsdata.cn",
        api_key="sk-test",
    ) as client:
        assert client.dashboard.ping("ok") == "dashboard:ok"
        assert client.model.ping("sql") == "model:sql"
        assert client.dashboard.label == "dashboard"
        async_client = client._async_client

    assert client._closed is True
    async_client.aclose.assert_awaited_once()


def test_sync_client_close_is_idempotent_and_rejects_new_work(monkeypatch):
    """Test closing a sync client twice is safe."""
    monkeypatch.setattr(client_module, "AsyncSensorsAnalyticsClient", FakeAsyncClient)
    client = SensorsAnalyticsClient(
        base_url="https://example.sensorsdata.cn",
        api_key="sk-test",
    )

    client.close()
    client.close()

    client._async_client.aclose.assert_awaited_once()
    with pytest.raises(RuntimeError, match="Client is closed"):
        client._run_sync(None)


def test_sync_client_factories(monkeypatch):
    """Test sync client factories derive expected settings."""
    monkeypatch.setattr(client_module, "AsyncSensorsAnalyticsClient", FakeAsyncClient)
    config = ClientConfig(
        base_url="https://example.sensorsdata.cn",
        api_key="sk-config",
        project="sync-project",
        timeout=10.0,
        max_retries=5,
    )

    from_config = SensorsAnalyticsClient.from_config(config)
    try:
        assert from_config._sync_timeout == 30.0
        assert from_config._async_client.init_args["project"] == "sync-project"
    finally:
        from_config.close()

    monkeypatch.setattr(
        "sa_openapi.client.ConfigManager.get_profile",
        lambda self, profile="default": config if profile == "prod" else None,
    )

    from_profile = SensorsAnalyticsClient.from_profile("prod")
    try:
        assert from_profile._async_client.init_args["api_key"] == "sk-config"
    finally:
        from_profile.close()

    with pytest.raises(ValueError, match="Profile 'missing' not found"):
        SensorsAnalyticsClient.from_profile("missing")
