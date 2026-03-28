"""Tests for Version class."""

from __future__ import annotations

import pytest

from version_bump.exceptions import VersionParseError
from version_bump.version import Version


class TestVersionCreation:
    """Tests for Version object creation."""

    def test_create_version(self) -> None:
        """Test creating a Version with valid components."""
        v = Version(major=1, minor=2, patch=3)
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3

    def test_create_version_zeros(self) -> None:
        """Test creating a Version with zero components."""
        v = Version(major=0, minor=0, patch=0)
        assert v.major == 0
        assert v.minor == 0
        assert v.patch == 0

    def test_create_version_negative_major(self) -> None:
        """Test that negative major raises ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            Version(major=-1, minor=0, patch=0)

    def test_create_version_negative_minor(self) -> None:
        """Test that negative minor raises ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            Version(major=0, minor=-1, patch=0)

    def test_create_version_negative_patch(self) -> None:
        """Test that negative patch raises ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            Version(major=0, minor=0, patch=-1)


class TestVersionFromString:
    """Tests for Version.from_string() parsing."""

    def test_parse_valid_version(self) -> None:
        """Test parsing a valid version string."""
        v = Version.from_string("1.2.3")
        assert v == Version(major=1, minor=2, patch=3)

    def test_parse_version_with_whitespace(self) -> None:
        """Test parsing a version string with leading/trailing whitespace."""
        v = Version.from_string("  1.2.3  ")
        assert v == Version(major=1, minor=2, patch=3)

    def test_parse_version_zeros(self) -> None:
        """Test parsing version with zeros."""
        v = Version.from_string("0.0.0")
        assert v == Version(major=0, minor=0, patch=0)

    def test_parse_large_numbers(self) -> None:
        """Test parsing version with large numbers."""
        v = Version.from_string("100.200.300")
        assert v == Version(major=100, minor=200, patch=300)

    def test_parse_invalid_format_missing_patch(self) -> None:
        """Test that missing patch raises VersionParseError."""
        with pytest.raises(VersionParseError):
            Version.from_string("1.2")

    def test_parse_invalid_format_missing_minor(self) -> None:
        """Test that missing minor raises VersionParseError."""
        with pytest.raises(VersionParseError):
            Version.from_string("1")

    def test_parse_invalid_format_extra_component(self) -> None:
        """Test that extra component raises VersionParseError."""
        with pytest.raises(VersionParseError):
            Version.from_string("1.2.3.4")

    def test_parse_invalid_format_letters(self) -> None:
        """Test that letters raise VersionParseError."""
        with pytest.raises(VersionParseError):
            Version.from_string("1.2.a")

    def test_parse_invalid_format_empty(self) -> None:
        """Test that empty string raises VersionParseError."""
        with pytest.raises(VersionParseError):
            Version.from_string("")

    def test_parse_invalid_format_with_v_prefix(self) -> None:
        """Test that v prefix raises VersionParseError."""
        with pytest.raises(VersionParseError):
            Version.from_string("v1.2.3")

    def test_parse_alias(self) -> None:
        """Test that parse() is an alias for from_string()."""
        v = Version.parse("1.2.3")
        assert v == Version(major=1, minor=2, patch=3)


class TestVersionStr:
    """Tests for Version string representation."""

    def test_str_basic(self) -> None:
        """Test string representation."""
        v = Version(major=1, minor=2, patch=3)
        assert str(v) == "1.2.3"

    def test_str_zeros(self) -> None:
        """Test string representation with zeros."""
        v = Version(major=0, minor=0, patch=0)
        assert str(v) == "0.0.0"

    def test_str_large_numbers(self) -> None:
        """Test string representation with large numbers."""
        v = Version(major=100, minor=200, patch=300)
        assert str(v) == "100.200.300"


class TestVersionBumping:
    """Tests for Version bump methods."""

    def test_bump_major(self) -> None:
        """Test bumping major version."""
        v = Version(major=1, minor=2, patch=3)
        new_v = v.bump_major()
        assert new_v == Version(major=2, minor=0, patch=0)

    def test_bump_major_from_zero(self) -> None:
        """Test bumping major version from zero."""
        v = Version(major=0, minor=5, patch=10)
        new_v = v.bump_major()
        assert new_v == Version(major=1, minor=0, patch=0)

    def test_bump_minor(self) -> None:
        """Test bumping minor version."""
        v = Version(major=1, minor=2, patch=3)
        new_v = v.bump_minor()
        assert new_v == Version(major=1, minor=3, patch=0)

    def test_bump_minor_from_zero(self) -> None:
        """Test bumping minor version from zero."""
        v = Version(major=1, minor=0, patch=5)
        new_v = v.bump_minor()
        assert new_v == Version(major=1, minor=1, patch=0)

    def test_bump_patch(self) -> None:
        """Test bumping patch version."""
        v = Version(major=1, minor=2, patch=3)
        new_v = v.bump_patch()
        assert new_v == Version(major=1, minor=2, patch=4)

    def test_bump_patch_from_zero(self) -> None:
        """Test bumping patch version from zero."""
        v = Version(major=1, minor=2, patch=0)
        new_v = v.bump_patch()
        assert new_v == Version(major=1, minor=2, patch=1)

    def test_bump_does_not_mutate(self) -> None:
        """Test that bump methods return new objects, not mutate."""
        v = Version(major=1, minor=2, patch=3)
        v.bump_major()
        v.bump_minor()
        v.bump_patch()
        assert v == Version(major=1, minor=2, patch=3)


class TestVersionEquality:
    """Tests for Version equality."""

    def test_equal_versions(self) -> None:
        """Test that equal versions are equal."""
        v1 = Version(major=1, minor=2, patch=3)
        v2 = Version(major=1, minor=2, patch=3)
        assert v1 == v2

    def test_unequal_versions_major(self) -> None:
        """Test that different major versions are not equal."""
        v1 = Version(major=1, minor=2, patch=3)
        v2 = Version(major=2, minor=2, patch=3)
        assert v1 != v2

    def test_unequal_versions_minor(self) -> None:
        """Test that different minor versions are not equal."""
        v1 = Version(major=1, minor=2, patch=3)
        v2 = Version(major=1, minor=3, patch=3)
        assert v1 != v2

    def test_unequal_versions_patch(self) -> None:
        """Test that different patch versions are not equal."""
        v1 = Version(major=1, minor=2, patch=3)
        v2 = Version(major=1, minor=2, patch=4)
        assert v1 != v2

    def test_version_is_hashable(self) -> None:
        """Test that Version is hashable (can be used in sets/dicts)."""
        v1 = Version(major=1, minor=2, patch=3)
        v2 = Version(major=1, minor=2, patch=3)
        version_set = {v1, v2}
        assert len(version_set) == 1
