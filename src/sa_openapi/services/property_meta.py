"""PropertyMeta service implementation."""

from .._auth import AuthHandler
from .._transport import AiohttpTransport
from ..models.property_meta import (
    EventWithProperty,
    GetPropertyValueRequest,
    PropertyDefine,
    UserGroupDefine,
    UserTagDirDefine,
)


class PropertyMetaServiceV1:
    """PropertyMeta service for Sensors Analytics."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_v1_base_url

    async def list_all_event_properties(self) -> list[PropertyDefine]:
        """Get all event properties.

        Returns:
            List of property definitions
        """
        response = await self._transport.get(
            f"{self._base_url}/property-meta/event-properties/all",
        )
        data = response.json()
        raw = data.get("data", {})
        props = raw.get("properties", []) if isinstance(raw, dict) else []
        return [PropertyDefine(**item) for item in props if isinstance(item, dict)]

    async def list_event_properties(self, events: list[str]) -> list[EventWithProperty]:
        """Get properties for specified events.

        Args:
            events: List of event names

        Returns:
            List of events with their properties
        """
        params = {"events": events}
        response = await self._transport.post(
            f"{self._base_url}/property-meta/event-properties",
            json=params,
        )
        data = response.json()
        raw = data.get("data", {})
        event_props = (
            raw.get("eventProperties", raw.get("event_properties", []))
            if isinstance(raw, dict)
            else []
        )
        return [EventWithProperty(**item) for item in event_props if isinstance(item, dict)]

    async def list_all_user_properties(self) -> list[PropertyDefine]:
        """Get all user properties.

        Returns:
            List of user property definitions
        """
        response = await self._transport.get(
            f"{self._base_url}/property-meta/user-properties/all",
        )
        data = response.json()
        raw = data.get("data", {})
        props = (
            raw.get("userProperties", raw.get("user_properties", []))
            if isinstance(raw, dict)
            else []
        )
        return [PropertyDefine(**item) for item in props if isinstance(item, dict)]

    async def list_user_groups(self) -> list[UserGroupDefine]:
        """Get all user groups (分群).

        Returns:
            List of user group definitions
        """
        response = await self._transport.get(
            f"{self._base_url}/property-meta/user-groups/all",
        )
        data = response.json()
        raw = data.get("data", {})
        groups = raw.get("userGroups", raw.get("user_groups", [])) if isinstance(raw, dict) else []
        return [UserGroupDefine(**item) for item in groups if isinstance(item, dict)]

    async def list_user_tags_with_dir(self) -> list[UserTagDirDefine]:
        """Get user tags with directory structure.

        Returns:
            List of user tag directory nodes (tree)
        """
        response = await self._transport.get(
            f"{self._base_url}/property-meta/user-tags/dir",
        )
        data = response.json()
        raw = data.get("data", {})
        tags = raw.get("userTags", raw.get("user_tags", [])) if isinstance(raw, dict) else []
        return [UserTagDirDefine(**item) for item in tags if isinstance(item, dict)]

    async def get_property_values(
        self,
        table_type: str,
        property_name: str,
        limit: int | None = None,
    ) -> list[str]:
        """Get candidate values for a property.

        Args:
            table_type: Table type (e.g. "event", "user")
            property_name: Property name
            limit: Max number of values to return

        Returns:
            List of property values
        """
        req = GetPropertyValueRequest(
            table_type=table_type,
            property_name=property_name,
            limit=limit,
        )
        response = await self._transport.post(
            f"{self._base_url}/property-meta/property/values",
            json=req.model_dump(by_alias=True, exclude_none=True),
        )
        data = response.json()
        raw = data.get("data", {})
        if isinstance(raw, dict):
            return raw.get("values", [])
        return []
