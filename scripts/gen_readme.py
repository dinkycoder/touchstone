#!/usr/bin/env python
"""Regenerate marked README.md blocks from their real source of truth, in place.

This is a separate concern from docs-map.yml/check_docs.py: docs-map.yml answers "did you
forget to touch the doc"; this script answers "is this specific generated block stale."
Sprint 1 ships one real block (the README status line, from docs/sprint/CURRENT.md's
frontmatter). Extend this by adding another `_render_*`/marker pair when there's real data to
generate from (a benchmark table, an endpoint list, ...) — not by generalizing the schema.
"""
from __future__ import annotations

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


def main() -> int:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")

    text, found = _replace_block(text, "sprint-status", render_sprint_status())
    if not found:
        print("gen_readme: missing docs-map markers for 'sprint-status' in README.md", file=sys.stderr)
        return 1

    readme.write_text(text, encoding="utf-8")
    print("gen_readme: updated README.md#sprint-status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
