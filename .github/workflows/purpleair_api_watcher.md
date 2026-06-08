---
name: PurpleAir API Watcher

on:
  schedule:
    - cron: "24 10 * * 1"
  workflow_dispatch:
  skip-if-match:
    query: "is:pr is:open head:automation/purpleair-api-sync label:automated-pr"

permissions:
  actions: read
  contents: read

safe-outputs:
  create-pull-request:
    title-prefix: "[api-sync]"
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
- Reflect any confirmed changes in `purpleair_api/PurpleAirAPIConstants.py` and related modules.
- Keep `docs/purpleair_api_snapshot.txt` as a plain-text content snapshot to track what was last seen.
- Open a PR only when meaningful changes are found.

## Steps

### 1. Fetch the current API documentation

Retrieve the HTML source of the PurpleAir API documentation page:

```bash
curl -fsSL "https://api.purpleair.com/" -o /tmp/gh-aw/agent/api_current.html

If the fetch fails (non-zero exit, empty file, or clear HTTP error response), log the failure, skip all further steps, and end cleanly without opening a PR.

Extract the human-readable text content from the HTML (strip tags, collapse whitespace) into a flat text file for diffing:

```bash
python3 - <<'EOF'
import re, sys

with open("/tmp/gh-aw/agent/api_current.html", "r", encoding="utf-8", errors="replace") as f:
    html = f.read()

# Remove scripts and styles
html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
# Strip all remaining tags
text = re.sub(r"<[^>]+>", " ", html)
# Collapse whitespace
text = re.sub(r"[ \t]+", " ", text)
text = re.sub(r"\n\s*\n+", "\n\n", text)

with open("/tmp/gh-aw/agent/api_current_text.txt", "w", encoding="utf-8") as f:
    f.write(text.strip())
EOF
```

### 2. Compare with the stored snapshot

Check whether a previous snapshot file exists at `docs/purpleair_api_snapshot.txt` in the repository.

- If the file does not exist yet, treat the entire current content as "new" and proceed to update steps.
- If the file exists, compute a diff:
  ```bash
  diff docs/purpleair_api_snapshot.txt /tmp/gh-aw/agent/api_current_text.txt > /tmp/gh-aw/agent/api_diff.txt || true
  ```
  If `/tmp/gh-aw/agent/api_diff.txt` is empty (no diff), log "No API documentation changes detected." and stop cleanly with no file edits.

### 3. Analyze the diff for actionable changes

Read the diff and the full current text to identify:

**Field names** — Look for any sensor data field names that appear in or near tables or lists on the API page. Common patterns include strings like `pm2.5`, `temperature`, `humidity`, `pm1.0`, `pm10.0`, `pressure`, `voc`, `rssi`, `uptime`, `latitude`, `longitude`, `altitude`, `confidence`, `channel_state`, `channel_flags`, `led_brightness`, `firmware_version`, `location_type`, `date_created`, `last_seen`, `last_modified`, etc. — as well as their `_a`, `_b`, `_atm`, `_cf_1`, `_alt`, `_10minute`, `_30minute`, `_60minute`, `_6hour`, `_24hour`, `_1week` variants. Also look for ThingSpeak-related fields: `primary_id_a`, `primary_key_a`, `secondary_id_a`, `secondary_key_a`, and their `_b` counterparts.

**Endpoints** — Look for new or changed `GET`, `POST`, `PUT`, `DELETE` endpoint paths (e.g., `/v1/sensors`, `/v1/groups`, `/v1/members`).

**Variable descriptions** — Note any human-readable descriptions of fields that could improve inline comments in the codebase.

Classify changes as:
- **New fields**: present in the current page but not in `ACCEPTED_FIELD_NAMES_DICT` in `purpleair_api/PurpleAirAPIConstants.py`.
- **Removed fields**: present in `ACCEPTED_FIELD_NAMES_DICT` but no longer mentioned in the API docs.
- **Renamed fields**: a strong indication (e.g., old name replaced by new name in context) that a field was renamed.
- **New or changed endpoints**: changes to the API endpoint paths, parameters, or descriptions.
- **Description/comment improvements**: updated wording or added details about what a field means.

If none of these actionable changes are identified from the diff, log "API documentation changed but no actionable code updates required." and proceed only to update the snapshot file (step 4), then stop without opening a PR.

### 4. Update the snapshot file

Overwrite `docs/purpleair_api_snapshot.txt` with the contents of `/tmp/gh-aw/agent/api_current_text.txt`. This must happen on every run where the content has changed, regardless of whether code changes were also made.

### 5. Apply code updates

For each actionable change identified:

**For new fields** — Add an entry to `ACCEPTED_FIELD_NAMES_DICT` in `purpleair_api/PurpleAirAPIConstants.py`:
- Use the same key string as it appears in the API docs.
- Choose a sensible default value type: `0` for integer fields, `0.0` for float fields, `""` for string fields.
- Place the new entry under the appropriate comment group (e.g., "PM2.5 fields", "Environmental fields", "Station information"). If no group fits, append before the ThingSpeak block.
- Add or update an inline comment if the API docs provide a useful description of the field.

**For removed fields** — Do NOT automatically remove entries from `ACCEPTED_FIELD_NAMES_DICT`. Instead, add a comment above the entry:
```python
# NOTE: This field may have been removed from the PurpleAir API as of <date>. Verify before deleting.
```

**For renamed fields** — Do NOT automatically rename. Add a comment above the old entry noting the suspected rename, and add the new name as a new entry if it is confirmed present in the API docs.

**For improved descriptions** — Update the inline comments on existing entries to reflect better wording from the API docs.

**For new or changed endpoints** — If there is a constant string defining an endpoint path (e.g., in `PurpleAirAPIConstants.py` or `PurpleAirAPIHelpers.py`), update it. If a wholly new endpoint is documented, add a comment noting it exists so a developer can implement it.

After all edits, format the changed Python files with Black:

```bash
python3 -m pip install --quiet black
python3 -m black purpleair_api/ --line-length 100
```

### 6. Create a pull request

If any files were changed (code or snapshot), create or update a PR:

- Branch: `automation/purpleair-api-sync`
- Base: `main`
- Title style: `[api-sync] Sync with PurpleAir API documentation <YYYY-MM-DD>`

PR body must include:

- Date the API page was fetched.
- Summary of what changed in the diff (new fields, removed fields, endpoint changes, etc.).
- List of files modified and the nature of each change.
- A note that removed fields were flagged with comments but not deleted, and that renames require human review before merging.
- Any follow-up items for a human reviewer (e.g., fields needing new API method implementations, suspected removals to verify).

## Constraints

- Only modify `purpleair_api/PurpleAirAPIConstants.py`, `purpleair_api/PurpleAirAPIHelpers.py`, and `docs/purpleair_api_snapshot.txt` unless a change clearly and unambiguously requires touching another file.
- Do not implement new API methods; only update constants, field definitions, and inline comments.
- Do not delete existing field entries from `ACCEPTED_FIELD_NAMES_DICT`; use comments to flag suspected removals.
- Do not rename existing fields without explicit human approval; add the new name instead.
- If the API page is unreachable or returns an error, stop without modifying any files.
- If no actionable code changes are found, still update the snapshot file if the page content changed, but do not open a PR solely for the snapshot update — commit it to the automation branch silently.
- Keep all Python code Black-formatted with line length 100.
- Always include the snapshot file update in the same PR as any code changes.






