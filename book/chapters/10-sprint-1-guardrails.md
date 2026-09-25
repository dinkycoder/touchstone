---
chapter: 10
title: "Sprint 1: Guardrails before code"
part: III. Building Touchstone
status: outline
durability: durable
written: now (Sprint 1 shipped)
curriculum: [Introduction to Git and GitHub, Software Testing and Agentic Software Development, CI/CD and Software Maintenance]
---

# 10. Sprint 1: Guardrails before code

Ready to draft: everything in it already happened and is in the repo's history.

**By the end, the reader can:**
- explain why the first sprint built guardrails instead of product code
- explain how Claude Code hooks enforce rules, and what an exit code of 2 means
- explain "fail closed", and the difference between a tripwire and a sandbox
- explain why a docs check failed when someone ticked a checkbox, and how it was fixed

## Outline

1. **Why guardrails first.** One human reviewing many agent sessions. `CLAUDE.md` can only ask; hooks
   and permissions enforce.
2. **The repo's shape.** A protected `main` (pull request required, `test` check required, squash-merge
   only, no bypass for anyone), CI on every push, tests before code.
3. **Three hooks.** `guard.py` runs before every shell command; `bench_gate.py` and
   `commit_checkpoint.py` run when a session tries to stop. How Claude Code reads a hook's exit code.
4. **Probing the guard.** The first version missed in every category it was meant to cover: reading
   `.env`, reaching mainnet, touching the sealed set, writing raw sanctions data. The fixes:
   - match what a command *names*, not which program it runs
   - check three normalized views of each command
   - fail closed when the guard itself breaks
   - the false positive where `8453` also matched Base Sepolia's `84532`
5. **False positives versus misses.** Blocking commit messages that merely mentioned `.env`, and the
   later carve-out for message text the shell can't expand.
6. **The docs check that failed on a checkbox.** Mapping a source file to a doc generated from it, and
   the fix: check whether the generated text is stale (`gen_readme.py --check`), not whether the file
   changed.
7. **The live probe.** Listing hooks with `/hooks`, blocking a PowerShell and a Bash command, and learning
   from the block message that PowerShell commands arrive in the field the guard expected.
8. **What a tripwire can't do.** The known gaps (scripts that read files themselves, paths built from
   variables, recursive searches), and why the sealed set has to leave the checkout entirely.

## In Touchstone

- [.claude/hooks/guard.py](../../.claude/hooks/guard.py) and
  [tests/hooks/test_guard.py](../../tests/hooks/test_guard.py)
- [scripts/gen_readme.py](../../scripts/gen_readme.py), [docs/docs-map.yml](../../docs/docs-map.yml),
  [.github/workflows/ci.yml](../../.github/workflows/ci.yml)
- The history: [#1](https://github.com/dinkycoder/touchstone/pull/1) (scaffolding),
  [#2](https://github.com/dinkycoder/touchstone/pull/2) (guard hardening and the docs check),
  [#3](https://github.com/dinkycoder/touchstone/pull/3) (live probe results),
  [#4](https://github.com/dinkycoder/touchstone/pull/4) (commit-message carve-out)

## Quiz

1. Why does the guard exit with code 2 on any internal error instead of 0 or 1?
2. Why did `8453` block Base Sepolia commands, and what was the fix?
3. Why does the guard match paths and hosts rather than program names like `cat`?
4. Why is a command-string guard a tripwire and not a sandbox? Name two things it can't see.
5. Why did ticking a checkbox turn CI red, and why is `--check` the better test?
6. The commit-message carve-out blanks some message text before checking. Why is `-m "$(cat .env)"`
   still blocked?

## Sources to check

- Claude Code hooks documentation (exit-code semantics, Stop hooks, exec-form commands)
- PRs #1–#4 and [docs/sprint/CURRENT.md](../../docs/sprint/CURRENT.md)
