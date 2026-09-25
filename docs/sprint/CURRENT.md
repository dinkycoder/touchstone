---
sprint: 1
status: in-progress
goal: Repo, CI, and full .claude guardrail config; validate every hook blocks what it should.
---

# Sprint 1 (Weeks 1-2)

Source: [docs/plan/solo-build-plan.md](../plan/solo-build-plan.md) Section 12, Wk 1-2 row.

## Goal

Repo, CI, and the full `.claude` guardrail config (hooks, settings, tests) exist and are proven to block
what they should — plus, outside Claude Code, the founder's 8-10 customer interviews, validation memo,
risk register and architecture note.

## In scope for Claude Code this sprint

- [x] `docs/plan/solo-build-plan.md` (moved here from the pasted plan; a different, superseded research
      draft remains at the repo root as `touchstone-solo-build-plan.md` — founder to archive/delete)
- [x] `CLAUDE.md`
- [x] GitHub branch ruleset on `main` (PR + passing `test` check + no force-push, empty bypass list),
      secret scanning + push protection, squash-merge-only
- [x] `.claude/settings.json` (env, permissions, hook registration)
- [x] `.claude/hooks/guard.py`, `bench_gate.py`, `commit_checkpoint.py`
- [x] `tests/hooks/` — one blocked + one allowed case per guard
- [x] `docs/docs-map.yml`, `scripts/check_docs.py`, `scripts/gen_readme.py`
- [x] `.claude/skills/readme-sync/`, `.claude/skills/ship/`
- [x] `.github/workflows/ci.yml` (pytest + `gen_readme.py --check` + check_docs)
- [x] Probe every guard once more from a live session with a command it should block (do this in `/hooks`
      and a real prompt, not just the pytest cases, before calling the sprint done)
      — 2026-09-25: `.env` read (Bash + PowerShell), mainnet `cast`, sealed eval read and
      `data/sanctions/raw` delete all blocked by `guard.py`; `git status` control allowed.

## Out of scope for Claude Code this sprint (founder-only — see CLAUDE.md "Stop-and-ask list")

- 8-10 customer interviews + validation memo, risk register, architecture note — founder's own research,
  not a coding task.
- Creating the CDP project, a Sepolia server wallet, or a hardware-wallet receive-only `payTo` address.
- Installing the GitHub Claude review app, adding `ANTHROPIC_API_KEY` as a repo secret, or setting an
  Anthropic Console spend limit, or release-please setup — needed once CI runs Claude itself (Sprint 3+),
  not for this sprint's pytest+check_docs CI.
- Anything that registers an onchain schema, touches mainnet, or reads/writes a real key.

## Definition of done

- `.venv/Scripts/python -m pytest -q` is green, including `tests/hooks/`.
- `/hooks` lists `guard.py`, `bench_gate.py` and `commit_checkpoint.py` under the right events.
- `.venv/Scripts/python scripts/gen_readme.py --check` and `.venv/Scripts/python scripts/check_docs.py`
  pass.
- Everything is committed on `chore/bootstrap` with a draft PR open against `main`.

## Next sprint preview (Wk 3-4, plan Section 12)

Four-list sanctions ingestion, Arabic adapter v0, benchmark harness, sealed set v0 — see the plan before
starting; that sprint touches `services/ingest` and `ml/matching`, neither of which exists yet.
