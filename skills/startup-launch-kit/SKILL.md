---
name: startup-launch-kit
description: Opt-in umbrella orchestrator that sequences the full five-step startup pipeline (`brand-workshop` → `validation-canvas` → `riskiest-assumption-test` → `pitch-deck` → `startup-grill`) with shared state via `kit-manifest.json`. **Every individual skill remains independently invocable** — this orchestrator is convenience, not replacement. It calls each pipeline skill in turn, never bypasses any of their gates, and surfaces every step's prompts to the founder (no batching, no silent automation). Records gate overrides with reasons; surfaces loop-back recommendations after RAT or grill but does not auto-route. Use whenever the user asks to "build my whole startup kit", "do the full pipeline", "end-to-end startup workflow", "orchestrate brand → canvas → tests → pitch → grill", "set up my whole launch", "I'm starting from scratch — take me through everything", "launch kit", "full validation pipeline", or asks Claude to coordinate the five startup-pipeline skills together. Triggers explicitly via `/startup-launch-kit` slash command. Does NOT trigger for single-step requests ("just the canvas", "build my deck") — those route to the named skill directly. Does NOT replace the pipeline philosophy that "sequential teaches iteration" — gates are honored, steps surface their own prompts, loop-back stays founder-driven.
---

# Startup Launch Kit

Opt-in orchestrator that sequences the five-step startup pipeline with state
tracking via `kit-manifest.json`. The orchestrator is convenience for founders
who want end-to-end coordination without manual step-chaining; it is **not** a
replacement for any individual skill, and it never bypasses the gates each
skill enforces.

The orchestrator's job is **sequencing + state**, not content. Each pipeline
skill runs as itself — same prompts, same outputs, same gates the founder
would see if they invoked the skill directly. The orchestrator just remembers
where the founder is, surfaces the next step, and records overrides for audit.

---

## STOP gate — When NOT to use this skill

Hand off to a different skill — do not run the orchestrator — if any of these
apply:

- **The user wants only one step**, named explicitly (e.g., "just build my
  validation canvas", "rework my pitch deck slide 5", "grill my idea") →
  route to the named skill directly. The orchestrator's value is end-to-end
  sequencing; running it for one step is overhead with no benefit.
- **The user is mid-step inside one skill**, asking for changes within that
  skill's scope (e.g., "update the UVP block", "re-rank the top-3
  hypotheses") → route to the same skill in update mode. The orchestrator
  doesn't add value to within-skill iterations.
- **The user wants to discuss the pipeline conceptually** ("which validation
  method should I use?", "explain how the gates work") → answer directly or
  route to `team-composer` with `@startup_strategist`. The orchestrator
  executes; it doesn't teach.
- **The user is grilling someone else's startup** (advisor / investor mode)
  → route to `startup-grill` directly. The orchestrator assumes the founder
  is building their own pipeline.

**Bright-line rule:** if the founder names a single pipeline skill they want
to invoke, route to that skill. The orchestrator only runs when the request
is genuinely end-to-end ("the whole pipeline", "everything from brand to
grill", "set up my launch kit"), or when the founder explicitly invokes
`/startup-launch-kit`.

---

## What this skill produces

The orchestrator does not produce its own content artifacts — it produces
**sequencing + state**. Specifically:

1. **`docs/startup-kit/kit-manifest.json`** — a thin JSON state journal:
   manifest version, current step, completed steps with mtimes,
   gate-override flags with reason+timestamp, founder-intake-answers cache.
   Atomic writes (write `.tmp`, then rename). The orchestrator creates the
   `docs/startup-kit/` folder if absent. See
   [`references/manifest-schema.md`](references/manifest-schema.md) for the
   schema and three worked examples.
2. **Sequenced invocations** of the five pipeline skills via the Skill tool.
   Each skill runs as itself with the founder seeing its normal prompts; the
   orchestrator merely calls them in order, gates the transitions, passes
   the per-skill `output_dir` (`docs/startup-kit/<skill>/`), and reads the
   manifest entries each skill writes after completing.
3. **A final-summary report** when all five steps complete: artifact list,
   gate-override log, iteration count, time-elapsed.

The orchestrator does NOT:
- Re-implement any skill's content (no canvas blocks, no test methods, no
  slide construction, no kill-report logic).
- Bypass any gate enforced by any pipeline skill.
- Batch multiple steps without surfacing each step's prompts.
- Auto-route loop-back actions (it surfaces recommendations; the founder
  decides).

---

## Phase 0: STOP gate + path resolution + manifest discovery

Apply the STOP-gate rules above first. If the request passes, then:

### Step 0.1 — Resolve the kit root

Resolve the kit root once at invocation, in this precedence order
(canonical chain):

1. **`STARTUP_KIT_DOCS_ROOT` env var** → `${STARTUP_KIT_DOCS_ROOT}/startup-kit/`
2. **Default** → `docs/startup-kit/`

The orchestrator passes `<kit_root>/<skill-folder>/` to each child skill as
its `output_dir` argument when invoking. Per-skill folder names
(`brand/`, `canvas/`, `rat/`, `pitch/`, `grill/`) are fixed by the
conventions doc.

If the kit root directory does not exist yet, create it before manifest
discovery (mkdir -p semantics).

### Step 0.2 — Manifest discovery

1. **Look for `kit-manifest.json`** at `<kit_root>/kit-manifest.json` first.
2. **Backward-compat fallback:** if absent, also check the
   working-directory root (`./kit-manifest.json`). If found at the legacy
   path, surface a one-line notice so the founder knows: *"Found legacy
   `kit-manifest.json` at repo root. To consolidate, `mv kit-manifest.json
   docs/startup-kit/` after this run."* Continue using the legacy location
   for this run; do NOT auto-move.
3. **If absent in both locations:** this is a fresh start. Create the
   manifest at `<kit_root>/kit-manifest.json` at the end of Phase 1 once
   intake answers are captured. Proceed to Phase 1.
4. **If present:** read it. Reconcile against the filesystem per
   [`references/state-detection.md`](references/state-detection.md):
   - Files exist that the manifest doesn't list → assume manual run; absorb
     into the manifest with `status: "completed"` and the file's mtime.
   - Manifest references files that don't exist → mark step as `failed`;
     recommend re-running that step.
   - Manifest's intake-answers cache exists → surface them and ask the
     founder to confirm or update before proceeding to Phase 2 (skip
     re-asking from scratch).

---

## Phase 1: Intake (once, written to manifest)

Run the **same three calibration questions** that
[`validation-canvas`](../validation-canvas/SKILL.md) Phase 0.1–0.3 asks:

1. *"Have you founded or co-founded a startup that reached paying customers
   before?"*
2. *"Is this idea in a domain you've worked in professionally?"*
3. *"Do you have direct experience with this customer segment?"*

Map the answers to a mode (Guided / Focused / Compressed-with-Challenge per
the same matrix as `validation-canvas`). Confirm the inferred mode in one
line. **Write the answers to the manifest's `intake_answers` cache.**

Note: this duplicates the question set in `validation-canvas` Phase 0
deliberately. The orchestrator asks at pipeline start so downstream skills
can read the cache and offer to confirm/update rather than re-asking blind.
The cache is a hint, not a bypass — `validation-canvas` Phase 0 still runs
in full, just with cached defaults.

If the manifest already had intake answers (resume path), present them and
offer confirm/update — do **NOT** silently re-use without confirmation. The
founder's experience may have changed; the manifest is a hint, not truth.

---

## Phase 2: Sequence execution

For each step in pipeline order — `brand-workshop`, `validation-canvas`,
`riskiest-assumption-test`, `pitch-deck`, `startup-grill` — do the following:

### Step 2.1 — Manifest check

Read the current manifest entry for this step:

- `status: "pending"` → fresh run; proceed to Step 2.2.
- `status: "completed"` → ask the founder: *"Already completed on [date].
  Update mode (re-run with prior artifacts), fresh run (rebuild from
  scratch), or skip to next step?"* Then proceed accordingly.
- `status: "blocked"` → the prior orchestrator run hit a gate STOP. Surface
  the blocker (`blocked_by`) and route the founder to resolve it (typically:
  re-run the upstream skill in update mode).
- `status: "failed"` → an artifact disappeared between runs. Recommend
  re-running this step.

### Step 2.2 — Invoke the skill

Use the Skill tool to invoke the pipeline skill by name (e.g.,
`Skill(brand-workshop)`). The orchestrator does **NOT** inline the skill's
content. The skill runs as itself, surfaces its own prompts to the founder
(intake questions, draft canvases, slide interviews, defense rounds), and
when it completes it writes its own manifest entry per the Phase A pattern
each pipeline skill carries.

The founder sees the same UX they would see invoking the skill directly. The
orchestrator's role is purely sequencing — call the skill, wait for it to
finish, read the updated manifest, decide what comes next.

### Step 2.3 — Gate enforcement

After the called skill completes, read its manifest entry. If the entry
records a downstream gate STOP (e.g., RAT Results empty for top-3
hypotheses → blocks pitch-deck), surface the STOP message verbatim and
**pause the orchestrator**. The founder can resolve the block manually
(re-run the upstream skill in update mode, fill in the missing data,
re-invoke the orchestrator) OR explicitly accept an override (recorded in
manifest per [`references/gate-override-protocol.md`](references/gate-override-protocol.md)).

The orchestrator **never** silently bypasses a gate. The whole point of
the orchestrator preserving the pipeline philosophy is that gates remain
visible and overrides remain audited.

### Step 2.4 — Move to the next step

Once gates are satisfied (or overridden with reason), advance to the next
pipeline step. Loop back to Step 2.1 with the new step's manifest entry.

---

## Phase 3: Loop-back surfacing

After RAT Results land OR after `startup-grill` ships its kill report, scan
for **invalidated hypotheses or canvas-block weaknesses**:

- **From RAT:** any top-3 hypothesis with `result: "invalidated"` in
  the assumption-test plan (`<kit-root>/rat/assumption-test-plan.md` or
  legacy `rat/assumption-test-plan.md`).
- **From grill:** any "Lethal & Fixable" or "Material & Fixable" weakness
  whose `Suggested attack` line names a canvas block.

If found, surface a **one-line recommendation** to the founder, not an
auto-route:

> *"Hypothesis #2 was invalidated (per-seat pricing failed). That points to
> the Revenue Streams block of your validation canvas. Re-invoke
> validation-canvas in update mode? (Y/n)"*

The founder decides. Loop-back stays founder-driven — the orchestrator
recommends, never executes a loop-back without explicit confirmation. This
preserves the "sequential teaches iteration" philosophy: the founder sees
that invalidation happens, and they choose to act on it.

---

## Phase 4: Final summary

When all five steps record `status: "completed"` AND no unresolved
loop-back recommendations remain, surface a final summary:

```markdown
## Startup Launch Kit — Complete

**Pipeline run summary**

| Step | Status | Iterations | Last updated |
|---|---|---|---|
| brand-workshop          | ✅ completed | 1 | YYYY-MM-DD |
| validation-canvas       | ✅ completed | 2 | YYYY-MM-DD |
| riskiest-assumption-test | ✅ completed | 1 | YYYY-MM-DD |
| pitch-deck              | ✅ completed | 1 | YYYY-MM-DD |
| startup-grill           | ✅ completed | 1 | YYYY-MM-DD |

**Artifacts produced (under `docs/startup-kit/`):**
- brand/ (logo, brief, design system, descriptions, banners)
- canvas/validation-canvas.md + .html
- rat/assumption-test-plan.md + test-matrix.html
- pitch/deck.html + speaker-notes.md + deck-checklist.md
- grill/kill-report.md

**Gate overrides recorded:** N (see docs/startup-kit/kit-manifest.json `gate_overrides[]`)

**Time elapsed:** [start] → [end]

**Terminal verdict:** see docs/startup-kit/grill/kill-report.md
```

Point the founder to `docs/startup-kit/grill/kill-report.md` as the
authoritative read on where the startup stands.

---

## Hard rules

1. **Independent invocability is sacred.** Every pipeline skill must work
   identically when invoked directly without the orchestrator. The
   orchestrator's edits to those skills (Phase A of v2.1.0) are additive
   manifest-awareness only; no skill depends on the orchestrator existing.

2. **Gates are never bypassed.** The orchestrator can advance past a STOP
   only via an explicit, recorded override in `gate_overrides[]` with a
   founder-acknowledgment flag. Silent bypass is forbidden.

3. **No batching.** Each pipeline skill surfaces its own prompts. The
   orchestrator does not collect all intake up front and then auto-feed
   each skill — that would defeat the value of each skill's discipline.

4. **Loop-back is founder-driven.** The orchestrator recommends; never
   executes a loop-back without explicit confirmation.

5. **Manifest is a hint, never truth.** When manifest disagrees with
   filesystem, the filesystem wins (real artifacts override stale manifest
   entries). When intake-cache disagrees with current founder state, ask.

6. **No content duplication.** The orchestrator never grep-parses heading
   anchors that the called skills own. It reads only the manifest's
   structured fields. If a downstream check needs content from an artifact
   (e.g., pitch-deck checking RAT Results), the downstream skill does that
   read — not the orchestrator.

7. **Single working directory, single kit root.** The orchestrator assumes
   one working directory for the whole pipeline AND a single kit root
   (`docs/startup-kit/` by default, or `${STARTUP_KIT_DOCS_ROOT}/startup-kit/`
   if the env var is set). The orchestrator passes the resolved per-skill
   `output_dir` to each child skill at invocation. Multi-directory
   composition (multiple startups in one repo) is out of scope; founders
   running multiple startups should use separate working directories.

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `brand-workshop` (our own) | Step 1 of the pipeline; orchestrator calls it. Independently invocable for brand-only work. |
| `validation-canvas` (our own) | Step 2; orchestrator calls it. Independently invocable for canvas-only work or update mode. |
| `riskiest-assumption-test` (our own) | Step 3; orchestrator calls it. Independently invocable for test design or results-update. |
| `pitch-deck` (our own) | Step 4; orchestrator calls it. Independently invocable for deck construction or single-slide rework. |
| `startup-grill` (our own) | Step 5; orchestrator calls it. Independently invocable for adversarial review at any stage. |
| `team-composer` (our own) | Use **instead of** the orchestrator for pipeline-strategy discussions, single-block deep dives, or naming/positioning workshops that don't fit the pipeline shape. |
| `theme-factory` (Anthropic) | Independent of the orchestrator; can be applied to any artifact for visual styling. |
| `pdf` (Anthropic) | Independent; for assembling the orchestrator's output artifacts into a board packet. |

**Principle:** the orchestrator owns sequencing, state, and gate-honoring.
Each pipeline skill owns its content and gate enforcement. No skill depends
on the orchestrator existing; the orchestrator depends on every pipeline
skill being manifest-aware (added in v2.1.0 Phase A).

**Graceful degradation:** if the runtime does not support invoking the
Skill tool from within a skill, fall back to instructional prose at each
step boundary: *"Now run `validation-canvas` — I'll wait for the artifact
to appear, then continue."* The orchestrator can still manage the manifest
and gate-checking even if direct skill invocation isn't available.
