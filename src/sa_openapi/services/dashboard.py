"""Dashboard service implementation."""

from typing import Any

from .._auth import AuthHandler
from .._log import get_logger
from .._transport import AiohttpTransport
from ..models.common import BookmarkData
from ..models.dashboard import (
    Bookmark,
    BookmarkDataParams,
    BookmarkExportParams,
    Navigation,
)

logger = get_logger("services.dashboard")


class DashboardServiceV1:
    """Dashboard service for Sensors Analytics (v1 API)."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_v1_base_url

    async def list_navigation(self, nav_type: str = "PRIVATE") -> list[Navigation]:
        """Get navigation list.

        Args:
            nav_type: Navigation type (PRIVATE or PUBLIC)

        Returns:
            List of navigation items
        """
        response = await self._transport.get(
            f"{self._base_url}/dashboard/navigation",
            params={"type": nav_type},
        )
        data = response.json()
        raw_data = data.get("data", [])
        logger.debug(
            "list_navigation raw data type=%s, keys=%s",
            type(raw_data).__name__,
            raw_data.keys() if isinstance(raw_data, dict) else "N/A",
        )
        # API returns {"data": {"groups": [...], "type": "..."}}
        if isinstance(raw_data, dict):
            raw_items = raw_data.get("groups", raw_data.get("list", raw_data.get("items", [])))
        else:
            raw_items = raw_data if isinstance(raw_data, list) else []
        logger.debug("list_navigation raw_items len=%s", len(raw_items))
        if raw_items and isinstance(raw_items, list):
            logger.debug("list_navigation first item: %r", raw_items[0])
        return [Navigation(**item) for item in raw_items if isinstance(item, dict)]

    async def get_navigation(self, navigation_id: int) -> Navigation:
        """Get specific navigation.

        Args:
            navigation_id: Navigation ID

        Returns:
            Navigation details
        """
        response = await self._transport.get(
            f"{self._base_url}/dashboard/navigation/{navigation_id}",
        )
        data = response.json()
        return Navigation(**data.get("data", {}))

    async def list_bookmark(self, navigation_id: int) -> list[Bookmark]:
        """Get bookmark list for a navigation.

        Args:
            navigation_id: Navigation ID

        Returns:
            List of bookmarks
        """
        response = await self._transport.get(
            f"{self._base_url}/dashboard/bookmark",
            params={"navigation_id": navigation_id},
        )
        data = response.json()
        return [Bookmark(**item) for item in data.get("data", [])]

    async def get_bookmark(self, bookmark_id: int) -> Bookmark:
        """Get specific bookmark.

        Args:
            bookmark_id: Bookmark ID

        Returns:
            Bookmark details
        """
        response = await self._transport.get(
            f"{self._base_url}/dashboard/bookmark/{bookmark_id}",
        )
        data = response.json()
        return Bookmark(**data.get("data", {}))

    async def get_bookmark_data(
        self,
        bookmark_id: int,
        params: BookmarkDataParams | dict[str, Any],
    ) -> BookmarkData:
        """Get bookmark data.

        Args:
            bookmark_id: Bookmark ID
            params: Query parameters

        Returns:
            Bookmark data
        """
        if isinstance(params, dict):
            params = BookmarkDataParams(**params)

        response = await self._transport.post(
            f"{self._base_url}/dashboard/bookmark/{bookmark_id}/data",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        data = response.json()
        return BookmarkData(**data.get("data", {}))

    async def export_bookmark(
        self,
        bookmark_id: int,
        params: BookmarkExportParams | dict[str, Any],
    ) -> bytes:
        """Export bookmark data.

        Args:
            bookmark_id: Bookmark ID
            params: Export parameters

        Returns:
            Export file content (bytes)
        """
        if isinstance(params, dict):
            params = BookmarkExportParams(**params)

        response = await self._transport.post(
            f"{self._base_url}/dashboard/bookmark/{bookmark_id}/export",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        return response.content
