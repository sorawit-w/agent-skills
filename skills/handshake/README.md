<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/handshake-li.svg" alt="handshake — calibrate before the work starts" width="100%"/>
</p>

# handshake

A Claude Code skill for the brief mutual exchange that should happen before real work begins. Calibrates how the agent will collaborate with you (core) and what it needs to know about this project (overlay) — privacy-conscious, consent-gated, written to the existing two-tier memory store.

## Why this exists

Agents that don't know who they're talking to give generic answers. The auto-memory system in modern Claude runtimes captures user context *passively* over many sessions, which is great for accrual but bad for two things:

1. **The user never sees what's been captured** until a memory accidentally surfaces in chat — at which point it can feel surveilling.
2. **Calibration is reactive, not deliberate.** You only find out the agent learned the wrong thing about you after it acts on the wrong thing.

`handshake` exists to flip that: a short, opt-in moment where the agent shows you what it already knows, asks ≤4 high-leverage questions about how you want to work together, and (optionally) ≤6 scoped questions about the current project. It writes the answers to the same memory store the auto-system uses — same file format, same conventions, no parallel layout — but the writes are explicit and transparent.

This is a working agreement, not a friendship. The skill is named `handshake` deliberately: brief, mutual, professional, honest about what's happening.

## What it does

- **Phase 0 — Show what I know.** Surfaces the most relevant existing `user`-type memory entries (≤5) so you can correct stale facts or confirm what's on file before anything new gets added. If memory is empty, says so plainly.
- **Phase 1 — Core calibration (always runs).** Asks ≤4 pill questions about expertise framing, default collaboration mode, output verbosity, and one explicit collaboration norm — plus 1 free-text "what did past assistants get wrong?" question. Each question states its behavioral payoff. Writes to `user`-type memory.
- **Phase 2 — Project overlay (opt-in).** Triggered by `/handshake --project` or accepted at the end of Phase 1. Asks ≤6 scoped questions about the current project (goal, stage, stakeholders, constraints, past decisions, external resources). All skippable. Writes to `project`-type memory — never `user`-type.
- **Phase 3 — Closes with a written-to-memory summary** so you can see exactly what was captured, and where.

## What it doesn't do

- **Doesn't gather project content.** "Help me build a resume" needs work-history details; that's content for the resume, not preferences for how the agent works. The project *overlay* captures meta-context (stage, constraints, stakeholders), not subject-matter material.
- **Doesn't invent a new memory store.** All writes go to the existing two-tier system — `user_*.md` and `project_*.md` files indexed in `MEMORY.md`. Same frontmatter, same conventions.
- **Doesn't handle multi-user identity.** Memory is per-Claude-instance. Teammates each run `/handshake` on their own instance; team-shared context belongs in `CLAUDE.md` or a committed `project`-type entry.
- **Doesn't auto-trigger aggressively at v1.** Slash-command-only invocation. Other skills MAY suggest running it; never invoke it silently.
- **Doesn't ask anything on the never-ask list.** Hard refusal — even if the user invites it.

## When to use it

- You invoke `/handshake` directly, or ask to "calibrate" / "tune in" / "set a working agreement."
- A new project is starting and you accept a suggestion to run `/handshake --project`.
- You've noticed the agent giving generic answers and want to fix the input rather than the output.
- Another skill (`team-composer`, `brand-workshop`, etc.) suggests calibration because relevant memory is sparse, and you accept.

## When not to use it

- Mid-task — calibration interrupts flow. Save it for the next session.
- You've just finished `/handshake` recently — re-invoking the same session adds noise without signal.
- The runtime has no persistent memory (the skill has nothing to write to).
- You're asking for project content (resume bullets, codebase summaries) — wrong skill, route to a content-producing skill instead.

## Hard never-ask list

The skill must NEVER ask about, store, or surface: protected attributes (race, ethnicity, religion, age, sex, sexual orientation, gender identity, immigration status, disability, serious illness, union membership), government identifiers (SSN, driver's license, passport), financial accounts, health information, home addresses, or passwords / secret tokens. This list mirrors the existing auto-memory PII rules — divergence between surfaces would create a privacy hole.

If the user volunteers any of the above unprompted, the skill completes the task but does not write the volunteered detail to memory.

## Single-user contract

`handshake` calibrates only the agent for the **single person running this Claude instance**. It is not multi-user aware, and v1 will not pretend to be. Teammates each run `/handshake` on their own instance; team-shared context belongs in `CLAUDE.md` or a committed `project`-type memory entry.

## Design choices worth knowing

- **Show-then-ask is mandatory, not optional.** Surfacing existing memory before asking anything new builds trust and validates that memory isn't a black box. Skipping Phase 0 turns the skill into a survey, which it is not.
- **Every question carries a behavioral payoff.** If a question can't be tied to "next time you do X, I'll do Y differently," it doesn't ship. This bounds scope and keeps the skill from drifting into casual interrogation.
- **One question at a time.** Walls of form questions hit consent fatigue and produce shallow answers. The pacing is deliberately conversational, even though the format is structured.
- **Writes are immediate, not batched.** Each answer goes to memory the moment it's received, so a mid-flow disconnect doesn't lose the work that was done.
- **Capability-gated integration with `productivity:memory-management`.** If installed, defer to its file-layout conventions; if not, write directly to the runtime's persistent memory using the standard frontmatter format. Vendor identity is not a routing input.
- **Slash-command-only at v1.** Aggressive auto-trigger is a Phase 2 decision gated on observed user value (per the staged-rollout principle in this repo). Lowering the trigger threshold first and rolling back is the wrong direction.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

Once installed, invocation triggers on `/handshake`, `/handshake --project`, or phrases like "calibrate how we work," "set a working agreement," "tune in to me," or "let's get on the same page about how we collaborate."

## Status and scope

`v0.1` — slash-command-only triggering, two-mode design (core + project overlay), single-user contract, hard never-ask list, capability-gated memory integration.

- **Supported:** core calibration, project overlay, show-then-ask preamble, write-to-existing-memory, single-user calibration.
- **Not supported (deferred to Phase 2 with evidence):** auto-trigger when memory is empty, multi-user identity awareness, re-calibration cadence detection, cross-skill auto-invocation.

If asked to do something outside this scope, the skill says so explicitly rather than expanding silently.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
