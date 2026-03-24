"""EventMeta service implementation."""

from .._auth import AuthHandler
from .._transport import AiohttpTransport
from ..models.event_meta import EventDefine, TagInfo


class EventMetaServiceV1:
    """EventMeta service for Sensors Analytics."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_v1_base_url

    async def list_events_all(self) -> list[EventDefine]:
        """Get all events list.

        Returns:
            List of event definitions
        """
        response = await self._transport.get(
            f"{self._base_url}/event-meta/events/all",
        )
        data = response.json()
        raw = data.get("data", {})
        events = raw.get("events", []) if isinstance(raw, dict) else []
        return [EventDefine(**item) for item in events if isinstance(item, dict)]

    async def list_event_tags(self) -> list[TagInfo]:
        """Get all event tags list.

        Returns:
            List of event tags
        """
        response = await self._transport.get(
            f"{self._base_url}/event-meta/events/tags",
        )
        data = response.json()
        raw = data.get("data", {})
        tag_infos = raw.get("tagInfos", raw.get("tag_infos", [])) if isinstance(raw, dict) else []
        return [TagInfo(**item) for item in tag_infos if isinstance(item, dict)]
