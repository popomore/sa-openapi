"""sa-openapi - Sensors Analytics OpenAPI Python SDK and CLI.

A Python SDK and CLI tool for Sensors Analytics OpenAPI.

Usage:
    from sa_openapi import SensorsAnalyticsClient

    client = SensorsAnalyticsClient(
        base_url="https://your-instance.sensorsdata.cn",
        api_key="sk-xxx",
        project="default",
    )

    # Use services
    navigations = client.dashboard.list_navigation()
    campaigns = client.channel.list_campaigns()
    datasets = client.dataset.list_datasets()
    events = client.event_meta.list_events_all()
    props = client.property_meta.list_all_event_properties()
    alarm = client.smart_alarm.get_alarm_config(1)

    client.close()

Async usage:
    from sa_openapi import AsyncSensorsAnalyticsClient

    async with AsyncSensorsAnalyticsClient(
        base_url="https://your-instance.sensorsdata.cn",
        api_key="sk-xxx",
        project="default",
    ) as client:
        navigations = await client.dashboard.list_navigation()
"""

from ._config import ClientConfig, ConfigManager
from ._exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    SensorsAnalyticsError,
    ServerError,
    TimeoutError,
    ValidationError,
)
from .async_client import AsyncSensorsAnalyticsClient
from .client import SensorsAnalyticsClient

__version__ = "0.1.0"

__all__ = [
    "AsyncSensorsAnalyticsClient",
    "AuthenticationError",
    "ClientConfig",
    "ConfigManager",
    "NetworkError",
    "NotFoundError",
    "RateLimitError",
    # Client
    "SensorsAnalyticsClient",
    # Exceptions
    "SensorsAnalyticsError",
    "ServerError",
    "TimeoutError",
    "ValidationError",
    # Version
    "__version__",
]
