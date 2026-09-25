---
chapter: 4
title: Ethereum, smart contracts and Base
part: II. Foundations
status: outline
durability: durable (Base's governance details get re-checked each release)
written: before Sprint 3
curriculum: [Decentralized Applications, Blockchains in Practice]
---

# 4. Ethereum, smart contracts and Base

**By the end, the reader can:**
- explain what a smart contract is, and the difference between reading one and sending it a transaction
- explain what a rollup is and what kind of network Base is
- tell mainnet from testnet by chain ID, and explain why that distinction is a safety rule in this repo

## Outline

1. **From ledger to computer.** The Ethereum Virtual Machine; contracts as programs with their own
   storage.
2. **Talking to contracts.** Free reads versus paid transactions; ABIs; event logs, and why indexers
   build everything from them.
3. **Gas.** Why computation costs money, and who pays.
4. **Scaling with rollups.** Run transactions off Ethereum, post the data back to Ethereum. Optimistic
   rollups and the OP Stack. Base as an OP Stack network operated by Coinbase (check its current
   decentralization stage when drafting).
5. **Mainnet versus testnet.** Base is chain ID 8453 and Base Sepolia is 84532. Why the guard blocks one
   and allows the other, and the bug where `8453` also matched `84532` (see Chapter 10).
6. **Standards.** How an EIP becomes an ERC, and why shared standards are the real infrastructure.
7. **Why no custom contracts on mainnet in the solo phase.** Unaudited code, real money, and no second
   engineer to catch mistakes.

## In Touchstone

- The chain-ID rule in [.claude/hooks/guard.py](../../.claude/hooks/guard.py)
- `contracts/` stays on Sepolia during the solo phase ([plan](../../docs/plan/solo-build-plan.md)
  Section 2)

## Quiz

1. What's the difference between Base and Base Sepolia, and how does a program tell them apart?
2. What does a rollup post to Ethereum, and why?
3. What is an event log, and why do indexers depend on them?
4. Why is reading a contract free when writing to it costs gas?
5. Why does the solo phase deploy no custom contracts to mainnet?

## Sources to check

- ethereum.org documentation (EVM, gas, smart contracts, events)
- EIP-155 (chain IDs and replay protection): <https://eips.ethereum.org/EIPS/eip-155>
- Base documentation (network details, chain IDs); OP Stack documentation
