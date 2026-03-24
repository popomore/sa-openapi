"""Channel service implementation."""

from typing import Any

from .._auth import AuthHandler
from .._transport import AiohttpTransport
from ..models.channel import (
    CampaignListResponse,
    ChannelLinkListResponse,
    ChannelUrlData,
    CreatedLinkItem,
    CreateLinkResult,
)


class ChannelServiceV1:
    """Channel service for Sensors Analytics."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_v1_base_url

    async def list_campaigns(
        self,
        page_num: int = 1,
        page_size: int = 20,
    ) -> CampaignListResponse:
        """Get campaign list.

        Args:
            page_num: Page number (1-based)
            page_size: Page size

        Returns:
            Campaign list response
        """
        response = await self._transport.post(
            f"{self._base_url}/channel/campaigns/list",
            json={"page_num": page_num, "page_size": page_size},
        )
        data = response.json()
        return CampaignListResponse(**data.get("data", {}))

    async def list_links(
        self,
        page_num: int = 1,
        page_size: int = 20,
    ) -> ChannelLinkListResponse:
        """Get channel link list.

        Args:
            page_num: Page number (1-based)
            page_size: Page size

        Returns:
            Channel link list response
        """
        response = await self._transport.post(
            f"{self._base_url}/channel/links/list",
            json={"page_num": page_num, "page_size": page_size},
        )
        data = response.json()
        return ChannelLinkListResponse(**data.get("data", {}))

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
            "channel_urls": [item.model_dump(by_alias=True, exclude_none=True) for item in items]
        }
        response = await self._transport.post(
            f"{self._base_url}/channel/links/create",
            json=payload,
        )
        data = response.json()
        raw = data.get("data", {})
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
