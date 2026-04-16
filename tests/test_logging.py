"""Tests for logging helpers."""

import logging

import pytest

from sa_openapi._log import get_logger, setup_logging


@pytest.fixture(autouse=True)
def reset_sa_logger():
    """Restore the shared package logger after each test."""
    logger = logging.getLogger("sa_openapi")
    original_level = logger.level
    original_handlers = list(logger.handlers)
    logger.handlers.clear()

    try:
        yield logger
    finally:
        logger.handlers.clear()
        for handler in original_handlers:
            logger.addHandler(handler)
        logger.setLevel(original_level)


def test_setup_logging_debug_is_idempotent(reset_sa_logger):
    """Test debug logging setup only adds one handler."""
    setup_logging(debug=True)
    assert reset_sa_logger.level == logging.DEBUG
    assert len(reset_sa_logger.handlers) == 1

    setup_logging(debug=True)
    assert reset_sa_logger.level == logging.DEBUG
    assert len(reset_sa_logger.handlers) == 1


def test_setup_logging_warning_clears_handlers(reset_sa_logger):
    """Test non-debug logging removes handlers."""
    setup_logging(debug=True)
    setup_logging(debug=False)

    assert reset_sa_logger.level == logging.WARNING
    assert reset_sa_logger.handlers == []


def test_get_logger_prefixes_package_name():
    """Test module logger naming."""
    logger = get_logger("services.dashboard")
    assert logger.name == "sa_openapi.services.dashboard"
