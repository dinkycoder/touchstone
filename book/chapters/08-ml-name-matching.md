---
chapter: 8
title: Machine learning for name matching
part: II. Foundations
status: outline
durability: durable
written: before Sprint 2 (sections 1–5); the fine-tuning section before Sprint 4
curriculum: [Introduction to Machine Learning, Data Preprocessing, Logistic Regression, Introduction to Deep Learning, AI Model Fine-Tuning]
---

# 8. Machine learning for name matching

**By the end, the reader can:**
- describe the matching pipeline: normalize, block, score, calibrate, decide
- explain why matchers are measured by recall at a fixed false-positive rate instead of by accuracy
- explain calibration, leakage, and why a sealed test set exists
- list the Arabic naming features that break exact matching

## Outline

1. **Why exact matching fails.** Transliteration, script, word order, missing parts, and deliberate
   variation.
2. **Arabic as the reference language.** Romanization families (Muhammad, Mohammed, Mohamed); the
   article and sun-letter assimilation; Abd al- compounds; nasab chains (bin, ibn, bint, ould); kunya (Abu,
   Umm); laqab and nisba; missing short vowels; hamza and alef forms; ta marbuta; alif maqsura; tashkeel;
   tatweel; Arabizi; name order. Match native script to native script when both sides have it, and fall
   back to romanized variants otherwise.
3. **The pipeline.** Normalization, blocking keys, candidate scoring (string similarity first,
   embeddings later), calibration into a probability, and a threshold that's a policy decision.
4. **Measuring honestly.** Precision, recall and false-positive rate; recall at a fixed FPR; calibration
   and expected calibration error; why accuracy is meaningless when true hits are rare.
5. **Not fooling yourself.** Train, dev and test splits; leakage; a sealed set nobody tuning the model
   can see; reporting only aggregates from it.
6. **One interface, many languages.** The `LanguageAdapter` protocol, and why a new language reports
   metrics but doesn't gate releases until a native reviewer signs off.
7. **Fine-tuning** (drafted before Sprint 4). Multilingual encoders, training pairs from public aliases,
   hard negatives.

> **From the field:** which variants matter most in real screening, and which ones analysts learn to
> ignore. (Founder.)

## In Touchstone

- `ml/matching/core/` and `ml/matching/languages/arabic/` (planned, Sprint 2)
- `ml/eval/sealed/`, which agents are denied and `guard.py` blocks
- The `LanguageAdapter` protocol in the [plan](../../docs/plan/solo-build-plan.md), Section 11

## Quiz

1. Why measure recall at a fixed false-positive rate instead of accuracy?
2. A calibrated model says 0.8. What does that mean, and why does a reviewer need it?
3. What is leakage, and how does a sealed set protect against tuning to the test?
4. Name three Arabic naming features that break exact matching, and how normalization handles each.
5. Why doesn't a new language gate releases until a native reviewer signs off?

## Sources to check

- scikit-learn documentation on probability calibration
- [docs/plan/solo-build-plan.md](../../docs/plan/solo-build-plan.md), Section 11
- Published research on cross-script name matching and transliteration (to find while drafting)
