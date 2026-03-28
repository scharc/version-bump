"""Handler for build.gradle and build.gradle.kts version updates (Java/Kotlin)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


# Match version = "X.Y.Z" or version "X.Y.Z" patterns
VERSION_PATTERNS = [
    re.compile(r'version\s*=\s*["\']([^"\']+)["\']'),
    re.compile(r'version\s+["\']([^"\']+)["\']'),
]


class GradleHandler(FileHandler):
    """Handler for build.gradle files (Java/Groovy projects)."""

    filename = "build.gradle"

    def read_version(self) -> Version | None:
        """Read the version from build.gradle."""
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8")
            for pattern in VERSION_PATTERNS:
                match = pattern.search(content)
                if match:
                    version_str = match.group(1)
                    # Skip SNAPSHOT or other non-semver suffixes for reading
                    version_str = version_str.split('-')[0]
                    from ..version import Version
                    return Version.from_string(version_str)
        except (OSError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Write the version to build.gradle."""
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")
            updated = False

            for pattern in VERSION_PATTERNS:
                if pattern.search(content):
                    def replacer(m: re.Match[str]) -> str:
                        original = m.group(0)
                        quote = '"' if '"' in original else "'"
                        if '=' in original:
                            return f'version = {quote}{version}{quote}'
                        return f'version {quote}{version}{quote}'

                    content = pattern.sub(replacer, content)
                    updated = True
                    break

            if updated:
                self.file_path.write_text(content, encoding="utf-8")
                return True
            return False
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e


class GradleKtsHandler(FileHandler):
    """Handler for build.gradle.kts files (Kotlin projects)."""

    filename = "build.gradle.kts"

    def read_version(self) -> Version | None:
        """Read the version from build.gradle.kts."""
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8")
            for pattern in VERSION_PATTERNS:
                match = pattern.search(content)
                if match:
                    version_str = match.group(1)
                    version_str = version_str.split('-')[0]
                    from ..version import Version
                    return Version.from_string(version_str)
        except (OSError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Write the version to build.gradle.kts."""
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")
            updated = False

            for pattern in VERSION_PATTERNS:
                if pattern.search(content):
                    def replacer(m: re.Match[str]) -> str:
                        original = m.group(0)
                        quote = '"' if '"' in original else "'"
                        if '=' in original:
                            return f'version = {quote}{version}{quote}'
                        return f'version {quote}{version}{quote}'

                    content = pattern.sub(replacer, content)
                    updated = True
                    break

            if updated:
                self.file_path.write_text(content, encoding="utf-8")
                return True
            return False
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e
