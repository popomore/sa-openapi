"""Dataset data models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

# ============================================================================
# OpenAPI-aligned models (v1 spec)
# ============================================================================


class ColumnMeta(BaseModel):
    """Column metadata for a dataset."""

    column_name: str
    column_cname: str | None = None
    data_type: str | None = None
    column_type: str | None = None
    column_usage_type: str | None = None
    origin_column_name: str | None = None
    sort_num: int | None = None
    origin_data_type: str | None = None
    is_system_time: bool | None = None

    model_config = {"populate_by_name": True}


class PageInfo(BaseModel):
    """Pagination info."""

    current_page: int
    page_count: int
    total: int

    model_config = {"populate_by_name": True}


class DatasetResponse(BaseModel):
    """Simplified dataset summary."""

    dataset_id: int
    dataset_type: str | None = None
    dataset_cname: str | None = None
    is_scheduler_pause: bool | None = None

    model_config = {"populate_by_name": True}


class DatasetDetailResponse(BaseModel):
    """Full dataset detail."""

    dataset_id: int
    dataset_type: str | None = None
    dataset_storage_type: str | None = None
    dataset_cname: str | None = None
    columns: list[ColumnMeta] = Field(default_factory=list)
    last_sync_success_time: str | None = None
    sync_status: str | None = None
    scheduler_status: str | None = None
    sync_crontab: str | None = None
    sync_type: str | None = None
    update_time: str | None = None
    description: str | None = None
    time_unit: str | None = None

    model_config = {"populate_by_name": True}


class DatasetGroup(BaseModel):
    """Dataset group."""

    id: int | None = None
    group_name: str | None = None

    model_config = {"populate_by_name": True}


class DatasetDetailRequest(BaseModel):
    """Request for dataset detail."""

    dataset_id: int
    model_type: str | None = None

    model_config = {"populate_by_name": True}


class DatasetListRequest(BaseModel):
    """Request for dataset list."""

    group_name: str | None = None
    dataset_types: list[str] | None = None
    scheduler_statuses: list[str] | None = None
    sync_statuses: list[str] | None = None
    page_index: int | None = None
    page_size: int | None = None
    is_scheduler_pause: bool | None = None

    model_config = {"populate_by_name": True}


class QueryParameter(BaseModel):
    """SQL query parameter (key-value pair)."""

    param_key: str
    param_value: str | None = None

    model_config = {"populate_by_name": True}


class DatasetTableSqlRequest(BaseModel):
    """Request for dataset SQL query."""

    sql: str
    query_parameters: list[QueryParameter] | None = None
    description: str | None = None

    model_config = {"populate_by_name": True}


class DatasetTableSqlResponse(BaseModel):
    """Response for dataset SQL query."""

    data: list[list[Any]] | None = None
    columns: list[str] | None = None

    model_config = {"populate_by_name": True}


class DatasetModelRequest(BaseModel):
    """Request for dataset model query."""

    dataset_id: int
    dimensions: list[str] | None = None
    measures: list[Any] | None = None
    dimension_filters: list[Any] | None = None
    sorts: list[Any] | None = None
    description: str | None = None
    page_index: int | None = None
    page_size: int | None = None
    from_date: str | None = None
    to_date: str | None = None
    measure_filters: list[Any] | None = None
    model_type: str | None = None

    model_config = {"populate_by_name": True}


class DatasetModelResponse(BaseModel):
    """Response for dataset model query."""

    data: list[list[Any]] | None = None
    columns: list[str] | None = None
    page_info: PageInfo | None = None

    model_config = {"populate_by_name": True}


class DatasetRefreshRequest(BaseModel):
    """Request to refresh a dataset."""

    dataset_id: int
    sync_type: str | None = None
    refresh_from_date: str | None = None
    refresh_to_date: str | None = None

    model_config = {"populate_by_name": True}


class DatasetRefreshResponse(BaseModel):
    """Response for dataset refresh."""

    sync_task_id: str | None = None

    model_config = {"populate_by_name": True}


class DatasetSyncTaskDetailResponse(BaseModel):
    """Response for sync task detail."""

    sync_task_id: str | None = None
    sync_status: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    duration_seconds: int | None = None
    failed_reason: str | None = None

    model_config = {"populate_by_name": True}


# ============================================================================
# Legacy models (kept for backward compatibility)
# ============================================================================


class Dataset(BaseModel):
    """Dataset model (legacy)."""

    id: int
    name: str
    description: str | None = None
    type: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}


class SchemaField(BaseModel):
    """Schema field model."""

    name: str
    field_type: str = Field(alias="type")
    nullable: bool
    comment: str | None = None

    model_config = {"populate_by_name": True}


class Schema(BaseModel):
    """Dataset schema model."""

    fields: list[SchemaField]


class SavedQuery(BaseModel):
    """Saved query model."""

    id: int
    name: str
    sql: str
    dataset_id: int = Field(alias="datasetId")
    created_by: int = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}


class QueryParams(BaseModel):
    """SQL query parameters."""

    sql: str
    limit: int | None = None
    offset: int | None = None

    model_config = {"populate_by_name": True}


class QueryResult(BaseModel):
    """SQL query result."""

    columns: list[str]
    rows: list[list[Any]]
    total: int | None = None
    elapsed_ms: int | None = Field(None, alias="elapsedMs")

    model_config = {"populate_by_name": True}


class CreateSavedQueryParams(BaseModel):
    """Parameters for creating saved query."""

    name: str
    sql: str
    description: str | None = None

    model_config = {"populate_by_name": True}
