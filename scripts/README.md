# Release Scripts

This folder contains scripts used for repository release maintenance.

## `release.sh`

`release.sh` updates the current package version across the tracked release metadata and user-facing source documentation.

### Requirements

Run it from a Git checkout of this repository with:

- Bash
- Git
- Perl
- `sed`

The script uses the repository root found by `git rev-parse`, so it may be started from any directory inside the checkout.

### Usage

Show which files would change without editing anything:

```bash
bash scripts/release.sh --dry-run 1.5.1
```

Apply a release bump. When the old version is omitted, it is read from the `version =` setting in `setup.cfg`:

```bash
bash scripts/release.sh 1.5.1
```

An explicit old version can be supplied when the repository contains mixed metadata or when correcting a previous release bump:

```bash
bash scripts/release.sh 1.5.1 1.5.0
```

Supported version forms are stable releases such as `1.5.1` and prereleases such as `1.5.1a1`, `1.5.1b1`, and `1.5.1rc1`.

### Files and validation

The script searches tracked text files for the old version and updates matching active release references. It requires the old version to be present in both:

- `setup.cfg`
- `sphinx_docs_build/source/conf.py`

The current README and other active tracked source documentation are updated when they contain the old version.

The script deliberately excludes:

- `CHANGELOG.md`, which should be maintained as a release-history document
- `docs/html/**`, which is generated documentation
- Historical documentation under `docs/html_v*/`
- Sphinx doctrees under `docs/doctrees/`
- Build output under `build/`
- The local `python3.12.venv/` environment
- Generated agentic workflow lock files under `.github/workflows/`

After an actual bump, the script checks that no old-version references remain in the active tracked scope. It exits without changes when the requested version is already current.

### Release checklist

1. Run the dry run and review the selected files.
2. Run the script with the target release version.
3. Update `CHANGELOG.md` separately with the release notes and date.
4. Build or regenerate published documentation through the normal Sphinx process when required.
5. Run the repository test suite before tagging the release.
