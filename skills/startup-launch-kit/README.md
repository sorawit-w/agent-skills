<p align="center">
  <em>startup-launch-kit — opt-in orchestrator that sequences the five-step startup pipeline with shared state, never bypassing any gate.</em>
</p>

# startup-launch-kit

Opt-in umbrella orchestrator for the five-step startup pipeline:

```
brand-workshop ─▶ validation-canvas ─▶ riskiest-assumption-test ─▶ pitch-deck ─▶ startup-grill
```

This skill is **convenience, not replacement**. Every individual pipeline skill remains independently invocable. The orchestrator's job is *sequencing + state*, not content — it calls each skill in turn via the Skill tool, manages a thin `kit-manifest.json` state journal, and never bypasses any of the gates each skill enforces.

The pipeline philosophy from v2.0.0 stays intact: *sequential teaches iteration*. The orchestrator preserves that lesson by surfacing every step's prompts to the founder, recording every gate override with a reason, and surfacing loop-back recommendations after RAT or grill — without auto-routing.

## What it does

- **Sequences the five pipeline skills** in order (`brand-workshop` → `validation-canvas` → `riskiest-assumption-test` → `pitch-deck` → `startup-grill`) via the Skill tool. Each skill runs as itself; founder sees the same UX as direct invocation.
- **Manages `kit-manifest.json`** at the working-directory root — a thin state journal: completed steps, mtimes, gate-override flags with reason+timestamp, founder-intake-answers cache. Atomic writes; versioned schema.
- **Asks the 3-question intake once** at pipeline start (founding history × domain × customer-segment experience), writes answers to manifest, and lets downstream skills read the cache and offer confirm/update rather than re-asking blind.
- **Honors every gate.** When a downstream skill STOPs (e.g., pitch-deck refuses to ship without populated RAT Results), the orchestrator surfaces the STOP message and pauses. It never silently bypasses.
- **Records gate overrides** with founder reason + timestamp + acknowledgment flag. Overrides honored on resume; surfaced in `startup-grill`'s `## Iteration Evidence` section as signals worth probing.
- **Surfaces loop-back recommendations** after RAT Results or grill kill-report identify invalidated assumptions or canvas-block weaknesses. Founder decides; orchestrator never auto-routes.
- **Resumes gracefully** from manual or partial runs. If you ran `brand-workshop` + `validation-canvas` manually then invoke the orchestrator, it absorbs the existing artifacts into the manifest and resumes at the next pending step.
- **Final summary** when all five steps complete: artifact list, gate-override log, iteration count, time-elapsed, terminal-verdict pointer.

## What it doesn't do

- **Replace any pipeline skill.** Every individual skill is fully invocable directly without the orchestrator. The orchestrator depends on the skills; the skills do not depend on the orchestrator.
- **Bypass gates.** Silent bypass is forbidden. Overrides require explicit founder acknowledgment + reason recorded in the manifest.
- **Batch.** Each pipeline skill surfaces its own prompts to the founder. The orchestrator does not collect intake up front and auto-feed each skill — that would defeat the discipline of each step.
- **Auto-route loop-back.** When invalidated assumptions or canvas weaknesses surface, the orchestrator recommends; the founder decides. Loop-back stays founder-driven.
- **Re-implement content.** The orchestrator never grep-parses heading anchors that called skills own. It reads only the manifest's structured fields.
- **Run partial / custom pipelines** in v2.1.0. Subset-pipeline support (e.g., "just brand + canvas") is deferred. Use the individual skills directly for partial work.
- **Multi-directory composition.** v2.1.0 assumes a single working directory for the whole pipeline.
- **Teach the pipeline conceptually.** Use `team-composer` with `@startup_strategist` for "which validation method should I use?" questions.

## When to use it

- You're starting a new idea from scratch and want end-to-end coordination through brand → validation → testing → pitch → grill.
- You're resuming a prior pipeline session (manifest already exists from an earlier orchestrator run).
- You ran a couple of pipeline skills manually and now want the orchestrator to absorb the existing artifacts and continue from where you left off.
- Investor or advisor asked you to "show me your full validation work" and you want one coherent artifact set produced through one consistent state-tracked flow.

## When to use something else

- **Single step (named explicitly)** → use that skill directly. "Just my canvas" → `validation-canvas`. "Rework my deck slide 5" → `pitch-deck`. "Grill my idea" → `startup-grill`.
- **Within-skill iteration** → the same skill in update mode. "Update my UVP block" → re-invoke `validation-canvas` directly.
- **Pipeline-strategy discussion** → `team-composer` with `@startup_strategist`.
- **Partial / custom pipeline** (e.g., brand + canvas only, no testing yet) → use the individual skills directly. Subset-pipeline orchestration is deferred from v2.1.0.

## How it works

Four phases, one Claude session (which may be paused and resumed across multiple sessions thanks to the manifest).

**Phase 0 — STOP gate + manifest discovery.** Routes single-step requests to the named skill. Then looks for `kit-manifest.json`; if absent, fresh start; if present, reconciles against filesystem per [`references/state-detection.md`](references/state-detection.md).

**Phase 1 — Intake.** Three calibration questions (same as `validation-canvas` Phase 0). Writes answers to manifest's `intake_answers` cache. Skipped on resume if cache is populated and the founder confirms it's still accurate.

**Phase 2 — Sequence execution.** For each of the 5 pipeline skills in order: check manifest entry → invoke skill via Skill tool → wait for completion → read updated manifest → enforce downstream gate → advance. Gates that STOP pause the orchestrator until the founder resolves manually or accepts an explicit override.

**Phase 3 — Loop-back surfacing.** After RAT or grill, scan for invalidated hypotheses or canvas-block weaknesses. Surface a one-line recommendation to re-invoke `validation-canvas` in update mode. Founder decides.

**Phase 4 — Final summary.** When all steps `completed` and no pending loop-backs, ship the summary table and point to `grill/kill-report.md` as the terminal verdict.

## What the output looks like

```
<your-working-folder>/
├── kit-manifest.json           ← orchestrator's state journal (NEW in v2.1.0)
├── brand-kit/                  ← from brand-workshop
├── validation-canvas.{md,html} ← from validation-canvas
├── rat/                        ← from riskiest-assumption-test
├── pitch/                      ← from pitch-deck
└── grill/                      ← from startup-grill
```

The orchestrator produces only `kit-manifest.json`. Every other artifact is produced by the called skills exactly as if they had been invoked manually.

## Manifest example

See [`references/manifest-schema.md`](references/manifest-schema.md) for the full schema and three worked examples (fresh start, mid-pipeline blocked-on-gate, complete-with-overrides).

```json
{
  "manifest_version": 1,
  "created": "2026-05-04T17:30:00Z",
  "updated": "2026-05-08T14:22:00Z",
  "intake_answers": {
    "founding_history": "yes-with-revenue",
    "domain_experience": "no",
    "customer_segment_experience": "yes",
    "inferred_mode": "focused"
  },
  "steps": [
    { "skill": "brand-workshop",          "status": "completed", "mtime": "2026-05-04T18:45:00Z", "iterations": 1 },
    { "skill": "validation-canvas",       "status": "completed", "mtime": "2026-05-06T11:20:00Z", "iterations": 2 },
    { "skill": "riskiest-assumption-test", "status": "completed", "mtime": "2026-05-07T09:15:00Z", "iterations": 1 },
    { "skill": "pitch-deck",              "status": "completed", "mtime": "2026-05-08T13:50:00Z", "iterations": 1 },
    { "skill": "startup-grill",           "status": "completed", "mtime": "2026-05-08T14:22:00Z", "iterations": 1 }
  ],
  "gate_overrides": []
}
```

## Pipeline philosophy preservation

The folder-contract from v2.0.0 explicitly stated: *"There is no one-shot orchestrator skill that runs the whole pipeline. This is intentional — sequential teaches the right mental model."* The v2.1.0 orchestrator preserves that lesson by:

- **Surfacing every step's prompts** — no batching, no silent automation. The founder sees the canvas interview, the RAT method selection, the slide-by-slide pitch construction, the grill panel — exactly as if invoked directly.
- **Honoring every gate** — the medium gate (canvas → RAT), the heavy gate (RAT → pitch-deck), and the iteration-evidence check (grill) all run normally. The orchestrator can pause on a STOP but cannot bypass.
- **Recording every override** — when a founder accepts a gate override (e.g., `[PRE-VALIDATION DRAFT]` for pitch-deck without populated RAT Results), the override goes into `gate_overrides[]` with reason + timestamp + acknowledgment. This makes overrides visible later (especially to `startup-grill`'s iteration-evidence check) instead of invisible silent bypasses.
- **Keeping loop-back founder-driven** — invalidated assumptions trigger recommendations, not auto-routing. The founder still does the deciding, which is where the validation lesson lives.

The orchestrator is convenience for sequencing the steps. The pipeline still teaches iteration; the orchestrator just removes the manual chaining overhead.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install startup-launch-kit@sorawit-w
```

The orchestrator depends on the five pipeline skills also being installed (they are part of the same `agent-skills` plugin bundle, so a single install covers all six).

## Related skills

- **[`brand-workshop`](../brand-workshop/README.md)** — Step 1 of the pipeline; called by the orchestrator. Independently invocable.
- **[`validation-canvas`](../validation-canvas/README.md)** — Step 2; called by the orchestrator. Independently invocable.
- **[`riskiest-assumption-test`](../riskiest-assumption-test/README.md)** — Step 3; called by the orchestrator. Independently invocable.
- **[`pitch-deck`](../pitch-deck/README.md)** — Step 4; called by the orchestrator. Independently invocable.
- **[`startup-grill`](../startup-grill/README.md)** — Step 5; called by the orchestrator. Independently invocable.
- **[`team-composer`](../team-composer/README.md)** — alternative to the orchestrator for pipeline-strategy discussions, single-block deep dives, or work that doesn't fit the pipeline shape.

## Status and scope

**v2.1.0 (initial release).**

**Supported:**
- End-to-end orchestration of the five-step pipeline
- Resume from prior orchestrator runs (manifest exists)
- Resume from manual partial runs (manifest absent; orchestrator absorbs existing artifacts)
- Gate overrides with reason + timestamp + acknowledgment recording
- Loop-back recommendations after RAT or grill
- Single working directory

**Not supported (deferred to v2.2.0+):**
- Subset / custom pipelines (e.g., "just brand + canvas")
- Manifest query API ("what state am I in?" introspection from outside the orchestrator)
- Multi-directory composition
- Maurya 1st-edition addendum for catalog comparison
- Auto-routing of loop-back actions
