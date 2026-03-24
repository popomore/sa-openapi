"""Channel service implementation."""

from typing import Any

from .._auth import AuthHandler
from .._transport import AiohttpTransport
from ..models.channel import (
    Channel,
    ChannelUrlData,
    CreatedLinkItem,
    CreateLinkResult,
    Link,
    LinkData,
    LinkDataParams,
    LinkExportParams,
)


class ChannelServiceV1:
    """Channel service for Sensors Analytics."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_v1_base_url

    async def list_channel(self) -> list[Channel]:
        """Get channel list.

        Returns:
            List of channels
        """
        response = await self._transport.get(f"{self._base_url}/channel")
        data = response.json()
        return [Channel(**item) for item in data.get("data", [])]

    async def list_link(self, channel_id: int) -> list[Link]:
        """Get link list for a channel.

        Args:
            channel_id: Channel ID

        Returns:
            List of links
        """
        response = await self._transport.get(
            f"{self._base_url}/channel/link",
            params={"channel_id": channel_id},
        )
        data = response.json()
        return [Link(**item) for item in data.get("data", [])]

    async def get_link(self, link_id: int) -> Link:
        """Get specific link.

        Args:
            link_id: Link ID

        Returns:
            Link details
        """
        response = await self._transport.get(
            f"{self._base_url}/channel/link/{link_id}",
        )
        data = response.json()
        return Link(**data.get("data", {}))

    async def get_link_data(
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

        response = await self._transport.post(
            f"{self._base_url}/channel/link/{link_id}/data",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        data = response.json()
        return LinkData(**data.get("data", {}))

    async def create_link(
        self,
        channel_urls: list[ChannelUrlData | dict[str, Any]],
    ) -> CreateLinkResult:
        """Create one or more channel tracking links.

        Args:
            channel_urls: List of channel link definitions to create

        Returns:
            CreateLinkResult with created/duplicated/failed counts and link details
        """
        items = [
            item if isinstance(item, ChannelUrlData) else ChannelUrlData(**item)
            for item in channel_urls
        ]
        payload = {
            "channel_urls": [
                item.model_dump(by_alias=True, exclude_none=True) for item in items
            ]
        }
        response = await self._transport.post(
            f"{self._base_url}/channel/links/create",
            json=payload,
        )
        data = response.json()
        raw = data.get("data", {})
        # channel_urls may be a list or a nested object with its own channel_urls list
        raw_urls = raw.get("channel_urls", [])
        if isinstance(raw_urls, dict):
            raw_urls = raw_urls.get("channel_urls", [])
        link_items = [CreatedLinkItem(**item) for item in raw_urls]
        return CreateLinkResult(
            created=raw.get("created"),
            duplicated=raw.get("duplicated"),
            failed=raw.get("failed"),
            status=raw.get("status"),
            channel_urls=link_items,
        )

    async def export_link(
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

        response = await self._transport.post(
            f"{self._base_url}/channel/link/{link_id}/export",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        return response.content
