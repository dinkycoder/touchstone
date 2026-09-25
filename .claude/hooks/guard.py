#!/usr/bin/env python
"""PreToolUse guard for Bash and PowerShell: blocks mainnet ops, secret access, and
sealed/raw data access. Translated from the plan's guard-bash.sh (docs/plan/solo-build-plan.md
Section 9), widened to catch PowerShell's own read commands alongside the POSIX ones.

False positives are acceptable; misses are not.
"""
from __future__ import annotations

import json
import re
import sys

DENY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"(?i)(8453|base-mainnet|--network[ =]+mainnet)"),
        "mainnet operations are human-only in the solo phase.",
    ),
    (re.compile(r"--broadcast"), "every broadcast is human-only in the solo phase."),
    (re.compile(r"(?im)^\s*cast\s+(send|wallet)\b"), "cast send/wallet is human-only."),
    (
        re.compile(
            r"(?i)\b(cat|type|get-content|less|head|tail|printenv|env)\b"
            r".*(\.env\b|keystore|PRIVATE_KEY|CDP_API_KEY)"
        ),
        "secret access is blocked.",
    ),
    (re.compile(r"ml[\\/]eval[\\/]sealed"), "sealed evaluation data is CI-only."),
    (re.compile(r"release-mainnet"), "the release script is run by the founder only."),
]


def main() -> int:
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "") or ""

    for pattern, reason in DENY_PATTERNS:
        if pattern.search(command):
            print(f"Blocked by TOUCHSTONE policy: {reason}", file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
