"""Abstract base handler for file version updates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..version import Version


class FileHandler(ABC):
    """Abstract base class for file version handlers."""

    filename: str

    def __init__(self, base_path: Path | None = None) -> None:
        """Initialize the handler with an optional base path.

        Args:
            base_path: The directory containing the file. Defaults to current directory.
        """
        self.base_path = base_path or Path.cwd()

    @property
    def file_path(self) -> Path:
        """Return the full path to the file."""
        return self.base_path / self.filename

    def exists(self) -> bool:
        """Check if the file exists."""
        return self.file_path.exists()

    @abstractmethod
    def read_version(self) -> Version | None:
        """Read the version from the file.

        Returns:
            The Version object if found, None if not found or file doesn't exist.
        """
        pass

    @abstractmethod
    def write_version(self, version: Version) -> bool:
        """Write the version to the file.

        Args:
            version: The Version object to write.

        Returns:
            True if the file was updated successfully, False otherwise.
        """
        pass
