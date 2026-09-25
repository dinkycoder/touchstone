# CLAUDE.md — TOUCHSTONE

Pre-settlement counterparty-trust & sanctions oracle for AI-agent payments on Base.
We sell screening DECISIONS + EVIDENCE, never legal conclusions.

Full plan: [docs/plan/solo-build-plan.md](docs/plan/solo-build-plan.md) — read it, don't duplicate it here.
Current sprint: [docs/sprint/CURRENT.md](docs/sprint/CURRENT.md).

## Environment (this machine)
- Windows 11, Python 3.12 via `py -3.12`, venv at `.venv`. Every `uv run X` in the plan doc means
  `.venv/Scripts/python -m X` here.
- Console is cp1252; `.claude/settings.json` sets `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` so hooks and
  scripts don't mis-decode. Don't remove those.
- Both Bash (Git Bash) and PowerShell are in active use — guardrail hooks match both tools.

## Operating model
Solo build: one human reviews everything. Work arrives as PRs from worktree sessions. The Claude review
action and any subagent are second readers, never approvers. Roles in docs/handoff/ROLES.md (once it
exists) are future teammates — keep code, commits and notes legible to them.

`main` is protected by a GitHub ruleset: PR required, `test` check must pass, no force-push, empty bypass
list (nobody, including the repo owner, can push directly). Squash-merge is the only merge method. This
means local Git hygiene rules exist for good workflow, not because they're the only thing stopping a bad
push.

## Solo-phase scope (plan Section 2)
- NO custom contracts on mainnet. EAS schema v1 has no resolver; the attester is a managed signer.
- The API returns riskTier + evidence. Sanctions hits are REVIEW_REQUIRED; never emit BLOCK.
- Arabic is the only gating language adapter; all others are provisional.

## Architecture (plan Section 4 repo layout — most of this doesn't exist yet; Sprint 1 is tooling only)
- `services/api` Flask `/check/fast`, `/check/deep` behind x402 (CDP facilitator); responses signed.
- `services/ingest` Base events + sanctions lists -> PostgreSQL + pgvector.
- `ml/matching` is language-pluggable; see `ml/matching/core/INTERFACE.md` once it exists.

## Commands
- `.venv/Scripts/python -m pytest -q`
- `.venv/Scripts/python scripts/check_docs.py` / `.venv/Scripts/python scripts/gen_readme.py`
- `.venv/Scripts/python -m ruff check --fix && .venv/Scripts/python -m ruff format` (once ruff is added)

## Non-negotiables (hooks enforce these; do not work around them)
- Never read or print keys, `.env`, keystores. Never run anything against Base mainnet (chain id 8453).
- Never edit `data/sanctions/raw/**`. Only salted entity hashes onchain; evidence stays offchain.
- TDD: tests first; never weaken or delete a test to pass. Matcher changes must pass the per-language gate.
- Verify x402/CDP/EAS/ERC-8004 APIs against installed source or spec; never invent names or addresses.

## Git and docs
- Never commit to main. Work on the worktree branch or `feat/<scope>-<topic>`.
- After each green test cycle: Conventional Commit (`feat(matcher-ar): …`, `fix(api): …`, `docs: …`), then
  `git push -u origin HEAD`.
- First push of a task: `gh pr create --draft --fill`. Keep the PR checklist current.
- If `scripts/check_docs.py` flags docs, run `/readme-sync` before finishing. Never type metrics into docs.
- `/ship` (human-triggered) runs the full checklist and marks the PR ready for review. Claude never merges.

## Stop-and-ask list
Anything touching real keys, CDP/wallet setup, onchain schema registration, or mainnet is a founder-only
step. If a task would require one, print the exact command(s) and stop — don't run them.
