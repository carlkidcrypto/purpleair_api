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

When running `bump_version.sh` (or `release.sh`) in `purpleair_api`, the following files are synchronized:

1. `python/setup.cfg` &mdash; Python package distribution version (`version = <VER>`)
2. `python/pyproject.toml` &mdash; Modern Python build system specification (`version = "<VER>"`)
3. `meson.build` &mdash; Root C++17 Meson build configuration (`version: '<VER>'`)
4. `python/meson.build` &mdash; Python extension Meson build configuration (`version: '<VER>'`)
5. `javascript/package.json` &mdash; Node.js package version (mapped to SemVer 2.0.0 e.g. `YYYY.M.D-alpha.N`)
6. `javascript/package-lock.json` &mdash; Node.js package lock version
7. `csharp/PurpleAirAPI.csproj` &mdash; .NET C# project package version (`<Version>...</Version>`)
8. `sphinx_docs_build/source/conf.py` &mdash; Sphinx documentation release variable (`release = "v<VER>"`)
9. `README.rst` &mdash; Release badge download shield URLs (`v<VER>`)
10. `tools/generate_winget_manifest.py` &mdash; WinGet manifest generator fallback default
11. `python/uv.lock` &mdash; Dependency lockfile package version

### Excluded Files

The following files are intentionally excluded from version bump scripts:
- `CHANGELOG.md` &mdash; Generated and maintained by `auto_change_log.md`
- `docs/html/**`, `docs/html_v*/**` &mdash; Generated documentation artifacts
- `tests/**`, `python/tests/**` &mdash; Test suite files
- External specification files (e.g. CSA Matter 1.5.1 specification references)

---

## Standard Release Checklist

1. **Create a release branch or worktree**:
   ```bash
   git worktree add -b release/v2026.11.11a0 ../purpleair_api-release-v2026.11.11a0 origin/main
   cd ../purpleair_api-release-v2026.11.11a0
   ```
2. **Execute version bump with verification**:
   ```bash
   ./release_tools/bump_version.sh --verify 2026.11.11a0
   ```
   *(or use the symlink `./release_tools/release.sh --verify 2026.11.11a0`)*
3. **Inspect the git status and diff**:
   ```bash
   git diff
   ```
4. **Commit and push using targeted staging**:
   ```bash
   git add <modified-files>
   git commit -m "chore(release): bump version to 2026.11.11a0 across multi-language manifests"
   git push -u origin release/v2026.11.11a0
   ```
5. **Open Pull Request**:
   - Open a PR targeting `main` using `gh pr create`.
   - Monitor CI check status and hand off to maintainer for merging.
