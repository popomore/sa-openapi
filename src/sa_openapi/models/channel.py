"""Channel data models."""

from datetime import datetime

from pydantic import BaseModel, Field


class Channel(BaseModel):
    """Channel model."""

    id: int
    name: str
    description: str | None = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}


class Link(BaseModel):
    """Channel link model."""

    id: int
    name: str
    channel_id: int = Field(alias="channelId")
    url: str
    created_by: int = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}


class LinkDataParams(BaseModel):
    """Parameters for getting link data."""

    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    filters: list[dict] | None = None
    time_zone: str | None = Field("Asia/Shanghai", alias="timeZone")

    model_config = {"populate_by_name": True}


class LinkData(BaseModel):
    """Link data response."""

    columns: list[str]
    rows: list[list]
    total: int | None = None


class LinkExportParams(BaseModel):
    """Parameters for exporting link."""

    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    filters: list[dict] | None = None
    format: str = "csv"
    time_zone: str | None = Field("Asia/Shanghai", alias="timeZone")

    model_config = {"populate_by_name": True}
