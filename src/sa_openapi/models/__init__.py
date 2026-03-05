"""Data models for sa-openapi."""

from .channel import Channel, Link, LinkData, LinkDataParams, LinkExportParams
from .common import (
    BookmarkData,
    ErrorInfo,
    HttpApiResult,
    Pagination,
    QueryResult,
)
from .dashboard import BookmarkDataParams, BookmarkExportParams, Navigation
from .dataset import CreateSavedQueryParams, Dataset, SavedQuery
from .model import (
    ApiFunnelDefine,
    ApiRequestElementCondition,
    ApiRequestEventWithFilter,
    ApiRequestFilter,
    ApiRequestMeasure,
    AttributionReport,
    AttributionReportRequest,
    AttributionReportResponse,
    FunnelReport,
    FunnelReportRequest,
    FunnelReportResponse,
    LinkEvent,
    Measure,
    RetentionReport,
    RetentionReportRequest,
    RetentionReportResponse,
    SqlExplainResult,
    SqlQueryRequest,
    SqlQueryResponse,
    SqlValidateResult,
)

__all__ = [
    # model (v1 aligned)
    "ApiFunnelDefine",
    "ApiRequestElementCondition",
    "ApiRequestEventWithFilter",
    "ApiRequestFilter",
    "ApiRequestMeasure",
    "AttributionReport",
    "AttributionReportRequest",
    "AttributionReportResponse",
    # common
    "BookmarkData",
    # dashboard
    "BookmarkDataParams",
    "BookmarkExportParams",
    "ByField",
    # channel
    "Channel",
    # dataset
    "CreateSavedQueryParams",
    "Dataset",
    "ErrorInfo",
    # backward compatibility
    "Filter",
    "FunnelReport",
    "FunnelReportRequest",
    "FunnelReportResponse",
    "HttpApiResult",
    "Link",
    "LinkData",
    "LinkDataParams",
    "LinkEvent",
    "LinkExportParams",
    "Measure",
    "Navigation",
    "Pagination",
    "QueryResult",
    "RetentionReport",
    "RetentionReportRequest",
    "RetentionReportResponse",
    "SavedQuery",
    "SqlExplainResult",
    "SqlQueryRequest",
    "SqlQueryResponse",
    "SqlValidateResult",
]
