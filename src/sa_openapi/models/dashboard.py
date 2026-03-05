"""Dashboard data models."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DashboardType(str, Enum):
    """Dashboard type enumeration."""

    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class Navigation(BaseModel):
    """Dashboard navigation model.

    API list 返回: id, title, dashboards
    API get 返回: id, name, type, ownerId, createdAt, updatedAt
    """

    id: int
    name: str | None = None  # get 接口
    title: str | None = None  # list 接口
    type: DashboardType | str | None = None
    owner_id: int | None = Field(None, alias="ownerId")
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")
    dashboards: list = Field(default_factory=list)

    model_config = {"populate_by_name": True}

    @property
    def display_name(self) -> str:
        """显示名称, 兼容 name 和 title."""
        return self.name or self.title or str(self.id)


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
