---
chapter: 15
title: "Sprint 6: Going live carefully"
part: III. Building Touchstone
status: outline
durability: durable
written: after Sprint 6 ships
curriculum: [Performance Monitoring, CI/CD and Software Maintenance, Cloud Foundations, Microservices II]
---

# 15. Sprint 6: Going live carefully

A planned outline from the [solo build plan](../../docs/plan/solo-build-plan.md), Sections 12–13, Weeks
11–12. It gets rewritten once the sprint ships. Whether this sprint includes mainnet is the founder's
decision.

**By the end, the reader can:**
- explain the release checklist and what each step protects against
- explain why there's a 24-hour cooling-off before any mainnet step
- explain why the latency target is the 95th percentile rather than the average
- describe what the handoff package gives the first hire

## Planned outline

1. **The release checklist.** What's on it, and the failure each item exists to prevent.
2. **Separation of duties for one person.** The 24-hour cooling-off, and the founder running the mainnet
   steps personally.
3. **Keys and caps.** Who holds which key, and why payments start capped.
4. **Monitoring and p95.** Measuring latency the way users feel it.
5. **The ship log and the handoff.** Leaving the repo ready for the first teammate.

## In Touchstone

- `scripts/release-mainnet.sh` (founder-only; `guard.py` blocks it for Claude)
- `docs/ship-log/` and `docs/handoff/` (planned)

## Anticipated quiz

1. What does a 24-hour cooling-off protect against when there's only one person?
2. Why is p95 the target and not the average?
3. Why start with capped payments?
