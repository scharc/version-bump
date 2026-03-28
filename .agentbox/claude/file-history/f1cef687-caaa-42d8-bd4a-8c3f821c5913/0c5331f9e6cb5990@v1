"""Tests for new file handlers with real-world fixtures."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from version_bump.handlers import (
    CargoHandler,
    ComposerHandler,
    DunderVersionHandler,
    GradleHandler,
    GradleKtsHandler,
    HelmChartHandler,
    MavenHandler,
    MixHandler,
    PubspecHandler,
    SetupCfgHandler,
    SetupPyHandler,
    VersionFileHandler,
    VersionPyHandler,
    VersionTxtHandler,
)
from version_bump.version import Version


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_project(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    return tmp_path


def copy_fixture(fixture_name: str, dest_dir: Path) -> Path:
    """Copy a fixture file to destination directory."""
    src = FIXTURES_DIR / fixture_name
    dest = dest_dir / fixture_name
    shutil.copy(src, dest)
    return dest


class TestCargoHandler:
    """Tests for Cargo.toml handler (Rust)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from Cargo.toml."""
        copy_fixture("Cargo.toml", temp_project)
        handler = CargoHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to Cargo.toml."""
        copy_fixture("Cargo.toml", temp_project)
        handler = CargoHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "Cargo.toml").read_text()
        assert 'version = "2.0.0"' in content

    def test_preserves_other_fields(self, temp_project: Path) -> None:
        """Test that other fields are preserved."""
        copy_fixture("Cargo.toml", temp_project)
        handler = CargoHandler(temp_project)
        handler.write_version(Version(2, 0, 0))

        content = (temp_project / "Cargo.toml").read_text()
        assert 'name = "my-rust-project"' in content
        assert 'edition = "2021"' in content


class TestSetupPyHandler:
    """Tests for setup.py handler (Python legacy)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from setup.py."""
        copy_fixture("setup.py", temp_project)
        handler = SetupPyHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to setup.py."""
        copy_fixture("setup.py", temp_project)
        handler = SetupPyHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "setup.py").read_text()
        assert "2.0.0" in content


class TestSetupCfgHandler:
    """Tests for setup.cfg handler (Python)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from setup.cfg."""
        copy_fixture("setup.cfg", temp_project)
        handler = SetupCfgHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to setup.cfg."""
        copy_fixture("setup.cfg", temp_project)
        handler = SetupCfgHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "setup.cfg").read_text()
        assert "version = 2.0.0" in content


class TestGradleHandler:
    """Tests for build.gradle handler (Java/Groovy)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from build.gradle."""
        copy_fixture("build.gradle", temp_project)
        handler = GradleHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to build.gradle."""
        copy_fixture("build.gradle", temp_project)
        handler = GradleHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "build.gradle").read_text()
        assert '"2.0.0"' in content


class TestGradleKtsHandler:
    """Tests for build.gradle.kts handler (Kotlin)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from build.gradle.kts."""
        copy_fixture("build.gradle.kts", temp_project)
        handler = GradleKtsHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to build.gradle.kts."""
        copy_fixture("build.gradle.kts", temp_project)
        handler = GradleKtsHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "build.gradle.kts").read_text()
        assert '"2.0.0"' in content


class TestMavenHandler:
    """Tests for pom.xml handler (Maven/Java)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from pom.xml."""
        copy_fixture("pom.xml", temp_project)
        handler = MavenHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to pom.xml."""
        copy_fixture("pom.xml", temp_project)
        handler = MavenHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "pom.xml").read_text()
        assert "<version>2.0.0</version>" in content

    def test_does_not_update_dependency_versions(self, temp_project: Path) -> None:
        """Test that dependency versions are not updated."""
        copy_fixture("pom.xml", temp_project)
        handler = MavenHandler(temp_project)
        handler.write_version(Version(2, 0, 0))

        content = (temp_project / "pom.xml").read_text()
        # The junit version should remain unchanged
        assert "<version>5.9.0</version>" in content


class TestComposerHandler:
    """Tests for composer.json handler (PHP)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from composer.json."""
        copy_fixture("composer.json", temp_project)
        handler = ComposerHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to composer.json."""
        copy_fixture("composer.json", temp_project)
        handler = ComposerHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        import json
        content = (temp_project / "composer.json").read_text()
        data = json.loads(content)
        assert data["version"] == "2.0.0"


class TestPubspecHandler:
    """Tests for pubspec.yaml handler (Dart/Flutter)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from pubspec.yaml."""
        copy_fixture("pubspec.yaml", temp_project)
        handler = PubspecHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to pubspec.yaml."""
        copy_fixture("pubspec.yaml", temp_project)
        handler = PubspecHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "pubspec.yaml").read_text()
        assert "version: 2.0.0" in content


class TestHelmChartHandler:
    """Tests for Chart.yaml handler (Helm)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from Chart.yaml."""
        copy_fixture("Chart.yaml", temp_project)
        handler = HelmChartHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to Chart.yaml."""
        copy_fixture("Chart.yaml", temp_project)
        handler = HelmChartHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "Chart.yaml").read_text()
        assert "version: 2.0.0" in content

    def test_does_not_change_appversion(self, temp_project: Path) -> None:
        """Test that appVersion is not changed."""
        copy_fixture("Chart.yaml", temp_project)
        handler = HelmChartHandler(temp_project)
        handler.write_version(Version(2, 0, 0))

        content = (temp_project / "Chart.yaml").read_text()
        assert 'appVersion: "2.0.0"' in content  # Original appVersion preserved


class TestMixHandler:
    """Tests for mix.exs handler (Elixir)."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from mix.exs."""
        copy_fixture("mix.exs", temp_project)
        handler = MixHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to mix.exs."""
        copy_fixture("mix.exs", temp_project)
        handler = MixHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "mix.exs").read_text()
        assert 'version: "2.0.0"' in content


class TestVersionTxtHandler:
    """Tests for version.txt handler."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from version.txt."""
        copy_fixture("version.txt", temp_project)
        handler = VersionTxtHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to version.txt."""
        copy_fixture("version.txt", temp_project)
        handler = VersionTxtHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "version.txt").read_text().strip()
        assert content == "2.0.0"


class TestVersionFileHandler:
    """Tests for VERSION file handler."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from VERSION file."""
        copy_fixture("VERSION", temp_project)
        handler = VersionFileHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to VERSION file."""
        copy_fixture("VERSION", temp_project)
        handler = VersionFileHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "VERSION").read_text().strip()
        assert content == "2.0.0"


class TestDunderVersionHandler:
    """Tests for __version__.py handler."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from __version__.py."""
        copy_fixture("__version__.py", temp_project)
        handler = DunderVersionHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to __version__.py."""
        copy_fixture("__version__.py", temp_project)
        handler = DunderVersionHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "__version__.py").read_text()
        assert '__version__ = "2.0.0"' in content

    def test_preserves_other_fields(self, temp_project: Path) -> None:
        """Test that other fields are preserved."""
        copy_fixture("__version__.py", temp_project)
        handler = DunderVersionHandler(temp_project)
        handler.write_version(Version(2, 0, 0))

        content = (temp_project / "__version__.py").read_text()
        assert '__title__ = "my-python-project"' in content
        assert '__author__ = "Test Author"' in content


class TestVersionPyHandler:
    """Tests for _version.py handler."""

    def test_read_version(self, temp_project: Path) -> None:
        """Test reading version from _version.py."""
        copy_fixture("_version.py", temp_project)
        handler = VersionPyHandler(temp_project)
        version = handler.read_version()
        assert version == Version(1, 2, 3)

    def test_write_version(self, temp_project: Path) -> None:
        """Test writing version to _version.py."""
        copy_fixture("_version.py", temp_project)
        handler = VersionPyHandler(temp_project)
        new_version = Version(2, 0, 0)
        assert handler.write_version(new_version) is True

        content = (temp_project / "_version.py").read_text()
        assert '__version__ = "2.0.0"' in content


class TestHandlerMissingFile:
    """Tests for handler behavior when files are missing."""

    @pytest.mark.parametrize("handler_class", [
        CargoHandler,
        SetupPyHandler,
        SetupCfgHandler,
        GradleHandler,
        GradleKtsHandler,
        MavenHandler,
        ComposerHandler,
        PubspecHandler,
        HelmChartHandler,
        MixHandler,
        VersionTxtHandler,
        VersionFileHandler,
        DunderVersionHandler,
        VersionPyHandler,
    ])
    def test_read_version_missing_file(self, temp_project: Path, handler_class) -> None:
        """Test reading version when file is missing returns None."""
        handler = handler_class(temp_project)
        assert handler.read_version() is None

    @pytest.mark.parametrize("handler_class", [
        CargoHandler,
        SetupPyHandler,
        SetupCfgHandler,
        GradleHandler,
        GradleKtsHandler,
        MavenHandler,
        ComposerHandler,
        PubspecHandler,
        HelmChartHandler,
        MixHandler,
        VersionTxtHandler,
        VersionFileHandler,
        DunderVersionHandler,
        VersionPyHandler,
    ])
    def test_write_version_missing_file(self, temp_project: Path, handler_class) -> None:
        """Test writing version when file is missing returns False."""
        handler = handler_class(temp_project)
        assert handler.write_version(Version(2, 0, 0)) is False
