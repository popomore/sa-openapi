"""Model data models - OpenAPI v1 aligned."""

from typing import Any

from pydantic import BaseModel, Field

# ============================================================================
# Request Models (OpenAPI v1)
# ============================================================================


class ApiRequestFilter(BaseModel):
    relation: str | None = None
    conditions: list['ApiRequestElementCondition'] | None = None
    filters: list['ApiRequestFilter'] | None = None


class ApiRequestElementCondition(BaseModel):
    field: str | None = None
    function: str | None = None
    params: list[Any] | None = None


class ApiRequestEventWithFilter(BaseModel):
    event_name: str | None = None
    filter: dict[str, Any] | None = None
    by_field: str | None = None
    relevance_field: str | None = None


class ApiFunnelDefine(BaseModel):
    steps: list[ApiRequestEventWithFilter] | None = None
    max_convert_time: int | None = None


class ApiRequestMeasure(BaseModel):
    event_name: str | None = None
    aggregator: str | None = None
    field: str | None = None
    expression: str | None = None
    expression_filters: list[ApiRequestFilter] | None = None
    filter: dict[str, Any] | None = None
    name: str | None = None
    events: list[str] | None = None
    params: list[dict[str, Any]] | None = None
    split: bool | None = None
    profit_rate: float | None = None
    by_session: bool | None = None
    expression_denominator_without_group: bool | None = None
    atom_measure_without_group: bool | None = None
    show_cname: str | None = None


class LinkEvent(BaseModel):
    event_name: str | None = None
    link_properties: dict[str, Any] | None = None
    filter: dict[str, Any] | None = None


# --- Funnel Request ---

class FunnelReportRequest(BaseModel):
    funnel: dict[str, Any] | None = None
    from_date: str | None = Field(None, alias='fromDate')
    to_date: str | None = Field(None, alias='toDate')
    filter: dict[str, Any] | None = None
    by_fields: list[str] | None = Field(None, alias='byFields')
    extend_over_end_date: bool | None = Field(None, alias='extendOverEndDate')
    by_field_step: int | None = Field(None, alias='byFieldStep')
    sampling_factor: int | None = Field(None, alias='samplingFactor')
    filter_field_steps: list[int] | None = Field(None, alias='filterFieldSteps')
    request_id: str | None = Field(None, alias='requestId')
    use_cache: bool | None = Field(None, alias='useCache')
    rollup: bool | None = None
    calculation_caliber: str | None = Field(None, alias='calculationCaliber')
    limit: int | None = None
    bucket_params: dict[str, Any] | None = Field(None, alias='bucketParams')
    by_field_steps: list[int] | None = Field(None, alias='byFieldSteps')
    time_zone_mode: str | None = Field(None, alias='timeZoneMode')
    server_time_zone: str | None = Field(None, alias='serverTimeZone')
    subject_id: str | None = Field(None, alias='subjectId')
    unit: str | None = None
    funnel_id: int | None = Field(None, alias='funnelId')

    model_config = {'populate_by_name': True}


# --- Retention Request ---

class RetentionReportRequest(BaseModel):
    from_date: str | None = Field(None, alias='fromDate')
    to_date: str | None = Field(None, alias='toDate')
    duration: int | None = None
    first_event: dict[str, Any] | None = Field(None, alias='firstEvent')
    second_event: dict[str, Any] | None = Field(None, alias='secondEvent')
    filter: dict[str, Any] | None = None
    measures: list[ApiRequestMeasure] | None = None
    user_filter: dict[str, Any] | None = Field(None, alias='userFilter')
    unit: str | None = None
    extend_over_end_date: bool | None = Field(None, alias='extendOverEndDate')
    sampling_factor: int | None = Field(None, alias='samplingFactor')
    is_wastage: bool | None = Field(None, alias='isWastage')
    use_cache: bool | None = Field(None, alias='useCache')
    request_id: str | None = Field(None, alias='requestId')
    by_fields: list[str] | None = Field(None, alias='byFields')
    rollup: bool | None = None
    limit: int | None = None
    bucket_params: dict[str, Any] | None = Field(None, alias='bucketParams')
    time_zone_mode: str | None = Field(None, alias='timeZoneMode')
    server_time_zone: str | None = Field(None, alias='serverTimeZone')
    subject_id: str | None = Field(None, alias='subjectId')

    model_config = {'populate_by_name': True}


# --- Attribution Request ---

class AttributionReportRequest(BaseModel):
    from_date: str | None = Field(None, alias='fromDate')
    to_date: str | None = Field(None, alias='toDate')
    use_cache: bool | None = Field(None, alias='useCache')
    direct_conversion: bool | None = Field(None, alias='directConversion')
    sampling_factor: int | None = Field(None, alias='samplingFactor')
    target_event: dict[str, Any] | None = Field(None, alias='targetEvent')
    link_events: list[LinkEvent] | None = Field(None, alias='linkEvents')
    attribution_events: dict[str, Any] | None = Field(None, alias='attributionEvents')
    filter: dict[str, Any] | None = None
    model_type: str | None = Field(None, alias='modelType')
    lookback_window: dict[str, Any] | None = Field(None, alias='lookbackWindow')
    request_id: str | None = Field(None, alias='requestId')
    rollup: bool | None = None
    limit: int | None = None
    time_zone_mode: str | None = Field(None, alias='timeZoneMode')
    server_time_zone: str | None = Field(None, alias='serverTimeZone')
    subject_id: str | None = Field(None, alias='subjectId')

    model_config = {'populate_by_name': True}


# --- SQL Request ---

class SqlQueryRequest(BaseModel):
    sql: str | None = None
    limit: str | None = None
    request_id: str | None = Field(None, alias='requestId')

    model_config = {'populate_by_name': True}


# ============================================================================
# Response Models (OpenAPI v1)
# ============================================================================


class FunnelReportResponse(BaseModel):
    truncated: bool | None = None
    metadata_columns: dict[str, Any] | None = Field(None, alias='metadataColumns')
    detail_rows: list[list[Any]] | None = Field(None, alias='detailRows')

    model_config = {'populate_by_name': True}


class RetentionReportResponse(BaseModel):
    truncated: bool | None = None
    metadata_columns: dict[str, Any] | None = Field(None, alias='metadataColumns')
    detail_rows: list[list[Any]] | None = Field(None, alias='detailRows')

    model_config = {'populate_by_name': True}


class AttributionReportResponse(BaseModel):
    truncated: bool | None = None
    metadata_columns: dict[str, Any] | None = Field(None, alias='metadataColumns')
    detail_rows: list[list[Any]] | None = Field(None, alias='detailRows')

    model_config = {'populate_by_name': True}


class SqlQueryResponse(BaseModel):
    columns: list[str] | None = None
    data: list[dict[str, Any]] | None = None

    model_config = {'populate_by_name': True}


class SqlExplainResult(BaseModel):
    plan: str | None = None
    estimated_cost: float | None = Field(None, alias='estimatedCost')
    estimated_rows: int | None = Field(None, alias='estimatedRows')

    model_config = {'populate_by_name': True}


class SqlValidateResult(BaseModel):
    valid: bool | None = None
    error: str | None = None


# ============================================================================
# Backward Compatibility Aliases
# ============================================================================

class FunnelReport(BaseModel):
    steps: list[dict[str, Any]] | None = None
    total: int | None = None
    overall_conversion: float | None = Field(None, alias='overallConversion')

    model_config = {'populate_by_name': True}


class RetentionReport(BaseModel):
    data: list[dict[str, Any]] | None = None
    cohort_size: int | None = Field(None, alias='cohortSize')

    model_config = {'populate_by_name': True}


class AttributionReport(BaseModel):
    data: list[dict[str, Any]] | None = None
    total_conversions: int | None = Field(None, alias='totalConversions')

    model_config = {'populate_by_name': True}


Measure = ApiRequestMeasure
Filter = ApiRequestFilter
ByField = ApiRequestEventWithFilter
