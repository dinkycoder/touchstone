---
chapter: 13
title: "Sprint 4: Getting better honestly"
part: III. Building Touchstone
status: outline
durability: durable
written: after Sprint 4 ships
curriculum: [Introduction to Deep Learning, AI Model Fine-Tuning, Clustering with Unsupervised Learning]
---

# 13. Sprint 4: Getting better honestly

A planned outline from the [solo build plan](../../docs/plan/solo-build-plan.md), Section 12, Weeks 7–8.
It gets rewritten once the sprint ships.

**By the end, the reader can:**
- explain how the matcher was fine-tuned and calibrated, and how the gain was checked for leakage
- explain what the evasion red team does, and why its output starts as provisional
- explain the Sybil-resistant scorer and how it was compared with a naive average
- say what the public benchmark claims and what it deliberately doesn't

## Planned outline

1. **Fine-tuning the matcher.** Training pairs from public aliases, hard negatives, calibration.
2. **Suspicious gains.** Why any improvement of more than five points triggers a leakage review.
3. **The red team.** The `evasion-red-team` subagent writes plausible evasion variants; they stay
   provisional until the founder validates them.
4. **Sybil-resistant reputation.** Clustering raters, collapsing each cluster to one voice, and ranking
   against ground truth on staged attacks.
5. **Publishing a benchmark.** What goes public, what stays sealed, and how to word claims.

## In Touchstone

- `ml/matching/`, `ml/reputation/`, `ml/eval/` (planned)

## Research

- [Evidence log](../research/evidence-log.md) H7

## Anticipated quiz

1. Why does a gain of more than five points trigger a review rather than a celebration?
2. Why are red-team fixtures provisional until a human validates them?
3. What does collapsing a rater cluster change in the final ranking?
4. What can a public benchmark claim, and what can't it?
