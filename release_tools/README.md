# Release Tools

Standardized automation and validation utilities for managing releases, version bumps, and documentation checks across `purpleair_api`.

## Overview

The `release_tools/` directory provides release utilities for `purpleair_api` following the unified `carlkidcrypto` ecosystem standard.

## Available Tools

### `bump_version.sh` (or `release.sh`)

Atomically bumps version strings across all tracked package and documentation files.

- **Aliases**: `release_tools/release.sh` is a symlink to `bump_version.sh`.
- **Validation**: Supports Semantic Versioning (e.g. `1.5.1`, `1.5.1a1`) and Calendar Versioning.
- **Auto-detection**: Automatically extracts the current version from `setup.cfg` if omitted.
- **Safety checks**:
  - Ensures required target files contain the expected current version before making edits.
  - Checks after replacement that no stale references to the old version remain in tracked active files.
  - Leaves historical files (e.g. `CHANGELOG.md`) and generated HTML intact.

### Command-Line Usage

```bash
# Preview changes without modifying files
./release_tools/bump_version.sh --dry-run 1.5.1

# Bump version and automatically verify code formatting, docs (-W), and tests
./release_tools/bump_version.sh --verify 1.5.1

# Bump version directly
./release_tools/bump_version.sh 1.5.1

# Specify old version explicitly (if needed)
./release_tools/bump_version.sh 1.5.1 1.5.1a1
```

### Options

| Flag | Long Option | Description |
| :--- | :--- | :--- |
| `-n` | `--dry-run` | Shows files that would be modified without writing changes. |
| `-v` | `--verify` | Runs Black formatting check, Sphinx doc build with `-W` (zero warnings), and pytest suite. |
| `-h` | `--help` | Displays help message and examples. |

---

## Managed File Touchpoints

When running `bump_version.sh` in `purpleair_api`, the following files are synchronized:

1. `setup.cfg` &mdash; Python package distribution version (`version = <VER>`)
2. `sphinx_docs_build/source/conf.py` &mdash; Sphinx documentation release variable (`release = "v<VER>"`)

### Excluded Files

The following files are intentionally excluded from version bump scripts:
- `CHANGELOG.md` &mdash; Generated and maintained by `auto_change_log.md`
- `docs/html/**`, `docs/html_v*/**` &mdash; Generated documentation artifacts
- `tests/**` &mdash; Test suite files

---

## Standard Release Checklist

1. **Create a release branch or worktree**:
   ```bash
   git checkout -b chore/bump-v1.5.1
   ```
2. **Execute version bump with verification**:
   ```bash
   ./release_tools/bump_version.sh --verify 1.5.1
   ```
3. **Inspect the git status and diff**:
   ```bash
   git diff
   ```
4. **Commit and push**:
   ```bash
   git commit -am "chore: bump version to 1.5.1"
   git push -u origin chore/bump-v1.5.1
   ```
5. **Open Pull Request**:
   - Open a PR targeting `main`.
   - Wait for maintainer review and merge.
