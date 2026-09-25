import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "commit_checkpoint.py"


def init_repo(path: Path, branch: str) -> None:
    subprocess.run(["git", "init", "-b", branch, "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True)
    (path / "README.md").write_text("hello\n")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "chore: initial commit"], cwd=path, check=True)


def run_hook(cwd: Path) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"cwd": str(cwd), "stop_hook_active": False})
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
    )


def test_blocks_on_protected_branch(tmp_path: Path) -> None:
    init_repo(tmp_path, "main")

    result = run_hook(tmp_path)

    assert result.returncode == 0
    decision = json.loads(result.stdout)
    assert decision["decision"] == "block"
    assert "protected branch" in decision["reason"]


def test_allows_clean_feature_branch(tmp_path: Path) -> None:
    init_repo(tmp_path, "chore/bootstrap")

    result = run_hook(tmp_path)

    assert result.returncode == 0
    assert result.stdout.strip() == ""
