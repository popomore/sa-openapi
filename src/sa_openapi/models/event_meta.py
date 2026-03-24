"""EventMeta data models."""

from pydantic import BaseModel, Field


class EventDefine(BaseModel):
    """Event definition model."""

    id: int
    name: str
    cname: str
    is_virtual: bool = False
    tags: list[int] = Field(default_factory=list)
    comment: str | None = None
    total_count: int | None = None
    platforms: list[str] = Field(default_factory=list)
    trigger_opportunity: str | None = None
    create_time: str | None = None
    update_time: str | None = None

    model_config = {"populate_by_name": True}


class TagInfo(BaseModel):
    """Event tag model."""

    id: int
    name: str
    color: str | None = None

    model_config = {"populate_by_name": True}
