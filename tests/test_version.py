"""Tests for package version metadata."""

from importlib.metadata import version

import sa_openapi


def test_exported_version_matches_installed_package_metadata():
    """The exported package version should match installed distribution metadata."""
    assert sa_openapi.__version__ == version("sa-openapi")
