---
name: Docs Continuous Improvement Every 3 Days
on:
  workflow_dispatch:
  schedule:
    - cron: "0 9 */3 * *"
  skip-if-match:
    query: 'is:pr is:open head:automation/docs-continuous-improvement label:documentation label:automated-pr'
permissions:
  actions: read
  contents: read
  copilot-requests: write
safe-outputs:
  create-pull-request:
    title-prefix: "[docs-improvement] "
    labels: [documentation, automated-pr]
    draft: true
    preserve-branch-name: true
    if-no-changes: "ignore"
    allowed-base-branches: [main]
timeout-minutes: 15
max-ai-credits: 25
model: claude-sonnet-5
engine:
  id: copilot
tools:
  edit:
  bash: true
---

# Documentation Continuous Improvement

Review and improve repository documentation gradually over time.

## Scope

Audit and improve:

- `README.rst`
- `HOWTOAI.rst`
- `HOWTO_MATTER.rst`
- `sphinx_docs_build/source/*.rst`
- inline docstrings in Python files under `purpleair_api/**`
- comments/doc text in interface/docs-related files where clearly incorrect or missing

## Hard Requirements & Scope Limits (Token & AIC Optimization)

0. **Deterministic Audit Helper**:
   Execute the audit helper script to check for common typos, broken class casings, and syntax issues before doing any manual file reads:
   ```bash
   python3 .github/scripts/audit_docs.py
   ```
   If issues are found, you may use `python3 .github/scripts/audit_docs.py --fix` to auto-resolve them.

- **Single-Target Scope**: Limit each run to at most 1–2 documentation files or 1 Python module's docstrings (1–3 focused improvements maximum). Do not attempt a repo-wide audit in a single run.
- **Bounded file reads**: Files larger than 20 KB must **not** be read in full. Use targeted `grep`, `head`, `tail`, or line-range views.
- **Turn Budget**: Complete inspection and edits within 10–12 turns. If no clear improvements are found, stop cleanly without editing.

## Goals

- Fix typos, grammar, and broken wording
- Fix inaccurate or misleading statements
- Improve clarity where current text could cause user confusion
- Add or correct missing/incorrect Python docstrings for public functions/classes
- Keep edits small and focused each run (no massive rewrites)

## Constraints

- Do not change API behavior or runtime logic; documentation-only edits
- Avoid changing generated artifacts (files under `docs/` or compiled HTML)
- If no meaningful improvements are found, do not edit files
- If Python docstrings were modified, ensure formatting matches Black:
  ```bash
  python -m pip install black
  black <modified_files>
  ```

## Pull Request

If changes are made, create or update one PR:

- Branch: `automation/docs-continuous-improvement`
- Base: `main`
- Title style: `[docs-improvement] <short summary>`

PR body must include:

- Files updated
- Types of improvements (typos, clarifications, docstrings, etc.)
- Any follow-up documentation gaps discovered