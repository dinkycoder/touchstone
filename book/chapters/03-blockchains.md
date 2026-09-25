---
chapter: 3
title: Blockchains from first principles
part: II. Foundations
status: outline
durability: durable
written: before Sprint 3
curriculum: [Introduction to Blockchain]
---

# 3. Blockchains from first principles

**By the end, the reader can:**
- explain what a hash function and a digital signature each guarantee
- explain where a wallet address comes from, and why it says nothing about who controls it
- explain what a transaction is and why it can't be reversed like a card payment

## Outline

1. **The problem a blockchain solves.** A ledger many parties share without trusting one keeper.
2. **Hash functions.** Fingerprints for data, and how chaining them makes history tamper-evident.
3. **Keys, signatures and addresses.** A private key, the public key derived from it, and the address
   derived from that. A signature proves control of a key, not identity. Anyone can make a new address
   at any time, and that one fact is why Touchstone exists.
4. **Transactions.** Bitcoin's inputs and outputs versus Ethereum's accounts; nonces; fees.
5. **Blocks and consensus.** Proof of work and proof of stake at the level a builder needs; finality;
   why there are no chargebacks.
6. **Public but pseudonymous.** Every transaction is visible and none is labelled. What that means for
   screening: the data is all there, the names aren't.

## In Touchstone

- Signed API responses in `services/api` (planned, Sprint 3)
- Only salted entity hashes go onchain (see Chapter 7)

## Hands-on

From the [learning plan](../learning-plan.md): generate a throwaway key offline, sign a message, and
recover the signer's address from the signature.

## Quiz

1. What does a valid signature prove, and what doesn't it prove?
2. Where does an Ethereum address come from?
3. Why can't a confirmed transaction be reversed the way a card payment can?
4. What does "pseudonymous" mean for someone trying to screen a counterparty?
5. What would an attacker have to do to rewrite an old block, and why is that impractical?

## Sources to check

- Satoshi Nakamoto, "Bitcoin: A Peer-to-Peer Electronic Cash System" (2008)
- ethereum.org developer documentation (accounts, transactions, proof of stake)
- Further reading: Antonopoulos, *Mastering Bitcoin*; Antonopoulos and Wood, *Mastering Ethereum*
