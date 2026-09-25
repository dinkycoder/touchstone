#!/usr/bin/env python
"""Stop/SubagentStop hook: "green means commit."

Order (per the founder's design):
1. Already fired this turn -> let Claude stop; never loop.
2. On a protected branch (main/master) -> block, tell Claude to switch branches.
3. Nothing uncommitted -> let Claude stop; nothing to do.
4. Tests pass -> block: commit and push before stopping.
   Tests fail -> let Claude stop (e.g. to report/ask for help); don't force a commit of red work.
"""
from __future__ import annotations

import json
import subprocess
import sys

PROTECTED_BRANCHES = {"main", "master"}


def run(cmd: list[str], cwd: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main() -> int:
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return 0

    cwd = data.get("cwd", ".")

    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd).stdout.strip()
    if branch in PROTECTED_BRANCHES:
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": (
                        f"You're on the protected branch '{branch}'. Switch to a "
                        "feature/chore branch before continuing."
                    ),
                }
            )
        )
        return 0

    status = run(["git", "status", "--porcelain"], cwd).stdout.strip()
    if not status:
        return 0

    tests = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if tests.returncode == 0:
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": (
                        "Tests are green and there are uncommitted changes. Commit "
                        "(Conventional Commits) and push before stopping."
                    ),
                }
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
