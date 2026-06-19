# Global skills policy

> **What this is:** the canonical, source-of-truth copy of the cross-surface skills policy. It is a **reference artifact** — it is *not* loaded automatically by any skill or harness. Because it shapes behavior across *all* tasks, it does not live as a repo file you load; the live copy must be pasted into each surface's settings separately (the surfaces don't share memory):
>
> - **Chat** → profile / personal instructions
> - **Cowork** → its settings
> - **Code** → each repo's `CLAUDE.md` / `BOOTSTRAP`
>
> Keep it short. A bloated global instruction is self-defeating — context rot is the whole reason skills exist.

---

## Skills policy

- **Skill vs. always-on context.** Conventions that apply to *every* task (stack, project rules, how I work) belong in passive global context — not in a skill. Reserve skills for narrow, action-specific workflows the agent loads on demand. If you're tempted to write a skill for something that should always be true, it belongs here instead. A passive index reliably beats an always-firing skill for global conventions.

- **Write software, not rules (shift-left).** When behavior must be deterministic, don't encode it as prose imperatives — models learn to skim walls of "ALWAYS / NEVER" the way a developer ignores a wall of warning text. Push the judgment into a script or a check so the wrong action is *impossible*, not merely discouraged. Reserve prose for explaining the **why**.

- **Mental model.** System prompt = instinct. Global / `AGENTS.md` = project README. Skills = the runbook loaded on demand. MCP = hands. Don't reach for a skill when a passive note does the job.

---

*Relationship to this repo's authoring doc:* `CLAUDE.md`'s "Harness vocabulary" (Context engineering, Progressive disclosure) covers the same ground as the skill-vs-passive-context point above, but from the in-repo authoring angle. This doc owns the global-settings framing; `CLAUDE.md` owns the authoring framing. They point at each other rather than duplicating.
