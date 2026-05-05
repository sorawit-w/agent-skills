---
name: handshake
description: >
  A brief, opt-in calibration ritual that runs before the real work. Shows the
  user what the agent already knows about them, then asks ≤4 high-leverage
  questions about how they want to collaborate (core mode), and optionally
  ≤6 scoped questions about the current project (overlay mode). Writes to the
  existing two-tier memory store using standard `user`-type and `project`-type
  entries — never a parallel store. Privacy-conscious by construction: hard
  never-ask list, every question carries a stated behavioral payoff, and the
  user can skip any item. Slash-command-only at v1 (no aggressive auto-trigger).
  Use this skill when the user invokes `/handshake`, when they ask to "calibrate
  how we work," "tune in to me," "set a working agreement," "share my
  preferences," or "get to know me," or when an upstream skill suggests
  calibration because user memory is sparse. NOT for codebase orientation
  ("get to know my codebase"), performance-review calibration ("set Q3
  calibration goals"), or content gathering (resumes, bios, requirements docs,
  CV bullets) — those are different jobs handled by other skills.
instructions: |
  Load this skill when:
  - The user invokes the `/handshake` slash command directly
  - The user says "calibrate how we work," "let's set working preferences,"
    "tune in to me," "set up a working agreement," or "get to know me"
  - Another skill (e.g., `team-composer`, `brand-workshop`) suggests running
    handshake first because relevant `user`-type memory is empty or stale,
    AND the user accepts that suggestion

  Do NOT load this skill when:
  - The user is in the middle of unrelated work and hasn't asked for calibration
  - There is no persistent memory system available in the current runtime
    (the skill writes to memory — without it, there's nothing to capture)
  - The user has already run `/handshake` recently and has core `user`-type
    memory entries — re-invocation should be deliberate, not automatic
  - The request is for project-content gathering (resume bullets, codebase
    summaries, requirements docs) — that's a different skill's job

tags:
  - calibration
  - collaboration
  - memory
  - onboarding
  - personalization
  - working-agreement
---

# Handshake

A brief mutual exchange that establishes the terms of subsequent collaboration. Not a friendship, not an interview — a handshake.

This skill exists because agents that don't know who they're talking to give generic answers. It exists *as a separate skill* — rather than relying on passive memory accrual — because **deliberate calibration is structurally different from incidental capture**: the user gets to see what's already known, correct it, and consent to what's added. That's the entire job.

---

## The three-part test (front and center)

Per the agent-skills repo convention, every new skill is checked against three axes before it earns a slot. Here's where `handshake` lands honestly:

| Axis | Verdict | Notes |
|---|---|---|
| **Unique structure** | Partial | Show-then-ask is a different control flow from passive memory accrual, but the underlying memory store is shared with the auto-memory system and `productivity:memory-management`. |
| **Unique deliverable** | No | The output is standard `user`-type and `project`-type memory entries — same format other surfaces produce. The skill **wraps** the existing memory contract; it does not invent a parallel one. |
| **Unique elicitation** | **Yes** | Privacy-conscious, consent-gated, show-what-I-know-first, ≤4 pill + 1 free-text core, optional ≤6 project overlay, hard never-ask list. This is the load-bearing reason the skill exists. |

The skill ships because the elicitation pattern is genuinely worth ritualizing — but it stays narrow on the other two axes by deliberate design. If you find yourself extending it to invent new memory types or invent new control flows, stop and ask whether you're really still inside `handshake`.

---

## What this skill does

- **Phase 0 — Show what I know.** Before asking anything, surfaces the most relevant existing `user`-type memory entries (≤5) so the user can correct stale facts or confirm what's already on file. If memory is empty, says so plainly.
- **Phase 1 — Core calibration (always runs).** Asks ≤4 high-leverage pill questions about how to collaborate, plus 1 free-text "what did past assistants get wrong about you?" question. Each question explains its behavioral payoff. Writes to `user`-type memory.
- **Phase 2 — Project overlay (optional).** If invoked with `--project`, or auto-suggested when `project`-type memory is empty for the current work, asks ≤6 scoped questions about the project (goal, stage, stakeholders, constraints, past decisions, external resources). All skippable. Writes to `project`-type memory — never `user`-type.
- **Closes with a written-to-memory summary** so the user can see exactly what was captured.

---

## What this skill does NOT do

- **Does not gather project content.** "Help me build a resume" needs work-history details — that is content for the resume, not preferences for how the agent works. Resume content belongs in a hypothetical `resume` skill (or in normal conversation), not in `handshake`. The project *overlay* captures meta-context (stage, constraints, stakeholders), not subject-matter material.
- **Does not invent a new memory store.** All writes go to the existing two-tier system — `user_*.md` files for personal preferences, `project_*.md` for project context, indexed in `MEMORY.md`. Same frontmatter, same conventions.
- **Does not handle multi-user identity.** Memory is per-Claude-instance, not per-team. If a teammate wants similar calibration, they run `/handshake` on their own Claude instance. Team-shared context belongs in `CLAUDE.md` or a `project`-type entry that's committed to the repo — not in `user`-type memory.
- **Does not auto-trigger aggressively at v1.** Slash-command-only invocation. Other skills MAY suggest running it, but never invoke it silently. Auto-trigger is a Phase 2 decision gated on observed user value (per the staged-rollout principle in this repo).
- **Does not ask anything on the never-ask list.** Hard refusal — even if the user's prompt invites it.

---

## When to use it

- The user invokes `/handshake` directly, or asks to "calibrate" / "tune in" / "set a working agreement."
- A new project is starting and `project`-type memory for it is empty — the user accepts a suggestion to run `/handshake --project`.
- The user has noticed the agent giving generic answers and wants to fix the input rather than the output.
- A different skill (`team-composer`, `brand-workshop`, etc.) suggests calibration because relevant `user`-type memory is sparse, AND the user accepts.

## When NOT to use it

- Mid-task — calibration interrupts flow. Save the suggestion for the next session.
- The user has just finished `/handshake` recently. Re-invoking the same session adds noise without signal.
- The runtime has no persistent memory (the skill has nothing to write to). Tell the user instead of running through the motions.
- The user is asking for project content (resume bullets, codebase summaries) — wrong skill, route them to a content-producing skill instead.

---

## How it works — the loop

### Phase 0 — Show what I know (always runs first)

Before asking anything new, read `MEMORY.md` (or its equivalent in the runtime) and surface the most relevant `user`-type entries. Format as a short, scannable list:

```
Here's what I have about you on file:
- [user_role.md] — Lead Software Engineer at UPS; frontend-strong fullstack
- [user_communication.md] — Prefers concise output, thorough reasoning
- [user_location.md] — Torrance, CA (originally Bangkok)
- [+ 2 more — say "show all" to see them]

Anything stale or wrong? Tell me and I'll update before we go further.
```

**Rules for Phase 0:**

- Cap visible entries at 5; offer "show all" for the rest. Long memory dumps feel surveilling.
- Include the file name in brackets so the user knows where it lives — memory should not feel like a black box.
- If memory is empty, say so plainly: *"I don't have anything on file about you yet — let's start fresh."*
- If the user corrects something, update the relevant memory file BEFORE moving to Phase 1. Do not batch corrections.
- **Transition to Phase 1 in the SAME response when memory is empty** — nothing to confirm, so proceeding directly avoids dead air. **When memory is non-empty, end the Phase 0 turn with the correction prompt and WAIT for the user's reply before showing Q1.** Surfacing memory and Q1 in one breath defeats the "show first, then ask" purpose — the user needs a beat to read what's on file before being asked something new.

### Phase 1 — Core calibration (always runs)

Ask ≤4 pill questions plus 1 free-text question. Each question MUST be:

1. Answerable in one line.
2. Tied to a specific change in agent behavior — state the payoff in the same breath as the question.
3. Skippable — "skip" is a first-class option on every pill.

**Default question bank (use these unless you have a strong reason to swap):**

#### Q1 — Expertise framing (pill)
> *"Roughly where do you sit on the technical spectrum?"*
> Options: `Engineer (senior)` · `Engineer (early-career)` · `Designer / PM / non-engineer technical` · `Non-technical` · `Skip`
>
> **Why I'm asking:** so I know how much to explain when I introduce a new pattern, library, or trade-off.

#### Q2 — Default collaboration mode (pill)
> *"When you give me a complex task, what's your default preference?"*
> Options: `Just do it, summarize after` · `Walk me through your plan first` · `Ask 1–2 questions to align, then start` · `Depends — ask each time` · `Skip`
>
> **Why I'm asking:** so I don't surprise you mid-task with the wrong altitude of involvement.

#### Q3 — Output verbosity (pill)
> *"Default depth for written output?"*
> Options: `Terse — bullets, no fluff` · `Balanced — explain, but tightly` · `Thorough — context + reasoning + examples` · `Skip`
>
> **Why I'm asking:** so my default response length matches what you actually want to read.

#### Q4 — One thing to remember (pill, optional 4th)
> *"Pick one to flag as important to remember about working with you:"*
> Options: `Show your reasoning, not just the answer` · `Push back if I'm wrong, don't just agree` · `Be skeptical of your own answers` · `Prefer editing over rewriting` · `Skip`
>
> **Why I'm asking:** captures one explicit collaboration norm that's easy to recall and apply.

#### Q5 — Free-text frustration
> *"What did the last AI assistant get wrong about you that drove you nuts?"* (free-text, optional)
>
> **Why I'm asking:** the gold lives here. One sentence is enough.

**Hard rules for Phase 1:**

- Ask the questions ONE AT A TIME, not as a wall of form. Wait for each answer before showing the next question.
- Cap at 4 pill + 1 free-text. If you find yourself wanting to add a 5th pill, you are scope-creeping into the project overlay — stop and ask whether the question really belongs in core.
- Every "skip" is honored silently. Do not nudge.
- Write each answer to memory IMMEDIATELY after receiving it (not at the end). If the user disconnects mid-flow, what they did say is captured.
- **Do NOT name the skill ("handshake," "this skill," "the handshake skill is designed to…") in user-facing turns.** Speak as a colleague calibrating, not a meta-narrator describing a workflow. The user knows what they invoked; surfacing that breaks the working-agreement framing and makes the conversation feel like a system explaining itself rather than two parties getting on the same page. Internal reasoning is fine; the user-facing response should sound like a colleague's first day, not a feature announcement.

### Phase 2 — Project overlay (optional, opt-in)

Triggered by:
- User invokes `/handshake --project` directly, OR
- Phase 1 just completed AND `project`-type memory for the current work is empty AND the user accepts a one-line offer: *"Want me to ask 3–6 questions about this project too? Skip if you'd rather I learn it as we go."*

**Default project-overlay question bank (cap at 6, all skippable):**

| # | Question | Why I'm asking |
|---|---|---|
| P1 | What's the project trying to achieve? (one sentence) | Goal anchor for prioritization. |
| P2 | What stage is it in? (`idea / prototype / MVP / production / maintenance`) | Calibrates risk tolerance and how aggressive to be on changes. |
| P3 | Who else is involved? (`solo / small team / larger org / external stakeholders`) | Affects how I write commits, comments, and docs. |
| P4 | Any non-obvious constraints? (deadlines, regulations, team norms, taboos) | Avoids landmines I can't see from the code alone. |
| P5 | Past decisions worth remembering? (one or two sentences) | Captures intent that the code itself doesn't carry. |
| P6 | External resources I should know about? (dashboards, docs, channels) | Stored as `reference`-type memory entries, not `project`. |

**Hard rules for Phase 2:**

- Project overlay writes to `project`-type memory (or `reference`-type for Q6). Never to `user`-type.
- Same one-at-a-time pacing as Phase 1.
- If Q6 is answered, write each link as a separate `reference`-type entry, not bundled.
- If the project changes (new directory, new repo), the overlay is invalid — re-run on demand, or accept the user's decision to skip.

### Phase 3 — Close with a written-to-memory summary

End the session with a tight, scannable summary of what was captured:

```
Done. Here's what I just wrote:

user-type:
  + user_expertise.md — senior engineer, frontend-strong fullstack
  + user_collaboration.md — prefers "walk me through the plan first"
  + user_verbosity.md — terse default
  + user_norms.md — push back if wrong; prefer editing over rewriting
  + user_frustration.md — past assistants over-explained the obvious

project-type (if overlay ran):
  + project_goal.md — ship v1 of agent-skills handshake skill by EOW

reference-type (if Q6 ran):
  + reference_design_md_spec.md — Google Labs DESIGN.md alpha

I'll lean on these going forward. Run `/handshake` again any time to update.
```

This closing summary is non-negotiable — it makes memory transparent rather than mysterious.

---

## Memory write contract

Every entry follows the standard auto-memory file format already in use:

```markdown
---
name: <short, human-readable name>
description: <one-line description used to decide relevance in future conversations>
type: user | project | reference | feedback
---

<body — for user/project entries, lead with the fact, then optional **Why:** and **How to apply:** lines>
```

**File naming:** `<type>_<topic>.md` — e.g., `user_collaboration.md`, `project_goal.md`, `reference_dashboard.md`. If a file already exists, **update in place** rather than creating a duplicate.

**Index update:** every new file gets a one-line entry in `MEMORY.md`. Format: `- [Title](file.md) — one-line hook`. Do NOT write the body of the memory into `MEMORY.md` itself — `MEMORY.md` is an index.

---

## Hard never-ask list

The skill must NEVER ask about, store, or surface:

- **Protected attributes:** race, ethnicity, national origin, religion, age, sex, sexual orientation, gender identity, immigration status, disability, serious illness, union membership.
- **Government identifiers:** SSN, driver's license, passport, government ID numbers.
- **Financial account details:** credit card, bank account numbers.
- **Health information:** medical conditions, diagnoses, lab results, mental-health details, therapy/counseling history.
- **Home or personal mailing addresses.** (Work addresses or general region — e.g., "Torrance, CA" — are fine if the user volunteered them.)
- **Account passwords, secret tokens, secret keys.**

If the user volunteers any of the above unprompted, the skill **completes the task** but **does not write the volunteered detail to memory**. State this politely once, then move on.

The never-ask list is the same one already encoded in the auto-memory system. Keeping them aligned is intentional — divergence between surfaces would create a privacy hole.

---

## Single-user contract

`handshake` calibrates only the agent for the **single person running this Claude instance**. It is not multi-user aware, and v1 will not pretend to be.

If teammates want similar calibration:
- They each run `/handshake` on their own Claude instance.
- Team-shared context (norms, conventions, glossary, decisions) belongs in:
  - `CLAUDE.md` at the repo root (loaded for every session in the repo), OR
  - `project`-type memory entries that the team agrees to commit to the repo.

Multi-user awareness (e.g., "are you still Kiang, or someone else?" prompts) is an open Phase 2 question, gated on evidence that the case actually appears in practice.

---

## Triggering rules

| Trigger | Action |
|---|---|
| `/handshake` slash command | Run Phase 0 → Phase 1. Offer Phase 2 if appropriate. |
| `/handshake --project` | Run Phase 0 → Phase 1 → Phase 2 (project overlay required). |
| User says "calibrate," "tune in," "set working preferences," "get to know me" | Run as if `/handshake` was invoked. |
| Another skill suggests handshake AND user accepts | Run as if `/handshake` was invoked. The suggesting skill MUST get explicit user acceptance — never auto-route. |
| Memory is empty mid-conversation, user has not asked | Do NOT auto-trigger. May offer a one-line suggestion at most. |

---

## Cross-skill integration

| Skill | When to interact |
|---|---|
| `productivity:memory-management` (if installed) | `handshake` writes into the same two-tier `MEMORY.md` + `memory/` store. If `productivity:memory-management` is installed and managing the file layout, defer to its conventions for file location and frontmatter — do not invent a parallel layout. If not installed, write directly into the runtime's persistent memory store using the standard frontmatter format. **Capability-gated, not vendor-gated.** |
| `team-composer` | When `team-composer` is about to assemble a team and `user`-type memory is empty, it MAY suggest running `/handshake` first so the team can be tailored. Suggestion only — never auto-route. |
| `brand-workshop` | Similar — may suggest `/handshake` if running for a personal-brand or solo-founder identity package and user memory is sparse. Suggestion only. |
| `validation-canvas` / `riskiest-assumption-test` / `pitch-deck` | These read project state, not user state. May suggest `/handshake --project` at kickoff if `project`-type memory for the current work is empty. Suggestion only. |
| `startup-launch-kit` | Does NOT include `handshake` in its pipeline. The launch kit is a startup pipeline; calibration is a generic collaboration primitive — they should not be coupled. The orchestrator MAY surface a one-line suggestion at start-up if appropriate. |
| Future hypothetical content-gathering skills (`resume`, `cv`, `portfolio`) | Belong in a separate skill. `handshake` covers HOW we work; content skills cover WHAT we work on. Don't fold one into the other. |

**Graceful degradation:** if no persistent memory store is available in the runtime, the skill says so explicitly at invocation and offers to print the answers to chat instead. It does not pretend to write.

---

## Status and scope

`v0.1` — slash-command-only triggering, two-mode design (core + project overlay), single-user contract, hard never-ask list, capability-gated memory integration.

**Supported:** core calibration, project overlay, show-then-ask preamble, write-to-existing-memory, single-user calibration.

**Not supported (deferred to Phase 2 with evidence):** auto-trigger when memory is empty, multi-user identity awareness, re-calibration cadence detection, cross-skill auto-invocation.

If asked to do something outside this scope, the skill says so explicitly rather than expanding silently.

---

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
