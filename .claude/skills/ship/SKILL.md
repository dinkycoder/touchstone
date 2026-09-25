---
name: ship
description: Human-triggered pre-push checklist for TOUCHSTONE - tests, docs sync, conventional commit, push, mark the PR ready for review. Only run this when the founder explicitly asks to ship; never invoke it proactively.
---

Run each step in order; stop and report if any step fails instead of continuing to the next one.

1. `.venv/Scripts/python -m pytest -q`
2. `.venv/Scripts/python scripts/gen_readme.py --check` and `.venv/Scripts/python scripts/check_docs.py`
   — if either fails, run the `readme-sync` skill first, then re-run this step.
3. Confirm the current branch is not `main`/`master` (never commit there — `main` is also protected by a
   GitHub ruleset that would reject the push anyway).
4. Review `git status` (never `git add -A`/`.` blindly), stage the relevant files, and commit with a
   Conventional Commits message (`feat(scope): summary`, `fix: summary`, `docs: summary`, ...).
5. `git push -u origin HEAD`.
6. If this branch has no open PR yet: `gh pr create --draft --fill`. If a draft PR already exists: mark it
   ready with `gh pr ready`.
7. Report the PR URL and the checklist state back to the founder. Never run `gh pr merge` — the founder
   merges.
