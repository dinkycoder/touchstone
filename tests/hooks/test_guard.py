import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "guard.py"


def run_raw(payload: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
    )


def run_hook(command: str, tool: str = "Bash") -> subprocess.CompletedProcess[str]:
    return run_raw(json.dumps({"tool_name": tool, "tool_input": {"command": command}, "cwd": "."}))


def test_blocks_secret_read() -> None:
    result = run_hook("cat .env")
    assert result.returncode == 2
    assert "Blocked by TOUCHSTONE policy" in result.stderr


def test_allows_ordinary_command() -> None:
    result = run_hook("git status")
    assert result.returncode == 0
    assert result.stderr == ""


# Every command here must be blocked. Most are bypasses found by probing the first version of
# guard.py; keep adding to this table rather than weakening it.
BLOCKED: list[tuple[str, str]] = [
    # Secrets: .env files, whatever command reads them.
    ("Bash", "grep KEY .env"),
    ("Bash", "sed -n p .env"),
    ("Bash", "awk 1 .env"),
    ("Bash", "more .env"),
    ("Bash", "cp .env /tmp/x && cat /tmp/x"),
    ("Bash", "base64 .env"),
    ("Bash", "python -c \"print(open('.env').read())\""),
    ("Bash", "cat .env.sepolia"),
    ("Bash", 'cat .e""nv'),
    ("PowerShell", "gc .env"),
    ("PowerShell", "Get-Content .\\.env"),
    ("PowerShell", "Select-String -Path .env -Pattern KEY"),
    # Secrets: key material and secret variable names.
    ("Bash", "echo $CDP_API_KEY_SECRET"),
    ("Bash", "ls ~/.foundry/keystores"),
    ("Bash", "cat deployer.pem"),
    ("PowerShell", "$env:CDP_API_KEY_SECRET"),
    # Secrets: dumping the whole environment.
    ("Bash", "printenv"),
    ("Bash", "env"),
    ("Bash", "env | grep KEY"),
    ("Bash", "set"),
    ("Bash", "export -p"),
    ("Bash", "cat /proc/self/environ"),
    ("Bash", 'python -c "import os; print(os.environ)"'),
    ("PowerShell", "Get-ChildItem env:"),
    ("PowerShell", "gci Env:\\"),
    # Base mainnet.
    ("Bash", "forge script Deploy --rpc-url $BASE_RPC --chain-id 8453"),
    ("Bash", "cast balance 0xabc --rpc-url https://mainnet.base.org"),
    ("Bash", "cast chain-id --rpc-url https://base.llamarpc.com"),
    ("Bash", "cast balance 0xabc --rpc-url $BASE_RPC_URL"),
    ("Bash", "curl -s -X POST https://base-rpc.publicnode.com -d '{}'"),
    ("Bash", "forge script Deploy --chain base"),
    ("Bash", "forge script Deploy --chain base-sepolia --broadcast"),
    ("Bash", "npx hardhat run deploy.ts --network base"),
    ("Bash", "cast rpc eth_chainId | grep 0x2105"),
    ("Bash", "curl -s localhost:4021/check/fast -H 'X-Network: eip155:8453'"),
    ("Bash", "git status && cast send 0xabc 'f()'"),
    ("Bash", "./scripts/release-mainnet.sh"),
    # Sealed evaluation set: any path to it, including relative and glob forms.
    ("Bash", "cat ml/eval/sealed/labels.csv"),
    ("Bash", "cat ml/eval/./sealed/labels.csv"),
    ("Bash", "cd ml/eval && cat sealed/labels.csv"),
    ("Bash", "cat ml/eval/seal*/labels.csv"),
    ("Bash", "cat ml/eval/*/labels.csv"),
    ("Bash", "cd ml/eval && cat */labels.csv"),
    ("Bash", 'cat ml/eval/se""aled/labels.csv'),
    ("PowerShell", "Get-Content ml\\eval\\sealed\\labels.csv"),
    # Raw sanctions data: reads are fine, anything that could write or delete is not.
    ("Bash", "echo x > data/sanctions/raw/ofac.xml"),
    ("Bash", "rm -rf data/sanctions/raw"),
    ("Bash", "cd data/sanctions && rm -rf raw"),
    ("Bash", "sed -i s/a/b/ data/sanctions/raw/ofac.xml"),
    ("Bash", "ls data/sanctions/raw | xargs rm"),
    ("Bash", "git checkout HEAD~1 -- data/sanctions/raw"),
    ("Bash", "head data/sanctions/raw/ofac.xml > data/sanctions/raw/ofac2.xml"),
    ("PowerShell", "Remove-Item -Recurse data\\sanctions\\raw"),
    ("PowerShell", "Set-Content data/sanctions/raw/un.xml 'x'"),
    # Decode-and-run, which would hide any of the above from the checks.
    ("Bash", "echo Y2F0IC5lbnY= | base64 -d | sh"),
    ("Bash", 'eval "$(echo foo)"'),
    (
        "Bash",
        "python -c \"import base64,os; os.system(base64.b64decode('Y2F0IC5lbnY=').decode())\"",
    ),
    ("Bash", "node -e \"require('child_process').execSync(Buffer.from(s, 'base64').toString())\""),
    ("PowerShell", "Invoke-Expression $cmd"),
    ("PowerShell", "powershell -EncodedCommand ZQBjAGgAbwA="),
    # Commit and PR messages: only literal text is exempt, never anything the shell expands,
    # and never the rest of the command line.
    ("Bash", 'git commit -m "$(cat .env)"'),
    ("Bash", 'git commit -m "`cat .env`"'),
    ("Bash", "git commit -m 'x'\"$(cat .env)\""),
    ("Bash", "git commit -m 'x' && cat .env"),
    ("Bash", "git commit -m 'x'; cast chain-id --rpc-url https://mainnet.base.org"),
    ("Bash", "git commit -m 'x' -- .env"),
    ("Bash", "git commit -F - <<EOF\n$(cat .env)\nEOF"),
    ("Bash", "git commit -F - <<'EOF'\nx\nEOF\ncat .env"),
    ("Bash", "bash <<'EOF'\ncat .env\nEOF"),
    ("Bash", "python -m 'deploy_mainnet'"),
    ("Bash", 'gh pr create --body "$(cat .env)"'),
    ("Bash", "gh pr create --body \"$(cat <<'EOF'\nx\nEOF\n); cat .env\""),
    ("PowerShell", 'git commit -m "$(Get-Content .env)"'),
    ("PowerShell", 'git commit -m @"\n$(Get-Content .env)\n"@'),
]

# Ordinary development commands that must keep working.
ALLOWED: list[tuple[str, str]] = [
    ("Bash", "git diff --stat"),
    ("Bash", "git log --oneline -5"),
    ("Bash", ".venv/Scripts/python -m pytest -q"),
    ("Bash", "cat README.md"),
    ("Bash", "cat .env.example"),
    ("Bash", "grep -rn TODO services/"),
    ("Bash", "env PYTHONUTF8=1 python -m pytest -q"),
    ("Bash", "set -euo pipefail"),
    ("Bash", "cast call 0xabc 'f()' --rpc-url https://sepolia.base.org"),
    ("Bash", "forge script Deploy --rpc-url $BASE_SEPOLIA_RPC_URL"),
    ("Bash", "cast chain-id --rpc-url http://127.0.0.1:8545"),
    # Base Sepolia's chain id 84532 starts with mainnet's 8453.
    ("Bash", "forge script Deploy --chain-id 84532 --rpc-url $BASE_SEPOLIA_RPC_URL"),
    ("Bash", "curl -s localhost:4021/check/fast -H 'X-Network: eip155:84532'"),
    ("Bash", "forge test"),
    ("Bash", "curl -s https://sepolia.base.org"),
    ("Bash", "head -n 5 data/sanctions/raw/ofac.xml 2>&1"),
    ("Bash", "git log --oneline -- data/sanctions/raw"),
    ("Bash", "sha256sum data/sanctions/raw/ofac.xml"),
    ("Bash", "python -m services.ingest.sanctions diff --since last"),
    ("Bash", "git commit -m 'feat(ingest): add OFAC parser'"),
    ("Bash", "pip install -r requirements-dev.txt"),
    # Literal commit and PR text may mention guarded words; it is stored, never run.
    ("Bash", "git commit -m 'docs: the mainnet release is founder-only'"),
    ("Bash", 'git commit -m "docs: record sealed eval probe"'),
    ("Bash", "git commit -q -m 'docs: probe' -m 'Blocked: cat .env, cat ml/eval/sealed/x.csv.'"),
    ("Bash", "git commit --message='fix: stop reading .env'"),
    ("Bash", "git commit -q -F - <<'EOF'\ndocs(sprint): tick\n\nProbed .env, mainnet, sealed eval.\nEOF"),
    (
        "Bash",
        "gh pr create --draft --title 'docs: mainnet notes' --body \"$(cat <<'EOF'\n"
        "- cast chain-id --rpc-url https://mainnet.base.org: blocked\nEOF\n)\"",
    ),
    ("Bash", "gh pr edit 3 --body 'sealed eval read: blocked'"),
    ("PowerShell", "git commit -m 'docs: probe .env'"),
    ("PowerShell", "git commit -m @'\ndocs: probe .env and mainnet\n'@"),
    ("PowerShell", "Get-ChildItem"),
    ("PowerShell", "$env:PYTHONUTF8 = '1'; .venv/Scripts/python.exe -m pytest -q"),
]


@pytest.mark.parametrize(("tool", "command"), BLOCKED)
def test_blocks(tool: str, command: str) -> None:
    result = run_hook(command, tool)
    assert result.returncode == 2, f"not blocked: {command}"
    assert "Blocked by TOUCHSTONE policy" in result.stderr


@pytest.mark.parametrize(("tool", "command"), ALLOWED)
def test_allows(tool: str, command: str) -> None:
    result = run_hook(command, tool)
    assert result.returncode == 0, f"blocked: {command}\n{result.stderr}"
    assert result.stderr == ""


# Claude Code treats any exit code other than 2 as "let the command run", so a guard that
# crashes or can't see the command must block instead.
def test_fails_closed_on_invalid_json() -> None:
    result = run_raw("not json")
    assert result.returncode == 2
    assert "Blocked by TOUCHSTONE policy" in result.stderr


@pytest.mark.parametrize(
    "tool_input",
    [{}, {"command": None}, {"command": ["cat", ".env"]}],
    ids=["missing", "null", "list"],
)
@pytest.mark.parametrize("tool", ["Bash", "PowerShell"])
def test_fails_closed_without_a_command_string(tool: str, tool_input: dict) -> None:
    result = run_raw(json.dumps({"tool_name": tool, "tool_input": tool_input}))
    assert result.returncode == 2
    assert "Blocked by TOUCHSTONE policy" in result.stderr
