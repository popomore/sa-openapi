"""Async HTTP transport using aiohttp."""

from __future__ import annotations

import asyncio
import json as json_module
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import aiohttp

from ._exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)
from ._log import get_logger

if TYPE_CHECKING:
    from ._auth import AuthHandler
    from ._config import ClientConfig

logger = get_logger("_transport")


@dataclass
class Response:
    """Unified response wrapper compatible with service layer."""

    _data: Any
    content: bytes
    status_code: int

    def json(self) -> Any:
        """Return parsed JSON data."""
        return self._data


class AiohttpTransport:
    """Async HTTP transport backed by aiohttp."""

    def __init__(self, config: ClientConfig, auth: AuthHandler):
        self.config = config
        self.auth = auth
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def close(self) -> None:
        """Close the underlying aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> Response:
        """Make an HTTP request with retry logic."""
        headers = kwargs.pop("headers", {})
        headers = self.auth.inject_headers(headers)
        kwargs["headers"] = headers

        method_upper = method.upper()
        attempts = max(1, self.config.max_retries)
        retryable = method_upper in {"GET", "HEAD", "OPTIONS"}

        session = await self._get_session()
        last_exception: Exception | None = None

        for attempt in range(attempts):
            try:
                logger.debug("HTTP %s %s (attempt %d/%d)", method_upper, url, attempt + 1, attempts)
                async with session.request(method_upper, url, **kwargs) as resp:
                    logger.debug("HTTP response %d %s", resp.status, url)
                    return await self._handle_response(resp)
            except aiohttp.ClientConnectionError as e:
                last_exception = NetworkError(str(e))
                if retryable and attempt < attempts - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                raise last_exception from e
            except asyncio.TimeoutError as e:
                last_exception = TimeoutError(str(e))
                if retryable and attempt < attempts - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                raise last_exception from e

        raise last_exception if last_exception else NetworkError("Request failed")

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Response:
        """Parse response and map HTTP/API errors to exceptions."""
        content = await response.read()
        status = response.status

        if status == 401:
            raise AuthenticationError("Invalid API key")
        if status == 403:
            raise AuthenticationError("Access forbidden")
        if status == 404:
            raise NotFoundError("Resource not found")
        if status == 429:
            raise RateLimitError("Rate limit exceeded")
        if status >= 500:
            detail = ""
            try:
                body = json_module.loads(content)
                if isinstance(body, dict):
                    detail = f" | {json_module.dumps(body, ensure_ascii=False)[:800]}"
                elif content:
                    detail = f" | {content.decode(errors='replace')[:500]}"
            except Exception:
                if content:
                    detail = f" | {content.decode(errors='replace')[:500]}"
            raise ServerError(f"Server error: {status}{detail}")

        data: Any = None
        try:
            data = json_module.loads(content)
            if isinstance(data, dict):
                code = data.get("code", "SUCCESS")
                if code != "SUCCESS":
                    message = data.get("message", "API error")
                    error_info = data.get("error_info", {})
                    error_code = (
                        error_info.get("code", code) if isinstance(error_info, dict) else code
                    )

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
        except (ValueError, UnicodeDecodeError):
            pass

        return Response(_data=data, content=content, status_code=status)

    async def get(self, url: str, **kwargs: Any) -> Response:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> Response:
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> Response:
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Response:
        return await self.request("DELETE", url, **kwargs)


# Alias for backward compatibility
Transport = AiohttpTransport
