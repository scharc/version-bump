"""Handler for __version__.py and _version.py updates (Python)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


# Match __version__ = "X.Y.Z" or __version__ = 'X.Y.Z'
VERSION_PATTERN = re.compile(r'__version__\s*=\s*["\']([^"\']+)["\']')


class DunderVersionHandler(FileHandler):
    """Handler for __version__.py files (Python version modules)."""

    filename = "__version__.py"

    def read_version(self) -> Version | None:
        """Read the version from __version__.py."""
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
        """Write the version to __version__.py."""
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")
            if not VERSION_PATTERN.search(content):
                return False

            def replacer(m: re.Match[str]) -> str:
                original = m.group(0)
                quote = '"' if '"' in original else "'"
                return f'__version__ = {quote}{version}{quote}'

            updated_content = VERSION_PATTERN.sub(replacer, content)
            self.file_path.write_text(updated_content, encoding="utf-8")
            return True
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e


class VersionPyHandler(FileHandler):
    """Handler for _version.py files (Python version modules)."""

    filename = "_version.py"

    def read_version(self) -> Version | None:
        """Read the version from _version.py."""
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
        """Write the version to _version.py."""
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")
            if not VERSION_PATTERN.search(content):
                return False

            def replacer(m: re.Match[str]) -> str:
                original = m.group(0)
                quote = '"' if '"' in original else "'"
                return f'__version__ = {quote}{version}{quote}'

            updated_content = VERSION_PATTERN.sub(replacer, content)
            self.file_path.write_text(updated_content, encoding="utf-8")
            return True
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e
