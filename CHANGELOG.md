# Changelog

All notable changes to this plugin are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.4.0] — 2026-05-06

Adds the **`gtm`** skill in **BETA**. Seventh skill in the startup pipeline —
covers the missing post-pipeline step (actually getting users) after
`brand-workshop → validation-canvas → riskiest-assumption-test → pitch-deck →
startup-grill`. Designed-for-orchestration: works standalone today, slots into
a future virtual-company agent fleet via structured handoff events.

> **⚠️ Beta — read before installing.** The skill ships with a 100% vs 27.8%
> first-iteration eval delta (24/24 vs 7/24 across three test cases:
> first-run-with-artifacts, cold-start, kill-switch). Those evals validate
> *structural* reliability — config files, helper-function pattern, handoff
> event vocabulary. They do **not** validate real founder workflows on a real
> startup project; that dogfooding is the next milestone. Breaking changes
> possible before v1 (graduating out of beta). Treat outputs as drafts to
> review, not artifacts to ship.

### Added (gtm — BETA)

- **New skill: `gtm`.** Phased go-to-market for startup products. Builds a
  GTM playbook from upstream artifacts (`validation-canvas`, `pitch-deck`,
  `brand-workshop` `DESIGN.md`), produces multi-channel content, schedules
  cadenced tasks (daily metrics pull, daily/weekly digests, 6-hour budget
  check), enforces compliance (CAN-SPAM/GDPR/FTC/TOS), and emits structured
  handoff events to `.workspace/events/` so downstream workers (support,
  sales, eng) can plug in cleanly.
- **Trust ramp (one-way) — P1 → P2 → P3.** P1 ships read-only playbook +
  content drafts (no external API calls). P2 adds scheduled execution with
  state and digests. P3 adds autonomous-with-escalation once MCPs are
  configured. Skipping levels is a configured refusal — empirically, founders
  who skip the ramp burn an account, reputation, or several thousand dollars
  in ad spend within the first week.
- **Architectural kill switch — never prompt-only.** `.gtm/HALT` file checked
  by `require_active()` helper-function wrapper before every external action.
  Three layers (HALT file → `state.json` status → harness-killable schedule
  via the `schedule` skill). Honest about best-effort enforcement in a Claude
  harness — see `references/kill-switch-pattern.md`.
- **Project-local config.** `.gtm/` per-project folder with `config.yaml`,
  `state.json`, `digests/`, `drafts/`, gitignored `secrets.local.yaml`. No
  global `~/.gtm/`. Each project namespace lives in its own folder.
- **Marketing skill orchestration with inline fallback.** When the
  `marketing:*` plugin is installed (default in Claude Cowork/Code), gtm
  dispatches per-channel content production via `sub-agent-coordinator`. When
  not installed, falls back to inline prompts (lower quality, still
  functional). See `references/marketing-fallback.md`.
- **Region adapters.** `references/regions/{code}.md` per region in
  `config.yaml#regions`. v1 ships `us` and a `_template.md`. Other regions
  (TH, JP, EU, BR) deferred until real launches into those markets.
- **Handoff event taxonomy v1.** `lead.captured`, `lead.qualified_b2b`,
  `content.needs_eng`, `crisis.detected`, `feedback.collected`,
  `experiment.concluded`. Append-only JSONL at
  `<repo-root>/.workspace/events/YYYY-MM.jsonl`. Future workers consume by
  `event_type` + `consumed_by` not containing their worker ID.
- **Asset additions:**
  - `assets/icons/gtm.svg` — 32×32 pixel-art megaphone with concentric
    signal-wave accents in the warm-orange palette.
  - `assets/gtm-li.svg` — 1200×627 LI-share banner: PLAYBOOK · CONTENT ·
    DIGEST three-card layout matching the repo's visual language. Centre
    card highlights the human-review approval gate (Approve & queue /
    Revise / Pass / HALT) — the most distinctive behavior. Carries a
    visible BETA pill in the top-right corner so the beta status is
    obvious wherever the banner is shared.

### Eval results (iteration-1)

- 100% pass rate with skill (24/24 assertions) vs 27.8% baseline (7/24).
- +72pp delta across three tests:
  - **first-run-with-artifacts** — auto-detects `validation-canvas.md` +
    `DESIGN.md` + `deck.html`, runs the wizard with smart defaults, creates
    `.gtm/config.yaml` + `.gtm/state.json`, ships P1 playbook + content
    drafts. 9/9 vs 3/9.
  - **cold-start** — empty project, idea-stage. Wizard handles missing
    artifacts gracefully, offers `brand-workshop` as a path, asks one Q at a
    time. 6/6 vs 1/6.
  - **kill-switch** — writes `.gtm/HALT` with the founder's reason, updates
    `state.json` status to "halted", explains the helper-function
    architecture honestly, walks through resume protocol cleanly. 9/9 vs 3/9.
- Workspace, grader script, eval viewer, and benchmark.json retained
  *locally* in `skills/gtm-workspace/` while iterating; not committed (git
  ignore `skills/*-workspace/`).

### Honest deferrals

- **Description-optimization loop** (`skill-creator/run_loop.py`) deferred to
  a Mac-terminal session because the sandbox `claude` CLI is not
  authenticated. Manual surgical pass applied instead — added explicit
  anti-triggers for: (a) Google Tag Manager (acronym overload), (b) "going to
  market with [findings]" idiom, (c) single-channel content for non-startup
  contexts (coffee shop announcements, personal posts). Description was
  compressed from 3,183 chars to 1,018 chars to fit the frontmatter cap;
  long-form versions of all rules remain in the SKILL.md body.
- **`skill-evaluator` audit** deferred until after first dogfooded run —
  iteration-1 evals were structural-only; rule-adherence audit on real
  prompts is the right next step before v1.
- **Real founder workflow dogfooding.** The 100% iteration-1 score reflects
  pristine fixture inputs. Real-world use will surface what breaks.
- **Region adapters beyond US.** TH, JP, EU, BR will be added when real
  launches into those markets demand them.

### Plugin

- Plugin version: `3.2.0` → `3.4.0` (minor + skipped 3.3.0 to align plugin
  and marketplace catalog versions; new skill, no breaking changes to any
  existing skill).
- Marketplace catalog: `3.2.0` → `3.4.0` (sync).
- Plugin description: updated to list `gtm (BETA — go-to-market for startup
  products)` after `startup-launch-kit`.
- Skills array: 12 → 13.
- Keywords added: `gtm`, `go-to-market`, `marketing`.

## [3.2.0] — 2026-05-05

Refines `handshake` following the pre-shipment audit (skill-evaluator pass +
manual description-trigger read). Two body fixes for adherence, two
description fixes for triggering accuracy. Minor bump rather than patch
because the description changes affect *which* prompts trigger the skill.

### Changed (handshake)

- **SKILL.md description:** added `"tune in to me"`, `"set a working
  agreement"`, and `"share my preferences"` to the trigger phrase list — the
  skill body uses these phrasings but the description didn't mirror them, so
  trigger queries that used those phrases were under-firing in the manual
  description read.
- **SKILL.md description:** added an explicit negative gate — *"NOT for
  codebase orientation, performance-review calibration, or content gathering
  (resumes, bios, requirements docs, CV bullets) — those are different jobs
  handled by other skills."* Closes the over-triggering risk on adjacent
  prompts that share keywords ("get to know," "calibration") but mean
  different things.
- **Phase 0 transition rule clarified.** Added a fifth bullet to "Rules for
  Phase 0" naming the explicit branch on memory state: when memory is
  empty, transition to Phase 1 in the same response; when memory is
  non-empty, end the Phase 0 turn with the correction prompt and wait for
  the user's reply before showing Q1. Resolves an ambiguity surfaced by the
  audit where executors split 6:2 on whether to pause or proceed.
- **Phase 1 voice rule added (META-LEAK).** New fifth bullet under "Hard
  rules for Phase 1": do not name the skill ("handshake," "this skill,"
  "the handshake skill is designed to…") in user-facing turns. Speak as a
  colleague calibrating, not a meta-narrator. Two of the eight audit runs
  leaked the skill name into the response — this rule closes the gap
  without adding new structural rules elsewhere.

### Audit details

- 8-test audit via `skill-evaluator`: 31/37 assertions passed (84%) before
  fixes. Of 5 failures, 2 were [SKILL] (META-LEAK on T7 and T8), 3 were
  [BRIEF] framing on T2 (test-quality issues, not skill issues).
- Manual description-trigger read flagged 4 risk areas; all 4 addressed in
  this version. Optimization-loop run via `skill-creator/run_loop` deferred
  to a Mac-terminal session because the sandbox `claude` CLI is not
  authenticated.
- No changes to: never-ask list, single-user contract, slash-command-only
  triggering, capability-gated memory integration. Those held cleanly under
  audit (T5 PII = 5/5, T6 multi-user = 5/5).

### Plugin

- Plugin version: `3.1.0` → `3.2.0` (minor — description triggering
  changed; widened on three new phrases, narrowed via explicit negative
  gate).
- Marketplace catalog: `3.1.0` → `3.2.0` (sync).
- Skills array: unchanged at 12.

## [3.1.0] — 2026-05-05

Adds the `handshake` skill — a brief, opt-in collaboration calibration ritual
that runs before the real work. Additive over v3.0.0; no breaking changes. All
prior skills continue to work unchanged.

### Added

- **New skill: `handshake`.** Slash-command-only at v1 (`/handshake`,
  `/handshake --project`). Two-mode design:
  - **Core mode** — shows ≤5 existing `user`-type memory entries (Phase 0
    "show what I know"), then asks ≤4 high-leverage pill questions plus 1
    free-text "what did past assistants get wrong?" question. Each question
    states its behavioral payoff. Writes to `user`-type memory in the
    existing two-tier store.
  - **Project overlay** — optional, opt-in. Asks ≤6 scoped questions about
    the current project (goal, stage, stakeholders, constraints, past
    decisions, external resources). All skippable. Writes to `project`-type
    memory — never `user`-type.
- **Hard never-ask list** — encodes the same PII exclusions used by the
  auto-memory system (protected attributes, government IDs, financial
  accounts, health information, home addresses, secrets). The skill refuses
  to ask, even if the user invites it.
- **Single-user contract** — `handshake` calibrates only the agent for the
  single person running this Claude instance. Multi-user identity awareness
  is explicitly deferred to Phase 2 with evidence.
- **Capability-gated memory integration** — defers to
  `productivity:memory-management` for file-layout conventions if installed,
  otherwise writes directly to the runtime's persistent memory using the
  standard frontmatter format. Vendor identity is not a routing input.
- **Show-then-ask preamble is mandatory.** Surfacing existing memory before
  asking anything new is a non-negotiable design choice, not an option.
  Skipping Phase 0 turns the skill into a survey, which it is not.
- **Asset additions:** `assets/icons/handshake.svg` (32×32 pixel-art icon,
  two hands clasping in the warm-orange accent palette) and
  `assets/handshake-li.svg` (1200×627 banner: KNOW · ASK · CALIBRATE
  three-card layout matching the repo's visual language).

### Design choices worth knowing

- **Three-part skill test was applied.** `handshake` passes on **unique
  elicitation** (privacy-conscious, consent-gated, show-what-I-know-first,
  hard never-ask list) and only partially on structure. The deliverable
  (`user`-type and `project`-type memory entries) is shared with the
  auto-memory system by design — `handshake` wraps the existing memory
  contract; it does not invent a parallel one.
- **Slash-command-only at v1, per the staged-rollout principle.** Aggressive
  auto-trigger (when `user`-type memory is empty mid-conversation) is a
  Phase 2 decision gated on observed user value. Other skills MAY suggest
  invoking `/handshake`; never auto-route.
- **Not folded into `startup-launch-kit`.** Calibration is a generic
  collaboration primitive, not a startup pipeline step. Coupling them would
  drift the kit's scope.

### Plugin

- Plugin version: `3.0.0` → `3.1.0` (additive — new skill, no breaking
  changes to the v3.0.0 `DESIGN.md` schema or any pipeline contract).
- Marketplace catalog: `3.0.0` → `3.1.0` (sync).
- Skills array: 11 → 12.

## [3.0.0] — 2026-05-05

Migrates `brand-workshop`'s starter design-system output to the
[Google Labs `DESIGN.md` format](https://github.com/google-labs-code/design.md)
(spec version: `alpha`). The prior `design-system.md` artifact is replaced
in lockstep across the four startup-pipeline skills that read it. **No
backward-compat alias** — clean migration.

### Changed (BREAKING)

- **`brand-workshop` output rename: `design-system.md` → `DESIGN.md`.** The
  starter design-system file is now emitted at `<brand-root>/DESIGN.md`
  (uppercase, exactly that). When the founder adopts the brand kit into a
  real repo, this file moves to the repo root per the spec convention.
- **New file format: YAML front matter + markdown prose.**
  - YAML front matter holds machine-readable design tokens — `colors`,
    `typography`, `rounded`, `spacing`, plus `version` / `name` /
    `description`. Tokens use spec-recommended names: `primary`,
    `secondary`, `tertiary`, `neutral` (lowercase).
  - Markdown body holds human-readable rationale, organized into the
    canonical spec section order: Overview → Colors → Typography →
    Layout → Shapes → Do's and Don'ts → Voice. (Components and Elevation
    sections are intentionally omitted at "starter" scope — they're
    stack-dependent.)
- **Cross-plugin contract retired.** The previous "Token Mapping
  Convention" block (`Primary | Secondary | Accent` prose labels grep'd
  by downstream plugins) is removed entirely. Downstream plugins now read
  `colors.primary` directly from the YAML front matter — no prose-grep
  fallback.
- **Downstream consumer updates** (input contract):
  - `validation-canvas` — `--canvas-accent` now binds to `colors.primary`
    from `<brand-root>/DESIGN.md` YAML front matter.
  - `riskiest-assumption-test` — `--rat-accent` same.
  - `pitch-deck` — `--deck-accent` same; typography tokens
    (`--deck-font-heading`) bind to `typography.h1.fontFamily`.
- **Quality Checklist gates rewritten** in `brand-workshop`:
  - File exists at `<brand-root>/DESIGN.md` (uppercase).
  - YAML front matter starts the file (`head -1` returns `---`).
  - `colors.primary` exists in the YAML.
  - Sections appear in canonical spec order.
  - Old "Token Mapping Convention" verbatim-grep gate removed.

### Added

- **Spec compliance.** Every emitted `DESIGN.md` is structured to lint
  clean against the optional `npx @google/design.md lint` CLI shipped by
  Google Labs. The spec is alpha; brand-workshop pins its target version
  to `alpha` and expects re-checking on each spec release.
- **`@senior_product_designer` persona grounding** in `team-composer` —
  if a `DESIGN.md` exists at repo root, treat its YAML tokens as locked
  Round 1 constraints and challenge any deviation. Cite the prose body
  when defending a design position.

### Migration

- **Existing v2.x users running brand-workshop:** new runs produce
  `DESIGN.md` instead of `design-system.md`. Downstream skills only read
  `DESIGN.md` going forward — old `design-system.md` files are no longer
  parsed. Re-run `brand-workshop` to regenerate.
- **Manual rename is not recommended.** Re-running the workshop is
  cheaper than hand-converting prose labels to the YAML schema, since
  the new format adds typography/spacing/rounded tokens the old file
  didn't capture.

### Plugin

- Plugin version: `2.2.0` → `3.0.0` (BREAKING — output filename + schema
  change in `brand-workshop`; input contract change in `validation-canvas`,
  `riskiest-assumption-test`, `pitch-deck`).
- Marketplace catalog: `2.1.0` → `3.0.0` (sync; was lagging plugin.json).

## [2.2.0] — 2026-05-05

Tidies the founder's working directory by rooting all startup-pipeline
artifacts under `docs/`. **Backward compatible**: every v2.1.0 invocation
still works because skills read v1 paths via fallback.

### Changed

- **Default output paths now under `docs/`.** Each pipeline skill writes to
  a per-skill subfolder:

  | Skill                       | Solo path             | Orchestrated path                    |
  |-----------------------------|-----------------------|--------------------------------------|
  | `brand-workshop`            | `docs/brand/`         | `docs/startup-kit/brand/`            |
  | `validation-canvas`         | `docs/canvas/`        | `docs/startup-kit/canvas/`           |
  | `riskiest-assumption-test`  | `docs/rat/`           | `docs/startup-kit/rat/`              |
  | `pitch-deck`                | `docs/pitch/`         | `docs/startup-kit/pitch/`            |
  | `startup-grill`             | `docs/grill/`         | `docs/startup-kit/grill/`            |

- **Path resolution precedence chain** (each pipeline skill, Step 0.0):
  1. Explicit `output_dir` arg passed by the orchestrator
  2. `STARTUP_KIT_DOCS_ROOT` env var (e.g., monorepos / Jekyll sites)
  3. Smart default — if `docs/startup-kit/` exists, write to
     `docs/startup-kit/<skill>/` and surface a one-line notice
  4. Solo fallback: `docs/<skill>/`

- **`kit-manifest.json` now lives at `docs/startup-kit/kit-manifest.json`**
  (was `./kit-manifest.json` at cwd root). The orchestrator creates the
  folder if absent. Legacy `./kit-manifest.json` is still read as a
  backward-compat fallback.

- **Cross-skill reads** (e.g., `pitch-deck` reading the validation canvas)
  resolve via the same precedence chain — siblings of the resolved root —
  with legacy v1 paths as fallback. Founders never need to migrate; the
  fallback handles old artifacts indefinitely.

- **Smart-default behavior:** running a child skill solo when
  `docs/startup-kit/` already exists writes to
  `docs/startup-kit/<skill>/` (auto-coalesces with prior orchestrated runs).
  The skill logs *"Writing to `docs/startup-kit/<skill>/` (smart default).
  Set `STARTUP_KIT_DOCS_ROOT=./docs` to write standalone instead."* — no
  silent surprise.

- **Re-run behavior:** overwrite, with git history as the version-control
  layer. Skills with additive sections (`riskiest-assumption-test`'s
  `## Results` table, `startup-grill`'s `defense-log.md`) preserve those
  per their existing skill-specific contracts.

- **Skill self-containment:** each skill's path-resolution rules live
  inline in its own SKILL.md Step 0.0. No cross-skill or external doc
  references — copying a single skill folder remains fully functional.

### Migration

- **Existing v1 users don't have to migrate.** Backward-compat reads
  handle `brand-kit/`, `validation-canvas.md` at root, `rat/`, `pitch/`,
  `grill/`, and `./kit-manifest.json` indefinitely.

- **To consolidate manually** (optional — for a tidy repo):

  ```bash
  # Solo runs (no kit-manifest.json):
  mkdir -p docs/canvas
  mv brand-kit docs/brand
  mv validation-canvas.md validation-canvas.html docs/canvas/
  mv rat pitch grill docs/

  # Orchestrated runs (kit-manifest.json at root):
  mkdir -p docs/startup-kit/canvas
  mv kit-manifest.json docs/startup-kit/
  mv brand-kit docs/startup-kit/brand
  mv validation-canvas.md validation-canvas.html docs/startup-kit/canvas/
  mv rat pitch grill docs/startup-kit/
  ```

  Skip lines for folders that don't exist in your project.

### Notes

- Plugin version: `2.1.0` → `2.2.0` (MINOR — additive, non-breaking).
- 19 files updated (6 SKILL.md + 12 reference files + plugin.json).
- No new dependencies, no new skills, no new artifacts shipped — just
  tidier defaults.

## [2.1.0] — 2026-05-02

Adds the **`startup-launch-kit` orchestrator** plus deeper sourcing on the
**`riskiest-assumption-test` test-method catalog**. Both tracks are
**additive and non-breaking** — every v2.0.0 invocation continues to work
unchanged. The pipeline philosophy from v2.0.0 (*sequential teaches
iteration*) is preserved by the orchestrator's design: gates are honored,
overrides are recorded with reason, every step's prompts surface to the
founder (no batching), and loop-back stays founder-driven.

### Added

- **NEW skill: `startup-launch-kit`.** Opt-in umbrella orchestrator that
  sequences the five-step startup pipeline (`brand-workshop` →
  `validation-canvas` → `riskiest-assumption-test` → `pitch-deck` →
  `startup-grill`) with shared state via `kit-manifest.json`.
  - **Hard constraint preserved:** every individual pipeline skill remains
    independently invocable. The orchestrator depends on the skills; the
    skills do not depend on the orchestrator.
  - **Auto-fires on end-to-end framing** ("build my whole startup kit",
    "do the full pipeline", "set up my whole launch", etc.) AND via
    explicit `/startup-launch-kit` slash command. Single-step requests
    route to the named skill directly via the STOP gate.
  - **Four phases:** Phase 0 (STOP gate + manifest discovery + filesystem
    reconciliation), Phase 1 (3-question intake once at orchestrator
    level, written to manifest cache), Phase 2 (sequence execution via
    Skill tool invocation per step, with gate enforcement between),
    Phase 3 (loop-back surfacing — founder decides; never auto-routes),
    Phase 4 (final summary).
  - **`kit-manifest.json` schema:** thin state journal with
    `manifest_version: 1`, `created`/`updated` timestamps,
    `intake_answers` cache, `steps[]` (status + mtime + iterations per
    skill), and `gate_overrides[]` (audit-trail entries with reason ≥ 20
    chars + `founder_acknowledged: true`). Atomic writes (`.tmp` +
    rename). See `references/manifest-schema.md` for the full schema and
    three worked examples.
  - **State-detection rules** (manifest vs. filesystem reconciliation):
    filesystem always wins on artifact presence; stale-artifact threshold
    is 30 days; manifest entries get absorbed silently when a manual run
    is detected; `blocked` status requires explicit founder unblocking.
    See `references/state-detection.md` for the full reconciliation loop.
  - **Gate-override protocol:** every override is append-only, persistent,
    and revocable. Required fields enforced (gate identifier, ISO-8601
    timestamp, ≥ 20-char reason, `founder_acknowledged: true`). Surfaced
    in `startup-grill`'s `## Iteration Evidence` section as direct
    grilling ammunition — overrides are deliberate decisions worth
    probing, not hidden bypasses. See `references/gate-override-protocol.md`.
  - **References shipped:** `manifest-schema.md`, `state-detection.md`,
    `gate-override-protocol.md`.
  - **New asset:** `assets/icons/startup-launch-kit.svg` — five color-coded
    pipeline-step boxes connected by a state-tracking thread, manifest
    indicator at the top.
- **Phase A — manifest awareness in all 5 pipeline skills.** Each pipeline
  skill (`brand-workshop`, `validation-canvas`, `riskiest-assumption-test`,
  `pitch-deck`, `startup-grill`) gains an additive Step 0.0 that reads
  `kit-manifest.json` if present, uses it as a hint (never as a bypass),
  and appends/updates its own entry after writing artifacts. Five-line
  pattern, identical across all five skills, with two special cases:
  - **`validation-canvas` Step 0.0 — intake-cache:** if the manifest's
    `intake_answers` cache is populated, present cached answers and ask
    the founder to confirm or update (single code path through Phase 0;
    never silently skip).
  - **`pitch-deck` Step 0.0 — override-flag:** if the manifest records a
    `pitch-deck-pre-validation` override with `founder_acknowledged:
    true`, honor it silently (proceed with `[PRE-VALIDATION DRAFT]`
    watermark) but surface a one-line acknowledgment.
- **Catalog deepening — `riskiest-assumption-test/references/`.**
  - **NEW: `sources.md`** — full bibliography for all canonical sources
    referenced inline in the catalog. Primary sources: Maurya *Running
    Lean* 3rd ed. (2022), Ries *Lean Startup* (2011), Fitzpatrick
    *The Mom Test* (2013). Secondary: Savoia *The Right It / Pretotype
    It* (2019), Hall *Just Enough Research* 2nd ed. (2019). Cited but
    not primary: Blank *Four Steps to the Epiphany* (2nd ed., 2013;
    cited for "get out of the building" framing and LOI-as-validation,
    NOT for the dated four-stage Customer Development vocabulary).
    Includes a "notes on conflicts and defaults" section that resolves
    sample-size disagreements (n=5 floor per Maurya; expand if signal
    is noisy per Hall) and concierge-vs-WoZ boundary (Maurya's
    separation: concierge tests viability, WoZ tests experience).
  - **`test-method-catalog.md` deepened in place:** intro paragraph
    cites Blank's *get out of the building* + lists primary sources +
    points to `sources.md`. Each of the 8 methods gains terse inline
    surname-only citations (e.g., *per Maurya*, *following Fitzpatrick*)
    where a source directly justifies a claim, plus a "Further reading"
    line before the entry separator (3–5 references). Per-entry ceiling
    (~60 lines) preserved for 7 of 8 methods.
  - **Method 6 renamed and extended:** `Pre-Sale` → `Pre-Sale or Letter
    of Intent (B2B variant)`. New LOI sub-section covers when LOI >
    Pre-Sale (regulated industries, large enterprise procurement,
    cofounder/team commitments), what makes an LOI credible (signed +
    dated + named decision-maker + named dollar amount or seat count +
    named trigger condition + signing authority), and investor-credibility
    weighting (enterprise LOIs > equivalent-revenue individual pre-sales
    per VC consensus; LOIs without specific dollar amounts < $1 of real
    revenue). Method 6 ceiling: 75 lines (the explicit exception per the
    v2.1.0 plan).
  - **Common-trap deepening discipline (anti-bloat lazy rule):** added
    Fitzpatrick's three sins (opinion / future-tense / hypothetical
    questions) to the 5-Interview Rule's Common trap; added Savoia's
    YODA principle ("Your Own Data Always") to Fake-Door's; added
    Fitzpatrick's expert-flattery anti-pattern to Expert Interview's.
    Other methods left untouched where current copy was already
    source-aligned.
- **`validation-canvas/references/folder-contract.md`** — un-deferred the
  manifest section. The "no one-shot orchestrator" line now reads "as of
  v2.1.0, the `startup-launch-kit` skill is an opt-in orchestrator…"
  with explicit pointers to the orchestrator's references. Pipeline
  skills are now manifest-aware (Phase A); the orchestrator owns the
  manifest's lifecycle.
- **Root `README.md`** — new `startup-launch-kit` row in the shelf table;
  new detail section after `startup-grill`; new "Pipeline shortcut
  (v2.1.0+)" paragraph in the startup pipeline description that explicitly
  preserves the philosophy. Status section bumped to 2.1.0.
- **Plugin manifest** — `startup-launch-kit` registered alphabetically
  alphabetical-by-purpose at the end of the pipeline group; version
  bumped `2.0.0` → `2.1.0`; description updated; new `orchestrator`
  keyword added.

### Notes

- No changes to existing skills' content semantics — only additive Phase 0
  manifest-awareness blocks (~30 lines per skill).
- No new methods in the catalog; the 8-method count is preserved (Pre-Sale
  absorbs LOI as a sub-section variant).
- Customer Development sprints are still explicitly out of scope (per
  v2.0.0, kept in the catalog's "What this catalog deliberately does NOT
  include" closing section).
- All five pipeline skills' frontmatter `description` fields are unchanged
  in v2.1.0 — the orchestrator does not change how individual skills are
  triggered.
- Open follow-ups deferred to v2.2.0+: subset/custom pipelines, manifest
  query API, multi-directory composition, Maurya 1st-edition addendum,
  auto-routing of loop-back actions.

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
