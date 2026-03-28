"""Tests for file handlers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from version_bump.exceptions import FileUpdateError
from version_bump.handlers import (
    PackageJsonHandler,
    PyprojectHandler,
    ReadmeHandler,
    get_all_handlers,
    get_current_version,
    update_all_files,
)
from version_bump.version import Version


class TestPyprojectHandler:
    """Tests for PyprojectHandler."""

    def test_exists_when_file_present(self, temp_pyproject: Path) -> None:
        """Test exists() returns True when file is present."""
        handler = PyprojectHandler(temp_pyproject.parent)
        assert handler.exists() is True

    def test_exists_when_file_missing(self, temp_project: Path) -> None:
        """Test exists() returns False when file is missing."""
        handler = PyprojectHandler(temp_project)
        assert handler.exists() is False

    def test_read_version(self, temp_pyproject: Path) -> None:
        """Test reading version from pyproject.toml."""
        handler = PyprojectHandler(temp_pyproject.parent)
        version = handler.read_version()
        assert version == Version(major=1, minor=2, patch=3)

    def test_read_version_missing_file(self, temp_project: Path) -> None:
        """Test reading version from missing file returns None."""
        handler = PyprojectHandler(temp_project)
        assert handler.read_version() is None

    def test_read_version_no_version_field(self, temp_project: Path) -> None:
        """Test reading version when no version field exists."""
        pyproject = temp_project / "pyproject.toml"
        pyproject.write_text('[tool.poetry]\nname = "test"\n', encoding="utf-8")
        handler = PyprojectHandler(temp_project)
        assert handler.read_version() is None

    def test_write_version(self, temp_pyproject: Path) -> None:
        """Test writing version to pyproject.toml."""
        handler = PyprojectHandler(temp_pyproject.parent)
        new_version = Version(major=2, minor=0, patch=0)
        assert handler.write_version(new_version) is True

        content = temp_pyproject.read_text(encoding="utf-8")
        assert 'version = "2.0.0"' in content

    def test_write_version_missing_file(self, temp_project: Path) -> None:
        """Test writing version to missing file returns False."""
        handler = PyprojectHandler(temp_project)
        new_version = Version(major=2, minor=0, patch=0)
        assert handler.write_version(new_version) is False


class TestPackageJsonHandler:
    """Tests for PackageJsonHandler."""

    def test_exists_when_file_present(self, temp_package_json: Path) -> None:
        """Test exists() returns True when file is present."""
        handler = PackageJsonHandler(temp_package_json.parent)
        assert handler.exists() is True

    def test_exists_when_file_missing(self, temp_project: Path) -> None:
        """Test exists() returns False when file is missing."""
        handler = PackageJsonHandler(temp_project)
        assert handler.exists() is False

    def test_read_version(self, temp_package_json: Path) -> None:
        """Test reading version from package.json."""
        handler = PackageJsonHandler(temp_package_json.parent)
        version = handler.read_version()
        assert version == Version(major=1, minor=2, patch=3)

    def test_read_version_missing_file(self, temp_project: Path) -> None:
        """Test reading version from missing file returns None."""
        handler = PackageJsonHandler(temp_project)
        assert handler.read_version() is None

    def test_read_version_no_version_field(self, temp_project: Path) -> None:
        """Test reading version when no version field exists."""
        package_json = temp_project / "package.json"
        package_json.write_text('{"name": "test"}', encoding="utf-8")
        handler = PackageJsonHandler(temp_project)
        assert handler.read_version() is None

    def test_write_version(self, temp_package_json: Path) -> None:
        """Test writing version to package.json."""
        handler = PackageJsonHandler(temp_package_json.parent)
        new_version = Version(major=2, minor=0, patch=0)
        assert handler.write_version(new_version) is True

        content = temp_package_json.read_text(encoding="utf-8")
        data = json.loads(content)
        assert data["version"] == "2.0.0"

    def test_write_version_missing_file(self, temp_project: Path) -> None:
        """Test writing version to missing file returns False."""
        handler = PackageJsonHandler(temp_project)
        new_version = Version(major=2, minor=0, patch=0)
        assert handler.write_version(new_version) is False

    def test_write_version_preserves_other_fields(self, temp_package_json: Path) -> None:
        """Test writing version preserves other JSON fields."""
        handler = PackageJsonHandler(temp_package_json.parent)
        new_version = Version(major=2, minor=0, patch=0)
        handler.write_version(new_version)

        content = temp_package_json.read_text(encoding="utf-8")
        data = json.loads(content)
        assert data["name"] == "test-project"
        assert data["version"] == "2.0.0"


class TestReadmeHandler:
    """Tests for ReadmeHandler."""

    def test_exists_when_file_present(self, temp_readme: Path) -> None:
        """Test exists() returns True when file is present."""
        handler = ReadmeHandler(temp_readme.parent)
        assert handler.exists() is True

    def test_exists_when_file_missing(self, temp_project: Path) -> None:
        """Test exists() returns False when file is missing."""
        handler = ReadmeHandler(temp_project)
        assert handler.exists() is False

    def test_read_version(self, temp_readme: Path) -> None:
        """Test reading version from README.md."""
        handler = ReadmeHandler(temp_readme.parent)
        version = handler.read_version()
        assert version == Version(major=1, minor=2, patch=3)

    def test_read_version_missing_file(self, temp_project: Path) -> None:
        """Test reading version from missing file returns None."""
        handler = ReadmeHandler(temp_project)
        assert handler.read_version() is None

    def test_read_version_no_version_badge(self, temp_project: Path) -> None:
        """Test reading version when no version badge exists."""
        readme = temp_project / "README.md"
        readme.write_text("# Test\n\nNo version here.", encoding="utf-8")
        handler = ReadmeHandler(temp_project)
        assert handler.read_version() is None

    def test_write_version(self, temp_readme: Path) -> None:
        """Test writing version to README.md."""
        handler = ReadmeHandler(temp_readme.parent)
        new_version = Version(major=2, minor=0, patch=0)
        assert handler.write_version(new_version) is True

        content = temp_readme.read_text(encoding="utf-8")
        assert "v2.0.0" in content
        assert "v1.2.3" not in content

    def test_write_version_missing_file(self, temp_project: Path) -> None:
        """Test writing version to missing file returns False."""
        handler = ReadmeHandler(temp_project)
        new_version = Version(major=2, minor=0, patch=0)
        assert handler.write_version(new_version) is False

    def test_write_version_updates_all_badges(self, temp_project: Path) -> None:
        """Test writing version updates all version badges."""
        readme = temp_project / "README.md"
        readme.write_text(
            "# Test v1.0.0\n\nBadge: v1.0.0\nAnother: v1.0.0",
            encoding="utf-8",
        )
        handler = ReadmeHandler(temp_project)
        new_version = Version(major=2, minor=0, patch=0)
        handler.write_version(new_version)

        content = readme.read_text(encoding="utf-8")
        assert content.count("v2.0.0") == 3
        assert "v1.0.0" not in content


class TestHandlerRegistry:
    """Tests for handler registry functions."""

    def test_get_all_handlers(self, temp_project: Path) -> None:
        """Test get_all_handlers returns all handlers."""
        handlers = get_all_handlers(temp_project)
        assert len(handlers) == 17
        # Check first few handlers are in expected order
        assert isinstance(handlers[0], PyprojectHandler)
        assert isinstance(handlers[1], PackageJsonHandler)

    def test_get_current_version_from_pyproject(self, temp_pyproject: Path) -> None:
        """Test get_current_version reads from pyproject.toml."""
        version = get_current_version(temp_pyproject.parent)
        assert version == Version(major=1, minor=2, patch=3)

    def test_get_current_version_from_package_json(
        self, temp_project: Path, temp_package_json: Path
    ) -> None:
        """Test get_current_version falls back to package.json."""
        version = get_current_version(temp_project)
        assert version == Version(major=1, minor=2, patch=3)

    def test_get_current_version_no_files(self, temp_project: Path) -> None:
        """Test get_current_version returns None when no version files."""
        version = get_current_version(temp_project)
        assert version is None

    def test_update_all_files(
        self, temp_project: Path, temp_pyproject: Path, temp_readme: Path
    ) -> None:
        """Test update_all_files updates all present files."""
        new_version = Version(major=2, minor=0, patch=0)
        updated = update_all_files(new_version, temp_project)

        assert "pyproject.toml" in updated
        assert "README.md" in updated
        assert "package.json" not in updated  # Not created by fixture

    def test_update_all_files_no_files(self, temp_project: Path) -> None:
        """Test update_all_files with no files returns empty list."""
        new_version = Version(major=2, minor=0, patch=0)
        updated = update_all_files(new_version, temp_project)
        assert updated == []
