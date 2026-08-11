#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'EOF'
Usage: scripts/release.sh [--dry-run] NEW_VERSION [OLD_VERSION]

Bump the current release version in tracked source and current documentation files.
If OLD_VERSION is omitted, it is read from setup.cfg.
EOF
}

dry_run=false
if [[ "${1:-}" == "--dry-run" ]]; then
    dry_run=true
    shift
fi

if [[ $# -lt 1 || $# -gt 2 ]]; then
    usage >&2
    exit 2
fi

new_version=$1
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

if [[ ! "$new_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+([abrc][0-9]+)?$ ]]; then
    printf 'Invalid release version: %s\n' "$new_version" >&2
    exit 2
fi

if [[ $# -eq 2 ]]; then
    old_version=$2
else
    old_version=$(sed -nE 's/^version[[:space:]]*=[[:space:]]*([^[:space:]]+).*$/\1/p' setup.cfg | head -n 1)
fi

if [[ -z "$old_version" ]]; then
    printf 'Could not determine the current version from setup.cfg\n' >&2
    exit 1
fi

if [[ "$old_version" == "$new_version" ]]; then
    printf 'New version is the same as the current version: %s\n' "$old_version"
    exit 0
fi

pathspecs=(
    ':(exclude)CHANGELOG.md'
    ':(exclude)build/**'
    ':(exclude)python3.12.venv/**'
    ':(exclude)docs/html/**'
    ':(exclude)docs/html_v*/**'
    ':(exclude)docs/doctrees/**'
    ':(exclude)docs/html/**/_sources/**'
    ':(exclude).github/workflows/*.lock.yml'
)

mapfile -t files < <(git grep -Il -F -- "$old_version" -- . "${pathspecs[@]}" || true)

required_files=(
    setup.cfg
    sphinx_docs_build/source/conf.py
)
for required_file in "${required_files[@]}"; do
    if [[ ! " ${files[*]} " == *" $required_file "* ]]; then
        printf 'Expected release version %s in %s\n' "$old_version" "$required_file" >&2
        exit 1
    fi
done

if [[ ${#files[@]} -eq 0 ]]; then
    printf 'No tracked release files contain version %s\n' "$old_version" >&2
    exit 1
fi

printf '%s version %s -> %s in %d file(s):\n' \
    "$([[ "$dry_run" == true ]] && printf 'Would bump' || printf 'Bumping')" \
    "$old_version" "$new_version" "${#files[@]}"
printf '  %s\n' "${files[@]}"

if [[ "$dry_run" == true ]]; then
    exit 0
fi

OLD_VERSION="$old_version" NEW_VERSION="$new_version" perl -0pi -e \
    's/\Q$ENV{OLD_VERSION}\E/$ENV{NEW_VERSION}/g' "${files[@]}"

remaining=$(git grep -Il -F -- "$old_version" -- . "${pathspecs[@]}" || true)
if [[ -n "$remaining" ]]; then
    printf 'Version %s remains in active tracked files:\n%s\n' "$old_version" "$remaining" >&2
    exit 1
fi

printf 'Release version updated to %s.\n' "$new_version"