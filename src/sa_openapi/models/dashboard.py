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


class BookmarkRelateDashboard(BaseModel):
    """Dashboard that a bookmark belongs to."""

    id: str | None = None
    name: str | None = None

    model_config = {"populate_by_name": True}


class Bookmark(BaseModel):
    """Dashboard bookmark model (from GET /dashboard/bookmarks)."""

    id: int | None = None
    user_id: int | None = None
    type: str | None = None
    name: str | None = None
    user_cname: str | None = None
    create_time: str | None = None
    dashboards: list[BookmarkRelateDashboard] = Field(default_factory=list)

    model_config = {"populate_by_name": True}
