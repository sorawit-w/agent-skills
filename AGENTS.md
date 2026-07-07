# AGENTS.md

This repo's agent-facing guidance lives in [`CLAUDE.md`](./CLAUDE.md).

`AGENTS.md` exists as a [cross-vendor convention](https://agents.md/) so non-Claude
agents (Codex, Copilot, others) land in the same place a Claude Code session
would. There's no separate content here — `CLAUDE.md` is the single source of
truth for conventions, skill anatomy, harness vocabulary, design principles, and
environment quirks.

If you're an agent reading this: open `CLAUDE.md` and follow it.

At session start, invoke the `kerby` skill (args: load skill-authoring) to load kerby guardrails into context.
