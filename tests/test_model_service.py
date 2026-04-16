"""Tests for ModelServiceV1.sql_query NDJSON parsing."""

import json
from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock

import pytest

from sa_openapi.services.model import ModelServiceV1


@dataclass
class FakeResponse:
    content: bytes
    _data: Any = None
    status_code: int = 200


def _ndjson(*lines: dict) -> bytes:
    return "\n".join(json.dumps(line) for line in lines).encode()


def _make_service() -> ModelServiceV1:
    transport = AsyncMock()
    auth = AsyncMock()
    transport.config.model_v1_base_url = "http://fake"
    service = ModelServiceV1(transport, auth)
    return service


@pytest.mark.asyncio
async def test_sql_query_extracts_columns():
    service = _make_service()
    service._transport.post.return_value = FakeResponse(
        content=_ndjson(
            {"code": "SUCCESS", "data": {"columns": ["name", "age"], "data": ["Alice", 30]}},
            {"code": "SUCCESS", "data": {"data": ["Bob", 25]}},
        )
    )
    result = await service.sql_query("SELECT name, age FROM users")
    assert result.columns == ["name", "age"]
    assert result.data == [["Alice", 30], ["Bob", 25]]


@pytest.mark.asyncio
async def test_sql_query_nested_data():
    service = _make_service()
    service._transport.post.return_value = FakeResponse(
        content=_ndjson(
            {
                "code": "SUCCESS",
                "data": {
                    "columns": ["x", "y"],
                    "data": [["a", 1], ["b", 2]],
                },
            },
        )
    )
    result = await service.sql_query("SELECT x, y FROM t")
    assert result.columns == ["x", "y"]
    assert result.data == [["a", 1], ["b", 2]]


@pytest.mark.asyncio
async def test_sql_query_no_columns():
    service = _make_service()
    service._transport.post.return_value = FakeResponse(
        content=_ndjson(
            {"code": "SUCCESS", "data": {"data": [1, 2]}},
            {"code": "SUCCESS", "data": {"data": [3, 4]}},
        )
    )
    result = await service.sql_query("SELECT 1, 2")
    assert result.columns is None
    assert result.data == [[1, 2], [3, 4]]


@pytest.mark.asyncio
async def test_sql_query_empty_response():
    service = _make_service()
    service._transport.post.return_value = FakeResponse(content=b"")
    result = await service.sql_query("SELECT 1")
    assert result.columns is None
    assert result.data is None


@pytest.mark.asyncio
async def test_sql_query_skips_non_success():
    service = _make_service()
    service._transport.post.return_value = FakeResponse(
        content=_ndjson(
            {"code": "SUCCESS", "data": {"columns": ["id"], "data": [1]}},
            {"code": "ERROR", "data": {"message": "fail"}},
            {"code": "SUCCESS", "data": {"data": [2]}},
        )
    )
    result = await service.sql_query("SELECT id FROM t")
    assert result.columns == ["id"]
    assert result.data == [[1], [2]]
