---
chapter: 11
title: "Sprint 2: Sanctions data in, candidates out"
part: III. Building Touchstone
status: outline
durability: durable
written: after Sprint 2 ships
curriculum: [Relational Databases, Data Preprocessing, Paradigms and Patterns]
---

# 11. Sprint 2: Sanctions data in, candidates out

A planned outline from the [solo build plan](../../docs/plan/solo-build-plan.md), Section 12, Weeks 3–4.
It gets rewritten around what actually happened once the sprint ships.

**By the end, the reader can:**
- explain how the four lists are ingested deterministically, and why raw data is never edited
- describe what data lineage records and why an examiner would ask for it
- explain how the Arabic adapter was built test-first, one naming feature at a time
- explain why the sealed set was frozen before any tuning

## Planned outline

1. **Four lists, four formats.** One parser per list; where native-script names come from.
2. **Raw data is read-only.** Why, and how `guard.py` enforces it.
3. **Data lineage.** What came from where, when, and in which version.
4. **The Arabic adapter v0.** Each naming feature from Chapter 8 as a fixture and a test.
5. **The benchmark harness.** The dev split, the baseline, report files as the only source of numbers.
6. **Freezing the sealed set.** Why the person who writes the labels mustn't be able to tune to them.
7. **Measuring H1.** Do agent registrations name an operator? (Only if the mainnet-read decision in the
   evidence log is settled.)

## In Touchstone

- `services/ingest/`, `ml/matching/core/`, `ml/matching/languages/arabic/`, `ml/eval/` (planned)

## Anticipated quiz

1. Why is `data/sanctions/raw/` read-only even for the person who fetched it?
2. What does a lineage record hold, and who would ask for it?
3. What does the baseline measure, and why keep it after better models exist?
4. Why freeze the sealed set before any tuning?
