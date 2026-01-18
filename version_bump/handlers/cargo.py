"""Handler for Cargo.toml version updates (Rust)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


# Match version in [package] section: version = "X.Y.Z"
VERSION_PATTERN = re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE)


class CargoHandler(FileHandler):
    """Handler for Cargo.toml files (Rust projects)."""

    filename = "Cargo.toml"

    def read_version(self) -> Version | None:
        """Read the version from Cargo.toml."""
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8")
            match = VERSION_PATTERN.search(content)
            if match:
                from ..version import Version
                return Version.from_string(match.group(1))
        except (OSError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Write the version to Cargo.toml."""
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")
            updated_content = VERSION_PATTERN.sub(f'version = "{version}"', content)
            self.file_path.write_text(updated_content, encoding="utf-8")
            return True
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e
