import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "check_docs.py"


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def make_repo(root: Path, docs_map: str) -> None:
    """A repo whose origin/main is its first commit, checked out on a feature branch."""
    git(root, "init", "-b", "main", "-q")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "Test")
    (root / "scripts").mkdir()
    shutil.copy(SCRIPT, root / "scripts" / "check_docs.py")
    (root / "docs" / "sprint").mkdir(parents=True)
    (root / "docs" / "docs-map.yml").write_text(docs_map, encoding="utf-8")
    (root / "docs" / "sprint" / "CURRENT.md").write_text("- [ ] a task\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("x = 1\n", encoding="utf-8")
    (root / "README.md").write_text("# X\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "chore: initial commit")
    git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(root, "checkout", "-q", "-b", "feat/x")


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "check_docs.py")],
        capture_output=True,
        text=True,
    )


def test_flags_mapped_path_changed_without_its_doc(tmp_path: Path) -> None:
    make_repo(tmp_path, "src/**: [README.md]\n")
    (tmp_path / "src" / "app.py").write_text("x = 2\n", encoding="utf-8")

    result = run(tmp_path)

    assert result.returncode == 1
    assert "README.md (needed by: src/app.py)" in result.stdout


def test_ticking_a_sprint_checkbox_passes_with_the_real_docs_map(tmp_path: Path) -> None:
    # README's sprint-status block is generated from CURRENT.md's frontmatter only, so an
    # edit to the sprint body leaves README unchanged. That must not fail the docs check.
    make_repo(tmp_path, (REPO / "docs" / "docs-map.yml").read_text(encoding="utf-8"))
    current = tmp_path / "docs" / "sprint" / "CURRENT.md"
    current.write_text("- [x] a task\n", encoding="utf-8")

    result = run(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr


def test_missing_gh_means_no_bypass_label(monkeypatch: pytest.MonkeyPatch) -> None:
    spec = importlib.util.spec_from_file_location("check_docs", SCRIPT)
    assert spec and spec.loader
    check_docs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check_docs)

    def gh_not_installed(*args: object, **kwargs: object) -> None:
        raise FileNotFoundError("gh")

    monkeypatch.setattr(check_docs.subprocess, "run", gh_not_installed)

    assert check_docs.has_bypass_label() is False
