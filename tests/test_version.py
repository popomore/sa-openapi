"""Tests for package version metadata."""

import importlib
import importlib.metadata
from importlib.metadata import version

import sa_openapi


def test_exported_version_matches_installed_package_metadata():
    """The exported package version should match installed distribution metadata."""
    assert sa_openapi.__version__ == version("sa-openapi")


def test_exported_version_falls_back_when_package_metadata_is_missing(monkeypatch):
    """The exported version should fall back when package metadata is unavailable."""

    def raise_package_not_found(_: str) -> str:
        raise importlib.metadata.PackageNotFoundError()

    with monkeypatch.context() as patch:
        patch.setattr(importlib.metadata, "version", raise_package_not_found)
        importlib.reload(sa_openapi)
        assert sa_openapi.__version__ == "0.0.0"

    importlib.reload(sa_openapi)
