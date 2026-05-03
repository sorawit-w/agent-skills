# Changelog

All notable changes to this plugin are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] — 2026-05-02

Restructures the startup pipeline. The prior `business-model-canvas` skill is
renamed to `validation-canvas` and refocused on the **Lean Canvas (Maurya) +
Value Proposition Canvas (Osterwalder)** combined artifact (right altitude for
an idea-stage founder; the 9-block Osterwalder BMC was a Series-A operating-plan
tool — wrong altitude). A new `riskiest-assumption-test` skill is inserted
between canvas and pitch-deck. **Inter-step gates** (light/medium/heavy/light)
are now enforced inside each skill's Phase 0; **loop-back is first-class** —
invalidated assumptions trigger canvas updates, not pipeline restarts. The
pipeline becomes:

```
brand-workshop ─▶ validation-canvas ─▶ riskiest-assumption-test ─▶ pitch-deck ─▶ startup-grill
```

### Changed (BREAKING)

- **`business-model-canvas` → `validation-canvas` (rename).** Skill folder
  renamed via `git mv` (history preserved). Canonical artifact renamed:
  `business-model.md` → `validation-canvas.md`; `business-model.html` →
  `validation-canvas.html`. Reference files renamed:
  `references/bmc-html-template.md` → `references/canvas-html-template.md`;
  `references/nine-blocks.md` → `references/canvas-blocks.md`. Asset icons
  + LinkedIn/X social banners renamed in lockstep
  (`assets/icons/business-model-canvas.svg` →
  `assets/icons/validation-canvas.svg`; same for `-li.svg`, `-x.svg`, and
  the matching `.png` files). **No alias provided** — update any saved
  invocations.
- **Skill content rewritten.** The 9-block BMC is replaced by Lean Canvas
  (Problem / Customer Segments / UVP / Solution / Channels / Revenue Streams
  / Cost Structure / Key Metrics / Unfair Advantage) PLUS a Value
  Proposition Canvas pass (Customer Jobs / Pains / Gains ↔ Products & Services
  / Pain Relievers / Gain Creators) with a mandatory Fit Check. SWOT, Porter,
  and Wardley are explicitly out of scope (wrong altitude / overlap with
  `startup-grill`).
- **Heading-anchor contracts updated** in `pitch-deck` and `startup-grill`.
  Downstream skills now grep for `### Customer Segments`, `### Unique Value
  Proposition`, `### Revenue Streams`, `### Customer Pains`, `### Pain
  Relievers`, etc., under the new `## Lean Canvas` and `## Value Proposition
  Canvas` parents. `## Stress Tests` heading is preserved (it's the seed for
  `riskiest-assumption-test`'s assumption dump).
- **CSS token rename.** `--bmc-accent` → `--canvas-accent` in
  `validation-canvas.html`. Added a parallel `--rat-accent` for
  `rat/test-matrix.html`. The Token Mapping Convention block in
  `brand-workshop`'s `design-system.md` template was updated; the prior name
  is documented in a migration note.
- **`startup-grill` kill-report gains a 7th section** —
  `## Iteration Evidence`. The verifier checklist now requires all seven
  sections in order. The new section yellow-flags pristine pipelines (canvas
  not updated after RAT testing) — pristine pipelines are a strong predictor
  of weak iteration discipline.

### Added

- **NEW skill: `riskiest-assumption-test`.** Inserted between
  `validation-canvas` and `pitch-deck`. Job: *"what have we proven?"*
  (experimental, vs. canvas's declarative *"what do we believe?"*).
  - Five phases: Phase 0 (read prior artifacts, medium gate STOPs without
    canvas), Phase 1 (assumption dump categorized desirability / viability /
    feasibility per Christensen), Phase 2 (3×3 risk × impact ranking, Top 3
    from high-impact corner), Phase 3 (falsifiable hypothesis rewriting —
    "We believe X. We'll know this is true if [measurable outcome] within
    [time]"), Phase 4 (test method selection from 8-method catalog),
    Phase 5 (render & ship + update mode for results).
  - Outputs: `rat/assumption-test-plan.md` (canonical, with `## Top 3
    Hypotheses`, `## Test Plan`, `## Kill Criteria`, `## Results` —
    headings load-bearing for downstream) AND `rat/test-matrix.html`
    (interactive risk × impact matrix; drag-to-rerank, click-to-expand,
    color-coded by category, Top 3 highlighted, prints cleanly).
  - Test method catalog: 5-interview rule, landing page + email capture,
    fake-door, concierge MVP, Wizard of Oz, pre-sale, smoke test, expert
    interview. With when-to-use, when-not-to-use, cost estimates,
    success/kill patterns, and worked examples for each.
  - References: `test-method-catalog.md`, `ranking-matrix.md`,
    `hypothesis-rewriting.md`, `matrix-html-template.md`.
- **Phase 0 experience-adaptive intake on `validation-canvas`.** Three
  calibration questions at invocation:
  1. *"Have you founded or co-founded a startup that reached paying
     customers before?"*
  2. *"Is this idea in a domain you've worked in professionally?"*
  3. *"Do you have direct experience with this customer segment?"*
  Maps to one of three modes — **Guided** (~60–90 min, definitions and
  examples per block), **Focused** (~30–45 min, lighter scaffolding, weight
  on commonly underweighted boxes by founder background), or
  **Compressed-with-Challenge** (~15–20 min, push back on glib answers).
  Smart intake: scans context for signals first, asks only the delta,
  confirms inferred mode in one line. Hard rules: ask immediately at
  invocation BEFORE canvas work, never mid-canvas; observed answer quality
  overrides declared mode. Explicit rule against delegating to
  `grill-with-docs` for intake (wrong job/tone/target).
- **Inter-step gates** (light/medium/heavy/light), enforced in each skill's
  Phase 0:
  - `brand-workshop` → `validation-canvas`: **light** (informational
    suggestion in brand-workshop's new Phase 7 Closing).
  - `validation-canvas` → `riskiest-assumption-test`: **medium** (RAT's
    Phase 0 STOPs without `validation-canvas.md`).
  - `riskiest-assumption-test` → `pitch-deck`: **heavy** (pitch-deck's new
    Phase 0 STOPs without populated `## Results` for top-3 hypotheses;
    override available with `[PRE-VALIDATION DRAFT]` watermark).
  - `pitch-deck` → `startup-grill`: **light** (grill works on minimum
    input; just enriched by full pipeline).
- **First-class loop-back protocol** documented in
  `validation-canvas/references/folder-contract.md`. Invalidated
  hypotheses route back to `validation-canvas` in update mode (read existing
  file, revise affected blocks only, mark with HTML comment, do not
  overwrite untouched blocks). Loop-back is normal pipeline behavior, not
  failure — pristine pipelines are the actual yellow flag.
- **Iteration-evidence check on `startup-grill`** (Phase 1 Step 1c). Compares
  mtimes across `validation-canvas.md` and `rat/assumption-test-plan.md`.
  Yellow-flags four pipeline states: full-with-iteration ✅, pristine 🟡,
  no-RAT 🟠, no-canvas ⚪. Surfaces in the new `## Iteration Evidence`
  kill-report section.
- Cross-references in `brand-workshop`, `team-composer`, root `README.md`,
  and `.claude-plugin/plugin.json` + `marketplace.json` updated to the new
  pipeline shape and skill names.
- New asset: `assets/icons/riskiest-assumption-test.svg` (3×3 risk×impact
  matrix with top-right Top-3 cell highlighted in gold; pixel-art style
  matching the rest of the shelf).

### Migration

- **Existing `business-model.md` files:** rename to `validation-canvas.md`
  and restructure under the new `## Lean Canvas` + `## Value Proposition
  Canvas` heading contract. The existing `## Stress Tests` section can
  carry over verbatim — that's the one block the new skill preserves from
  the old structure.
- **Saved invocations of `business-model-canvas`:** update to
  `validation-canvas`. No alias is provided.
- **Custom HTML themes binding to `--bmc-accent`:** rename to
  `--canvas-accent`. Brand-workshop's design-system template was updated
  in lockstep; the prior name is documented in a migration note inside the
  Token Mapping Convention block.
- **Pipeline workflow:** insert `riskiest-assumption-test` between
  `validation-canvas` and `pitch-deck`. The pitch-deck heavy gate WILL stop
  workflows that previously chained canvas → deck directly. Override path
  (`[PRE-VALIDATION DRAFT]`) preserves the old behavior with an explicit
  watermark.

### Notes

- No changes to `brand-workshop`'s identity-package output structure (still
  ships the same logos, favicons, social banners, descriptions pack, and
  design-system tokens). Only added a closing-suggestion line for
  `validation-canvas` and updated cross-references + the design-system
  Token Mapping block for the renamed `--canvas-accent`.
- No changes to `team-composer` Phase 1–6 logic, `sub-agent-coordinator`
  patterns, `i18n-contextual-rewriting`, `skill-evaluator`,
  `tech-stack-recommendations`, or `superpowers` integration. Only
  cross-skill table references in those skills updated to name the new
  pipeline shape.
- Plugin version: `1.6.0` → `2.0.0` (BREAKING — skill rename,
  artifact-name contract change, downstream heading-anchor contract change).

## [1.6.0] — 2026-05-01

Tightens `startup-grill` rule adherence and widens its trigger coverage
based on a skill-evaluator + skill-creator audit pass run immediately
after the 1.5.0 ship. The audit surfaced one critical Round 2 logic
gap, one verdict-spec gap, one STOP-gate redirect discipline gap, and
two trigger-coverage gaps. All five fixed in this version.

### Changed

- **startup-grill** — Round 2 downgrade rule
  (`references/round-structure.md`) rewritten to explicitly forbid the
  "defense gap + downgrade" pattern. Steelman defenses that name a
  defense gap MUST keep the probe at its Round 1 severity. Anti-pattern
  added. Surfaced by skill-evaluator T1 fixture (B2B SaaS happy path):
  the original prose-form rule let probes get downgraded despite
  explicit defense gaps in every steelman, producing empty Lethal
  sections and over-optimistic verdicts on briefs that genuinely had
  named gaps. Now reads as a hard rule keyed off specific phrases
  ("defense gap:", "the brief does not", "no [evidence type]") so it
  bites against Claude's natural pull toward synthesis and closure.
- **startup-grill** — Verdict spec (`references/kill-report.md`) now
  requires citing at least one specific weakness from sections 2–4 by
  item number (e.g., "see L2") or unambiguous reference (e.g., "the
  GTM channel weakness"). Generic aggregations like "five gaps remain"
  or "some risks need addressing" are explicitly forbidden. Was a
  checklist-only rule; promoted to body spec with PASS/FAIL examples.
- **startup-grill** — STOP gate in `SKILL.md` gains a "redirect
  discipline" note: when routing to `team-composer`, describe the
  *kind of lens* needed rather than inventing role tags that aren't in
  team-composer's canonical catalog (e.g., do NOT write
  `@market_researcher` or `@sustainability_expert` — those aren't in
  `team-composer/references/role-personas.md`). Surfaced by
  skill-evaluator T3 fixture.
- **startup-grill** — Description (frontmatter) widened with common
  adversarial-review synonyms (`pressure-test`, `roast my pitch`,
  `rip apart this`, `find the weaknesses in my idea`,
  `give me brutal feedback`, `be ruthless`) plus an explicit
  `team-composer` disambiguation paragraph for `review my X
  adversarially` / `review with VC eyes` / `stress-test my business
  model` framings — all route to `startup-grill`, not to
  `team-composer`'s broader "review" trigger. Surfaced by
  skill-creator description-collision check; addresses under-triggering
  risk where users use synonyms not in the original trigger list.
  Description grew from ~190 to ~290 words; still discriminating.

### Notes

- No changes to panel-resolution rules, grill-mode persona overlays,
  the kill-report deliverable shape, or the round structure itself.
  Only rule-text precision and trigger-coverage breadth.
- No changes to other skills.
- Audit pass-rate before fixes: 35/38 assertions (92%). Re-running the
  evaluator after these fixes is a follow-up; expected to lift T1's
  Round 2 + verdict assertions to PASS.

## [1.5.0] — 2026-05-01

Adds a new skill — `startup-grill` — to the shelf. Additive and non-breaking;
existing skills route the same way.

### Added

- **`startup-grill`** — adversarially probe a startup idea with a panel of
  domain-aware grillers and ship a structured kill report. New skill at
  `skills/startup-grill/`. Triggers on phrases like "grill my startup",
  "stress-test my pitch", "kill my idea", "pre-mortem my startup", "what
  would a VC hate about this", "tear apart my deck", "is this fundable".
  - **Fixed grill core (4 roles), flex slot 5.** Universal axes (capital,
    distribution, narrative, user reality) probed by `@vc_partner`,
    `@growth_marketer`, `@startup_strategist`, `@ux_researcher` always.
    Slot 5 resolves to `@senior_software_architect` (technical due
    diligence) by default and to `@brand_strategist` for consumer-brand-
    dominant products that aren't regulated and don't make novel ML claims.
    Two carve-outs (regulated, novel-ML) prevent the brand slot from
    silently winning when technical risk dominates.
  - **Specialist injection by signal** with a cap of 3 (panel ≤ 8). Risk-
    blocking specialists (legal, developmental psych, clinical psych, AI
    safety) are non-droppable when their trigger fires. Symmetric specialist
    forcing — when slot 5 flips to one lens, the other becomes a forced
    specialist if signals warrant.
  - **Persona import + grill-mode overlay.** Imports
    `team-composer/references/role-personas.md` as the canonical persona
    base; applies grill overlays so each panelist probes for failure rather
    than collaborates. Universal grill posture: probes for failure, demands
    evidence, states severity declaratively, names failure modes
    specifically, closes with a falsifier.
  - **Three-round structure.** Round 1 (Probe) — each panelist contributes
    one probe per startup-axis they own with a falsifier. Round 2 (Forced
    steelman defense) — skill responds *as the founder would* using only
    evidence in the brief; probes the brief credibly answers get
    downgraded. Round 3 (Synthesis) — `@startup_strategist` assembles the
    kill report; `@vc_partner` writes the verdict in 3–6 sentences with one
    of four canonical labels (`Investable as-is`, `Investable with
    conditions`, `Pivot signal`, `Pass`).
  - **Two-axis kill report.** Output at `grill/kill-report.md` ranks
    weaknesses on severity (lethal vs material) and fixability (fixable vs
    unfixable), then names them in four sections that read in priority
    order: *attack now / pivot signal / roadmap items / diligence asks*.
  - **No-soft-report rule.** If Round 1 surfaces no lethal probes, Round 1
    re-runs with sharpened posture; if still nothing surfaces, the response
    explicitly notes the no-lethal outcome rather than silently shipping a
    `material`-only kill report.
  - **Interactive defense mode.** After the report ships, the response ends
    with the interactive-mode invitation. If the founder picks a weakness
    number and brings new evidence, the relevant 1–2 panelists re-probe
    that line; the verdict on that item updates in place; other items stay
    frozen. Defenses log to `grill/defense-log.md` (append-only). A single
    weakness gets defended at most 3 times per session.
  - **Composes with the startup-artifact chain.** Reads
    `business-model.md` (Stress Tests), `pitch/deck.html` (slide-contract
    anti-patterns), and `brand-kit/brand-brief.md` (Positioning) as direct
    grilling ammunition when present. Sits at the end of the pipeline:
    `brand-workshop` → `business-model-canvas` → `pitch-deck` →
    `startup-grill`.
  - **STOP gate.** Five wrong-skill scenarios (brainstorming, building,
    plan review, brand voice review, diligence prep) route explicitly to
    the right skill before grilling logic runs.
- **References shipped:**
  - `references/kill-report.md` — six-section deliverable contract with
    forbidden patterns and verifier checklist
  - `references/panel-resolution.md` — Phase A (signals), B (fixed core),
    C (slot-5 detection rule with worked examples), D (specialist
    injection table), E (symmetry rules), F (cap-and-trim priority order),
    G (panel write-up format)
  - `references/grill-overlay.md` — universal grill posture +
    role-specific overlays for the fixed core, slot-5 alternates, and all
    specialists; anti-overlay section listing what NOT to do
  - `references/round-structure.md` — one-shot mode (R1/R2/R3) +
    interactive defense mode with refusal conditions and per-defense quality
    bar
- **`evals/evals.json`** — 10 fixtures covering the slot-5 matrix (B2B SaaS
  default, D2C consumer brand, AI consumer carve-out, regulated crypto
  carve-out, indie game, kids' EdTech with forced developmental psych),
  STOP-gate routing, minimum-brief refusal, soft-panel re-run, and
  interactive defense with evidence.
- **Root README** — new `startup-grill` row in the shelf table; new
  detail section; pipeline diagram extended to four stages
  (`brand-workshop` → `business-model-canvas` → `pitch-deck` →
  `startup-grill`); cross-references added to `pitch-deck` and
  `business-model-canvas` sections.
- **Plugin manifest** — `startup-grill` registered alphabetically between
  `skill-evaluator` and `sub-agent-coordinator`.
- **Banner assets** — `assets/icons/startup-grill.svg`,
  `assets/startup-grill-x.svg`, `assets/startup-grill-li.svg` matching the
  repo's pixel-art visual language.

### Notes

- No changes to existing skills' triggers, panels, or output contracts.
- Persona drift between `team-composer` and `startup-grill` is prevented by
  importing the canonical role catalog rather than forking — the grill
  ships posture overlays, not new persona definitions.

## [1.4.0] — 2026-05-01

Adds opt-in coexistence with the `superpowers` plugin. All new behavior
is capability-gated on `superpowers:brainstorming` appearing in the
session's available-skills list — when absent, the new routing is a
no-op and existing flows route the same way.

### Added

- **team-composer** — Phase 0.5 Skill arbitration with superpowers.
  team-composer becomes the repo default for "brainstorm / discuss /
  plan / review" requests when no skill is named. Defers to
  `superpowers:brainstorming` only on explicit invocation. Asks one
  disambiguation question when genuinely ambiguous. No-op when
  superpowers is not installed.
  - **"Explicit invocation" defined by exclusion.** Slash command,
    `"use [skill-name]"`, or a `[Skill]` tool call counts. Describing a
    workflow's *shape* ("one question at a time", "with the team")
    does not count — those are shape matches, not skill invocations.
    The rule explicitly forbids rationalizing shape-description as
    "implicit explicit choice." Surfaced by skill-evaluator audit
    against the original Phase 0.5 draft.
- **team-composer** — Phase 6 trigger row updated with handoff chain:
  `@staff_engineer`'s Structured Plan can hand off to
  `superpowers:writing-plans` → `superpowers:subagent-driven-development`
  for TDD-granular execution when superpowers is installed. Without
  superpowers, the Structured Plan remains the terminus.
- **team-composer** — three new Cross-Skill Integration rows for
  `superpowers:brainstorming`, `superpowers:writing-plans`, and
  `superpowers:subagent-driven-development`, all gated "if installed."
- **sub-agent-coordinator** — new "What this skill is NOT — sequential
  TDD execution" section with routing table. Disambiguates from
  `superpowers:subagent-driven-development`: parallel deliverable
  fan-out stays here; sequential TDD-task execution with reviewer
  gates routes to subagent-driven-development. The two are
  complementary, not competing — different deliverable shapes,
  different phases of the pipeline. Falls back to this skill's
  Pipeline pattern when superpowers is absent.
- **sub-agent-coordinator** — one new Cross-Skill Integration row for
  `superpowers:subagent-driven-development`, gated "if installed."

## [1.3.0] — 2026-04-27

Adds an optional structural plan-review phase to `team-composer`.
Additive and non-breaking — existing briefs route the same way; the
new phase only fires when the brief's signals warrant it AND the
runtime exposes the `Plan` subagent.

### Added

- **team-composer** — Phase 6.6 Structural Plan Review. Hands the draft
  Structured Plan authored by `@staff_engineer` in Phase 5 to the
  built-in `Plan` subagent for a focused rigor pass against a fixed
  checklist (decisions locked vs deferred, assumptions, phase
  acceptance criteria, files/modules, dependencies, ring-fence,
  agent-executability). Designed as siblings to Phase 6.5 (External
  Audit) — both can fire on the same run; 6.5 catches blind spots,
  6.6 catches structural weaknesses in the plan itself.
  - **Asymmetric reviewer/author contract.** `Plan` returns ranked
    findings with severity (blocker | major | minor) and per-finding
    suggested edits. `@staff_engineer` keeps authorship and edits the
    Structured Plan in place. No co-authorship.
  - **Capability-gated, not vendor-gated.** Triggers check whether the
    `Plan` subagent type is registered in the current runtime, not
    whether the host is Claude / Cowork / Claude Code. When unavailable,
    the phase is skipped with a logged fallback line in the user-facing
    output; in-context self-review is explicitly forbidden.
  - **Two-stage rollout.** Stage 1 (launch) auto-fires at
    `complexity=high`. Stage 2 lowers the floor to `complexity >= medium`
    once observed cost (median tokens <2k), latency (median <30s added),
    and value-yield (≥60% of runs surface ≥1 actionable finding) hold
    across enough Stage 1 runs.
  - **Opt-in trigger phrases bypass the complexity floor:** "tighten
    the plan", "Plan-review this", "stress-test the plan", "is this
    plan rigorous?", "make this agent-executable".
  - **Fold-back protocol.** Blockers must be addressed; majors should
    be addressed unless rejected with a recorded reason; minors are
    optional. Rejections are recorded as `**Plan-review notes:**`
    bullets at the bottom of the Structured Plan so the audit trail
    moves with the artifact, not in a separate log.
  - **Fixed run order:** Phase 6 → 6.5 → 6.6 → final synthesis. The
    reviewer always sees a stable plan. If the run-level token budget
    hits, 6.6 is the first to drop.
  - **User-facing output** appends one line:
    `Structural review by Plan subagent: <verdict>. <N> findings folded
    in, <M> rejected (see Plan-review notes).` The raw critique is not
    shown by default — users can ask for it on demand.
- **team-composer** — five new evals (ids 17–21) covering positive
  trigger, low-complexity skip, no-`@staff_engineer` skip, opt-in
  threshold bypass, and rejection-recorded-in-plan invariant. The sixth
  case (no `Plan` subagent registered → fallback note) is documented in
  the proposal as deferred — it requires runtime fixture support that
  the current prompt+assertion eval format doesn't have.
- **team-composer** — `proposals/plan-subagent-route.md` captures the
  design rationale, resolved decisions, and deferred future enhancements
  (Phased-Launch Variant support; Stage 2 threshold lowering).

### Notes

- No changes to Phases 1–5, `selection-algorithm.md`, or `role-personas.md`.
  `@staff_engineer` remains the in-context plan author; persona, tensions,
  and signature phrases are unchanged.
- Phased-Launch Variant review path is deferred until observed in a real
  regulated/phased-launch run. Premature support would add brief-template
  branching without evidence it's needed.

## [1.2.0] — 2026-04-20

Adds a new role to the `team-composer` roster. Additive and
non-breaking — existing briefs route the same way; the new role only
joins the team when the brief's signals warrant it.

### Added

- **team-composer** — `@design_engineer` as a new Tier 3 role in the
  Emil Kowalski tradition (Sonner, Vaul). Full parity with peer Tier 3
  roles:
  - Trigger row in `SKILL.md`'s Tier 3 table (motion, micro-interactions,
    component-library polish, "does this feel right?" reviews).
  - Q11 added to the Phase 3.5 Gap Detection Pass.
  - Full scoring section in `role-scoring.md` (include/skip criteria,
    differentiation from adjacent roles, partner-with notes) plus four
    new Signal-to-Role Quick Reference rows.
  - Full persona in `role-personas.md` (perspective, bias, tension,
    signature phrases with specific easings, blind spot, handoff,
    grounding) plus four new Healthy Conflict Patterns rows covering
    the three-way seam with Frontend Engineer, Product Designer, PM,
    and Accessibility.
- Grounds in the optional `emilkowalski/skill` plugin when installed;
  works standalone otherwise.

## [1.1.0] — 2026-04-19

A full-shelf adherence audit using `skill-evaluator`. Twelve rule-text
fixes landed across five skills. No breaking changes; existing prompts
still work, they just route and produce more predictably.

### Added

- **team-composer** — Phase 0 stop-gate. Prompts that ask for a logo,
  tagline, visual identity, or brand kit now route to `brand-workshop`
  before any team-assembly logic runs.
- **sub-agent-coordinator** — pre-delegation routing gate. Spawning
  role-based personas (strategist, copywriter, PM…) for one synthesized
  output now routes to `team-composer`. This skill keeps N-independent
  parallel work.
- **pitch-deck** — deck-variant classification step. Asks pre-seed /
  seed / Series A|B / demo-day before drafting, so slide depth and
  emphasis match the stage.
- **pitch-deck** — explicit closing triad (Ask · Use of Funds · Vision)
  and explicit three-files output contract (`.html`, `.md`, `assets/`).

### Changed

- **pitch-deck** — traction slide rules tightened: a time axis is
  required, and future-dated pilots are no longer allowed to appear as
  traction.

### Fixed

- **skill-evaluator** — artifact-policy rules clarified (inline by
  default, one file at workspace root only when the user asks).
- **business-model-canvas** — block-level rules sharpened to reduce
  drift between blocks.

### Notes

Prior versions (`1.0.0`, `1.0.1`) shipped before formal changelog
tracking — see `git log` for history. Starting from `1.1.0`, every
plugin version bump gets an entry here.

## [1.0.1] — prior

Pre-changelog. See `git log`.

## [1.0.0] — prior

Repo-as-plugin consolidation. Pre-changelog. See `git log`.
