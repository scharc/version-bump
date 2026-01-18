"""Handler for version.txt and VERSION file updates (Generic)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


# Match semantic version at start of file
VERSION_PATTERN = re.compile(r'^v?(\d+\.\d+\.\d+)', re.MULTILINE)


class VersionTxtHandler(FileHandler):
    """Handler for version.txt files."""

    filename = "version.txt"

    def read_version(self) -> Version | None:
        """Read the version from version.txt."""
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8").strip()
            # Remove 'v' prefix if present
            if content.startswith('v'):
                content = content[1:]
            from ..version import Version
            return Version.from_string(content.split()[0])  # Take first word
        except (OSError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Write the version to version.txt."""
        if not self.exists():
            return False

        try:
            self.file_path.write_text(f"{version}\n", encoding="utf-8")
            return True
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e


class VersionFileHandler(FileHandler):
    """Handler for VERSION files (no extension)."""

    filename = "VERSION"

    def read_version(self) -> Version | None:
        """Read the version from VERSION file."""
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8").strip()
            if content.startswith('v'):
                content = content[1:]
            from ..version import Version
            return Version.from_string(content.split()[0])
        except (OSError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Write the version to VERSION file."""
        if not self.exists():
            return False

        try:
            self.file_path.write_text(f"{version}\n", encoding="utf-8")
            return True
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e
