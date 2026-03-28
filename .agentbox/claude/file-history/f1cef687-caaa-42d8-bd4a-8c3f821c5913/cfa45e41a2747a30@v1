"""Version class with semantic versioning logic."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .exceptions import VersionParseError


VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


@dataclass(frozen=True)
class Version:
    """Represents a semantic version (major.minor.patch)."""

    major: int
    minor: int
    patch: int

    def __post_init__(self) -> None:
        """Validate version components are non-negative."""
        if self.major < 0 or self.minor < 0 or self.patch < 0:
            raise ValueError("Version components must be non-negative integers")

    def __str__(self) -> str:
        """Return version as 'X.Y.Z' string."""
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def from_string(cls, version_string: str) -> Version:
        """Parse a version string into a Version object.

        Args:
            version_string: A semantic version string (e.g., "1.2.3")

        Returns:
            A Version object

        Raises:
            VersionParseError: If the string is not a valid semantic version
        """
        match = VERSION_PATTERN.match(version_string.strip())
        if not match:
            raise VersionParseError(version_string)

        return cls(
            major=int(match.group(1)),
            minor=int(match.group(2)),
            patch=int(match.group(3)),
        )

    @classmethod
    def parse(cls, version_string: str) -> Version:
        """Alias for from_string() for convenience."""
        return cls.from_string(version_string)

    def bump_major(self) -> Version:
        """Return a new Version with major incremented and minor/patch reset to 0."""
        return Version(major=self.major + 1, minor=0, patch=0)

    def bump_minor(self) -> Version:
        """Return a new Version with minor incremented and patch reset to 0."""
        return Version(major=self.major, minor=self.minor + 1, patch=0)

    def bump_patch(self) -> Version:
        """Return a new Version with patch incremented."""
        return Version(major=self.major, minor=self.minor, patch=self.patch + 1)
