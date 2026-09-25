#!/usr/bin/env python
"""Fail if a path in docs/docs-map.yml changed without its mapped docs also changing.

Compares the current branch against origin/main (falling back to the working-tree diff when
that ref doesn't resolve, e.g. before the first push). Skip enforcement on a PR labeled
"no-docs-needed".
"""
from __future__ import annotations

import fnmatch
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = ROOT / "docs" / "docs-map.yml"
BYPASS_LABEL = "no-docs-needed"


def _git(args: list[str]) -> list[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def changed_files() -> set[str]:
    files: set[str] = set()
    files.update(_git(["diff", "--name-only", "origin/main...HEAD"]))
    files.update(_git(["diff", "--name-only"]))
    for line in _git(["status", "--porcelain"]):
        files.add(line[3:].strip())
    return files


def has_bypass_label() -> bool:
    try:
        result = subprocess.run(
            ["gh", "pr", "view", "--json", "labels", "-q", ".labels[].name"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:  # gh isn't installed, so there's no label to find
        return False
    if result.returncode != 0:
        return False
    return BYPASS_LABEL in result.stdout.splitlines()


def main() -> int:
    doc_map: dict[str, list[str]] = yaml.safe_load(MAP_PATH.read_text(encoding="utf-8")) or {}
    changed = changed_files()

    if not changed:
        print("check_docs: no changed files to check.")
        return 0

    stale: dict[str, set[str]] = {}
    for pattern, docs in doc_map.items():
        matches = [f for f in changed if fnmatch.fnmatch(f, pattern)]
        if not matches:
            continue
        for doc in docs:
            doc_path = doc.split("#", 1)[0]
            if doc_path not in changed:
                stale.setdefault(doc, set()).update(matches)

    if not stale:
        print("check_docs: all mapped docs are current.")
        return 0

    if has_bypass_label():
        print(f"check_docs: stale docs found, but the PR is labeled '{BYPASS_LABEL}' - skipping.")
        return 0

    print("check_docs: these paths changed without updating their mapped docs:")
    for doc, sources in sorted(stale.items()):
        print(f"  - {doc} (needed by: {', '.join(sorted(sources))})")
    print(f"Run the readme-sync skill, update the docs by hand, or label the PR '{BYPASS_LABEL}'.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
