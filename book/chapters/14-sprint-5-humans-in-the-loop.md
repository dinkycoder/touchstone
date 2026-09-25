---
chapter: 14
title: "Sprint 5: Humans in the loop"
part: III. Building Touchstone
status: outline
durability: durable
written: after Sprint 5 ships
curriculum: [LLM-Based Apps, User-Centered Design, Interactive Web Pages, Professionalism and Ethics]
---

# 14. Sprint 5: Humans in the loop

A planned outline from the [solo build plan](../../docs/plan/solo-build-plan.md), Section 12, Weeks 9–10.
It gets rewritten once the sprint ships.

**By the end, the reader can:**
- explain how rationales are produced, and why templates come before LLM drafts
- describe what the review console shows a reviewer, and why
- explain what the public explorer page does and doesn't reveal
- explain what hardening the MCP server involved

## Planned outline

1. **Rationales.** Templates first, then LLM drafts that a human signs off on; the words a rationale must
   never use.
2. **The review console.** A Streamlit queue built around one question: what does a reviewer need to see
   to decide in under a minute?
3. **Every `REVIEW_REQUIRED` gets a human.** The founder confirms each one during the sprint.
4. **The Agent Trust Explorer.** One static page, and what it deliberately leaves out.
5. **Hardening the MCP server.** Rate limits, input validation, and what the second reader found.
6. **First design partners on Sepolia.** This needs conversations; see the
   [evidence log](../research/evidence-log.md) on what research can't replace.

## In Touchstone

- `console/`, `web/`, `services/mcp/` (planned)

## Anticipated quiz

1. Why do templates come before LLM-drafted rationales?
2. What must a reviewer see to clear a match, and what would slow them down?
3. What should a public explorer never show?
