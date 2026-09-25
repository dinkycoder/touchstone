---
chapter: 5
title: Stablecoins and onchain money
part: II. Foundations
status: outline
durability: durable (the regulatory section is re-checked each release)
written: before Sprint 3
curriculum: [Decentralized Finance]
---

# 5. Stablecoins and onchain money

**By the end, the reader can:**
- explain how a fiat-backed stablecoin keeps its value
- explain ERC-20 tokens, and what EIP-3009 adds for payments
- explain what powers a stablecoin issuer holds, and what that means for sanctions
- sketch the main kinds of DeFi protocol and where counterparty risk appears in each

## Outline

1. **Money that doesn't move in price.** Why volatility rules out payments; fiat-backed stablecoins;
   reserves and redemption.
2. **Tokens are contracts.** ERC-20 balances, transfers and approvals.
3. **Paying without holding gas: EIP-3009.** Signed transfer authorizations, and why x402 builds on them
   (check against the current x402 payment scheme when drafting).
4. **Issuer powers.** An issuer like Circle can block addresses in the USDC contract. What that means:
   the issuer is part of the screening chain too.
5. **Primary versus secondary markets.** Minting and redemption with the issuer, versus transfers
   between third parties. Why regulators now care about the second (Chapter 17).
6. **A short map of DeFi.** Exchanges (automated market makers), lending, and where counterparty risk
   sits in each. Touchstone's phase-two credit product lives here (Chapter 18).

## In Touchstone

- USDC settlement for every paid check (Chapter 6)

## Research

- [Evidence log](../research/evidence-log.md) H3 (secondary-market screening obligations)

## Quiz

1. What does EIP-3009 let a payer do that a plain ERC-20 transfer doesn't?
2. Who can freeze USDC at an address, and what does that imply for sanctions?
3. What's the difference between the primary and secondary market for a stablecoin?
4. Why are stablecoins, rather than ETH, the natural currency for agent payments?
5. Where does counterparty risk show up in a lending protocol?

## Sources to check

- ERC-20: <https://eips.ethereum.org/EIPS/eip-20>
- EIP-3009: <https://eips.ethereum.org/EIPS/eip-3009>
- Circle's USDC documentation and the USDC contract's blocking functions
- The GENIUS Act text (congress.gov)
