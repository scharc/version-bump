"""Custom exceptions for version-bump."""

from __future__ import annotations


class VersionBumpError(Exception):
    """Base exception for version-bump errors."""

    pass


class VersionParseError(VersionBumpError):
    """Raised when a version string cannot be parsed."""

    def __init__(self, version_string: str, message: str | None = None) -> None:
        self.version_string = version_string
        if message is None:
            message = f"Invalid version format: '{version_string}'. Expected semantic versioning (e.g., 1.0.0)."
        super().__init__(message)


class FileUpdateError(VersionBumpError):
    """Raised when a file cannot be updated."""

    def __init__(self, filename: str, reason: str) -> None:
        self.filename = filename
        self.reason = reason
        super().__init__(f"Failed to update '{filename}': {reason}")


class GitOperationError(VersionBumpError):
    """Raised when a git operation fails."""

    def __init__(self, operation: str, reason: str) -> None:
        self.operation = operation
        self.reason = reason
        super().__init__(f"Git {operation} failed: {reason}")
