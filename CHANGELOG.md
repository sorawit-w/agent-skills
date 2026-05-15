# Changelog

All notable changes to this plugin are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.11.0] — 2026-05-12

Hardens the `coding-rules` workflow boundaries to fix two stacked failure
modes: agents over-applying full TDD + build + lint discipline to one-line
copy changes (turning 30-second tasks into 5-minute ceremonies), and
agents *under*-applying discipline by self-classifying a one-line edit to
`auth/middleware.ts` (or `migrations/`, `payments/`, `terraform/`, etc.)
as quick-task and skipping the verification floor because the LOC delta
looked small. Five additions across four files in
`skills/coding-rules/resources/` — no `SKILL.md` text changes, no new
skill, no breaking changes.

### Added

- **`skills/coding-rules/resources/workflows/quick-task.md`**
  (`<fit_check>` section) — hard-floor criteria for quick-task routing:
  no new files, no test logic changes, no schema/contract/public-type
  changes, no high-stakes paths (see BOOTSTRAP §3), diff stays
  ≤ ~50 LOC, change is strings/copy/comments/config/data/formatting only
  (not logic, not refactoring, not behavior change). Comes with a
  2–4-line declaration template the agent states before starting (files,
  estimated LOC, type of change, confirmation that no new
  files/tests/schema/contracts/high-stakes paths are touched). If the
  agent can't state the fit cleanly, the task doesn't fit and routes to
  `workflows/feature.md`.
- **`skills/coding-rules/resources/workflows/quick-task.md`** (step 3
  rewrite) — split into 3a Scope-check and 3b Quality-check. 3a runs
  `git diff --stat` *after* implementation and re-validates the declared
  fit; if the actual diff now violates any fit criterion (LOC over
  budget, new file appeared, test/schema/contract/infra path touched,
  behavior change snuck in), the agent STOPS and escalates to
  `workflows/feature.md` from step 2. Trust-but-verify counterweight to
  self-classification — declared scope must match actual diff, or the
  workflow upgrades mid-task.
- **`skills/coding-rules/resources/BOOTSTRAP.md`** §3 (Route to Workflow)
  — high-stakes path override block that always routes to
  `workflows/feature.md` regardless of the task-type table, for: schema
  migrations (`**/migrations/**`, `**/prisma/migrations/**`,
  `**/alembic/**`, `**/db/migrate/**`, `**/drizzle/**`), auth/authz code
  (`**/auth/**`, `*authz*` / `*authentication*` / `*login*` / `*session*`
  / `*token*` filename matches), payments/billing flows (`**/payments/**`,
  `**/billing/**`, `**/stripe/**`, `**/checkout/**`), infrastructure
  (`**/*.tf`, `**/*.tfvars`, `**/terraform/**`, `**/k8s/**`,
  `**/kubernetes/**`, `**/Dockerfile*`, `**/docker-compose*.{yml,yaml}`,
  `**/helm/**`), CI/CD pipelines (`**/.github/workflows/**`,
  `**/.gitlab-ci.{yml,yaml}`, `**/Jenkinsfile`, `**/.circleci/**`,
  `**/buildkite/**`), and production-traffic-shaping values
  (retry/timeout/rate-limit constants, prod-gating feature-flag defaults,
  secrets-loading code). Closes the "one-line config change in
  `/auth/`" abuse pattern — blast radius isn't bounded by LOC, so the
  discipline floor can't be either.
- **`skills/coding-rules/resources/references/quality-gates.md`**
  (Formatter Scope section) — forbids repo-wide formatter and auto-fix
  invocations (`prettier --write .`, `eslint --fix .`,
  `biome check --apply .`, `black .`, `gofmt -w .`,
  `rustfmt --recursive .`). Defers to `lint-staged` / `husky` /
  `pre-commit` / `lefthook` when detected (via `package.json`
  `lint-staged` key, `.husky/pre-commit`, `.pre-commit-config.yaml`, or
  `lefthook.yml`). Provides touched-files-only invocation patterns per
  stack (Prettier, ESLint, Biome, Black, gofmt, rustfmt) using
  `git diff --name-only HEAD --diff-filter=ACMR` piped through `xargs -r`
  to avoid the zero-arg-means-format-everything trap that most formatters
  fall into when given no file arguments. Names the explicit
  normalization-pass exception (adopting a new formatter config,
  one-off repo normalization) with an announce-the-scope requirement so
  the developer isn't surprised by a 200-file diff.
- **`skills/coding-rules/resources/references/external-resources.md`**
  (Transport reliability paragraph) — STDIO preference for IDE-coupled
  MCP servers (JetBrains MCP and future LSP-bridge / language-server-MCP
  variants). Three reasons in declining order of importance:
  topology match (one server per IDE per developer = no shared state to
  amortize, no central deploy to update, no multi-client coordination —
  STDIO matches the topology exactly); spec direction (`sse` was
  deprecated in the MCP spec revision 2025-03-26 in favor of Streamable
  HTTP — use Streamable HTTP only when the server is genuinely remote and
  hosted, never for an IDE-coupled MCP); enterprise-network reality
  (corporate proxies, TLS interceptors, and idle-connection timeouts
  frequently break SSE and Streamable HTTP for long-lived MCP sessions
  through buffered events, dropped connections, and MITM cert distrust —
  on restricted networks STDIO is often the only reliably-working option
  regardless of topology preference). Notes that JetBrains 2025.2+
  in-IDE *MCP Server* settings and the `mcp-proxy` setup already default
  to STDIO; manually choosing an HTTP-based transport for an IDE MCP is
  almost always unnecessary.

### Why

Two failure modes were stacking. Mode 1: agents over-applying full
discipline to legitimately trivial tasks — comment fixes, copy updates,
config-value tweaks — running build + lint + full test suite when none
of those gates can catch a regression that's not present. Mode 2: agents
*under*-applying discipline by routing a one-line `auth/middleware.ts`
edit through `quick-task.md` because the LOC delta looked small, even
though the blast radius (auth, all sessions, all users) is the highest
in the codebase. Both modes came from the same root cause — the existing
`quick-task` vs `feature` boundary was advisory ("complexity 1–3")
rather than enforceable, and entirely self-declared without a
post-implementation check.

This release adds three enforcement layers without inventing new
vocabulary:

1. **Negative criteria for the trivial path** — `quick-task` fits only
   if specific things are NOT being touched (new files, test logic,
   schemas, contracts, high-stakes paths). What's NOT touched is
   observable from the diff; "complexity" was a self-rating.
2. **Path-pattern elevation** — auth / payments / migrations / infra /
   CI always get `feature.md` regardless of LOC. The blast radius
   matters, not the diff size. Hard-coded glob list, not self-declared.
3. **Post-implementation diff-check** — declared scope must match actual
   diff, or the workflow upgrades mid-task. Trust-but-verify, not honor
   system.

The formatter-scope rule addresses an adjacent observed pain point:
prettier-creep ballooning diffs into 200-file noise that hides the
actual change. The IDE-MCP transport-reliability note addresses another:
SSE and Streamable-HTTP MCP transports breaking on restricted corporate
networks where STDIO would have worked fine.

Vocabulary stayed deliberately native — no parallel "Tier 0 / 1 / 2"
naming was introduced. The existing `quick-task` / `feature` / `bugfix`
workflows are the tier system; this release hardens their boundaries
instead of inventing a parallel one. Introducing new tier numbers would
have created the abstraction-vs-payoff drag the change is meant to
remove.

### Notes

- **No `SKILL.md` text changes.** All edits live under
  `skills/coding-rules/resources/`. Per `CLAUDE.md`, the pre-shipment
  `skill-evaluator` + `skill-creator` description audit is required for
  `SKILL.md` text changes; resource-file additions don't require it.
  Self-review pass run on the four diffs; cross-references checked
  (quick-task's fit-check references BOOTSTRAP §3's path override; the
  formatter scope rule and the high-stakes path list are mutually
  consistent).
- **Diff-check is one-sided.** Only added to `quick-task.md` where the
  abuse pattern is "self-classify down to skip discipline."
  `workflows/feature.md` already has full gates + complexity-scaled
  validation + delegation signals; adding a diff-check there is
  gold-plating until evidence emerges that `feature.md` sessions
  self-classify their internal complexity rating too low.
- **BOOTSTRAP.md weight.** The high-stakes path override added ~15 lines
  to a file loaded into every `coding-rules` session. Inside the budget
  for a full operating playbook (vs. a frontmatter-adjacent skill) but
  worth flagging — a future v3.11.x could move the glob list to
  `references/guardrails.md` and leave a one-line pointer in BOOTSTRAP
  if loaded-context size becomes a real concern.
- **No keyword changes** in `plugin.json` / `marketplace.json`. Existing
  `coding-rules`, `guardrails`, `agentic-coding` keywords cover the
  additions; no new themes were introduced. No description-text changes
  in either manifest — no skills added or removed.
- **Backwards-compatible.** Existing sessions resume cleanly. Agents
  that had already routed to `feature.md` for high-stakes paths see no
  change; agents that had been routing to `quick-task.md` for those
  paths now correctly elevate.

## [3.10.2] — 2026-05-11

Adherence patch on `pixel-art` from a pre-shipment `skill-evaluator`
audit (4 tests, 17 assertions, 17/17 pass with two coverage gaps
flagged). Two SKILL.md text findings folded in, plus the skill is
formally labeled **🚧 BETA** until it has been dogfooded across more
subject categories and generators than the smoke test exercised.

### Changed

- **`skills/pixel-art/SKILL.md`** (verification section) — updated
  from "at least 4 of 5 craft markers" to "at least 5 of 6" with
  marker 6 (pixel scale matches density anchor) inlined.
  `references/anti-patterns.md` was updated to the 6-marker checklist
  in v3.10.1 but the SKILL.md mirror paragraph still said "4 of 5" —
  stale-after-patch inconsistency surfaced by the audit's T1 executor
  sub-agent (not by the grader rubric, which is the failure mode the
  `skill-evaluator` "don't lead with the pass-rate number" rule warns
  about).
- **`skills/pixel-art/SKILL.md`** (IP guardrail section) — tightened
  from *"Never reference a living artist by name"* to *"Never
  reference any specific named artist — living or deceased."* Deceased
  artists' work is typically still under copyright; the literal
  v3.10.0 / v3.10.1 wording left an ambiguity (e.g., Eyvind Earle,
  d. 2000). The audit's T2 executor handled it correctly by choosing
  the safer interpretation and explicitly flagged the gap — folded
  into the rule text here so a less cautious executor cannot leak the
  reference through on a different prompt.

### Added

- **🚧 BETA label** on `pixel-art` — surfaced in the SKILL.md body
  callout, plugin manifest descriptions, and root README shelf +
  detail sections. Same pattern as `gtm` (v3.4.0): structural
  smoke-tests pass and the routing rule + IP guardrail + craft-marker
  discipline are verified at the rule level, but the broader surface
  has not been dogfooded yet — scenes-only smoke test, Z-image only,
  no reference-image-supplied briefs. Patches expected as adjacent
  surface area surfaces gaps.

### Why

The 17/17 audit pass-rate hides two real findings — both Layer-1
skill-text gaps surfaced via executor sub-agent self-reflection, not
via the grader rubric. Pass-rate without coverage context is
misleading; `skill-evaluator`'s "Assertions ≠ Scoring" rule is the
right framing. v3.10.2 closes the pre-shipment audit ritual loop that
CLAUDE.md mandates for SKILL.md rule-text changes (recommended in
v3.10.0, deferred in v3.10.1, run here).

The BETA label is honest signaling. The skill works for moderate-
density scenes via Z-image and produces correct routing decisions for
hi-density briefs — both verified in the smoke test. But the broader
surface (characters, buildings, nature, lo-fi banners, non-Z-image
generators, reference-image-supplied briefs, multi-MCP routing) is
unverified in practice. Same shape as `gtm`'s BETA status —
structural reliability without real-workflow validation.

### Notes

- No new feature, no contract change for existing flows.
- Coverage gaps flagged by the audit and not closed in v3.10.2 —
  author/auditor bias (same person designed skill + tests), untested
  Path-B-only-when-no-MCP-connected, untested style-mode ambiguity,
  untested lo-fi generation, untested multi-MCP routing, untested
  reference-image-supplied briefs. Next audit round (with a different
  test author or new prompt angles) is the right close. v1 graduation
  gated on those gaps being exercised in real use, not on hitting a
  new pass-rate target.
- Same `skills/pixel-art/SKILL.md` file got both Finding A + Finding B
  edits in this patch; PyYAML strict-mode validation still passes.

## [3.10.1] — 2026-05-11

Adherence patch for `pixel-art`. Folds in real findings from the
first end-to-end smoke test (medieval harbor at dusk via Z-image
Turbo) which surfaced a routing-gap: Z-image scored 5/5 on the
original craft-marker checklist while still failing the user's
actual density target. Z-image caps at moderate density
(Stardew / Octopath aesthetic) and cannot reach hi-density
AI-pixel-art density via prompting alone — verified across two
regen attempts with explicit density emphasis and a resolution
bump from 1536×864 to 2048×1152.

### Changed

- **`skills/pixel-art/references/density.md`** — replaced the
  "approximately 96 pixels per character" numeric target (which
  image-gen models do not honor) with a **named density-anchor
  table**: 8-bit/NES, 16-bit/SNES, modern indie (Stardew / Celeste),
  HD-pixel-game (Octopath / Sea of Stars), and AI-pixel-art-density
  (matching hi-density AI-rendered references). Image-gen models
  honor named aesthetics from their training data far better than
  numeric pixel-per-unit constraints.
- **`skills/pixel-art/references/anti-patterns.md`** — added a
  **6th craft marker**: *"Pixel scale matches the density anchor."*
  Markers 1–5 check *how pixels behave* (hue shifts, clusters,
  dithering, banding, edge cleanup); marker 6 checks *whether the
  pixels are the right size*. The hi-fi pass bar raised from 4/5 to
  5/6. Added regenerate-recipe for marker 6 misses — *"if the anchor
  is HD-pixel-game-density or above and you're on Z-image, switch
  generators; prompt-only fixes cap at moderate density."*
- **`skills/pixel-art/references/model-routing.md`** — sharpened
  Z-image's "Known weak spots" to call out the density ceiling
  explicitly, named the empirical verification, and listed the
  escalation paths (Midjourney `--niji 6`, SDXL + pixel-art LoRA).
  Added a new **"Picking by density target"** section that maps each
  density anchor to the right generator and names the routing rule:
  *"if the user supplies a hi-density reference, do not start with
  Z-image even if it is the only connected MCP — generate a Midjourney
  or SDXL prompt brief via Path B instead. That is a real, useful
  output, not a degraded fallback."*
- **`skills/pixel-art/SKILL.md`** — Phase 3 (Generation routing) gets
  a **density-target pre-check** that runs *before* the MCP-availability
  check. If the brief's density anchor is HD-pixel-game-density or
  above, the skill skips Z-image and routes to Path B with a
  Midjourney or SDXL prompt brief, even when Z-image is the only
  connected MCP. Closes the routing gap that produced the smoke-test
  miss.

### Why

The 3.10.0 design assumed prompt-only fixes could push any image
generator to any density target. Empirical smoke testing falsified
that — Z-image has a hard ceiling and won't reach hi-density via
prompting. The skill's checklist passed (5/5 markers) while the user's
actual taste target failed, which is the worst possible failure
mode: a green light on a wrong output. Marker 6 (pixel scale matches
density anchor) is the missing check that catches this; the routing
rule (don't start with Z-image for hi-density briefs) is the upstream
fix so the failure doesn't happen in the first place.

Adherence-pattern parallel: same shape as v3.6.1 (skill-evaluator
audit surfaced a rule gap in `wear-the-hat`) and v3.5.1 (audit
surfaced executor-brief and `coding-rules` README gaps). Here the
auditor was a real smoke test, not a sub-agent — the gap surfaced
faster.

### Notes

- No new feature, no new skill. Pure adherence patch on `pixel-art`.
- Pre-existing prompt briefs and references (palette / composition /
  lighting / fonts / templates) unchanged.
- Recommended next: run `skill-evaluator` against the patched
  `SKILL.md` to confirm the Phase 3 density pre-check rule lands as
  written. The CLAUDE.md pre-shipment audit ritual applies to any
  SKILL.md rule-text change; deferred here because the change is
  responsive to a confirmed empirical finding (same precedent as
  v3.6.1 / v3.9.2 ship-then-audit pattern).

## [3.10.0] — 2026-05-11

Adds the **`pixel-art`** skill — a pocket-sized hi-density pixel-art
studio with a built-in design system, model-agnostic prompts, and a
code-based SVG title-card path. Encodes palette, density, composition,
lighting, typography, and craft-marker discipline once so the user
does not have to re-specify the style on every prompt.

### Added

- **`skills/pixel-art/`** — new skill (v0.1) with:
  - **Two style modes:** `hi-fi` (default, painterly hi-density pixel
    art — anchors on the user's medieval harbor and tavern interior
    references) and `lo-fi` (scanlined warm-paper banner aesthetic,
    matching the repo's own banners).
  - **Five subject categories:** scenes, characters, buildings,
    nature, title cards. Each has its own prompt template; all share
    the same `references/` design system.
  - **`references/` design system (8 files):** `style-modes.md`,
    `palette.md` (5 hi-fi palettes + lo-fi banner anchors with hex
    tokens), `density.md` (per-mode pixel density + dithering rules),
    `composition.md` (three-layer scene rule, eye-line, focal point,
    light source), `lighting.md` (6 lighting profiles — golden hour,
    candlelit, twilight, stormy, midday, dawn, plus banner / lo-fi),
    `fonts.md` (5-font catalog with **VT323 as default** per the user's
    pick, plus Pixelify Sans, Press Start 2P, Silkscreen, DotGothic16),
    `anti-patterns.md` (5-marker craft-marker checklist + explicit
    forbid list), `model-routing.md` (per-generator phrasing tweaks
    for Z-image, OpenAI Image / DALL-E 3, Imagen / Nano Banana,
    Midjourney, SDXL).
  - **`templates/` prompt scaffolds (7 files):** scene, character,
    building, nature, title-card-prompt, title-card.svg (portable SVG
    template with VT323 + bold + inset-shadow styling — the
    "Whispers of the Flame" look), and prompt-brief-fallback (the
    Path B copy-pasteable brief format).
  - **Capability-gated generation routing.** Path A: if an image-gen
    MCP is connected (Z-image Turbo, Imagen, OpenAI Image, etc.),
    generate inline with per-model phrasing tweaks. Path B: emit a
    copy-pasteable, model-agnostic prompt brief with per-model
    variants — first-class deliverable, not degraded fallback.
  - **Title-card SVG path.** Subject `title-card` additionally emits
    a portable SVG using VT323 with bold + inset-shadow styling; works
    without any image generator.
  - **IP guardrail** mirroring `algorithmic-art`'s standard: no
    living-artist names in prompts; original compositions only.
  - **5-marker craft-marker checklist** (hi-fi mode) — deliberate hue
    shifts, cluster studies, banding avoidance, painterly mid-tones
    via dithering, clean edges. Each marker has a regenerate recipe.
- **`assets/pixel-art-li.svg`**, **`assets/pixel-art-x.svg`** —
  LinkedIn (1200×627) and X (1600×467) banners. Three-panel
  composition: brief → design system (palette swatches + density
  ramp + VT323 sample) → output mini-scene (lighthouse, ships,
  castle silhouette, dithered water and sky).
- **`assets/icons/pixel-art.svg`** — 32×32 icon: tiny pixel-art scene
  with lighthouse (warm-accent light + reflection), ships, water
  bands.

### Changed

- `README.md` (root) — TL;DR count seventeen → eighteen; new shelf
  table row for `pixel-art`; new Skill details entry; Status section
  promotes 3.10.0 and demotes 3.9.2.
- `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` —
  version 3.9.2 → 3.10.0; description appended; skills list appended;
  keywords appended (`pixel-art`, `image-generation`, `design-system`,
  `VT323`, `hi-density`, `title-card`, `capability-gated`).

### Why

Re-typing palette, density, composition, lighting, and typography on
every pixel-art generation request is wasteful and produces drift
across runs. The skill encodes them once in `references/` and lets
the user express *intent* in 4–6 words. The design choice that
matters most: gating on **capability**, not **vendor**. The skill
works with any image-gen MCP that is connected, and it works without
any MCP via the model-agnostic prompt brief. This avoids the
two failure modes the planning discussion surfaced — (a) skill
hard-locked to a single image generator that the user may not have,
and (b) skill silently falls through to "no output" when no MCP is
present. Path B is first-class instead.

The title-card subject was bumped into v1 (rather than deferred to
v2) because typography is the most code-friendly subject and the
user's "Whispers of the Flame" reference is the clearest example
of the skill's value. Image models render text inconsistently;
SVG renders it perfectly. The skill pairs image-model background
generation with SVG text overlay so the user gets atmospheric
backdrops plus crisp typography in one deliverable.

VT323 is the default font per the user's pick during the planning
discussion. The catalog of four alternates covers the common pixel
typography cases (modern friendly, hard arcade, tiny labels, JRPG).

### Notes

- The skill ships without a pinned reference image set — those are
  generated by the user post-install (fresh originals chosen during
  planning to avoid any derivative-IP concern over the user's
  reference screenshots).
- Pre-shipment `skill-evaluator` + `skill-creator` description-check
  audits are recommended before users build on top of this skill;
  see `CLAUDE.md` → "Pre-shipment audit ritual."
- Out of scope for v1: image-to-pixel-art conversion of existing
  photographs; animated / sprite-sheet output; path C hybrid
  (programmatic composition skeleton + model fill). Future minor
  releases if demand surfaces.

## [3.9.2] — 2026-05-11

Adherence-only YAML frontmatter cleanup across 8 skills to align with the
cross-tool [SKILL.md standard](https://agentskills.io) consumed by Claude
Code, Codex CLI, Gemini CLI, Cursor, and other agents. No skill behavior
or description content changed.

### Fixed

- **`skills/coding-rules/SKILL.md`**, **`skills/pitch-deck/SKILL.md`**,
  **`skills/validation-canvas/SKILL.md`** — plain-inline `description:`
  fields contained `: ` (colon-space) sequences that YAML parsers
  interpreted as nested mapping keys, breaking frontmatter parsing
  entirely. Each `description:` is now a `>` folded scalar (the same
  style 9 other skills already use). PyYAML strict mode + Codex now
  accept all three.

### Changed

- **`skills/handshake/SKILL.md`**, **`skills/sub-agent-coordinator/SKILL.md`**,
  **`skills/wear-the-hat/SKILL.md`** — moved `instructions:` and `tags:`
  frontmatter keys into the body as a new `## When to use this skill`
  section + `**Tags:**` line. Codex's documented optional fields are
  `when_to_use`, `allowed-tools`, `disable-model-invocation`,
  `argument-hint`, `arguments`, `paths`, `model`, `effort` —
  `instructions` and `tags` are not in the allowlist. Moving them to
  the body preserves all content (Claude reads the body on activation
  regardless) and avoids unknown-field errors in stricter parsers.
- **`skills/ai-ux-review/SKILL.md`**, **`skills/ai-eval-review/SKILL.md`** —
  same treatment for `tags:` (no `instructions:` to move). Defensive
  alignment with the same standard.

### Why

Reactive corollary — the user reported three named skills (`coding-rules`,
`pitch-deck`, `validation-canvas`) failing to load in Codex with "invalid
YAML frontmatter" errors, plus `handshake` as a fourth case with a
different failure mode. PyYAML confirmed the three with `: ` collisions
in plain-inline scalars; `handshake` parsed cleanly per PyYAML, so the
unverified-but-plausible hypothesis is unknown-field rejection on the
`instructions:` key. Fix #1 (move to body) addresses both failure modes
without information loss and without changing Claude behavior. The two
tags-only skills (`ai-ux-review`, `ai-eval-review`) got the same
treatment defensively even though no failure was reported, because the
risk profile is identical to the affected three.

### Verification

- PyYAML strict-mode validation across all 17 SKILL.md files: **17/17
  pass** after the patch (3 were invalid before, 14 valid before).
- All 5 cleaned files now contain only `name` + `description` in
  frontmatter — the documented minimum required by both Claude Code and
  Codex per the open agent skills standard.

### Notes

- Cosmetic: the new `## When to use this skill` section in
  `handshake` / `sub-agent-coordinator` / `wear-the-hat` sits after the
  existing `## License` section. Functional correctness is unaffected;
  structural reorder deferred to a future cleanup.
- No README catalog changes — frontmatter patch inside existing skills,
  not new skills.
- The `handshake` failure was not directly reproducible via PyYAML, so
  the fix for that skill is hypothesis-driven (labeled as such in the
  conversation that produced this patch, per the §Diagnosis rule
  introduced in v3.9.0).

## [3.9.1] — 2026-05-11

Adherence-only documentation patch. Surfaces the token cost of
`skill-evaluator`'s split-role harness in both the skill's README and
the root README. The information was already present in Phase 4 of
`skill-evaluator`'s `SKILL.md` (high-stakes mode "Cost roughly doubles,
so default is off") but tucked deep in the workflow rather than where
users deciding whether to invoke the skill would see it.

### Changed

- **`skills/skill-evaluator/README.md`** — new `## What it costs to
  run` section between "Design choices worth knowing" and "Install."
  Names the per-test cost (one executor + one grader sub-agent, fresh
  context for the grader, Phase 1 read pass through every reference
  file the target skill cites), the typical run cost (~10 sub-agent
  invocations for 5 prompts, ~30 for 10 prompts + opt-in second-grader
  quorum), the design rationale (bias-free grading is the load-bearing
  constraint), and when a lighter in-context adversarial review is the
  right substitute (single-section rule edits — ~80–90% of the value
  at ~10% of the cost).
- **`README.md`** (root) — new `**Heads up — token-hungry by design.**`
  paragraph in the `skill-evaluator` detail entry, between "Reach for
  it when" and "Pairs well with." Compressed restatement pointing
  readers at the skill's own README for the full cost breakdown.

### Why

"Is this expensive?" is the first question users ask before invoking
an audit harness, and the answer was buried in workflow-body prose.
Surfacing it in both the per-skill README (where users land after
deciding to look) and the root README (where users decide whether to
look) means readers can make the call without reading Phase 4 first.

### Notes

- No skill text or behavior changes. `SKILL.md` is unchanged.
- No new skills, no catalog changes, no breaking changes.

## [3.9.0] — 2026-05-11

Adds a new **§Diagnosis** hard rule to `coding-rules`' BOOTSTRAP.md.
Closes the symptom-driven-fix failure mode — pattern-matching on error
messages, stack traces, or "what a similar bug usually looks like"
without reading the code that actually produced the failure. Generalizes
the Iron Law from `references/debugging.md` ("No fixes without root
cause investigation first") to all coding work, not just bugfixes —
feature-work failures (adding `*` to CORS allow-lists, wrapping in
`try/catch` to silence errors, copy-pasting unverified snippets) are
the same failure mode under a different name.

### Added

- **`skills/coding-rules/resources/BOOTSTRAP.md`** — new `### Diagnosis`
  section between `### Verification` and `### Resource Cleanup` in
  `<hard_rules>`. Three bolded leads: "Diagnose with evidence, not
  symptoms" (scope: any code edit, not just non-trivial), "Cite the
  evidence in your response" (citation must be from code/logs/config
  actually read this session, not invented — citing a file you have
  not opened is a §Accuracy violation), and "If evidence is not
  reachable after reasonable effort, STOP and surface the uncertainty"
  (escape valve: labeled hypothesis + verification path + 1–3 candidate
  fixes, with an anti-fabrication clause for the list). Defines
  "reasonable effort" as at least 2-of-4 concrete actions: read failing
  path / check `git log` / grep for failing symbol / read governing
  spec.
- **`skills/coding-rules/resources/BOOTSTRAP.md`** — new row in §When
  Stuck table: "Can't find evidence for the cause → Apply §Diagnosis
  escape valve."

### Changed

- **`skills/coding-rules/resources/BOOTSTRAP.md`** — §When Stuck table
  row "After 3 focused attempts" now sequences: apply §Diagnosis escape
  valve first (hypothesis + path + options), then mark BLOCKED.
  Previous wording made escape valve and BLOCKED look like competing
  options.

### Why

The Iron Law in `references/debugging.md` already says "no fixes
without root cause investigation first" — but it (a) lives in a
level-2 reference file that only loads via the bugfix workflow, (b) is
framed around *debugging* only, leaving feature-work symptom-fixing
untouched, and (c) provides no sanctioned alternative when the agent
genuinely can't find evidence, so agents under any pressure to ship
rationalize past it. This release promotes the rule to a top-level
Hard Rule in BOOTSTRAP (loaded in every session), generalizes the
scope, and adds an explicit escape valve so agents have somewhere to
land that isn't "ship a guess as a fix."

Pre-shipment ritual: in-context `skill-evaluator` audit on the drafted
rule surfaced six adherence gaps — three load-bearing (citation could
be invented, "non-trivial edit" was a scope leak, "confirms the cause"
allowed the error message itself to count as evidence) and three
lower-risk (effort threshold undefined, fabricated-alternative pressure
on the 2–3 fixes requirement, ambiguous interaction with the "After 3
attempts → BLOCKED" rule). All six were folded into the shipped rule
text.

### Notes

- No breaking changes — additive Hard Rule + clarification to one
  §When Stuck row.
- The rule cannot currently be mechanically enforced; a future hook
  (`pre-edit-check.sh` that blocks `Edit` on a file the agent hasn't
  `Read` in this session) is the natural next step and is filed
  against `references/hooks.md` enhancements rather than this release.
- No README catalog changes — this is a rule addition inside an
  existing skill, not a new skill.

## [3.8.0] — 2026-05-11

Adds the **`ai-eval-review`** skill — sibling to `ai-ux-review`, shipped
the same day. Eval-design-completeness review for AI products: seven
elicitation blocks covering necessity → ground truth → offline eval →
online metrics → cohorts + disparate impact → adversarial + robustness
→ drift + monitoring. Six mandatory cross-block checks plus a regulatory
cross-cutting lens (EU AI Act / FDA SaMD / FTC). Produces editable
Markdown plus a self-contained HTML visualization (3+3+1 card grid in
teal — visually distinct from `ai-ux-review`'s warm orange when both
reviews are open). Authored from first principles; informed by HELM
(Apache 2.0), Anthropic's claude-cookbooks (MIT), OpenAI Evals (MIT),
and EU AI Act / FTC / FDA SaMD regulatory texts — none reproduced
verbatim.

### Added

- **`skills/ai-eval-review/SKILL.md`** — full skill with frontmatter,
  Phase 0 intake (resolves `docs/ai-ux/` shared folder; reads
  `ai-ux-review.md` Block 7 gaps and seeds Block 1 from them; four
  intake facts), Phase 1 block-by-block elicitation (`@data_scientist` +
  `@ai_system_architect` + `@ai_safety_specialist` + `@senior_product_manager`
  + `@legal_compliance_advisor`), Phase 2 cross-block stress test with
  regulatory cross-cutting lens, Phase 3 render-and-ship, update mode,
  quality checklist.
- **`skills/ai-eval-review/references/blocks/01-07*.md`** — seven block
  reference files. Each carries the block's definition, primary probe,
  secondary probes per AI type (LLM-specific, agentic-specific,
  classical-ML), acceptance criteria, common gap patterns, and a worked
  example (continuing the LLM email-drafting product from `ai-ux-review`
  for narrative continuity). All authored from first principles —
  zero verbatim content from any cited influence.
- **`skills/ai-eval-review/templates/ai-eval-review.md`** — starter
  Markdown template with seven H2 sections, Block 6's adversarial table
  (failure mode × severity × eval set × resistance rate), Gap Summary
  placeholder.
- **`skills/ai-eval-review/templates/ai-eval-review.html`** — single
  self-contained HTML. Mirrors `ai-ux-review`'s 3+3+1 card grid for
  visual parity; teal `--ai-eval-accent` (vs. ai-ux-review's warm
  orange) signals sibling-not-twin relationship. Block 6 includes an
  inline adversarial table. CSS paged media for clean PDF print, zero
  network dependencies, no localStorage.
- **`skills/ai-eval-review/README.md`** — user-facing README per the
  14-section convention. Explicit "Influences" section names HELM,
  Anthropic claude-cookbooks, OpenAI Evals, EU AI Act, FTC, FDA SaMD
  with their licenses and the copyright-vs-derivative-work reasoning.
- **`assets/ai-eval-review-li.svg`** — LinkedIn banner (1200×627). Same
  three-card composition as `ai-ux-review`'s banner for visual sibling
  parity, but content is eval-specific (dashboard with `?` chips on the
  left, eval-block walk in the middle with Blocks 5+6 accented teal
  under a "RESPONSIBLE-AI" tag, review artifact on the right).
- **`assets/ai-eval-review-x.svg`** — X/Twitter banner (1600×467),
  adapted to wide aspect.
- **`assets/icons/ai-eval-review.svg`** — 32×32 icon. Same 3+3+1 grid
  structure as `ai-ux-review`'s icon but with Blocks 5+6 accented teal
  and Block 2 carrying the gap marker (ground-truth quality, the most
  common eval gap).
- **`skills/ai-ux-review/SKILL.md`** + **`skills/ai-ux-review/README.md`**
  — bidirectional cross-link to `ai-eval-review` added to "Cross-Skill
  Integration" and "Related skills" sections respectively (mirrors the
  forward link this skill carries).
- **`.claude-plugin/plugin.json`** + **`marketplace.json`** — new skill
  registered, version bumped to 3.8.0, six new keywords (`eval`,
  `evaluation`, `mlops`, `fairness`, `drift`, `ground-truth`).
- **`README.md`** — TL;DR skill count incremented (sixteen → seventeen);
  new row in "The shelf" table immediately after `ai-ux-review`; full
  skill-details entry with anchor, icon, what-it-does, reach-for-it-when,
  pairs-well-with, try-it. Status section promotes 3.8.0 to the current
  line and demotes 3.7.0 to "Earlier in v3.7.0."

### Changed

- **`skills/ai-ux-review/SKILL.md`** + **`README.md`** — both files'
  cross-skill-integration / related-skills sections now reference
  `ai-eval-review` as the sibling skill. No other changes to ai-ux-review's
  behavior, frontmatter, or trigger phrases.

### Why

The shelf now has two skills covering AI products: `ai-ux-review` for the
human-AI design surface (was the experience intentionally designed?) and
`ai-eval-review` for the measurement layer (do we have signal for whether
the design works?). The three-part skill-separation test held: unique
structure (eval-specific blocks), distinct deliverable (eval review
artifact), new elicitation pattern (eval-design-completeness via probes
and acceptance criteria, different from ai-ux-review's design-completeness).

The team-composer discussion that scoped this skill (10 roles, three
rounds, full conclusion) converged on "eval-design-completeness, not
engineering implementation" — the skill names what to measure and where
the gaps are, but does not write eval code, label data, or configure
monitoring infrastructure. That layer lives in HELM, Anthropic's
claude-cookbooks, OpenAI Evals, W&B, Evidently, or the team's eval
platform.

Block 6 is the boundary block: `ai-ux-review` Block 6 (Output Integrity)
asks *was prompt-injection mitigation designed?*; `ai-eval-review` Block
6 (Adversarial & Robustness) asks *is prompt-injection resistance
measured?*. The Phase 2 cross-block check explicitly verifies the boundary.

Block 5 (Cohort breakdown & disparate impact) carries the responsible-AI
weight as a first-class block — mirroring `ai-ux-review`'s decision to
make Block 6 (Output Integrity) first-class rather than relegate it to a
sub-bullet. Both choices come from the same design principle: under-served
concerns should be elevated, not folded.

Regulatory rigor (EU AI Act high-risk, FDA SaMD, FTC AI guidance) lives
as a cross-cutting lens applied in Phase 2, not as its own block. Treating
regulation as a lens forces it to influence eval rigor where it actually
applies (Blocks 2, 4, 5, 6, 7); treating it as a block would compress it
into a checklist and miss the cross-cutting nature.

### Notes

- **Pre-shipment audit ritual still owed.** Same as `ai-ux-review` —
  run `skill-evaluator` and `skill-creator`'s description-check on this
  skill's `SKILL.md` from a Mac terminal before commit. Expected
  categories of audit findings: trigger overlap with `ai-ux-review` (the
  "this skill assumes the UX layer is reviewed" boundary clause should
  fire), Block 6 specificity across AI types (LLM-specific probes
  dominate the reference file; classical-ML and agentic adaptations are
  shorter), regulatory cross-check's edge cases.
- **Block 1 ≠ Block 4 distinction is load-bearing.** The single most
  common AI eval failure is conflating the success target (Block 1) with
  the production metric (Block 4). The skill's Phase 2 cross-block check
  #1 verifies the proxy-vs-direct relationship is named honestly.
- **Block 2's label-quality push-back may surprise builders.** Most AI
  teams treat labels as a solved problem. The skill is designed to surface
  label-quality debt teams haven't noticed. Expect this block to generate
  more `[Gap — …]` markers than any other on first run.
- **No `kit-manifest.json` integration yet.** This skill ships standalone
  and via sibling composition with `ai-ux-review`. Future enhancement
  candidate: integrate into the `startup-launch-kit` orchestrator's
  `kit-manifest.json` flow if AI-product startups want both reviews as
  part of the pipeline.

## [3.7.0] — 2026-05-11

Adds the **`ai-ux-review`** skill — design-completeness review for AI
products and features. Seven elicitation blocks (necessity → mental model →
trust → feedback → errors → output integrity → success), six mandatory
cross-block checks, and a Gap Summary that names the unmade design
decisions with cheapest-experiment-to-resolve. Produces editable Markdown
plus a self-contained HTML visualization. Authored from first principles;
inspired by Google's [People + AI Guidebook](https://pair.withgoogle.com/guidebook/)
(CC BY-NC-SA 4.0) but not a derivative work — no Guidebook prose,
worksheets, or pattern names reproduced.

### Added

- **`skills/ai-ux-review/SKILL.md`** — full skill with frontmatter, intake
  phase, seven-block elicitation, cross-block stress test, render-and-ship
  phase, update mode, quality checklist, and cross-skill integration. The
  `[Gap — …]` marker is first-class and rolls up into Phase 2's Gap
  Summary.
- **`skills/ai-ux-review/references/blocks/01-07.md`** — seven block
  reference files. Each carries the block's definition, primary probe,
  secondary probes, acceptance criteria, common gap patterns, and a worked
  example (LLM email drafting throughout, for narrative coherence). All
  authored in the skill's own voice — no PAIR Guidebook text imported.
- **`skills/ai-ux-review/templates/ai-ux-review.md`** — starter Markdown
  template with the seven H2 sections and Gap Summary placeholder.
- **`skills/ai-ux-review/templates/ai-ux-review.html`** — single
  self-contained HTML template. Renders blocks as cards in a 3+3+1 grid,
  `[GAP]` chips on blocks with unresolved decisions, Gap Summary footer.
  CSS paged media for clean PDF print, brand-token-aware via
  `--ai-ux-accent` custom property, zero network dependencies, no
  localStorage.
- **`skills/ai-ux-review/README.md`** — user-facing README per the 14-section
  repo convention, with an explicit "Influences" section laying out the
  PAIR attribution and the copyright-vs-license reasoning for why this
  skill is not a derivative work.
- **`assets/ai-ux-review-li.svg`** — LinkedIn banner (1200×627), pixel-art,
  scanlined warm paper, three-card composition (AI feature spec →
  seven-block walk with Block 6 accented as the gen-AI layer → review
  artifact with gap chips), chapter ribbon below.
- **`assets/ai-ux-review-x.svg`** — X/Twitter banner (1600×467), same
  composition adapted for the wider aspect ratio.
- **`assets/icons/ai-ux-review.svg`** — 32×32 icon: a 3+3+1 grid of blocks
  with Block 6 in the warm accent (gen-AI integrity layer) and a red gap
  marker on Block 2.
- **`.claude-plugin/plugin.json`** + **`marketplace.json`** — new skill
  registered, version bumped to 3.7.0, five new keywords (`ai-ux`,
  `human-ai`, `design-review`, `hallucination`, `responsible-ai`).
- **`README.md`** — TL;DR skill count incremented (fifteen → sixteen);
  new row in "The shelf" table next to `skill-evaluator` and
  `tech-stack-recommendations`; full skill-details entry with anchor,
  icon, what-it-does, reach-for-it-when, pairs-well-with, try-it. Status
  section promotes 3.7.0 to the current line and demotes 3.6.3 to
  "Earlier in v3.6.3."

### Changed

- None. Existing skills' SKILL.md, README, and trigger phrases unchanged.
  All other touches are additive registrations.

### Why

The shelf had no AI-product UX review skill. The closest existing tool
was `team-composer` with `@ux_researcher` + `@ai_safety_specialist` — a
discussion mode, not a persistent artifact. The decision to add a
standalone skill rather than extend `team-composer` followed the repo's
three-part test:

1. **Unique structure** — block-by-block elicitation with acceptance
   criteria and explicit gap markers, not multi-role debate.
2. **Distinct deliverable** — a persistent Markdown + HTML artifact the
   builder can edit and share, not a transcript.
3. **New elicitation pattern** — design-completeness questions ("have
   you designed for X?") differ structurally from `validation-canvas`'s
   declarative belief capture ("here's what I think is true").

The skill is inspired by Google's PAIR Guidebook (CC BY-NC-SA 4.0). The
license analysis (see `ai-ux-review/README.md` → Influences) confirms
copyright protects expression, not ideas — using general AI UX concepts
in our own voice with our own elicitation flow is not a derivative work.
No PAIR prose, worksheets, illustrations, or pattern names are
reproduced anywhere in the skill or its references.

Block 6 (Output Integrity) is the modernization layer that differentiates
this skill from a re-housing of pre-2022 frameworks. It covers
hallucination handling, output verifiability, provenance and citation,
prompt-injection exposure, multi-turn drift, and agent autonomy levels —
the gen-AI surface that PAIR's 2021 framework predates.

### Notes

- **Pre-shipment audit ritual still owed.** The skill ships with locked
  frontmatter and full body, but `skill-evaluator` and `skill-creator`'s
  description-check have not been run on the new `SKILL.md`. Run them
  before committing (the sandbox can't dispatch fresh-context subagents
  for this kind of audit). Expected categories of audit findings:
  trigger-phrase overlap with `validation-canvas` for AI startups (the
  explicit boundary clause should fire), Block 6 specificity for
  non-LLM AI types, output-path resolution under the kit orchestrator.
- **Future companion skill candidate.** `ai-eval-rubric` is named in
  Block 7's "eval gap to companion" field as the natural place for the
  engineering eval layer (data labeling, eval code, online metrics
  setup, drift monitoring). Not built; not promised.
- **Block headings are load-bearing.** `## Block 1 — …` through
  `## Block 7 — …` and `## Gap Summary` are the parse anchors for any
  future companion skill. Adding or renumbering blocks is a MINOR bump
  minimum.

## [3.6.3] — 2026-05-11

Absorb harness-engineering vocabulary into `CLAUDE.md` and existing skills.
No new skill, no rule changes — names the discipline that skill authoring
in this repo was already doing partly by instinct, and points at
`coding-rules` as the canonical implementation.

### Added

- **`CLAUDE.md`** — new "Harness vocabulary" section after Quick reference:
  the five primitives (context engineering, progressive disclosure,
  observable feedback loops, state preservation, eval discipline) with one
  repo pointer each, plus a "Canonical implementation in this repo"
  paragraph naming `coding-rules`. External-reading footnote links the
  Anthropic, OpenAI, and `AGENTS.md` sources.
- **`CLAUDE.md`** — new **Design Principle 6** "Observable feedback loops
  over aspirational prose," with a reactive-constraint corollary. Cites
  `team-composer` Phase 6.6 Plan-review, `skill-evaluator`, the
  pre-shipment audit ritual, and the four-file version bump as existing
  examples of the principle.
- **`skills/coding-rules/SKILL.md`** — new "Harness engineering connection"
  section mapping each primitive to its concrete artifact in `coding-rules`
  (`BOOTSTRAP.md`, `CONTEXT.md`, vendor agent-context files, `references/`,
  hooks like `pre-commit-check.sh` / `protect-env.sh` / `protect-git.sh` /
  `session-start-context.sh` / `knowledge-bootstrap.sh`, `.ai/memory.log`,
  `.ai/STATUS.md`, `.ai/knowledge/`, `.ai/BLOCKERS.md`, `quality-gates.md`,
  `validation.md`). Names `coding-rules` as the canonical implementation
  that the abstract vocabulary in `CLAUDE.md` describes.
- **`skills/skill-evaluator/SKILL.md`** — new "Harness lens" section with
  five audit questions beyond rule adherence: does the skill name its
  primitives; is it using progressive disclosure or front-loading; are
  feedback loops machine-checkable; is a known failure mode an environment
  problem misdiagnosed as a prompting problem; is there a state-
  preservation gap.
- **`skills/sub-agent-coordinator/SKILL.md`** — framing paragraph in the
  intro: sub-agent coordination is harness engineering for delegated work
  (briefings carry context, verify-before-completion is a feedback loop,
  no-nested-sub-agents is state preservation). Names what's already there;
  doesn't change mechanics.
- **`skills/team-composer/SKILL.md`** — one-line annotation on Phase 6.6
  intro naming it as an observable feedback loop over the draft Structured
  Plan.
- **`README.md`** — one sentence after "The shelf" pointing readers at the
  harness vocabulary in `CLAUDE.md`.
- **`AGENTS.md`** — new eleven-line pointer to `CLAUDE.md` as a
  cross-vendor convention ([agents.md](https://agents.md/)). Non-Claude
  agents (Codex, Copilot, others) land in the same place a Claude Code
  session would. No content duplicated.

### Changed

- **`CLAUDE.md`** Skill anatomy table — `references/*.md` row annotated to
  name **progressive disclosure** explicitly as the harness pattern of
  loading detail on demand instead of front-loading into `SKILL.md`.

### Why

Anthropic and OpenAI both published harness-engineering posts framing the
work *around* the agent — context, scaffolding, feedback, state, eval — as
a discipline distinct from prompting. This repo was already doing most of
it under different names. Absorbing the vocabulary lets future skill edits
cite the primitives deliberately rather than rediscover them. The choice
to absorb into existing files (rather than add a top-level skill) follows
this repo's separation test: a new skill is justified when the workflow is
both reusable and elicitation-shaped, neither of which fits "name a
discipline already practiced."

An earlier draft of this release added a `progress.md` continuity log and
a `workflow-templates/` folder with `init-project` / `resume-project`
slash commands. Both were removed during review — they duplicated
`coding-rules`' `.ai/memory.log`, `.ai/STATUS.md`, and session-start
hooks (`session-start-context.sh`, `knowledge-bootstrap.sh`), which are
the sharper, working system. The State preservation row in the Harness
vocabulary table now cites those `coding-rules` artifacts directly.

External reading:
- [Effective harnesses for long-running agents (Anthropic)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Harness design for long-running application development (Anthropic)](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Harness engineering: leveraging Codex in an agent-first world (OpenAI)](https://openai.com/index/harness-engineering/)
- [agents.md convention](https://agents.md/)

### Notes

- No skill rules, triggers, YAML frontmatter, or output contracts changed.
  All edits are additive prose.
- No new top-level skill. Harness-engineering principles live in
  `CLAUDE.md` and existing skill bodies, not as a separate skill.
- `skills/coding-rules/resources/agent-context.schema.yaml` had a
  pre-existing local modification unrelated to this release; not included.

## [3.6.2] — 2026-05-11

Adherence-only documentation patch. The 3.6.0 release introduced the
`wear-the-hat` skill but failed to update the root README's catalog
sections — TL;DR count, "The shelf" table, and "Skill details" entry.
The skill was registered in `plugin.json` / `marketplace.json` (so it
auto-triggers on its description) but invisible to GitHub-repo readers
browsing the README. This patch fills those gaps and adds a new-skill
catalog requirement to `CLAUDE.md`'s release ritual so future skill
additions don't miss the catalog updates.

### Changed

- **`README.md`** — TL;DR count corrected (fourteen → fifteen); new
  row for `wear-the-hat` in "The shelf" table (between
  `sub-agent-coordinator` and `skill-evaluator`); full skill-details
  entry for `wear-the-hat` added with anchor, icon, **What it does** /
  **Reach for it when** / **Pairs well with** / **Try it** sections;
  "Pairs well with" lists in `team-composer`, `sub-agent-coordinator`,
  and `coding-rules` entries updated to reference `wear-the-hat`
  bidirectionally.

- **`CLAUDE.md`** — release ritual expanded: when a release ADDS a
  new skill, three additional root-README touches are required beyond
  the standard 4-file version bump (TL;DR count + "The shelf" table +
  "Skill details" section). Catches the exact failure mode that
  affected 3.6.0.

### Why

A new skill registered in the plugin manifests will auto-trigger on
its description (Claude reads frontmatter to decide whether to
invoke), but human readers browsing the GitHub repo discover skills
through the root README's catalog. Without catalog updates, the new
skill is effectively invisible to the human-reader discovery path —
Status section mentions persist only until the next release demotes
them; the catalog is permanent.

`CLAUDE.md` previously listed 4 files for a version bump but didn't
flag the additional requirement when introducing a new skill. 3.6.0
hit this trap; 3.6.2 closes it both by fixing 3.6.0's omission and
by adding the rule to `CLAUDE.md` so future Claude sessions catch
it before shipping.

### Notes

- **Adherence-only.** No behavior change to any skill — every skill's
  triggers, contracts, and outputs are unchanged.
- **Optional polish applied.** Adjacent skills' "Pairs well with"
  lists (team-composer, sub-agent-coordinator, coding-rules) now
  reference `wear-the-hat` bidirectionally. The wear-the-hat entry
  already referenced these neighbors; now the neighbors reference
  back.

---

## [3.6.1] — 2026-05-11

Adherence-only patch surfaced during pre-shipment `skill-evaluator`
audit of the new `wear-the-hat` skill. One small SKILL.md addition
closes a rule-adherence gap the audit exposed. No external contract
change to any skill.

### Changed

- **`skills/wear-the-hat/SKILL.md`** — Phase 2 (Load persona) gains a
  **Role name authority** paragraph: when reading a role from
  `team-composer/references/role-personas.md`, use the exact name from
  the catalog and do not paraphrase or invent variants. Adds a
  graceful-degradation rule for the case where the auto-pick heuristic
  returns a role that can't be found in the catalog (fall back to the
  closest match with disclosure).

### Why

A live-execute round of the `skill-evaluator` audit on `wear-the-hat`
surfaced one rule-adherence gap (T3 in the audit report): an executor
reading the auto-pick heuristic correctly saw `@accessibility_specialist`
for the "accessibility, a11y, WCAG" signal row, but renamed it to
`@accessibility_advocate` when embodying the persona in the response.
The SKILL.md Phase 2 didn't have an explicit rule about preserving the
exact catalog name, so the rename slipped through.

The auto-pick heuristic reference file already had a "Role name
authority" rule for maintenance discipline ("rows MUST exist as defined
personas in role-personas.md"), but that rule was framed as guidance to
the heuristic-file author, not as a runtime rule for the executor loading
a persona. This patch adds the runtime form of the same rule into
SKILL.md Phase 2 — where the executor actually loads the role.

### Notes

- **Adherence-only.** No behavior change to any other skill.
  `wear-the-hat`'s trigger gate, auto-pick outcomes, mode selection,
  and team-composer handoff path are all unchanged.
- **Audit ritual honored.** Per the pre-shipment skill-evaluator ritual,
  the audit caught a gap that self-review reliably missed. Acting on it
  now rather than batching keeps the remediation tight.
- All other audit findings (5 across the three skills audited:
  `wear-the-hat`, `sub-agent-coordinator`, `team-composer`) classified
  as test-design issues (Layer 2 rubric / Layer 3 brief framing) — not
  skill-text issues. No additional skill patches warranted. Overall
  audit pass rate: 66/73 assertions (90.4%).

---

## [3.6.0] — 2026-05-10

Consolidates sub-agent brief conventions into `sub-agent-coordinator` as
the canonical home, adds the **`wear-the-hat`** skill for single-role
embodiment, and updates `coding-rules` + `team-composer` to reference
the consolidated framework. Additive changes only — no external contract
breaks across existing skills.

### Added

- **New skill: `wear-the-hat`** — single-role embodiment for solo work
  where the user wants one specific lens applied to a task without
  convening a multi-role panel. Reuses `team-composer`'s
  `role-personas.md` as the canonical role catalog (no parallel
  taxonomy). 4-phase flow: trigger gate (deliberate signals only —
  `@role` tags, embodiment phrases, hat metaphors, lens framings) →
  pick role (explicit or auto-pick via keyword/verb table) → load
  persona (perspective + signature phrases only — not biases) →
  mode-select + execute (inline or sub-agent handoff). Four-outcome
  auto-pick: clean match, multi-candidate (ask user), multi-role
  (explicit handoff to `team-composer` with user confirmation), or
  fallback default. Includes banner SVGs and icon.

- **`sub-agent-coordinator` § Model Selection — Capability, Reasoning,
  Speed** — three orthogonal axes for sub-agent model selection:
  capability tier (low / standard / high), reasoning effort (off / on),
  speed lane (flex / standard / priority). Default mapping for coding
  work (10 rows), generic fallback mapping for non-coding (9 rows by
  task shape), disclosure-in-brief contract for axis overrides.

- **`sub-agent-coordinator` § Picking the Role** — task-verb-implicit
  role principle, optional `Role:` tag using `team-composer`'s catalog
  as shared vocabulary, runtime agent-type guidance (Explore / Plan /
  code-reviewer / general-purpose) as orthogonal to role tag.

- **`BLOCKED_SCOPE_EXPANDED` status** in `sub-agent-coordinator`'s Full
  Brief Reporting Section. Preserves the hard "no nested spawning"
  rule while letting sub-agents propose a split when scope expands.
  Communication Protocol gains a paragraph on the three valid
  orchestrator responses (approve split / re-brief tighter / accept
  partial).

- **`coding-rules` README Companion skills callout** — surfaces
  `team-composer`, `sub-agent-coordinator`, `wear-the-hat`,
  `skill-evaluator`, and `tech-stack-recommendations` near the top of
  the README so readers see the constellation without scrolling past
  220 lines.

- **`coding-rules` BOOTSTRAP routing** for architecture/scope
  decisions before coding — routes to `team-composer` first when
  installed, otherwise to `When Stuck → Architecture decision`.

- **`team-composer/references/role-personas.md` shared-catalog
  header** — names the three consumers (team-composer,
  sub-agent-coordinator, wear-the-hat) and the no-forking rule.

### Changed

- **`coding-rules/resources/references/sub-agent-delegation.md`** —
  Capability Tier + Reasoning Effort section and Picking the Role
  section both collapse to thin pointers at `sub-agent-coordinator`.
  Rule 3 (no nested sub-agents) qualified to match coordinator's
  Rule 6 with the `BLOCKED_SCOPE_EXPANDED` escalation path.

- **`team-composer` Phase 6 Model Routing** — retires the "future
  enhancement" note. Now points at `sub-agent-coordinator`'s Model
  Selection section. Adds an explicit "do not encode vendor-specific
  model strings" rule (e.g., no `opus-4-6` in skill content — they
  rot across vendor releases).

### Why

The repo had three places where sub-agent brief conventions were
documented or implied:

1. `coding-rules/resources/references/sub-agent-delegation.md` —
   delegation triggers, brief template anchors, coordination rules.
2. `sub-agent-coordinator/SKILL.md` — full briefing templates,
   coordination patterns, communication protocol.
3. `team-composer` Phase 6 — model routing principles, deferred to
   future implementation.

Model selection, role-picking, and nested-spawning protocol were
either missing entirely (model tiers were "future work" in
team-composer's Phase 6) or fragmented across the three locations.
This release moves the canonical framework into
`sub-agent-coordinator` and reduces the other two skills to
consumers — closing the gap that team-composer's Phase 6 had
explicitly flagged.

The new `wear-the-hat` skill captures a real workflow gap: cases
where the user wants a specific role's lens on a task without
running `team-composer`'s panel discussion or
`sub-agent-coordinator`'s worker fan-out. The shape that previously
required invoking `team-composer` and waiting for "someone in the
team to work on it" now has a direct entry point.

### Notes

- **Backward-compatible.** No existing skill behavior breaks.
  `wear-the-hat` triggers only on deliberate signals (explicit
  `@role` tags, embodiment phrases, hat metaphors, lens framings);
  it does NOT auto-fire on generic tasks that didn't ask for a role
  lens.
- **Shared catalog.** `team-composer/references/role-personas.md`
  remains the single source of truth for role definitions. Three
  consumers now reference it; extending the catalog there
  propagates to all of them.
- **Capability-gated graceful degradation.** `wear-the-hat` works
  without `team-composer` installed (the `Role:` tag becomes
  informational); `sub-agent-coordinator`'s Picking the Role
  section similarly degrades cleanly.

---

## [3.5.1] — 2026-05-10

Adherence-only patches surfaced during a `skill-evaluator` audit of
the new `coding-rules` skill. Two doc/template-level changes — no
external contract change to either skill. The audit itself produced
zero rule-text edits to `coding-rules`; these patches address gaps
in the harness and the user-facing docs that the audit exposed.

### Changed

- **`skills/skill-evaluator/references/executor-brief.md`** — Output
  Format section rewritten:
  - All three sections (Trace, Reasoning, Final deliverable) now
    explicitly mandatory. A one-line deliverable does NOT exempt the
    executor from emitting Trace and Reasoning.
  - Trace section gains a `(no tool calls)` fallback so the section
    is never silently dropped on zero-tool-call runs.
  - Anti-instructions list extended with an explicit "Do NOT skip the
    Trace or Reasoning sections even if the deliverable is one line".
  - Brief now warns that skipping a required section will cause
    trace-dependent assertions to grade as `unclear` or `fail`.

- **`skills/coding-rules/README.md`** — Sub-commands section expanded
  with two new subsections:
  - **How to invoke** — concrete slash-command examples for every
    sub-command (`/agent-skills:coding-rules`, `… load`, `… reload`,
    `… status`, `… install`, `… uninstall`) plus parallel
    natural-language phrasings.
  - **`load` vs `install` — they're independent** — explicit
    clarification that `load` is session-scoped while `install` is
    persistent-across-future-sessions; neither requires the other;
    `install` does NOT auto-activate BOOTSTRAP in the current
    session. Three example call patterns documenting the
    standalone-load, standalone-install, and combined
    first-time-in-project flows.

### Why

A live-execute round-3 audit of the `coding-rules` skill surfaced two
adherence-layer gaps — neither in the skill's rule text:

1. **`skill-evaluator`'s executor brief was too permissive about
   output omissions.** One executor produced a correct one-line
   `reload` confirmation but silently omitted Trace and Reasoning.
   The deliverable was right; the harness couldn't verify *how* the
   executor reached it. Two assertions graded `fail` / `unclear`
   with no underlying skill problem — a brief-layer issue exposed
   by terse interactions.
2. **`coding-rules`' README didn't make `load` vs `install` clearly
   independent.** A reader could plausibly conclude either "install
   is required before load" or "install activates rules in the
   current session" — both wrong. README now spells out the lifetime
   distinction, the three common call patterns, and the subtle
   gotcha that `install` doesn't activate BOOTSTRAP in the current
   session.

### Notes

- Adherence-only changes. No behavior change to either skill's
  external contract — trigger phrases, sub-command semantics, phase
  ordering, fix taxonomy, output template, artifact policy,
  second-grader quorum, and Phase 6.5 version-bump protocol are all
  unchanged.
- No skill-text edits to any skill. The `coding-rules` audit itself
  produced zero rule-text diffs across three rounds; the BOOTSTRAP
  rules and SKILL.md sub-command logic ship unchanged.

---

## [3.5.0] — 2026-05-10

Adds the **`coding-rules`** skill — a session loader for one author's
opinionated agentic-coding rules, ported from a separate working repo. Pure
addition, no breaking changes.

> ⚠️ **Read before installing.** The rules are aggressively personal — captured
> from years of breaking and fixing things while pairing with agents. They are
> not a neutral best-practice guide. Read `BOOTSTRAP.md` end-to-end first; fork,
> edit, or skip rules that don't fit your taste before adopting.

### Added (coding-rules)

- **New skill: `coding-rules`.** Session loader + per-project install for the
  bundled BOOTSTRAP rules under `skills/coding-rules/resources/`. Five
  sub-commands via the `args` parameter: `load` (default — `Read`s BOOTSTRAP
  into context as a tool result), `reload` (re-inject after compaction),
  `status` (scan for BOOTSTRAP signatures in current context), `install`
  (two opt-in phases — Phase 1: per-file append to detected vendor
  agent-instruction files `CLAUDE.md` / `AGENTS.md` / `AI-CONTEXT.md` /
  `.cursorrules`; Phase 2 (optional): register six `PreToolUse` /
  `SessionStart` lifecycle hooks in a user-chosen settings file with a single
  full-diff confirmation), `uninstall` (mirror — both phases optional, both
  confirmed). Both phases idempotent; both bias toward not modifying files on
  any uncertainty.
- **Phase 2 hook registration — what gets wired** (when the user opts in):
  - `PreToolUse` / matcher `Edit|Write` → `protect-env.sh` (hard-block
    `.env` edits — security, not env-var disablable).
  - `PreToolUse` / matcher `Bash` → `protect-git.sh` (hard-block destructive
    git: `reset --hard`, `push --force` to protected branches, `clean -f`,
    `branch -D`, `checkout .` / `restore .` / `checkout -- .` — data-loss,
    not env-var disablable).
  - `PreToolUse` / matcher `Bash` → `pre-commit-check.sh` (soft-warn on
    missing quality gates before `git commit`; hard-block on detected
    secrets in staged files).
  - `SessionStart` → `session-start-context.sh` (inject `.ai/STATUS.md`
    head + recent `.ai/memory.log` so the agent resumes with state).
  - `SessionStart` → `knowledge-bootstrap.sh` (scaffold
    `.ai/knowledge/KNOWLEDGE.md`, reindex AUTO-INDEX block, flag entries
    older than 180 days).
  - `SessionStart` → `context-bootstrap.sh` (scaffold `CONTEXT.md` if
    missing; never overwrites an existing one).
  Phase 2 writes by default to `<project>/.claude/settings.local.json`
  (gitignored, machine-only — lowest blast radius); user may pick
  `~/.claude/settings.json` (global) or `<project>/.claude/settings.json`
  (committed) instead. Three soft hooks (`session-start-context`,
  `knowledge-bootstrap`, `context-bootstrap`) plus the soft half of
  `pre-commit-check` are runtime-disablable via the existing
  `CODING_RULES_HOOK_DISABLED` env var (comma-separated, no spaces);
  security-critical hooks are not env-var disablable by design.
- **Auto-locate strategy.** Glob discovery (preferred) → `CODING_RULES_DIR` env
  var → ask the user, in that order. Resolves whether the install is global
  (`~/.claude/skills/coding-rules/`) or project-local
  (`<project>/.claude/skills/coding-rules/`).
- **Compaction-safe.** Long sessions can strip earlier context. `args: status`
  checks whether BOOTSTRAP markers (`Prime Directive`, `<hard_rules>`, etc.)
  are present; `args: reload` re-injects.
- **Bundled rule content.** `resources/BOOTSTRAP.md` (loader entry),
  `resources/workflows/` (`new-project.md`, `feature.md`, `bugfix.md`,
  `quick-task.md`), `resources/references/` (~25 long-tail topic guides —
  working patterns, quality gates, error handling, debugging, communication,
  git worktrees, guardrails, validation, context management, sub-agent
  delegation, vendor adapters, knowledge management, roadmap, hooks,
  multi-tool support, safety mindset, design-token authority via `DESIGN.md`,
  domain glossary), `resources/templates/` (starter `agent-context.yaml`,
  `STATUS.md`, `KNOWLEDGE.md`, `CONTEXT.md`), `resources/hooks/` (optional
  shell hooks for projects that want git/session-boundary enforcement), and
  `resources/scripts/validate-agent-context.ts` (Bun/Node validator with
  bundled JSON Schema).
- **Asset additions:**
  - `assets/icons/coding-rules.svg` — 32×32 pixel-art clipboard with a rule
    checklist and a small opinion-stamp accent in the warm-orange palette.
  - `assets/coding-rules-li.svg` + `.png` — 1200×627 LinkedIn-share banner:
    DIRECTIVE · RULES · CAVEAT three-card layout matching the repo's visual
    language. Centre card shows the six-item hard-rules checklist (orange
    checks); right card carries a prominent OPINIONATED — READ FIRST stamp so
    the caveat is visible wherever the banner is shared.
  - `assets/coding-rules-x.svg` + `.png` — 1600×467 X-share banner adapting
    the same content for X's aspect ratio.

### Notes

- **No breaking changes.** Pure addition. Existing skills, manifest layouts,
  and CHANGELOG conventions are untouched.
- **Activation stays skill-scoped — never plugin-wide (load-bearing design
  choice).** No `hooks` field is added to the parent plugin's `plugin.json`,
  and there is no `hooks/hooks.json` at the plugin root. Users who installed
  `agent-skills@sorawit-w` for any other skill (`team-composer`, `pitch-deck`,
  the startup pipeline, etc.) must not silently inherit `coding-rules`'
  `PreToolUse` / `SessionStart` guardrails. Hooks are only ever registered
  through Phase 2 of the skill's own `install` sub-command, with explicit
  consent on both phases. Future contributors: do **not** lift this
  restriction without a dedicated discussion — it preserves the opt-in
  framing the skill's README sells.
- **Reference fixes during port.** Two stale paths from the source repo were
  updated:
  - `resources/BOOTSTRAP.md`'s reference-index footer (was hardcoded to
    `.ai/coding-rules/resources/`; now resolves correctly whether the rules
    were loaded via the skill or copied into a project as a separate install).
  - The usage comment in `resources/scripts/validate-agent-context.ts` (now
    lists both possible install paths instead of assuming the legacy one).
- **Opinion-vs-evaluation boundary preserved.** The skill's own `CLAUDE.md`
  (which governs *editing* the rules, not loading them) routes rule changes to
  the `skill-evaluator` skill for split-context audit. Inline grading by the
  same agent that wrote the rule remains explicitly forbidden — that's the
  asymmetric-reviewer principle the shelf is built around.
- **Rule-cost gate enforced for future additions.** Every proposed new rule
  must pass a five-question cost gate (line count, frequency, severity,
  coverage, testability) before earning its place. Aesthetic rules are
  explicitly rejected — agents won't self-enforce them and they bloat context
  for no behavioral payoff.

### Status

`v0.1` of the `coding-rules` skill. The rules have been used and refined over
time in the source repo, but the marketplace packaging is new — treat as
alpha. Loader-behavior bug reports welcome via
[issues](https://github.com/sorawit-w/agent-skills/issues); rule-content
feedback should generally take the shape of fork-and-edit, not
feature-request.

---

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
