"""Handler for setup.cfg version updates (Python)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


# Match version = X.Y.Z in [metadata] section
VERSION_PATTERN = re.compile(r'^version\s*=\s*(.+)$', re.MULTILINE)


class SetupCfgHandler(FileHandler):
    """Handler for setup.cfg files (Python projects)."""

    filename = "setup.cfg"

    def read_version(self) -> Version | None:
        """Read the version from setup.cfg."""
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8")
            match = VERSION_PATTERN.search(content)
            if match:
                version_str = match.group(1).strip()
                from ..version import Version
                return Version.from_string(version_str)
        except (OSError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Write the version to setup.cfg."""
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")
            if not VERSION_PATTERN.search(content):
                return False

            updated_content = VERSION_PATTERN.sub(f'version = {version}', content)
            self.file_path.write_text(updated_content, encoding="utf-8")
            return True
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e
