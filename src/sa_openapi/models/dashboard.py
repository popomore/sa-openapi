"""Dashboard data models."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DashboardType(str, Enum):
    """Dashboard type enumeration."""

    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class Navigation(BaseModel):
    """Dashboard navigation model."""

    id: int
    name: str
    type: DashboardType
    owner_id: int = Field(alias="ownerId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}


class Bookmark(BaseModel):
    """Dashboard bookmark model."""

    id: int
    name: str
    navigation_id: int = Field(alias="navigationId")
    owner_id: int = Field(alias="ownerId")
    description: str | None = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}


class BookmarkDataParams(BaseModel):
    """Parameters for getting bookmark data."""

    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    filters: list[dict] | None = None
    time_zone: str | None = Field("Asia/Shanghai", alias="timeZone")

    model_config = {"populate_by_name": True}


class BookmarkData(BaseModel):
    """Bookmark data response."""

    columns: list[str]
    rows: list[list]
    total: int | None = None


class BookmarkExportParams(BaseModel):
    """Parameters for exporting bookmark."""

    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    filters: list[dict] | None = None
    format: str = "csv"
    time_zone: str | None = Field("Asia/Shanghai", alias="timeZone")

    model_config = {"populate_by_name": True}
