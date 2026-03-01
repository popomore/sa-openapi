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
    channels = client.channel.list_channel()
    datasets = client.dataset.list_dataset()

    client.close()
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
from .client import SensorsAnalyticsClient

__version__ = "0.1.0"

__all__ = [
    # Version
    "__version__",
    # Client
    "SensorsAnalyticsClient",
    "ClientConfig",
    "ConfigManager",
    # Exceptions
    "SensorsAnalyticsError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
    "TimeoutError",
]
