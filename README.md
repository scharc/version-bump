# Version-Bump 🚀

Version: **v0.2.0**

Are you tired of manually updating version numbers in your project? Sick of forgetting to tag releases in Git? Say no more—**Version-Bump** is here to save your day (and your sanity). This tool is slick, funny, and as gritty as your late-night coding sessions.

## What is Version-Bump? 🤔

**Version-Bump** is a no-nonsense, straight-to-the-point tool for managing semantic versioning in your projects. Whether you’ve got a Python project, a Node.js app, or a README.md crying for a new version tag, this bad boy’s got you covered.

You:
- 🔢 Increment versions (major, minor, patch) with a single command.
- 🎉 Automatically update `pyproject.toml`, `package.json`, and `README.md`.
- 💅 Tag your Git repo like a pro (no more "Oops, forgot the tag" situations).
- 🤯 Feel like a rockstar with every bump.

## Features 🌟

- **One-liner Bumps**: `version-bump --patch` to go from 1.0.0 to 1.0.1. Done.
- **Interactive Mode**: Want to choose the next version manually? We got you.
- **Git Integration**: Updates and commits only the files you actually changed.
- **Flexible**: Works even if you don’t have `pyproject.toml` or `package.json`. It just updates what’s there.
- **Force Mode**: Skip the confirmation and live on the edge with `--force`.

## Installation 📦

### Using Poetry

1. Clone this repo:
   ```bash
   git clone https://github.com/scharc/version-bump.git
   cd version-bump
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run it within the Poetry environment:
   ```bash
   poetry run version-bump --help
   ```
4. Optionally, add the tool to your PATH by creating a symbolic link:
   ```bash
   ln -s $(poetry run which version-bump) ~/.local/bin/version-bump
   ```

## Usage 🛠️

Run it from anywhere in your repo and watch the magic happen:

```bash
# Show current version and get prompted for the next patch version:
version-bump

# Increment the patch version (e.g., 1.0.0 -> 1.0.1):
version-bump --patch

# Increment the minor version (e.g., 1.0.0 -> 1.1.0):
version-bump --minor

# Increment the major version (e.g., 1.0.0 -> 2.0.0):
version-bump --major

# Set a specific version:
version-bump --bump 2.3.4

# Skip all confirmations and live dangerously:
version-bump --patch --force
```

## What It Does Behind the Scenes 🔍

1. Finds your current version in `pyproject.toml`, `package.json`, or both.
2. Updates the version to your liking.
3. Updates version tags in your `README.md` (because documentation matters!).
4. Commits only the files it changed.
5. Tags the commit in Git with the new version.
6. Pushes everything to your repo (you’re welcome).

## Why You Need This 🦾

- **Your coworkers will think you’re a versioning wizard. 🧙**
- **It saves you from the pain of manual edits.**
- **Automated Git tags? Hell yeah.**

## Contributing 🤝

We’re not picky, but we’re picky:
- Fork this repo.
- Make your changes.
- Open a pull request.
- Add a meme to your PR description (optional, but highly encouraged).

## License 📜

GPL-3.0. Because freedom matters.

---

Bump your version. Save your soul. 🖖

