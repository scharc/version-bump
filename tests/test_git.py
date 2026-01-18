"""Tests for Git operations."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from version_bump.exceptions import GitOperationError
from version_bump.git import GitClient
from version_bump.version import Version


class TestGitClientDryRun:
    """Tests for GitClient in dry-run mode."""

    def test_dry_run_add_does_nothing(self, temp_project: Path) -> None:
        """Test add() does nothing in dry-run mode."""
        client = GitClient(temp_project, dry_run=True)
        with patch("subprocess.run") as mock_run:
            client.add("file1.txt", "file2.txt")
            mock_run.assert_not_called()

    def test_dry_run_commit_does_nothing(self, temp_project: Path) -> None:
        """Test commit() does nothing in dry-run mode."""
        client = GitClient(temp_project, dry_run=True)
        with patch("subprocess.run") as mock_run:
            client.commit("Test message")
            mock_run.assert_not_called()

    def test_dry_run_tag_does_nothing(self, temp_project: Path) -> None:
        """Test tag() does nothing in dry-run mode."""
        client = GitClient(temp_project, dry_run=True)
        with patch("subprocess.run") as mock_run:
            client.tag(Version(1, 2, 3))
            mock_run.assert_not_called()

    def test_dry_run_push_does_nothing(self, temp_project: Path) -> None:
        """Test push() does nothing in dry-run mode."""
        client = GitClient(temp_project, dry_run=True)
        with patch("subprocess.run") as mock_run:
            client.push()
            mock_run.assert_not_called()


class TestGitClientOperations:
    """Tests for GitClient operations with mocked subprocess."""

    def test_add_files(self, temp_project: Path) -> None:
        """Test add() calls git add with correct files."""
        client = GitClient(temp_project)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            client.add("file1.txt", "file2.txt")
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "add", "file1.txt", "file2.txt"]

    def test_add_no_files(self, temp_project: Path) -> None:
        """Test add() with no files does nothing."""
        client = GitClient(temp_project)
        with patch("subprocess.run") as mock_run:
            client.add()
            mock_run.assert_not_called()

    def test_commit(self, temp_project: Path) -> None:
        """Test commit() calls git commit with correct message."""
        client = GitClient(temp_project)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            client.commit("Test commit message")
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "commit", "-m", "Test commit message"]

    def test_tag_with_default_message(self, temp_project: Path) -> None:
        """Test tag() creates annotated tag with default message."""
        client = GitClient(temp_project)
        version = Version(1, 2, 3)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            client.tag(version)
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == [
                "git", "tag", "-a", "v1.2.3", "-m", "Release v1.2.3"
            ]

    def test_tag_with_custom_message(self, temp_project: Path) -> None:
        """Test tag() creates annotated tag with custom message."""
        client = GitClient(temp_project)
        version = Version(1, 2, 3)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            client.tag(version, message="Custom release")
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == [
                "git", "tag", "-a", "v1.2.3", "-m", "Custom release"
            ]

    def test_push_with_tags(self, temp_project: Path) -> None:
        """Test push() pushes commits and tags."""
        client = GitClient(temp_project)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            client.push(include_tags=True)
            assert mock_run.call_count == 2
            calls = mock_run.call_args_list
            assert calls[0][0][0] == ["git", "push"]
            assert calls[1][0][0] == ["git", "push", "--tags"]

    def test_push_without_tags(self, temp_project: Path) -> None:
        """Test push() without tags only pushes commits."""
        client = GitClient(temp_project)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            client.push(include_tags=False)
            assert mock_run.call_count == 1
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "push"]


class TestGitClientErrors:
    """Tests for GitClient error handling."""

    def test_add_failure_raises_error(self, temp_project: Path) -> None:
        """Test add() raises GitOperationError on failure."""
        client = GitClient(temp_project)
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git", stderr="error: pathspec 'file.txt' did not match any files"
            )
            with pytest.raises(GitOperationError) as exc_info:
                client.add("file.txt")
            assert "add" in str(exc_info.value)

    def test_commit_failure_raises_error(self, temp_project: Path) -> None:
        """Test commit() raises GitOperationError on failure."""
        client = GitClient(temp_project)
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git", stderr="nothing to commit"
            )
            with pytest.raises(GitOperationError) as exc_info:
                client.commit("Test message")
            assert "commit" in str(exc_info.value)

    def test_tag_failure_raises_error(self, temp_project: Path) -> None:
        """Test tag() raises GitOperationError on failure."""
        client = GitClient(temp_project)
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git", stderr="tag 'v1.0.0' already exists"
            )
            with pytest.raises(GitOperationError) as exc_info:
                client.tag(Version(1, 0, 0))
            assert "tag" in str(exc_info.value)

    def test_push_failure_raises_error(self, temp_project: Path) -> None:
        """Test push() raises GitOperationError on failure."""
        client = GitClient(temp_project)
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git", stderr="failed to push"
            )
            with pytest.raises(GitOperationError) as exc_info:
                client.push()
            assert "push" in str(exc_info.value)


class TestGitClientIntegration:
    """Integration tests for GitClient with real git."""

    def test_commit_and_tag_in_real_repo(self, temp_git_repo: Path) -> None:
        """Test full commit and tag workflow in real git repo."""
        # Create a file to commit
        test_file = temp_git_repo / "test.txt"
        test_file.write_text("test content", encoding="utf-8")

        client = GitClient(temp_git_repo)
        version = Version(1, 0, 0)

        # Add, commit, and tag (skip push - no remote)
        client.add("test.txt")
        client.commit(f"Bump version to {version}")
        client.tag(version)

        # Verify the tag was created
        result = subprocess.run(
            ["git", "tag", "-l"],
            cwd=temp_git_repo,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "v1.0.0" in result.stdout

    def test_commit_and_tag_helper(self, temp_git_repo: Path) -> None:
        """Test commit_and_tag helper method."""
        # Create files to commit
        file1 = temp_git_repo / "file1.txt"
        file1.write_text("content1", encoding="utf-8")
        file2 = temp_git_repo / "file2.txt"
        file2.write_text("content2", encoding="utf-8")

        client = GitClient(temp_git_repo, dry_run=True)  # dry-run to skip push
        version = Version(2, 0, 0)

        # Would normally add, commit, tag, and push
        # In dry-run, nothing happens but no error
        client.commit_and_tag(version, ["file1.txt", "file2.txt"])

    def test_commit_and_tag_empty_files(self, temp_git_repo: Path) -> None:
        """Test commit_and_tag with empty file list does nothing."""
        client = GitClient(temp_git_repo)
        version = Version(1, 0, 0)

        with patch.object(client, "add") as mock_add:
            client.commit_and_tag(version, [])
            mock_add.assert_not_called()
