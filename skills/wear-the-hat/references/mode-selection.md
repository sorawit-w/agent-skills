# Mode Selection — Inline vs Sub-Agent

After the role is picked (Phase 1) and the persona is loaded (Phase 2), wear-the-hat decides how to execute: in-place (orchestrator speaks as the role) or via a sub-agent (a separate worker with the persona context loaded). This file is the decision tree.

---

## TL;DR

| Task characteristic | Mode |
|---|---|
| Short analytical task, single-paragraph or short-list response | **inline** |
| Hits any of `sub-agent-coordinator`'s spawning signals | **sub-agent** |
| Read-heavy investigation that benefits from isolated context | **sub-agent** |
| Live conversation that needs full orchestrator state | **inline** |
| User explicitly requested one mode | **as requested** (always wins) |

The orchestrator announces the choice in the 1-line disclosure:

> Wearing `@security_specialist`'s hat (sub-agent mode — task hits 3+ files signal).
>
> Wearing `@dataviz_engineer`'s hat (inline mode — single-encoding question).

---

## Decision tree

Walk the tree top to bottom. First match wins.

### 1. User explicit override

If the user said "do this inline" / "in this conversation" / "don't spawn" → **inline.**

If the user said "spawn a sub-agent" / "fan out" / "delegate this" → **sub-agent.**

User intent always overrides heuristics. Skip the rest of the tree.

### 2. Spawning signals (from sub-agent-coordinator)

If any of these are true → **sub-agent mode.** These are the canonical signals from `sub-agent-coordinator` § Spawning Signals:

- The task estimates > 2 minutes of actual work
- The task is iterative (multiple fix-test cycles expected): styling, performance tuning, debugging
- The task touches 3+ files
- The task involves dependency issues (cache clearing, lock file regen, version conflicts)
- The task is a test suite, not a single test
- The task updates docs across 2+ files
- The task is an investigation / research dive into unfamiliar code or third-party APIs

If wear-the-hat is being invoked for a task that hits these signals, the role embodiment runs inside a sub-agent — both for isolation and because the sub-agent can stay focused without the orchestrator's conversational context bleeding in.

### 3. Inline-fitting characteristics

If none of the spawning signals fire, AND any of these are true → **inline mode.**

- The task is a single-paragraph or short-list response (e.g., "from the security perspective, what should I worry about here?")
- The task is a quick analytical lens applied to text already in the conversation
- The task is a sanity-check or sniff-test (e.g., "would the data-viz engineer flag anything about this chart spec?")
- The task is a brainstorm or option-listing that doesn't produce a deliverable file
- The task is < 2 minutes of estimated work

### 4. Ambiguous (default)

If neither branch above gives a clean answer → **inline.** Inline is the lower-overhead choice; sub-agent has spawning latency cost. When unsure, prefer inline; the user can ask to "spawn a sub-agent for this" if they need isolation.

---

## What changes between the modes

### Inline mode

- The orchestrator stays in this conversation
- Response is in the role's voice using the loaded perspective + signature phrases
- All conversation context is available (prior messages, files read, decisions)
- Lower latency, no spawning cost
- Suitable for: single-response analytical work, quick lenses, brainstorms, sniff-tests

### Sub-agent mode

- A new sub-agent is spawned with the persona context baked into the brief
- The sub-agent has only what the brief provides — no implicit conversation context
- Quality gates run inside the sub-agent's worktree
- Returns a structured report (per `sub-agent-coordinator`'s Reporting Section shape)
- Suitable for: multi-file work, iterative tasks, investigations, anything that fits coordinator's spawning signals

---

## Hand-off shape (sub-agent mode)

When sub-agent mode is chosen, wear-the-hat produces a brief and **hands off to `sub-agent-coordinator`'s protocol.** It does NOT duplicate coordinator's spawning, briefing, or coordination logic.

The brief uses `sub-agent-coordinator`'s Full Brief template, with two additions:

```
Constraints:
  - ... (other constraints)
  - Role: @<picked-role>
  - Persona context:
      Perspective: <from role-personas.md>
      Signature phrases:
        - "<phrase 1>"
        - "<phrase 2>"
        - "<phrase 3>"
```

The `Role:` line and `Persona context:` block sit alongside the regular Constraints lines (model selection, tool budget, etc.). The sub-agent reads them, embodies the persona for its scoped work, and reports back per the coordinator's Reporting Section shape.

**wear-the-hat does NOT stay engaged across sub-agent execution.** Once the brief is produced and handed off, coordinator owns the lifecycle. wear-the-hat returns control to the orchestrator with the brief; the orchestrator (or `sub-agent-coordinator`) spawns from there.

---

## Edge cases

### Sub-agent mode but task is huge

If a single task is large enough that the sub-agent might hit `BLOCKED_SCOPE_EXPANDED` (per `sub-agent-coordinator` rule 6), include this in the brief's `Done when:` clause:

> If scope expands beyond this brief, report `BLOCKED_SCOPE_EXPANDED` with a proposed split — do NOT silently keep going.

This is just `sub-agent-coordinator`'s existing protocol. wear-the-hat surfaces it explicitly because role-embodied sub-agents tend to over-scope (the persona's perspective can pull the work toward "let me also check…" territory).

### Inline mode but conversation context is lacking

If inline mode is chosen but the orchestrator notices it doesn't have enough context (e.g., files haven't been read), it reads first, then proceeds in role. Don't switch modes mid-flight just because reading is needed — that's just normal work.

### Mode mismatch with user expectation

If the user invoked wear-the-hat with phrasing that implies one mode but the heuristic suggests the other, **disclose and ask:**

> Task suggests sub-agent mode (touches 4 files). You phrased it as a quick lens. Inline or sub-agent?

Respect the user's reply. Don't second-guess silently.

---

## Why this lives in wear-the-hat, not in sub-agent-coordinator

`sub-agent-coordinator` answers "should I spawn a sub-agent for this work?" — a general question. wear-the-hat answers "for a single-role embodiment task, should I run it inline or as a sub-agent?" — a wear-the-hat-specific question with role-embodiment-specific nuances (persona context bleed, role over-scoping risk).

The two skills compose: wear-the-hat picks the mode and the role; if sub-agent mode is chosen, coordinator handles the spawning/coordination protocol. Clean separation, no duplication.
