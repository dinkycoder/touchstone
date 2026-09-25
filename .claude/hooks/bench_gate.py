#!/usr/bin/env python
"""Stop/SubagentStop gate: block finishing while the test suite is red.

This is a Sprint 1 stand-in for the plan's per-language ML benchmark gate
(docs/plan/solo-build-plan.md Section 9, bench-gate.sh), which needs ml/matching to exist
(Sprint 3-4). Once ml/matching lands, extend this to also run
`ml.matching.core.bench --lang <lang> --split dev --gate` for each changed language, the way
the plan describes, instead of (or in addition to) the blanket pytest run below.
"""
from __future__ import annotations

import json
import subprocess
import sys


def main() -> int:
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return 0

    cwd = data.get("cwd", ".")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        tail = "\n".join((result.stdout + result.stderr).splitlines()[-20:])
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": f"pytest is failing; fix before stopping.\n{tail}",
                }
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
