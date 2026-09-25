---
chapter: 12
title: "Sprint 3: A paid, signed decision"
part: III. Building Touchstone
status: outline
durability: durable
written: after Sprint 3 ships
curriculum: [Back Ends, Microservices I, Decentralized Applications]
---

# 12. Sprint 3: A paid, signed decision

A planned outline from the [solo build plan](../../docs/plan/solo-build-plan.md), Section 12, Weeks 5–6.
It gets rewritten once the sprint ships.

**By the end, the reader can:**
- explain how `/check/fast` and `/check/deep` are paywalled with x402 on Base Sepolia
- explain why responses are signed even over HTTPS
- explain how an attestation is issued, and why the founder registers the schema by hand
- follow the sprint's demo from payment to attestation

## Planned outline

1. **Two endpoints.** A fast cached read and a deep check, and what each returns.
2. **The paywall.** x402 middleware and the CDP facilitator on Base Sepolia; verify before doing any work.
3. **Signing decisions.** What a signature adds over HTTPS: proof that can be shown to someone else later.
4. **Attestations from a managed signer.** EAS schema v1 on Sepolia, registered by the founder;
   attestations issued by the service.
5. **Reading ERC-8004.** The identity and reputation registries as inputs.
6. **A first MCP server.** A thin client over `/check/*`.
7. **The second reader.** What the `security-auditor` subagent found, and what changed because of it.
8. **The demo.** A test agent pays $0.001 and receives a signed decision and an attestation UID.

## In Touchstone

- `services/api/`, `services/mcp/` (planned); the `x402-endpoint` and `eas-attest` skills (planned)

## Anticipated quiz

1. What does "verify before work" prevent?
2. How could a payment header be replayed, and what stops it?
3. Why sign responses when the connection already uses HTTPS?
4. Why does the founder, and not Claude, register the schema?
