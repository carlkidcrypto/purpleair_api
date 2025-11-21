# Agent Instructions Update Required

## Summary
The agent instructions file in `.github/agents/` references workflows that do not exist in this repository. This document outlines what needs to be updated.

## Current State vs Agent Instructions

### Workflows That EXIST in Repository:
1. ✅ `.github/workflows/black.yml` - Python code formatting with Black
2. ✅ `.github/workflows/build_and_publish_to_pypi.yml` - PyPI package publishing
3. ✅ `.github/workflows/build_and_publish_to_test_pypi.yml` - Test PyPI publishing
4. ✅ `.github/workflows/sphinx_build.yml` - Sphinx documentation building
5. ✅ `.github/workflows/tests.yml` - Unit tests across multiple OS/Python versions

### Workflows Referenced in Agent Instructions But NOT in Repository:
1. ❌ `.github/workflows/auto_change_log.yml` - Not present
2. ❌ `.github/workflows/clang_format.yml` - Not applicable (Python project, no C++ code)
3. ❌ `.github/workflows/codeql.yml` - Not present

## Recommended Agent Instruction Updates

### Remove These Sections:
```
- Ensure that `.github/workflows/clang_format.yml` focuses on
    linting/formatting c++ code with clang-format
```
**Reason:** This is a Python-only project. There is no C++ code, so clang-format is not applicable.

### Optional Removals (if not planning to add these workflows):
```
- Ensure that `.github/workflows/auto_change_log.yml` focuses on
    updating/running the `changelog.md updating chore`.
```
**Reason:** This workflow doesn't exist and changelog management is currently manual.

```
- Ensure that `.github/workflows/codeql.yml` focuses on running GitHub
    codeql
```
**Reason:** This workflow doesn't exist and CodeQL security scanning is not currently configured.

## Recommended Updated Agent Instructions

```
You are a Github Workflow operations specialist focused exclusively on the
contents of `.github/workflows/` in this repository. Do not modify code outside
`.github/workflows/` or project-wide settings unless explicitly instructed.

Focus on the following instructions:
- Ensure that .github/workflows/ pass reliably and consistently within
    their runners
- Ensure that `.github/workflows/black.yml` focuses on
    linting/formatting python code with Black
- Ensure that `.github/workflows/build_and_publish_to_pypi.yml` focuses on
    building and publishing packages to PyPI (source distribution only)
- Ensure that `.github/workflows/build_and_publish_to_test_pypi.yml` focuses on
    building and publishing packages to Test PyPI (source distribution only)
- Ensure that `.github/workflows/sphinx_build.yml` focuses on building the
    sphinx documentation to attach to published releases
- Ensure that `.github/workflows/tests.yml` focuses on running
    `tests` using native dependencies across multiple OS and Python versions.
    Comments on PRs whether success or failure of all unit tests
- Ensure that workflows cache items that are commonly downloaded like pip packages
- Ensure that workflows all trigger when they are updated
- Ensure all GitHub Actions use hash-based SHA pinning for security
```

## Note on Project Type
This is a **Python-only project** for interacting with the PurpleAir API. The repository contains:
- Python source code (`purpleair_api/`)
- Python tests (`tests/`)
- Sphinx documentation (`sphinx_docs_build/`)
- Python packaging files (`setup.py`, `setup.cfg`)

There is **no C++ code**, so C++ related workflows (like clang-format) are not applicable.

## Actions Taken in This PR
All existing workflows have been updated with:
1. ✅ Hash-based SHA pinning for all GitHub Actions (security enhancement)
2. ✅ Pip caching for faster builds (performance optimization)
3. ✅ Workflows trigger on their own file changes (improved CI coverage)
4. ✅ All YAML syntax validated

See `.github/WORKFLOW_DOCUMENTATION.md` for detailed information about each workflow.
