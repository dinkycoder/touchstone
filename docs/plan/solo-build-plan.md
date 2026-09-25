# TOUCHSTONE on Claude Code: Solo Build Plan

*One founder, Claude Code as the missing team, 12 weeks, then a team-ready handoff. Revised September 25, 2026 from the team build plan.*

## Executive Summary

When one person has to review every line an agent writes, the safe move is to shrink what gets built, not how carefully it is built. This plan keeps the team plan's full guardrail stack: hooks, permission rules, a sealed evaluation set that agents cannot read, and CI gates. It narrows scope to what one founder whose strength is data and ML can defend alone. That means sanctions ingestion, the Arabic reference matcher and its benchmark, the x402-paid check API, EAS attestations from a managed signer, a minimal review console, and TOUCHSTONE's own MCP server. Custom smart contracts stay on Sepolia and off the critical path. Nothing shipped to mainnet in the solo phase therefore depends on unaudited Solidity, and that work becomes the first hire's job.

Claude Code stands in for the missing teammates in two ways. Subagents and worktree sessions supply parallel hands. Adversarial reviewers supply a second reader: the `security-auditor` subagent, the Claude review action on every pull request, and workflows that have a second agent verify the first. These reviewers can share a model's blind spots, so the plan adds three outside humans where a wrong answer is costly. A paid native reviewer checks each language after Arabic, a sanctions-compliance advisor reviews any public true-positive claim, and an auditor reviews any custom contract before it reaches mainnet.

At roughly 15–20 focused hours a week, the six sprints still fit 12 weeks. The repo, subagents and worktree names are organized by role from day one, so each future hire inherits a ready-made seat instead of a solo codebase to decode.

"Verified" below means behavior stated in the Claude Code docs as fetched for the team plan. "Recommendation" marks design judgment.

## 1. What changes when one person builds it

The team plan divided work by person. The solo plan divides it by time and by agent. Three consequences follow.

**Review becomes the bottleneck, not typing.** Every Claude session's output still needs your judgment, so the plan caps you at three concurrent sessions: a `lead` session in the main checkout plus at most two worktree sessions. Parallel sessions also draw from your single plan's quota (docs/agent-view), so more sessions would burn usage faster than you could review the results.

**Separation of duties has to be rebuilt.** With no second engineer, you are both author and approver. The plan replaces the missing second person in three ways. It separates steps in time with a 24-hour cooling-off before any mainnet step. It adds adversarial agents and deterministic CI gates as second readers. It brings in outside humans at the three costly points named above.

**Scope must match your strongest skills.** Contracts are where a non-specialist carries the most risk that nobody else can catch. The solo phase therefore deploys zero custom contracts to mainnet. EAS allows a schema to be registered without a resolver contract, so attestations can go live from a managed signer while the audited resolver, ERC-8004 validator and TrustGate hook wait for the team phase (Recommendation). The trade-off is a schema version bump later: v1 has no resolver and v2 will have the audited one. Every attestation already carries `modelVersion`, and consumers pin the attester address, so the migration is mechanical.

## 2. Solo scope: what ships now and what waits for the team

| Component | Solo phase (Weeks 1–12) | Deferred to team phase |
|---|---|---|
| Sanctions ingestion (OFAC, UN, EU, UK) | Full, deterministic, daily refresh in CI | — |
| Arabic adapter + benchmark | Baseline, then fine-tuned; you validate every label | — |
| Other languages | Persian stretch in Sprint 6, only with a booked native reviewer | Russian, Korean (Hangugeo), Mandarin |
| `/check/fast`, `/check/deep` + x402 | Sepolia, then capped mainnet payments via the CDP facilitator | Rate tiers, horizontal scaling |
| EAS attestations | Schema v1 with no resolver; attester is a managed signer; Sepolia first, mainnet after checklist | Schema v2 with audited `TouchstoneSchemaResolver` |
| ERC-8004 | Read Identity and Reputation registries | Post validation responses through a validator contract |
| TrustGate hook, spend-policy module | Optional Sepolia prototypes labeled unaudited | Audit, then mainnet |
| Sybil-resistant reputation | Rater clustering + collapse + weighted score, benchmarked against the naive average | Graph models |
| Agent-vs-script classifier | Deferred | Random forest + k-means archetypes |
| Rationales | Templates first, LangChain drafting reviewed by you | — |
| Review console | Minimal Streamlit queue | Full analyst workflow |
| Front end | One static "Agent Trust Explorer" page | OnchainKit seller onboarding |
| TOUCHSTONE MCP server | Yes, as a thin client over `/check/*` | — |
| Performance | Single-instance p95 target | Kubernetes or serverless scaling |

If you fall behind, cut in this order: the explorer page, then fine-tuning (keep the calibrated baseline), then the Persian stretch, then the Sybil scorer (keep only the naive-versus-clustered comparison). Never cut the guards, the sealed evaluation set or the review console. Those three are what make the output trustworthy enough to show a design partner.

## 3. Weekly operating rhythm

Background sessions and scheduled jobs keep working while you are away, so the rhythm alternates setting direction, which needs you, with verifying, which needs you in shorter bursts (Recommendation).

| Block | Time | What you do in Claude Code |
|---|---|---|
| Weekend deep work | 6–8 hours | Plan the sprint in the `lead` session with plan mode, write each stream's `/goal`, start one or two worktree sessions, review workflow results, merge. |
| Weekday evenings | 45–90 minutes, 3–4 times | Open agent view, answer rows marked *Needs input*, review PRs whose checks are green, merge or send back. |
| Unattended | Nightly and on push | CI runs the sanctions refresh, nightly benchmarks (including the sealed split) and the Claude PR review. Background `/goal` loops run only in worktrees whose guards you have tested. |

A Notification hook pushes "a session needs you" to your phone (Section 9). A blocked session therefore waits hours, not days, without you checking the terminal.

## 4. Repo layout and CLAUDE.md

The layout is the team layout, kept on purpose so future hires find their directories already in place. `.claude/` sits at the root so every worktree inherits it. Verified: subdirectory `CLAUDE.md` files load on demand, and CLAUDE.md is "context, not enforced configuration," so rules that must hold go into hooks and permissions (docs/memory).

```text
touchstone/
├── CLAUDE.md  .mcp.json  .worktreeinclude  .gitignore   # ignore .claude/worktrees/, CLAUDE.local.md, .env*
├── .claude/  settings.json  agents/  skills/  workflows/  hooks/  rules/
├── services/api (Flask + x402)  services/ingest  services/mcp
├── ml/matching/core/  ml/matching/languages/{_template, arabic}   # arabic = reference adapter
├── ml/reputation/  ml/eval/sealed/ (CI-only; agents denied)
├── contracts/ (Sepolia prototypes only in the solo phase)
├── console/ (Streamlit)  web/ (static explorer)  infra/  scripts/release-mainnet.sh
└── docs/ (model-card, data-lineage, ship-log, release/, handoff/ROLES.md)
```

```markdown
# CLAUDE.md (root) — TOUCHSTONE
Pre-settlement counterparty-trust & sanctions oracle for AI-agent payments on Base.
We sell screening DECISIONS + EVIDENCE, never legal conclusions.
## Operating model
Solo build: one human reviews everything. Work arrives as PRs from worktree sessions. The Claude review
action and security-auditor are second readers, never approvers. Roles in docs/handoff/ROLES.md are
future teammates; keep code, commits and notes legible to them.
## Solo-phase scope
- NO custom contracts on mainnet. EAS schema v1 has no resolver; the attester is a managed signer.
- The API returns riskTier + evidence. Sanctions hits are REVIEW_REQUIRED; never emit BLOCK.
- Arabic is the only gating language adapter; all others are provisional.
## Architecture
- services/api Flask /check/fast, /check/deep behind x402 (CDP facilitator); responses signed.
- services/ingest Base events + sanctions lists → PostgreSQL + pgvector.
- ml/matching is language-pluggable; see @ml/matching/core/INTERFACE.md
## Commands
- `uv run pytest -q` · `uv run ruff check --fix && uv run ruff format`
- `uv run python -m ml.matching.core.bench --lang <lang> --split dev`
## Non-negotiables (hooks enforce; do not work around)
- Never read or print keys, .env, keystores. Never run anything against Base mainnet (8453).
- Never edit data/sanctions/raw/**. Only salted entity hashes onchain; evidence stays offchain.
- TDD: tests first; never weaken or delete a test to pass. Matcher changes must pass the per-language gate.
- Verify x402/CDP/EAS/ERC-8004 APIs against installed source or spec; never invent names or addresses.
```

## 5. Subagents: a smaller roster with a stronger second reader

The team plan gave each human two or three specialists. Solo, eight subagents cover the work, and three of them exist mainly to disagree with the others. Verified (docs/sub-agents): project subagents live in `.claude/agents/`, and only `name` and `description` are required. Supported fields include `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `isolation: worktree` and `effort`. Since v2.1.198, `/agents` no longer has a creation wizard, so ask Claude to write the files.

| Subagent | Model | Can edit | Role in the solo build |
|---|---|---|---|
| `arabic-name-matcher` (+ `_template-language-matcher`) | Opus | Arabic adapter only | Builds the reference adapter test-first |
| `data-ingestion-engineer` | Sonnet | `services/ingest` (never raw data) | List parsers, Base event ingestion |
| `x402-cdp-integrator` | Sonnet | `services/api`, `services/mcp` | Paywalled endpoints, MCP server |
| `test-writer` | Sonnet | Tests only | The only agent allowed to change committed tests |
| `ml-evaluator` | Sonnet | Nothing | Metrics at fixed FPR, calibration, leakage flags |
| `security-auditor` | Opus | Nothing | Adversarial second reader for API, signing, x402 and any contract |
| `evasion-red-team` | Opus | Provisional fixtures only | Tries to slip Arabic name variants past the matcher |
| `solidity-engineer` (optional, Sprint 6) | Opus | `contracts/` | Sepolia prototypes only, clearly labeled unaudited |

```markdown
<!-- .claude/agents/security-auditor.md -->
---
name: security-auditor
description: Read-only adversarial reviewer and the solo founder's second reader. Use proactively before merging anything touching services/api auth, response signing, x402 settlement, attestation code, services/mcp or contracts/.
tools: Read, Grep, Glob, Bash
disallowedTools: Edit, Write
model: opus
effort: high
maxTurns: 40
---
Assume the author (human or agent) is wrong. Look for: payment-header replay, verify-before-work gaps,
unsigned or mis-signed responses, attestation fields leaking PII or unsalted identifiers, SSRF or injection
through registration metadata, missing rate limits, and any path that could emit BLOCK. For contracts, add
reentrancy, access control and resolver bypass. Output severity, file:line, an exploit sketch and a failing test
to add. Never fix. End with "Merge: yes/no" and your single biggest doubt.
```

```markdown
<!-- .claude/agents/evasion-red-team.md -->
---
name: evasion-red-team
description: Generates adversarial Arabic-script and romanized name variants that a sanctioned party might use to evade matching. Use after each matcher milestone.
tools: Read, Grep, Glob, Write
model: opus
maxTurns: 30
---
Write only to ml/matching/languages/arabic/fixtures/provisional/. For each sanctioned-name sample, produce
variants that stay plausible to a human reader: dropped nasab links, kunya-only forms, swapped
article spellings, Arabizi, mixed scripts, homoglyphs, inserted tatweel and diacritics. Tag every row
`# provisional — needs founder validation`. The harness ignores provisional rows until validated.
```

The Arabic specialist keeps the team plan's full list of phenomena (Section 11). Its frontmatter carries `isolation: worktree`, `memory: project`, `maxTurns: 60`, the `add-language-adapter` and `run-language-benchmark` skills, and a PostToolUse hook that runs the Arabic fast tests after every edit. Verified caveat: `isolation: worktree` branches from the default branch, not your current HEAD (docs/worktrees), so merge the base work you need first.

## 6. Parallel work for one person

**Worktrees are how one person gets parallel streams without collisions.** Run `claude --worktree matcher --name matcher` and `claude --worktree api --name api`. Each gets `.claude/worktrees/<name>/` on branch `worktree-<name>`, and `.worktreeinclude` copies Sepolia-only env files in. Verified: hook scripts must read the input's `cwd` rather than `${CLAUDE_PROJECT_DIR}`, which stays at the main checkout, and worktrees created by `-p` runs are not cleaned up automatically (docs/worktrees).

**Agent view is your cockpit.** A solo founder mostly waits on agents, so `claude agents` (research preview) becomes the main screen. You dispatch a background task, move on, and return when a row shows *Needs input* or its PR label turns green. Dispatched sessions move into their own worktree before editing, and `--json` exposes state to scripts (docs/agent-view). Fallback: tmux plus `/tasks`.

**Cross-session messaging keeps the two worktrees consistent.** When the `api` session changes the attestation payload, it can `SendMessage` the `ingest` session. You can also ask to be notified when `matcher` goes idle. Verified: this needs v2.1.224+ on macOS/Linux (v2.1.234+ on Windows), messages are plain text, and the receiving session's permissions still apply (docs/cross-session-messaging).

**Dynamic workflows are your second reviewer at scale.** Workflows run in the background and can check one agent's work with another, which gives a solo builder a review step that does not depend on anyone else's time. Verified (docs/workflows): trigger with `ultracode` or "use a workflow," watch in `/workflows`, save with `s` into `.claude/workflows/` as `/<name>`. Paid plan required; Pro enables them in `/config`. Save three:

```text
ultracode: for PR <n>, spawn two independent reviewers (security-auditor lens and correctness lens) that
must each cite file:line evidence; a third agent keeps only findings both can reproduce with a failing test.
                                                                  → save as /pr-second-opinion
use a workflow to run the Arabic dev benchmark, compare against baseline.json, and bisect the last 10
commits for any regression.                                       → save as /matcher-regression-sweep
use a workflow to take today's sanctions diff, re-screen affected entities, and draft a triage note that
separates new exposures, removals and name changes.               → save as /rescreen-triage
```

**`/goal` lets work continue while you are at your day job.** Verified (docs/goal): after each turn, a small fast model checks the condition against what the transcript shows. Conditions can run up to 4,000 characters, `/goal clear` cancels, it works with `claude -p`, and unattended runs need auto mode. Always include the command that proves the condition and a turn cap, so a stuck loop ends instead of burning your quota:

```text
/goal `uv run pytest ml/matching -q` exits 0 AND the arabic dev bench prints recall@FPR1% >= 0.90 and
ECE <= 0.05, no test or fixture file was deleted, git status shows only ml/matching changes — or stop after 25 turns.
```

**Keep agent teams off.** They look like a way to simulate a team, which is why they are tempting solo, but three verified facts argue against them (docs/agent-teams). Teammates are not isolated in worktrees. A teammate's plan is auto-approved "without the lead reviewing it." And teams use significantly more tokens. With no second human to catch what slips through, those properties are worse solo than in a team, so `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` stays `0`.

## 7. MCP servers

Verified (docs/mcp): remote servers use `claude mcp add --transport http <name> <url>`, and stdio servers use `claude mcp add <name> -- <cmd>`. Scope is set with `--scope local|project|user`. Project scope is committed in `.mcp.json` and needs approval on first run. Some credential variables in remote `url`/`headers` read as empty, so credentialed servers go in user scope. Solo, you are the only person approving project servers, but committing `.mcp.json` now means your first hire gets the same tools the day they join.

| Server | Scope | Solo use | Install |
|---|---|---|---|
| Claude Code docs | project | Exact syntax lookups | `claude mcp add --scope project --transport http claude-code-docs https://code.claude.com/docs/mcp` |
| GitHub | user | PRs, issues, CI | `claude mcp add -s user --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $GITHUB_PAT"` |
| PostgreSQL (DBHub) | project | Read-only entity-graph queries | `claude mcp add --transport stdio touchstone-db -- npx -y @bytebase/dbhub --dsn "$TOUCHSTONE_RO_DSN"` |
| x402 buyer (CDP guide) | local | A test agent that pays your Sepolia endpoints | Build per CDP "MCP Server with x402" guide |
| TOUCHSTONE dev | project | The product's own MCP server under test | `.mcp.json` below |
| Playwright | project, optional | Smoke-test the explorer page | `claude mcp add playwright -- npx -y @playwright/mcp@latest` |

```json
{
  "mcpServers": {
    "claude-code-docs": { "type": "http", "url": "https://code.claude.com/docs/mcp" },
    "touchstone-db": { "type": "stdio", "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "${TOUCHSTONE_RO_DSN}"] },
    "touchstone-dev": { "type": "stdio", "command": "uv",
      "args": ["run", "python", "-m", "services.mcp.server"],
      "env": { "TOUCHSTONE_API_URL": "http://localhost:5000", "X402_NETWORK": "eip155:84532" } }
  }
}
```

Build TOUCHSTONE's own MCP server with the documented scaffold: `/plugin install mcp-server-dev@claude-plugins-official`, then `/mcp-server-dev:build-mcp-server` (docs/mcp). Keep it to four tools (`check_fast`, `check_deep`, `get_attestation`, `explain_decision`) implemented as thin clients over `/check/*`. Pricing and verification then live in one place, and tool descriptions stay small in every agent's context.

## 8. Skills

Verified (docs/skills): skills live at `.claude/skills/<name>/SKILL.md` and run as `/<name>`, or automatically when their description matches. `` !`cmd` `` injects live output, and arguments arrive via `$ARGUMENTS` and `$0`. Commit every skill, because cloud routines do not read `~/.claude/skills/`. Solo, skills also serve as your written procedures: a teammate who later reads them learns how the system is operated.

| Skill | Invocation | What it codifies |
|---|---|---|
| `add-language-adapter` | you, per language | Replicates the Arabic adapter pattern |
| `run-language-benchmark` | forked, as `ml-evaluator` | Dev run, baseline comparison, report |
| `sanctions-ingest` / `sanctions-refresh` | auto / human-only | Parsers for each list's native-script fields; fetch, diff, re-screen queue |
| `x402-endpoint` | auto on `services/api/**` | Flask x402 middleware against the CDP facilitator on `eip155:84532` |
| `eas-attest` | auto on `services/api/**` | Schema v1 (no resolver), payload building, managed-signer calls |
| `model-card`, `ship-log` | you + scheduled | Model card and lineage from benchmark manifests; weekly log |
| `handoff-brief` | you, before each hire | Generates `docs/handoff/<role>.md` from the repo, agents and skills |

```markdown
<!-- .claude/skills/eas-attest/SKILL.md -->
---
name: eas-attest
description: Work with TOUCHSTONE's EAS schema v1 (no resolver) and build attestation payloads signed by the managed signer. Use for attestation code and Sepolia tests in services/api.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(uv run pytest *)
paths:
  - "services/api/**"
---
Schema v1: bytes32 agentId, bytes32 operatorEntityHash, uint8 riskTier, bool sanctionsHit, uint16 score,
bytes32 modelVersion, uint64 expiry. Resolver: none. Revocable: true, so errors can be corrected.
EAS addresses come from deployments/eas.json with a source URL; never hardcode or guess them.
Automated attestations set riskTier and score only. sanctionsHit=true is written only after the founder's
review in console/. Schema registration and every mainnet call are human-only: print the exact command, then stop.
```

The `add-language-adapter` skill carries over from the team plan unchanged. It copies `_template` to `languages/$0`, lists every phenomenon in `ADAPTER.md` with one fixture and one test each, builds a provenance-tagged dev set from public list aliases, and opens a PR with the reviewer checklist. Skills that combine `disable-model-invocation` with `context: fork` set `background: false`, because GitHub issue #84217 reports lost arguments in that combination.

## 9. Hooks: the guards that replace a second engineer

Verified (docs/hooks-guide): on PreToolUse, exit code 2 blocks the call and sends stderr back to Claude. Stop and SubagentStop can return `{"decision":"block","reason":…}`. Notification matchers include `permission_prompt` and `agent_needs_input`. Solo, hooks carry more weight than in a team, because often nobody else is watching when a session runs.

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/guard-bash.sh" }] },
      { "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/guard-writes.sh" }] }
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh" }] }
    ],
    "Stop": [ { "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/bench-gate.sh" }] } ],
    "SubagentStop": [ { "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/bench-gate.sh" }] } ],
    "SessionStart": [ { "matcher": "compact", "hooks": [{ "type": "command", "command": "cat \"$CLAUDE_PROJECT_DIR\"/docs/sprint/CURRENT.md" }] } ],
    "Notification": [ { "matcher": "permission_prompt|agent_needs_input", "hooks": [{ "type": "command", "command": "curl -s -d 'TOUCHSTONE: a session needs you' \"https://ntfy.sh/$TOUCHSTONE_PUSH_TOPIC\" >/dev/null" }] } ]
  }
}
```

```bash
#!/bin/bash
# .claude/hooks/guard-bash.sh — PreToolUse(Bash). False positives are acceptable; misses are not.
CMD=$(jq -r '.tool_input.command // empty')
deny(){ echo "Blocked by TOUCHSTONE policy: $1" >&2; exit 2; }
echo "$CMD" | grep -Eqi '(8453|base-mainnet|--network[ =]+mainnet)' && deny "mainnet operations are human-only in the solo phase."
echo "$CMD" | grep -Eq -- '--broadcast' && deny "every broadcast is human-only in the solo phase."
echo "$CMD" | grep -Eq '^\s*cast (send|wallet)' && deny "cast send/wallet is human-only."
echo "$CMD" | grep -Eq '(cat|less|head|tail|printenv|env)\b.*(\.env|keystore|PRIVATE_KEY|CDP_API_KEY)' && deny "secret access."
echo "$CMD" | grep -q 'ml/eval/sealed' && deny "sealed evaluation data is CI-only."
echo "$CMD" | grep -q 'release-mainnet' && deny "the release script is run by the founder only."
exit 0
```

```bash
#!/bin/bash
# .claude/hooks/bench-gate.sh — Stop/SubagentStop per-language regression gate (worktree-aware)
IN=$(cat); [[ $(echo "$IN" | jq -r '.stop_hook_active') == "true" ]] && exit 0
cd "$(echo "$IN" | jq -r .cwd)" || exit 0
CHANGED=$(git diff --name-only origin/main...HEAD; git diff --name-only)
LANGS=$(echo "$CHANGED" | grep -oE 'ml/matching/languages/[a-z]+' | sort -u | awk -F/ '{print $4}')
echo "$CHANGED" | grep -q 'ml/matching/core/' && LANGS=$(ls ml/matching/languages | grep -v '^_')
for L in $LANGS; do
  uv run python -m ml.matching.core.bench --lang "$L" --split dev --gate || {
    jq -n --arg r "Benchmark gate failed for $L. Fix the regression; do not edit baseline.json or fixtures." \
      '{decision:"block", reason:$r}'; exit 0; }
done
exit 0
```

`guard-writes.sh` blocks edits to `data/sanctions/raw/**` and `ml/eval/sealed/**`, and any content that looks like a private key or PEM block. It also enforces the test lock: committed tests are editable only when the hook input's `agent_type` is `test-writer`. Probe that field in Week 0, because it is documented only for events inside subagents. The `--gate` tolerance (recall at 1% FPR may drop no more than 0.5 points, ECE may rise no more than 0.01) is a Recommendation. Only you, through a PR labeled `baseline-update`, change `baseline.json`.

## 10. Automation: CI, schedules and channels

Verified (docs/scheduled-tasks): `/loop` and the cron tools are session-scoped. They fire only when the session is idle, recurring tasks expire after seven days, and a session holds at most 50. Cloud routines survive a closed laptop but start from a fresh clone and run at most hourly. Compliance-critical jobs therefore run as deterministic code in GitHub Actions, and Claude only writes the triage notes (Recommendation).

| Job | Mechanism | Cadence | Where you see it |
|---|---|---|---|
| Sanctions fetch + diff (OFAC, UN, EU, UK) | Actions cron, no LLM | Daily | PR labeled `needs-compliance-review` |
| Re-screen triage note | `claude --bare -p "/rescreen-triage"` | Daily after diff | Same PR |
| Dev + sealed benchmarks | Actions | Nightly | Aggregate-only report on the PR |
| PR review (second reader) | `anthropics/claude-code-action@v1` | Every PR, even your own | PR comments |
| Weekly ship log | Routine via `/schedule` (preview); fallback Actions | Weekly | `docs/ship-log/` |
| CI babysitting | `/loop 15m check CI on my PR and fix failures` | Ad hoc | Session |

```yaml
# .github/workflows/sanctions-refresh.yml (excerpt)
on: { schedule: [{ cron: "17 5 * * *" }], workflow_dispatch: {} }
jobs:
  refresh:
    runs-on: ubuntu-latest
    permissions: { contents: write, pull-requests: write }
    steps:
      - uses: actions/checkout@v4
      - run: uv run python -m services.ingest.sanctions fetch --all && uv run python -m services.ingest.sanctions diff --since last
      - run: |
          claude --bare -p "/rescreen-triage" --settings .claude/ci-settings.json \
            --allowedTools "Read,Grep,Glob,Bash(uv run python -m services.ingest.*),Workflow(rescreen-triage)" \
            --output-format json > triage.json && jq '.total_cost_usd' triage.json
        env: { ANTHROPIC_API_KEY: "${{ secrets.ANTHROPIC_API_KEY }}" }
      - run: gh pr create --title "sanctions: daily diff" --body-file docs/sanctions/latest-triage.md --label needs-compliance-review
```

Verified (docs/headless): `--bare` skips project hooks, skills, MCP and CLAUDE.md and needs `ANTHROPIC_API_KEY`. Without it, a `-p` run in an untrusted checkout would still run the project's hooks and `.mcp.json` servers. CI therefore always uses `--bare` with an explicit `--settings`. `--output-format json` reports `total_cost_usd`, which feeds your weekly cost line.

**Channels are the away-from-desk inbox.** Verified (docs/channels): channels are a research preview. Telegram, Discord, iMessage and fakechat plugins push events into a running session, for example `claude --channels plugin:discord@claude-plugins-official`. Senders are allowlisted by pairing, and claude.ai or Console authentication is required. Solo, a persistent `ops` session on Telegram or Discord receives design-partner messages and CI alerts, so you can triage from your phone. The Notification hook above is the non-preview fallback for "a session needs you," and a labeled GitHub issue is the fallback for everything else.

## 11. Arabic as the reference adapter, and how it scales

Every language implements one interface, so the scorer, calibrator, benchmark harness and API never change when a language is added (Recommendation):

```python
class LanguageAdapter(Protocol):
    code: str                     # "ar", "fa", "ru", "ko", "zh"
    scripts: set[str]             # ISO 15924: {"Arab"}, {"Cyrl"}, {"Hang","Hani"}, {"Hans","Hant"}
    def detect(self, text: str) -> ScriptSpan: ...
    def normalize(self, text: str) -> NormalizedName: ...         # native-script key
    def romanize_variants(self, n: NormalizedName, k: int = 64) -> list[Variant]: ...
    def parse(self, n: NormalizedName) -> NameStructure: ...        # roles: given, nasab, kunya, family
    def blocking_keys(self, n: NormalizedName) -> list[str]: ...
```

**Arabic comes first because it is the one language whose labels you can judge yourself.** It is therefore the only fully human-validated benchmark in the solo phase, and it sets the quality bar for every language after it. The deterministic layer handles romanization families (Muhammad/Mohammed/Mohamed/Mohamad), articles (al-/el-/ul-/ad-/ash-) with sun-letter assimilation, Abd al- compounds, nasab chains (bin/ibn/bint/ould), kunya (Abu/Umm), laqab and nisba, missing short vowels, hamza and alef forms, ta marbuta, alif maqsura, tashkeel, tatweel, Arabizi, and name-order variation. The parser assigns roles, so "Abu Bakr al-Baghdadi" and a full nasab form align by role rather than by position.

Match native script to native script when both the sanctions list and the onchain metadata carry it, and fall back to romanized variants otherwise. The lists publish native script in four different formats: OFAC's advanced XML with a `ScriptID`, the UN list's "Name (original script)," the EU list's `nameLanguage` tag, and the UK list's non-Latin-script fields. Per-list parsers belong in `sanctions-ingest`.

**One solo-specific guard protects the benchmark from you.** You write the sealed labels, so you could tune toward them without noticing. Freeze the sealed set before any tuning. CI reports only aggregate sealed metrics, never per-item failures, so you can see *that* something regressed without learning *which* names to fix.

| Order / timing | Language | Adds beyond Arabic | Validation before it can gate |
|---|---|---|---|
| 1 — Sprint 6 stretch, only with a booked reviewer | Persian | پ چ ژ گ; Persian yeh U+06CC and kaf U+06A9 folded with the Arabic forms; ezafe; Persian vowel realization; -zadeh and -i suffixes; OFAC may label Persian names "Arabic:", so detect language as well as script | Paid native Persian reviewer |
| 2 — team phase | Russian | GOST vs BGN/PCGN vs ICAO passport transliteration; patronymics; gendered surname endings | Russian linguist |
| 3 — team phase | Korean (Hangugeo) | Revised Romanization vs McCune-Reischauer vs personal spellings (이 = Lee/Yi/Rhee/Ri; 박 = Park/Pak/Bak); DPRK conventions; hanja links | Korean linguist with DPRK naming experience |
| 4 — team phase | Mandarin (+ Cantonese) | Pinyin vs Wade-Giles vs Hong Kong spellings; simplified/traditional folding; tone-loss collisions; company names translated by meaning | Mandarin and Cantonese reviewers |

Each new language starts with `/add-language-adapter <lang> <script>` in its own worktree, gets its own specialist subagent copied from the template, and reports metrics without gating until its reviewer signs off. Otherwise the gate would enforce Claude's own guesses.

## 12. Sprint-by-sprint solo execution

| Sprint | Deliverable | Claude Code in use | Your checkpoints |
|---|---|---|---|
| Wk 1–2 | 8–10 interviews and a validation memo, risk register, architecture note, repo, CI, all `.claude` config | Plan mode, `/init`, CLAUDE.md, docs + GitHub MCP, review action, guards | Probe every guard with a command it should block; memo sign-off |
| Wk 3–4 | Four-list sanctions ingestion; **Arabic adapter v0**; benchmark harness; sealed set v0 | Worktrees `ingest` + `matcher`; `data-ingestion-engineer`, `arabic-name-matcher`, `test-writer`, `ml-evaluator`; `/goal`; daily refresh + nightly eval | You validate Arabic fixtures; you freeze sealed v0 |
| Wk 5–6 | `/check/*` with x402 on Sepolia; EAS schema v1 on Sepolia; attestations from the managed signer; ERC-8004 reads; dev MCP server | Worktrees `api` + `ingest`; `x402-cdp-integrator`, `security-auditor`; `x402-endpoint`, `eas-attest`; cross-session messaging | You register the Sepolia schema; a test agent pays $0.001 and receives a signed decision and attestation UID |
| Wk 7–8 | Fine-tuned Arabic matcher with calibration; Sybil scorer v1 against the naive average; public benchmark v1 | `/matcher-regression-sweep`, `evasion-red-team`, metric `/goal`s, private benchmark artifact | Leakage review of any gain over 5 points; you validate red-team fixtures; publication sign-off |
| Wk 9–10 | Rationales, Streamlit review queue, static explorer, hardened MCP server, 1–2 design partners on Sepolia | `/pr-second-opinion`, Playwright smoke, channels or push alerts | You confirm every REVIEW_REQUIRED decision; rationale-language review |
| Wk 11–12 | Capped mainnet payments + schema v1 attestations; monitoring; p95 target; ship log; handoff package; stretch: Persian or Sepolia contract prototypes | p95 `/goal`, routines, `handoff-brief`, public artifact | Release checklist, then 24-hour cooling-off, then you run the mainnet steps and set caps |

**Week-0 checklist.** Complete these in order:

1. Install the current Claude Code, run `/login` and confirm your plan tier. Workflows need a paid plan (Pro enables them in `/config`), artifacts need Pro or higher, and channels need claude.ai authentication.
2. Create the repo and commit `CLAUDE.md`, `.claude/settings.json`, the rules files and `.gitignore`.
3. Run `chmod +x .claude/hooks/*.sh`, check the hooks with `/hooks`, probe `agent_type`, and try one blocked command per guard.
4. Add the docs MCP at project scope, GitHub at user scope and DBHub with a read-only role, then approve the project servers.
5. Have Claude write the subagents and check them in `/agents`.
6. Author the first four skills and confirm them in `/skills`.
7. Run `/install-github-app`, add `ANTHROPIC_API_KEY` as a secret, set a spend limit on that key's workspace in the Anthropic Console, and commit the workflows and `ci-settings.json`.
8. Create the CDP project and a Sepolia server wallet, and generate a receive-only `payTo` address from a hardware wallet for mainnet revenue.
9. Set `TOUCHSTONE_PUSH_TOPIC` and test the phone notification.
10. Seed `ml/eval/sealed/` from pairs you validated, and confirm that agents are denied read access.

## 13. Governance without a second human

**Separation in time.** Mainnet steps run only through `scripts/release-mainnet.sh`, which you execute yourself and which the Bash guard blocks for Claude. It refuses to proceed until the release checklist has been committed for 24 hours with no unchecked items. That gives you the second look a teammate would have given you, delayed a day (Recommendation):

```bash
#!/bin/bash
# scripts/release-mainnet.sh — founder only; Claude is denied by guard-bash.sh
set -euo pipefail
CL="docs/release/CHECKLIST-$1.md"
[[ -f "$CL" ]] || { echo "missing $CL"; exit 1; }
AGE=$(( $(date +%s) - $(git log -1 --format=%ct -- "$CL") ))
(( AGE >= 86400 )) || { echo "cooling-off: checklist committed $((AGE/3600))h ago; wait 24h"; exit 1; }
grep -q '^- \[ \]' "$CL" && { echo "unchecked checklist items remain"; exit 1; }
echo "Proceed: run the mainnet steps listed in $CL yourself."
```

**Separation in agents, backed by tests.** Every change arrives as a PR, so the review action, the `security-auditor` and `/pr-second-opinion` all read it. They can share blind spots with the agent that wrote the code, so deterministic tests, the sealed evaluation and the per-language gate remain the real safety net.

**Separation by product design.** In the solo phase the API returns a risk tier, evidence and `REVIEW_REQUIRED`, never an automatic block, and the customer decides what to do. `sanctionsHit=true` attestations are written only after you review the case. Before the first public true-positive claim, a sanctions-compliance advisor reviews it too.

**Keys.** Mainnet revenue lands at a receive-only address from a hardware wallet. The attester and response signer are managed signers (a CDP server wallet if it supports the signing you need, otherwise a cloud KMS). No private key ever sits in a file an agent could read.

```json
{
  "permissions": {
    "defaultMode": "default",
    "disableBypassPermissionsMode": "disable",
    "allow": ["Bash(uv run pytest *)", "Bash(uv run ruff *)", "Bash(uv run python -m ml.matching.core.bench *)",
              "Bash(forge build *)", "Bash(forge test *)", "Bash(forge fmt *)", "Bash(git status)", "Bash(git diff *)"],
    "ask": ["Bash(git push *)", "Bash(gh pr merge *)", "Bash(forge script *)", "Bash(aws *)", "Workflow"],
    "deny": ["Read(./.env)", "Read(./.env.*)", "Read(~/.foundry/keystores/**)", "Read(./ml/eval/sealed/**)",
             "Edit(./data/sanctions/raw/**)", "Write(./data/sanctions/raw/**)",
             "Bash(cast send *)", "Bash(cast wallet *)", "Bash(./scripts/release-mainnet.sh *)"]
  },
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "0" },
  "worktree": { "baseRef": "fresh" }
}
```

**Cost.** One plan's quota covers every interactive session, so use Sonnet by default and reserve Opus for the matcher, the security auditor and the red team. Put `maxTurns` on every subagent and a turn clause in every `/goal`. CI runs bill against the API key separately. Log `total_cost_usd` weekly next to the ship log, and treat the Console spend limit as a hard ceiling.

**Failure modes to watch hardest solo.** The first is hallucinated APIs for young standards (x402, CDP, EAS, ERC-8004), contained by the verify-against-source rule, the docs MCP and addresses read from `deployments/*.json`. The second is test gaming, contained by the test lock and the sealed split. The third is quiet drift between your two worktrees, contained by `baseRef: fresh`, daily rebases and cross-session schema messages. The fourth is your own overfitting to labels you wrote, contained by the frozen, aggregate-only sealed set.

## 14. From solo repo to team: the handoff

The solo phase deliberately skipped the contracts, which are the riskiest work and furthest from your strengths. That makes the smart-contract engineer the first hire. Each hire inherits a seat that already exists in the repo (Recommendation):

| Hire order | Role | Inherits | First assignment |
|---|---|---|---|
| 1 | Smart-contract engineer | `solidity-engineer`, `security-auditor`, `contracts/` prototypes, worktree `contracts` | Schema v2 with the audited resolver, ERC-8004 validator, TrustGate; audit preparation |
| 2 | Backend/cloud engineer | `x402-cdp-integrator`, `data-ingestion-engineer`, worktrees `api` and `ingest` | Rate tiers, scaling, SLOs, infrastructure |
| 3 | Front-end/DX engineer | A new `frontend-dx` subagent, the static explorer | OnchainKit seller onboarding and explorer |
| 4 | Data engineer/evaluator | `test-writer`, `ml-evaluator`, language template | Russian, Korean and Mandarin adapters with linguists; agent-vs-script classifier |

Before each hire, run `/handoff-brief <role>` to generate their onboarding page. On day one they clone the repo, trust the workspace, approve the project MCP servers, add GitHub at user scope, and take their first task from agent view. The team build plan then applies as written, and you move into the product and ML/risk lead seat it describes.

## 15. Preview and plan-limited features, with fallbacks

| Feature | Status and limits (verified) | Solo fallback |
|---|---|---|
| Agent view | Research preview; shares your quota across sessions | tmux + `/tasks` + `--worktree` |
| Channels | Research preview; claude.ai or Console authentication | Notification hook push + labeled GitHub issues |
| Routines | Research preview; hourly minimum; fresh clone | Actions cron + `claude --bare -p` |
| Dynamic workflows | Paid plans; Pro enables in `/config`; keyword ignored from `-p` | A fan-out skill or `/batch` |
| Artifacts | Pro and above; Pro and Max share by public link only; auto mode may publish without prompting | Keep dashboards unshared; publish reviewed, aggregate-only snapshots from a default-mode session |
| Agent teams | Experimental; no worktree isolation; plans auto-approved | Kept off: subagents + worktrees + workflows |
| Cross-session messaging | v2.1.224+ (macOS/Linux), v2.1.234+ (Windows) | Handoff notes in `docs/sprint/CURRENT.md` |

Artifacts double as recruiting material in the solo phase. A public, aggregate-only benchmark summary and a demo explainer show prospective teammates and design partners the work without exposing sanctions data.

## Caveats

The 12-week calendar assumes roughly 15–20 focused hours a week. At fewer hours, stretch the sprints rather than cut the guards. Young third-party details change quickly: ERC-8004 registry addresses, the Validation Registry's revisions, x402 package names and EAS predeploy addresses should be re-verified at each sprint boundary and read from `deployments/*.json`, never from memory. Moving from schema v1 to v2 creates a new schema UID, so plan the consumer migration in the team phase. If you intend this repo to become your MSAIE capstone project, check the program's rules on work started before the capstone, since the capstone is defined as a team build. Every rationale TOUCHSTONE produces is a screening explanation, not a legal determination.

## Sources

Claude Code documentation: https://code.claude.com/docs/en/agents · https://code.claude.com/docs/en/sub-agents · https://code.claude.com/docs/en/agent-view · https://code.claude.com/docs/en/agent-teams · https://code.claude.com/docs/en/cross-session-messaging · https://code.claude.com/docs/en/workflows · https://code.claude.com/docs/en/worktrees · https://code.claude.com/docs/en/mcp-quickstart · https://code.claude.com/docs/en/mcp · https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/artifacts · https://code.claude.com/docs/en/hooks-guide · https://code.claude.com/docs/en/channels · https://code.claude.com/docs/en/scheduled-tasks · https://code.claude.com/docs/en/goal · https://code.claude.com/docs/en/headless · https://code.claude.com/docs/en/memory · https://code.claude.com/docs/en/routines

Other: Claude Code GitHub Action, https://github.com/anthropics/claude-code-action · Skill argument issue #84217, https://github.com/anthropics/claude-code/issues/84217 · CDP "MCP Server with x402," https://docs.cdp.coinbase.com/x402/mcp-server · x402 Flask example, https://github.com/x402-foundation/x402/tree/main/examples/python/servers/flask · ERC-8004 contracts, https://github.com/erc-8004/erc-8004-contracts · GitHub MCP install guide, https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md · OFAC Sanctions List Service, https://ofac.treasury.gov/sanctions-list-service · UN Security Council Consolidated List, https://main.un.org/securitycouncil/en/content/un-sc-consolidated-list · UK Sanctions List format guide, https://www.gov.uk/guidance/format-guide-for-the-uk-sanctions-list
