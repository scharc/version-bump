"""Handler for composer.json version updates (PHP)."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


class ComposerHandler(FileHandler):
    """Handler for composer.json files (PHP projects)."""

    filename = "composer.json"

    def read_version(self) -> Version | None:
        """Read the version from composer.json."""
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
        """Write the version to composer.json."""
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")
            data = json.loads(content)

            # Only update if version field exists or we're adding it
            data["version"] = str(version)
            updated_content = json.dumps(data, indent=4) + "\n"
            self.file_path.write_text(updated_content, encoding="utf-8")
            return True
        except (OSError, json.JSONDecodeError) as e:
            raise FileUpdateError(self.filename, str(e)) from e
