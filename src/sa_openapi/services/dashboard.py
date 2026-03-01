"""Dashboard service implementation."""

from typing import Any

from .._auth import AuthHandler
from .._transport import Transport
from ..models.common import BookmarkData
from ..models.dashboard import (
    Bookmark,
    BookmarkDataParams,
    BookmarkExportParams,
    Navigation,
)


class DashboardService:
    """Dashboard service for Sensors Analytics."""

    def __init__(self, transport: Transport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_base_url

    def list_navigation(self, type: str = "PRIVATE") -> list[Navigation]:
        """Get navigation list.

        Args:
            type: Navigation type (PRIVATE or PUBLIC)

        Returns:
            List of navigation items
        """
        response = self._transport.get(
            f"{self._base_url}/dashboard/navigation",
            params={"type": type},
        )
        data = response.json()
        return [Navigation(**item) for item in data.get("data", [])]

    def get_navigation(self, navigation_id: int) -> Navigation:
        """Get specific navigation.

        Args:
            navigation_id: Navigation ID

        Returns:
            Navigation details
        """
        response = self._transport.get(
            f"{self._base_url}/dashboard/navigation/{navigation_id}",
        )
        data = response.json()
        return Navigation(**data.get("data", {}))

    def list_bookmark(self, navigation_id: int) -> list[Bookmark]:
        """Get bookmark list for a navigation.

        Args:
            navigation_id: Navigation ID

        Returns:
            List of bookmarks
        """
        response = self._transport.get(
            f"{self._base_url}/dashboard/bookmark",
            params={"navigation_id": navigation_id},
        )
        data = response.json()
        return [Bookmark(**item) for item in data.get("data", [])]

    def get_bookmark(self, bookmark_id: int) -> Bookmark:
        """Get specific bookmark.

        Args:
            bookmark_id: Bookmark ID

        Returns:
            Bookmark details
        """
        response = self._transport.get(
            f"{self._base_url}/dashboard/bookmark/{bookmark_id}",
        )
        data = response.json()
        return Bookmark(**data.get("data", {}))

    def get_bookmark_data(
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

        response = self._transport.post(
            f"{self._base_url}/dashboard/bookmark/{bookmark_id}/data",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        data = response.json()
        return BookmarkData(**data.get("data", {}))

    def export_bookmark(
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

        response = self._transport.post(
            f"{self._base_url}/dashboard/bookmark/{bookmark_id}/export",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        return response.content
