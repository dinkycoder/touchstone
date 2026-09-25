---
chapter: 7
title: Identity, reputation and attestations onchain
part: II. Foundations
status: outline
durability: durable (ERC-8004 details re-checked against the current draft)
written: before Sprint 3
curriculum: [Decentralized Applications, AI Agents]
---

# 7. Identity, reputation and attestations onchain

**By the end, the reader can:**
- explain what an attestation is, and how the Ethereum Attestation Service (EAS) stores one
- describe ERC-8004's three registries for agents
- explain a Sybil attack on a reputation system, and why a naive average falls for it
- explain why Touchstone puts only a salted entity hash onchain

## Outline

1. **Saying something about someone, onchain.** Attestations versus transactions; schemas; revocation.
2. **EAS.** The schema registry, attestations, optional resolver contracts. Touchstone's schema v1:
   `agentId`, `operatorEntityHash`, `riskTier`, `sanctionsHit`, `score`, `modelVersion`, `expiry`. Why v1
   has no resolver in the solo phase, and why it's revocable.
3. **Agent identity: ERC-8004.** The identity, reputation and validation registries; agent registration
   files.
4. **Names and verifications.** Basenames; Coinbase Verifications as a positive signal that a human
   principal passed a check.
5. **Reputation and Sybil attacks.** Fake raters, naive averages, and clustering raters into single
   entities before weighting their feedback.
6. **Privacy.** Evidence stays offchain. What a salted hash hides, and what an unsalted hash of a name
   would leak to anyone with a list of names.

## In Touchstone

- The `eas-attest` skill (planned; [plan](../../docs/plan/solo-build-plan.md) Section 8)
- `ml/reputation/` (planned, Sprint 4)

## Research

- [Evidence log](../research/evidence-log.md) H1 (do registrations name an operator?) and H7 (Sybil-prone
  reputation)

## Quiz

1. What's the difference between an attestation and a payment transaction?
2. What is each of ERC-8004's three registries for?
3. How does a Sybil attack beat a naive average, and what does clustering change?
4. Why is `operatorEntityHash` salted? What would an unsalted hash leak?
5. Why is Touchstone's schema revocable?

## Sources to check

- EAS documentation and contracts (schema registry, resolvers, revocation)
- ERC-8004: <https://eips.ethereum.org/EIPS/eip-8004> (check the current draft status)
- Basenames documentation; the Coinbase Verifications schema
