"""Tests for CLI."""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from version_bump.cli import main


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a Click CLI test runner."""
    return CliRunner()


class TestCLIVersion:
    """Tests for --version flag."""

    def test_version_flag(self, cli_runner: CliRunner) -> None:
        """Test --version shows version."""
        result = cli_runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "Version-bump" in result.output

    def test_version_flag_exits_early(self, cli_runner: CliRunner) -> None:
        """Test --version exits without checking for version files."""
        result = cli_runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "Current version:" not in result.output


class TestCLIShowCurrentVersion:
    """Tests for showing current version."""

    def test_shows_current_version(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test CLI shows current version."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                result = cli_runner.invoke(main, ["--patch", "--force"])
                assert "Current version: 1.2.3" in result.output
        finally:
            os.chdir(old_cwd)

    def test_error_when_no_version_file(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test CLI shows error when no version file exists."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = cli_runner.invoke(main, ["--patch"])
            assert result.exit_code == 1
            assert "Could not determine current version" in result.output
        finally:
            os.chdir(old_cwd)


class TestCLIBumpFlags:
    """Tests for bump flags (--major, --minor, --patch)."""

    def test_patch_flag(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test --patch increments patch version."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                result = cli_runner.invoke(main, ["--patch", "--force"])
                assert "1.2.4" in result.output
        finally:
            os.chdir(old_cwd)

    def test_minor_flag(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test --minor increments minor version."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                result = cli_runner.invoke(main, ["--minor", "--force"])
                assert "1.3.0" in result.output
        finally:
            os.chdir(old_cwd)

    def test_major_flag(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test --major increments major version."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                result = cli_runner.invoke(main, ["--major", "--force"])
                assert "2.0.0" in result.output
        finally:
            os.chdir(old_cwd)


class TestCLIBumpOption:
    """Tests for --bump option."""

    def test_bump_to_specific_version(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test --bump sets specific version."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                result = cli_runner.invoke(main, ["--bump", "5.0.0", "--force"])
                assert "5.0.0" in result.output
        finally:
            os.chdir(old_cwd)

    def test_bump_invalid_version(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test --bump with invalid version shows error."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = cli_runner.invoke(main, ["--bump", "invalid"])
            assert result.exit_code == 1
            assert "Invalid version format" in result.output
        finally:
            os.chdir(old_cwd)


class TestCLIForceFlag:
    """Tests for --force flag."""

    def test_force_skips_confirmation(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test --force skips confirmation prompt."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                result = cli_runner.invoke(main, ["--patch", "--force"])
                assert "Are you sure" not in result.output
                assert result.exit_code == 0
        finally:
            os.chdir(old_cwd)

    def test_without_force_prompts(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test without --force prompts for confirmation."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = cli_runner.invoke(main, ["--patch"], input="n\n")
            assert "cancelled" in result.output.lower()
        finally:
            os.chdir(old_cwd)


class TestCLIDryRun:
    """Tests for --dry-run flag."""

    def test_dry_run_shows_what_would_happen(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test --dry-run shows what would happen without making changes."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = cli_runner.invoke(main, ["--patch", "--dry-run"])
            assert result.exit_code == 0
            assert "Would update version to 1.2.4" in result.output
            assert "pyproject.toml" in result.output
        finally:
            os.chdir(old_cwd)

    def test_dry_run_does_not_modify_files(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test --dry-run does not modify files."""
        pyproject = tmp_path / "pyproject.toml"
        original_content = '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n'
        pyproject.write_text(original_content, encoding="utf-8")

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            cli_runner.invoke(main, ["--patch", "--dry-run"])
            assert pyproject.read_text(encoding="utf-8") == original_content
        finally:
            os.chdir(old_cwd)


class TestCLIInteractiveMode:
    """Tests for interactive mode."""

    def test_interactive_mode_prompts_for_version(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test interactive mode prompts for version."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                # Enter "2.0.0" as version
                result = cli_runner.invoke(main, ["--force"], input="2.0.0\n")
                assert "2.0.0" in result.output
        finally:
            os.chdir(old_cwd)

    def test_interactive_mode_uses_default(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test interactive mode uses default (patch bump) when enter pressed."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                # Just press enter to accept default
                result = cli_runner.invoke(main, ["--force"], input="\n")
                assert "1.2.4" in result.output
        finally:
            os.chdir(old_cwd)


class TestCLIFileUpdates:
    """Tests for file update behavior."""

    def test_updates_pyproject_toml(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test CLI updates pyproject.toml."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                result = cli_runner.invoke(main, ["--patch", "--force"])
                assert "Updated pyproject.toml" in result.output
        finally:
            os.chdir(old_cwd)

    def test_updates_multiple_files(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test CLI updates multiple files when present."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )
        readme = tmp_path / "README.md"
        readme.write_text("# Test v1.2.3\n", encoding="utf-8")

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient"):
                result = cli_runner.invoke(main, ["--patch", "--force"])
                assert "Updated pyproject.toml" in result.output
                assert "Updated README.md" in result.output
        finally:
            os.chdir(old_cwd)


class TestCLIGitOperations:
    """Tests for git operations in CLI."""

    def test_commits_and_tags(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test CLI commits and tags after update."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient") as mock_git_class:
                mock_git = mock_git_class.return_value
                result = cli_runner.invoke(main, ["--patch", "--force"])
                assert "Committed and tagged" in result.output
                mock_git.commit_and_tag.assert_called_once()
        finally:
            os.chdir(old_cwd)

    def test_git_error_shows_message(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        """Test CLI shows error when git operation fails."""
        from version_bump.exceptions import GitOperationError

        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.poetry]\nname = "test"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("version_bump.cli.GitClient") as mock_git_class:
                mock_git = mock_git_class.return_value
                mock_git.commit_and_tag.side_effect = GitOperationError(
                    "push", "no remote configured"
                )
                result = cli_runner.invoke(main, ["--patch", "--force"])
                assert result.exit_code == 1
                assert "push" in result.output.lower() or "Error" in result.output
        finally:
            os.chdir(old_cwd)
