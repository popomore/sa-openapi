"""Response handling for sa-openapi."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    import httpx

T = TypeVar("T")


@dataclass
class HttpApiResult(Generic[T]):
    """Wrapper for API response with data."""

    data: T
    request_id: str | None = None
    code: str = "SUCCESS"
    message: str | None = None


@dataclass
class ErrorInfo:
    """Error information from API response."""

    code: str
    message: str


@dataclass
class Pagination:
    """Pagination information."""

    page: int
    page_size: int
    total: int
    total_pages: int

    @property
    def has_next(self) -> bool:
        """Check if there is a next page."""
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        """Check if there is a previous page."""
        return self.page > 1


def unwrap_response(response: httpx.Response) -> Any:
    """Unwrap API response and extract data field.

    Args:
        response: HTTP response from API

    Returns:
        The data field from API response

    Raises:
        SensorsAnalyticsError: If API returns error
    """
    data = response.json()

    # Handle list response
    if isinstance(data, list):
        return data

    # Handle object response
    if isinstance(data, dict):
        code = data.get("code", "SUCCESS")
        if code != "SUCCESS":
            message = data.get("message", "API error")
            error_info = data.get("error_info")

            if error_info and isinstance(error_info, dict):
                error_code = error_info.get("code", code)
                error_message = error_info.get("message", message)
            else:
                error_code = code
                error_message = message

            # Import here to avoid circular import
            from ._exceptions import (
                AuthenticationError,
                NotFoundError,
                RateLimitError,
                ServerError,
                TimeoutError,
                ValidationError,
            )

            error_map = {
                "VALIDATION_ERROR": ValidationError,
                "NOT_FOUND": NotFoundError,
                "AUTH_ERROR": AuthenticationError,
                "RATE_LIMIT_ERROR": RateLimitError,
                "TIMEOUT_ERROR": TimeoutError,
            }

            exc_class = error_map.get(error_code, ServerError)
            raise exc_class(error_message)

        return data.get("data")

    return data
