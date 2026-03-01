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
from .dataset import (
    CreateSavedQueryParams,
    Dataset,
    QueryParams,
    SavedQuery,
    Schema,
    SchemaField,
)
from .model import (
    AttributionData,
    AttributionParams,
    AttributionReport,
    ByField,
    Filter,
    FunnelParams,
    FunnelReport,
    FunnelStep,
    Measure,
    RetentionData,
    RetentionParams,
    RetentionReport,
    SqlExplainResult,
    SqlQueryParams,
    SqlValidateResult,
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
    # Dataset
    "Dataset",
    "Schema",
    "SchemaField",
    "SavedQuery",
    "QueryParams",
    "CreateSavedQueryParams",
    # Model - Common
    "Measure",
    "Filter",
    "ByField",
    # Model - Funnel
    "FunnelParams",
    "FunnelStep",
    "FunnelReport",
    # Model - Retention
    "RetentionParams",
    "RetentionData",
    "RetentionReport",
    # Model - Attribution
    "AttributionParams",
    "AttributionData",
    "AttributionReport",
    # Model - SQL
    "SqlQueryParams",
    "SqlExplainResult",
    "SqlValidateResult",
]
