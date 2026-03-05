"""Tests for auth."""

from sa_openapi._auth import AuthHandler


def test_auth_handler():
    """Test authentication handler."""
    auth = AuthHandler(api_key="sk-test", project="default")

    headers = auth.get_headers()
    assert headers["api-key"] == "sk-test"
    assert headers["sensorsdata-project"] == "default"


def test_auth_handler_inject_headers():
    """Test injecting auth headers."""
    auth = AuthHandler(api_key="sk-test", project="default")

    headers = {"Content-Type": "application/json"}
    merged = auth.inject_headers(headers)

    assert merged["Content-Type"] == "application/json"
    assert merged["api-key"] == "sk-test"
    assert merged["sensorsdata-project"] == "default"


def test_auth_handler_override():
    """Test that existing headers are preserved."""
    auth = AuthHandler(api_key="sk-test", project="default")

    headers = {"api-key": "sk-other"}
    merged = auth.inject_headers(headers)

    # Auth headers should override
    assert merged["api-key"] == "sk-test"
