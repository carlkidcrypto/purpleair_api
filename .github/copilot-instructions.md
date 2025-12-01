# GitHub Copilot Code Review Instructions

## Review Philosophy
- Only comment when you have HIGH CONFIDENCE (>80%) that an issue exists
- Be concise: one sentence per comment when possible
- Focus on actionable feedback, not observations
- When reviewing text, only comment on clarity issues if the text is genuinely confusing or could lead to errors. "Could be clearer" is not the same as "is confusing" - stay silent unless HIGH confidence it will cause problems

## Priority Areas (Review These)

### Security & Safety
- Unsafe code blocks without justification
- Command injection risks (shell commands, user input)
- Path traversal vulnerabilities
- Credential exposure or hardcoded secrets
- Missing input validation on external data
- Improper error handling that could leak sensitive info

### Correctness Issues
- Logic errors that could cause panics or incorrect behavior
- Race conditions in async code
- Resource leaks (files, connections, memory)
- Off-by-one errors or boundary conditions
- Incorrect error propagation (using bare `except` or failing to propagate exceptions appropriately)
- Optional types that don't need to be optional
- Booleans that should default to false but are set as optional
- Error context that doesn't add useful information (e.g., `raise Exception("Failed to do X")` when the exception already describes the failure)
- Overly defensive code that adds unnecessary checks
- Unnecessary comments that just restate what the code already shows (remove them)

### Architecture & Patterns
- Code that violates existing patterns in the codebase
- Missing error handling (should use `try`/`except` and propagate exceptions appropriately)
- Async/await misuse or blocking operations in async functions
- Incorrect or missing implementation of special methods (e.g., `__str__`, `__eq__`)



## Project-Specific Context

- This is a Python 3 project using virtual environments and pip for dependency management
- Core modules: `purpleair_api`
- Error handling: Use `try`/`except` blocks and propagate exceptions with context; avoid bare `except` and do not use `sys.exit()` in library code
- Async runtime: asyncio
- See HOWTOAI.md for AI-assisted code standards
- MCP protocol implementations require extra scrutiny

## CI Pipeline Context

**Important**: You review PRs immediately, before CI completes. Do not flag issues that CI will catch.

### What Our CI Checks

**Black formatting** (`.github/workflows/black.yml`):
- Runs `psf/black` action to check code formatting
- Triggered on changes to Python files, tests, or setup files

**Tests** (`.github/workflows/tests.yml`):
- Runs unit tests via `coverage run -m unittest` on Ubuntu, macOS, and Windows
- Tests against Python 3.10, 3.11, 3.12, 3.13, and 3.14
- Uploads coverage reports to Codecov
- Uses pip to install: wheel, setuptools, pip, coverage, requests_mock

**Sphinx docs** (`.github/workflows/sphinx_build.yml`):
- Builds documentation from Sphinx sources
- Checks RST files and documentation configuration

**Setup steps CI performs:**
- Sets up Python environment with caching for pip packages
- Installs dependencies: wheel, setuptools, pip, coverage, requests_mock
- Runs tests across multiple OS platforms and Python versions

**Key insight**: CI does NOT run flake8, mypy, isort, or pydocstyle. Focus reviews on correctness, security, and architecture issues rather than style that Black will catch.

## Skip These (Low Value)

Do not comment on:
- **Black formatting** - CI handles this (black.yml)
- **Test failures** - CI handles this (tests.yml runs full unittest suite)
- **Missing test dependencies** - CI installs coverage and requests_mock
- **Minor naming suggestions** - unless truly confusing
- **Suggestions to add comments** - for self-documenting code
- **Refactoring suggestions** - unless there's a clear bug or maintainability issue
- **Multiple issues in one comment** - choose the single most critical issue
- **Logging suggestions** - unless for errors or security events (the codebase needs less logging, not more)
- **Pedantic accuracy in text** - unless it would cause actual confusion or errors. No one likes a reply guy
- **Type hints** - project does not use mypy or type checking in CI
- **Import ordering** - project does not use isort in CI
- **Docstring style** - project does not use pydocstyle in CI

## Response Format

When you identify an issue:
1. **State the problem** (1 sentence)
2. **Why it matters** (1 sentence, only if not obvious)
3. **Suggested fix** (code snippet or specific action)

Example:
```
This could raise an IndexError if the list is empty; consider using `list[0]` only after checking the length or use `list[0] if list else None`.
```

## When to Stay Silent

If you're uncertain whether something is an issue, don't comment. False positives create noise and reduce trust in the review process.