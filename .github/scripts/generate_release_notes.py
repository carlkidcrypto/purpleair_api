#!/usr/bin/env python3
"""Generate and update GitHub release notes for purpleair_api.

This script automates the generation of high-signal, human-readable release
notes for tagged purpleair_api releases, following the specification in
``.github/workflows/auto_release_notes.md``.

It deterministically:
1. Identifies release context (tag, prerelease status, PyPI version).
2. Resolves the appropriate base tag according to semantic priority rules.
3. Extracts and categorizes commit history and pull request references into
   standard themes based on file paths and conventional prefixes.
4. Generates a formatted release note matching the purpleair_api template.
5. Optionally patches the GitHub release via the GitHub CLI (gh).

Usage:
    # Process a single release tag (dry-run):
    python3 .github/scripts/generate_release_notes.py --tag v1.5.0

    # Process and publish a single release tag:
    python3 .github/scripts/generate_release_notes.py --tag v1.5.0 --publish

    # Process the latest published release:
    python3 .github/scripts/generate_release_notes.py --latest --publish

    # Backfill all existing releases (chronological order):
    python3 .github/scripts/generate_release_notes.py --backfill --publish
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPO = "carlkidcrypto/purpleair_api"
DEFAULT_PACKAGE = "purpleair_api"

# Standard theme categories in priority display order
THEME_CATEGORIES = [
    "Features / Enhancements",
    "Bug Fixes",
    "API / Core Library",
    "Tests",
    "Packaging",
    "CI / Workflows",
    "Documentation",
    "Dependencies",
    "Chores / Misc",
]


def run_cmd(
    cmd: list[str],
    cwd: Path | None = None,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> str:
    """Run a subprocess command and return stdout."""
    effective_env = os.environ.copy()
    if env:
        effective_env.update(env)
    if "/opt/homebrew/bin" not in effective_env.get("PATH", ""):
        effective_env["PATH"] = f"/opt/homebrew/bin:{effective_env.get('PATH', '')}"

    res = subprocess.run(
        cmd,
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
        env=effective_env,
    )
    if check and res.returncode != 0:
        raise RuntimeError(
            f"Command failed (exit {res.returncode}): {' '.join(cmd)}\nStderr: {res.stderr}"
        )
    return res.stdout.strip()


def ensure_git_tags(repo_root: Path = REPO_ROOT) -> None:
    """Ensure git tags are fetched, handling shallow repositories gracefully."""
    try:
        is_shallow = run_cmd(
            ["git", "rev-parse", "--is-shallow-repository"],
            cwd=repo_root,
            check=False,
        )
        if is_shallow.strip() == "true":
            run_cmd(
                ["git", "fetch", "--tags", "--unshallow"],
                cwd=repo_root,
                check=False,
            )
        else:
            run_cmd(["git", "fetch", "--tags"], cwd=repo_root, check=False)
    except Exception as exc:
        print(f"Warning: git tag fetch failed: {exc}", file=sys.stderr)


def get_git_tags(repo_root: Path = REPO_ROOT) -> set[str]:
    """Return all git tags present in the local repository."""
    out = run_cmd(["git", "tag"], cwd=repo_root, check=False)
    if not out:
        return set()
    return set(out.splitlines())


def get_all_releases(repo: str = DEFAULT_REPO) -> list[dict[str, Any]]:
    """Fetch all releases from GitHub API via gh cli in chronological order (oldest first)."""
    raw = run_cmd(
        [
            "gh",
            "api",
            f"/repos/{repo}/releases?per_page=100",
            "--paginate",
        ]
    )
    if not raw:
        return []
    releases = json.loads(raw)
    releases.sort(key=lambda r: r.get("created_at") or r.get("published_at") or "")
    return releases


def clean_title(title: str) -> str:
    """Clean PR and commit titles, removing PR numbers and release noise."""
    t = title.strip()
    t = re.sub(
        r"\s+by\s+@[\w-]+(?:\s+in\s+https://github\.com/[^\s]+)?",
        "",
        t,
        flags=re.IGNORECASE,
    )
    t = re.sub(r"\s*\(\s*#\d+\s*\)\s*$", "", t)
    t = re.sub(r"\s+#\d+\b", "", t)
    t = re.sub(
        r"^[\U00010000-\U0010ffff\u2600-\u27bf\u2b50\ufe0f\s]+",
        "",
        t,
    ).strip()
    return t


def rewrite_to_natural_language(title: str) -> str:
    """Rewrite terse commit messages to natural language with active verbs."""
    t = clean_title(title)

    # Detect conventional prefix like feat(scope): or fix:
    prefix_match = re.match(
        r"^(feat|fix|docs|test|tests|chore|ci|refactor|style|build|perf)(?:\([\w-]+\))?:\s*",
        t,
        flags=re.IGNORECASE,
    )
    prefix = prefix_match.group(1).lower() if prefix_match else ""

    # Detect bracket tag like [docs], [coverage-autofix]
    bracket_match = re.match(r"^\[([\w-]+)\]\s*", t)
    bracket_tag = bracket_match.group(1).lower() if bracket_match else ""

    t = re.sub(r"^\[[\w-]+\]\s*", "", t)
    t = re.sub(
        r"^(feat|fix|docs|test|tests|chore|ci|refactor|style|build|perf)(?:\([\w-]+\))?:\s*",
        "",
        t,
        flags=re.IGNORECASE,
    )
    t = t.strip()
    if not t:
        return title

    # Ensure capitalized
    t = t[0].upper() + t[1:]

    # Conjugate leading verb to 3rd person singular active
    verb_replacements: list[tuple[str, str]] = [
        (r"^(?:Add|Added)\b", "Adds"),
        (r"^(?:Fix|Fixed)\b", "Fixes"),
        (r"^(?:Update|Updated)\b", "Updates"),
        (r"^(?:Improve|Improved)\b", "Improves"),
        (r"^(?:Remove|Removed)\b", "Removes"),
        (r"^(?:Allow|Allowed)\b", "Allows"),
        (r"^(?:Support|Supported)\b", "Supports"),
        (r"^(?:Ensure|Ensured)\b", "Ensures"),
        (r"^(?:Refactor|Refactored)\b", "Refactors"),
        (r"^(?:Resolve|Resolved)\b", "Resolves"),
        (r"^(?:Prevent|Prevented)\b", "Prevents"),
        (r"^(?:Enable|Enabled)\b", "Enables"),
        (r"^(?:Disable|Disabled)\b", "Disables"),
        (r"^(?:Bump|Bumped)\b", "Bumps"),
        (r"^(?:Upgrade|Upgraded)\b", "Upgrades"),
        (r"^(?:Move|Moved)\b", "Moves"),
        (r"^(?:Clean|Cleaned)\b", "Cleans"),
        (r"^(?:Serialize|Serialized)\b", "Serializes"),
        (r"^(?:Handle|Handled)\b", "Handles"),
        (r"^(?:Align|Aligned)\b", "Aligns"),
        (r"^(?:Scope|Scoped)\b", "Scopes"),
        (r"^(?:Split|Splitted)\b", "Splits"),
        (r"^(?:Drop|Dropped)\b", "Drops"),
        (r"^(?:Harden|Hardened)\b", "Hardens"),
        (r"^(?:Correct|Corrected)\b", "Corrects"),
        (r"^(?:Introduce|Introduced)\b", "Introduces"),
        (r"^(?:Include|Included)\b", "Includes"),
        (r"^(?:Switch|Switched)\b", "Switches"),
        (r"^(?:Standardize|Standardized)\b", "Standardizes"),
        (r"^(?:Migrate|Migrated)\b", "Migrates"),
        (r"^(?:Optimize|Optimized)\b", "Optimizes"),
        (r"^(?:Configure|Configured)\b", "Configures"),
        (r"^(?:Adopt|Adopted)\b", "Adopts"),
    ]
    conjugated = False
    for pattern, replacement in verb_replacements:
        if re.search(pattern, t):
            t = re.sub(pattern, replacement, t)
            conjugated = True
            break

    # If no leading verb was matched, infer active verb from commit prefix/tag
    if not conjugated:
        known_active = (
            "Adds",
            "Fixes",
            "Updates",
            "Improves",
            "Removes",
            "Allows",
            "Supports",
            "Ensures",
            "Refactors",
            "Resolves",
            "Prevents",
            "Enables",
            "Disables",
            "Bumps",
            "Upgrades",
            "Moves",
            "Cleans",
            "Serializes",
            "Handles",
            "Aligns",
            "Scopes",
            "Splits",
            "Drops",
            "Hardens",
            "Corrects",
            "Introduces",
            "Includes",
            "Switches",
            "Standardizes",
            "Migrates",
            "Optimizes",
            "Configures",
            "Adopts",
        )
        if not any(t.startswith(f"{v} ") for v in known_active):
            first_char_lower = t[0].lower() + t[1:]
            if prefix == "fix":
                t = f"Fixes {first_char_lower}"
            elif prefix == "feat":
                t = f"Adds {first_char_lower}"
            elif prefix in ("docs",) or bracket_tag == "docs":
                t = f"Updates {first_char_lower}"
            elif prefix in ("test", "tests"):
                t = f"Adds {first_char_lower}"

    return t


def categorize_item(title: str, files: list[str]) -> str:
    """Categorize an item into one of the 9 standard themes."""
    title_lower = title.lower()

    # 1. Dependencies
    if (
        any(
            title_lower.startswith(p)
            for p in ["bump", "chore(deps)", "deps:", "chore(deps-dev)"]
        )
        or "dependabot" in title_lower
    ):
        return "Dependencies"
    if files and all(
        f
        in (
            "requirements.txt",
            "tests/requirements.txt",
        )
        for f in files
    ):
        return "Dependencies"

    # 2. CI / Workflows (priority over docs so .github/workflows/*.md isn't marked doc)
    if files and all(f.startswith(".github/") for f in files):
        return "CI / Workflows"
    if any(
        title_lower.startswith(p)
        for p in ["ci", "workflow", "workflows", "action", "actions"]
    ):
        return "CI / Workflows"

    # 3. Documentation
    if files and all(
        (f.startswith(("docs/", "sphinx_docs_build/")) or f.endswith((".rst", ".md")))
        and not f.startswith(".github/")
        for f in files
    ):
        return "Documentation"
    if any(title_lower.startswith(p) for p in ["docs", "doc:"]):
        return "Documentation"

    # 4. Tests
    if files and all(f.startswith("tests/") for f in files):
        return "Tests"
    if any(title_lower.startswith(p) for p in ["test", "tests"]):
        return "Tests"

    # 5. Packaging
    if (
        files
        and any(
            f
            in (
                "setup.py",
                "setup.cfg",
                "pyproject.toml",
                "requirements.txt",
            )
            for f in files
        )
        and not any(f.startswith("purpleair_api/") for f in files)
    ):
        return "Packaging"
    if any(
        title_lower.startswith(p)
        for p in [
            "packaging",
            "wheel",
            "pypi",
        ]
    ):
        return "Packaging"

    # 6. Core Library / Bug Fixes / Features
    touches_core = any(f.startswith("purpleair_api/") for f in files)
    is_bug = any(
        w in title_lower
        for w in [
            "fix",
            "bug",
            "patch",
            "error",
            "leak",
            "crash",
            "regression",
            "resolve",
            "prevent",
        ]
    )
    is_feat = any(
        w in title_lower
        for w in [
            "feat",
            "add",
            "support",
            "implement",
            "new",
            "allow",
            "introduce",
            "option",
        ]
    )

    if touches_core:
        if is_bug:
            return "Bug Fixes"
        elif is_feat:
            return "Features / Enhancements"
        return "API / Core Library"

    if is_bug:
        return "Bug Fixes"
    if is_feat:
        return "Features / Enhancements"

    return "Chores / Misc"


def parse_semver(tag: str) -> tuple[int, int, int, int, str] | None:
    """Parse a version tag into (major, minor, patch, is_stable, prerelease_suffix)."""
    m = re.match(r"^v?(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[.-]?([a-zA-Z0-9.-]+))?$", tag)
    if not m:
        return None
    major = int(m.group(1))
    minor = int(m.group(2) or 0)
    patch = int(m.group(3) or 0)
    suffix = m.group(4) or ""
    is_stable = 1 if not suffix else 0
    return (major, minor, patch, is_stable, suffix)


def determine_base_tag(
    current_release: dict[str, Any],
    all_chronological_releases: list[dict[str, Any]],
    git_tags: set[str],
) -> str:
    """Determine the base tag according to the priority rules in auto_release_notes.md."""
    body = current_release.get("body") or ""

    # Priority 1: Explicit override marker
    override_match = re.search(r"<!--\s*BASE_TAG:\s*([^\s]+)\s*-->", body)
    if override_match:
        base = override_match.group(1).strip()
        print(f"Selected base for {current_release['tag_name']}: {base}")
        return base

    current_tag = current_release["tag_name"]
    is_prerelease = current_release.get("prerelease", False)

    # Find position of current release in chronological list
    idx = -1
    for i, r in enumerate(all_chronological_releases):
        if r["tag_name"] == current_tag:
            idx = i
            break

    if idx > 0:
        earlier_releases = all_chronological_releases[:idx]
        if not is_prerelease:
            # Priority 2: Most recent earlier stable release by publish date
            for r in reversed(earlier_releases):
                if not r.get("prerelease", False) and r["tag_name"] != current_tag:
                    base = r["tag_name"]
                    print(f"Selected base for {current_tag}: {base}")
                    return base
        else:
            # Priority 3: Most recent earlier release (stable or prerelease)
            for r in reversed(earlier_releases):
                if r["tag_name"] != current_tag:
                    base = r["tag_name"]
                    print(f"Selected base for {current_tag}: {base}")
                    return base

    # Priority 4: Semver sorting fallback from git tags
    current_semver = parse_semver(current_tag)
    if current_semver:
        lower_tags: list[tuple[tuple[int, int, int, int, str], str]] = []
        for t in git_tags:
            if t == current_tag:
                continue
            sv = parse_semver(t)
            if sv and sv < current_semver:
                lower_tags.append((sv, t))
        if lower_tags:
            lower_tags.sort()
            base = lower_tags[-1][1]
            print(f"Selected base for {current_tag}: {base}")
            return base

    # Priority 5: Final fallback root commit
    root_commit = run_cmd(["git", "rev-list", "--max-parents=0", "HEAD"]).splitlines()[
        0
    ]
    print(f"Selected base for {current_tag}: {root_commit}")
    return root_commit


def get_git_commits_in_range(
    base: str, current: str, repo_root: Path = REPO_ROOT
) -> dict[str, dict[str, Any]]:
    """Run a single batched git command to retrieve commit hashes, titles, and touched files."""
    try:
        raw = run_cmd(
            [
                "git",
                "log",
                f"{base}..{current}",
                "--name-only",
                "--format=COMMIT:%H%x09%s",
            ],
            cwd=repo_root,
        )
    except Exception as exc:
        print(f"Warning: git log {base}..{current} failed: {exc}", file=sys.stderr)
        return {}

    commits: dict[str, dict[str, Any]] = {}
    current_commit: str | None = None

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("COMMIT:"):
            parts = line[len("COMMIT:") :].split("\t", 1)
            commit_hash = parts[0]
            title = parts[1] if len(parts) > 1 else ""
            current_commit = commit_hash
            commits[current_commit] = {"title": title, "files": []}
        elif current_commit:
            commits[current_commit]["files"].append(line)

    return commits


def parse_existing_prs(
    raw_body: str,
    git_commits: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], set[str]]:
    """Extract PRs mentioned in previous release notes."""
    prs: list[dict[str, Any]] = []
    seen: set[str] = set()

    for line in raw_body.splitlines():
        line = line.strip()
        m = re.match(
            r"^\*\s*(?:[^\w\s\[\(]+\s*)?(.*?)\s+by\s+@.*?in\s+https://github\.com/[^/]+/[^/]+/pull/(\d+)",
            line,
        )
        if m:
            title, pr_num = m.group(1), m.group(2)
            if pr_num not in seen:
                seen.add(pr_num)
                matched_files: list[str] = []
                for _, cdata in git_commits.items():
                    if (
                        f"(#{pr_num})" in cdata["title"]
                        or f"#{pr_num}" in cdata["title"]
                    ):
                        matched_files.extend(cdata["files"])
                prs.append(
                    {
                        "title": title,
                        "pr": pr_num,
                        "files": list(set(matched_files)),
                    }
                )

    return prs, seen


def synthesize_summary(
    categories: dict[str, list[str]],
    is_prerelease: bool,
    additional_context: str = "",
) -> str:
    """Synthesize a 1-2 sentence human-readable executive summary."""
    highlights: list[str] = []
    if categories["Features / Enhancements"]:
        highlights.append("features and enhancements")
    if categories["Bug Fixes"]:
        highlights.append("bug fixes")
    if categories["API / Core Library"]:
        highlights.append("core API client improvements")
    if categories["Packaging"]:
        highlights.append("packaging and build infrastructure")
    if categories["Tests"]:
        highlights.append("test coverage expansion")
    if categories["Documentation"]:
        highlights.append("documentation updates")
    if categories["Dependencies"] or categories["CI / Workflows"]:
        highlights.append("routine CI and dependency maintenance")

    if not highlights:
        highlights = ["maintenance updates and stability improvements"]

    if len(highlights) == 1:
        hl_str = highlights[0]
    elif len(highlights) == 2:
        hl_str = f"{highlights[0]} and {highlights[1]}"
    else:
        hl_str = f"{', '.join(highlights[:-1])}, and {highlights[-1]}"

    release_type = "prerelease" if is_prerelease else "release"
    summary = (
        f"This {release_type} focuses on {hl_str} across the purpleair_api package."
    )
    if additional_context:
        summary = f"{summary} {additional_context.strip()}"
    return summary


def build_release_notes(
    release: dict[str, Any],
    base_tag: str,
    git_commits: dict[str, dict[str, Any]],
    additional_context: str = "",
    repo: str = DEFAULT_REPO,
) -> str:
    """Build formatted release notes markdown adhering to the purpleair_api template."""
    tag = release["tag_name"]
    is_prerelease = release.get("prerelease", False)
    pypi_version = tag[1:] if tag.startswith("v") else tag
    has_valid_pypi = bool(re.match(r"^\d+(\.\d+)*", pypi_version))
    pypi_url = f"https://pypi.org/project/purpleair_api/{pypi_version}/"
    raw_body = release.get("body") or ""

    parsed_prs, seen_pr_numbers = parse_existing_prs(raw_body, git_commits)

    # Collect uncovered git commits (excluding merge commits)
    uncovered_commits: list[dict[str, Any]] = []
    for h, cdata in git_commits.items():
        s = cdata["title"]
        if s.startswith("Merge branch") or s.startswith("Merge pull request"):
            continue
        pr_match = re.search(r"#(\d+)", s)
        if pr_match and pr_match.group(1) in seen_pr_numbers:
            continue
        uncovered_commits.append({"title": s, "hash": h[:7], "files": cdata["files"]})

    # Combine items
    items: list[dict[str, Any]] = []
    for pr in parsed_prs:
        items.append(
            {
                "title": pr["title"],
                "ref": f"(#{pr['pr']})",
                "files": pr["files"],
            }
        )
    for c in uncovered_commits:
        items.append(
            {
                "title": c["title"],
                "ref": f"({c['hash']})",
                "files": c["files"],
            }
        )

    # Categorize items into the 9 standard themes
    categorized: dict[str, list[str]] = {cat: [] for cat in THEME_CATEGORIES}
    for it in items:
        cat = categorize_item(it["title"], it["files"])
        cleaned = rewrite_to_natural_language(it["title"])
        bullet = f"- {cleaned} {it['ref']}"
        categorized[cat].append(bullet)

    # Build markdown output
    lines: list[str] = []
    summary = synthesize_summary(categorized, is_prerelease, additional_context)
    lines.append(summary)
    lines.append("")
    lines.append(f"Compared to: {base_tag}")
    lines.append("")

    if has_valid_pypi:
        lines.append("## Install / Upgrade")
        lines.append("")
        lines.append("```bash")
        lines.append(f"pip install purpleair_api=={pypi_version}")
        lines.append("```")
        lines.append("")
        lines.append(f"Or browse this release on PyPI: {pypi_url}")
        lines.append("")

    for cat in THEME_CATEGORIES:
        bullets = categorized[cat]
        if bullets:
            lines.append(f"## {cat}")
            lines.append("")
            lines.extend(bullets)
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        f"**Full Changelog**: https://github.com/{repo}/compare/{base_tag}...{tag}"
    )

    return "\n".join(lines).strip() + "\n"


def process_release(
    release: dict[str, Any],
    all_releases: list[dict[str, Any]],
    git_tags: set[str],
    publish: bool = False,
    additional_context: str = "",
    repo: str = DEFAULT_REPO,
    output_file: Path | None = None,
) -> bool:
    """Process a single release and optionally update it via gh."""
    tag = release["tag_name"]
    body = release.get("body") or ""

    if "<!-- PROTECTED -->" in body:
        print(f"Skipping {tag}: marked <!-- PROTECTED -->")
        return False

    base_tag = determine_base_tag(release, all_releases, git_tags)
    git_commits = get_git_commits_in_range(base_tag, tag)
    notes = build_release_notes(
        release,
        base_tag,
        git_commits,
        additional_context=additional_context,
        repo=repo,
    )

    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(notes, encoding="utf-8")
        print(f"Wrote generated release notes to {output_file}")

    if publish:
        rel_id = release["id"]
        print(f"Publishing release notes for {tag} (ID: {rel_id})...")
        payload = json.dumps({"body": notes})
        run_cmd(
            [
                "gh",
                "api",
                "--method",
                "PATCH",
                f"/repos/{repo}/releases/{rel_id}",
                "--input",
                "-",
            ],
            env={"GH_PAYLOAD": payload},
        )
        print(f"Successfully updated release {tag} on GitHub.")
    else:
        print(f"\n--- [DRY-RUN] Release Notes for {tag} ---")
        print(notes)
        print("--- [END DRY-RUN] ---\n")

    return True


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Generate and update GitHub release notes for purpleair_api."
    )
    parser.add_argument("--tag", help="Specific release tag to process.")
    parser.add_argument(
        "--latest", action="store_true", help="Process the latest published release."
    )
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="Process ALL existing releases in chronological order.",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Update the GitHub release body directly via gh cli.",
    )
    parser.add_argument(
        "--additional-context",
        default="",
        help="Optional additional context to incorporate into the summary.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        help="Optional path to write generated release notes markdown.",
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=f"Target GitHub repository (default: {DEFAULT_REPO}).",
    )

    args = parser.parse_args()

    ensure_git_tags()
    git_tags = get_git_tags()
    all_releases = get_all_releases(repo=args.repo)

    if not all_releases:
        print("No releases found on GitHub.", file=sys.stderr)
        return 1

    if args.tag:
        target = next((r for r in all_releases if r["tag_name"] == args.tag), None)
        if not target:
            print(f"Release with tag '{args.tag}' not found.", file=sys.stderr)
            return 1
        process_release(
            target,
            all_releases,
            git_tags,
            publish=args.publish,
            additional_context=args.additional_context,
            repo=args.repo,
            output_file=args.output_file,
        )
    elif args.latest:
        target = all_releases[-1]
        process_release(
            target,
            all_releases,
            git_tags,
            publish=args.publish,
            additional_context=args.additional_context,
            repo=args.repo,
            output_file=args.output_file,
        )
    elif args.backfill:
        print(f"Backfilling {len(all_releases)} releases in chronological order...")
        count = 0
        for r in all_releases:
            updated = process_release(
                r,
                all_releases,
                git_tags,
                publish=args.publish,
                additional_context=args.additional_context,
                repo=args.repo,
                output_file=args.output_file,
            )
            if updated:
                count += 1
                if args.publish:
                    time.sleep(1)  # Throttling protection
        print(f"Completed backfill. Updated {count} release(s).")
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
