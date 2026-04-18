# Delegation Matrix — `agent-skills` ↔ Anthropic's official skill shelf

**Status:** Phase 1 artifact from the audit recommended by `team-composer` on
2026-04-18. This is the working document for the 4-phase absorb / delegate /
reference / keep pass across the 8 custom skills in this repo.

## What this document is

A per-skill map of how each custom skill in `/skills` relates to Anthropic's
officially-shipped skills (the ones installed by default under
`~/.claude/skills/` — `skill-creator`, `docx`, `pptx`, `xlsx`, `pdf`,
`canvas-design`, `algorithmic-art`, `theme-factory`, `web-artifacts-builder`,
`mcp-builder`, `brand-guidelines`, `doc-coauthoring`, `ui-ux-pro-max`,
`ai-safety-mindset`, `consolidate-memory`, `schedule`, `setup-cowork`).

For every custom skill we pick one of four actions per official skill it
touches:

| Action | Meaning |
|---|---|
| **Keep** | No relationship. No mention needed. |
| **Reference** | The custom skill names the official skill in a `Cross-Skill Integration` section and explains when to hand off. |
| **Delegate** | The custom skill actively invokes or hands artifact production to the official skill (e.g., deck styling → `theme-factory`). |
| **Absorb** | Import patterns/conventions from the official skill into our own text (e.g., `skill-creator` authoring conventions). |

## Guiding principles

1. **No deprecations.** Every custom skill has unique orchestration value. The
   overlap is on *output primitives*, not *domain logic*.
2. **Custom owns orchestration + opinion; official owns format + primitive.**
   `pitch-deck` owns founder interview + narrative gating; `theme-factory` owns
   tokens; `pptx` owns binary format fallback.
3. **Graceful degradation.** If a referenced official skill isn't installed,
   the custom skill must still produce *something* — not fail silently.
4. **Reduce trigger collisions.** Where two skills compete on keywords,
   descriptions must state the boundary explicitly.

---

## Per-skill analysis

### 1. `brand-workshop`

**What it produces:** brand strategy brief (.md), tagline, SVG logo, favicon
pack, social banners, descriptions pack, `design-system.md`, branded
pitch-deck template.

| Official skill | Action | Why |
|---|---|---|
| `canvas-design` | **Reference** | For high-fidelity static poster/brand art output quality standards. Brand-workshop's SVG logo generation does not match canvas-design's depth — hand off when the user wants brand art beyond a logo. |
| `algorithmic-art` | **Reference** | When the brand direction calls for generative / procedural visual motifs rather than a mark. |
| `theme-factory` | **Delegate** | Color tokens and font pairing are exactly what `theme-factory` does. Brand-workshop should emit a `design-system.md` that is *compatible with* theme-factory's token shape, so downstream skills (pitch-deck, business-model-canvas) can skin themselves. |
| `brand-guidelines` | **Keep** | `brand-guidelines` is Anthropic-brand-specific. Not applicable. |
| `pitch-deck` (our own) | **Delegate** | Remove brand-workshop's own `pitch-template.html` generation; instead emit a `brand-kit/` folder and let `pitch-deck` consume it. Reduces duplication. |
| `docx` | **Reference** | If the founder wants the brand brief as a Word document. |

**Action summary:** add `Cross-Skill Integration` section. Audit whether the
`brand-kit/deck/pitch-template.html` output should be replaced by a pointer
to `pitch-deck`. Keep SVG logo generation in-skill (that's the differentiator).

---

### 2. `business-model-canvas`

**What it produces:** `business-model.md` + `business-model.html` (9-block
Osterwalder canvas).

| Official skill | Action | Why |
|---|---|---|
| `theme-factory` | **Delegate** | The HTML canvas should pick up `brand-kit/design-system.md` tokens via theme-factory when present. Today it has minimal styling logic — theme-factory is the right owner. |
| `docx` | **Reference** | For `.docx` export when the founder wants to paste into a board doc. Not default. |
| `web-artifacts-builder` | **Reference** | For interactive canvas variants (filters, block toggling). Out of scope for v1 but natural upgrade path. |
| `pdf` | **Reference** | Print-to-PDF is already handled by the inline HTML — no direct delegation needed, but document that `pdf` is the skill for programmatic PDF manipulation if the founder wants to merge the canvas into a larger packet. |
| `team-composer` (our own) | Already referenced. |

**Action summary:** update the stale `pitch-deck (forthcoming)` row (it now
exists). Add `theme-factory` and `docx` rows to the Cross-Skill Integration
section.

---

### 3. `i18n-contextual-rewriting`

**What it produces:** culturally-authentic translations of i18n resource
files.

| Official skill | Action | Why |
|---|---|---|
| All | **Keep** | No overlap. Official shelf has no translation/i18n skill. This is the purest "keep as-is" in the set. |

**Action summary:** audit pass only. Confirm description is collision-free.
No structural changes expected.

---

### 4. `pitch-deck`

**What it produces:** single self-contained Reveal.js HTML deck +
speaker-notes + investor-readiness checklist.

| Official skill | Action | Why |
|---|---|---|
| `theme-factory` | **Delegate** (already documented) | Theme-factory is the styling owner when no `brand-kit/` is present. |
| `pptx` | **Reference (fallback only)** | Per team-composer's own cross-skill guidance: use `.pptx` *only* when the user explicitly requests it. State the trade-off (loss of interactivity, custom animations, programmable charts). Add a short note in our skill. |
| `canvas-design` | **Reference** | For hero/cover-slide static art that justifies the investment in real design over a chart. |
| `web-artifacts-builder` | **Reference** | When the deck needs shadcn/ui components, routing, or state management — i.e., when the "deck" is actually a product demo. |
| `doc-coauthoring` | **Reference** | For long-form narrative drafts that precede the deck (e.g., founder's memo → deck). |

**Action summary:** the existing `Cross-Skill Integration` table is ~90%
correct. Add `pptx` fallback row and a `canvas-design` row. Do not change
core HTML-first behavior.

---

### 5. `skill-evaluator`

**What it produces:** audit findings on rule adherence for an existing
skill, with proposed rule-text diffs.

| Official skill | Action | Why |
|---|---|---|
| `skill-creator` | **Delegate + Absorb** | This is the highest-overlap relationship in the entire repo. `skill-creator` already ships: *"run evals to test a skill, benchmark skill performance with variance analysis, optimize a skill's description for better triggering accuracy."* Our skill must declare a hard boundary: **evaluator = production-time rule adherence + fix-layer classification**; **skill-creator = build-time benchmarking + description optimization**. The existing SKILL.md already has a `Differentiation from skill-creator` table — we should elevate that boundary to the description field so it fires at trigger time, not after. |
| `consolidate-memory` | **Keep** | Unrelated. |

**Action summary:** tighten the description line to put the boundary clause
earlier and more emphatically. Confirm the existing `Differentiation from
skill-creator` section stays intact. Benchmark trigger accuracy in Phase 3.

---

### 6. `sub-agent-coordinator`

**What it produces:** coordination patterns (fan-out, pipeline, specialist)
and sub-agent briefing templates.

| Official skill | Action | Why |
|---|---|---|
| `skill-creator` | **Reference** | For authoring sub-agent-specific skills. Not a delegation — a pointer. |
| Built-in `Task` / Agent SDK | **Reference (external)** | Not an Anthropic *skill* per se, but the Claude Code Agent SDK + `Task` tool is the runtime this skill advises on. Link to `docs.claude.com` where useful. |

**Action summary:** add a short `Cross-Skill Integration` section. No
structural changes.

---

### 7. `team-composer`

**What it produces:** virtual team assembly + 3-round discussion + optional
audit + deliverable delegation.

| Official skill | Action | Why |
|---|---|---|
| `ui-ux-pro-max` | Already referenced. |
| `theme-factory` | Already referenced. |
| `pptx` | Already referenced as fallback. |
| `web-artifacts-builder` | **Reference (new)** | When the team produces a full-stack demo artifact rather than a deck. Currently not named. |
| `mcp-builder` | **Reference (new)** | When the discussion surfaces that the deliverable requires building an MCP server. |
| `ai-safety-mindset` | **Reference (new)** | When `@ai_safety_specialist` is on the team — point them to the official Anthropic mindset skill for shared vocabulary. |

**Action summary:** extend the existing Cross-Skill Integration table with
the three new rows. No discussion-flow changes.

---

### 8. `tech-stack-recommendations`

**What it produces:** opinionated stack guidance for new projects and
migrations.

| Official skill | Action | Why |
|---|---|---|
| `mcp-builder` | **Reference** | When the stack choice involves whether/how to build an MCP server. Point to mcp-builder for authoring guidance. |
| `web-artifacts-builder` | **Reference** | When the recommendation is to prototype in claude.ai artifacts before committing to a full stack. |
| `doc-coauthoring` | **Reference** | When the founder wants the recommendation written up as an ADR / decision doc. |

**Action summary:** add `Cross-Skill Integration` section with the three
rows above.

---

## Summary table

| Custom skill | Keep | Reference | Delegate | Absorb |
|---|---|---|---|---|
| brand-workshop | — | canvas-design, algorithmic-art, docx | theme-factory, pitch-deck (own) | — |
| business-model-canvas | — | docx, web-artifacts-builder, pdf | theme-factory | — |
| i18n-contextual-rewriting | all | — | — | — |
| pitch-deck | — | pptx, canvas-design, web-artifacts-builder, doc-coauthoring | theme-factory | — |
| skill-evaluator | consolidate-memory | — | skill-creator (benchmarking) | skill-creator (conventions) |
| sub-agent-coordinator | — | skill-creator, Agent SDK | — | — |
| team-composer | — | web-artifacts-builder, mcp-builder, ai-safety-mindset (new) | theme-factory, pptx, ui-ux-pro-max (existing) | — |
| tech-stack-recommendations | — | mcp-builder, web-artifacts-builder, doc-coauthoring | — | — |

## Risks

1. **Chain fragility.** If a referenced official skill isn't installed, the
   user hits a silent dead-end. Every delegation must be paired with a
   graceful fallback paragraph in the SKILL.md.
2. **Trigger collisions.** `pitch-deck` + `brand-workshop` both touch
   "deck". `skill-evaluator` + `skill-creator` both touch "eval / audit a
   skill". Phase 3 benchmark must verify <15% collision rate on paired
   prompts.
3. **Description-length limits.** Adding cross-skill guidance to the
   description field risks blowing the trigger budget. Keep boundary
   clauses ≤ 30 words and prefer the body of the SKILL.md for detailed
   hand-offs.
4. **Upstream drift.** Anthropic's official shelf changes. A reference that
   works today may break silently if an official skill is renamed or
   retired. Add a CI check in a later phase that validates referenced
   skill names exist in the default install.

## Phase plan recap

- **Phase 1 (this doc):** delegation matrix produced and reviewed.
- **Phase 2:** SKILL.md edits per the "Action summary" rows above. Target:
  `brand-workshop`, `business-model-canvas`, `pitch-deck` first (highest
  value). Then `skill-evaluator` description boundary. Then the remaining
  three.
- **Phase 3:** trigger-collision benchmark via `skill-creator`. Gate:
  collision rate <15% on paired prompts.
- **Phase 4:** README update + release.

## Open questions

### Q1 — Paired-prompt A/B trigger testing in `skill-creator` (resolved 2026-04-18)

**Finding:** `skill-creator` does **not** natively support paired-skill
trigger tests. Confidence 0.9 based on reading
`~/.claude/skills/skill-creator/scripts/run_eval.py` and `run_loop.py`.

**Why it can't:**

- `run_eval` / `run_loop` each accept a single `skill_path`.
- Each query is tested by writing one fake command file into
  `.claude/commands/`, invoking `claude -p <query>`, and watching the stream
  for whether Claude invoked `Skill`/`Read` on *that* file. No other
  custom skills are loaded into the subprocess.
- Triggering detection is hard-coded to a single `clean_name` match.
- The blind comparator (`agents/comparator.md`) compares two *outputs* of a
  run — not two competing skills.

**What it *does* give us:**

- One-skill triggerability against a labeled eval set
  (`should_trigger: true|false`), with stratified 60/40 train/test split
  and held-out scoring to avoid overfitting.
- Automatic description rewriting via `improve_description.py` in a loop.

**Recommendation — two paths:**

| Path | Effort | Fidelity | Use when |
|---|---|---|---|
| **A. Run the loop twice** (once per skill) against the *same* cross-labeled eval set, then cross-reference | Low | Biased — each run sees only one skill; measures raw triggerability, not head-to-head selection | Quick Phase 3 pass to sanity-check `skill-evaluator` vs `skill-creator` collision rate |
| **B. Thin wrapper around `run_eval`** that writes *both* skills' command files before spawning `claude -p`, then scores each query as `correct-winner / wrong-winner / both / neither` | ~40 lines Python | Correct — measures actual selection under collision | Before shipping any delegation-matrix change that claims a boundary works |

**Follow-up action:** add Path B to `skill-evaluator`'s roadmap as a real
capability gap it fills — "paired-skill collision harness that wraps
`skill-creator`'s `run_eval` primitives and tracks which of N skills
fires." This isn't duplicating Anthropic's shelf; it's extending it.

### Q2 — Fate of `brand-workshop`'s `brand-kit/deck/` template (resolved 2026-04-18)

**Finding:** Remove both `deck/pitch-template.html` and
`deck/pitch-styles.css` from `brand-workshop`'s output entirely.
`design-system.md` stays as the single source of truth; `pitch-deck`
generates its own CSS from those tokens at render time (same pattern
`business-model-canvas` already uses). Confidence 0.85.

**Evidence:**

- `brand-workshop` today emits two deck files:
  - `pitch-template.html` — self-contained HTML deck where every content
    slot is a literal `[fill in: …]` prompt.
  - `pitch-styles.css` — *byte-for-byte copy* of the `<style>` block from
    the HTML. A `diff -q` verification gate enforces the sync.
- `pitch-deck`'s Phase 1 Step 1 treats them asymmetrically:
  - `pitch-styles.css` — consumed as starting Reveal theme CSS (real reuse).
  - `pitch-template.html` — "layout / class-name reference only. **Do not**
    copy its `[fill in: …]` prompt strings into the generated deck."
- `business-model-canvas` already demonstrates the right pattern:
  read `design-system.md` → substitute tokens into its own HTML template
  at render time → done. No cached CSS intermediate.

**Why full removal beats keeping either file:**

1. **Standalone value to a founder who skips `pitch-deck` is near-zero.**
   A deck with `[fill in: …]` on every slide plus a footnote saying "run
   `pitch-deck` to fill this in" is a notch above a blank Keynote file.
   The founder still has to learn every slide's purpose and police the
   four cardinal sins — which is `pitch-deck`'s job, not a brand-kit
   artifact's job.
2. **Drift hazard.** The `diff -q` gate between HTML `<style>` and
   extracted CSS is maintenance overhead that catches nothing interesting
   — it only exists because both files exist.
3. **One source of truth.** Tokens live in `design-system.md`; rendered
   CSS is a derived artifact that should live with the render-time owner,
   not be cached upstream.
4. **Alignment with our own pattern.** `business-model-canvas` already
   renders its own CSS from tokens without an intermediate file.
   `pitch-deck` should follow suit.

**Concrete edits (Phase 2 follow-up, separate commit):**

*`skills/brand-workshop/SKILL.md`:*
- Remove the entire "Branded Pitch-Deck Template" section (~lines 477–564).
- Remove `/deck/` from the Output Files tree (~lines 595–597).
- Remove the 4 deck-related quality-checklist items (~lines 661–664).
- Remove the "deck template" item from the Minimum viable set priority
  list (~line 601).
- Update the `pitch-deck` row in Cross-Skill Integration: "Produces
  `brand-kit/` which `pitch-deck` consumes for visual tokens
  (`design-system.md`), positioning (`brand-brief.md`), and tagline
  (`descriptions.md`). `pitch-deck` owns all deck-construction logic."

*`skills/pitch-deck/SKILL.md`:*
- Drop items 5 and 6 from Phase 1 Step 1 (the `pitch-styles.css` and
  `pitch-template.html` reads).
- Update the `brand-workshop` row in Cross-Skill Integration to match.
- Add an explicit note: CSS is generated from `design-system.md` tokens
  at render time (same pattern as `business-model-canvas`).

*`skills/brand-workshop/README.md`:*
- Remove the "self-contained branded pitch-deck template" claim from the
  outputs list.

**Risk:** founders who wanted a "quick deck scaffold" lose that output.
Mitigation: brand-workshop still emits `design-system.md` + tagline +
logo + descriptions. For a deck, they run `pitch-deck` (or `team-composer`,
or start from `theme-factory`). This is the correct boundary.

### Q3 — Plugin spec "recommended official skills" declaration (resolved 2026-04-18)

**Finding:** No, the plugin spec does not support declaring "recommended
official skills." Confidence 0.9 based on
[`/en/plugins-reference`](https://code.claude.com/docs/en/plugins-reference)
and [`/en/plugin-dependencies`](https://code.claude.com/docs/en/plugin-dependencies).

**What `plugin.json` does support:**

- A top-level `dependencies` array — each entry is either a plugin name
  string or `{ name, version, marketplace? }`. `version` accepts npm semver
  ranges (`~2.1.0`, `^2.0`, `>=1.4`, `=2.1.0`).
- Resolution against git tags `{plugin-name}--v{version}` on the marketplace
  repo.
- Cross-marketplace dependencies, if the target marketplace is allowlisted
  in our `marketplace.json`.
- Auto-install at install time; failure disables the dependent plugin with
  one of: `dependency-version-unsatisfied`, `no-matching-tag`, or
  `range-conflict`.

**What it does *not* support:**

| Capability | Supported? |
|---|---|
| Hard-require another marketplace plugin with semver range | Yes — `dependencies` |
| Hard-require an Anthropic-bundled official skill (`skill-creator`, `theme-factory`, etc.) | **No** — those aren't marketplace plugins |
| Recommend / suggest / soft-depend on another plugin | **No** — no `recommends`/`suggests`/`peer`/`optional` field |
| Recommend specific *skills within* another plugin | **No** — dependency granularity is plugin-level |

**Why we can't use `dependencies` for the delegation matrix:** the official
shelf skills (`skill-creator`, `theme-factory`, `docx`, `pptx`, `pdf`,
`canvas-design`, `algorithmic-art`, `web-artifacts-builder`, `mcp-builder`,
`brand-guidelines`, `doc-coauthoring`, `ui-ux-pro-max`, `ai-safety-mindset`,
`consolidate-memory`, `schedule`, `setup-cowork`) are part of the Claude
Code default install. They show up in `<available_skills>` without a
`plugin:` namespace prefix. There's no marketplace repo with `{name}--v{version}`
git tags for the resolver to target.

**Recommendation — keep doing what we're already doing:**

1. **README expectations.** Document "this plugin works best when these
   official skills are present" in `agent-skills/README.md` (already added
   in Phase 2 — the "Delegate to Anthropic's official shelf" principle).
2. **`Cross-Skill Integration` table in each SKILL.md.** Already added /
   updated in Phase 2 for `brand-workshop`, `business-model-canvas`,
   `pitch-deck`. Remaining custom skills get this in a future Phase 2.5.
3. **Graceful-degradation paragraph in each SKILL.md.** Already added in
   Phase 2 — this is the only real safety net if a referenced official
   skill isn't installed.

**Future-proofing:** if Anthropic ever publishes the official shelf as
installable marketplace plugins (e.g., an `anthropic/skills` marketplace),
revisit and add hard `dependencies`. Worth tracking, not betting on.

**Side discovery worth filing for later:** the `dependencies` field is
useful within our *own* marketplace if we ever split this repo into
multiple plugins. For example, if `pitch-deck` were extracted into its
own plugin, `brand-workshop` could declare
`dependencies: [{ "name": "pitch-deck", "version": "^1.0" }]` and the
install flow would auto-install `pitch-deck`. Defer to a future
"split-the-repo" decision.
