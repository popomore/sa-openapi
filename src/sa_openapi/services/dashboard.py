"""Dashboard service implementation."""

from .._auth import AuthHandler
from .._log import get_logger
from .._transport import AiohttpTransport
from ..models.dashboard import (
    Bookmark,
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
            candidate = raw_data.get("groups", raw_data.get("list", raw_data.get("items", [])))
            raw_items = candidate if isinstance(candidate, list) else []
        else:
            raw_items = raw_data if isinstance(raw_data, list) else []
        logger.debug("list_navigation raw_items len=%s", len(raw_items))
        if raw_items:
            logger.debug("list_navigation first item: %r", raw_items[0])
        return [Navigation(**item) for item in raw_items if isinstance(item, dict)]

    async def list_bookmarks(
        self,
        bookmark_type: str | None = None,
        has_widget: bool | None = None,
        has_lego: bool | None = None,
    ) -> list[Bookmark]:
        """Get all bookmarks.

        Args:
            bookmark_type: Filter by bookmark type
            has_widget: Filter by has_widget flag
            has_lego: Filter by has_lego flag

        Returns:
            List of bookmarks
        """
        params: dict = {}
        if bookmark_type is not None:
            params["type"] = bookmark_type
        if has_widget is not None:
            params["has_widget"] = has_widget
        if has_lego is not None:
            params["has_lego"] = has_lego

        response = await self._transport.get(
            f"{self._base_url}/dashboard/bookmarks",
            params=params or None,
        )
        data = response.json()
        raw = data.get("data", {})
        items = raw.get("bookmarks", []) if isinstance(raw, dict) else []
        return [Bookmark(**item) for item in items if isinstance(item, dict)]
