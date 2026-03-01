"""Model data models."""

from typing import Any

from pydantic import BaseModel, Field


# --- Common ---


class Measure(BaseModel):
    """Measure definition for analysis."""

    event: str
    aggregator: str  # COUNT, SUM, AVG, etc.
    property: str | None = None

    model_config = {"populate_by_name": True}


class Filter(BaseModel):
    """Filter condition."""

    property: str
    operator: str  # =, !=, >, <, IN, etc.
    value: Any

    model_config = {"populate_by_name": True}


class ByField(BaseModel):
    """Group by field."""

    property: str
    type: str | None = None

    model_config = {"populate_by_name": True}


# --- Funnel ---


class FunnelParams(BaseModel):
    """Funnel analysis parameters."""

    measures: list[Measure]
    filter: Filter | None = None
    by_fields: list[ByField] | None = Field(None, alias="byFields")
    window: int | None = None  # Conversion window in days
    start_date: str | None = Field(None, alias="startDate")
    end_date: str | None = Field(None, alias="endDate")

    model_config = {"populate_by_name": True}


class FunnelStep(BaseModel):
    """Funnel step result."""

    step: int
    event: str
    total: int
    conversion_rate: float = Field(alias="conversionRate")
    avg_duration: float | None = Field(None, alias="avgDuration")

    model_config = {"populate_by_name": True}


class FunnelReport(BaseModel):
    """Funnel analysis report."""

    steps: list[FunnelStep]
    total: int
    overall_conversion: float = Field(alias="overallConversion")

    model_config = {"populate_by_name": True}


# --- Retention ---


class RetentionParams(BaseModel):
    """Retention analysis parameters."""

    initial_event: str = Field(alias="initialEvent")
    return_event: str = Field(alias="returnEvent")
    filter: Filter | None = None
    by_fields: list[ByField] | None = Field(None, alias="byFields")
    periods: list[int]  # [1, 3, 7, 14, 30]
    start_date: str | None = Field(None, alias="startDate")
    end_date: str | None = Field(None, alias="endDate")

    model_config = {"populate_by_name": True}


class RetentionData(BaseModel):
    """Retention data."""

    period: int
    retention_rate: float = Field(alias="retentionRate")
    returned_users: int = Field(alias="returnedUsers")
    total_users: int = Field(alias="totalUsers")

    model_config = {"populate_by_name": True}


class RetentionReport(BaseModel):
    """Retention analysis report."""

    data: list[RetentionData]
    cohort_size: int = Field(alias="cohortSize")

    model_config = {"populate_by_name": True}


# --- Attribution ---


class AttributionParams(BaseModel):
    """Attribution analysis parameters."""

    conversion_event: str = Field(alias="conversionEvent")
    touch_points: list[str] = Field(alias="touchPoints")
    model: str  # FIRST_TOUCH, LAST_TOUCH, LINEAR, etc.
    window: int | None = None
    start_date: str | None = Field(None, alias="startDate")
    end_date: str | None = Field(None, alias="endDate")

    model_config = {"populate_by_name": True}


class AttributionData(BaseModel):
    """Attribution data."""

    touch_point: str = Field(alias="touchPoint")
    credit: float
    conversions: int

    model_config = {"populate_by_name": True}


class AttributionReport(BaseModel):
    """Attribution analysis report."""

    data: list[AttributionData]
    total_conversions: int = Field(alias="totalConversions")

    model_config = {"populate_by_name": True}


# --- SQL ---


class SqlQueryParams(BaseModel):
    """SQL query parameters."""

    sql: str
    limit: int | None = None

    model_config = {"populate_by_name": True}


class SqlExplainResult(BaseModel):
    """SQL execution plan."""

    plan: str
    estimated_cost: float = Field(alias="estimatedCost")
    estimated_rows: int = Field(alias="estimatedRows")

    model_config = {"populate_by_name": True}


class SqlValidateResult(BaseModel):
    """SQL validation result."""

    valid: bool
    error: str | None = None
