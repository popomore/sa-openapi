"""
SensorsData Analytics OpenAPI Python SDK.

提供 Python SDK 和 CLI 工具来访问神策分析平台 API。
"""

from sa_openapi.client import SensorsAnalyticsClient
from sa_openapi.exceptions import (
    AuthenticationError,
    NotFoundError,
    SensorsAnalyticsError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "SensorsAnalyticsClient",
    "SensorsAnalyticsError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
]

# 异步客户端按需导入
try:
    from sa_openapi.async_client import AsyncSensorsAnalyticsClient

    __all__.append("AsyncSensorsAnalyticsClient")
except ImportError:
    pass
