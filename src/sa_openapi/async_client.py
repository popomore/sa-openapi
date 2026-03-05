"""Async client for sa-openapi."""

from __future__ import annotations

import asyncio
from typing import Any

import httpx
from typing_extensions import Self

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


class AsyncTransport:
    """Async HTTP transport."""

    def __init__(self, config: ClientConfig, auth: AuthHandler):
        self.config = config
        self.auth = auth
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(config.timeout),
            follow_redirects=True,
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make HTTP request with retry logic and error mapping."""
        headers = kwargs.pop("headers", {})
        headers = self.auth.inject_headers(headers)
        kwargs["headers"] = headers

        method_upper = method.upper()
        attempts = max(1, self.config.max_retries)
        retryable = method_upper in {"GET", "HEAD", "OPTIONS"}

        last_exception: Exception | None = None
        for attempt in range(attempts):
            try:
                response = await self._client.request(method_upper, url, **kwargs)
                return self._handle_response(response)
            except httpx.TimeoutException as e:
                last_exception = TimeoutError(str(e))
                if retryable and attempt < attempts - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                raise last_exception from e
            except httpx.NetworkError as e:
                last_exception = NetworkError(str(e))
                if retryable and attempt < attempts - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                raise last_exception from e

        raise last_exception if last_exception else NetworkError("Request failed")


    def _handle_response(self, response: httpx.Response) -> httpx.Response:
        """Handle HTTP response and map to exceptions (same contract as sync)."""
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
        except ValueError:
            pass

        return response

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """GET request."""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> httpx.Response:
        """POST request."""
        return await self.request("POST", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> httpx.Response:
        """DELETE request."""
        return await self.request("DELETE", url, **kwargs)


class AsyncDashboardService:
    """Async Dashboard service."""

    def __init__(self, transport: AsyncTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_base_url

    async def list_navigation(self, type: str = "PRIVATE"):
        """Get navigation list."""
        response = await self._transport.get(
            f"{self._base_url}/dashboard/navigation",
            params={"type": type},
        )
        data = response.json()
        from .models.dashboard import Navigation

        return [Navigation(**item) for item in data.get("data", [])]


class AsyncChannelService:
    """Async Channel service."""

    def __init__(self, transport: AsyncTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_base_url

    async def list_channel(self):
        """Get channel list."""
        response = await self._transport.get(f"{self._base_url}/channel")
        data = response.json()
        from .models.channel import Channel

        return [Channel(**item) for item in data.get("data", [])]


class AsyncDatasetService:
    """Async Dataset service."""

    def __init__(self, transport: AsyncTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_base_url

    async def list_dataset(self):
        """Get dataset list."""
        response = await self._transport.get(f"{self._base_url}/dataset")
        data = response.json()
        from .models.dataset import Dataset

        return [Dataset(**item) for item in data.get("data", [])]


class AsyncModelService:
    """Async Model service."""

    def __init__(self, transport: AsyncTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.model_base_url


class AsyncSensorsAnalyticsClient:
    """Async client for Sensors Analytics API."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        project: str = "default",
        *,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.config = ClientConfig(
            base_url=base_url,
            api_key=api_key,
            project=project,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._auth = AuthHandler(api_key, project)
        self._transport = AsyncTransport(self.config, self._auth)

        # Initialize services
        self.dashboard = AsyncDashboardService(self._transport, self._auth)
        self.channel = AsyncChannelService(self._transport, self._auth)
        self.dataset = AsyncDatasetService(self._transport, self._auth)
        self.model = AsyncModelService(self._transport, self._auth)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the client."""
        await self._transport.close()
