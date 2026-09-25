import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "bench_gate.py"


def run_hook(cwd: Path) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"cwd": str(cwd), "stop_hook_active": False})
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
    )


def test_blocks_on_failing_tests(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text("def test_fail():\n    assert False\n")

    result = run_hook(tmp_path)

    assert result.returncode == 0
    decision = json.loads(result.stdout)
    assert decision["decision"] == "block"
    assert "pytest is failing" in decision["reason"]


def test_allows_on_passing_tests(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text("def test_ok():\n    assert True\n")

    result = run_hook(tmp_path)

    assert result.returncode == 0
    assert result.stdout.strip() == ""
