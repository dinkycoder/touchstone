# Learning plan

Learn each topic just before the sprint that needs it, one level deeper than the sprint needs. The book's
foundations chapters are the pre-reading; the quiz at the end of each one is the check.

**The rule that makes this work:** don't merge what you can't explain. Before merging a PR, write two or
three sentences in its description, in your own words, about what it does and why. Claude asks follow-up
questions until the explanation holds up.

**Where you start:** you already know sanctions screening and multilingual name matching from practice.
The new ground is blockchain, onchain payments, and AI engineering at production quality. The plan spends
its time there.

Sprints follow the plan's weeks in [docs/plan/solo-build-plan.md](../docs/plan/solo-build-plan.md)
Section 12.

## Now, before Sprint 2 (Weeks 3–4: sanctions ingestion, Arabic matcher v0, benchmark, sealed set)

This sprint sits on your home ground, so the learning is about measuring it rigorously in code.

- **Read:** [Ch. 8, Machine learning for name matching](chapters/08-ml-name-matching.md) and
  [Ch. 2, Sanctions screening](chapters/02-sanctions-screening.md) (you'll correct more than you learn in
  Ch. 2; those corrections become its field notes).
- **Hands-on (off the critical path):**
  - Compute precision, recall and false-positive rate by hand on 20 invented name pairs, then check your
    numbers with scikit-learn.
  - Plot a calibration curve for a toy classifier and explain what a well-calibrated 0.8 means.
  - Open one entry from each list's published format (OFAC XML, UN XML, EU, UK) and find where the
    native-script name lives.
- **Book:** draft [Ch. 10](chapters/10-sprint-1-guardrails.md) now (Sprint 1 already shipped); draft
  [Ch. 11](chapters/11-sprint-2-ingest-and-matcher.md) after the sprint ships.
- **Research:** H1 (do agent registrations name an operator?) and H3–H4 (the GENIUS Act rule and its
  comment letters) in the [evidence log](research/evidence-log.md).
- **Curriculum:** Machine Learning (Intro to ML, Data Preprocessing, Logistic Regression); Relational
  Databases; Software Testing and CI/CD.

## Before Sprint 3 (Weeks 5–6: x402 API, EAS attestations, ERC-8004 reads, all on Sepolia)

The biggest learning block. Start it during Sprint 2.

- **Read, in order:** [Ch. 3](chapters/03-blockchains.md) → [Ch. 4](chapters/04-ethereum-and-base.md) →
  [Ch. 5](chapters/05-stablecoins.md) → [Ch. 6](chapters/06-x402.md) →
  [Ch. 7](chapters/07-identity-and-reputation.md).
- **Hands-on.** Use Sepolia and throwaway keys only; you run anything that touches a key, and Claude
  prints the commands.
  - Generate a throwaway key offline, sign a message, and recover the signer's address from the
    signature.
  - Read a USDC balance on Base Sepolia, then find the same transfer on a block explorer.
  - Look up one EAS attestation on Base Sepolia and decode its fields against its schema.
  - Trace one x402 request against a local test server: the 402 response, the signed payment, the retry.
- **Book:** Ch. 3–7 drafted before the sprint; [Ch. 12](chapters/12-sprint-3-paid-signed-decision.md)
  after.
- **Research:** H5 (would sellers pay per check?) and H6 (how much x402 volume is really agentic?).
- **Curriculum:** Blockchain specialization (Intro to Blockchain, Decentralized Applications, Blockchains
  in Practice, Decentralized Finance); Back Ends (Flask).

## Before Sprint 4 (Weeks 7–8: fine-tuned matcher, calibration, Sybil-resistant reputation)

- **Read:** Ch. 8 again (the embeddings, fine-tuning and calibration sections) and Ch. 7's section on
  Sybil attacks.
- **Hands-on:**
  - Fine-tune a small multilingual encoder on public alias pairs (never the sealed set), and compare it
    with the Sprint 2 baseline.
  - Run k-means on invented rater data, then stage a Sybil attack on a naive average and watch it win.
- **Book:** [Ch. 13](chapters/13-sprint-4-getting-better-honestly.md) after the sprint.
- **Research:** H7 (is naive ERC-8004 reputation Sybil-prone?).
- **Curriculum:** Machine Learning (Clustering, Intro to Deep Learning, AI Model Fine-Tuning, Linear
  Algebra for ML).

## Before Sprint 5 (Weeks 9–10: rationales, review console, explorer page, MCP server)

- **Read:** [Ch. 9, Building with LLMs and coding agents](chapters/09-llms-and-coding-agents.md).
- **Hands-on:**
  - Write a rationale template, then an LLM-drafted rationale for the same match, and list what the LLM
    added that you wouldn't sign.
  - Sketch the review console's screens before building them: what a reviewer needs to see to decide in
    under a minute.
- **Book:** [Ch. 14](chapters/14-sprint-5-humans-in-the-loop.md) after the sprint.
- **Curriculum:** AI Engineering Techniques (Prompt Engineering, LLM-Based Apps, AI Agents); Interactive
  Web Pages; User-Centered Design; Professionalism and Ethics.

## Before Sprint 6 (Weeks 11–12: release checklist, monitoring, p95 target, and the mainnet decision)

- **Read:** the release and governance sections of the plan (Sections 12–13), then Ch. 15's outline.
- **Hands-on:**
  - Measure p95 latency of `/check/fast` locally and explain why p95 is the target instead of the
    average.
  - Walk through the release checklist and the 24-hour cooling-off, and write down what each step
    protects against.
- **Book:** [Ch. 15](chapters/15-sprint-6-going-live.md) after the sprint; refresh Part IV
  (Ch. 16–18) with "as of" dates.
- **Curriculum:** Performance Monitoring; CI/CD and Software Maintenance; Cloud Foundations;
  Microservices I–II.

## Curriculum coverage

| Curriculum area | Where it shows up | Chapters |
|---|---|---|
| Managing AI Engineering | Sprints, user-centered design, ethics of screening decisions | 1, 2, 14 |
| Web Application and Interface Design | Flask API, PostgreSQL + pgvector, explorer page | 11, 12, 14 |
| Software Testing and CI/CD | Test-first development, CI, hooks, monitoring | 10, 15 |
| AI Engineering Techniques | LLM rationales, Streamlit console, vector search, agents, MCP | 9, 14 |
| Software Design and Architecture | The language-adapter interface, service boundaries | 8, 11 |
| Machine Learning to Fine-Tuning | Calibrated matcher, fine-tuning, clustering | 8, 11, 13 |
| AI and Organizational Transformation | How compliance teams adopt automated screening | 2, 16 |
| Microservices Architectures | API, ingest and MCP services in containers | 12, 15 |
| Blockchain specialization | Base, EAS, ERC-8004, x402, USDC | 3–7, 12 |
| Cloud specialization | Deployment in Sprint 6 | 15 |

**Weakest fit: DeFi.** Touchstone touches stablecoin payments and counterparty risk, but not exchanges or
lending. Chapter 5 covers the DeFi basics the course expects, and Chapter 18 looks at credit, the phase-two
product, which is where DeFi comes back in.

## Quiz log

One row per quiz session. It's evidence of learning for the capstone, and it tells the drafts where to
get clearer.

| Date | Chapter | Shaky on | What changed in the chapter |
|---|---|---|---|
