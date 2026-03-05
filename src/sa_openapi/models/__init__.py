"""Data models for sa-openapi."""

from .channel import Channel, Link, LinkData, LinkDataParams, LinkExportParams
from .common import (
    BookmarkData,
    ErrorInfo,
    HttpApiResult,
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
    "AttributionData",
    # Model - Attribution
    "AttributionParams",
    "AttributionReport",
    "Bookmark",
    # Common
    "BookmarkData",
    "BookmarkDataParams",
    "BookmarkExportParams",
    "ByField",
    # Channel
    "Channel",
    "CreateSavedQueryParams",
    # Dashboard
    "DashboardType",
    # Dataset
    "Dataset",
    "ErrorInfo",
    "Filter",
    # Model - Funnel
    "FunnelParams",
    "FunnelReport",
    "FunnelStep",
    "HttpApiResult",
    "Link",
    "LinkData",
    "LinkDataParams",
    "LinkExportParams",
    # Model - Common
    "Measure",
    "Navigation",
    "Pagination",
    "QueryParams",
    "QueryResult",
    "RetentionData",
    # Model - Retention
    "RetentionParams",
    "RetentionReport",
    "SavedQuery",
    "Schema",
    "SchemaField",
    "SqlExplainResult",
    # Model - SQL
    "SqlQueryParams",
    "SqlValidateResult",
]
