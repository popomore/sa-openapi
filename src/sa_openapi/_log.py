"""Logging configuration for sa-openapi."""

from __future__ import annotations

import logging
import sys


def setup_logging(debug: bool = False) -> None:
    """Configure logging for sa-openapi.

    Args:
        debug: If True, set level to DEBUG and emit to stderr.
    """
    logger = logging.getLogger("sa_openapi")
    if debug:
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
            )
            logger.addHandler(handler)
    else:
        logger.setLevel(logging.WARNING)
        logger.handlers.clear()


def get_logger(name: str) -> logging.Logger:
    """Get a logger for the given module name."""
    return logging.getLogger(f"sa_openapi.{name}")
