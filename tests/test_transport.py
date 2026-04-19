"""Tests for the aiohttp transport layer."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, call

import aiohttp
import pytest

from sa_openapi._auth import AuthHandler
from sa_openapi._config import ClientConfig
from sa_openapi._exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from sa_openapi._exceptions import (
    TimeoutError as RequestTimeoutError,
)
from sa_openapi._transport import AiohttpTransport, Response

pytestmark = pytest.mark.asyncio


class FakeClientResponse:
    """Small aiohttp-like response object for transport tests."""

    def __init__(self, status: int, content: bytes):
        self.status = status
        self._content = content

    async def read(self) -> bytes:
        return self._content


class FakeRequestContext:
    """Async context manager returned by the fake session."""

    def __init__(self, outcome):
        self._outcome = outcome

    async def __aenter__(self):
        if isinstance(self._outcome, BaseException):
            raise self._outcome
        return self._outcome

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        return False


class FakeSession:
    """Minimal request-recording session stub."""

    def __init__(self, outcomes: list[object]):
        self.outcomes = list(outcomes)
        self.calls: list[dict[str, object]] = []
        self.closed = False

    def request(self, method: str, url: str, **kwargs):
        self.calls.append({"method": method, "url": url, "kwargs": kwargs})
        if not self.outcomes:
            raise AssertionError("No more fake outcomes configured")
        return FakeRequestContext(self.outcomes.pop(0))

    async def close(self) -> None:
        self.closed = True


def make_config(*, timeout: float = 30.0, max_retries: int = 3) -> ClientConfig:
    return ClientConfig(
        base_url="https://example.sensorsdata.cn",
        api_key="sk-test",
        project="default",
        timeout=timeout,
        max_retries=max_retries,
    )


def make_transport(*, timeout: float = 30.0, max_retries: int = 3) -> AiohttpTransport:
    return AiohttpTransport(make_config(timeout=timeout, max_retries=max_retries), make_auth())


def make_auth() -> AuthHandler:
    return AuthHandler(api_key="sk-test", project="default")


async def test_response_json_returns_wrapped_data():
    """Test the lightweight response wrapper."""
    response = Response(_data={"ok": True}, content=b"{}", status_code=200)
    assert response.json() == {"ok": True}


async def test_get_session_creates_reuses_and_reopens_session(monkeypatch):
    """Test session lifecycle and timeout wiring."""
    created_sessions = []

    class FakeClientSession:
        def __init__(self, timeout):
            self.timeout = timeout
            self.closed = False
            created_sessions.append(self)

        async def close(self) -> None:
            self.closed = True

    monkeypatch.setattr("sa_openapi._transport.aiohttp.ClientSession", FakeClientSession)
    transport = make_transport(timeout=12.5)

    first = await transport._get_session()
    second = await transport._get_session()

    assert first is second
    assert first.timeout.total == 12.5

    first.closed = True
    third = await transport._get_session()

    assert third is not first
    assert len(created_sessions) == 2


async def test_close_only_closes_open_session():
    """Test transport close respects session state."""
    transport = make_transport()
    open_session = SimpleNamespace(closed=False)
    open_session.close = AsyncMock(side_effect=lambda: setattr(open_session, "closed", True))
    transport._session = open_session

    await transport.close()
    open_session.close.assert_awaited_once()

    closed_session = SimpleNamespace(closed=True)
    closed_session.close = AsyncMock()
    transport._session = closed_session

    await transport.close()
    closed_session.close.assert_not_awaited()


async def test_request_uppercases_method_injects_headers_and_handles_response():
    """Test a successful request path."""
    transport = make_transport()
    session = FakeSession([FakeClientResponse(200, b'{"data": {"value": 1}}')])
    transport._get_session = AsyncMock(return_value=session)
    expected = Response(_data={"data": {"value": 1}}, content=b"{}", status_code=200)
    transport._handle_response = AsyncMock(return_value=expected)

    result = await transport.request(
        "get",
        "https://example.sensorsdata.cn/api/test",
        headers={"X-Test": "1"},
        params={"page": 2},
    )

    assert result is expected
    assert session.calls == [
        {
            "method": "GET",
            "url": "https://example.sensorsdata.cn/api/test",
            "kwargs": {
                "headers": {
                    "X-Test": "1",
                    "api-key": "sk-test",
                    "sensorsdata-project": "default",
                },
                "params": {"page": 2},
            },
        }
    ]
    transport._handle_response.assert_awaited_once()


async def test_request_retries_retryable_connection_errors(monkeypatch):
    """Test GET retries on connection failures."""
    transport = make_transport(max_retries=2)
    session = FakeSession(
        [
            aiohttp.ClientConnectionError("boom"),
            FakeClientResponse(200, b'{"data": {"ok": true}}'),
        ]
    )
    transport._get_session = AsyncMock(return_value=session)
    sleep = AsyncMock()
    monkeypatch.setattr("sa_openapi._transport.asyncio.sleep", sleep)

    result = await transport.request("GET", "https://example.sensorsdata.cn/api/test")

    assert result.json() == {"data": {"ok": True}}
    assert len(session.calls) == 2
    sleep.assert_awaited_once_with(1)


async def test_request_does_not_retry_non_retryable_connection_errors(monkeypatch):
    """Test POST does not retry network errors."""
    transport = make_transport(max_retries=3)
    session = FakeSession([aiohttp.ClientConnectionError("post failed")])
    transport._get_session = AsyncMock(return_value=session)
    sleep = AsyncMock()
    monkeypatch.setattr("sa_openapi._transport.asyncio.sleep", sleep)

    with pytest.raises(NetworkError, match="post failed"):
        await transport.request("POST", "https://example.sensorsdata.cn/api/test")

    assert len(session.calls) == 1
    sleep.assert_not_awaited()


async def test_request_retries_timeout_errors_and_raises_last_failure(monkeypatch):
    """Test timeout retry behavior for retryable methods."""
    transport = make_transport(max_retries=2)
    session = FakeSession([asyncio.TimeoutError("slow"), asyncio.TimeoutError("still slow")])
    transport._get_session = AsyncMock(return_value=session)
    sleep = AsyncMock()
    monkeypatch.setattr("sa_openapi._transport.asyncio.sleep", sleep)

    with pytest.raises(RequestTimeoutError, match="still slow"):
        await transport.request("HEAD", "https://example.sensorsdata.cn/api/test")

    assert len(session.calls) == 2
    sleep.assert_awaited_once_with(1)


async def test_request_raises_generic_network_error_when_retry_loop_never_runs():
    """Test the defensive fallback when retries resolve to zero iterations."""

    class ZeroRetryCount:
        def __gt__(self, other: object) -> bool:
            return True

        def __lt__(self, other: object) -> bool:
            return False

        def __index__(self) -> int:
            return 0

    transport = make_transport()
    transport.config.max_retries = ZeroRetryCount()  # type: ignore[assignment]
    transport._get_session = AsyncMock(return_value=FakeSession([]))

    with pytest.raises(NetworkError, match="Request failed"):
        await transport.request("GET", "https://example.sensorsdata.cn/api/test")


@pytest.mark.parametrize(
    ("status", "error_type", "message"),
    [
        (401, AuthenticationError, "Invalid API key"),
        (403, AuthenticationError, "Access forbidden"),
        (404, NotFoundError, "Resource not found"),
        (429, RateLimitError, "Rate limit exceeded"),
    ],
)
async def test_handle_response_maps_http_client_errors(status, error_type, message):
    """Test direct HTTP status to exception mapping."""
    transport = make_transport()

    with pytest.raises(error_type, match=message):
        await transport._handle_response(FakeClientResponse(status, b"{}"))


async def test_handle_response_includes_json_detail_for_server_errors():
    """Test server error JSON bodies are surfaced in the exception."""
    transport = make_transport()
    content = json.dumps({"error": "bad gateway", "retry": False}).encode("utf-8")

    with pytest.raises(ServerError, match="Server error: 500") as exc_info:
        await transport._handle_response(FakeClientResponse(500, content))

    assert '"error": "bad gateway"' in str(exc_info.value)


async def test_handle_response_includes_non_dict_json_detail_for_server_errors():
    """Test server error JSON arrays fall back to decoded content."""
    transport = make_transport()

    with pytest.raises(ServerError, match=r"\[1, 2, 3\]"):
        await transport._handle_response(FakeClientResponse(503, b"[1, 2, 3]"))


async def test_handle_response_includes_plain_text_detail_for_server_errors():
    """Test server error plain-text bodies are surfaced in the exception."""
    transport = make_transport()

    with pytest.raises(ServerError, match="upstream unavailable"):
        await transport._handle_response(FakeClientResponse(502, b"upstream unavailable"))


@pytest.mark.parametrize(
    ("payload", "error_type", "message"),
    [
        (
            {"code": "FAIL", "message": "bad input", "error_info": {"code": "VALIDATION_ERROR"}},
            ValidationError,
            "bad input",
        ),
        (
            {"code": "AUTH_ERROR", "message": "auth denied", "error_info": "raw"},
            AuthenticationError,
            "auth denied",
        ),
        (
            {"code": "NOT_FOUND", "message": "gone"},
            NotFoundError,
            "gone",
        ),
        (
            {"code": "RATE_LIMIT_ERROR", "message": "slow down"},
            RateLimitError,
            "slow down",
        ),
        (
            {"code": "TIMEOUT_ERROR", "message": "deadline"},
            RequestTimeoutError,
            "deadline",
        ),
        (
            {"code": "UNKNOWN", "message": "explode"},
            ServerError,
            "UNKNOWN: explode",
        ),
    ],
)
async def test_handle_response_maps_api_error_codes(payload, error_type, message):
    """Test API-level error payloads are mapped consistently."""
    transport = make_transport()

    with pytest.raises(error_type, match=message):
        await transport._handle_response(
            FakeClientResponse(200, json.dumps(payload).encode("utf-8"))
        )


async def test_handle_response_returns_raw_content_for_non_json_body():
    """Test successful non-JSON payloads remain accessible."""
    transport = make_transport()

    result = await transport._handle_response(FakeClientResponse(200, b"not-json"))

    assert result.json() is None
    assert result.content == b"not-json"
    assert result.status_code == 200


async def test_handle_response_returns_non_dict_json_payloads():
    """Test list JSON payloads are preserved without API error handling."""
    transport = make_transport()

    result = await transport._handle_response(FakeClientResponse(200, b'[{"id": 1}]'))

    assert result.json() == [{"id": 1}]


async def test_http_verb_helpers_delegate_to_request():
    """Test convenience HTTP methods dispatch to request()."""
    transport = make_transport()
    expected = Response(_data={"ok": True}, content=b"{}", status_code=200)
    transport.request = AsyncMock(return_value=expected)

    assert await transport.get("https://example/get", params={"q": "1"}) is expected
    assert await transport.post("https://example/post", json={"x": 1}) is expected
    assert await transport.put("https://example/put", json={"x": 2}) is expected
    assert await transport.delete("https://example/delete") is expected
    assert transport.request.await_args_list == [
        call("GET", "https://example/get", params={"q": "1"}),
        call("POST", "https://example/post", json={"x": 1}),
        call("PUT", "https://example/put", json={"x": 2}),
        call("DELETE", "https://example/delete"),
    ]
