"""Authentication handling for sa-openapi."""

from typing import Any


class AuthHandler:
    """Handle authentication for API requests."""

    def __init__(self, api_key: str, project: str):
        self.api_key = api_key
        self.project = project

    def get_headers(self) -> dict[str, str]:
        """Get authentication headers."""
        return {
            "api-key": self.api_key,
            "sensorsdata-project": self.project,
        }

    def inject_headers(self, headers: dict[str, Any]) -> dict[str, Any]:
        """Inject authentication headers into existing headers."""
        return {**headers, **self.get_headers()}
