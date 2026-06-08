---
name: Coverage Autofix Every 3 Days

on:
  schedule:
    - cron: "0 9 */3 * *"
  workflow_dispatch:
  skip-if-match:
    query: "is:pr is:open head:automation/coverage-autofix-every-3-days label:automated-pr"

permissions:
  actions: read
  contents: read

safe-outputs:
  create-pull-request:
    title-prefix: "[coverage-autofix]"
    labels:
      - automated-pr
    draft: true
    preserve-branch-name: true
    if-no-changes: ignore

timeout-minutes: 45

network: defaults

tools:
  edit:
  bash: true

engine:
  id: copilot
  model: claude-sonnet-4.6

Run an end-to-end coverage health check for the Python test suite, then propose and implement minimal, safe fixes that improve coverage and reliability.

## Hard Requirements

- Focus only on this repository.
- Keep changes scoped and low-risk.
- Prefer tests first when improving coverage.
- Do not open a new pull request if an open automation PR already exists for branch `automation/coverage-autofix-every-3-days`.
- If no meaningful change is needed, make no file edits and end cleanly.

## Coverage Check Procedure

1. Prepare Python dependencies and run Python tests with coverage:
   - `python -m pip install --upgrade pip wheel setuptools`
   - `python -m pip install -r tests/requirements.txt`
   - `cd tests && coverage run -m unittest`
   - `coverage json -o coverage.json`
   - Read coverage from `coverage.json` when available.
   - Also generate an XML report for detailed line-level analysis: `coverage xml -o coverage.xml`

2. Identify coverage gaps:
   - Parse `coverage.xml` or `coverage.json` to find modules with less than 99% line coverage.
   - Note which specific lines/branches are uncovered.
   - Focus on modules under `purpleair_api/`: `PurpleAirAPI.py`, `PurpleAirReadAPI.py`, `PurpleAirWriteAPI.py`, `PurpleAirLocalAPI.py`, `PurpleAirAPIHelpers.py`, `PurpleAirAPIError.py`, `PurpleAirAPIConstants.py`.

3. Determine if action is needed:
   - If Python coverage is below 99%, or tests reveal clear reliability gaps, create targeted fixes.
   - If current coverage looks healthy and no concrete improvement is justified, do not change code.

## Fix Strategy

- Prioritize:
  - Adding missing test coverage for uncovered branches/paths in `tests/`.
  - Fixing brittle tests.
  - Small correctness fixes discovered while writing tests.
- Test file naming convention: `tests/test_<module_name>.py` (e.g., `tests/test_purpleair_read_api.py`).
- New tests must use `unittest` and `requests_mock` for HTTP mocking (already used in the repo).
- All code must be formatted with Black (`python -m black . --line-length 100`).
- Avoid broad refactors or unrelated formatting churn.
- Keep commits coherent and reviewable.

## Pull Request Output

When changes exist, create exactly one PR using this fixed branch name:

- Branch: `automation/coverage-autofix-every-3-days`
- Base: `main`
- Title style: `[coverage-autofix] <short summary>`
- PR body must include:
  - Python coverage before/after (by module if measurable)
  - Summary of tests added/updated
  - Any limitations or follow-up recommendations

After creating the PR, attempt a best-effort follow-up label step:

- Add supplemental labels to the created PR when possible: `coverage`, `tests`, `python`.
- Treat this as non-critical metadata enrichment. If supplemental labeling fails, do not treat the run as a primary failure and do not abandon the created PR.

If no changes are required, report that coverage checks passed without actionable improvements.


