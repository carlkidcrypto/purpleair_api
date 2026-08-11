---
name: Matter Standards Watcher
description: Monitor Matter standards releases and propose synchronized converter, test, and documentation updates.
on:
  schedule:
    - cron: "0 9 1 * *"
  workflow_dispatch:
  skip-if-match:
    query: "is:pr is:open head:automation/matter-standards-watcher label:automated-pr"

permissions:
  actions: read
  contents: read
  copilot-requests: write

safe-outputs:
  create-pull-request:
    title-prefix: "[matter-standards]"
    labels:
      - automated-pr
    draft: true
    preserve-branch-name: true
    if-no-changes: ignore
    allowed-files:
      - purpleair_api/PurpleAirMatterConverter.py
      - tests/test_purpleair_matter_converter.py
      - purpleair_api/README.rst
      - README.rst
      - docs/**
      - sphinx_docs_build/source/**

timeout-minutes: 45

network:
  allowed:
    - csa-iot.org
    - www.csa-iot.org
    - github
    - python

tools:
  edit:
  bash: true

model: claude-sonnet-5
engine:
  id: copilot
---

## Matter Standards Watcher

Monitor the Connectivity Standards Alliance Matter specifications and keep this repository's
PurpleAir-to-Matter implementation synchronized with the latest published standard that affects
the converter. The repository currently documents Matter 1.5.1 as its baseline.

## Authoritative sources

- CSA specifications index: https://csa-iot.org/developer-resource/specifications/
- Matter specification documents and release notes linked from that index
- The Matter device library and cluster definitions in the published specification
- https://github.com/project-chip/matter.js only as a secondary implementation reference; never
  treat it as authoritative when it conflicts with the CSA specification

Do not infer a standards change from an unavailable page, a search-result snippet, or an
implementation library alone. If the CSA source cannot be fetched or the apparent change cannot
be verified against an authoritative Matter document, stop cleanly without editing files or
opening a PR.

## Review scope

Inspect the current Matter version, device type IDs, cluster IDs, attribute IDs, enum values,
measurement units, scaling/encoding rules, required and optional cluster mappings, and references
in `purpleair_api/PurpleAirMatterConverter.py`. Check the corresponding behavior in
`tests/test_purpleair_matter_converter.py` and the public explanations in `README.rst`,
`purpleair_api/README.rst`, `docs/**`, and `sphinx_docs_build/source/**`.

## Required steps

1. Fetch the CSA specifications index and identify the newest published Matter release or errata
   that is relevant to the converter. Record the document title, version, publication date, and
   stable URL. Do not treat a draft or preview as the current release unless the source explicitly
   marks it as published.
2. Compare the authoritative device-library and cluster definitions with the implementation. Look
   specifically for changed identifiers, names, enum values, required/optional status, units,
   numeric ranges, scaling, and deprecations. Distinguish a genuine standards change from a
   documentation-only wording change.
3. If no verified, actionable Matter change affects this converter, call `noop` with a concise
   explanation and the source checked. Do not edit files.
4. If a verified change exists, update the implementation and its focused tests together. Preserve
   the public API unless the standard requires a change, and do not add support for speculative or
   vendor-specific behavior.
5. Update all affected user-facing documentation and references, including the documented Matter
   version and stable source links. Do not edit generated Sphinx HTML or doctree artifacts.
6. Run the narrow converter tests first, then the repository's relevant Python test command. If
   tests fail for an unrelated pre-existing reason, do not hide the failure; report it in the PR
   body and avoid unrelated fixes.
7. Review the diff for accidental changes, stale Matter 1.5.1 references, inconsistent IDs or
   units, and documentation that claims support beyond what the implementation and tests cover.
8. Create one draft pull request on branch `automation/matter-standards-watcher` against `main`
   using the configured safe output. Include the authoritative source, old and new Matter versions,
   exact specification sections, each code/test/doc change, validation commands and results, and
   any remaining compatibility concern.

## Constraints

- Only modify files allowed by `safe-outputs.create-pull-request.allowed-files`.
- Do not modify generated documentation under `docs/html/**` or `docs/doctrees/**`.
- Do not remove existing mappings solely because a secondary implementation omits them.
- Do not change unrelated PurpleAir API behavior, formatting, dependencies, or release metadata.
- Keep the patch small and internally consistent; one standards update per PR.
- If the source is unavailable, ambiguous, or unchanged, use `noop` and leave the repository
  untouched.

## Safe output

- Use the configured `create-pull-request` output only after verified implementation or documentation
  changes and successful validation.
- Use `noop` when no verified change is needed, when the source cannot be validated, or when an
  existing open watcher PR already covers the same release.