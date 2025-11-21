# GitHub Workflows Documentation

## Current Workflows (as of November 2024)

This repository contains the following GitHub Actions workflows:

### 1. black.yml
**Purpose:** Lint and format Python code using Black  
**Triggers:** 
- Push to main branch (for .py files and workflow file changes)
- Pull requests to main branch (for .py files and workflow file changes)

**Actions Used (SHA-pinned):**
- actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 (v4.2.2)
- tj-actions/changed-files@c3a1bb2c992d77180ae65be6ae6c166cf40f857c (v46.0.1)
- psf/black@17d0bb0b67b589b7a5bc1dce983f57f93aac88a2 (25.9.0)

### 2. build_and_publish_to_pypi.yml
**Purpose:** Build and publish packages to PyPI using source distribution  
**Triggers:** 
- Release published
- Manual workflow dispatch

**Actions Used (SHA-pinned):**
- actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 (v4.2.2)
- actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b (v5.3.0)
- pypa/gh-action-pypi-publish@f7600683efdcb7656dec5b0f46560eaefbacd9a2 (release/v1.13)

**Features:**
- Python 3.11
- Pip caching enabled
- Uses pypa/build for building source tarball

### 3. build_and_publish_to_test_pypi.yml
**Purpose:** Build and publish packages to Test PyPI for testing before production release  
**Triggers:** 
- Push to main branch (for setup.py, setup.cfg, or workflow file changes)

**Actions Used (SHA-pinned):**
- actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 (v4.2.2)
- tj-actions/changed-files@c3a1bb2c992d77180ae65be6ae6c166cf40f857c (v46.0.1)
- actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b (v5.3.0)
- pypa/gh-action-pypi-publish@f7600683efdcb7656dec5b0f46560eaefbacd9a2 (release/v1.13)

**Features:**
- Python 3.11
- Pip caching enabled
- Skip existing packages on Test PyPI
- Uses pypa/build for building source tarball

### 4. sphinx_build.yml
**Purpose:** Build Sphinx documentation for pull requests and releases  
**Triggers:** 
- Push to main branch (for sphinx_docs_build/** or workflow file changes)
- Pull requests to main branch (for sphinx_docs_build/** or workflow file changes)

**Actions Used (SHA-pinned):**
- actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 (v4.2.2)
- tj-actions/changed-files@c3a1bb2c992d77180ae65be6ae6c166cf40f857c (v46.0.1)
- actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b (v5.3.0)
- carlkidcrypto/os-specific-runner@0396cb2145e0ba19f3b87ff667de7dce2a4ce0b3 (v2.1.1)
- actions/upload-artifact@6f51ac03b9356f520e9adb1b1b7802705f340c2b (v4.4.3)

**Features:**
- Python 3.11
- Pip caching enabled
- Uploads HTML documentation as artifact
- Fails on Sphinx warnings (-W flag)

### 5. tests.yml
**Purpose:** Run unit tests across multiple OS and Python versions  
**Triggers:** 
- Push to main branch (for .py files, tests/**, or workflow file changes)
- Pull requests to main branch (for .py files, tests/**, or workflow file changes)

**Actions Used (SHA-pinned):**
- actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 (v4.2.2)
- tj-actions/changed-files@c3a1bb2c992d77180ae65be6ae6c166cf40f857c (v46.0.1)
- actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b (v5.3.0)
- carlkidcrypto/os-specific-runner@0396cb2145e0ba19f3b87ff667de7dce2a4ce0b3 (v2.1.1)
- codecov/codecov-action@3627e82763ce9c92c8de489a8c30f2e23c62c44b (v5.1.2)

**Features:**
- Multi-OS testing: Ubuntu, macOS, Windows
- Multi-Python testing: 3.9, 3.10, 3.11, 3.12, 3.13
- Pip caching enabled
- Coverage reporting to Codecov
- Matrix strategy with fail-fast disabled

## Workflows NOT in This Repository

The following workflows were mentioned in agent instructions but do not exist in this Python-focused repository:

- **auto_change_log.yml** - Not present (changelog management not automated)
- **clang_format.yml** - Not applicable (no C++ code in this Python project)
- **codeql.yml** - Not present (CodeQL security scanning not configured)

## Security Enhancements Applied

All workflows now use **hash-based SHA pinning** instead of tag-based versioning for third-party GitHub Actions. This prevents:
- Supply chain attacks via compromised action repositories
- Unexpected behavior from action updates
- Tag moving to malicious commits

Format: `uses: action/name@<full-sha-hash> # version-tag-comment`

## Performance Optimizations

All workflows that use Python now have pip caching enabled via:
```yaml
uses: actions/setup-python@<sha>
with:
  python-version: "X.Y"
  cache: 'pip'
```

This reduces workflow execution time by caching pip packages between runs.

## Workflow Trigger Improvements

All workflows now trigger when their own workflow file is modified, ensuring:
- Workflow changes are tested before merge
- CI validates workflow syntax and functionality
- Developers can see workflow changes in action

---

**Note for Agent Instructions:** The agent instructions should be updated to remove references to:
- `clang_format.yml` (not applicable to Python projects)
- Consider whether `auto_change_log.yml` and `codeql.yml` should be added or removed from instructions
