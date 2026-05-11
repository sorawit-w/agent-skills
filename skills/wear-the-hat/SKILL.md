---
name: wear-the-hat
description: >
  Pick ONE role from `team-composer`'s catalog (or a user-specified role) and
  perform a task in that role's voice — solo, no panel discussion. Use this
  skill when the user wants a single specific lens applied to a task without
  convening a multi-role discussion. Triggers on explicit `@role` tags
  ("audit middleware/ as @security_specialist"), role-embodiment phrases
  ("act as a security specialist", "wear the hat of the architect", "from the
  data-viz perspective", "have the copywriter rewrite this", "embody"), or
  any prompt that names a role-shaped lens to apply. Does NOT trigger on
  generic tasks that don't ask for a role lens — those route to coding-rules,
  team-composer, or sub-agent-coordinator as usual. When the task spans
  multiple roles (e.g., "create an HTML slide deck from source URL" — needs
  HTML construction + content extraction + narrative), the skill stops,
  surfaces candidate single roles, and offers an explicit hand-off to
  `team-composer`. Never silently picks one role for a multi-role task.
  Reuses `team-composer/references/role-personas.md` as the canonical role
  catalog (no duplicate taxonomy). For panel discussion of one decision use
  `team-composer`; for parallel worker fan-out use `sub-agent-coordinator`.
instructions: |
  Load this skill when:
  - The user explicitly tags a role with `@role` from the team-composer catalog
  - The user uses a role-embodiment phrase ("act as", "wear the hat of",
    "as the [role]", "from the [role]'s perspective", "embody", "channel")
  - The user wants one specific lens applied to a task — solo, not panel

  Do NOT load this skill when:
  - The user wants multiple roles to discuss the same decision → team-composer
  - The user wants N parallel workers on independent tasks → sub-agent-coordinator
  - The task has no role-lens framing — let the normal skill stack handle it

tags:
  - role
  - persona
  - solo-embodiment
  - single-role
  - lens
  - auto-pick
---

# wear-the-hat

Put on a single role's hat and do the work in their voice. This skill is for **solo embodiment** — one role per invocation, no panel discussion. When the user wants `@security_specialist` to audit middleware, or the architect's lens applied to a design, or the copywriter to rewrite a paragraph, this is the entry point.

Use **`team-composer`** for multi-role panel discussion. Use **`sub-agent-coordinator`** for parallel worker fan-out. Use **wear-the-hat** when the deliverable is one role's work, in their voice.

---

## Phase 0 — Trigger gate

Activate this skill only on one of these signals:

| Signal | Example |
|---|---|
| Explicit `@role` tag | "audit middleware/ as `@security_specialist`" |
| Embodiment phrase | "act as a security specialist and audit middleware/" |
| Hat metaphor | "wear the hat of the architect and review this design" |
| Lens framing | "from the data-viz perspective, how should this chart be encoded?" |
| Verb-led role assignment | "have the copywriter rewrite this paragraph" |

**Do NOT trigger when:**

- The task could conceivably benefit from a role lens but doesn't ask for one (e.g., "audit middleware/" alone — that's a normal task, let other skills handle it).
- The user wants multiple perspectives discussed before deciding → route to `team-composer`.
- The user wants parallel workers → route to `sub-agent-coordinator`.

This skill is opt-in by deliberate signal, not by greedy keyword matching. Role taxonomies rot fastest when applied silently to tasks that didn't ask for them.

---

## Phase 1 — Pick the role

If the user named a role explicitly (`@role` tag), use it. Skip to Phase 2.

Otherwise, run auto-pick against `references/auto-pick-heuristic.md`. There are exactly **four possible outcomes**:

### Outcome A — Clean match (one strong candidate)

Most clear-signal tasks land here: "security audit", "encode this chart", "name this product", "accessibility review".

**Action:** pick the role, do a 1-line disclosure, proceed.

> Wearing `@security_specialist`'s hat for this audit.

### Outcome B — Multi-candidate (2–3 plausible roles, none dominant)

Real ambiguity. Example: "review this code" could fit `@lead_software_engineer`, `@senior_software_architect`, or `@security_specialist` depending on what kind of review.

**Action:** present 2–3 candidates with one-line rationale each, ask the user to pick.

> Auto-pick is ambiguous. Best candidates:
> - `@lead_software_engineer` — for general code-quality review (readability, patterns)
> - `@senior_software_architect` — for architectural review (boundaries, scalability)
> - `@security_specialist` — for security-focused review (threats, vulnerabilities)
>
> Pick one, or specify another from `team-composer/references/role-personas.md`.

### Outcome C — Multi-role task (3+ candidates all materially needed)

The task intrinsically needs more than one role's work. Example: "create an HTML slide deck from <source URL>" needs HTML construction + content extraction + narrative structure.

**Action:** stop. Present the multi-role nature, offer best single-role escape, AND offer an explicit hand-off to `team-composer`. Never silently pick one role.

> **Multi-role task detected.** Creating an HTML slide deck spans HTML construction, content extraction, and narrative structure. wear-the-hat needs one role. Three options:
>
> 1. Proceed solo as `@senior_frontend_engineer` (HTML construction focus)
> 2. Proceed solo as `@senior_copywriter` (content + narrative focus)
> 3. Hand off to `team-composer` for a multi-role panel that produces a synthesized deliverable. wear-the-hat will invoke it with this task; I won't stay engaged.
>
> Pick 1, 2, or 3. (Or cancel and rethink.)

If the user picks 3, invoke `team-composer` with the same task brief and exit. Do not stay engaged across the panel discussion — `team-composer` owns it from there.

### Outcome D — No match (auto-pick yields zero candidates)

Task verb doesn't match any keyword in the heuristic. Example: a generic "help me with this" with no domain signal.

**Action:** default to `@lead_software_engineer` for coding work, `@senior_product_manager` for generic non-coding, with disclosure.

> Couldn't auto-pick a specialized role. Defaulting to `@lead_software_engineer`. If you wanted a different lens, name it: `as @<role>`.

---

## Phase 2 — Load persona

Once the role is picked, read its block from `team-composer/references/role-personas.md`. Extract **only these fields:**

- **Perspective** — the lens the role applies
- **Signature phrases** — characteristic vocabulary, framings, questions they ask

**Explicitly NOT loaded:** blind spots, natural biases, tensions with other roles. The skill embodies what's useful from the persona; it does not enforce the role's weaknesses on the work. (A `@senior_product_manager` is biased toward "ship fast" — wear-the-hat does not propagate that bias; it just applies the perspective and uses the vocabulary.)

If the role's block in `role-personas.md` is missing or malformed, fall back to using the role name + the user's task description, and disclose: "Couldn't load `@<role>`'s full persona; proceeding with role name only."

---

## Phase 3 — Mode selection (inline vs sub-agent)

Decide whether the orchestrator does the work itself (inline) or hands off to a sub-agent. See `references/mode-selection.md` for the full decision tree. Summary:

| Task characteristic | Mode |
|---|---|
| Short analytical task, single-paragraph response in role's voice | inline |
| Hits `sub-agent-coordinator`'s spawning signals (3+ files, iterative debug, >2 min, etc.) | sub-agent |
| Read-heavy investigation that needs isolation | sub-agent |
| Live conversation that needs full orchestrator context | inline |

**Announce the mode pick** in the 1-line disclosure:

> Wearing `@security_specialist`'s hat (sub-agent mode — task hits 3+ files signal).

Or:

> Wearing `@dataviz_engineer`'s hat (inline mode — single-encoding question).

---

## Phase 4 — Execute

### Inline mode

Respond in the role's voice. Apply the role's perspective explicitly — cite the lens when relevant ("from a security perspective…", "as the architect would frame this…"). Use the signature phrases naturally, not as obvious tags.

Stay in role until the task is complete. After the work, the orchestrator returns to its own voice (no need to mark the transition — context makes it clear).

### Sub-agent mode

Produce a brief shape that `sub-agent-coordinator` consumes. Use its Full Brief template, with the `Role:` field tagged and a `Persona context:` block populated from the loaded persona. Example:

```
Task: audit middleware/ for missing CSRF guards
Scope:
  - middleware/auth.ts
  - middleware/csrf.ts
  Out of scope: middleware/logging.ts
Done when:
  ✅ All POST endpoints have CSRF token validation
  ✅ Findings logged with severity per OWASP
  ✅ Quality gates pass

Constraints:
  - Tool budget: ~20 calls
  - Model selection (inherit if omitted): Tier=standard, Thinking=optional
  - Role: @security_specialist
  - Persona context:
      Perspective: System integrity and security boundaries
      Signature phrases:
        - "What's the threat model here?"
        - "How does an attacker exploit this?"
        - "We need defense in depth."
```

Hand off to `sub-agent-coordinator`'s protocol from there. Do not duplicate any of its spawning, briefing-template, or coordination logic — defer to that skill.

---

## What this skill is NOT

- **Not a panel.** One role per invocation. For multi-role discussion, use `team-composer`.
- **Not a worker fan-out.** One brief, one role. For parallel workers, use `sub-agent-coordinator`.
- **Not a role taxonomy.** The catalog lives in `team-composer/references/role-personas.md`. This skill consumes it; it does not extend or fork it.
- **Not an enforcement of bias.** Persona perspective + signature phrases load; blind spots and biases do not. The skill applies what's useful, not what's authentic-but-counterproductive.
- **Not silent.** Every pick (auto or explicit) gets a 1-line disclosure. Every mode choice gets announced. Multi-role tasks stop and ask.

---

## Slash invocation

Slash command works as a fallback when natural-language triggers don't fire:

```
/agent-skills:wear-the-hat <task>
/agent-skills:wear-the-hat as @security_specialist <task>
/agent-skills:wear-the-hat audit middleware/ for missing CSRF guards
```

Equivalent to the natural-language form, just unambiguous.

---

## Cross-skill integration

| Skill | Relationship |
|---|---|
| `team-composer` | Owns the role catalog (`references/role-personas.md`). wear-the-hat consumes it. For multi-role panel discussion, route to team-composer directly. |
| `sub-agent-coordinator` | Owns sub-agent spawning, briefing templates, model-selection axes, picking-the-role guidance. wear-the-hat's sub-agent mode hands off to coordinator's protocol — no duplication. |
| `coding-rules` | Lists wear-the-hat in its Companion skills callout. For coding-task role embodiment, the two compose: coding-rules sets the engineering discipline; wear-the-hat applies the lens. |

---

## Status

v0.1 — new skill. Catalog lives in `team-composer` until a fourth consumer emerges or the catalog moves to a shared location. The auto-pick heuristic is a small keyword/verb table (~25–30 rows), not an ML classifier — calibrate by editing `references/auto-pick-heuristic.md`.
