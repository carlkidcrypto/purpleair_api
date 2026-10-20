"""Unit tests for .github/scripts/generate_release_notes.py in purpleair_api."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

# Dynamically import generate_release_notes from .github/scripts/
_SCRIPT_PATH = Path(__file__).resolve().parent.parent / "generate_release_notes.py"
spec = importlib.util.spec_from_file_location(
    "generate_release_notes", str(_SCRIPT_PATH)
)
gen_mod = importlib.util.module_from_spec(spec)
sys.modules["generate_release_notes"] = gen_mod
spec.loader.exec_module(gen_mod)

clean_title = gen_mod.clean_title
rewrite_to_natural_language = gen_mod.rewrite_to_natural_language
categorize_item = gen_mod.categorize_item
parse_semver = gen_mod.parse_semver
determine_base_tag = gen_mod.determine_base_tag
parse_existing_prs = gen_mod.parse_existing_prs
synthesize_summary = gen_mod.synthesize_summary
build_release_notes = gen_mod.build_release_notes


def test_clean_title():
    raw1 = "✨ Fix rate limit header parsing (#123) by @carlkidcrypto in https://github.com/carlkidcrypto/purpleair_api/pull/123"
    assert clean_title(raw1) == "Fix rate limit header parsing"

    raw2 = "[docs] Update documentation for Read API #456"
    assert clean_title(raw2) == "[docs] Update documentation for Read API"


def test_rewrite_to_natural_language_prefixes_and_verbs():
    # Conventional commit prefixes stripped and verb conjugated
    assert (
        rewrite_to_natural_language("feat(read): add batch sensor request option")
        == "Adds batch sensor request option"
    )
    assert (
        rewrite_to_natural_language("fix: resolve timeout on large sensor payload")
        == "Resolves timeout on large sensor payload"
    )
    assert (
        rewrite_to_natural_language("chore(deps): bump requests from 2.31 to 2.32")
        == "Bumps requests from 2.31 to 2.32"
    )
    assert (
        rewrite_to_natural_language("[coverage-autofix] improve branch coverage")
        == "Improves branch coverage"
    )

    # Past tense verbs conjugated to 3rd person singular present
    assert (
        rewrite_to_natural_language("Fixed connection handling in Read API")
        == "Fixes connection handling in Read API"
    )
    assert (
        rewrite_to_natural_language("Added support for Python 3.14")
        == "Adds support for Python 3.14"
    )
    assert (
        rewrite_to_natural_language("Updated dependencies in requirements.txt")
        == "Updates dependencies in requirements.txt"
    )

    # Prefix with noun gets inferred active verb
    assert (
        rewrite_to_natural_language("fix: header error in local API")
        == "Fixes header error in local API"
    )
    assert (
        rewrite_to_natural_language("feat: matter protocol converter")
        == "Adds matter protocol converter"
    )

    # Already third person present unchanged
    assert (
        rewrite_to_natural_language("Adds support for historical sensor queries")
        == "Adds support for historical sensor queries"
    )


def test_categorize_item():
    # Dependencies
    assert categorize_item("Bump requests from 2.31 to 2.32", []) == "Dependencies"
    assert (
        categorize_item(
            "Update packages",
            ["requirements.txt"],
        )
        == "Dependencies"
    )

    # CI / Workflows (priority over docs)
    assert (
        categorize_item(
            "Update CI workflow for Python 3.14",
            [".github/workflows/tests.yml"],
        )
        == "CI / Workflows"
    )
    assert (
        categorize_item(
            "Update changelog workflow",
            [".github/workflows/auto_change_log.md"],
        )
        == "CI / Workflows"
    )

    # Documentation
    assert (
        categorize_item(
            "Update README.rst with new examples",
            ["README.rst"],
        )
        == "Documentation"
    )
    assert (
        categorize_item(
            "Add documentation for local API",
            ["docs/index.rst"],
        )
        == "Documentation"
    )

    # Tests
    assert (
        categorize_item(
            "Add unit tests for Read API",
            ["tests/test_purpleair_read_api.py"],
        )
        == "Tests"
    )

    # Packaging
    assert (
        categorize_item(
            "Update wheel configuration",
            ["setup.cfg", "setup.py"],
        )
        == "Packaging"
    )

    # Core Library / Features / Bug Fixes
    assert (
        categorize_item(
            "Fix JSON decoding error when response is truncated",
            ["purpleair_api/PurpleAirReadAPI.py"],
        )
        == "Bug Fixes"
    )
    assert (
        categorize_item(
            "Add support for custom session timeout",
            ["purpleair_api/PurpleAirAPI.py"],
        )
        == "Features / Enhancements"
    )
    assert (
        categorize_item(
            "Internal refactor of sensor query construction",
            ["purpleair_api/PurpleAirAPIHelpers.py"],
        )
        == "API / Core Library"
    )

    # Chores / Misc
    assert categorize_item("Clean up repository whitespace", []) == "Chores / Misc"


def test_parse_semver():
    assert parse_semver("v1.5.0") == (1, 5, 0, 1, "")
    assert parse_semver("1.5.0") == (1, 5, 0, 1, "")
    assert parse_semver("v1.5.0a1") == (1, 5, 0, 0, "a1")
    assert parse_semver("v2.0.0-rc.1") == (2, 0, 0, 0, "rc.1")
    assert parse_semver("invalid_tag") is None


def test_determine_base_tag_override():
    curr = {
        "tag_name": "v1.5.0",
        "body": "Some body <!-- BASE_TAG: v1.3.0 --> with override",
        "prerelease": False,
    }
    base = determine_base_tag(curr, [curr], {"v1.3.0", "v1.5.0"})
    assert base == "v1.3.0"


def test_determine_base_tag_stable():
    releases = [
        {"tag_name": "v1.0.0", "prerelease": False, "body": ""},
        {"tag_name": "v1.1.0a1", "prerelease": True, "body": ""},
        {"tag_name": "v1.1.0", "prerelease": False, "body": ""},
        {"tag_name": "v1.2.0", "prerelease": False, "body": ""},
    ]
    curr = releases[3]  # v1.2.0
    base = determine_base_tag(curr, releases, {r["tag_name"] for r in releases})
    assert base == "v1.1.0"


def test_determine_base_tag_prerelease():
    releases = [
        {"tag_name": "v1.0.0", "prerelease": False, "body": ""},
        {"tag_name": "v1.1.0a1", "prerelease": True, "body": ""},
        {"tag_name": "v1.1.0a2", "prerelease": True, "body": ""},
    ]
    curr = releases[2]  # v1.1.0a2
    base = determine_base_tag(curr, releases, {r["tag_name"] for r in releases})
    assert base == "v1.1.0a1"


def test_determine_base_tag_semver_fallback():
    releases = [{"tag_name": "v1.5.0", "prerelease": False, "body": ""}]
    git_tags = {"v1.0.0", "v1.4.0", "v1.5.0", "v1.6.0"}
    base = determine_base_tag(releases[0], releases, git_tags)
    assert base == "v1.4.0"


def test_parse_existing_prs():
    raw_body = """
    ## What's Changed
    * Fix rate limit retry logic by @carlkidcrypto in https://github.com/carlkidcrypto/purpleair_api/pull/101
    * Add Matter cluster attribute support by @carlkidcrypto in https://github.com/carlkidcrypto/purpleair_api/pull/102
    """
    git_commits = {
        "abcdef1": {
            "title": "Fix rate limit retry logic (#101)",
            "files": ["purpleair_api/PurpleAirReadAPI.py"],
        },
        "abcdef2": {
            "title": "Add Matter cluster attribute support (#102)",
            "files": ["purpleair_api/PurpleAirMatterConverter.py"],
        },
    }
    prs, seen = parse_existing_prs(raw_body, git_commits)
    assert len(prs) == 2
    assert prs[0]["pr"] == "101"
    assert prs[0]["title"] == "Fix rate limit retry logic"
    assert prs[0]["files"] == ["purpleair_api/PurpleAirReadAPI.py"]
    assert "101" in seen
    assert "102" in seen


def test_synthesize_summary():
    cats: dict[str, list[str]] = {
        "Features / Enhancements": ["- Adds new feature (#1)"],
        "Bug Fixes": ["- Fixes bug (#2)"],
        "API / Core Library": [],
        "Tests": [],
        "Packaging": [],
        "CI / Workflows": [],
        "Documentation": [],
        "Dependencies": [],
        "Chores / Misc": [],
    }
    s = synthesize_summary(cats, is_prerelease=False)
    assert "features and enhancements" in s
    assert "bug fixes" in s
    assert "purpleair_api" in s

    # With additional context
    s_extra = synthesize_summary(
        cats, is_prerelease=False, additional_context="Includes security patch."
    )
    assert s_extra.endswith("Includes security patch.")


def test_build_release_notes():
    release = {
        "id": 12345,
        "tag_name": "v1.5.0",
        "prerelease": False,
        "body": "* Add Matter cluster attribute support by @carlkidcrypto in https://github.com/carlkidcrypto/purpleair_api/pull/102",
    }
    base_tag = "v1.4.0"
    git_commits = {
        "commit1": {
            "title": "Add Matter cluster attribute support (#102)",
            "files": ["purpleair_api/PurpleAirMatterConverter.py"],
        },
        "commit2": {
            "title": "Fix rate limiting (#103)",
            "files": ["purpleair_api/PurpleAirReadAPI.py"],
        },
    }
    notes = build_release_notes(release, base_tag, git_commits)

    assert "Compared to: v1.4.0" in notes
    assert "pip install purpleair_api==1.5.0" in notes
    assert "https://pypi.org/project/purpleair_api/1.5.0/" in notes
    assert "## Features / Enhancements" in notes
    assert "## Bug Fixes" in notes
    assert (
        "**Full Changelog**: https://github.com/carlkidcrypto/purpleair_api/compare/v1.4.0...v1.5.0"
        in notes
    )
