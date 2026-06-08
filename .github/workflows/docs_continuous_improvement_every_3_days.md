---
name: Docs Continuous Improvement Every 3 Days

on:
  workflow_dispatch:
  schedule:
    - cron: "0 9 */3 * *"
  skip-if-match:
    query: "is:pr is:open head:automation/docs-continuous-improvement label:documentation label:automated-pr"

permissions:
  actions: read
  contents: read

safe-outputs:
  create-pull-request:
    title-prefix: "[docs-improvement]"
    labels:
      - documentation
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

- `README.rst`
- `HOWTOAI.md`
- `docs/**`
- `sphinx_docs_build/**` (RST source files, `conf.py`, `index.rst`, etc. — not generated HTML output)
- inline docstrings in Python files under `purpleair_api/**`
- comments/doc text in interface/docs-related files where clearly incorrect or missing

## Goals

- Fix typos, grammar, and broken wording
- Fix inaccurate or misleading statements
- Improve clarity where current text could cause user confusion
- Add or correct missing/incorrect Python docstrings for public functions/classes in `purpleair_api/`
- Keep edits small and focused each run (no massive rewrites)

## Constraints

- Do not change API behavior or runtime logic; documentation-only edits
- Avoid changing generated artifacts (e.g., `docs/html/**`, compiled Sphinx output)
- If no meaningful improvements are found, do not edit files

## Pull Request

If changes are made, create or update one PR:

- Branch: `automation/docs-continuous-improvement`
- Base: `main`
- Title style: `[docs-improvement] <short summary>`

PR body must include:

- Files updated
- Types of improvements (typos, clarifications, docstrings, etc.)
- Any follow-up documentation gaps discovered





