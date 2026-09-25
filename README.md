# TOUCHSTONE

Pre-settlement counterparty-trust and sanctions oracle for AI-agent payments on Base.

Full plan: [docs/plan/solo-build-plan.md](docs/plan/solo-build-plan.md)

The book being written alongside the build: [book/README.md](book/README.md)

## Status

<!-- docs-map:start:sprint-status -->
**Sprint 1 (in-progress):** Repo, CI, and full .claude guardrail config; validate every hook blocks what it should.
<!-- docs-map:end:sprint-status -->

See [docs/sprint/CURRENT.md](docs/sprint/CURRENT.md) for details. Don't hand-edit the block above — run
`.venv/Scripts/python scripts/gen_readme.py` (or the `readme-sync` skill) instead.

## Development

```
py -3.12 -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python -m pytest -q
.venv/Scripts/python scripts/gen_readme.py --check
.venv/Scripts/python scripts/check_docs.py
```
