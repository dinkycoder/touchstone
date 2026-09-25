#!/usr/bin/env python
"""Regenerate marked README.md blocks from their real source of truth, in place.

`--check` writes nothing and exits 1 if any block is stale; CI runs it.

This is a separate concern from docs-map.yml/check_docs.py: docs-map.yml answers "did you
forget to touch the doc"; this script answers "is this specific generated block stale."
Sprint 1 ships one real block (the README status line, from docs/sprint/CURRENT.md's
frontmatter). Extend this by adding another `render_*` function to BLOCKS when there's real
data to generate from (a benchmark table, an endpoint list, ...) — not by generalizing the
schema.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, fm, _ = text.split("---", 2)
    return yaml.safe_load(fm) or {}


def _replace_block(text: str, marker_id: str, body: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf"(<!-- docs-map:start:{marker_id} -->)(.*?)(<!-- docs-map:end:{marker_id} -->)",
        re.DOTALL,
    )
    if not pattern.search(text):
        return text, False
    new_text = pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)
    return new_text, True


def render_sprint_status() -> str:
    fm = _frontmatter(ROOT / "docs" / "sprint" / "CURRENT.md")
    return "**Sprint {sprint} ({status}):** {goal}".format(**fm)


BLOCKS = {"sprint-status": render_sprint_status}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate marked README.md blocks.")
    parser.add_argument(
        "--check", action="store_true", help="write nothing; exit 1 if any block is stale"
    )
    args = parser.parse_args(argv)

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")

    stale: list[str] = []
    for marker_id, render in BLOCKS.items():
        new_text, found = _replace_block(text, marker_id, render())
        if not found:
            print(
                f"gen_readme: missing docs-map markers for '{marker_id}' in README.md",
                file=sys.stderr,
            )
            return 1
        if new_text != text:
            stale.append(marker_id)
        text = new_text

    if args.check:
        if stale:
            print(
                f"gen_readme: stale README.md block(s): {', '.join(stale)}. Run "
                "scripts/gen_readme.py (or the readme-sync skill) and commit the result.",
                file=sys.stderr,
            )
            return 1
        print("gen_readme: README.md generated blocks are current.")
        return 0

    if stale:
        readme.write_text(text, encoding="utf-8")
    for marker_id in BLOCKS:
        state = "updated" if marker_id in stale else "already current"
        print(f"gen_readme: README.md#{marker_id} {state}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
