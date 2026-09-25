import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "guard.py"


def run_hook(command: str) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}, "cwd": "."})
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
    )


def test_blocks_secret_read() -> None:
    result = run_hook("cat .env")
    assert result.returncode == 2
    assert "Blocked by TOUCHSTONE policy" in result.stderr


def test_allows_ordinary_command() -> None:
    result = run_hook("git status")
    assert result.returncode == 0
    assert result.stderr == ""
