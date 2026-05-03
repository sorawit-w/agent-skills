---
name: startup-grill
description: >
  Adversarially grill a startup idea or pitch with a panel of domain-aware probers
  (VC partner, growth marketer, founder strategist, UX researcher, plus a flexible
  technical-or-brand fifth seat and up to 3 domain specialists from team-composer's
  catalog), and ship a structured kill report ranked across two axes — severity
  (lethal vs material) and fixability (fixable vs unfixable).
  Use this skill when the user says: "grill my startup", "grill this idea",
  "stress-test my pitch", "pressure-test my idea", "roast my pitch", "rip apart
  this", "tear apart my deck", "kill my idea", "pre-mortem my startup", "find the
  weaknesses in my idea", "what would kill this startup", "what would a VC hate
  about this", "give me brutal feedback on my deck", "be ruthless about this idea",
  "where would this fail", "is this fundable", "investability check", or uploads a
  one-pager / validation-canvas.md / RAT plan / pitch deck and asks for adversarial
  review.
  Use this skill — NOT `team-composer` — whenever the user wants an *adversarial*
  review with a *verdict* (Investable / Pivot / Pass), even if they use the word
  "review". `team-composer`'s "review" mode is collaborative and constructive;
  this skill's mode is probing and decisive. If the user says "review my startup
  adversarially", "review with VC eyes", "stress-test my business model", or
  similar, use this skill, not team-composer.
  Default to one-shot mode (panel probes → forced steelman defense → verdict →
  kill report). After the report ships, offer interactive defense mode where the
  founder can defend a specific weakness with new evidence and the relevant
  panelists re-probe that line item.
  Composes downstream of `validation-canvas`, `riskiest-assumption-test`, and
  `pitch-deck` — reads their outputs as input artifacts when present. Includes
  an iteration-evidence check that yellow-flags pristine pipelines (canvas not
  updated after RAT). Do NOT use this skill for collaborative brainstorming,
  positioning workshops, canvas construction, assumption test design, or
  pitch-deck building — those route to `team-composer`, `validation-canvas`,
  `riskiest-assumption-test`, and `pitch-deck` respectively.
---

# Startup Grill

Adversarially probe a startup idea with a panel of domain-aware grillers. Ship a
structured kill report. Optionally enter interactive defense mode.

This skill is **not** a collaborative thinking partner. The job is to surface
what would kill this startup if unaddressed — not to shape the idea, not to
brainstorm next moves, not to be encouraging. If you want collaborative work,
use `team-composer` instead.

---

## STOP — When NOT to use this skill

Hand off to a different skill — do not run the grill — if any of these apply:

- The user is **brainstorming** an idea or shaping a problem space → use
  `team-composer` (or `superpowers:brainstorming` if installed).
- The user wants to **build** a validation canvas, brand identity, or pitch deck
  → use `validation-canvas`, `brand-workshop`, or `pitch-deck` respectively.
  Grilling can run *after* those exist.
- The user wants to **design assumption tests** → use
  `riskiest-assumption-test`. Grilling exposes weaknesses; RAT designs
  experiments to test them.
- The user wants **positioning review** or **brand voice review** → use
  `team-composer` with `@brand_strategist` / `@humorist` / `@senior_copywriter`.
- The user wants to **review their plan** with a multi-perspective team that
  includes constructive feedback → use `team-composer` with `scope=review`.
- The user is mid-deal and wants **investor diligence prep** rather than
  adversarial idea review → use `team-composer` with
  `@vc_partner` + `@finance_manager` + `@startup_strategist`.

**Bright-line rule:** if the user wants help making the idea *better*, that's
not this skill. Grilling produces a verdict, not improvements. Improvements
come from the user acting on the kill report's `Suggested attack` lines, then
optionally re-grilling.

**Redirect discipline.** When the STOP gate fires and you route to another
skill, describe the *kind of lens* the user needs — don't invent role tags.
`team-composer`'s persona catalog lives in
`skills/team-composer/references/role-personas.md`; defer naming specific
roles to that skill rather than coining tags that don't exist there
(e.g., do NOT write `@market_researcher` or `@sustainability_expert` —
those aren't in the canonical catalog and will confuse the user when
team-composer assembles its actual team).

---

## Skill Boundaries

This skill overlaps with `team-composer` (`@vc_partner`, `@startup_strategist`,
and `@ux_researcher` are all team-composer roles too) but the deliverable and
the round structure are different.

| Request | Skill |
|---|---|
| "Grill my startup idea" | `startup-grill` (this skill) |
| "Tear apart my pitch" | `startup-grill` |
| "Pre-mortem this startup" | `startup-grill` |
| "Stress-test my business model" | `startup-grill` |
| "Brainstorm my startup" | `team-composer` |
| "Review my plan with a team" | `team-composer` with `scope=review` |
| "Build my pitch deck" | `pitch-deck` |
| "Build my validation canvas / lean canvas / VPC" | `validation-canvas` |
| "Design tests for my assumptions" | `riskiest-assumption-test` |
| "Workshop the brand for my startup" | `brand-workshop` |

If the user request mixes grilling with building ("grill my startup *and*
help me fix it"), run the grill first to ship the kill report, then route the
fix work to the appropriate builder skill (`pitch-deck`, `validation-canvas`,
`riskiest-assumption-test`, or `team-composer`). Don't try to do both at once —
that produces a soft kill report.

---

## What this skill produces

Every one-shot run produces exactly **one file**:

- **`grill/kill-report.md`** — the structured kill report. Format spec in
  `references/kill-report.md`.

If the founder enters interactive defense mode, a second file is produced
and updated on each defense round:

- **`grill/defense-log.md`** — append-only log of founder defenses, panel
  re-probes, and updated reads. Format spec in `references/round-structure.md`.

Both files go into `grill/` inside the founder's working directory. Existing
files from prior sessions are appended-to, never overwritten.

---

## Phase 1: Intake

**Goal:** assemble the brief the panel will grill.

### Step 0.0 — Manifest awareness (optional, v2.1.0+)

If `kit-manifest.json` exists in the working-directory root, read it. Use it
as a hint, never as a bypass:

- If the manifest lists `startup-grill` as `completed` with a recent mtime,
  surface that fact: *"Manifest says you ran the grill on [date]. New
  defense round (interactive mode), fresh grill (rebuild kill report from
  scratch), or skip and review the prior report?"*
- The manifest's `gate_overrides[]` array is direct grilling ammunition:
  every recorded override is a deliberate decision the founder made
  to bypass a gate, and is worth probing in Round 1. Surface them in the
  kill-report's `## Iteration Evidence` section per the Phase 1 Step 1c
  iteration-evidence check.
- The manifest's `iterations` counter on `validation-canvas` (incremented
  on each loop-back) directly informs the iteration-evidence read: zero
  iterations + populated RAT Results = pristine pipeline yellow flag.
- Manifest read failures (corrupt JSON, missing fields) are non-fatal — log
  the issue inline and proceed as if no manifest exists.

After this skill ships its kill report (Phase 3), if `kit-manifest.json`
exists, append/update this skill's entry. Use atomic write (write `.tmp`,
then rename). If the manifest doesn't exist, do **NOT** create it — that's
the `startup-launch-kit` orchestrator's job. See
[`startup-launch-kit/references/manifest-schema.md`](../startup-launch-kit/references/manifest-schema.md)
for the schema.

### Step 1 — Read the working directory

Check for these files in order. When present, parse them as input — the
founder doesn't need to re-state what's already written down:

1. **`validation-canvas.md`** (from `validation-canvas`) — read the
   `### Customer Segments`, `### Unique Value Proposition`, `### Revenue
   Streams`, `### Customer Pains`, `### Pain Relievers`, and `## Stress Tests`
   sections. The Stress Tests section is **direct ammunition** for grilling —
   surface those weaknesses unless the founder has explicitly retired them.
   Un-relieved Pains and un-created Gains in the VPC are also direct
   ammunition.
2. **`rat/assumption-test-plan.md`** (from `riskiest-assumption-test`) — read
   `## Top 3 Hypotheses`, `## Test Plan`, and `## Results`. Confirmed results
   are evidence the founder can defend with; invalidated results that haven't
   propagated to the canvas are red flags. Pristine plans (no Results yet)
   indicate the founder skipped validation — see Step 1c below.
3. **`pitch/deck.html`** + **`pitch/speaker-notes.md`** (from `pitch-deck`) —
   parse the slide content for Problem, Solution, Market, Product, Business
   Model, Traction, Team, Competition, Ask. Use `pitch-deck`'s
   `references/slide-contracts.md` anti-patterns as a starting probe list.
4. **`brand-kit/brand-brief.md`** (from `brand-workshop`) — read the
   Positioning section (used by Slot 5 brand-strategist if active).

**If none exist:** ask the founder to provide a one-pager (or paste the
deck / canvas into the conversation). Refuse to grill on a single sentence —
the kill report would be all guesses. Minimum input: one paragraph each on
Problem, Solution, ICP, GTM motion, and Team.

### Step 1c — Iteration evidence check

Compare timestamps and content across the pipeline artifacts to detect a
**pristine pipeline** (one that ran end-to-end without the canvas being
revised after testing). This is a yellow flag, not a hard stop — but the
panel should probe accordingly:

1. If `validation-canvas.md` exists AND `rat/assumption-test-plan.md` exists
   AND `## Results` in the RAT has populated rows: check whether
   `validation-canvas.md`'s mtime is **earlier** than the latest Results
   entry in `rat/assumption-test-plan.md`. Earlier mtime means the canvas
   was NOT updated after testing.
2. If the canvas wasn't updated after RAT, surface as a yellow flag in the
   kill report's new `## Iteration Evidence` section: *"Canvas was not
   revised after assumption testing. Either the tests confirmed every
   belief (rare — be skeptical) or the founder is not closing the loop on
   what they learned. Probe accordingly."*
3. If `rat/assumption-test-plan.md` is **missing** entirely while
   `pitch/deck.html` exists: large yellow flag. Pitch built without
   assumption testing is sales theater. Surface in `## Iteration Evidence`:
   *"This pipeline shipped a pitch without testing assumptions. Treat
   every Traction claim as belief, not evidence."*
4. If `validation-canvas.md` is **missing** while later artifacts exist:
   the founder may have compiled the pipeline manually. Surface as a flag
   that the kill-report can't cross-check beliefs against documented
   stress tests.

The Iteration Evidence findings appear in a dedicated section in the
kill-report — see `references/kill-report.md` Section 7 (added in v2.0.0).

### Step 2 — Classify the variant

Ask exactly one question and wait for the answer:

> "Variant: (a) idea / pre-seed (no traction yet), (b) seed (early traction),
> (c) Series A+ (scaling)? This sets the bar for what counts as evidence."

If the user refuses to pick, default to **seed** and state the assumption
verbatim. Variant tunes evidence thresholds, not panel composition.

### Step 3 — Detect signals and resolve panel

Apply `references/panel-resolution.md` end-to-end:

1. Detect signals (Phase A)
2. Lock the fixed core (Phase B — 4 roles)
3. Resolve slot 5 (Phase C — technical DD or brand-strategist)
4. Inject specialists from triggers (Phase D)
5. Apply symmetry rules (Phase E — forced specialists)
6. Apply cap and trim if > 3 specialists (Phase F)

### Step 4 — Show the panel before grilling

Output the panel summary block per Phase G of `panel-resolution.md`. The
user can challenge the panel ("drop X, add Y") before Round 1 starts. If the
user redirects, accept and re-trim — don't re-debate.

---

## Phase 2: Grilling

Read `references/round-structure.md` and run **one-shot mode** end-to-end:

1. **Round 1 — Probe.** Each panelist contributes one probe per startup-axis
   they own. Per-probe shape and 60–100 word cap defined in
   `round-structure.md`.
2. **Round 2 — Forced steelman defense.** The skill itself responds *as the
   founder would* using only evidence in the brief. Lethal probes that the
   brief credibly answers get downgraded; probes that survive stand.
3. **Round 3 — Synthesis.** `@startup_strategist` assembles the kill-report
   sections; `@vc_partner` writes the verdict.

Apply persona overlays from `references/grill-overlay.md` for every
panelist, including the universal grill posture (probes for failure, demands
evidence, states severity declaratively, names failure modes specifically,
closes with falsifiers).

**Hard rule — Round 1 must surface at least one lethal-fixable or
lethal-unfixable read.** If every probe is `material` or `pass`, the panel
was too soft. Re-run Round 1 with sharper posture, or — if the idea
genuinely has no lethal weakness — note it explicitly: *"Round 1 surfaced no
lethal weaknesses. Re-running Round 1 with sharpened posture confirmed the
read."*

---

## Phase 3: Ship the kill report

Write `grill/kill-report.md` per `references/kill-report.md`. All seven
sections required, in order: Verdict / Lethal & Fixable / Lethal & Unfixable
/ Material & Fixable / Diligence Asks / Panel / Iteration Evidence.

Run the file's verifier checklist before presenting:

- [ ] All seven sections present in order
- [ ] Verdict label is one of the four canonical labels
- [ ] Lethal & Fixable has 2–3 items (no more, no fewer if verdict ≠ `Pass`)
- [ ] Each lethal item has all five fields filled
- [ ] Suggested attacks are specific (named artifact / signal)
- [ ] Diligence Asks are evidence requests, not change-the-business actions
- [ ] No weakness appears in two severity sections
- [ ] Panel table lists every role that contributed in Round 1
- [ ] Iteration Evidence section reflects actual working-directory state (full / pristine / no-RAT / no-canvas)

If any box fails, fix before shipping. Then present the file with
`present_files`.

---

## Phase 4: Offer interactive defense

The response after Phase 3 **must end with the interactive-mode invitation**
verbatim (or close variant — the prose can soften, the rule cannot drop).
See `references/round-structure.md` for the exact block.

If the founder picks a weakness and defends, run a defense round per
`round-structure.md`:

1. Identify relevant panelists (1–2)
2. Quote / summarize founder's defense
3. Re-probe with new-evidence rule (vibes-only defenses rejected)
4. Update the affected line item in `grill/kill-report.md` *only* — frozen
   items stay frozen
5. Append the round to `grill/defense-log.md`

A single weakness gets defended at most 3 times per session. After 3, the
verdict stands.

---

## Quality bars (skill-wide)

The skill must refuse to ship if any of these are true:

- **No lethal section** but verdict is `Pass` or `Pivot signal`
- **More than 3 lethal-fixable items** — re-rank, the bar drifted
- **A weakness appears in two severity sections** — pick one
- **A probe in Round 1 has no falsifier** — that's rhetoric, not grilling
- **A steelman defense in Round 2 invents favorable facts not in the brief**
- **The interactive invitation is missing** from the response after the
  report ships
- **Theatrical hostility** ("why would anyone fund this?") — name failure
  modes specifically or stay silent

---

## Cross-Skill Integration

| Skill | When to use |
|---|---|
| `team-composer` | Instead of this skill when the user wants brainstorming, planning, or constructive review. After this skill when the kill report's `Suggested attack` lines need a multi-role workshop to scope. |
| `validation-canvas` (our own) | Upstream input. If `validation-canvas.md` exists, this skill reads its Stress Tests section + un-relieved Pains + un-created Gains as direct grilling ammunition. After this skill when a `Pivot signal` verdict makes the founder rebuild their canvas. |
| `riskiest-assumption-test` (our own) | Upstream input. If `rat/assumption-test-plan.md` exists, this skill reads `## Top 3 Hypotheses` and `## Results`. The iteration-evidence check (Phase 1 Step 1c) yellow-flags pristine pipelines. After this skill when the kill report names assumptions the founder hasn't tested yet. |
| `pitch-deck` (our own) | Upstream input. If `pitch/deck.html` exists, this skill probes the deck's required-slot answers. After this skill when the kill report demands a re-cut deck. |
| `brand-workshop` (our own) | Upstream input when slot 5 = `@brand_strategist` and the panel needs the brand brief's Positioning section as a reference. |
| `skill-evaluator` (our own) | When you want to audit this skill's rules end-to-end. Good targets: the verdict-vs-body consistency rule, the no-lethal-skip rule, the interactive-invitation rule. |
| `superpowers:brainstorming` (if installed) | Use *before* this skill when the user is still shaping the idea. Grilling a half-formed idea produces a kill report full of "not enough information" findings, which is worse than no kill report. |

**Principle:** this skill owns adversarial probing of a startup idea with a
fixed-shape kill report as the deliverable. It does not build artifacts, does
not improve ideas, does not assemble teams for general work. Hand off to the
appropriate builder or thinker skill for everything else.

**Graceful degradation:** if no upstream artifact exists, this skill still
runs from a one-pager. Quality of the kill report scales with the quality
and specificity of the brief — garbage in, generic kill report out.
