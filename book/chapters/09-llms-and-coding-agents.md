---
chapter: 9
title: Building with LLMs and coding agents
part: II. Foundations
status: outline
durability: durable core, dated tooling details
written: before Sprint 5
curriculum: [Prompt Engineering, LLM-Based Apps, AI Agents, AI-Assisted Software Development]
---

# 9. Building with LLMs and coding agents

**By the end, the reader can:**
- explain the difference between a prompt, a tool and an agent
- explain retrieval and vector search, and when they help
- say where an LLM belongs in a sanctions decision, and where it must not be
- explain how this book's system was built with a coding agent without handing it the approvals

## Outline

1. **LLMs as components.** Prompts, structured output, and testing the output like any other code.
2. **Retrieval and vector search.** Embeddings, pgvector, and retrieval-augmented generation for
   rationales.
3. **Rationales without hallucinations.** Templates first; LLM drafts that a human reviews; an LLM never
   decides whether something is a hit.
4. **Agents and tools.** What makes software an agent. The Model Context Protocol (MCP), and Touchstone's
   MCP server as a thin client over `/check/*`.
5. **Building with a coding agent.** Claude Code, subagents, hooks and permissions. Why Claude and the
   subagents are second readers and never approvers. Guardrails as code (Chapter 10 tells the story).
6. **Evaluating LLM output.** Tests, rubrics, human review, and tracking cost.

## In Touchstone

- `services/mcp/` and `console/` (planned, Sprint 5)
- [.claude/](../../.claude/) (settings, hooks, skills) and [CLAUDE.md](../../CLAUDE.md)

## Quiz

1. What's the difference between a prompt, a tool and an agent?
2. At which step of a screening decision must no LLM be involved, and why?
3. What is MCP, and what would Touchstone's MCP server let another agent do?
4. Why are coding agents second readers here and never approvers?
5. When does retrieval-augmented generation help, and when does it add risk?

## Sources to check

- Model Context Protocol specification
- Claude Code documentation (hooks, subagents, permissions)
- LangChain and pgvector documentation
