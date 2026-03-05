"""Common data models for sa-openapi."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class HttpApiResult(BaseModel, Generic[T]):
    """Wrapper for API response with data."""

    code: str = "SUCCESS"
    message: str | None = None
    request_id: str | None = Field(None, alias="requestId")
    data: T | None = None
    error_info: ErrorInfo | None = Field(None, alias="errorInfo")

    model_config = {"populate_by_name": True}


class ErrorInfo(BaseModel):
    """Error information from API response."""

    code: str
    message: str


class Pagination(BaseModel):
    """Pagination information."""

    page: int
    page_size: int = Field(alias="pageSize")
    total: int
    total_pages: int = Field(alias="totalPages")

    model_config = {"populate_by_name": True}

    @property
    def has_next(self) -> bool:
        """Check if there is a next page."""
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        """Check if there is a previous page."""
        return self.page > 1


class BookmarkData(BaseModel):
    """Bookmark data response."""

    columns: list[str]
    rows: list[list[Any]]
    total: int | None = None


class LinkData(BaseModel):
    """Link data response."""

    columns: list[str]
    rows: list[list[Any]]
    total: int | None = None


class QueryResult(BaseModel):
    """SQL query result."""

    columns: list[str]
    rows: list[list[Any]]
    total: int | None = None
    elapsed_ms: int | None = Field(None, alias="elapsedMs")

    model_config = {"populate_by_name": True}
