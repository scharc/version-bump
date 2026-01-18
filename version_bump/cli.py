"""CLI entry point for version-bump."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from .exceptions import GitOperationError, VersionBumpError, VersionParseError
from .git import GitClient
from .handlers import get_current_version, update_all_files
from .version import Version


def get_tool_version() -> str:
    """Get the version of the version-bump tool."""
    try:
        from importlib.metadata import version

        return version("version-bump")
    except Exception:
        return "unknown"


@click.command()
@click.option("--version", "show_version", is_flag=True, help="Show the version of the tool.")
@click.option("--bump", default=None, help="Bump the version to the specified value.")
@click.option("--force", is_flag=True, help="Force version bump without confirmation.")
@click.option("--major", is_flag=True, help="Increment the major version.")
@click.option("--minor", is_flag=True, help="Increment the minor version.")
@click.option("--patch", is_flag=True, help="Increment the patch version.")
@click.option("--dry-run", is_flag=True, help="Show what would happen without making changes.")
def main(
    show_version: bool,
    bump: str | None,
    force: bool,
    major: bool,
    minor: bool,
    patch: bool,
    dry_run: bool,
) -> None:
    """Version-bump: A semantic versioning tool."""
    if show_version:
        click.echo(f"Version-bump {get_tool_version()}")
        return

    base_path = Path.cwd()
    current_version = get_current_version(base_path)

    if current_version is None:
        click.echo("Error: Could not determine current version.", err=True)
        click.echo("Ensure pyproject.toml or package.json exists with a version field.", err=True)
        sys.exit(1)

    click.echo(f"Current version: {current_version}")

    # Determine the new version
    try:
        new_version = _determine_new_version(
            current_version, bump, major, minor, patch
        )
    except VersionParseError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if new_version is None:
        click.echo("Version bump cancelled.")
        return

    # Confirm with user unless force flag is set
    if not force and not dry_run:
        confirm = click.prompt(
            f"Are you sure you want to bump the version to {new_version}? (y/N)",
            default="n",
            show_default=False,
        )
        if confirm.lower() != "y":
            click.echo("Version bump cancelled.")
            return

    # Update files
    if dry_run:
        click.echo(f"Would update version to {new_version}")
        click.echo("Files that would be updated:")
        from .handlers import get_all_handlers

        for handler in get_all_handlers(base_path):
            if handler.exists():
                click.echo(f"  - {handler.filename}")
        return

    try:
        updated_files = update_all_files(new_version, base_path)

        if not updated_files:
            click.echo("No files were updated.", err=True)
            sys.exit(1)

        for filename in updated_files:
            click.echo(f"Updated {filename} version to {new_version}.")

        # Git operations
        git_client = GitClient(base_path)
        git_client.commit_and_tag(new_version, updated_files)
        click.echo(f"Committed and tagged v{new_version}.")

    except GitOperationError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except VersionBumpError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def _determine_new_version(
    current_version: Version,
    bump: str | None,
    major: bool,
    minor: bool,
    patch: bool,
) -> Version | None:
    """Determine the new version based on CLI arguments.

    Args:
        current_version: The current version.
        bump: Explicit version string to bump to.
        major: Whether to bump major version.
        minor: Whether to bump minor version.
        patch: Whether to bump patch version.

    Returns:
        The new Version, or None if cancelled.

    Raises:
        VersionParseError: If bump string is invalid.
    """
    if major:
        return current_version.bump_major()
    elif minor:
        return current_version.bump_minor()
    elif patch:
        return current_version.bump_patch()
    elif bump:
        return Version.from_string(bump)
    else:
        # Interactive mode
        default_version = current_version.bump_patch()
        new_version_str = click.prompt(
            f"Enter the new version (default: {default_version})",
            default=str(default_version),
            show_default=False,
        )
        return Version.from_string(new_version_str)


if __name__ == "__main__":
    main()
