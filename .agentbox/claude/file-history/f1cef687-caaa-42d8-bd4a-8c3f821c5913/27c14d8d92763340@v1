"""Git operations for version bumping."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from .exceptions import GitOperationError

if TYPE_CHECKING:
    from .version import Version


class GitClient:
    """Client for Git operations related to version bumping."""

    def __init__(self, repo_path: Path | None = None, dry_run: bool = False) -> None:
        """Initialize the Git client.

        Args:
            repo_path: Path to the git repository. Defaults to current directory.
            dry_run: If True, don't execute any git commands.
        """
        self.repo_path = repo_path or Path.cwd()
        self.dry_run = dry_run

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        """Run a git command.

        Args:
            *args: Git command arguments (without 'git' prefix).

        Returns:
            The completed process.

        Raises:
            GitOperationError: If the command fails.
        """
        cmd = ["git", *args]
        try:
            return subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise GitOperationError(args[0], error_msg) from e

    def add(self, *files: str) -> None:
        """Stage files for commit.

        Args:
            *files: File paths to stage.

        Raises:
            GitOperationError: If the add operation fails.
        """
        if not files:
            return

        if self.dry_run:
            return

        self._run("add", *files)

    def commit(self, message: str) -> None:
        """Create a commit with the given message.

        Args:
            message: The commit message.

        Raises:
            GitOperationError: If the commit operation fails.
        """
        if self.dry_run:
            return

        self._run("commit", "-m", message)

    def tag(self, version: Version, message: str | None = None) -> None:
        """Create an annotated tag for the version.

        Args:
            version: The Version to tag.
            message: Optional tag message. Defaults to "Release vX.Y.Z".

        Raises:
            GitOperationError: If the tag operation fails.
        """
        if self.dry_run:
            return

        tag_name = f"v{version}"
        tag_message = message or f"Release {tag_name}"
        self._run("tag", "-a", tag_name, "-m", tag_message)

    def push(self, include_tags: bool = True) -> None:
        """Push commits and optionally tags to remote.

        Args:
            include_tags: Whether to push tags as well.

        Raises:
            GitOperationError: If the push operation fails.
        """
        if self.dry_run:
            return

        self._run("push")
        if include_tags:
            self._run("push", "--tags")

    def commit_and_tag(self, version: Version, files: list[str]) -> None:
        """Commit changes, tag, and push.

        Args:
            version: The Version being released.
            files: List of files to commit.

        Raises:
            GitOperationError: If any git operation fails.
        """
        if not files:
            return

        self.add(*files)
        self.commit(f"Bump version to {version}")
        self.tag(version)
        self.push()
