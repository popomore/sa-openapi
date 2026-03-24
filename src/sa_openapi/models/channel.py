"""Channel data models."""

from typing import Any

from pydantic import BaseModel, Field


class CampaignDetail(BaseModel):
    """Campaign detail model."""

    campaign_name: str | None = None
    branch_num: int | None = None
    latest_use_time: str | None = None

    model_config = {"populate_by_name": True}


class CampaignListResponse(BaseModel):
    """Response for campaign list."""

    campaign_details: list[CampaignDetail] = Field(default_factory=list)
    total_rows: int = 0
    total_page: int = 0
    page_num: int = 0
    page_size: int = 20

    model_config = {"populate_by_name": True}


class ChannelLinkDetail(BaseModel):
    """Channel link detail model."""

    id: int | None = None
    name: str | None = None
    channel_type: str | None = None
    device_type: str | None = None
    short_url: str | None = None
    whole_url: str | None = None
    app_address: str | None = None
    application_name: str | None = None
    web_landing_page: str | None = None
    create_time: str | None = None
    update_time: str | None = None

    model_config = {"populate_by_name": True}


class ChannelLinkListResponse(BaseModel):
    """Response for channel link list."""

    detail_results: list[ChannelLinkDetail] = Field(default_factory=list)
    total_rows: int = 0
    total_page: int = 0
    page_num: int = 0
    page_size: int = 20

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
