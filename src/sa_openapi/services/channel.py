"""Channel service implementation."""

from typing import Any

from .._auth import AuthHandler
from .._transport import Transport
from ..models.channel import (
    Channel,
    Link,
    LinkData,
    LinkDataParams,
    LinkExportParams,
)


class ChannelService:
    """Channel service for Sensors Analytics."""

    def __init__(self, transport: Transport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_base_url

    def list_channel(self) -> list[Channel]:
        """Get channel list.

        Returns:
            List of channels
        """
        response = self._transport.get(f"{self._base_url}/channel")
        data = response.json()
        return [Channel(**item) for item in data.get("data", [])]

    def list_link(self, channel_id: int) -> list[Link]:
        """Get link list for a channel.

        Args:
            channel_id: Channel ID

        Returns:
            List of links
        """
        response = self._transport.get(
            f"{self._base_url}/channel/link",
            params={"channel_id": channel_id},
        )
        data = response.json()
        return [Link(**item) for item in data.get("data", [])]

    def get_link(self, link_id: int) -> Link:
        """Get specific link.

        Args:
            link_id: Link ID

        Returns:
            Link details
        """
        response = self._transport.get(
            f"{self._base_url}/channel/link/{link_id}",
        )
        data = response.json()
        return Link(**data.get("data", {}))

    def get_link_data(
        self,
        link_id: int,
        params: LinkDataParams | dict[str, Any],
    ) -> LinkData:
        """Get link data.

        Args:
            link_id: Link ID
            params: Query parameters

        Returns:
            Link data
        """
        if isinstance(params, dict):
            params = LinkDataParams(**params)

        response = self._transport.post(
            f"{self._base_url}/channel/link/{link_id}/data",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        data = response.json()
        return LinkData(**data.get("data", {}))

    def export_link(
        self,
        link_id: int,
        params: LinkExportParams | dict[str, Any],
    ) -> bytes:
        """Export link data.

        Args:
            link_id: Link ID
            params: Export parameters

        Returns:
            Export file content (bytes)
        """
        if isinstance(params, dict):
            params = LinkExportParams(**params)

        response = self._transport.post(
            f"{self._base_url}/channel/link/{link_id}/export",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        return response.content
