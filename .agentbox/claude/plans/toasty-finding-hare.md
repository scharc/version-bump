# Version-Bump Refactoring Plan

## Summary
Comprehensive refactoring of version-bump CLI tool with modern Python practices, proper architecture, and full test coverage.

## Current Issues
1. **Hardcoded version** - `main.py:147` shows "1.0.0" but actual version is 0.1.3
2. **No type hints** - Reduces code clarity and IDE support
3. **Repetitive code** - Each file updater duplicates the same pattern
4. **Print statements** - Should use Click's echo or logging
5. **No error handling** - File operations can fail silently
6. **Zero test coverage** - pytest configured but no tests exist
7. **Monolithic structure** - All 175 lines in single file

## New Project Structure
```
version_bump/
├── __init__.py          # Package init with __version__
├── cli.py               # Click CLI entry point
├── version.py           # Version class with SemVer logic
├── handlers/
│   ├── __init__.py      # Handler registry
│   ├── base.py          # Abstract base handler
│   ├── pyproject.py     # pyproject.toml handler
│   ├── package_json.py  # package.json handler
│   └── readme.py        # README.md handler
├── git.py               # Git operations
└── exceptions.py        # Custom exceptions

tests/
├── __init__.py
├── conftest.py          # Pytest fixtures
├── test_version.py      # Version class tests
├── test_handlers.py     # File handler tests
├── test_git.py          # Git operation tests (mocked)
└── test_cli.py          # CLI integration tests
```

## Implementation Details

### 1. Custom Exceptions (`exceptions.py`)
```python
class VersionBumpError(Exception): ...
class VersionParseError(VersionBumpError): ...
class FileUpdateError(VersionBumpError): ...
class GitOperationError(VersionBumpError): ...
```

### 2. Version Class (`version.py`)
- Dataclass with `major`, `minor`, `patch` fields
- Class methods: `from_string()`, `parse()`
- Instance methods: `bump_major()`, `bump_minor()`, `bump_patch()`
- Validation on creation
- `__str__` returns "X.Y.Z" format

### 3. Abstract File Handler (`handlers/base.py`)
```python
class FileHandler(Protocol):
    filename: str
    def exists(self) -> bool: ...
    def read_version(self) -> Version | None: ...
    def write_version(self, version: Version) -> bool: ...
```

### 4. Concrete Handlers
- `PyprojectHandler` - Regex-based TOML version update
- `PackageJsonHandler` - JSON parsing for package.json
- `ReadmeHandler` - Regex replacement for version badges

### 5. Git Operations (`git.py`)
- `GitClient` class wrapping subprocess calls
- Methods: `add()`, `commit()`, `tag()`, `push()`
- Proper error handling with `GitOperationError`
- Optional dry-run mode

### 6. CLI (`cli.py`)
- Use `click.echo()` instead of `print()`
- Read version dynamically from `__init__.py`
- Clean separation of CLI logic from business logic
- Proper exit codes

### 7. Dynamic Version (`__init__.py`)
```python
from importlib.metadata import version
__version__ = version("version-bump")
```

## Files to Modify/Create

| File | Action | Purpose |
|------|--------|---------|
| `version_bump/__init__.py` | Modify | Add `__version__` |
| `version_bump/exceptions.py` | Create | Custom exceptions |
| `version_bump/version.py` | Create | Version dataclass |
| `version_bump/handlers/base.py` | Create | Abstract handler |
| `version_bump/handlers/pyproject.py` | Create | TOML handler |
| `version_bump/handlers/package_json.py` | Create | JSON handler |
| `version_bump/handlers/readme.py` | Create | README handler |
| `version_bump/handlers/__init__.py` | Create | Handler registry |
| `version_bump/git.py` | Create | Git operations |
| `version_bump/cli.py` | Create | CLI entry point |
| `version_bump/main.py` | Delete | Replaced by new structure |
| `pyproject.toml` | Modify | Update entry point |
| `tests/conftest.py` | Create | Pytest fixtures |
| `tests/test_version.py` | Create | Version tests |
| `tests/test_handlers.py` | Create | Handler tests |
| `tests/test_git.py` | Create | Git tests |
| `tests/test_cli.py` | Create | CLI tests |

## Test Coverage Goals
- **Version class**: parsing, validation, bumping (major/minor/patch)
- **File handlers**: read/write operations, missing file handling
- **Git operations**: mocked subprocess calls, error scenarios
- **CLI**: all flags, interactive mode, error messages

## Verification Steps
1. Run `poetry install` to install dependencies
2. Run `pytest -v` to execute all tests
3. Run `poetry run version-bump --help` to verify CLI works
4. Run `poetry run version-bump --version` to verify dynamic version
5. Test in a git repo: `poetry run version-bump --patch --force`

## Backward Compatibility
- CLI interface remains identical (same flags and behavior)
- Same files updated (pyproject.toml, package.json, README.md)
- Same Git workflow (commit, tag, push)
