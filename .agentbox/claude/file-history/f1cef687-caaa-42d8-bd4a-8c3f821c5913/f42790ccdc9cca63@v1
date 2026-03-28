"""Handler for README.md version badge updates."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


# Pattern matches version badges like v1.2.3
VERSION_BADGE_PATTERN = re.compile(r"v(\d+\.\d+\.\d+)")


class ReadmeHandler(FileHandler):
    """Handler for README.md files."""

    filename = "README.md"

    def read_version(self) -> Version | None:
        """Read the first version badge from README.md.

        Returns:
            The Version object if found, None if not found or file doesn't exist.
        """
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8")
            match = VERSION_BADGE_PATTERN.search(content)
            if match:
                from ..version import Version
                return Version.from_string(match.group(1))
        except (OSError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Update all version badges in README.md.

        Args:
            version: The Version object to write.

        Returns:
            True if the file was updated successfully, False if file doesn't exist.

        Raises:
            FileUpdateError: If the file exists but cannot be updated.
        """
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")
            updated_content = VERSION_BADGE_PATTERN.sub(f"v{version}", content)
            self.file_path.write_text(updated_content, encoding="utf-8")
            return True
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e
