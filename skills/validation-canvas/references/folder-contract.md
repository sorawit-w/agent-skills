# Folder Contract — Reference

Shared folder conventions across the **startup pipeline plugins**:
`brand-workshop`, `validation-canvas` (this skill),
`riskiest-assumption-test`, `pitch-deck`, and `startup-grill`. Each plugin
works independently, but when run in the same working directory they compose
via these paths.

## Canonical paths

```
<founder-working-directory>/
├── brand-kit/                       # produced by brand-workshop
│   ├── brand-brief.md               # contains `## Positioning` + `## Voice & Tone`
│   ├── descriptions.md              # tagline + bios (pitch-deck reads tagline)
│   ├── design-system.md             # tokens (validation-canvas + pitch-deck read)
│   ├── logos/
│   ├── favicons/
│   └── social/
│
├── validation-canvas.md             # produced by validation-canvas (this skill)
├── validation-canvas.html           # produced by validation-canvas (this skill)
│
├── rat/                             # produced by riskiest-assumption-test
│   ├── assumption-test-plan.md      # contains `## Top 3 Hypotheses`, `## Test Plan`, `## Results`
│   └── test-matrix.html             # interactive risk × impact matrix
│
├── pitch/                           # produced by pitch-deck
│   ├── deck.html
│   ├── speaker-notes.md
│   └── deck-checklist.md
│
└── grill/                           # produced by startup-grill
    ├── kill-report.md               # includes `## Iteration Evidence` section
    └── defense-log.md               # append-only, only created if interactive defense entered
```

## Read-before-write rule

When `validation-canvas` runs:

1. **Check for `brand-kit/design-system.md`.** If present, read the color
   tokens and font stack, and apply them to `validation-canvas.html` via the
   `:root` CSS custom properties (see `canvas-html-template.md`).
2. **Check for an existing `validation-canvas.md`.** If present, read it
   first — treat the interview as an *update*, not a rewrite. Surface changes
   explicitly to the founder ("You previously said X; we're now changing that
   to Y — confirm?"). See "Loop-back protocol" below.
3. **Check for `rat/assumption-test-plan.md`.** If present and `## Results`
   is populated with at least one invalidated hypothesis, the founder is
   probably looping back. Surface this proactively: *"Your last RAT run
   invalidated [hypothesis] — that points to the [block] block. Update just
   that block, or re-run the full canvas?"*
4. **Never overwrite `brand-kit/*`, `rat/*`, `pitch/*`, or `grill/*`.** Those
   files belong to other plugins. If the founder asks to change a color,
   route them back to `brand-workshop`. If they want to update a hypothesis,
   route to `riskiest-assumption-test`.

## Write rule

- Write to the founder's working directory, not a scratch folder.
- Never write outside the canonical paths.
- If the working directory contains files unrelated to this plugin (code,
  unrelated docs), don't touch them — the folder is shared, not owned.

---

## Pipeline gate weights

The pipeline is sequential by default. Each step's Phase 0 enforces a gate
on its upstream artifact, with weighted rigor:

| From | To | Gate | Enforcement |
|---|---|---|---|
| (start) | `brand-workshop` | none | Always invocable |
| `brand-workshop` | `validation-canvas` | **light** | brand-workshop's last phase suggests running `validation-canvas` next; not enforced |
| `validation-canvas` | `riskiest-assumption-test` | **medium** | RAT's Phase 0 STOPs without `validation-canvas.md` and routes back |
| `riskiest-assumption-test` | `pitch-deck` | **heavy** | pitch-deck's Phase 0 STOPs without `rat/assumption-test-plan.md` having populated `## Results`. Override available with `[PRE-VALIDATION DRAFT]` watermark |
| `pitch-deck` | `startup-grill` | **light** | Grill works on minimum input (one-pager); just enriched by full pipeline |

There is **no one-shot orchestrator skill** that runs the whole pipeline.
This is intentional — sequential, one-step-at-a-time execution teaches the
right mental model (validation is iterative, not a checklist).

---

## Loop-back protocol (first-class, not a failure mode)

The pipeline is **iterative**. Loop-back happens normally, especially after
RAT or startup-grill surfaces an invalidated assumption.

### When loop-back is triggered

- **From `riskiest-assumption-test`:** any top-3 hypothesis fails. RAT's
  Phase 5 instructs the founder: *"Return to `validation-canvas`, mark the
  affected blocks as updated, decide pivot vs. persevere. Do not advance to
  pitch-deck with invalidated core assumptions."*
- **From `startup-grill`:** kill-report's "Lethal & Fixable" or "Material &
  Fixable" sections name a weakness rooted in a canvas block. Founder is
  routed back to update that block.
- **From the founder directly:** they want to revise the canvas without a
  downstream signal.

### How to apply loop-back

When `validation-canvas` is invoked and `validation-canvas.md` already exists:

1. **Do NOT overwrite untouched blocks.** Read the existing file first.
   Identify which blocks the founder (or downstream signal) wants to change.
2. **Confirm the scope of update in one line:** *"Updating just the
   [block] based on [signal]. Other blocks stay frozen — say so if you want
   me to revisit them too."*
3. **Re-run the relevant section of Phase 1 + Phase 2** for changed blocks
   only. Apply mode-appropriate rigor (compressed-with-challenge gets
   push-back on glib revisions; first-timers get the full block-redo flow).
4. **Re-run the consistency checks** that touch changed blocks. (E.g.,
   changing the Customer Segments block forces re-checking Problem ↔
   Customer Segments and Channel ↔ Customer Segments.)
5. **Mark the change visibly.** Output canvas shows updated blocks marked
   with an HTML comment: `<!-- updated YYYY-MM-DD: invalidated by RAT
   hypothesis #2 (per-seat pricing failed) -->`.
6. **Update the Stress Tests section** to reflect what's been learned —
   often a previously listed assumption is now confirmed or invalidated and
   should be removed or rewritten.

### What loop-back is NOT

- **Not a rewrite.** Don't regenerate the whole canvas just because one
  block changed.
- **Not a failure.** A founder iterating on the canvas after testing
  assumptions is using the pipeline correctly. Pristine pipelines (no
  iteration) are the actual yellow flag — `startup-grill` checks for that.
- **Not silent.** Always surface what's changing and why, so the founder can
  steer.

---

## Manifest (deferred)

A `kit-manifest.json` at the working-directory root is planned for a future
`startup-launch-kit` orchestrator. Not implemented in v2 — folder
conventions are enough. If/when the manifest ships, each plugin will:

- Read it at start, if present, to discover which artifacts exist.
- Append/update its own entry after writing, if the manifest is present.
- Not create the manifest if it doesn't exist (that's the orchestrator's
  job).

A few lines of defensive read-if-present code keeps forward compatibility
cheap.
