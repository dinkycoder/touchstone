---
chapter: 1
title: Who's behind the wallet?
part: I. The problem
status: outline
durability: durable
written: late (it frames the whole book)
curriculum: [User-Centered Design, AI and Business Transformation]
---

# 1. Who's behind the wallet?

**By the end, the reader can:**
- say in one paragraph what Touchstone decides, for whom, and when
- explain why checking a wallet address isn't the same as checking who controls it
- name what Touchstone never claims

## Outline

1. **A payment between two programs.** An invented scenario: an agent buys a data lookup for a fraction
   of a cent. The seller has a moment to decide and no idea who operates the buyer.
2. **Why the seller should care.** Sanctions liability doesn't disappear because the counterparty is
   software. (Chapter 2 explains the law; this section only raises the stakes.)
3. **Addresses versus entities.** Screening an address checks it against a list of known wallets. A
   sanctioned party can create a new wallet in seconds. The real question is who operates it.
4. **What Touchstone returns.** A risk tier plus evidence, signed, fast enough to sit in front of the
   payment. Never a legal conclusion: a sanctions hit comes back as `REVIEW_REQUIRED` for a human, never
   as an automatic block.
5. **The touchstone.** The assayer's stone as a metaphor, and the route through the book.

## In Touchstone

- `/check/fast` and `/check/deep` in `services/api` (planned, Sprint 3)
- The solo-phase scope rules in [CLAUDE.md](../../CLAUDE.md)

## Research

- [Evidence log](../research/evidence-log.md) H1 (is there an operator to find?) and H2 (does address
  screening miss it?)

## Quiz

1. In one sentence: what does Touchstone decide, and for whom?
2. Why isn't screening the wallet address enough?
3. Why does a hit come back as `REVIEW_REQUIRED` instead of a block?
4. What does Touchstone never claim to provide?

## Sources to check

- [docs/plan/solo-build-plan.md](../../docs/plan/solo-build-plan.md), Sections 1–2
