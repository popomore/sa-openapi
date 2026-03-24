"""SmartAlarm data models."""

from pydantic import BaseModel, Field


class SmartAlarmConfig(BaseModel):
    """Smart alarm configuration model."""

    id: int
    title: str
    emails: list[str] = Field(default_factory=list)
    unit: str
    send_alarm: bool = Field(alias="sendAlarm")
    history: dict | None = None

    model_config = {"populate_by_name": True}


class SmartAlarmListRequest(BaseModel):
    """Request parameters for querying alarm list."""

    title: str | None = None
    units: list[str] | None = None
    create_user_ids: list[int] | None = Field(None, alias="createUserIds")
    disables: list[bool] | None = None
    request_id: str | None = Field(None, alias="requestId")

    model_config = {"populate_by_name": True}


class SmartAlarmListResponse(BaseModel):
    """Response for alarm list query."""

    total: int
    ids: list[int] = Field(default_factory=list)

    model_config = {"populate_by_name": True}
