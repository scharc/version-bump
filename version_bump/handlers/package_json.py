"""Handler for package.json version updates."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


class PackageJsonHandler(FileHandler):
    """Handler for package.json files."""

    filename = "package.json"

    def read_version(self) -> Version | None:
        """Read the version from package.json.

        Returns:
            The Version object if found, None if not found or file doesn't exist.
        """
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8")
            data = json.loads(content)
            version_str = data.get("version")
            if version_str:
                from ..version import Version
                return Version.from_string(version_str)
        except (OSError, json.JSONDecodeError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Write the version to package.json.

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
            data = json.loads(content)
            data["version"] = str(version)
            updated_content = json.dumps(data, indent=2) + "\n"
            self.file_path.write_text(updated_content, encoding="utf-8")
            return True
        except (OSError, json.JSONDecodeError) as e:
            raise FileUpdateError(self.filename, str(e)) from e
