#!/usr/bin/env python3

import click
import os
import subprocess
import re
from pathlib import Path
import json

# Constants
PYPROJECT_TOML = "pyproject.toml"
README = "README.md"
PACKAGE_JSON = "package.json"


def get_current_version():
    """Retrieve the current version from pyproject.toml or package.json."""
    if Path(PYPROJECT_TOML).exists():
        with open(PYPROJECT_TOML, "r") as file:
            match = re.search(r'version\s*=\s*"([^\"]+)"', file.read())
            if match:
                return match.group(1)

    if Path(PACKAGE_JSON).exists():
        with open(PACKAGE_JSON, "r") as file:
            package_data = json.load(file)
            return package_data.get("version")

    return "unknown"


def update_pyproject_toml_version(new_version):
    if not Path(PYPROJECT_TOML).exists():
        print(f"{PYPROJECT_TOML} not found. Skipping.")
        return False

    with open(PYPROJECT_TOML, "r") as file:
        content = file.read()

    updated_content = re.sub(r'version\s*=\s*"[^\"]+"', f'version = "{new_version}"', content)

    with open(PYPROJECT_TOML, "w") as file:
        file.write(updated_content)

    print(f"Updated {PYPROJECT_TOML} version to {new_version}.")
    return True


def update_readme_version(new_version):
    if not Path(README).exists():
        print(f"{README} not found. Skipping.")
        return False

    with open(README, "r") as file:
        content = file.read()

    updated_content = re.sub(r'v[0-9]+\.[0-9]+\.[0-9]+', f'v{new_version}', content)

    with open(README, "w") as file:
        file.write(updated_content)

    print(f"Updated {README} version to {new_version}.")
    return True


def update_package_json_version(new_version):
    if not Path(PACKAGE_JSON).exists():
        print(f"{PACKAGE_JSON} not found. Skipping.")
        return False

    with open(PACKAGE_JSON, "r") as file:
        package_data = json.load(file)

    package_data["version"] = new_version

    with open(PACKAGE_JSON, "w") as file:
        json.dump(package_data, file, indent=2)

    print(f"Updated {PACKAGE_JSON} version to {new_version}.")
    return True


def commit_and_tag(new_version, changed_files):
    try:
        if not changed_files:
            print("No files changed. Skipping git commit and tag.")
            return

        subprocess.run(["git", "add"] + changed_files, check=True)
        subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"], check=True)
        subprocess.run(["git", "tag", "-a", f"v{new_version}", "-m", f"Release v{new_version}"], check=True)
        subprocess.run(["git", "push"], check=True)
        subprocess.run(["git", "push", "--tags"], check=True)
        print(f"Committed and tagged v{new_version}.")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")


def bump_version(new_version, force):
    changed_files = []
    if not force:
        confirm = input(f"Are you sure you want to bump the version to {new_version}? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Version bump cancelled.")
            return
    
    if update_pyproject_toml_version(new_version):
        changed_files.append(PYPROJECT_TOML)
    if update_readme_version(new_version):
        changed_files.append(README)
    if update_package_json_version(new_version):
        changed_files.append(PACKAGE_JSON)

    

    commit_and_tag(new_version, changed_files)


def increment_version(version, part):
    """Increment the specified part (major, minor, patch) of a version string."""
    major, minor, patch = map(int, version.split('.'))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid version part: {part}")
    return f"{major}.{minor}.{patch}"


@click.command()
@click.option('--version', is_flag=True, help="Show the version of the tool.")
@click.option('--bump', default=None, help="Bump the version to the specified value.")
@click.option('--force', is_flag=True, help="Force version bump without confirmation.")
@click.option('--major', is_flag=True, help="Increment the major version.")
@click.option('--minor', is_flag=True, help="Increment the minor version.")
@click.option('--patch', is_flag=True, help="Increment the patch version.")
def main(version, bump, force, major, minor, patch):
    "Version-bump: A semantic versioning tool."

    if version:
        print("Version-bump 1.0.0")
        return

    current_version = get_current_version()
    print(f"Current version: {current_version}")

    if major:
        new_version = increment_version(current_version, "major")
    elif minor:
        new_version = increment_version(current_version, "minor")
    elif patch:
        new_version = increment_version(current_version, "patch")
    elif bump:
        if not re.match(r'^\d+\.\d+\.\d+$', bump):
            print("Invalid version format. Use semantic versioning (e.g., 1.0.1).")
            return
        new_version = bump
    else:
        default_version = increment_version(current_version, "patch")
        new_version = input(f"Enter the new version (default: {default_version}): ").strip() or default_version
        if not re.match(r'^\d+\.\d+\.\d+$', new_version):
            print("Invalid version format. Use semantic versioning (e.g., 1.0.1).")
            return

    bump_version(new_version, force)


if __name__ == "__main__":
    main()
