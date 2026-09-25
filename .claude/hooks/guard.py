#!/usr/bin/env python
"""PreToolUse guard for Bash and PowerShell: blocks mainnet ops, secret access, sealed-set
access and writes to raw sanctions data. Translated from the plan's guard-bash.sh
(docs/plan/solo-build-plan.md Section 9) and widened after probing for bypasses; the probe
cases live in tests/hooks/test_guard.py.

False positives are acceptable; misses are not. So the checks match what a command names (a
path, a host, a variable), not which program touches it, because any program can read a file.
One consequence: a `git commit -m` message that mentions `.env` or the sealed set is blocked
too. Commit with `-F <file>` instead; a message carve-out would let `-m "$(cat .env)"` through.

This is a tripwire, not a sandbox: it only sees the command string. A script that reads .env
itself, a path held in a variable, or a recursive search over the whole tree (`grep -r .`,
`git grep`) gets past it. Keep secrets and the sealed set out of the working tree.

Any failure blocks, because Claude Code runs the command on every exit code except 2.
"""
from __future__ import annotations

import json
import re
import sys

MAINNET = "mainnet operations are human-only in the solo phase."
SECRETS = "secret access is blocked."
SEALED = "sealed evaluation data is CI-only."
RAW_DATA = "data/sanctions/raw is read-only; only the deterministic fetcher writes it."
DECODE_AND_RUN = "decoding and running a command hides it from this guard."

DENY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"release-mainnet"), "the release script is run by the founder only."),
    # Base mainnet is chain id 8453 (0x2105). Base Sepolia's 84532 must not match.
    (re.compile(r"(?i)(?<!\d)8453(?!\d)|(?<![0-9a-f])0x2105(?![0-9a-f])|mainnet"), MAINNET),
    (re.compile(r"--broadcast"), "every broadcast is human-only in the solo phase."),
    (re.compile(r"(?i)\bcast\s+(send|wallet|mktx|publish)\b"), "cast send/wallet is human-only."),
    # .env files (a .env.example template is fine), key material and secret variable names.
    (re.compile(r"(?i)\.env(?:rc)?\b(?!\.(?:example|sample|template)\b)"), SECRETS),
    (
        re.compile(
            r"(?i)keystore|private[_-]?key|mnemonic|seed[_-]?phrase|wallet[_-]?secret"
            r"|cdp[_-]?api[_-]?key|anthropic[_-]?api[_-]?key|\.pem\b|\bid_(?:rsa|ecdsa|ed25519)\b"
        ),
        SECRETS,
    ),
    # Whole-environment dumps: printenv, os.environ, /proc/*/environ, PowerShell's env: drive.
    (re.compile(r"(?i)\bprintenv\b|environ\b|getenvironmentvariables|\benv:(?!\w)"), SECRETS),
    (re.compile(r"(?i)seal"), SEALED),
    (
        re.compile(
            r"(?i)(?:^|[\s;&|({]|\$\()eval\s|\binvoke-expression\b|\biex\b"
            r"|\b(?:powershell|pwsh)(?:\.exe)?\b.*\s-(?:e|ec|en\w*)\b"
        ),
        DECODE_AND_RUN,
    ),
]

# Bare commands that print every environment variable. Matched against a whole segment, so
# `env FOO=1 cmd` and `set -euo pipefail` still work.
ENV_DUMP = re.compile(r"(?i)env(?:\s+-\S+)*|set|export(?:\s+-p)?|declare(?:\s+-\w+)*")

URL = re.compile(r"(?i)\b(?:https?|wss?)://[^\s'\"]+")
# Flags and variables that pick a chain or an RPC endpoint; their value must name a safe one.
NETWORK_CHOICE = re.compile(
    r"(?i)(?:--(?:rpc-url|fork-url|rpc|network|chain|chain-id)[\s=]+|\bcast\b.*\s-r\s+"
    r"|\b\w*rpc\w*=)(\S+)"
)
SAFE_NETWORK = re.compile(r"(?i)sepolia|84532|localhost|127\.0\.0\.1|anvil|hardhat")

RAW_SANCTIONS = re.compile(r"(?i)\bdata/sanctions\b")
READ_ONLY_COMMANDS = {
    "cat", "head", "tail", "less", "more", "wc", "ls", "dir", "file", "stat", "grep", "egrep",
    "fgrep", "rg", "cmp", "diff", "jq", "md5sum", "sha1sum", "sha256sum", "sha512sum", "shasum",
    "cd", "pushd", "popd", "echo", "get-content", "gc", "type", "select-string", "sls",
    "get-childitem", "gci", "get-item", "get-filehash", "set-location", "sl",
}  # fmt: skip
READ_ONLY_GIT = {"log", "diff", "show", "status", "blame", "ls-files", "ls-tree", "grep"}

BASE64_DECODE = re.compile(
    r"(?i)base64\s+(?:-d|-D|--decode)\b|b64decode|frombase64string|\batob\(|,\s*['\"]base64['\"]"
)
SHELL = re.compile(
    r"(?i)\b(?:sh|bash|zsh|dash|pwsh|powershell|python\d*|node|deno|ruby|perl)(?:\.exe)?\b"
)

HARMLESS_REDIRECTS = re.compile(r"\d*>&\d+|\d*>\s*(?:/dev/null|\$null|nul)(?![\w/])")
SEGMENT_SPLIT = re.compile(r"\|\||&&|[;|&\n(){}`]")


def views(command: str) -> list[str]:
    """The command as written, plus forms with quoting and path noise removed, so that
    `.e""nv`, `ml\\eval\\sealed` and `ml/eval/./sealed` look like the paths they name."""
    unquoted = re.sub(r"[\"'`]", "", command)
    slashed = re.sub(r"/{2,}", "/", re.sub(r"/(?:\./)+", "/", unquoted.replace("\\", "/")))
    unescaped = unquoted.replace("\\", "")
    return [command, slashed, unescaped]


def segments(command: str) -> list[str]:
    """Split into simple commands, ignoring literal strings and redirects that write nothing."""
    code = re.sub(r"'[^']*'", "''", command)
    code = re.sub(r'"[^"$`]*"', '""', code)
    code = HARMLESS_REDIRECTS.sub(" ", code)
    return [s.strip() for s in SEGMENT_SPLIT.split(code) if s.strip()]


def is_read_only(segment: str) -> bool:
    words = segment.split()
    while words and re.match(r"^\w+=", words[0]):
        words.pop(0)
    if not words:
        return True
    name = re.split(r"[\\/]", words[0].strip("\"'"))[-1].lower().removesuffix(".exe")
    if name == "git":
        return len(words) > 1 and words[1].lower() in READ_ONLY_GIT
    return name in READ_ONLY_COMMANDS


def check(command: str) -> str | None:
    """Return why `command` is blocked, or None to allow it."""
    forms = views(command)
    for pattern, reason in DENY_PATTERNS:
        if any(pattern.search(form) for form in forms):
            return reason

    parts = segments(command)
    if any(ENV_DUMP.fullmatch(part) for part in parts):
        return SECRETS

    for form in forms:
        if any(re.search(r"(?i)\bbase\b", url) and "sepolia" not in url.lower()
               for url in URL.findall(form)):
            return MAINNET
        if any(not SAFE_NETWORK.search(value) for value in NETWORK_CHOICE.findall(form)):
            return MAINNET

    if any(re.search(r"(?i)\bml/eval\b", form) for form in forms) and re.search(r"[*?\[]", command):
        return SEALED

    if any(RAW_SANCTIONS.search(form) for form in forms):
        if ">" in " ".join(parts) or not all(is_read_only(part) for part in parts):
            return RAW_DATA

    if BASE64_DECODE.search(command) and SHELL.search(command):
        return DECODE_AND_RUN

    return None


def main() -> int:
    try:
        command = json.load(sys.stdin)["tool_input"]["command"]
        if not isinstance(command, str):
            raise TypeError(f"tool_input.command is {type(command).__name__}, not a string")
        reason = check(command)
    except Exception as exc:  # any failure must block; see the module docstring
        reason = f"guard.py could not check this command ({exc!r}), so it fails closed."

    if reason:
        print(f"Blocked by TOUCHSTONE policy: {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
