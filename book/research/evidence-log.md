# Evidence log

The solo build doesn't include customer interviews. This log gets most of the same information from
public records and measurement instead. Each open question is a hypothesis, tested against a named source
and recorded with a date and a confidence level. The book's market chapters cite this log, and so does any
pitch.

## What interviews would have told us, and where it comes from instead

| Interviews would tell us | Source instead |
|---|---|
| Who feels the pain, and why | Public comment letters on the GENIUS Act sanctions rule: buyers explaining their problems to a regulator, in writing. OFAC enforcement actions against crypto firms: what failures cost. |
| What they use today | Competitors' docs, pricing pages, GitHub repos, changelogs and job postings |
| Whether there's data to match on | Measuring it onchain: how many agent registrations name an operator (H1) |
| What they'd pay | Revealed demand: call counts on a live Sepolia endpoint behind the x402 paywall; competitor pricing; typical x402 payment sizes |
| What would make them switch | Builders' public issues and threads (x402 GitHub, ERC-8004 discussion, Base builder channels); gaps named in analyst reports |

**What this can't replace:** commitment. Research shows what people say and do in public; it can't show
whether a specific buyer will integrate or sign a letter of intent. The fund milestones in the
market-thesis report (3–5 design partners, one letter of intent) still need conversations, later.

## Method

- **Primary sources first.** A law firm's summary of a rule is a pointer; the rule text is the source.
  Aggregator sites are leads only (the market-thesis report already found them disagreeing).
- **Every finding has a date,** the date the source was read, because this field moves monthly.
- **Record conflicts** between sources instead of picking one silently.
- **Confidence:** *high* means a primary source or our own measurement; *medium* means a credible
  secondary source; *low* means a single aggregator or an inference.
- **Keep out of this log:** sealed-set data, personal data beyond public sanctions-list entries, and
  anything non-public.

The starting point is the founder's market-thesis report (September 2026; not in the repo). Its claims
are recorded below as **reported, not yet verified**.

## Hypotheses

### H1. Agent wallets expose enough about their operator to match against sanctions lists
- **Why it matters:** this is the product's premise. With no name, there's nothing to match.
- **Reported:** ERC-8004 registration files, Basenames, funding sources and payment counterparties can
  tie a fresh wallet to a listed person or company.
- **Test:** sample agent registrations from the ERC-8004 Identity Registry on Base. Measure the share
  whose registration file names an operator, links a domain, or resolves to a Basename. Repeat monthly.
- **Blocked on:** reading Base mainnet data. `guard.py` blocks any command that names mainnet, on
  purpose. Either the founder runs these read-only queries, or we add a narrow, tested exception for
  read-only access. This is a founder decision.
- **Status:** open · **Confidence:** —

### H2. Screening addresses misses exposure that screening entities would catch
- **Why it matters:** it's the 10x claim. Coinbase's facilitator already blocks listed addresses.
- **Reported:** sanctions evasion routinely uses fresh addresses, which pass an address check by
  construction.
- **Test:** OFAC's published digital-currency addresses compared with its enforcement actions and
  designation press releases (do designated parties keep using new addresses?); analytics firms'
  published research on address rotation.
- **Status:** open · **Confidence:** —

### H3. Stablecoin issuers and their distributors must screen secondary-market flows by January 2027
- **Why it matters:** it's the regulatory demand driver and the first buyer.
- **Reported:** a FinCEN/OFAC proposed rule (April 8, 2026) under the GENIUS Act requires sanctions
  programs "across both primary and secondary market activity", effective by January 18, 2027 at the
  latest.
- **Test:** the proposed rule's text in the Federal Register; whether a final rule has been issued, and
  what changed.
- **Status:** open · **Confidence:** —

### H4. What buyers say is hard about screening automated flows
- **Why it matters:** these are the interview answers, written down.
- **Test:** read the public comment letters on the H3 rule. Tag each pain point (volume, false
  positives, secondary-market visibility, cost, explainability) and count how many letters raise it.
- **Status:** open · **Confidence:** —

### H5. Sellers would pay $0.001–0.003 per check
- **Why it matters:** unit economics. The report puts the average x402 payment near $0.20, so screening
  has to cost around 1–2% of the payment or less.
- **Test:** competitor pricing pages; the average payment size from the H6 sources; call counts once a
  Sepolia endpoint is live.
- **Status:** open · **Confidence:** —

### H6. Only a small share of x402 volume is really agent-driven today
- **Why it matters:** timing risk. The report says per-check revenue is trivial at today's volume.
- **Reported:** TRM Labs found only 0.6–7.5% of screened x402 commerce plausibly agentic, roughly
  $5,000–11,000 a month.
- **Test:** the TRM report itself (method and date range), cross-checked with other published counts;
  re-measured monthly. That monthly measure could become the "Base Agent Trust Index" the report
  recommends.
- **Status:** open · **Confidence:** —

### H7. Naive reputation averages on ERC-8004 can be gamed by clustered raters
- **Why it matters:** it's the case for the Sybil-resistant scorer.
- **Reported:** an independent analysis of Base data found the top-ranked agent's feedback came mostly from
  a handful of addresses.
- **Test:** reproduce the analysis. This needs mainnet reads, so it's blocked in the same way as H1.
- **Status:** open · **Confidence:** —

### H8. No competitor does multilingual entity resolution for agent payments
- **Why it matters:** it's the competitive white space.
- **Reported:** t54 Labs is the closest competitor; the others do identity tokens, business
  verification, or address-level screening.
- **Test:** each competitor's public docs, API reference, changelog and job postings. Start with t54
  Labs, Skyfire, Baselayer, and TRM's and Chainalysis's agent products.
- **Status:** open · **Confidence:** —

### H9. Coinbase is more likely to partner than to build entity resolution into its facilitator
- **Why it matters:** platform risk, the report's biggest caveat after timing.
- **Test:** CDP changelogs and docs, Coinbase job postings in compliance engineering, and Coinbase
  Ventures' compliance investments.
- **Status:** open · **Confidence:** —

### H10. Base Batches and the Base Ecosystem Fund want this category and stage
- **Why it matters:** it decides the funding path.
- **Reported:** Base narrowed its priorities to trading, payments, agents and financing in 2026; Base
  Batches funds pre-seed teams, with the next cohort expected early 2027.
- **Test:** Base's own blog posts and the Batches program page, read directly.
- **Status:** open · **Confidence:** —

## Primary sources to read first

These come from the market-thesis report's source list. They're listed here so they get read at the
source.

- Base, "Base 2026 Mission, Vision, and Strategy": <https://blog.base.org/2026-mission-vision-and-strategy>
- Base, "Introducing Base Batches 004": <https://blog.base.org/introducing-base-batches-004>
- TRM Labs, "Who's Actually Paying? Measuring AI Agent Payments Onchain":
  <https://www.trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain>
- Holland & Knight on the FinCEN/OFAC GENIUS Act proposal:
  <https://www.hklaw.com/en/insights/publications/2026/04/fincen-and-ofac-propose-aml-sanctions-rules-for-stablecoin-issuers>
  (a pointer; find the rule text in the Federal Register)
- Coinbase Developer Docs, CDP Facilitator: <https://docs.cdp.coinbase.com/x402/core-concepts/facilitator>
- Coinbase Ventures, "Ideas we are excited for in 2026":
  <https://www.coinbase.com/blog/Coinbase-Ventures-Ideas-we-are-excited-for-in-2026>

## Findings

Add one entry per source read, newest first.

| Date read | Hypothesis | Source | Finding | Confidence |
|---|---|---|---|---|
