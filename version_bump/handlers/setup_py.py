"""Handler for setup.py version updates (Python legacy)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


# Match version="X.Y.Z" or version = "X.Y.Z" patterns
VERSION_PATTERNS = [
    re.compile(r'version\s*=\s*["\']([^"\']+)["\']'),
    re.compile(r'__version__\s*=\s*["\']([^"\']+)["\']'),
]


class SetupPyHandler(FileHandler):
    """Handler for setup.py files (Python legacy projects)."""

    filename = "setup.py"

    def read_version(self) -> Version | None:
        """Read the version from setup.py."""
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8")
            for pattern in VERSION_PATTERNS:
                match = pattern.search(content)
                if match:
                    from ..version import Version
                    return Version.from_string(match.group(1))
        except (OSError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Write the version to setup.py."""
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")
            updated = False

            for pattern in VERSION_PATTERNS:
                if pattern.search(content):
                    # Preserve the quote style used in the file
                    def replacer(m: re.Match[str]) -> str:
                        original = m.group(0)
                        quote = '"' if '"' in original else "'"
                        if '__version__' in original:
                            return f'__version__ = {quote}{version}{quote}'
                        return f'version={quote}{version}{quote}'

                    content = pattern.sub(replacer, content)
                    updated = True
                    break

            if updated:
                self.file_path.write_text(content, encoding="utf-8")
                return True
            return False
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e
