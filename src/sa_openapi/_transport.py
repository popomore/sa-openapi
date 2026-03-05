"""HTTP transport layer for sa-openapi."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

import httpx

from ._exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)

if TYPE_CHECKING:
    from ._auth import AuthHandler
    from ._config import ClientConfig


class Transport:
    """HTTP transport with retry logic."""

    def __init__(self, config: ClientConfig, auth: AuthHandler):
        self.config = config
        self.auth = auth
        self._client = httpx.Client(
            timeout=httpx.Timeout(config.timeout),
            follow_redirects=True,
        )

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        # Inject auth headers
        headers = kwargs.pop("headers", {})
        headers = self.auth.inject_headers(headers)
        kwargs["headers"] = headers

        method_upper = method.upper()
        # Always attempt at least once. Treat max_retries as total attempts.
        attempts = max(1, self.config.max_retries)
        retryable = method_upper in {"GET", "HEAD", "OPTIONS"}

        last_exception: Exception | None = None
        for attempt in range(attempts):
            try:
                response = self._client.request(method_upper, url, **kwargs)
                return self._handle_response(response)
            except httpx.TimeoutException as e:
                last_exception = TimeoutError(str(e))
                if retryable and attempt < attempts - 1:
                    time.sleep(2**attempt)
                    continue
                raise last_exception from e
            except httpx.NetworkError as e:
                last_exception = NetworkError(str(e))
                if retryable and attempt < attempts - 1:
                    time.sleep(2**attempt)
                    continue
                raise last_exception from e
            except httpx.HTTPStatusError as e:
                # Don't retry on HTTP errors
                return self._handle_response(e.response)

        # Should be unreachable due to raises above, but keep a safe fallback.
        raise last_exception if last_exception else NetworkError("Request failed")

    def _handle_response(self, response: httpx.Response) -> httpx.Response:
        """Handle HTTP response and map to exceptions."""
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        if response.status_code == 403:
            raise AuthenticationError("Access forbidden")
        if response.status_code == 404:
            raise NotFoundError("Resource not found")
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        if response.status_code >= 500:
            raise ServerError(f"Server error: {response.status_code}")

        # Check API response code
        try:
            data = response.json()
            if isinstance(data, dict):
                code = data.get("code", "SUCCESS")
                if code != "SUCCESS":
                    message = data.get("message", "API error")
                    error_info = data.get("error_info", {})
                    error_code = error_info.get("code", code) if isinstance(error_info, dict) else code

                    if error_code == "VALIDATION_ERROR":
                        raise ValidationError(message)
                    if error_code == "AUTH_ERROR":
                        raise AuthenticationError(message)
                    if error_code == "NOT_FOUND":
                        raise NotFoundError(message)
                    if error_code == "RATE_LIMIT_ERROR":
                        raise RateLimitError(message)
                    if error_code == "TIMEOUT_ERROR":
                        raise TimeoutError(message)
                    raise ServerError(f"{error_code}: {message}")
        except (ValueError, httpx.HTTPStatusError):
            pass

        return response

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """GET request."""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> httpx.Response:
        """POST request."""
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> httpx.Response:
        """PUT request."""
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> httpx.Response:
        """DELETE request."""
        return self.request("DELETE", url, **kwargs)
