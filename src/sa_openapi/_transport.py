"""HTTP transport layer for sa-openapi."""

from __future__ import annotations

import time
from typing import Any

import httpx

from ._auth import AuthHandler
from ._config import ClientConfig
from ._exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)


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

        # Retry logic
        last_exception: Exception | None = None
        for attempt in range(self.config.max_retries):
            try:
                response = self._client.request(method, url, **kwargs)
                return self._handle_response(response)
            except httpx.TimeoutException as e:
                last_exception = TimeoutError(str(e))
                if attempt < self.config.max_retries - 1:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
            except httpx.NetworkError as e:
                last_exception = NetworkError(str(e))
                if attempt < self.config.max_retries - 1:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
            except httpx.HTTPStatusError as e:
                # Don't retry on HTTP errors
                raise self._handle_response(e.response)

        raise last_exception or NetworkError("Request failed")

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
