"""Dataset data models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Dataset(BaseModel):
    """Dataset model."""

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
