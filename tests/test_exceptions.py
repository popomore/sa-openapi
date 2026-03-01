"""Tests for exceptions."""

import pytest

from sa_openapi._exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)


def test_sensors_analytics_error():
    """Test base exception."""
    from sa_openapi._exceptions import SensorsAnalyticsError

    err = SensorsAnalyticsError("test message", "TEST_CODE")
    assert err.message == "test message"
    assert err.code == "TEST_CODE"


def test_authentication_error():
    """Test authentication error."""
    err = AuthenticationError()
    assert err.code == "AUTH_ERROR"
    assert "Authentication" in err.message


def test_not_found_error():
    """Test not found error."""
    err = NotFoundError()
    assert err.code == "NOT_FOUND"
    assert "not found" in err.message.lower()


def test_validation_error():
    """Test validation error."""
    err = ValidationError()
    assert err.code == "VALIDATION_ERROR"


def test_rate_limit_error():
    """Test rate limit error."""
    err = RateLimitError()
    assert err.code == "RATE_LIMIT_ERROR"


def test_server_error():
    """Test server error."""
    err = ServerError()
    assert err.code == "SERVER_ERROR"


def test_timeout_error():
    """Test timeout error."""
    err = TimeoutError()
    assert err.code == "TIMEOUT_ERROR"
