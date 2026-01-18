"""Version-bump: A semantic versioning tool."""

from __future__ import annotations

try:
    from importlib.metadata import version

    __version__ = version("version-bump")
except Exception:
    __version__ = "unknown"

from .exceptions import (
    FileUpdateError,
    GitOperationError,
    VersionBumpError,
    VersionParseError,
)
from .version import Version

__all__ = [
    "__version__",
    "FileUpdateError",
    "GitOperationError",
    "Version",
    "VersionBumpError",
    "VersionParseError",
]
