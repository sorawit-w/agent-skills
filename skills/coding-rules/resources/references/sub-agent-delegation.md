# Sub-Agent Delegation

For detailed delegation patterns, load the `sub-agent-coordinator` skill (if available). This stub provides the minimum needed when the skill is not installed.

---

## When to Delegate

Use sub-agents to parallelize independent work. Delegate if ANY of these signals match:

| Signal | Trigger |
|--------|---------|
| 🐛 **Debugging / Iterative Fixes** | Multiple fix-test cycles, error hunting |
| 🔧 **Iterative Work** | Styling, tuning, API integration — expects multiple attempts |
| 🏗️ **Feature (3+ files)** | Touches 3 or more files in different areas |
| 📝 **Documentation** | Updates needed across multiple files |
| 🔍 **Investigation / Research** | Exploring unfamiliar codebases or third-party APIs |

If ANY signal matches AND your platform supports sub-agents (Claude Code, Aider, Cursor agent mode), delegate. Otherwise implement sequentially.

---

## Quick Brief Template

For straightforward tasks (complexity 1–5):

```
Task: [what to do]
Scope: [files/components to touch]
  - [file 1]
  - [file 2]
  Out of scope: [what NOT to touch]
Budget: ~[N] tool calls
Done when:
  ✅ [criterion 1]
  ✅ [criterion 2]
  ✅ Quality gates pass (build + lint + test)
```

### Tool-Call Budget Anchors

Use these as starting values when filling in `Budget: ~[N] tool calls` above. They are **anchors, not caps** — exceed them if the work genuinely demands it, but treat overruns as a signal that the task may be misscoped and worth re-planning rather than grinding through.

| Scope | Anchor | When overshoot is reasonable |
|-------|--------|-------------------------------|
| Lookup / single-file edit | ~10 calls | Rare — past 15 calls you've drifted |
| Targeted bug fix | ~20 calls | Reproduction was hard, or root cause moved between files |
| Feature touching 3–5 files | ~40 calls | Discovery surfaced unknown integration points |
| Cross-cutting refactor | ~80 calls | Genuine multi-file scope — but consider splitting first |
| Investigation / research | ~30 calls | Following an unexpectedly deep call chain |
| QA sub-agent (post-shutdown review) | ~15 calls | Issue density is high enough to warrant deeper inspection |

**Why anchors matter:** tool calls cost both latency and tokens. A stated budget makes overruns visible — if a "small" task balloons past its anchor, stop and re-scope rather than continuing on momentum.

---

## Vertical Slices Over Horizontal Layers

When breaking work into parallel sub-agent tasks, prefer **vertical slices** (each sub-agent owns one user-feature end-to-end — model + API + UI + tests) over **horizontal layers** (one sub-agent does all models, another all APIs, another all UIs).

**Why:** vertical slices ship and verify independently. Horizontal layers create handoff dependencies — the API agent waits for the model agent, the UI agent waits for the API agent — and integration debt surfaces at the worst possible time, after all the layers are "done."

**Heuristic:** if you can write the Done-when criterion as a user-observable behavior, it's a vertical slice. If the Done-when criterion is "interface X exists for layer Y to consume," it's a horizontal layer — re-slice.

**Exception:** foundational work (database schema migration, shared type definitions, build configuration) genuinely belongs in a single horizontal pass before vertical slices begin. Don't force-vertical when the work is shared infrastructure with no user-facing surface.

**Source:** absorbed from `gsd-build/get-shit-done` (2026-05-09); GSD's wave-parallelism doctrine is the load-bearing insight.

---

## Coordination Rules (Essential)

1. **Non-overlapping files** — Each sub-agent works on different files. If two tasks touch the same file, execute sequentially.

2. **Trust-but-verify** — Read the sub-agent's verification report. Only re-run quality gates if the report is missing, incomplete, or shows failures.

3. **No nested sub-agents** — Sub-agents do not spawn their own sub-agents. All spawning is done by the coordinating agent.

4. **Shared worktree by default** — Sub-agents operate in the same worktree as the coordinator. Rely on rule 1 (non-overlapping files) to prevent conflicts.

---

## Platform Fallback

If your agent platform does not support sub-agents, implement sequentially. Each implementation task should still follow the task loop (implement → check → commit → log → repeat).

---

## For Full Patterns & Templates

→ Load the `sub-agent-coordinator` skill for:
- Full briefing template (context, scope, constraints, reporting)
- Coordination patterns (fan-out, pipeline, specialist routing, review)
- Communication protocol & check-in intervals
- Example scenarios (monorepo setup, translation work, parallel review)
- Spawning checklist
- Common mistakes & how to avoid them
