# Context & Session Management

Long-running sessions consume context window tokens. If you don't manage this proactively, the conversation will hit its token limit mid-task and you'll lose working context.

---

## Monitor Your Context Usage

Be aware of how much context you've consumed. Warning signs:
- The conversation has been going for many back-and-forth exchanges
- You've read or generated large amounts of code
- You've pasted long error logs or command outputs

**Numeric targets.** Keep context usage under 40% of the window; aim for under 30% on intelligence-sensitive work (novel design, ambiguous debugging). On long-context models (1M tokens), quality degrades noticeably past ~300–400k tokens regardless of remaining capacity — the "dumb zone" kicks in well before the hard limit.

Source: "dumb zone" framing and 300–400k threshold distilled from `shanraisshan/claude-code-best-practice` (2026-04-19, MIT).

---

## Session Hygiene

Small disciplines to keep context cheap and focused. These are *suggestions to the developer*, not unilateral actions — the agent flags, the developer decides.

- **For files over 100KB, prefer targeted reads first** — `Read` with `offset`/`limit`, or grep for the specific symbol. Read the full file when targeted reads can't answer the question. The rule is to read *efficiently*, not *defensively* — never refuse or ask permission when the task requires the file.
- **Check cache health on long sessions.** When the conversation has run long, suggest the developer run `/cost` to confirm prompt caching is still working. Cache misses turn input tokens into a recurring cost — the rules themselves load on every turn.
- **New session when topics switch.** When the developer pivots to unrelated work (different repo, different feature area, different domain), suggest a fresh session. Carrying unrelated context forward inflates input cost and risks bleed-over from the previous topic.
- **Discard failed attempts, don't paper over them.** When a fix attempt fails, prefer discarding it from context (compact, restart, or rewind if your platform supports it) over layering corrections on top. Failed attempts pollute subsequent reasoning and steer the model back toward the same dead end.

Sources: first three bullets distilled from `drona23/claude-token-efficient` (2026-04-19); "discard failed attempts" distilled from `shanraisshan/claude-code-best-practice` (2026-04-19, MIT). Each rule is testable by the agent, addresses a frequent failure mode, and complements existing context-management without duplicating it.

---

## Create a Session Checkpoint Before You Run Out

When the conversation is getting long, **proactively create a full checkpoint before it's too late**. A session checkpoint captures everything the next session needs to resume seamlessly:

1. **Git checkpoint** — Commit and push all current work. Anything uncommitted will not survive a session boundary.
2. **Update `.ai/STATUS.md`** — Record current position, what's done, what's next, and any decisions made
3. **Update `.ai/memory.log`** — Write a detailed session summary covering: what was accomplished, key decisions and their rationale, open questions, and exact next steps
4. **Compact or request a new session** — If the agent supports conversation compaction/summarization, trigger it. Otherwise, tell the developer: *"This session is getting long. I've created a checkpoint — committed all work and updated `.ai/STATUS.md` and `memory.log`. A fresh session can pick up from where I left off."*

**Rule:** Never let a session expire without a checkpoint. The next agent (or the same agent in a new session) should be able to resume without guessing.

---

## Resuming from a Checkpoint

When starting a new session that continues prior work:

1. Read `.ai/STATUS.md` and `.ai/memory.log` first — this is your checkpoint
2. Check `git log --oneline -10` for recent commits
3. Run quality gates to confirm the repo is in a clean state
4. Pick up from the next task in the queue — don't re-do completed work

---

## Shutdown Sequence

When finishing a session or hitting a stopping point, create a final checkpoint.

**Shutdown is a distinct ritual, not a complexity-gated task validation.** Per-task
validation in `validation.md` scales with complexity — that's correct when the next
task is coming and you can re-verify later. At shutdown you're leaving; there is no
"later" in this session. The steps below run **regardless of how simple the session's
work looked in isolation**, because (a) cumulative session changes may be larger than
any single task, (b) a fresh-eyes pass catches drift a busy implementer missed, and
(c) you may not be the next agent to open this repo.

1. **Validate — always spawn a QA sub-agent.** Run a two-stage review (spec
   compliance → code quality) against the session's changes, not just the last edit.
   Do not skip this even if individual tasks were complexity 1–3. See
   `validation.md` for the two-stage structure; ignore its complexity table here —
   shutdown always gets the full sub-agent treatment.
2. **Verify — always run full quality gates.** Execute
   `{build_command} && {lint_command} && {test_command}` (or the three atomic
   equivalents). Unconditional. A session that produced only whitespace changes
   still runs gates, because whitespace can break YAML, Python indentation,
   or lint rules.
3. **Provide manual verification instructions — always.** Tell the developer how
   to manually verify what shipped this session. Even "no functional changes"
   warrants a one-line note ("session was cleanup only — no behavior to verify").
   Unconditional.
4. **Checkpoint** — Commit and push. No uncommitted changes left behind.
5. **Log** — Final session summary in `.ai/memory.log`
6. **Update** — `.ai/STATUS.md` reflects current state
7. **Document blockers** — If any, add to `.ai/BLOCKERS.md` and/or issue tracker
8. **Document human actions** — If any, ensure `DEVELOPER_TODO.md` is complete
9. **Do NOT merge** — Leave that for human review

> **Calibration note (2026-04-16):** This section was amended after round-1 of
> the coding-rules eval. The prior version inherited `validation.md`'s
> complexity table, which let an agent skip QA/verification/manual-steps for a
> low-complexity session. Shutdown now states its own rules explicitly and
> overrides the complexity gating.
