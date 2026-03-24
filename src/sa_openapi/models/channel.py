"""Channel data models."""

from datetime import datetime
from typing import Any

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


class ChannelUrlData(BaseModel):
    """Single channel link to create."""

    channel_type: str = Field(alias="channel_type")
    device_type: str | None = Field(None, alias="device_type")
    app_address: str | None = Field(None, alias="app_address")
    target_url: str | None = Field(None, alias="target_url")
    parameters: dict[str, str] | None = None
    app_inner_info: str | None = Field(None, alias="app_inner_info")
    web_landing_page: str | None = Field(None, alias="web_landing_page")
    application_name: str | None = Field(None, alias="application_name")
    custom_properties: list[Any] | None = Field(None, alias="custom_properties")
    app_id: str | None = Field(None, alias="app_id")
    app_secret: str | None = Field(None, alias="app_secret")
    mina_type: str | None = Field(None, alias="mina_type")
    access_token: str | None = Field(None, alias="access_token")

    model_config = {"populate_by_name": True}


class CreatedLinkItem(BaseModel):
    """Single created link result."""

    id: int | None = None
    name: str | None = None
    app_address: str | None = Field(None, alias="app_address")
    short_url: str | None = Field(None, alias="short_url")
    whole_url: str | None = Field(None, alias="whole_url")
    is_duplicate: bool | None = Field(None, alias="is_duplicate")
    error_msg: str | None = Field(None, alias="error_msg")
    resource_base64: str | None = Field(None, alias="resource_base64")
    application_name: str | None = Field(None, alias="application_name")
    web_landing_page: str | None = Field(None, alias="web_landing_page")

    model_config = {"populate_by_name": True}


class CreateLinkResult(BaseModel):
    """Response from create link API."""

    created: int | None = None
    duplicated: int | None = None
    failed: int | None = None
    status: str | None = None
    channel_urls: list[CreatedLinkItem] | None = Field(None, alias="channel_urls")

    model_config = {"populate_by_name": True}
