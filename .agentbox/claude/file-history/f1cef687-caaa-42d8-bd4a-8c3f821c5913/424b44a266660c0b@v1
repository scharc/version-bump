"""Handler for pom.xml version updates (Maven/Java)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .base import FileHandler
from ..exceptions import FileUpdateError

if TYPE_CHECKING:
    from ..version import Version


# Match <version>X.Y.Z</version> at project level (not in dependencies)
# This pattern looks for version tag that's a direct child of project
VERSION_PATTERN = re.compile(
    r'(<project[^>]*>.*?<version>)([^<]+)(</version>)',
    re.DOTALL
)

# Simpler pattern for standalone version tag near top of file
SIMPLE_VERSION_PATTERN = re.compile(r'^(\s*<version>)([^<]+)(</version>)', re.MULTILINE)


class MavenHandler(FileHandler):
    """Handler for pom.xml files (Maven/Java projects)."""

    filename = "pom.xml"

    def read_version(self) -> Version | None:
        """Read the version from pom.xml."""
        if not self.exists():
            return None

        try:
            content = self.file_path.read_text(encoding="utf-8")

            # Try to find version in first 50 lines (project-level version)
            lines = content.split('\n')[:50]
            header = '\n'.join(lines)

            match = SIMPLE_VERSION_PATTERN.search(header)
            if match:
                version_str = match.group(2).strip()
                # Remove -SNAPSHOT or other suffixes
                version_str = version_str.split('-')[0]
                from ..version import Version
                return Version.from_string(version_str)
        except (OSError, ValueError):
            pass

        return None

    def write_version(self, version: Version) -> bool:
        """Write the version to pom.xml."""
        if not self.exists():
            return False

        try:
            content = self.file_path.read_text(encoding="utf-8")

            # Only update the first <version> tag (project version)
            match = SIMPLE_VERSION_PATTERN.search(content)
            if match:
                # Replace only the first occurrence
                start, end = match.span()
                updated_content = (
                    content[:start] +
                    f'{match.group(1)}{version}{match.group(3)}' +
                    content[end:]
                )
                self.file_path.write_text(updated_content, encoding="utf-8")
                return True
            return False
        except OSError as e:
            raise FileUpdateError(self.filename, str(e)) from e
