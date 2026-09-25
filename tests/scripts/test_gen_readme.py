import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "gen_readme.py"

CURRENT_MD = """---
sprint: 2
status: in-progress
goal: Ship the thing.
---

# Sprint 2

- [ ] a task
"""

FRESH_BLOCK = "**Sprint 2 (in-progress):** Ship the thing."
STALE_BLOCK = "**Sprint 1 (in-progress):** An older goal."


def make_repo(root: Path, block: str) -> Path:
    """Lay out a minimal repo that gen_readme.py treats as its root."""
    (root / "scripts").mkdir()
    shutil.copy(SCRIPT, root / "scripts" / "gen_readme.py")
    (root / "docs" / "sprint").mkdir(parents=True)
    (root / "docs" / "sprint" / "CURRENT.md").write_text(CURRENT_MD, encoding="utf-8")
    readme = root / "README.md"
    readme.write_text(
        "# X\n\n<!-- docs-map:start:sprint-status -->\n"
        f"{block}\n"
        "<!-- docs-map:end:sprint-status -->\n",
        encoding="utf-8",
    )
    return readme


def run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "gen_readme.py"), *args],
        capture_output=True,
        text=True,
    )


def test_check_passes_when_blocks_are_current(tmp_path: Path) -> None:
    readme = make_repo(tmp_path, FRESH_BLOCK)
    before = readme.read_text(encoding="utf-8")

    result = run(tmp_path, "--check")

    assert result.returncode == 0, result.stderr
    assert readme.read_text(encoding="utf-8") == before


def test_check_fails_on_stale_block_without_writing(tmp_path: Path) -> None:
    readme = make_repo(tmp_path, STALE_BLOCK)
    before = readme.read_text(encoding="utf-8")

    result = run(tmp_path, "--check")

    assert result.returncode == 1
    assert "sprint-status" in result.stdout + result.stderr
    assert readme.read_text(encoding="utf-8") == before


def test_check_ignores_sprint_body_changes(tmp_path: Path) -> None:
    make_repo(tmp_path, FRESH_BLOCK)
    current = tmp_path / "docs" / "sprint" / "CURRENT.md"
    current.write_text(CURRENT_MD.replace("- [ ] a task", "- [x] a task"), encoding="utf-8")

    result = run(tmp_path, "--check")

    assert result.returncode == 0, result.stderr


def test_regenerates_stale_block(tmp_path: Path) -> None:
    readme = make_repo(tmp_path, STALE_BLOCK)

    result = run(tmp_path)

    assert result.returncode == 0, result.stderr
    text = readme.read_text(encoding="utf-8")
    assert FRESH_BLOCK in text
    assert STALE_BLOCK not in text
