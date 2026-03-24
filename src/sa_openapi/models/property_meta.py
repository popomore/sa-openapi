"""PropertyMeta data models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PropertyDefine(BaseModel):
    """Property definition model (shared by event and user properties)."""

    id: int
    name: str
    cname: str
    data_type: str
    is_virtual: bool = False
    has_dict: bool = False
    unit: str | None = None
    platforms: list[str] = Field(default_factory=list)
    trigger_opportunity: str | None = None
    create_time: str | None = None
    update_time: str | None = None

    model_config = {"populate_by_name": True}


class UserGroupDefine(BaseModel):
    """User group (分群) definition model."""

    id: int
    name: str
    cname: str
    data_type: str
    create_time: str | None = None
    update_time: str | None = None

    model_config = {"populate_by_name": True}


class UserTagDirDefine(BaseModel):
    """User tag directory node model (recursive tree)."""

    name: str
    cname: str
    data_type: str
    type: str
    sub_nodes: list[UserTagDirDefine] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class EventWithProperty(BaseModel):
    """Event with its associated properties."""

    event_define: dict = Field(alias="eventDefine")
    properties: list[PropertyDefine] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class GetPropertyValueRequest(BaseModel):
    """Request parameters for fetching property candidate values."""

    table_type: str = Field(alias="tableType")
    property_name: str = Field(alias="propertyName")
    limit: int | None = None

    model_config = {"populate_by_name": True}
