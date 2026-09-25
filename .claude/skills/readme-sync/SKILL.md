---
name: readme-sync
description: Regenerate docs-map.yml-managed README blocks from their source of truth, then verify with check_docs.py. Use before finishing any task that touched a generated block's source (docs/sprint/CURRENT.md frontmatter, or a future benchmark/endpoint manifest) or whenever `gen_readme.py --check` or check_docs.py flags drift.
---

Run, in order, and report the output of each:

1. `.venv/Scripts/python scripts/gen_readme.py`
2. `.venv/Scripts/python scripts/check_docs.py`

If step 2 still fails after step 1, the mismatch is either a path missing from `docs/docs-map.yml` or a doc
that genuinely needs a hand-written update (docs-map.yml only tracks "did the doc change too," not the
content) — fix it directly. Never hand-edit the generated region between the `docs-map:start`/`docs-map:end`
markers, and never type a metric into a doc by hand.
