---
chapter: 2
title: Sanctions screening from first principles
part: I. The problem
status: outline
durability: durable (law summaries get re-checked each release)
written: during Sprint 2
curriculum: [Professionalism and Ethics, Adopting AI in Your Organization]
---

# 2. Sanctions screening from first principles

The founder's home ground. Claude drafts it; the founder's field notes are what make it worth reading.

**By the end, the reader can:**
- explain what a sanction does, and who publishes the four lists Touchstone uses
- explain strict liability and OFAC's 50 Percent Rule, and why the rule makes this an entity problem
- describe the steps of a screening process, from candidates to a recorded decision
- explain why false positives and false negatives cost different people different things

## Outline

1. **What a sanction is.** Blocking property and prohibiting dealings. Who imposes them: the US (OFAC),
   the UN Security Council, the EU, the UK.
2. **Four lists, four formats.** What each list contains and where each one keeps names in their original
   script: OFAC's advanced XML with script IDs, the UN list's "Name (original script)", the EU list's
   `nameLanguage` tag, the UK list's non-Latin-script fields. Check which UK list is authoritative when
   drafting.
3. **Who has to comply.** US persons, and why civil liability is strict: not knowing isn't a defence,
   though a compliance program affects the penalty.
4. **Entities, not just names.** Ownership and control, the 50 Percent Rule, aliases and weak aliases.
   This is the gap between screening a name and screening who someone really is.
5. **What screening actually is.** Generating candidates, scoring them, human review, a decision, and a
   record of it. Alert fatigue, and why better recall is worthless if analysts drown.
6. **Errors cost differently.** A false positive refuses a legitimate customer and can harm their
   reputation; a false negative is a violation. Thresholds are policy choices, not technical ones.
7. **Evidence, not conclusions.** Why Touchstone returns `REVIEW_REQUIRED` and never `BLOCK`, and what
   the audit trail has to hold.

> **From the field:** how screening decisions get defended in practice, and what a reviewer needs to see
> to clear or escalate a match. (Founder; check pre-publication review first.)

## In Touchstone

- List parsers in `services/ingest` (planned, Sprint 2)
- `data/sanctions/raw/` is read-only, and `guard.py` enforces it
- The `REVIEW_REQUIRED` rule in [CLAUDE.md](../../CLAUDE.md)

## Research

- [Evidence log](../research/evidence-log.md) H2 (address versus entity screening) and H4 (what buyers
  say is hard)

## Quiz

1. What does strict liability mean for a seller who accepts an automated payment?
2. What is the 50 Percent Rule, and why does it make entity resolution harder than name matching?
3. Where does each of the four lists keep a name in its original script?
4. Who bears the cost of a false positive, and who bears the cost of a false negative?
5. Why does Touchstone route hits to a human instead of blocking them?

## Sources to check

- OFAC: the SDN list and its data formats; guidance on the 50 Percent Rule; the Economic Sanctions
  Enforcement Guidelines (31 CFR Part 501, Appendix A); Sanctions Compliance Guidance for the Virtual
  Currency Industry (2021)
- UN Security Council Consolidated List; the EU's consolidated financial sanctions list; the UK
  sanctions list (confirm which one is current)
- [docs/plan/solo-build-plan.md](../../docs/plan/solo-build-plan.md), Section 11
