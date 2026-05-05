# Folder Contract — Reference

Shared folder conventions across the **startup pipeline plugins**:
`brand-workshop`, `validation-canvas` (this skill),
`riskiest-assumption-test`, `pitch-deck`, and `startup-grill`. Each plugin
works independently, but when run in the same working directory they compose
via these paths.

## Canonical layout (v2.2.0+)

Artifacts go under `docs/` in the founder's working directory. Two layouts:

- **Solo** (skill invoked directly): `docs/<skill>/`
- **Orchestrated** (via `startup-launch-kit`): `docs/startup-kit/<skill>/`

Folder names per skill: `brand/`, `canvas/`, `rat/`, `pitch/`, `grill/`.
Per-skill artifact files keep their canonical names (e.g.,
`validation-canvas.md`, `assumption-test-plan.md`, `deck.html`).

Each pipeline skill resolves its own root in Step 0.0 of its Phase 0 with
this precedence chain:

1. Explicit `output_dir` arg passed by the orchestrator
2. `STARTUP_KIT_DOCS_ROOT` env var (e.g., `${STARTUP_KIT_DOCS_ROOT}/<skill>/`)
3. Smart default — if `docs/startup-kit/` exists, write to
   `docs/startup-kit/<skill>/` (with a one-line notice)
4. Solo fallback: `docs/<skill>/`

v1 layouts (artifacts at cwd root) are supported as backward-compat read
fallbacks indefinitely.

## Read-before-write rule

When `validation-canvas` runs:

1. **Check for the brand artifact.** Look at
   `<brand-root>/DESIGN.md` (sibling of this skill's canvas root). If present,
   read the color tokens and font stack from the YAML front matter and apply
   them to `validation-canvas.html` via the `:root` CSS custom properties
   (see `canvas-html-template.md`). Extract `colors.primary` from the YAML to
   bind to `--canvas-accent`.
2. **Check for an existing `validation-canvas.md`.** Look at
   `<canvas-root>/validation-canvas.md` first; fall back to cwd-relative
   `validation-canvas.md`. If present, read it first — treat the interview
   as an *update*, not a rewrite. Surface changes explicitly to the founder
   ("You previously said X; we're now changing that to Y — confirm?"). See
   "Loop-back protocol" below.
3. **Check for the assumption-test plan.** Look at
   `<rat-root>/assumption-test-plan.md` first; fall back to legacy
   `rat/assumption-test-plan.md`. If present and `## Results` is populated
   with at least one invalidated hypothesis, the founder is probably looping
   back. Surface this proactively: *"Your last RAT run invalidated
   [hypothesis] — that points to the [block] block. Update just that block,
   or re-run the full canvas?"*
4. **Never overwrite sibling skills' artifacts.** Files under
   `<brand-root>/`, `<rat-root>/`, `<pitch-root>/`, `<grill-root>/` (or
   their legacy fallbacks) belong to other plugins. If the founder asks to
   change a color, route them back to `brand-workshop`. If they want to
   update a hypothesis, route to `riskiest-assumption-test`.

## Write rule

- Write to the resolved canvas folder per the precedence chain above.
  Never to cwd root in v2.2.0+.
- Never write outside the canonical paths (canvas root only).
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
| `validation-canvas` | `riskiest-assumption-test` | **medium** | RAT's Phase 0 STOPs without the validation canvas (`<canvas-root>/validation-canvas.md` or legacy `validation-canvas.md`) and routes back |
| `riskiest-assumption-test` | `pitch-deck` | **heavy** | pitch-deck's Phase 0 STOPs without the assumption-test plan (`<rat-root>/assumption-test-plan.md` or legacy `rat/assumption-test-plan.md`) having populated `## Results`. Override available with `[PRE-VALIDATION DRAFT]` watermark |
| `pitch-deck` | `startup-grill` | **light** | Grill works on minimum input (one-pager); just enriched by full pipeline |

As of v2.1.0, the **`startup-launch-kit`** skill is an *opt-in*
orchestrator that sequences the five steps with shared state via a manifest
at `<kit-root>/kit-manifest.json` (default `docs/startup-kit/kit-manifest.json`
in v2.2.0+, with legacy fallback to `./kit-manifest.json` for backward
compat). It is convenience, not replacement: every individual skill remains
independently invocable, the orchestrator never bypasses any gate, and every
step still surfaces its own prompts to the founder (no batching). The
pipeline philosophy — *sequential teaches iteration* — is preserved by the
orchestrator's design (gates honored, overrides recorded with reason,
loop-back stays founder-driven). See
[`../../startup-launch-kit/SKILL.md`](../../startup-launch-kit/SKILL.md)
for the orchestrator and
[`../../startup-launch-kit/references/manifest-schema.md`](../../startup-launch-kit/references/manifest-schema.md)
for the manifest schema.

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

## Manifest (v2.1.0+, path moved in v2.2.0)

`kit-manifest.json` is the orchestrator's state journal. As of v2.2.0+ it
lives at `<kit-root>/kit-manifest.json` (default
`docs/startup-kit/kit-manifest.json`). v1 layouts had it at the
working-directory root; that legacy path is still supported as a
backward-compat fallback when reading.

Each pipeline skill is **manifest-aware** as of v2.1.0:

- Read the manifest at start, if present, to discover which artifacts
  exist and what intake answers are cached.
- Append/update this skill's entry after writing artifacts. Use atomic
  write (write `.tmp`, then rename).
- Do **NOT** create the manifest if it doesn't exist — that's the
  orchestrator's (`startup-launch-kit`'s) job.
- Treat manifest entries as *hints*, never as bypasses. Each skill's
  Phase 0 still runs in full; the manifest provides defaults the founder
  can confirm or update.
- Manifest read failures (corrupt JSON, missing fields) are non-fatal —
  log inline and proceed as if no manifest exists.

See [`../../startup-launch-kit/references/manifest-schema.md`](../../startup-launch-kit/references/manifest-schema.md)
for the full schema and worked examples,
[`../../startup-launch-kit/references/state-detection.md`](../../startup-launch-kit/references/state-detection.md)
for the manifest-vs-filesystem reconciliation rules, and
[`../../startup-launch-kit/references/gate-override-protocol.md`](../../startup-launch-kit/references/gate-override-protocol.md)
for how gate overrides get recorded and audited.
