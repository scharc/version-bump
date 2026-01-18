"""Pytest fixtures for version-bump tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Generator

import pytest

from version_bump.version import Version


@pytest.fixture
def temp_project(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    return tmp_path


@pytest.fixture
def temp_pyproject(temp_project: Path) -> Path:
    """Create a temporary pyproject.toml file."""
    pyproject = temp_project / "pyproject.toml"
    pyproject.write_text(
        '[tool.poetry]\nname = "test-project"\nversion = "1.2.3"\n',
        encoding="utf-8",
    )
    return pyproject


@pytest.fixture
def temp_package_json(temp_project: Path) -> Path:
    """Create a temporary package.json file."""
    package_json = temp_project / "package.json"
    data = {"name": "test-project", "version": "1.2.3"}
    package_json.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return package_json


@pytest.fixture
def temp_readme(temp_project: Path) -> Path:
    """Create a temporary README.md file with version badge."""
    readme = temp_project / "README.md"
    readme.write_text(
        "# Test Project\n\n![Version](https://img.shields.io/badge/version-v1.2.3-blue)\n",
        encoding="utf-8",
    )
    return readme


@pytest.fixture
def sample_version() -> Version:
    """Return a sample Version object."""
    return Version(major=1, minor=2, patch=3)


@pytest.fixture
def temp_git_repo(temp_project: Path) -> Generator[Path, None, None]:
    """Create a temporary git repository."""
    import subprocess

    subprocess.run(["git", "init"], cwd=temp_project, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=temp_project,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=temp_project,
        capture_output=True,
        check=True,
    )

    # Create initial commit
    (temp_project / "README.md").write_text("# Test\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=temp_project, capture_output=True, check=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=temp_project,
        capture_output=True,
        check=True,
    )

    yield temp_project
