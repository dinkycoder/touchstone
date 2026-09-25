# The Touchstone book

**Working title:** *Who's Behind the Wallet? Trust and sanctions screening for AI-agent payments, built
from first principles.*

A touchstone is the dark stone assayers once used to test gold: rub the metal on it and the streak tells
you what it is. This book does the same for payments between AI agents. It explains, from first
principles, how to tell who is behind a wallet before money moves, by building a working system that
does it: [TOUCHSTONE](../README.md).

**Readers:** engineers and data scientists who are new to blockchains, compliance people who are new to
agents, and the author, who is learning both while building. The book assumes Python and curiosity, not
crypto or sanctions experience.

## How the book is written

Claude is the lead writer. The founder is the author, the domain expert and the learner, and has the
final say.

| Step | Who | What happens | Chapter `status` after |
|---|---|---|---|
| 1. Outline | Claude | Learning goals, section plan, quiz questions and sources to check | `outline` |
| 2. Draft | Claude | Full first draft from the outline, the code, and the [evidence log](research/evidence-log.md) | `draft` |
| 3. Read and quiz | Both | The founder reads the draft, then Claude quizzes them in a session. Wherever an answer is shaky, the text gets clearer. | `quizzed` |
| 4. Field notes | Founder | Adds practitioner insight in `> **From the field:**` callouts, and corrects anything that rings false | `reviewed` |
| 5. Fact-check | Claude | Every claim about the world gets a primary source and an access date; every claim about the code gets a path or commit | `fact-checked` |
| 6. Sign-off | Founder | Approves the chapter | `final` |

A confused reader is a signal about the text, not the reader: if a quiz answer is wrong, the draft
changes too.

**Pace:** one foundations chapter before each sprint (it's that sprint's pre-reading) and one build
chapter after the sprint ships. That's about three hours a week of reading and quizzing inside the
15–20 hour build week. See the [learning plan](learning-plan.md) for the sprint-by-sprint schedule.

## Rules

- **Part III chapters are written about what was built,** after the sprint ships, never ahead of it.
- **Dated facts carry a date and a source.** Part IV (the market) goes stale fastest, so each of its
  chapters says "as of" in its frontmatter and gets refreshed before any release.
- **Numbers come from outputs, never from memory.** Benchmark figures are copied from the benchmark's
  report files, the same rule as the rest of the repo ("never type metrics into docs").
- **Education, not legal advice.** The preface says so, and chapters about sanctions law point to the
  primary text instead of paraphrasing it as advice.
- **Teaching examples use invented names.** Real sanctions-list entries appear only when quoting the
  public list, with a citation.
- **Never in the book:** anything from `ml/eval/sealed/`, secrets or keys, working evasion recipes beyond
  what's already public, and anything non-public from the founder's earlier roles. Before drafting
  anything about the founder's past methods, check whether that role carries a pre-publication review
  obligation.
- **Verify APIs against the spec.** x402, CDP, EAS and ERC-8004 details are checked against the current
  spec or source before they go in a chapter, as `CLAUDE.md` requires for code.

## Contents

| # | Chapter | Part | Status | Written around |
|---|---|---|---|---|
| — | [Preface](chapters/00-preface.md) | Front matter | `outline` | Last |
| 1 | [Who's behind the wallet?](chapters/01-whos-behind-the-wallet.md) | I. The problem | `outline` | Late (it frames everything) |
| 2 | [Sanctions screening from first principles](chapters/02-sanctions-screening.md) | I. The problem | `outline` | Sprint 2 |
| 3 | [Blockchains from first principles](chapters/03-blockchains.md) | II. Foundations | `outline` | Before Sprint 3 |
| 4 | [Ethereum, smart contracts and Base](chapters/04-ethereum-and-base.md) | II. Foundations | `outline` | Before Sprint 3 |
| 5 | [Stablecoins and onchain money](chapters/05-stablecoins.md) | II. Foundations | `outline` | Before Sprint 3 |
| 6 | [Agents that pay: x402](chapters/06-x402.md) | II. Foundations | `outline` | Before Sprint 3 |
| 7 | [Identity, reputation and attestations onchain](chapters/07-identity-and-reputation.md) | II. Foundations | `outline` | Before Sprint 3 |
| 8 | [Machine learning for name matching](chapters/08-ml-name-matching.md) | II. Foundations | `outline` | Before Sprint 2 |
| 9 | [Building with LLMs and coding agents](chapters/09-llms-and-coding-agents.md) | II. Foundations | `outline` | Before Sprint 5 |
| 10 | [Sprint 1: Guardrails before code](chapters/10-sprint-1-guardrails.md) | III. Building Touchstone | `outline` | Now (Sprint 1 shipped) |
| 11 | [Sprint 2: Sanctions data in, candidates out](chapters/11-sprint-2-ingest-and-matcher.md) | III. Building Touchstone | `outline` | After Sprint 2 |
| 12 | [Sprint 3: A paid, signed decision](chapters/12-sprint-3-paid-signed-decision.md) | III. Building Touchstone | `outline` | After Sprint 3 |
| 13 | [Sprint 4: Getting better honestly](chapters/13-sprint-4-getting-better-honestly.md) | III. Building Touchstone | `outline` | After Sprint 4 |
| 14 | [Sprint 5: Humans in the loop](chapters/14-sprint-5-humans-in-the-loop.md) | III. Building Touchstone | `outline` | After Sprint 5 |
| 15 | [Sprint 6: Going live carefully](chapters/15-sprint-6-going-live.md) | III. Building Touchstone | `outline` | After Sprint 6 |
| 16 | [The agent-payments landscape](chapters/16-landscape.md) | IV. The market (dated) | `outline` | Refreshed each release |
| 17 | [Regulation and the compliance clock](chapters/17-regulation.md) | IV. The market (dated) | `outline` | Refreshed each release |
| 18 | [Building a company on it](chapters/18-building-a-company.md) | IV. The market (dated) | `outline` | Refreshed each release |
| 19 | [What's next](chapters/19-whats-next.md) | Epilogue | `outline` | Last |
| — | [Glossary](glossary.md) | Back matter | Grows with each chapter | Ongoing |

Research that replaces customer interviews lives in the [evidence log](research/evidence-log.md).

## Open decisions (founder)

- **Title.** The one above is a placeholder.
- **License.** The repo has no license yet. Code and prose can be licensed separately (for example, a
  permissive code license plus CC BY 4.0 for the book).
- **Credit for AI assistance.** How the book says it was written with Claude as lead writer. The preface
  outline assumes you'll say so plainly.
- **Format and publisher.** Plain Markdown for now; it converts cleanly to mdBook, Quarto or Leanpub
  later, so there's no need to choose yet.
- **Pre-publication review.** Whether your earlier role requires it, and for which chapters.
