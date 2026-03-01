"""Data models for sa-openapi."""

from .channel import Channel, Link, LinkData, LinkDataParams, LinkExportParams
from .common import (
    BookmarkData,
    ErrorInfo,
    HttpApiResult,
    LinkData,
    Pagination,
    QueryResult,
)
from .dashboard import (
    Bookmark,
    BookmarkDataParams,
    BookmarkExportParams,
    DashboardType,
    Navigation,
)

__all__ = [
    # Common
    "BookmarkData",
    "ErrorInfo",
    "HttpApiResult",
    "LinkData",
    "Pagination",
    "QueryResult",
    # Dashboard
    "DashboardType",
    "Navigation",
    "Bookmark",
    "BookmarkDataParams",
    "BookmarkExportParams",
    # Channel
    "Channel",
    "Link",
    "LinkDataParams",
    "LinkExportParams",
]
